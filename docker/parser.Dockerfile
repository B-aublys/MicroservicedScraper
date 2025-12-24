FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY parser/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy parser module
COPY parser/ ./parser/

# Expose gRPC port
EXPOSE 50051

# Run the parser service
CMD ["python", "-m", "parser"]
