"""
Fallback LLM implementation using transformers directly
Use this if GGUF conversion doesn't work
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

class FinancialLLMFallback:
    def __init__(self, model_path="model/ollama_models/TinyLlama-1.1B-Financial-LoRA"):
        """
        Initialize the Financial LLM using transformers directly
        
        Args:
            model_path: Path to the fine-tuned model directory
        """
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Using device: {self.device}")
        print("Loading model and tokenizer...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # Try to load the model with different configurations
            try:
                # First try: Load with quantization config but force CPU
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True,
                    device_map="auto" if self.device == "cpu" else None,
                )
            except Exception as e1:
                print(f"First loading attempt failed: {e1}")
                try:
                    # Second try: Load without quantization
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_path,
                        torch_dtype=torch.float16,
                        low_cpu_mem_usage=True,
                        load_in_8bit=False,
                        load_in_4bit=False,
                    )
                except Exception as e2:
                    print(f"Second loading attempt failed: {e2}")
                    # Third try: Load with minimal configuration
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_path,
                        low_cpu_mem_usage=True,
                    )
            
            # Move to device
            if self.device != "cpu":
                self.model = self.model.to(self.device)
            
            print(f"Model loaded on {self.device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Trying to load base model instead...")
            
            # Try loading the base model
            try:
                base_model_path = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
                print(f"Loading base model: {base_model_path}")
                self.tokenizer = AutoTokenizer.from_pretrained(base_model_path)
                self.model = AutoModelForCausalLM.from_pretrained(
                    base_model_path,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True,
                ).to(self.device)
                print(f"Base model loaded on {self.device}")
            except Exception as e2:
                print(f"Failed to load base model: {e2}")
                raise

    def generate(self, prompt: str) -> str:
        """
        Generates a response from the financial LLM using the provided prompt.
        
        Args:
            prompt: The input prompt for the model
            
        Returns:
            The generated response as a string
        """
        # Format the prompt for the model
        formatted_prompt = f"""<|system|>
You are a helpful financial analyst assistant. Provide clear, professional responses based *only* on the context provided. Do not use any prior knowledge. If the context is insufficient, say you cannot answer.
<|user|>
{prompt}
<|assistant|>
"""
        
        try:
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.15,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()
            
            # Handle cases where the model generates an empty response or just control tokens
            if response.startswith('<') and response.endswith('>'):
                return "The model returned a control token, which may indicate an issue with the prompt or generation."

            return response
            
        except Exception as e:
            print(f"Error during generation: {e}")
            return f"An error occurred during text generation: {str(e)}"

# Example usage
if __name__ == '__main__':
    try:
        llm = FinancialLLMFallback()
        example_prompt = "User Question: What is the outlook for NVDA stock?\n\nContext:\nTitle: NVIDIA Announces New AI Chip\nNVIDIA today announced the H200, its next-generation AI chip, which is expected to double the inference speed of the previous H100 model. Major cloud providers have already signed on to use the new chip."
        
        response = llm.generate(example_prompt)
        print("\n--- LLM Response ---")
        print(response)
        print("--- End of Response ---")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nThis fallback implementation uses transformers directly.")
        print("It's slower than llama.cpp but should work with your quantized model.") 