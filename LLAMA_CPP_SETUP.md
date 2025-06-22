# Llama.cpp Setup Guide

This guide explains how to use llama.cpp for running your fine-tuned financial model on macOS.

## Why Llama.cpp?

- **Better quantized model support**: Llama.cpp handles quantized weights from LoRA fine-tuning much better than Ollama
- **Native macOS support**: Optimized for Apple Silicon and Intel Macs
- **Lower memory usage**: More efficient inference
- **No server required**: Runs directly in your Python process

## Recommended Workflow (Kaggle → Local)

Since quantization conversion requires GPU access, the recommended approach is:

### 1. On Kaggle (during fine-tuning):
```python
# After your LoRA fine-tuning is complete
# Convert to GGUF format directly on Kaggle
!git clone https://github.com/ggerganov/llama.cpp.git
!cd llama.cpp && python convert_hf_to_gguf.py /path/to/your/fine_tuned_model --outfile financial_model.gguf --outtype q4_k_m

# The GGUF file will be available in your Kaggle outputs
```

### 2. On your local machine:
1. Download the GGUF model from Kaggle outputs
2. Place it in your `model/` directory as `financial_model.gguf`
3. Install dependencies: `pip install -r requirements.txt`
4. Test the model: `python -m src.models.llm`

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download GGUF Model

Download your GGUF model from Kaggle and place it in:
```
model/financial_model.gguf
```

### 3. Test the Model

```bash
python -m src.models.llm
```

### 4. Run Analysis

```bash
python -m src.analysis.investment_analyzer
```

## File Structure

Your model directory should look like:

```
model/
├── financial_model.gguf  # Downloaded from Kaggle
└── ...
```

## Troubleshooting

### Model Not Found

If the model isn't found automatically, specify the path:

```python
from src.models.llm import FinancialLLM

llm = FinancialLLM(model_path="path/to/your/model.gguf")
```

### Performance Issues

- **CPU threads**: The model uses all available CPU threads by default
- **GPU layers**: Set `n_gpu_layers` > 0 if you have GPU support
- **Context window**: Adjust `n_ctx` based on your needs (default: 2048)

## Configuration Options

You can customize the llama.cpp model initialization:

```python
self.model = Llama(
    model_path=model_path,
    n_ctx=2048,           # Context window size
    n_threads=8,          # Number of CPU threads
    n_gpu_layers=0,       # GPU layers (0 for CPU only)
    verbose=False         # Verbose output
)
```

## Benefits of This Setup

1. **No Ollama dependency**: Runs independently
2. **Better quantized model support**: Handles your LoRA fine-tuned model properly
3. **Faster inference**: Optimized C++ implementation
4. **Lower memory usage**: More efficient than transformers
5. **Cross-platform**: Works on macOS, Linux, and Windows
6. **Simplified workflow**: No local conversion needed

## Fallback Mode

If llama.cpp doesn't work, the system automatically falls back to using transformers directly. This is slower but should work with your quantized model.

## Next Steps

1. Convert your model to GGUF on Kaggle during fine-tuning
2. Download the GGUF file from Kaggle
3. Place it in the model/ directory
4. Test with: `python -m src.models.llm`
5. Run analysis: `python -m src.analysis.investment_analyzer`

## Support

If you encounter issues:

1. Check the error messages in the console
2. Verify your model path is correct
3. Ensure all dependencies are installed
4. Make sure the GGUF file is not corrupted 