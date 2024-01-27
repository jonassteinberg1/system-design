# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file
COPY publisher2-requirements.txt ./

# Install any necessary dependencies
RUN pip install --no-cache-dir -r publisher2-requirements.txt

# Copy the publisher script to the container
COPY publisher2.py .

# no buffer ==> get logs immediately
ENV PYTHONUNBUFFERED=1

# Command to run when starting the container
CMD ["python", "./publisher2.py"]

