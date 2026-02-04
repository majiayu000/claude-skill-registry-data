---
name: session-start-hook
description: Configure SessionStart hooks for Claude Code on the web. Use when setting up a repository to run on cloud infrastructure, installing dependencies, or initializing environments for remote Claude Code sessions.
---

# SessionStart Hook Configuration

Configure your repository for Claude Code on the web using SessionStart hooks. This skill helps you create hooks that automatically run when Claude Code starts a session in the cloud environment.

## Overview

**SessionStart hooks** execute when Claude Code begins a session, allowing you to:
- Install project dependencies (npm, pip, etc.)
- Set up environment variables
- Configure databases or services
- Run initialization scripts
- Validate the environment

## Quick Setup

### 1. Create the settings file

Create `.claude/settings.json` in your repository root:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/claude-setup.sh",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### 2. Create the setup script

Create `scripts/claude-setup.sh`:

```bash
#!/bin/bash
set -e

# Detect package manager and install dependencies
if [ -f "package.json" ]; then
    if [ -f "pnpm-lock.yaml" ]; then
        pnpm install
    elif [ -f "yarn.lock" ]; then
        yarn install
    elif [ -f "bun.lockb" ]; then
        bun install
    else
        npm install
    fi
fi

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

if [ -f "pyproject.toml" ]; then
    if command -v uv &> /dev/null; then
        uv sync
    elif command -v poetry &> /dev/null; then
        poetry install
    else
        pip install -e .
    fi
fi

exit 0
```

### 3. Make the script executable

```bash
chmod +x scripts/claude-setup.sh
```

## Hook Configuration Reference

### Basic Structure

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "<pattern>",
        "hooks": [
          {
            "type": "command",
            "command": "<script-or-command>",
            "timeout": <seconds>,
            "statusMessage": "<optional-message>"
          }
        ]
      }
    ]
  }
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `matcher` | Optional | Pattern to match (use "startup" for all sessions) |
| `type` | Yes | Must be "command" |
| `command` | Yes | Shell command or script path |
| `timeout` | Optional | Max execution time in seconds (default: 60) |
| `statusMessage` | Optional | Message shown during execution |

## Environment Detection

### Detect Web vs Local Execution

The `CLAUDE_CODE_REMOTE` environment variable indicates cloud execution:

```bash
#!/bin/bash

# Run only in web/cloud environment
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
    echo "Skipping - not running in cloud environment"
    exit 0
fi

# Cloud-specific setup here
npm install
```

### Run Only Locally

```bash
#!/bin/bash

# Skip in cloud environment
if [ "$CLAUDE_CODE_REMOTE" = "true" ]; then
    exit 0
fi

# Local-only setup here
```

## Persisting Environment Variables

Write to `$CLAUDE_ENV_FILE` to set environment variables for the session:

```bash
#!/bin/bash

# Set environment variables for Claude Code
echo "DATABASE_URL=postgresql://localhost:5432/mydb" >> "$CLAUDE_ENV_FILE"
echo "NODE_ENV=development" >> "$CLAUDE_ENV_FILE"
echo "API_KEY=test-key" >> "$CLAUDE_ENV_FILE"
```

## Common Setup Patterns

### Node.js Project

```bash
#!/bin/bash
set -e

# Install dependencies
npm install

# Build if needed
if [ -f "tsconfig.json" ]; then
    npm run build 2>/dev/null || true
fi

# Set up environment
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi

exit 0
```

### Python Project

```bash
#!/bin/bash
set -e

# Create virtual environment if needed
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate and install
source .venv/bin/activate
pip install -r requirements.txt

# Set environment variables
echo "PYTHONPATH=$(pwd)" >> "$CLAUDE_ENV_FILE"

exit 0
```

### Full-Stack Application

```bash
#!/bin/bash
set -e

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Database
cd ..
if command -v docker &> /dev/null; then
    docker-compose up -d db redis 2>/dev/null || true
fi

exit 0
```

### Ruby Project

```bash
#!/bin/bash
set -e

# Set Ruby version if .ruby-version exists
if [ -f ".ruby-version" ]; then
    rbenv local $(cat .ruby-version) 2>/dev/null || true
fi

# Install gems
bundle install

exit 0
```

### Go Project

```bash
#!/bin/bash
set -e

# Download dependencies
go mod download

# Build to verify
go build ./... 2>/dev/null || true

exit 0
```

## Cloud Environment Details

### Pre-installed Tools

The Claude Code web environment includes:
- **Languages**: Python 3.x, Node.js (LTS), Ruby 3.x, Go, Rust, Java, PHP
- **Package Managers**: npm, yarn, pnpm, bun, pip, poetry, uv, gem, bundler, cargo
- **Databases**: PostgreSQL 16, Redis 7.0
- **Build Tools**: gcc, clang, make, cmake

Check available tools with: `check-tools`

### Network Access

Limited network access by default. Allowed domains include:
- Package registries (npm, PyPI, RubyGems, crates.io, etc.)
- GitHub, GitLab, Bitbucket
- Cloud providers (GCP, Azure, AWS)
- Container registries

## Troubleshooting

### Script Not Executing

1. Verify script is executable: `chmod +x scripts/claude-setup.sh`
2. Check shebang line: `#!/bin/bash`
3. Ensure script exits with 0 on success

### Dependencies Not Installing

1. Check network access allows required domains
2. Use explicit package managers instead of auto-detection
3. Add `set -e` to fail fast on errors

### Environment Variables Not Set

1. Write to `$CLAUDE_ENV_FILE`, not `export`
2. Use append (`>>`) not overwrite (`>`)
3. Verify file path: `echo "VAR=value" >> "$CLAUDE_ENV_FILE"`

## Templates

See `templates/` directory for ready-to-use setup scripts:
- `templates/nodejs-setup.sh` - Node.js/TypeScript projects
- `templates/python-setup.sh` - Python projects
- `templates/fullstack-setup.sh` - Full-stack applications

## Related Resources

- [Claude Code on the Web documentation](https://docs.anthropic.com/en/docs/claude-code/code-on-the-web)
- [Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Settings Reference](https://docs.anthropic.com/en/docs/claude-code/settings)
