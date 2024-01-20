# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY event-stream-consumer-requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r event-stream-consumer-requirements.txt

COPY event-stream-consumer.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "./event-stream-consumer.py"]
