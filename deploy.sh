#!/usr/bin/env bash
set -e

# 1. Clone or update repo
if [ -d ai-repo ]; then
  cd ai-repo && git pull
else
  git clone git@github.com:DigitalMith/ai-repo.git
  cd ai-repo
fi

# 2. Ensure Docker & NVIDIA setup
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker

# 3. Launch services
docker-compose pull
docker-compose up -d

# 4. Verify
echo "Waiting for services to spin up…"
sleep 5
curl --silent http://localhost:7860 | grep -q "Text-Generation WebUI" && \
  echo "✅ UI is live at http://<your_server_ip>:7860" || \
  echo "⚠️ Something went wrong—check docker logs"
