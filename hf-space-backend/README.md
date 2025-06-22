# Hugging Face Space: Financial Investment Analyzer API

This Space exposes a FastAPI API for financial news analysis using a finetuned TinyLlama model.

## Endpoints
- `POST /analyze_investment`  
  **Body:** `{ "ticker": "MSFT", "question": "What are the latest developments for Microsoft regarding AI?" }`  
  **Returns:** LLM analysis and retrieved context.

## Running Locally
```bash
uvicorn app:app --reload
```

## Environment Variables
- `POLYGON_API_KEY` (required for real-time news ingestion)

## Deploying to Hugging Face Spaces
1. Create a new Space (FastAPI SDK).
2. Push this code and the `src/`, `config/`, and `model/` folders as needed.
3. Set your environment variables in the Space settings.

--- 