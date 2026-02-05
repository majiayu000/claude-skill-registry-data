---
name: manage-python-env
description: Python virtual environment management using uv for fast and reliable environment setup. Create, maintain, and manage Python virtual environments with dependency management. Use uv for environment creation, package installation, dependency resolution, and project configuration. Use when setting up new Python projects, managing dependencies, troubleshooting environment issues, or ensuring reproducible development environments.
---

# Python Environment Management Skill

This skill provides tools and workflows for managing Python virtual environments using uv, a fast Python package installer and resolver.

## Quick Start

1. **Install uv**: Ensure uv is installed on your system
2. **Create environment**: Use uv to create a new virtual environment
3. **Install dependencies**: Add packages from requirements.txt or pyproject.toml
4. **Manage environment**: Update, freeze, or clean up dependencies
5. **Troubleshoot**: Resolve common environment issues

## Core Workflow

### 1. Environment Setup
```bash
# Initialize project with uv
uv init project-name
cd project-name

# Create virtual environment
uv venv

# Activate environment
# On Windows:
.venv\Scripts\activate
# On Unix/Mac:
source .venv/bin/activate
```

### 2. Dependency Management
```bash
# Install packages
uv add package-name
uv add "package-name>=1.0.0"
uv add "package-name[extra]"

# Install from requirements.txt
uv pip install -r requirements.txt

# Install with development dependencies
uv add --dev pytest black
```

### 3. Project Configuration
```bash
# Generate requirements.txt
uv pip freeze > requirements.txt

# Sync environment
uv sync

# Update packages
uv update
uv update package-name
```

## uv vs Traditional Tools

### Advantages of uv
- **Speed**: 10-100x faster than pip
- **Reliability**: Better dependency resolution
- **Unified tool**: Replaces pip, venv, pip-tools
- **Cross-platform**: Consistent behavior across systems
- **Modern features**: Built-in virtual environments, lock files

### Command Comparison
| Task | uv Command | Traditional Command |
|------|------------|---------------------|
| Create venv | `uv venv` | `python -m venv .venv` |
| Install package | `uv add package` | `pip install package` |
| Install dev package | `uv add --dev package` | `pip install package` |
| Freeze deps | `uv pip freeze` | `pip freeze` |
| Sync env | `uv sync` | `pip install -r requirements.txt` |
| Update package | `uv update package` | `pip install --upgrade package` |

## Environment Types

### Development Environment
```bash
# Complete development setup
uv venv
uv add --dev pytest black flake8 mypy
uv add pandas numpy matplotlib
uv sync
```

### Production Environment
```bash
# Production-ready with pinned versions
uv venv --python 3.11
uv add "package==1.2.3"  # Pin exact versions
uv pip compile requirements.in -o requirements.txt
```

### CI/CD Environment
```bash
# Minimal environment for CI
uv venv --python 3.11
uv add --no-dev package-name
uv sync --frozen
```

## Project Structure

### Recommended Layout
```
project/
├── .venv/                 # Virtual environment (gitignored)
├── src/                   # Source code
├── tests/                 # Test files
├── pyproject.toml         # Project configuration
├── requirements.txt       # Pinned dependencies
├── requirements-dev.txt   # Development dependencies
└── .python-version       # Python version specification
```

### Configuration Files

#### pyproject.toml
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My project description"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
    "pandas>=1.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]

[tool.uv]
# uv-specific settings
```

#### requirements.txt
```
# Pinned dependencies
requests==2.28.2
pandas==1.5.3
numpy==1.24.3
```

## Common Workflows

### New Project Setup
```bash
# 1. Create project directory
mkdir my-project && cd my-project

# 2. Initialize with uv
uv init

# 3. Create virtual environment
uv venv

# 4. Activate environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 5. Add initial dependencies
uv add requests pandas
uv add --dev pytest black

# 6. Create basic project structure
mkdir src tests
touch src/__init__.py tests/__init__.py

# 7. Create .gitignore
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

### Existing Project Setup
```bash
# 1. Clone repository
git clone https://github.com/user/project.git
cd project

# 2. Create environment with specific Python version
uv venv --python 3.11

# 3. Install dependencies
uv sync

# 4. Activate environment
source .venv/bin/activate
```

**Real-world example**: The YouTube-SC project includes complete setup scripts (`setup-environment.bat` and `setup-environment.sh`) and a comprehensive `requirements.txt` file. See `examples/youtube-sc/` for details.

### Dependency Updates
```bash
# Check for updates
uv update --outdated

# Update all packages
uv update

# Update specific package
uv update package-name

# Update with constraints
uv update --pre  # Include pre-release versions
```

## Troubleshooting

### Common Issues

#### 1. Environment Activation Fails
**Symptoms**: `source .venv/bin/activate` doesn't work
**Solutions**:
```bash
# Check if .venv exists
ls -la .venv/

# Try alternative activation
. .venv/bin/activate  # Note the space after the dot

# On Windows, use:
.venv\Scripts\activate
```

#### 2. Package Installation Failures
**Symptoms**: `uv add package` fails with errors
**Solutions**:
```bash
# Clear uv cache
uv cache clean

# Try with verbose output
uv add package -v

# Check Python version compatibility
python --version

# Try different package version
uv add "package>=1.0.0,<2.0.0"
```

#### 3. Dependency Conflicts
**Symptoms**: `uv sync` fails with resolution errors
**Solutions**:
```bash
# Use resolution strategy
uv sync --resolution=highest
uv sync --resolution=lowest-direct

# Check existing dependencies
uv pip list

# Remove conflicting package
uv remove conflicting-package
```

#### 4. Slow Package Installation
**Symptoms**: uv is slow (unusual)
**Solutions**:
```bash
# Use uv's native resolver (already fast)
# Check network connection

# Use mirror or local cache
uv config set global.index-url "https://pypi.tuna.tsinghua.edu.cn/simple"

# Pre-download packages
uv pip download package -d ./packages
```

## Advanced Features

### Lock Files
```bash
# Generate lock file
uv pip compile requirements.in -o requirements.txt

# Install from lock file
uv sync --frozen
```

### Multiple Python Versions
```bash
# Create environment with specific Python version
uv venv --python 3.11
uv venv --python 3.10
uv venv --python 3.9

# List available Python versions
uv python list
```

### Environment Isolation
```bash
# Create isolated environment
uv venv --isolated

# Copy existing environment
uv venv --copies
```

### Cross-Platform Compatibility
```bash
# Generate platform-specific requirements
uv pip compile requirements.in --platform linux --platform macos --platform windows

# Install platform-specific packages
uv add "package; sys_platform == 'linux'"
```

## Integration with Other Tools

### IDE Integration
**VS Code**: Add to settings.json:
```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "terminal.integrated.env.windows": {
        "VIRTUAL_ENV": "${workspaceFolder}/.venv"
    }
}
```

**PyCharm**: 
- File → Settings → Project → Python Interpreter
- Add → Existing environment → Select .venv/bin/python

### Docker Integration
```dockerfile
FROM python:3.11-slim

# Install uv
RUN pip install uv

# Copy project files
COPY . /app
WORKDIR /app

# Create virtual environment and install dependencies
RUN uv venv && uv sync --frozen

# Use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]
```

### CI/CD Integration
```yaml
# GitHub Actions example
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --frozen
      - run: uv run pytest
```

## Best Practices

### 1. Version Pinning
- Pin exact versions in production (`==`)
- Use ranges in development (`>=`)
- Maintain separate requirements files for dev/prod

### 2. Environment Management
- Keep `.venv` in project directory (not global)
- Include `.venv` in `.gitignore`
- Document Python version requirement

### 3. Dependency Hygiene
- Regularly update dependencies
- Remove unused packages
- Audit for security vulnerabilities

### 4. Reproducibility
- Use lock files for exact reproducibility
- Document environment setup in README
- Test across Python versions

## Resources

- **uv Documentation**: See `references/uv-docs.md` for complete uv reference
- **Common Recipes**: See `references/recipes.md` for common environment setups
- **Troubleshooting Guide**: See `references/troubleshooting.md` for solving common issues
- **Migration Guide**: See `references/migration.md` for migrating from pip/venv
- **Project Examples**: See `examples/youtube-sc/` for real-world configuration files from the YouTube-SC project

## When to Use This Skill

Use this skill when:

- Setting up new Python projects
- Managing dependencies for existing projects
- Troubleshooting environment issues
- Creating reproducible environments
- Migrating from pip/venv to uv
- Setting up CI/CD pipelines
- Managing multiple Python versions
- Ensuring cross-platform compatibility