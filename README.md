# Disaster-Recovery Playbook

## Prerequisites
- SSH key configured
- Docker & NVIDIA drivers installed

## Quickstart
\`\`\`bash
git clone git@github.com:DigitalMith/ai-repo.git
cd ai-repo
./deploy.sh
\`\`\`

## Model Downloads
\`\`\`bash
mkdir -p models/Meta-Llama-3-8B
# wget or gsutil cp your model weights here
\`\`\`

## Troubleshooting Tips
- Check GPU: \`nvidia-smi\`
- View logs: \`docker-compose logs -f llama3-webui\`
- Find port conflicts: \`lsof -i :7860\`
