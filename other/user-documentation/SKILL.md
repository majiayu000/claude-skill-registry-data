---
name: user-documentation
description: Create README files, installation guides, tutorials, quick starts, and user-facing documentation. Use when creating project documentation, onboarding.
---

# User Documentation

Create clear, accessible documentation that enables users to quickly understand, install, configure, and effectively use your software.

## When to Use This Skill

Use this skill when you need to:

- Create a professional README
- Write installation guides
- Build quick start tutorials
- Document configuration options
- Create FAQ sections
- Write troubleshooting guides

**Trigger phrases**: "write README", "create documentation", "installation guide", "quick start", "user guide", "getting started"

## What This Skill Does

### Documentation Types

1. **README** - Project overview and quick reference
2. **Installation Guide** - Setup instructions
3. **Quick Start** - Get running in minutes
4. **Usage Guide** - Feature documentation
5. **FAQ** - Common questions
6. **Troubleshooting** - Problem resolution

## Instructions

### README Template

```markdown
# Project Name

Brief one-line description of what the project does.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml)](actions)
[![Version](https://img.shields.io/npm/v/package)](https://npmjs.com/package/package)

## Overview

2-3 sentences explaining:
- What problem this solves
- Who it's for
- Key benefits

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Quick Start

```bash
# Install
pip install mypackage

# Basic usage
mypackage --help
```

## Installation

### Prerequisites

- Python 3.9+
- pip or pipx

### Install from PyPI

```bash
pip install mypackage
```

### Install from Source

```bash
git clone https://github.com/user/repo.git
cd repo
pip install -e .
```

## Usage

### Basic Example

```python
from mypackage import Client

client = Client(api_key="your-key")
result = client.process("input")
print(result)
```

### Advanced Usage

See the the generated `docs/` directory for advanced features.

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `api_key` | Required | Your API key |
| `timeout` | `30` | Request timeout in seconds |
| `retries` | `3` | Number of retry attempts |

## Contributing

See `CONTRIBUTING.md` for guidelines.

## License

MIT License - see `LICENSE` for details.
```

### Installation Guide Template

```markdown
# Installation Guide

## System Requirements

### Minimum Requirements
- OS: Windows 10, macOS 10.15, Ubuntu 20.04
- CPU: 2 cores
- RAM: 4 GB
- Disk: 1 GB free space

### Recommended
- OS: Latest stable release
- CPU: 4+ cores
- RAM: 8 GB
- Disk: 5 GB free space

## Prerequisites

### Python

Ensure Python 3.9+ is installed:

```bash
python --version
# Python 3.9.0 or higher
```

If not installed:
- **Windows**: Download from [python.org](https://python.org)
- **macOS**: `brew install python`
- **Linux**: `sudo apt install python3`

### Dependencies

The following will be installed automatically:
- requests >= 2.28.0
- pydantic >= 2.0.0
- click >= 8.0.0

## Installation Methods

### Method 1: pip (Recommended)

```bash
pip install mypackage
```

### Method 2: pipx (Isolated)

```bash
pipx install mypackage
```

### Method 3: From Source

```bash
git clone https://github.com/user/repo.git
cd repo
pip install -e .
```

### Method 4: Docker

```bash
docker pull user/mypackage
docker run user/mypackage --help
```

## Verification

Verify installation:

```bash
mypackage --version
# mypackage 1.0.0

mypackage doctor
# All checks passed!
```

## Configuration

### Initial Setup

```bash
mypackage init
# Creates ~/.mypackage/config.yaml
```

### Environment Variables

```bash
export MYPACKAGE_API_KEY="your-key"
export MYPACKAGE_DEBUG="true"
```

## Troubleshooting Installation

### Common Issues

#### Permission Denied

```bash
# Use user install
pip install --user mypackage

# Or use virtual environment
python -m venv .venv
source .venv/bin/activate
pip install mypackage
```

#### SSL Certificate Error

```bash
pip install --trusted-host pypi.org mypackage
```

#### Dependency Conflicts

```bash
# Create clean environment
python -m venv clean-env
source clean-env/bin/activate
pip install mypackage
```

## Uninstallation

```bash
pip uninstall mypackage
rm -rf ~/.mypackage  # Remove config
```
```

### Quick Start Guide Template

```markdown
# Quick Start Guide

Get up and running in 5 minutes.

## Step 1: Install

```bash
pip install mypackage
```

## Step 2: Configure

```bash
mypackage init
# Enter your API key when prompted
```

## Step 3: First Run

```bash
# Process a file
mypackage process input.txt

# Or use programmatically
python -c "
from mypackage import process
result = process('Hello, World!')
print(result)
"
```

## Step 4: Verify

```bash
mypackage doctor
# Should show: All checks passed!
```

## What's Next?

- `usage.md` (Usage Guide) - Learn all features
- `config.md` (Configuration) - Customize settings
- `examples/` (Examples) - Real-world examples
- `api.md` (API Reference) - Full API documentation

## Need Help?

- `faq.md` (FAQ) - Common questions
- `troubleshooting.md` (Troubleshooting) - Fix issues
- [GitHub Issues](https://github.com/user/repo/issues) - Report bugs
```

### FAQ Template

```markdown
# Frequently Asked Questions

## General

### What is MyPackage?

MyPackage is a tool for [purpose]. It helps you [benefit].

### Is it free?

Yes, MyPackage is open source under the MIT license.

### What languages are supported?

Currently Python 3.9+. JavaScript support is planned.

## Installation

### Why does installation fail on Windows?

Ensure you have Visual C++ Build Tools installed:
```bash
winget install Microsoft.VisualStudio.BuildTools
```

### Can I use it without internet?

Yes, after initial setup, offline mode is supported:
```bash
mypackage --offline process input.txt
```

## Usage

### How do I process multiple files?

Use glob patterns:
```bash
mypackage process "*.txt"
```

Or use the batch API:
```python
from mypackage import batch_process
results = batch_process(['file1.txt', 'file2.txt'])
```

### How do I handle large files?

Enable streaming mode:
```bash
mypackage process --stream large_file.txt
```

## Troubleshooting

### Why am I getting rate limited?

Implement exponential backoff:
```python
from mypackage import Client
client = Client(retry_config={'max_retries': 5, 'backoff': 2.0})
```

### How do I enable debug logging?

```bash
export MYPACKAGE_DEBUG=true
mypackage process input.txt
```
```

### Troubleshooting Guide Template

```markdown
# Troubleshooting Guide

## Quick Diagnostics

Run the diagnostic tool first:

```bash
mypackage doctor
```

This checks:
- Installation integrity
- Configuration validity
- Network connectivity
- API authentication

## Common Issues

### Issue: "Command not found"

**Symptoms**: Running `mypackage` returns "command not found"

**Solutions**:

1. Ensure package is installed:
   ```bash
   pip list | grep mypackage
   ```

2. Check PATH includes pip binaries:
   ```bash
   python -m mypackage --version
   ```

3. Reinstall:
   ```bash
   pip uninstall mypackage
   pip install mypackage
   ```

### Issue: "Authentication failed"

**Symptoms**: API calls return 401 Unauthorized

**Solutions**:

1. Verify API key is set:
   ```bash
   echo $MYPACKAGE_API_KEY
   ```

2. Regenerate API key in dashboard

3. Check key hasn't expired

### Issue: "Connection timeout"

**Symptoms**: Operations hang then fail

**Solutions**:

1. Check network connectivity:
   ```bash
   curl -I https://api.mypackage.com
   ```

2. Increase timeout:
   ```bash
   mypackage --timeout 60 process input.txt
   ```

3. Check firewall/proxy settings

## Getting Help

If issues persist:

1. Search [existing issues](https://github.com/user/repo/issues)
2. Check [community forum](https://forum.mypackage.com)
3. Open a [new issue](https://github.com/user/repo/issues/new) with:
   - `mypackage doctor` output
   - Error messages
   - Steps to reproduce
```

## Quality Checklist

- [ ] README provides clear overview
- [ ] Installation tested on all platforms
- [ ] Quick start works as documented
- [ ] Configuration options documented
- [ ] FAQ addresses common questions
- [ ] Troubleshooting covers known issues
- [ ] Links are valid
- [ ] Code examples work
- [ ] Screenshots current (if any)
- [ ] Version numbers accurate

## Common Issues and Solutions

### Issue: Documentation becomes outdated
**Solution**: Include documentation updates in PR requirements and review process.

### Issue: Users can't find information
**Solution**: Add search, improve navigation, use clear headings.

### Issue: Installation instructions don't work
**Solution**: Test on fresh environments regularly.

## Related Skills

- `technical-documentation` - Architecture documentation
- `api-documentation` - API reference
- `docstrings` - Code documentation

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates documentation_generation/user_docs/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
