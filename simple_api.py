#!/usr/bin/env python3
"""
Simple API using the financial analyst model with llama.cpp support
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Try to import the llama.cpp version first, fallback to transformers if needed
try:
    from src.models.llm import FinancialLLM
    LLM_CLASS = FinancialLLM
    print("Using llama.cpp-based LLM implementation")
except ImportError as e:
    print(f"llama.cpp LLM not available: {e}")
    try:
        from src.models.llm_fallback import FinancialLLMFallback
        LLM_CLASS = FinancialLLMFallback
        print("Using transformers-based LLM fallback")
    except ImportError as e2:
        print(f"Fallback LLM also not available: {e2}")
        raise ImportError("No LLM implementation available")

# Initialize LLM with error handling
try:
    llm = LLM_CLASS()
    print("LLM initialized successfully")
except Exception as e:
    print(f"Error initializing LLM: {e}")
    print("Trying fallback implementation...")
    try:
        from src.models.llm_fallback import FinancialLLMFallback
        llm = FinancialLLMFallback()
        print("Fallback LLM initialized successfully")
    except Exception as e2:
        print(f"Fallback also failed: {e2}")
        raise Exception("Could not initialize any LLM implementation")

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Generate response using the LLM
        response = llm.generate(prompt)
        
        return jsonify({"response": response})
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "llm_type": "llama.cpp" if "FinancialLLM" in str(type(llm)) else "transformers"
    })

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    try:
        model_path = getattr(llm, 'model_path', 'Unknown')
        return jsonify({
            "model_type": "llama.cpp" if "FinancialLLM" in str(type(llm)) else "transformers",
            "model_path": model_path,
            "status": "loaded"
        })
    except Exception as e:
        return jsonify({
            "model_type": "unknown",
            "error": str(e),
            "status": "error"
        })

if __name__ == '__main__':
    print("Starting API server...")
    print("Available endpoints:")
    print("- POST /analyze - Analyze financial data")
    print("- GET /health - Check API health")
    print("- GET /model_info - Get model information")
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False) 