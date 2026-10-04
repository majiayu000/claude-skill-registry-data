---
name: "OWASP ZAP"
description: "Web application security scanner with proxy and active/passive scanning"
version: "0.0.1"
category: "dast"
tags:
  - "template"
  - "example"
author: "Security Skills Team"
license: "MIT"
upstream:
  repo: "https://github.com/zaproxy/zaproxy"
  homepage: "https://example.com"
difficulty: 1
platforms:
  - claude-code
  - codex
  - antigravity
  - opencode
---

## Overview

Brief description of what this tool does, its core value proposition, and when a security practitioner should reach for it.

## Prerequisites

- **OS**: Linux (Ubuntu 22.04+ recommended)
- **Runtime**: Python 3.10+
- **Hardware**: No special requirements
- **API Keys**: None required

## Installation

```bash
# Step 1: Clone the upstream repository
git clone https://github.com/example/tool.git
cd tool

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Verify installation
tool --version
```

## Usage

### Basic Usage

```bash
tool scan --target ./my-project
```

### Advanced Usage

```bash
tool scan --target ./my-project --depth full --output report.json
```

## Workflow Examples

### Example 1: CI/CD Integration

```yaml
# .github/workflows/security.yml
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: tool scan --target . --format sarif > results.sarif
```

### Example 2: Local Development Loop

1. Write code changes
2. Run `tool scan --target .`
3. Review findings
4. Fix and re-scan

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Slow scan | Use `--depth quick` for faster results |

## References

- [Official Documentation](https://example.com/docs)
- [GitHub Repository](https://github.com/example/tool)
- [Research Paper](https://arxiv.org/abs/example)
