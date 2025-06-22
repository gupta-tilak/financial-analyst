FROM python:3.10-slim

# Set workdir
WORKDIR /code

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port (the default for Spaces is 7860, but FastAPI uses 8000 by default)
EXPOSE 7860

# Run FastAPI app with uvicorn on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]