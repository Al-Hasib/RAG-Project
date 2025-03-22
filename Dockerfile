# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the project directory to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements_dev.txt

EXPOSE 8000
# Set the default command to run the application (modify as needed)
CMD ["uvicorn", "app:app", "--server.address", "0.0.0.0", "--server.port", "8000"]
