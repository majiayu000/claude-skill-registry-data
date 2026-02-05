---
name: devcontainer-workflow
description: DevContainer configuration for consistent development environments with Docker, multi-stage builds, non-root users, environment management, Docker-in-Docker support, and Python with uv. Activate when working with .devcontainer/, devcontainer.json, Dockerfile, or container-based development workflows.
---

# DevContainer Workflow

Guidelines for setting up and maintaining consistent development environments using DevContainers with Docker, featuring non-root user configurations, environment management, multi-stage builds, and Python-focused patterns.

## Quick Start Checklist

- [ ] Create `.devcontainer/` directory structure
- [ ] Configure `devcontainer.json` with runtime settings
- [ ] Create multi-stage `Dockerfile` for development environment
- [ ] Set up non-root `vscode` user with proper permissions
- [ ] Configure volume mounts (home, SSH, docker socket)
- [ ] Create `.env.example` templates for configuration
- [ ] Set up `postCreateCommand` with Makefile integration
- [ ] Configure VS Code extensions in customizations
- [ ] Test container build and entry
- [ ] Verify all development tools are accessible

---

## Directory Structure

```
project/
├── .devcontainer/
│   ├── devcontainer.json       # Container runtime configuration
│   ├── Dockerfile              # Multi-stage development build
│   ├── .env.example            # Dev-specific config template
│   └── .env                    # Dev-specific config (gitignored)
├── .env.example                # Shared config template (committed)
├── .env                        # Shared config (gitignored)
├── Makefile                    # Development task automation
└── pyproject.toml              # Python project configuration
```

---

## Container Configuration

### Multi-Stage Dockerfile Pattern

Use multi-stage builds to separate development, testing, and production stages:

```dockerfile
# Base stage with common dependencies
FROM python:3.14-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    git \
    make \
    zsh \
    zsh-autosuggestions \
    zsh-syntax-highlighting \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Development stage with full tooling
FROM base AS development

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create non-root user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/zsh && \
    apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    vim \
    && rm -rf /var/lib/apt/lists/* && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /workspace
USER $USERNAME

# Configure shell
RUN echo 'source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ~/.zshrc && \
    echo 'source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ~/.zshrc && \
    echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc

# Production stage (minimal footprint)
FROM base AS production

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app
USER appuser

COPY --from=development /workspace /app
RUN /app/.venv/bin/pip install --no-cache-dir -e .
```

### Python 3.14+ with UV Installation

Ensure uv is installed in development stage:

```dockerfile
# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# (Later in USER vscode section)
# Copy project files for dependency installation
COPY --chown=vscode:vscode pyproject.toml uv.lock* ./
RUN uv sync --no-dev || uv sync
```

---

## Non-Root User Configuration

### User Setup in Dockerfile

Always use a non-root user for security. Standard name is `vscode`:

```dockerfile
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create user with home directory and shell
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/zsh && \
    apt-get update && apt-get install -y --no-install-recommends sudo && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    rm -rf /var/lib/apt/lists/*

# Set user for all subsequent commands
USER $USERNAME
```

### Permissions for Mounted Volumes

Ensure proper ownership of workspace and home directories:

```dockerfile
# After copying project files
COPY --chown=vscode:vscode . /workspace

# Ensure workspace permissions
RUN mkdir -p /workspace && chown -R vscode:vscode /workspace
```

### devcontainer.json User Configuration

```json
{
  "remoteUser": "vscode"
}
```

---

## Environment Management

### .env File Strategy

Use multiple `.env` files for different scopes:

1. **Project root `.env`** - Shared across all environments (gitignored)
2. **`.devcontainer/.env`** - Development-specific overrides (gitignored)
3. **`.env.example`** - Template for shared config (committed)
4. **`.devcontainer/.env.example`** - Template for dev config (committed)

### Root `.env.example`

```bash
# Shared configuration (safe for version control)
PROJECT_NAME=my-project
LOG_LEVEL=info
PYTHON_VERSION=3.14
DEBUG=false
```

### .devcontainer/.env.example

```bash
# Development-specific settings
DEBUG=true
LOG_LEVEL=debug
PYTHONUNBUFFERED=1
HOT_RELOAD=true
```

### Loading Environment in devcontainer.json

```json
{
  "runArgs": [
    "--env-file", "${localWorkspaceFolder}/.env",
    "--env-file", "${localWorkspaceFolder}/.devcontainer/.env"
  ]
}
```

Order matters: later files override earlier ones. Local `.devcontainer/.env` overrides shared `.env`.

---

## Docker-in-Docker Support

### When to Use

- Building Docker images within the devcontainer
- Running integration tests with containers
- Testing Docker Compose configurations
- Local CI/CD pipeline simulation

### Configuration

Add Docker-in-Docker feature to `devcontainer.json`:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "version": "latest",
      "moby": true
    }
  },
  "mounts": [
    "source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind"
  ]
}
```

### Security Considerations

Mounting the Docker socket grants the container full Docker daemon access:

- Use only in trusted development environments
- Never use in untrusted code environments
- Ensure user in container is trusted
- Consider using Docker contexts for isolation if running sensitive containers

### Testing with Docker Compose

```makefile
.PHONY: test-integration
test-integration:
	docker compose -f docker-compose.test.yml up -d
	uv run pytest tests/integration/ -v --tb=short
	docker compose -f docker-compose.test.yml down

.PHONY: build-image
build-image:
	docker build -t my-app:latest --target production .
```

---

## Development Tools

### Shell: Zsh Configuration

Configure zsh with plugins for better development experience:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    zsh \
    zsh-autosuggestions \
    zsh-syntax-highlighting \
    && rm -rf /var/lib/apt/lists/*

USER vscode
RUN echo 'source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ~/.zshrc && \
    echo 'source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ~/.zshrc && \
    echo 'setopt HIST_FIND_NO_DUPS' >> ~/.zshrc && \
    echo 'setopt SHARE_HISTORY' >> ~/.zshrc
```

### VS Code Extensions

Configure recommended extensions in `devcontainer.json`:

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "ms-azuretools.vscode-docker",
        "eamodio.gitlens",
        "ms-vscode.makefile-tools",
        "GitHub.copilot"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.formatting.provider": "black",
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
          }
        },
        "editor.formatOnSave": true,
        "files.trimTrailingWhitespace": true,
        "files.insertFinalNewline": true,
        "terminal.integrated.defaultProfile.linux": "zsh"
      }
    }
  }
}
```

### Essential Development Tools

Include in Dockerfile for all development environments:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    jq \
    && rm -rf /var/lib/apt/lists/*
```

---

## Volume Mounts

### Home Directory Persistence

Preserve shell history, configurations, and VS Code data across container rebuilds:

```json
{
  "mounts": [
    "source=${localWorkspaceFolderBasename}-home,target=/home/vscode,type=volume"
  ]
}
```

Benefits of dynamic naming with `${localWorkspaceFolderBasename}`:
- Unique volume per workspace (supports multiple projects)
- Prevents conflicts with other projects
- Clear naming: `project-name-home`

### SSH Key Access

Enable git operations and remote access with SSH keys:

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,type=bind,readonly"
  ]
}
```

On Windows, use:
```json
{
  "mounts": [
    "source=${localEnv:USERPROFILE}\\.ssh,target=/home/vscode/.ssh,type=bind,readonly"
  ]
}
```

Configure SSH for git:

```bash
# In devcontainer or post-create
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts 2>/dev/null
git config --global core.sshCommand "ssh -i ~/.ssh/id_rsa"
```

### Docker Socket for DinD

```json
{
  "mounts": [
    "source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind"
  ]
}
```

Add user to docker group in container:

```dockerfile
RUN groupadd docker || true && \
    usermod -aG docker vscode
```

---

## Post-Create Commands

### Makefile-Driven Initialization

Use `postCreateCommand` to invoke a Makefile target:

```json
{
  "postCreateCommand": "make initialize"
}
```

### Makefile Example

```makefile
.PHONY: initialize
initialize: deps env-setup
	@echo "Development environment initialized"

.PHONY: deps
deps:
	@echo "Installing dependencies with uv..."
	uv sync --extra dev

.PHONY: env-setup
env-setup:
	@echo "Setting up environment..."
	mkdir -p logs tmp .cache
	test -f .env || cp .env.example .env
	test -f .devcontainer/.env || cp .devcontainer/.env.example .devcontainer/.env
	@echo ".env files created from templates"

.PHONY: hooks
hooks:
	@echo "Setting up git hooks..."
	pre-commit install || true

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage .mypy_cache
	uv pip cache prune

.PHONY: test
test:
	uv run pytest tests/ -v --tb=short

.PHONY: check
check:
	uv run pytest tests/ -v
	uv run ruff check .
	uv run mypy src/ --ignore-missing-imports

.PHONY: run
run:
	uv run python -m myapp.cli
```

---

## Complete devcontainer.json Example

```json
{
  "name": "Python Development Environment",
  "description": "Development container with Python 3.14, uv, and Docker-in-Docker",
  "image": "mcr.microsoft.com/devcontainers/python:3.14",
  "dockerFile": "../Dockerfile",
  "target": "development",
  "context": "..",

  "runArgs": [
    "--env-file", "${localWorkspaceFolder}/.env",
    "--env-file", "${localWorkspaceFolder}/.devcontainer/.env"
  ],

  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "version": "latest",
      "moby": true
    }
  },

  "mounts": [
    "source=${localWorkspaceFolderBasename}-home,target=/home/vscode,type=volume",
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,type=bind,readonly"
  ],

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "ms-azuretools.vscode-docker",
        "eamodio.gitlens",
        "ms-vscode.makefile-tools"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.formatting.provider": "black",
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
          }
        },
        "editor.formatOnSave": true,
        "files.trimTrailingWhitespace": true,
        "files.insertFinalNewline": true,
        "terminal.integrated.defaultProfile.linux": "zsh",
        "terminal.integrated.profiles.linux": {
          "zsh": {
            "path": "/bin/zsh",
            "args": ["-l"]
          }
        }
      }
    }
  },

  "postCreateCommand": "make initialize",
  "postStartCommand": "git config --global --add safe.directory /workspace",

  "remoteUser": "vscode",
  "remoteEnv": {
    "PATH": "/home/vscode/.local/bin:${containerEnv:PATH}"
  }
}
```

---

## Python with UV Patterns

### Project Setup with uv

Initialize project with uv and modern Python:

```bash
# In container or locally
uv new my-project --python 3.14
cd my-project
uv sync
```

### Dependencies Management

```bash
# Add production dependency
uv add requests fastapi

# Add development dependency
uv add --group dev pytest pytest-cov black ruff mypy

# Add optional group
uv add --group notebook jupyter ipykernel

# Sync all dependencies
uv sync --extra dev

# Run with uv
uv run python -m myapp.cli
uv run pytest tests/ -v
```

### pyproject.toml Structure for Development

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.14"
dependencies = [
    "fastapi>=0.104.0",
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.9.0",
    "ruff>=0.10.0",
    "mypy>=1.5.0",
    "pre-commit>=3.3.0",
]

[tool.uv]
dev-dependencies = ["pytest", "black", "ruff", "mypy"]

[tool.black]
line-length = 88
target-version = ["py314"]

[tool.ruff]
line-length = 88
target-version = "py314"

[tool.mypy]
python_version = "3.14"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```

### Makefile UV Integration

```makefile
.PHONY: install
install:
	uv sync --extra dev

.PHONY: test
test:
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

.PHONY: lint
lint:
	uv run ruff check src/ tests/
	uv run mypy src/

.PHONY: format
format:
	uv run black src/ tests/
	uv run ruff check --fix src/ tests/

.PHONY: run
run:
	uv run python -m myapp.cli
```

### Installing from Dockerfile During Build

```dockerfile
COPY --chown=vscode:vscode pyproject.toml uv.lock* ./
RUN if [ -f uv.lock ]; then \
      uv sync --no-dev; \
    else \
      uv sync; \
    fi
```

---

## Testing Support

### Unit Testing with pytest

Configure pytest in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: unit tests",
    "integration: integration tests",
    "slow: slow tests",
]
```

### Integration Testing with Docker Compose

Create `docker-compose.test.yml`:

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: testpass
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### Test Makefile Targets

```makefile
.PHONY: test test-unit test-integration test-all
test: test-unit

test-unit:
	uv run pytest tests/unit/ -v -m "not slow"

test-integration:
	docker compose -f docker-compose.test.yml up -d
	uv run pytest tests/integration/ -v || true
	docker compose -f docker-compose.test.yml down

test-all:
	uv run pytest tests/ -v --cov=src --cov-report=html

test-watch:
	uv run pytest-watch tests/unit/
```

---

## Troubleshooting

### Permission Denied Errors

**Problem:** Files owned by root, cannot write from vscode user.

**Solution in Dockerfile:**

```dockerfile
RUN chown -R vscode:vscode /workspace /home/vscode
```

**Check in container:**

```bash
whoami
ls -la /workspace
ls -la /home/vscode
```

### Extensions Not Installing

**Problem:** VS Code extensions fail to install in container.

**Solution:** Use full extension IDs with version pins:

```json
{
  "extensions": [
    "ms-python.python@2024.0.0",
    "ms-python.vscode-pylance@2024.0.0"
  ]
}
```

Or rebuild container:

```bash
# In VS Code: Dev Containers: Rebuild Container
```

### Environment Variables Not Loading

**Problem:** `.env` files created but variables not available in container.

**Solution:** Verify files exist and rebuild:

```bash
# Check in container
printenv | grep YOUR_VAR
cat /home/vscode/.env

# Rebuild container
```

Ensure `runArgs` correctly references env files in `devcontainer.json`.

### Docker Socket Permission Issues

**Problem:** Cannot access Docker socket from container.

**Solution in Dockerfile:**

```dockerfile
RUN groupadd docker || true && \
    usermod -aG docker vscode
```

In `devcontainer.json`:

```json
{
  "postCreateCommand": "newgrp docker"
}
```

### UV Cache Issues

**Problem:** Dependency resolution slow or caching issues.

**Solution:**

```bash
# Clear uv cache in container
uv pip cache prune

# In Dockerfile, use specific versions
RUN uv sync --frozen  # Use uv.lock if available
```

### Volume Mount Issues on Windows

**Problem:** Volume mounts not working on Windows with WSL2.

**Solution:** Ensure Docker Desktop WSL2 integration enabled:

```bash
# In devcontainer.json, use Windows paths correctly
"mounts": [
  "source=${localEnv:USERPROFILE}\\.ssh,target=/home/vscode/.ssh,type=bind,readonly"
]
```

---

## Validation Guidance

### Pre-Build Validation

Check before building container:

```bash
# Validate JSON syntax
python -m json.tool .devcontainer/devcontainer.json

# Check file references
ls -la Dockerfile pyproject.toml .env.example

# Validate Makefile
make --dry-run initialize
```

### Post-Build Validation

After container builds:

```bash
# Verify user and permissions
docker exec <container> whoami
docker exec <container> ls -la /workspace

# Test uv installation
docker exec <container> uv --version

# Verify zsh and plugins
docker exec <container> zsh -c "echo $ZSH_VERSION"

# Check VS Code extensions installed
docker exec <container> code --list-extensions 2>/dev/null || echo "VS Code not in container"
```

### Development Environment Check

```makefile
.PHONY: validate
validate: validate-files validate-container validate-tools

.PHONY: validate-files
validate-files:
	@echo "Validating devcontainer configuration..."
	@python -m json.tool .devcontainer/devcontainer.json > /dev/null
	@test -f Dockerfile && echo "✓ Dockerfile found" || exit 1
	@test -f pyproject.toml && echo "✓ pyproject.toml found" || exit 1
	@test -f .env.example && echo "✓ .env.example found" || exit 1

.PHONY: validate-container
validate-container:
	@echo "Validating container setup..."
	@whoami | grep -q vscode && echo "✓ Running as vscode user" || exit 1
	@test -d /workspace && echo "✓ Workspace mounted" || exit 1
	@test -d /home/vscode && echo "✓ Home directory mounted" || exit 1

.PHONY: validate-tools
validate-tools:
	@echo "Validating development tools..."
	@uv --version && echo "✓ uv installed" || exit 1
	@python --version && echo "✓ Python available" || exit 1
	@zsh --version && echo "✓ zsh available" || exit 1
	@git --version && echo "✓ git available" || exit 1

.PHONY: check-env
check-env:
	@echo "Environment variables:"
	@printenv | grep -E '^(PYTHON|DEBUG|LOG_LEVEL|PROJECT_NAME)' || echo "No project vars found"
	@test -f .env && echo "✓ .env file loaded" || echo "⚠ .env file missing"
```

---

## Best Practices Summary

1. **Always use non-root user** (`vscode` by default) in containers
2. **Use dynamic volume naming** with `${localWorkspaceFolderBasename}-home` for persistence
3. **Prefer uv** for Python dependency management in devcontainers
4. **Multi-stage builds** separate development and production concerns
5. **Keep Dockerfile minimal** - offload setup to Makefile targets
6. **Environment as configuration** - use `.env` files for settings
7. **Document all tools** - list in VS Code extensions and Dockerfile
8. **Test container builds** - validate before committing devcontainer configs
9. **SSH access when needed** - mount `.ssh` as readonly for git operations
10. **DinD with caution** - only enable Docker socket when truly needed
