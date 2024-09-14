# Base image with Python 3.x
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's source code
COPY . .

# Set the entry point for the bot
CMD ["python", "main.py"]
