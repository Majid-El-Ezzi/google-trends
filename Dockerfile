# 1. Use an official Python runtime as a base image
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy requirements first (for efficient caching)
COPY requirements.txt .

# 4. Install Python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# install netcat
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*


# 5. Copy the rest of the app’s code
COPY . .

# 6. make script executable
RUN chmod +x wait-for-db.sh

# 7. Command to run the application
CMD ["./wait-for-db.sh"]     
