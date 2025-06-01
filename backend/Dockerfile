# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /backend

# Copy requirements files
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy backend source code
COPY . .

# Set Python path and expose port
ENV PYTHONPATH=/backend
EXPOSE 8000

# Run the FastAPI application
CMD ["python", "src/main/main.py"]
