import os
from typing import Optional
from llama_cpp import Llama

class FinancialLLM:
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the Financial LLM using llama.cpp
        
        Args:
            model_path: Path to the GGUF model file. If None, will look for common paths.
        """
        if model_path is None:
            # Look for GGUF model in common locations
            possible_paths = [
                "model/gguf_models/TinyLlama-1.1B-Financial-LoRA_f16.gguf",  # User's downloaded model
                "model/financial_model.gguf",  # Direct GGUF from Kaggle
                "model/TinyLlama-1.1B-Financial.gguf",
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if model_path is None:
                raise FileNotFoundError(
                    "No GGUF model found. Please:\n"
                    "1. Download your GGUF model from Kaggle\n"
                    "2. Place it in the model/gguf_models/ directory\n"
                    "3. Name it 'TinyLlama-1.1B-Financial-LoRA_f16.gguf' or specify the model_path parameter\n"
                    "4. The model should be converted to GGUF format on Kaggle during fine-tuning"
                )
        
        print(f"Loading model from: {model_path}")
        print("Using llama.cpp for inference...")
        
        # Initialize llama.cpp model
        self.model = Llama(
            model_path=model_path,
            n_ctx=2048,  # Context window
            n_threads=os.cpu_count(),  # Use all CPU threads
            n_gpu_layers=0,  # Set to > 0 if you have GPU support
            verbose=False
        )
        
        print("Model loaded successfully!")

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
            # Generate response using llama.cpp
            response = self.model(
                formatted_prompt,
                max_tokens=512,
                temperature=0.7,
                top_p=0.9,
                repeat_penalty=1.15,
                stop=["<|user|>", "<|system|>", "<|end|>"],
                echo=False
            )
            
            # Extract the generated text
            generated_text = response['choices'][0]['text'].strip()
            
            # Clean up the response
            if "<|assistant|>" in generated_text:
                generated_text = generated_text.split("<|assistant|>")[-1].strip()
            
            # Handle empty or control token responses
            if not generated_text or (generated_text.startswith('<') and generated_text.endswith('>')):
                return "The model returned an empty response or control token. Please try rephrasing your question."
            
            return generated_text
            
        except Exception as e:
            print(f"Error during generation: {e}")
            return f"An error occurred during text generation: {str(e)}"

# Example usage
if __name__ == '__main__':
    try:
        llm = FinancialLLM()
        example_prompt = "User Question: What is the outlook for NVDA stock?\n\nContext:\nTitle: NVIDIA Announces New AI Chip\nNVIDIA today announced the H200, its next-generation AI chip, which is expected to double the inference speed of the previous H100 model. Major cloud providers have already signed on to use the new chip."
        
        response = llm.generate(example_prompt)
        print("\n--- LLM Response ---")
        print(response)
        print("--- End of Response ---")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTo use this model, you need to:")
        print("1. Convert your fine-tuned model to GGUF format on Kaggle")
        print("2. Download the GGUF file from Kaggle")
        print("3. Place it in the model/ directory as 'financial_model.gguf'")
        print("4. Or specify the model_path parameter with the correct path") 