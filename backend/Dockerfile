FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY app /app

# Environment
ENV PYTHONUNBUFFERED=1

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]