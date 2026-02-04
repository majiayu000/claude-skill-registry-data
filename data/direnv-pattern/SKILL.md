---
name: direnv-pattern
description: |
  Implements the b00t environment management pattern: direnv → .envrc → dotenv → .env
  where datums specify WHICH environment variables are required and .env contains
  the actual secret VALUES. Ensures automatic environment loading per-project.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash
---

## What This Skill Does

The b00t direnv pattern provides secure, automatic environment variable management for projects. This skill helps you:

- Set up direnv + .envrc + .env configuration
- Follow the b00t pattern: WHICH (datums) vs VALUES (.env)
- Validate environment variables before execution
- Support multiple environments (dev, staging, prod)
- Integrate with b00t datum system

## When It Activates

Activate this skill when you see phrases like:

- "setup environment variables"
- "configure direnv"
- "create .envrc file"
- "add API keys"
- "environment not loading"
- "missing environment variables"
- "configure .env file"
- "setup direnv pattern"

## The b00t Pattern Flow

```
Developer enters directory
    ↓
direnv detects .envrc file
    ↓
.envrc calls: dotenv
    ↓
dotenv loads .env file
    ↓
Environment variables available
    ↓
Rust validates via datum
    ↓
✅ Agent runs
```

## Key Principles

1. **Datums specify WHICH** - `~/.dotfiles/_b00t_/*.ai.toml` files specify required variable names
2. **`.env` contains VALUES** - Actual API keys and secrets (gitignored)
3. **`direnv` loads automatically** - No manual `source` or `export` needed
4. **Rust validates** - Via PyO3 bindings, DRY approach

## File Structure

```
project/
├── .envrc              # ← Loaded by direnv (calls dotenv)
├── .env                # ← Contains actual API keys (GITIGNORED!)
├── .envrc.example      # ← Template for .envrc (committed)
├── .env.example        # ← Shows required keys (committed)
└── .gitignore          # ← Must include .env and .envrc
```

## Setup Instructions

### 1. Install direnv

```bash
# macOS
brew install direnv

# Ubuntu/Debian
sudo apt-get install direnv

# Add to shell (choose one):
# bash:
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# zsh:
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# fish:
echo 'direnv hook fish | source' >> ~/.config/fish/config.fish
```

### 2. Create .envrc

```bash
# b00t direnv configuration
# This file demonstrates the b00t pattern: direnv → .envrc → dotenv → .env

# Load project .env file (contains API keys)
dotenv

# Optionally load home directory .env for global keys
# dotenv ~/.env

# Optionally load environment-specific configs
# dotenv .env.local
# dotenv .env.development
```

### 3. Create .env with API Keys

```bash
# OpenRouter (200+ models via single API)
OPENROUTER_API_KEY=sk-or-v1-abc123...

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-api03-xyz789...

# OpenAI
OPENAI_API_KEY=sk-proj-def456...

# HuggingFace
HF_TOKEN=hf_ghi789...

# Groq (ultra-fast inference)
GROQ_API_KEY=gsk_jkl012...
```

### 4. Allow direnv

```bash
direnv allow
```

### 5. Verify Setup

```bash
# Check environment variables are loaded
echo $OPENROUTER_API_KEY

# Test with Python
python3 -c "import os; print('✅ Loaded' if os.getenv('OPENROUTER_API_KEY') else '❌ Not loaded')"
```

## .envrc.example Template

```bash
# b00t direnv configuration
# Setup:
#   1. Copy: cp .envrc.example .envrc
#   2. Copy: cp .env.example .env
#   3. Edit .env with your actual API keys
#   4. Enable: direnv allow

# Load project .env file (contains API keys)
dotenv

# Optionally load home directory .env for global keys
# dotenv ~/.env

# Optionally load environment-specific configs
# dotenv .env.local

# Layout python - ensures direnv works with Python virtual environments
# Uncomment if using a venv:
# layout python python3.12
```

## .env.example Template

```bash
# b00t Environment Configuration
# ==========================================
# API keys are loaded via direnv → .envrc → dotenv → .env pattern.
#
# Setup:
#   1. Copy: cp .env.example .env
#   2. Fill in your actual API keys in .env
#   3. Enable: direnv allow (after copying .envrc.example to .envrc)
#
# The b00t pattern:
#   - Datums (~/.dotfiles/_b00t_/*.ai.toml) specify WHICH vars are required
#   - This .env file contains the actual VALUES
#   - direnv loads them automatically when entering the directory

# OpenAI (gpt-4, gpt-3.5-turbo, etc.)
# OPENAI_API_KEY=sk-proj-...

# Anthropic (claude-3.5-sonnet, claude-3-opus, etc.)
# ANTHROPIC_API_KEY=sk-ant-api03-...

# Google Gemini
# GOOGLE_API_KEY=...

# Groq (llama-3.1, mixtral, etc.)
# GROQ_API_KEY=gsk_...

# OpenRouter (200+ models via single API)
# OPENROUTER_API_KEY=sk-or-...

# HuggingFace
# HF_TOKEN=hf_...

# Ollama (local models)
# OLLAMA_BASE_URL=http://localhost:11434
```

## Integration with Datums

### Provider Datum Example

```toml
[env]
# Required: Must be present in .env file
required = ["OPENROUTER_API_KEY"]

# Optional: Default values for non-secret configuration
defaults = { OPENROUTER_API_BASE = "https://openrouter.ai/api/v1" }
```

### Validation in Python

```python
import b00t_py
import os

# Ensure direnv loaded the environment
assert os.getenv('OPENROUTER_API_KEY'), "Run 'direnv allow' first!"

# Validate via datum system
validation = b00t_py.check_provider_env("openrouter", "~/.dotfiles/_b00t_")

if validation["available"]:
    print("✅ OpenRouter environment ready")
else:
    print(f"❌ Missing: {validation['missing_env_vars']}")
    print("Add them to your .env file and run 'direnv allow'")
```

## Advanced Patterns

### Multiple Environment Files

Load both global and project-specific keys:

```bash
# .envrc
# Load global keys from home directory
dotenv ~/.env

# Load project-specific keys (can override global)
dotenv
```

### Environment-Specific Configuration

```bash
# .envrc
# Load base environment
dotenv

# Load environment-specific overrides
if [ "$ENVIRONMENT" = "production" ]; then
    dotenv .env.production
elif [ "$ENVIRONMENT" = "staging" ]; then
    dotenv .env.staging
else
    dotenv .env.development
fi
```

### Custom Validation in .envrc

```bash
#!/usr/bin/env bash

# Load environment
dotenv

# Validate required keys are present
required_vars=("OPENROUTER_API_KEY" "ANTHROPIC_API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing: $var"
        echo "   Add it to your .env file"
        return 1
    fi
done

echo "✅ All required environment variables loaded"
```

## Security Best Practices

### ✅ DO

- ✅ Add `.env` to `.gitignore`
- ✅ Add `.envrc` to `.gitignore` (committed: `.envrc.example`)
- ✅ Use `.env.example` as template (committed to git)
- ✅ Store API keys only in `.env` files
- ✅ Use `direnv allow` to load environment per-project
- ✅ Validate environment variables before use

### ❌ DON'T

- ❌ Commit `.env` files to git
- ❌ Commit `.envrc` with secrets to git
- ❌ Hard-code API keys in source code
- ❌ Store secrets in datum TOML files
- ❌ Share `.env` files via chat/email
- ❌ Use production keys in examples

## .gitignore Configuration

```gitignore
# Environment files (secrets)
.env
.envrc
.env.local
.env.*.local

# Keep examples (templates)
!.env.example
!.envrc.example
```

## Troubleshooting

### Variables Not Loading

```bash
# Check if direnv is hooked
direnv status

# Re-allow .envrc
direnv allow

# Check what direnv loaded
direnv export bash | grep API_KEY
```

### Missing Required Variables

```python
import b00t_py

# List available providers
providers = b00t_py.list_ai_providers("~/.dotfiles/_b00t_")
print(f"Available: {providers}")

# Check specific provider
validation = b00t_py.check_provider_env("openrouter", "~/.dotfiles/_b00t_")
if not validation["available"]:
    print(f"Missing: {validation['missing_env_vars']}")
```

### Permission Denied

```bash
# Re-allow
direnv allow

# Check .envrc syntax
bash -n .envrc
```

## CI/CD Integration

For environments where direnv isn't available:

```yaml
# .gitlab-ci.yml
variables:
  OPENROUTER_API_KEY: ${CI_OPENROUTER_API_KEY}

test:
  script:
    - python3 -m pytest
```

```yaml
# .github/workflows/test.yml
env:
  OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: python3 -m pytest
```

## Workflow

### Initial Setup

1. **Install direnv** and add shell hook
2. **Copy templates**: `.envrc.example` → `.envrc`, `.env.example` → `.env`
3. **Edit .env** with actual API keys
4. **Run `direnv allow`**
5. **Verify** with `echo $API_KEY` or Python

### Adding New Keys

1. **Add to .env.example** (commented, as template)
2. **Add to .env** (actual value)
3. **Update datum** to specify required key
4. **Run `direnv allow`** if .envrc changed

### Per-Project Configuration

1. **Navigate to project**: `cd /path/to/project`
2. **Create .envrc**: Reference `.envrc.example`
3. **Create .env**: Reference `.env.example`
4. **Allow**: `direnv allow`
5. **Test**: Python imports should have env vars

## Related Skills

- **datum-system**: Specifies WHICH env vars are required
- **dry-philosophy**: Rust validates env, Python just uses it
- **justfile-usage**: Add environment setup commands

## References

- `b00t-j0b-py/docs/ENVIRONMENT_SETUP.md` - Complete guide
- `b00t-j0b-py/.envrc.example` - Template
- `b00t-j0b-py/.env.example` - API keys template
- `b00t-py/src/lib.rs` - PyO3 validation functions

## Summary

The b00t direnv pattern provides:

1. **DRY**: Single source of truth for requirements (datums)
2. **Secure**: Secrets in `.env` (gitignored), not in code
3. **Automatic**: `direnv` loads environment on `cd`
4. **Validated**: Rust checks required vars before execution
5. **Flexible**: Supports multiple `.env` files, local/global keys
