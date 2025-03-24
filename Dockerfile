# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the project directory to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements_dev.txt

EXPOSE 5000

ENV FLASK_APP=flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Default command to run the Flask application
CMD ["flask", "run"]
