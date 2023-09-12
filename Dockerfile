# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for whisper
RUN apt-get update && apt-get install -y ffmpeg

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install package for Whisper
RUN pip install "git+https://github.com/openai/whisper.git"

# Download whisper model
RUN whisper "sample1.mp3" --model small --model_dir /whisper-model

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run uvicorn to start the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]