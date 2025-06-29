#!/bin/bash

set -e  # Exit on error

echo "🔄 Updating system packages..."
sudo apt-get update

echo "🧼 Removing any old Docker versions..."
sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

echo "📦 Installing dependencies..."
sudo apt-get install -y ca-certificates curl gnupg lsb-release

echo "🔐 Adding Docker's official GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "📂 Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "🔄 Updating package list after adding Docker repo..."
sudo apt-get update

echo "🐳 Installing Docker and Docker Compose V2..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin git

echo "👤 Adding current user to Docker group..."
sudo usermod -aG docker "$USER"

echo "🔁 Restarting Docker service..."
sudo systemctl restart docker

# Step 6: Clone the repo if not already cloned
REPO_DIR="Assignment_Cyfuture"
REPO_URL="git@github.com:TanmayAT/Assignment_Cyfuture.git"

if [ ! -d "$REPO_DIR" ]; then
  echo "📥 Cloning the repository via SSH..."
  git clone "$REPO_URL"
else
  echo "Pulling latest changes from the repository..."
  cd "$REPO_DIR"
  git pull origin main
  

fi

# Step 7: Enter repo and update
cd "$REPO_DIR"
echo "📦 Switching to main branch and pulling latest changes..."
git checkout main
git pull origin main

# Step 8: Build and run containers
echo "🚀 Building and running Docker containers..."
docker compose up -d --build

echo "✅ Done! You may need to run 'newgrp docker' or restart the terminal for Docker group changes to take effect."
