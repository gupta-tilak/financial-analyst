Note: when you download the fine tuned LoRA adapters, you need to run merge_lora_for_ollama.py for merging the base model with the LoRA adapter weights.

1. Start the api service : python3 simple_api.py
2. Send the POST request with the prompt : curl -X POST http://localhost:5001/analyze -H "Content-Type: application/json" -d '{"prompt": "How do interest rate changes affect stock market valuations?"}'