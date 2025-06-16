"""Simplified LoRA training for college project"""

import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer
from datasets import load_dataset
import config.settings as config

class FinancialModelTrainer:
    def __init__(self):
        self.model_name = "meta-llama/Llama-2-7b-hf"  # More suitable base model
        self.tokenizer = None
        self.model = None
        
    def setup_model(self):
        """Setup model with quantization for efficiency"""
        # Use 4-bit quantization for memory efficiency
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto"
        )
        
    def create_lora_config(self):
        """Create LoRA configuration"""
        return LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=16,  # Moderate rank as per roadmap
            lora_alpha=16,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Attention blocks
            lora_dropout=0.1,
            bias="none",
            inference_mode=False
        )
        
    def prepare_dataset(self):
        """Create comprehensive financial dataset"""
        financial_data = [
            {
                "instruction": "Analyze the P/E ratio of AAPL",
                "response": "Let me analyze Apple's P/E ratio. First, I'll check the current stock price and earnings per share. Then, I'll compare it with industry peers and historical trends to provide a comprehensive analysis."
            },
            {
                "instruction": "What are the key risks in the current market?",
                "response": "I'll analyze several key risk factors: 1) Market volatility based on recent trends, 2) Economic indicators and their implications, 3) Sector-specific risks, and 4) Global market conditions."
            },
            {
                "instruction": "Explain the impact of recent SEC filings on MSFT",
                "response": "I'll analyze Microsoft's recent SEC filings by: 1) Reviewing key financial metrics, 2) Identifying significant changes in operations, 3) Assessing risk factors, and 4) Evaluating management's discussion of business conditions."
            },
            {
                "instruction": "Provide an investment thesis for GOOGL",
                "response": "Let me develop a comprehensive investment thesis for Alphabet by analyzing: 1) Core business metrics and growth, 2) Competitive advantages, 3) Market position, 4) Financial health, and 5) Future growth opportunities."
            }
        ]
        
        def format_prompt(example):
            return f"""### Instruction: {example['instruction']}

### Response: {example['response']}

### Analysis:
This response demonstrates proper financial analysis by:
1. Breaking down complex financial concepts
2. Providing structured analysis
3. Considering multiple factors
4. Maintaining professional tone
5. Focusing on actionable insights"""
            
        return [{"text": format_prompt(item)} for item in financial_data]
        
    def train_model(self):
        """Train the model with LoRA"""
        print("Setting up model...")
        self.setup_model()
        
        print("Applying LoRA...")
        lora_config = self.create_lora_config()
        self.model = get_peft_model(self.model, lora_config)
        
        print("Preparing dataset...")
        dataset = self.prepare_dataset()
        
        print("Starting training...")
        training_args = TrainingArguments(
            output_dir=config.FINE_TUNED_MODEL_PATH,
            per_device_train_batch_size=config.BATCH_SIZE,
            num_train_epochs=2,
            learning_rate=config.LEARNING_RATE,
            logging_steps=10,
            save_steps=100,
            warmup_steps=50,
        )
        
        trainer = SFTTrainer(
            model=self.model,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            args=training_args,
            max_seq_length=config.MAX_LENGTH,
        )
        
        trainer.train()
        trainer.save_model()
        print(f"✅ Model saved to {config.FINE_TUNED_MODEL_PATH}")
