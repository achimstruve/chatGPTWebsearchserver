FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variable to run the API
ENV RUN_API=true

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"] 