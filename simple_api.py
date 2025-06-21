#!/usr/bin/env python3
"""
Simple API using the financial analyst model directly with Hugging Face
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from flask import Flask, request, jsonify

app = Flask(__name__)

# Determine device
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

# Load model and tokenizer
print("Loading model...")
model_path = "model/ollama_models/TinyLlama-1.1B-Financial-LoRA"
tokenizer = AutoTokenizer.from_pretrained(model_path)
# Load model on CPU first, then move to MPS to avoid issues with device_map="auto"
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
).to(device)
print(f"Model loaded on {device}")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    # Format the prompt
    formatted_prompt = f"""<|system|>
You are a helpful financial analyst assistant. Provide clear, professional responses using standard ASCII characters. Avoid special Unicode characters and focus on delivering accurate financial analysis.
<|user|>
{prompt}
<|assistant|>
"""
    
    # Tokenize and ensure it's on the same device as the model
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.15,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the assistant's response
    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[-1].strip()
    
    return jsonify({"response": response})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting API server...")
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False) 