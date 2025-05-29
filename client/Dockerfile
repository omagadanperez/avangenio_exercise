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

# Copy the entire client project directory into the container
COPY . .

# Set environment variables if needed
ENV SERVER_HOST=server
ENV SERVER_PORT=8000

# Expose the port that Flask will listen on (default is 5000, change if needed)
EXPOSE 5000

# Run the Flask app (web.py) when the container starts
CMD ["python", "web.py"]

# Run the client script with arguments when the container starts
#CMD ["python", "client.py", "--num_strings", "100", "--output_file", "data/chains.txt", "--response_file", "data/responses.txt"]