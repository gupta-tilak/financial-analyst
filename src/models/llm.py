import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class FinancialLLM:
    def __init__(self, model_path="model/ollama_models/TinyLlama-1.1B-Financial-LoRA"):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Using device: {self.device}")

        print("Loading model and tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        ).to(self.device)
        print(f"Model loaded on {self.device}")

    def generate(self, prompt: str) -> str:
        """
        Generates a response from the financial LLM using the provided prompt.
        """
        # We reuse the prompt structure from the InvestmentAnalyzer.
        # It already includes the user question and the retrieved context.
        formatted_prompt = f"""<|system|>
You are a helpful financial analyst assistant. Provide clear, professional responses based *only* on the context provided. Do not use any prior knowledge. If the context is insufficient, say you cannot answer.
<|user|>
{prompt}
<|assistant|>
"""
        
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

# Example usage
if __name__ == '__main__':
    llm = FinancialLLM()
    example_prompt = "User Question: What is the outlook for NVDA stock?\n\nContext:\nTitle: NVIDIA Announces New AI Chip\nNVIDIA today announced the H200, its next-generation AI chip, which is expected to double the inference speed of the previous H100 model. Major cloud providers have already signed on to use the new chip."
    
    response = llm.generate(example_prompt)
    print("\n--- LLM Response ---")
    print(response)
    print("--- End of Response ---") 