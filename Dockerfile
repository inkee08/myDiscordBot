# DockerfileCopy code# Base image
FROM python:3.11

# Working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Command to start the server
CMD ["python", "bot.py"]