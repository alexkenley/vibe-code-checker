#!/bin/bash
# Vibe Code Scanner - Docker Wrapper Script for Linux/Mac

if [ -z "$1" ]; then
  echo "Error: Please provide a path to the project you want to scan."
  echo "Usage: ./docker-scan.sh /path/to/your/project [optional: -l language]"
  exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Error: Docker is not installed or not in your PATH."
  echo "Please install Docker from https://www.docker.com/products/docker-desktop"
  exit 1
fi

# Get absolute path to the project
PROJECT_PATH=$(realpath "$1")
echo "Project path: $PROJECT_PATH"

# Build the Docker image if it doesn't exist
if ! docker image inspect vibe-code-scanner &> /dev/null; then
  echo "Building Docker image for Vibe Code Scanner..."
  docker build -t vibe-code-scanner .
fi

# Run the scanner in Docker
echo "Running Vibe Code Scanner in Docker..."
docker run --rm -v "$PROJECT_PATH:/code" vibe-code-scanner /code "${@:2}"

echo "Scan complete!"
