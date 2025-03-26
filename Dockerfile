# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the project directory to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements_dev.txt

# Expose ports for Flask and FastAPI
EXPOSE 5000 8000

# Set environment variables
ENV FLASK_APP=flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run both Flask and FastAPI using Supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy the Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Command to run Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
