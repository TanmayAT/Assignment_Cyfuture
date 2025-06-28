#!/bin/bash

set -e  # Exit on any error

# Step 1: Update package list
echo "Updating packages..."
sudo apt-get update

# Step 2: Install Docker and Docker Compose
echo "Installing Docker and Docker Compose..."
sudo apt-get install -y docker.io docker-compose

# Step 3: Add current user to Docker group
echo "Adding current user to Docker group..."
sudo usermod -aG docker $USER

# Step 4: Restart Docker
echo "Restarting Docker..."
sudo systemctl restart docker

# Step 5: Clone the repo via SSH if not already cloned
REPO_DIR="Assignment_Cyfuture"
REPO_URL="git@github.com:TanmayAT/Assignment_Cyfuture.git"

if [ ! -d "$REPO_DIR" ]; then
  echo "Cloning the repository via SSH..."
  git clone "$REPO_URL"
else
  echo "Repository already cloned."
fi

# Step 6: Navigate to repo and update
cd "$REPO_DIR"
echo "Switching to main branch and pulling latest changes..."
git checkout main
git pull origin main

# Step 7: Build and run containers
echo "Building and running containers..."
docker-compose up -d --build
