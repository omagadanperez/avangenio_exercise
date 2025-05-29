# Use official Python 3.8.10 image as base
FROM python:3.8.10

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file to install dependencies
COPY requirements.txt .

# Upgrade pip to the latest version before installing dependencies
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire server project directory into the container
COPY . .

# Expose port 8000 to allow communication to/from the container
EXPOSE 8000

# Run the server script when the container starts
CMD ["python", "server.py"]