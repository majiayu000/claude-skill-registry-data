---
name: github-deploy
description: Deploy GitHub repositories to remote servers via SSH. Claude reads the README, understands build/start instructions, and executes deployment commands over SSH. Supports rollback on failure.
---

# GitHub Deploy Skill

Deploy GitHub repositories to remote servers. Claude handles the entire workflow: fetching the README, understanding build instructions, and executing deployment via SSH.

## Prerequisites

### 1. Claude.ai Network Allowlist (User must configure)

The user must add these to their project's allowed domains:
- `api.github.com` (for gh CLI)
- Server hostname or IP (for SSH outbound connections)

### 2. GitHub Token (User provides)

Claude should ask the user for their GitHub PAT if not already available.

### 3. SSH Key (User provides)

Claude should ask the user for their SSH private key to connect to the server.

---

## Claude's Setup Steps

When a user requests a deployment, Claude should:

### Step 1: Install SSH client

```bash
apt-get update && apt-get install -y openssh-client
```

### Step 2: Ask user for required information

Claude asks the user:
1. **GitHub repo** - "Which repository do you want to deploy?" (e.g., `owner/repo`)
2. **Server** - "What's the SSH connection string?" (e.g., `user@server.com`)
3. **SSH key** - "Please paste your SSH private key for the server"
4. **Deploy path** (optional) - "Where should I deploy? (default: `/opt/<repo-name>`)"
5. **GitHub token** (if private repo) - "Please provide your GitHub PAT"

### Step 3: Save SSH key securely

Once the user provides the key, Claude saves it:

```bash
cat << 'EOF' > /tmp/deploy_key
<paste user's key here>
EOF
chmod 600 /tmp/deploy_key
```

### Step 4: Set up environment

```bash
export GH_TOKEN="<user's token>"
SSH_CMD="ssh -i /tmp/deploy_key -o StrictHostKeyChecking=no <user@server>"
```

### Step 5: Test connection

```bash
$SSH_CMD "echo '✅ Connected successfully'"
```

---

## Deployment Workflow

Claude follows these steps:

### Step 1: Fetch and Read README

```bash
gh api repos/OWNER/REPO/contents/README.md --jq '.content' | base64 -d
```

Claude reads the output and identifies:
- Build commands (install dependencies, compile, etc.)
- Start command (how to run the application)
- Environment variables needed
- Any special requirements

### Step 2: Detect Project Type

Check for project files to determine build system:

```bash
gh api repos/OWNER/REPO/contents --jq '.[].name'
```

See `references/build-patterns.md` for detection patterns.

### Step 3: SSH to Server and Deploy

```bash
SSH_CMD="ssh -i /tmp/deploy_key -o StrictHostKeyChecking=no user@server"

# Test connection
$SSH_CMD "echo 'Connected successfully'"

# Set deploy path
DEPLOY_PATH="/opt/app"  # or user-specified path
REPO_URL="https://github.com/OWNER/REPO.git"
# For private repos with token:
REPO_URL="https://${GH_TOKEN}@github.com/OWNER/REPO.git"
```

### Step 4: Clone or Update Repository

```bash
$SSH_CMD << 'DEPLOY'
set -e
DEPLOY_PATH="/opt/app"
REPO_URL="https://github.com/OWNER/REPO.git"

if [ -d "$DEPLOY_PATH/.git" ]; then
    echo "📦 Updating existing repo..."
    cd "$DEPLOY_PATH"
    git rev-parse HEAD > .last-good-commit
    git pull
else
    echo "📦 Cloning repo..."
    mkdir -p "$(dirname $DEPLOY_PATH)"
    git clone "$REPO_URL" "$DEPLOY_PATH"
    cd "$DEPLOY_PATH"
    git rev-parse HEAD > .last-good-commit
fi
DEPLOY
```

### Step 5: Build

Based on README analysis, run appropriate build commands:

```bash
$SSH_CMD << 'BUILD'
set -e
cd /opt/app

# Example for Node.js
npm install
npm run build

# Example for Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Example for Rust
cargo build --release
BUILD
```

### Step 6: Start Application

```bash
$SSH_CMD << 'START'
cd /opt/app

# Stop existing process if any (example patterns)
pkill -f "node server.js" || true
pkill -f "python main.py" || true

# Start in background with nohup
nohup npm start > app.log 2>&1 &
# or
nohup python main.py > app.log 2>&1 &

echo "✅ Application started"
START
```

### Step 7: Verify (Optional)

If a health check endpoint is known:

```bash
$SSH_CMD "sleep 3 && curl -s http://localhost:3000/health || echo 'No health check'"
```

## Rollback on Failure

If any step fails:

```bash
$SSH_CMD << 'ROLLBACK'
set -e
cd /opt/app

if [ -f .last-good-commit ]; then
    echo "⚠️ Rolling back to last good commit..."
    git checkout $(cat .last-good-commit)
    
    # Re-run build (adjust based on project type)
    npm install
    
    # Restart
    pkill -f "node server.js" || true
    nohup npm start > app.log 2>&1 &
    
    echo "✅ Rollback complete"
else
    echo "❌ No rollback point available"
fi
ROLLBACK
```

## Example Full Deployment

User request: "Deploy github.com/acme/webapp to user@prod.server.com"

Claude executes:

```bash
# Setup
export GH_TOKEN="..."
SSH_CMD="ssh -i /tmp/deploy_key -o StrictHostKeyChecking=no user@prod.server.com"

# 1. Read README
gh api repos/acme/webapp/contents/README.md --jq '.content' | base64 -d

# 2. Claude analyzes: "This is a Node.js app. Build: npm install && npm run build. Start: npm start"

# 3. Deploy
$SSH_CMD << 'EOF'
set -e
cd /opt || mkdir -p /opt

if [ -d /opt/webapp/.git ]; then
    cd /opt/webapp
    git rev-parse HEAD > .last-good-commit
    git pull
else
    git clone https://github.com/acme/webapp.git /opt/webapp
    cd /opt/webapp
    git rev-parse HEAD > .last-good-commit
fi

npm install
npm run build

pkill -f "node" || true
nohup npm start > app.log 2>&1 &
echo "✅ Deployed successfully"
EOF
```

## Security Notes

- SSH keys are stored temporarily in `/tmp/` and should be removed after use
- For private repos, the GitHub token is embedded in the clone URL
- Use `StrictHostKeyChecking=no` only if acceptable; otherwise verify host keys manually first
- Consider using deploy keys with limited repo access instead of full PATs

## Environment Variables

Pass environment variables to the remote server:

```bash
$SSH_CMD << EOF
export NODE_ENV=production
export PORT=3000
export DATABASE_URL="postgres://..."

cd /opt/app
nohup npm start > app.log 2>&1 &
EOF
```

Or create a `.env` file:

```bash
$SSH_CMD "cat > /opt/app/.env << 'ENVFILE'
NODE_ENV=production
PORT=3000
ENVFILE"
```
