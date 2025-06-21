#!/usr/bin/env python3
"""
Script to merge LoRA adapter with base model in FP16 format for Ollama compatibility
"""

import os
import torch
import gc
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Configuration
BASE_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
NEW_MODEL_NAME = "TinyLlama-1.1B-Financial-LoRA"

def save_for_ollama_properly():
    """Save unquantized model for Ollama compatibility"""
    
    print("Loading base model in FP16 for Ollama compatibility...")
    
    # Load base model WITHOUT quantization (FP16)
    base_model_fp16 = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float16,  # Use FP16, not quantized
        device_map="auto",
        low_cpu_mem_usage=True
    )
    
    # Load your LoRA adapter onto the FP16 base model
    lora_path = os.path.join(os.getcwd(), "model", "saved_models", NEW_MODEL_NAME)
    print(f"Loading LoRA adapter from: {lora_path}")
    
    model_with_lora = PeftModel.from_pretrained(
        base_model_fp16,
        lora_path
    )
    
    # Now merge and unload - this will be FP16, not quantized
    merged_model_fp16 = model_with_lora.merge_and_unload()
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
    
    # Create output directory
    output_dir = os.path.join(os.getcwd(), "model", "ollama_models", NEW_MODEL_NAME)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the FP16 merged model for Ollama
    merged_model_fp16.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"✅ FP16 model saved to {output_dir}")
    print("This model is compatible with Ollama (no U8 quantization)")
    
    # Clean up memory
    del base_model_fp16, model_with_lora, merged_model_fp16
    torch.cuda.empty_cache()
    gc.collect()

if __name__ == "__main__":
    print("Starting LoRA merge for Ollama compatibility...")
    save_for_ollama_properly()
    print("✅ Merge completed successfully!")
    print("\nNext steps:")
    print("1. Your Modelfile should now work with the merged model")
    print("2. Run: ollama create financial-analyst -f model/Modelfile") 