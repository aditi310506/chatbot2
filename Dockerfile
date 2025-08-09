# Use a slim Python image for a smaller container
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 8080

# Define the command to run your application
CMD ["python", "app.py"]