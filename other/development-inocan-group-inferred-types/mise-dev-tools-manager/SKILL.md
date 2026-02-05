---
name: Mise Dev Tools Manager
description: Manage dev tools, runtime versions, environment variables, and tasks with mise. Universal tool version manager supporting 1000+ tools with task runner and env management.
---

## Overview
Mise is a polyglot tool version manager and task runner that replaces tools like asdf, nvm, pyenv, rbenv, and more. It manages development tool versions, environment variables, and project tasks—all from a single fast CLI with support for 1000+ tools.

## Key Features
- **Universal tool management**: One tool to manage Node.js, Python, Ruby, Go, Java, and 1000+ others
- **Lightning fast**: Written in Rust, up to 2-3x faster than asdf
- **Environment management**: Project-specific environment variables
- **Task runner**: Built-in task runner (like make/npm scripts but better)
- **Compatible**: Works with asdf plugins and .tool-versions files
- **Cross-platform**: Works on Linux, macOS, and Windows

## Installation

### Quick Install
```bash
# Linux/macOS
curl https://mise.run | sh

# macOS (Homebrew)
brew install mise

# Cargo
cargo install mise

# Verify installation
mise --version
```

### Shell Setup
After installation, add mise to your shell:

```bash
# Bash
echo 'eval "$(mise activate bash)"' >> ~/.bashrc

# Zsh
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc

# Fish
echo 'mise activate fish | source' >> ~/.config/fish/config.fish

# Restart shell or source the config
source ~/.bashrc  # or ~/.zshrc, etc.
```

## Quick Start

### Install a tool
```bash
# Install Node.js
mise install node@20

# Install Python
mise install python@3.12

# Install latest version
mise install node@latest
```

### Set project versions
```bash
# Set local (project) version
mise use node@20
mise use python@3.12

# Set global (system) version
mise use -g node@20
```

### Run a task
```bash
# List available tasks
mise tasks

# Run a task
mise run test
mise run build
```

## Tool Management

### Installing Tools

```bash
# Install specific version
mise install node@20.11.0
mise install python@3.12.1

# Install latest version
mise install node@latest
mise install python@latest

# Install from .mise.toml or .tool-versions
mise install

# List available versions
mise ls-remote node
mise ls-remote python
```

### Using Tools

```bash
# Set for current project (creates/updates .mise.toml)
mise use node@20
mise use python@3.12
mise use terraform@1.6

# Set globally for all projects
mise use -g node@20

# Set and pin to exact version
mise use node@20.11.0

# Set multiple tools at once
mise use node@20 python@3.12
```

### Listing Tools

```bash
# List installed tools for current project
mise list
mise ls

# List all installed tools globally
mise list --global

# List available tools
mise plugins ls-remote

# Check what tools are available
mise registry
```

### Updating Tools

```bash
# Update to latest version
mise upgrade node
mise upgrade python

# Update all tools
mise upgrade

# Update mise itself
mise self-update
```

### Removing Tools

```bash
# Uninstall a version
mise uninstall node@18

# Remove from current project
mise rm node
```

## Configuration Files

### .mise.toml (Recommended)

Create a `.mise.toml` in your project root:

```toml
[tools]
node = "20"
python = "3.12"
terraform = "1.6"
go = "1.22"

[env]
DATABASE_URL = "postgres://localhost/mydb"
API_KEY = "dev-key-123"
NODE_ENV = "development"

[tasks.test]
run = "pytest tests/"
description = "Run Python tests"

[tasks.lint]
run = ["eslint .", "black --check ."]
description = "Run linters"

[tasks.dev]
run = "npm run dev"
description = "Start development server"
```

### .tool-versions (Legacy)

Compatible with asdf format:

```
node 20.11.0
python 3.12.1
terraform 1.6.0
```

### Version Syntax

```toml
[tools]
node = "20"           # Latest 20.x
node = "20.11"        # Latest 20.11.x
node = "20.11.0"      # Exact version
node = "latest"       # Latest stable
python = "3.12"       # Latest 3.12.x
```

## Environment Variables

### Setting Variables

```toml
# In .mise.toml
[env]
DATABASE_URL = "postgres://localhost/mydb"
API_KEY = { file = ".env.local" }  # Load from file
PATH = ["./node_modules/.bin", "$PATH"]  # Prepend to PATH
```

### Using Templates

```toml
[env]
PROJECT_ROOT = "{{ cwd }}"
CONFIG_PATH = "{{ config_root }}/config"
HOME_DIR = "{{ env.HOME }}"
```

### Per-Environment Config

```bash
# Load different configs based on MISE_ENV
mise use --env production node@20
mise use --env development node@18

# Set environment
export MISE_ENV=production
```

## Task Runner

### Defining Tasks

```toml
# Simple task
[tasks.test]
run = "pytest tests/"

# Task with options
[tasks.build]
run = "npm run build"
description = "Build for production"
depends = ["lint", "test"]

# Multiple commands
[tasks.deploy]
run = [
  "npm run build",
  "aws s3 sync dist/ s3://my-bucket",
  "aws cloudfront create-invalidation --distribution-id XXX --paths '/*'"
]

# Task with arguments
[tasks.db-migrate]
run = "python manage.py migrate {{ arg(name='env', default='dev') }}"

# Task with environment variables
[tasks.test-e2e]
run = "playwright test"
env = { CI = "true", HEADLESS = "true" }
```

### Running Tasks

```bash
# Run a task
mise run test
mise run build

# Run with arguments
mise run db-migrate -- production

# List all tasks
mise tasks
mise tasks --json

# Run multiple tasks
mise run lint test build

# Run task from specific config
mise run -C /path/to/project test
```

### Task Dependencies

```toml
[tasks.deploy]
run = "kubectl apply -f k8s/"
depends = ["test", "build"]

[tasks.test]
run = "pytest tests/"

[tasks.build]
run = "docker build -t myapp ."
```

When you run `mise run deploy`, it will run `test` and `build` first.

### Watching for Changes

```toml
[tasks.dev]
run = "npm run dev"
sources = ["src/**/*.ts", "package.json"]
outputs = ["dist/**/*"]
```

Mise will track changes and only run when sources change.

## Common Workflows

### 1. Starting a New Project

```bash
# Initialize project with tools
cd my-project
mise use node@20 python@3.12

# This creates .mise.toml:
# [tools]
# node = "20"
# python = "3.12"

# Install the tools
mise install

# Verify
mise list
node --version
python --version
```

### 2. Cloning an Existing Project

```bash
# Clone project
git clone https://github.com/example/project
cd project

# Install all tools from .mise.toml
mise install

# Run project setup
mise run setup
```

### 3. Adding Environment Variables

```bash
# Edit .mise.toml
[env]
DATABASE_URL = "postgres://localhost/mydb"
REDIS_URL = "redis://localhost:6379"
API_KEY = "dev-key-123"

# Variables are automatically loaded when you cd into the directory
cd my-project
echo $DATABASE_URL  # postgres://localhost/mydb
```

### 4. Setting Up Tasks

```toml
# .mise.toml
[tasks.setup]
run = [
  "npm install",
  "python -m pip install -r requirements.txt",
  "cp .env.example .env"
]
description = "Setup project dependencies"

[tasks.dev]
run = "npm run dev"
description = "Start development server"

[tasks.test]
run = ["npm test", "pytest tests/"]
description = "Run all tests"

[tasks.format]
run = ["prettier --write .", "black ."]
description = "Format code"
```

```bash
# Use the tasks
mise run setup
mise run dev
mise run test
```

### 5. Managing Multiple Node.js Versions

```bash
# Install multiple versions
mise install node@18 node@20 node@21

# Set different versions per project
cd project-a && mise use node@18
cd project-b && mise use node@20

# Use temporary version for a command
mise exec node@21 -- node script.js
```

### 6. Language-Specific Package Managers

```bash
# Install language package managers
mise install node@20        # Includes npm
mise install python@3.12    # Includes pip
mise install ruby@3.3       # Includes gem

# They're automatically available
npm install
pip install requests
gem install rails
```

## Advanced Features

### Trust Configuration

Mise prompts before loading new configs for security:

```bash
# Trust a config
mise trust

# Trust and install
mise install

# Auto-trust all configs (use with caution)
mise settings set trusted_config_paths "~/.config/mise"
```

### Global Configuration

Edit `~/.config/mise/config.toml`:

```toml
[settings]
experimental = true
verbose = true

[tools]
node = "20"
python = "3.12"

[env]
EDITOR = "vim"
```

### Using Profiles

```bash
# Set up profiles
mise use --profile work node@20
mise use --profile personal node@18

# Switch profiles
export MISE_PROFILE=work
```

### Cache Management

```bash
# Clear plugin cache
mise cache clear

# Show cache location
mise cache show

# Clean old versions
mise prune
```

### Hook Scripts

```toml
# Run scripts on certain events
[hooks]
enter = "echo 'Entering project'"
leave = "echo 'Leaving project'"
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: CI
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: jdx/mise-action@v2
        with:
          version: latest

      - run: mise install

      - run: mise run test
      - run: mise run build
```

### Docker

```dockerfile
FROM ubuntu:22.04

# Install mise
RUN curl https://mise.run | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy config
COPY .mise.toml .
RUN mise install

# Run tasks
CMD ["mise", "run", "start"]
```

### GitLab CI

```yaml
image: ubuntu:22.04

before_script:
  - curl https://mise.run | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - mise install

test:
  script:
    - mise run test
```

## Best Practices

### 1. Commit Configuration

Always commit `.mise.toml` or `.tool-versions`:

```bash
git add .mise.toml
git commit -m "Add mise configuration"
```

This ensures all team members use the same tool versions.

### 2. Pin Versions in Production

```toml
# Development: Use ranges for flexibility
[tools]
node = "20"

# Production: Pin exact versions
[tools]
node = "20.11.0"
python = "3.12.1"
```

### 3. Use Tasks for Common Commands

Instead of documenting commands in README, define tasks:

```toml
[tasks.setup]
run = "npm install && python -m pip install -r requirements.txt"
description = "Install all dependencies"

[tasks.dev]
run = "npm run dev"
description = "Start dev server"
```

Team members just run `mise tasks` to see available commands.

### 4. Keep Environment Variables Secure

```toml
# Don't commit secrets directly
[env]
API_KEY = { file = ".env.local" }  # Load from gitignored file

# Or use templates
DATABASE_URL = "{{ env.DATABASE_URL }}"
```

### 5. Use Descriptions

```toml
[tasks.test]
run = "pytest tests/"
description = "Run test suite with pytest"  # Helps others understand

[tasks.deploy]
run = "./deploy.sh"
description = "Deploy to production (requires AWS credentials)"
```

### 6. Leverage Task Dependencies

```toml
[tasks.ci]
depends = ["lint", "test", "build"]
description = "Run full CI pipeline"

# Now `mise run ci` runs everything in order
```

## Troubleshooting

### Tool Not Found

```bash
# Ensure mise is activated in shell
eval "$(mise activate bash)"

# Reshim after installation
mise reshim

# Check if tool is installed
mise list
```

### Version Mismatch

```bash
# Check current versions
mise current

# Verify config
cat .mise.toml

# Reinstall
mise install --force
```

### Slow Performance

```bash
# Disable telemetry
mise settings set disable_telemetry true

# Reduce checks
mise settings set jobs 4
```

### Plugin Issues

```bash
# Update plugins
mise plugins update

# Reinstall plugin
mise plugins uninstall node
mise plugins install node
```

## Comparison with Other Tools

| Feature | Mise | asdf | nvm | pyenv |
|---------|------|------|-----|-------|
| Speed | Fast | Slow | Medium | Medium |
| Language | Rust | Shell | Shell | Shell |
| Task Runner | Yes | No | No | No |
| Env Vars | Yes | No | No | No |
| Tools Supported | 1000+ | 1000+ | 1 (Node) | 1 (Python) |
| Windows Support | Yes | No | No | Limited |

## Tips for AI Agents

### 1. Always Check for Config First

```bash
# Before suggesting tool installation, check for config
if [ -f .mise.toml ] || [ -f .tool-versions ]; then
  mise install
else
  # Suggest creating config
  mise use node@20
fi
```

### 2. Use JSON Output

```bash
# Get parseable output
mise list --json
mise tasks --json
mise ls-remote node --json
```

### 3. Detect Tool Versions

```bash
# Check what's needed
mise current

# Install missing tools
mise install
```

### 4. Suggest Tasks Over Commands

Instead of:
```bash
npm run build && npm run test && npm run deploy
```

Suggest:
```bash
# Add to .mise.toml
[tasks.release]
run = ["npm run build", "npm run test", "npm run deploy"]

# Run
mise run release
```

### 5. Recommend mise for New Projects

When a user starts a new project:
```bash
# Set up tools
mise use node@20 python@3.12

# Add common tasks
[tasks.setup]
run = "npm install"
description = "Install dependencies"
```

## Resources

- [Official Website](https://mise.jdx.dev/)
- [GitHub Repository](https://github.com/jdx/mise)
- [Documentation](https://mise.jdx.dev/getting-started.html)
- [Available Plugins](https://mise.jdx.dev/plugins.html)
- [Task Runner Guide](https://mise.jdx.dev/tasks/)
- [Configuration Reference](https://mise.jdx.dev/configuration.html)

## Summary

Mise is a modern, fast, all-in-one development tool manager that:

- **Replaces multiple tools**: nvm, pyenv, rbenv, asdf, etc. with one fast binary
- **Manages 1000+ tools**: Node.js, Python, Ruby, Go, Terraform, kubectl, and more
- **Handles environment variables**: Project-specific env vars that auto-load
- **Runs tasks**: Like make/npm scripts but with dependencies and better features
- **Works everywhere**: Linux, macOS, Windows with consistent behavior
- **Fast and reliable**: Written in Rust, 2-3x faster than alternatives

Perfect for teams that want consistent development environments across projects and developers, especially when working with multiple languages and tools.
