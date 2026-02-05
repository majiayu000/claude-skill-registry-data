---
name: Environment Setup
description: Environment verification, tool checking, version validation, and path configuration. Use when checking system requirements, verifying tool installations, validating versions, checking PATH configuration, or when user mentions environment setup, system check, tool verification, version check, missing tools, or installation requirements.
---

# Environment Setup

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

## Overview

Provides comprehensive environment verification, tool installation checking, version validation, PATH configuration, and environment variable management for development workflows.

## Instructions

### Environment Verification

1. Use `scripts/check-environment.sh` to verify all required tools are installed
2. Check versions of languages, package managers, and build tools
3. Validate PATH configuration and tool accessibility
4. Verify environment variables are properly configured
5. Generate comprehensive environment report

### Tool Installation Verification

1. Use `scripts/check-tools.sh` to verify specific tools (node, python, go, rust, etc.)
2. Check if tools are in PATH and accessible
3. Verify tool versions meet minimum requirements
4. Provide installation instructions for missing tools
5. Detect version managers (nvm, pyenv, rbenv, rustup)

### Version Validation

1. Use `scripts/validate-versions.sh` to check language and tool versions
2. Compare against project requirements (package.json, .tool-versions, etc.)
3. Identify version mismatches and compatibility issues
4. Suggest version upgrades or downgrades
5. Check for deprecated versions

### PATH Configuration

1. Use `scripts/validate-path.sh` to verify PATH is correctly configured
2. Check for tool binaries in expected locations
3. Detect PATH issues (missing entries, duplicate entries, ordering problems)
4. Suggest PATH fixes for shell configuration files
5. Validate system paths vs user paths

### Environment Variable Management

1. Use `scripts/check-env-vars.sh` to validate required environment variables
2. Check for missing, empty, or misconfigured variables
3. Validate API keys and credentials (without exposing values)
4. Suggest environment variable configuration
5. Detect conflicts between .env files and system environment

## Available Scripts

- **check-environment.sh**: Comprehensive environment verification across all tools
- **check-tools.sh**: Verify specific tools are installed and accessible
- **validate-versions.sh**: Check tool versions against requirements
- **validate-path.sh**: Verify PATH configuration and detect issues
- **check-env-vars.sh**: Validate environment variables and configuration

## Templates

- **environment-report.template**: Comprehensive environment status report
- **tool-requirements.md**: Project tool requirements documentation
- **path-config.sh.template**: Shell configuration for PATH setup
- **env-template.template**: Environment variable template file
- **version-requirements.json**: Tool version requirements specification
- **installation-guide.md.template**: Tool installation instructions

## Examples

See `examples/` directory for:
- **basic-usage.md**: Simple environment checks
- **advanced-usage.md**: Complex multi-tool verification
- **common-patterns.md**: Typical environment setup patterns
- **error-handling.md**: Handling missing tools and version issues
- **integration.md**: Using with other skills and workflows

## Requirements

- Support major languages: Node.js, Python, Go, Rust, Ruby, Java, PHP, .NET
- Support package managers: npm, yarn, pnpm, pip, poetry, cargo, gem, maven, composer
- Support build tools: make, cmake, gradle, webpack, vite, rollup
- Support version managers: nvm, pyenv, rbenv, rustup, jenv, phpbrew
- Detect operating system differences (Linux, macOS, Windows/WSL)
- Provide actionable error messages with installation instructions
- Generate reports in multiple formats (text, JSON, markdown)

## Best Practices

- **Never assume tools are installed** - Always verify before proceeding
- **Check versions before operations** - Prevent version-related failures
- **Provide clear error messages** - Include installation instructions
- **Support multiple OSes** - Handle Linux, macOS, Windows/WSL differences
- **Detect version managers** - Use nvm, pyenv, etc. when available
- **Cache verification results** - Avoid redundant checks within same session
- **Report all issues** - Don't fail on first error, collect all problems

## Output Format

All scripts output structured results:
```json
{
  "status": "success|warning|error",
  "tools": {
    "node": {"installed": true, "version": "20.11.0", "required": ">=18.0.0", "status": "ok"},
    "python": {"installed": true, "version": "3.11.5", "required": ">=3.9.0", "status": "ok"},
    "go": {"installed": false, "status": "missing"}
  },
  "path": {"valid": true, "issues": []},
  "env_vars": {"valid": true, "missing": []},
  "recommendations": []
}
```

---

**Purpose**: Comprehensive environment verification and configuration management
**Used by**: All agents requiring tool verification, project setup, and environment validation
