---
name: sdk-config-validator
description: Validates Claude Agent SDK configuration files, environment setup, dependencies, and project structure
allowed-tools: Bash, Read, Grep, Glob
category: validation
complexity: simple
---

# SDK Configuration Validator

Validates Claude Agent SDK project configuration, environment setup, and dependencies.

## Use when...
- User mentions "validate SDK setup", "check SDK configuration", or "SDK not working"
- User reports SDK initialization errors or import failures
- User asks "is my SDK project configured correctly?"
- User requests "troubleshoot SDK issues" or "debug SDK setup"
- Before starting SDK development work in a new project
- After installing SDK dependencies to verify correctness

## Capabilities
- Validates TypeScript/Python SDK configuration files
- Checks SDK version compatibility and dependencies
- Verifies environment variable setup (.env files)
- Validates project structure and required files
- Generates validation reports with actionable fixes
- Provides configuration templates for common setups

## Usage

### Basic Validation
```bash
# Validate TypeScript SDK setup
bash scripts/validate-typescript.sh /path/to/project

# Validate Python SDK setup
bash scripts/validate-python.sh /path/to/project

# Check SDK version compatibility
bash scripts/check-sdk-version.sh /path/to/project
```

### Environment Validation
```bash
# Validate .env file setup
bash scripts/validate-env-setup.sh /path/to/project
```

### Generate Templates
```bash
# Copy environment template
cp templates/.env.example.template /path/to/project/.env.example

# Copy TypeScript config
cp templates/tsconfig-sdk.json /path/to/project/tsconfig.json

# Copy Python config
cp templates/pyproject-sdk.toml /path/to/project/pyproject.toml
```

## Validation Workflow

1. **Detect Project Type**: Check for package.json (TS) or pyproject.toml (Python)
2. **Run Configuration Validation**: Execute appropriate validation script
3. **Check Dependencies**: Verify SDK package is installed with correct version
4. **Validate Environment**: Check .env files for required variables
5. **Generate Report**: Create validation report with findings and fixes
6. **Apply Fixes**: Offer to apply recommended configuration changes

## Common Issues Detected
- Wrong package name (`anthropic-agent-sdk` instead of `claude-agent-sdk`) ⚠️
- Missing SDK dependency in package.json/requirements.txt
- Incorrect TypeScript compiler options for SDK
- Missing required environment variables (ANTHROPIC_API_KEY)
- Missing FastMCP Cloud API key when using MCP servers
- Wrong MCP transport type (`"sse"` instead of `"http"` for FastMCP Cloud) ⚠️
- SDK version incompatibility with Node/Python version
- Missing configuration files (tsconfig.json, .env)
- Incorrect module resolution settings
- Missing async/await pattern in Python code

## Exit Codes
- 0: All validations passed
- 1: Configuration errors found (see report)
- 2: Critical errors (missing SDK, invalid structure)

## Examples
See examples/ directory for sample validation reports and common fix patterns.
