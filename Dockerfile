# 1. Use an official Python runtime as a base image
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy requirements first (for efficient caching)
COPY requirements.txt .

# 4. Install Python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the app’s code
COPY . .

# 6. Define the command to run your app
CMD ["python", "app/main.py"]
