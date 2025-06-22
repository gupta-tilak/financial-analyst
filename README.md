Note: Download the GGUF fine tuned model from Kaggle and place it model/gguf_models

To test the model follow below :
1. Start the api service : python3 simple_api.py
2. Send the POST request with the prompt : curl -X POST http://localhost:5001/analyze -H "Content-Type: application/json" -d '{"prompt": "How do interest rate changes affect stock market valuations?"}'

To test the Investment Analyzer :
1. PYTHONPATH=. python3 src/analysis/investment_analyzer.py