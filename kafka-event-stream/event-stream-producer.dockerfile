# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY event-stream-producer-requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r event-stream-producer-requirements.txt

# Copy the script and wait-for-it
COPY event-stream-producer.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "./event-stream-producer.py"]
