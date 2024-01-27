# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file
COPY subscriber1-requirements.txt ./

# Install any necessary dependencies
RUN pip install --no-cache-dir -r subscriber1-requirements.txt

# Copy the subscriber script to the container
COPY subscriber1.py .

# no buffer ==> get logs immediately
ENV PYTHONUNBUFFERED=1

# Command to run when starting the container
CMD ["python", "./subscriber1.py"]

