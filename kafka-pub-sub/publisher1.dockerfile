# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file
COPY publisher1-requirements.txt ./

# Install any necessary dependencies
RUN pip install --no-cache-dir -r publisher1-requirements.txt

# Copy the publisher script to the container
COPY publisher1.py .

# no buffer ==> get logs immediately
ENV PYTHONUNBUFFERED=1

# Command to run when starting the container
CMD ["python", "./publisher1.py"]

