#!/bin/bash

# Build workflow for yx-cc tool
# This script clones the repo, installs uv, and installs the tool globally
# Install YX-CC

set -e

REPO_URL="https://ghfast.top/https://github.com/DylanLIiii/claude-code-yx-action.git"
REPO_DIR="yx-cc"

echo "=== Building yx-cc workflow ==="

# Step 1: Clone the repository
echo "1. Cloning repository..."
if [ -d "$REPO_DIR" ]; then
    echo "Repository directory already exists, removing it..."
    rm -rf "$REPO_DIR"
fi
git clone "$REPO_URL" "$REPO_DIR"
cd "$REPO_DIR"

# Step 2: Install uv using Python
echo "2. Installing uv..."
python -m pip install uv

# Step 3: Use uv to install the tool globally
echo "3. Installing yx-cc globally..."
uv tool install .

uv tool update-shell

source /root/.bashrc

echo "=== Build completed successfully ==="
echo "You can now use the tool with: yx-cc -h"

# Install Claude Code and Set Base URL and 

npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com

## Set Claude Code Base URL 

(cat ~/.claude.json 2>/dev/null || echo 'null') | jq --arg key "${ANTHROPIC_API_KEY: -20}" '(. // {}) | .customApiKeyResponses.approved |= ([.[]?, $key] | unique)' > ~/.claude.json.tmp && mv ~/.claude.json.tmp ~/.claude.json