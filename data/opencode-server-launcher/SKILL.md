---
name: opencode-server-launcher
description: Launch and manage OpenCode servers with simple commands, from single instances to multi-server swarms
version: 1.0.0
author: Claude
tags: [opencode, server, launch, setup, swarm]
---

# OpenCode Server Launcher

Simple commands and scripts to launch and manage OpenCode servers, from single instances to multi-server swarms.

**UNIVERSAL CAPABILITY**: This skill launches servers for ANY agent type, not just the examples shown. The agent folder names (code-analyzer, documentation-writer, etc.) used in examples are for illustration ONLY. Real swarms will have completely different agent types and purposes. This skill works universally with any folder structure and any agent specialization.

## Quick Start

**IMPORTANT: Create custom agents in `.opencode/agent/` BEFORE launching the server. Agents are only loaded when the server starts.**

### Basic Server Launch
```bash
# Start server on random available port
opencode serve

# Start server on specific port
opencode serve --port 3000

# Start server on all interfaces
opencode serve --port 3000 --hostname 0.0.0.0
```

### Verify Server is Running
```bash
# Check server status
curl http://localhost:3000/config

# View available agents
curl http://localhost:3000/agent | jq .

# Check API documentation
curl http://localhost:3000/doc
```

## Multi-Server Setup

### Launch Multiple Servers
```bash
# Server 1 - General purpose
opencode serve --port 3001 &
SERVER1_PID=$!

# Server 2 - Build focused
opencode serve --port 3002 &
SERVER2_PID=$!

# Server 3 - Documentation focused
opencode serve --port 3003 &
SERVER3_PID=$!

echo "Started servers: $SERVER1_PID, $SERVER2_PID, $SERVER3_PID"
```

### Folder-Specific Server Launch (Swarm-Ready)

For swarm deployment, launch servers in specific folders:

**⚠️ EXAMPLE PATTERN ONLY - The folder names below are EXAMPLES. Use ANY folder names for your actual swarm:**

```bash
# EXAMPLE: Launch server in [ANY_AGENT_FOLDER] folder
cd [agent_folder_name]
opencode serve --port 3001 &
SERVER1_PID=$!
cd ..

# EXAMPLE: Launch server in [DIFFERENT_AGENT_FOLDER] folder
cd [another_agent_folder]
opencode serve --port 3002 &
SERVER2_PID=$!
cd ..

# EXAMPLE: Launch server in [THIRD_AGENT_FOLDER] folder
cd [third_agent_folder]
opencode serve --port 3003 &
SERVER3_PID=$!
cd ..
```

**UNIVERSAL TRUTH**: The pattern works for ANY folder names:
- `marketing-specialist/` → `cd marketing-specialist`
- `legal-advisor/` → `cd legal-advisor`
- `game-developer/` → `cd game-developer`
- `research-scientist/` → `cd research-scientist`
- `music-composer/` → `cd music-composer`
- `personal-trainer/` → `cd personal-trainer`

**REAL SWARMS WILL HAVE VASTLY DIFFERENT FOLDER NAMES** - These examples only show the launching pattern.

**Process Management:**
- Store PIDs for later management: `echo "3001:[folder_name]:$SERVER1_PID" >> .opencode/server-pids.txt`
- Stop servers: `kill $SERVER1_PID`
- Check if running: `kill -0 $SERVER1_PID`

**NOTE**: Replace `[folder_name]` with your actual folder names. The pattern `port:folder:pid` works for ANY folder names.

## Server Configuration

### Environment Variables
```bash
# Set log level
export OPENCODE_LOG_LEVEL=debug

# Set custom config directory
export OPENCODE_CONFIG_DIR=/path/to/config

# Set API keys for providers
export ANTHROPIC_API_KEY=your-key
export ZHIPU_API_KEY=your-key
```

### Configuration Files
OpenCode automatically loads configuration from:
- Global: `~/.config/opencode/`
- Project: `.opencode/` (in project root)

### Agent Configuration
Custom agents go in `.opencode/agent/`:

```markdown
---
description: Specialized agent for documentation
mode: subagent
tools:
  read: true
  grep: true
permissions:
  edit: allow
  bash:
    "git*": allow
    "*": ask
---

You are an expert technical documentation writer...
```

## Basic API Usage

### Create Session
```bash
curl -X POST http://localhost:3000/session \
  -H "Content-Type: application/json" \
  -d '{"title": "My Development Session"}'
```

### Send Message
```bash
curl -X POST http://localhost:3000/session/{session_id}/message \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "general",
    "model": {"providerID": "zai-coding-plan", "modelID": "glm-4.6"},
    "parts": [{"type": "text", "text": "Help me understand this codebase"}]
  }'
```

### List Sessions
```bash
curl http://localhost:3000/session | jq '.'
```

### Read Files
```bash
curl "http://localhost:3000/file/content?path=README.md"
```

## Swarm Health Monitoring

### Health Check
```bash
# Check multiple servers
for port in 3001 3002 3003; do
    if curl -s "http://localhost:$port/config" > /dev/null; then
        echo "✅ Server on port $port - HEALTHY"
    else
        echo "❌ Server on port $port - DOWN"
    fi
done
```

### Monitor Active Sessions
```bash
for port in 3001 3002 3003; do
    if curl -s "http://localhost:$port/config" > /dev/null; then
        sessions=$(curl -s "http://localhost:$port/session" | jq '. | length')
        echo "Port $port: $sessions active sessions"
    fi
done
```

## Production Deployment

### Docker Setup
```dockerfile
# Dockerfile
FROM node:18-alpine

RUN npm install -g opencode-ai

EXPOSE 3000

CMD ["opencode", "serve", "--port", "3000", "--hostname", "0.0.0.0"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  opencode-1:
    build: .
    ports:
      - "3001:3000"
    environment:
      - OPENCODE_LOG_LEVEL=info
    volumes:
      - ./config:/app/.opencode

  opencode-2:
    build: .
    ports:
      - "3002:3000"
    environment:
      - OPENCODE_LOG_LEVEL=info
    volumes:
      - ./config:/app/.opencode
```

## Best Practices

### Security
```bash
# Use API keys
export OPENCODE_API_KEY=your-secure-key

# Restrict access to localhost
opencode serve --hostname 127.0.0.1

# Use reverse proxy for SSL
# Configure nginx/cloudflare for HTTPS
```

### Performance
```bash
# Set appropriate log levels
export OPENCODE_LOG_LEVEL=warn

# Monitor server resources
curl http://localhost:3000/config | jq '.providers'
```

### Port Management
```bash
# Find available port
python -c "import socket; s=socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()"

# Kill process using port
lsof -ti:3000 | xargs kill -9
```

## Troubleshooting

### Common Issues
```bash
# Check if port is available
netstat -tulpn | grep :3000

# Kill existing server
pkill -f "opencode serve"

# Test server response
curl -v http://localhost:3000/config
```

This skill provides everything needed to launch, configure, and manage OpenCode servers from basic single instances to multi-server swarms, all using simple commands and tools that are already available.