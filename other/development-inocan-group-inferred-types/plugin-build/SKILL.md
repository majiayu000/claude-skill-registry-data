---
name: Plugin Build
description: Bundle plugin directory into a deployable Claude Code plugin package
---

# plugin.build

## Overview

**plugin.build** is the packaging tool that bundles your Betty Framework plugin into a distributable archive ready for deployment to Claude Code. It validates all entrypoints, gathers necessary files, and creates versioned packages with checksums.

## Purpose

Automates the creation of deployable plugin packages by:
- **Validating** all declared entrypoints and handler files
- **Gathering** all necessary plugin files (skills, utilities, registries)
- **Packaging** into `.tar.gz` or `.zip` archives
- **Generating** checksums for package verification
- **Reporting** validation results and build metrics

This eliminates manual packaging errors and ensures consistent, reproducible plugin distributions.

## What It Does

1. **Loads plugin.yaml**: Reads the plugin configuration
2. **Validates Entrypoints**: Checks that all command handlers exist on disk
3. **Gathers Files**: Collects skills, utilities, registries, and documentation
4. **Creates Package**: Bundles everything into a versioned archive
5. **Calculates Checksums**: Generates MD5 and SHA256 hashes
6. **Generates Manifest**: Creates manifest.json with entrypoint summary and checksums
7. **Creates Preview**: Generates plugin.preview.yaml for review before deployment
8. **Generates Report**: Outputs detailed build metrics as JSON
9. **Reports Issues**: Identifies missing files or validation errors

## Usage

### Basic Usage

```bash
python skills/plugin.build/plugin_build.py
```

Builds with defaults:
- Plugin: `./plugin.yaml`
- Format: `tar.gz`
- Output: `./dist/`

### Via Betty CLI

```bash
/plugin/build
```

### Custom Plugin Path

```bash
python skills/plugin.build/plugin_build.py /path/to/plugin.yaml
```

### Specify Output Format

```bash
python skills/plugin.build/plugin_build.py --format=zip
```

```bash
python skills/plugin.build/plugin_build.py --format=tar.gz
```

### Custom Output Directory

```bash
python skills/plugin.build/plugin_build.py --output-dir=/tmp/packages
```

### Full Options

```bash
python skills/plugin.build/plugin_build.py \
  /custom/path/plugin.yaml \
  --format=zip \
  --output-dir=/var/packages
```

## Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `plugin_path` | Positional | `./plugin.yaml` | Path to plugin.yaml file |
| `--format` | Option | `tar.gz` | Package format (tar.gz or zip) |
| `--output-dir` | Option | `./dist` | Output directory for packages |

## Output Files

### Package Archive

**Naming convention**: `{plugin-name}-{version}.{format}`

Examples:
- `betty-framework-1.0.0.tar.gz`
- `betty-framework-1.0.0.zip`

**Location**: `{output-dir}/{package-name}.{format}`

### Manifest File

**Naming convention**: `manifest.json`

**Location**: `{output-dir}/manifest.json`

Contains plugin metadata, entrypoint summary, and package checksums. This is the primary file for plugin distribution and installation.

### Plugin Preview

**Naming convention**: `plugin.preview.yaml`

**Location**: `{output-dir}/plugin.preview.yaml`

Contains the current plugin configuration for review before deployment. Useful for comparing changes or validating the plugin structure.

### Build Report

**Naming convention**: `{plugin-name}-{version}-build-report.json`

Example:
- `betty-framework-1.0.0-build-report.json`

**Location**: `{output-dir}/{package-name}-build-report.json`

## Package Structure

The generated archive contains:

```
betty-framework-1.0.0/
├── plugin.yaml               # Plugin manifest
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation (if exists)
├── LICENSE                   # License file (if exists)
├── CHANGELOG.md              # Change log (if exists)
├── betty/                    # Core utility package
│   ├── __init__.py
│   ├── config.py
│   ├── validation.py
│   ├── logging_utils.py
│   ├── file_utils.py
│   └── errors.py
├── registry/                 # Registry files
│   ├── skills.json
│   ├── commands.json
│   ├── hooks.json
│   └── agents.json
└── skills/                   # All active skills
    ├── api.define/
    │   ├── skill.yaml
    │   ├── SKILL.md
    │   └── api_define.py
    ├── api.validate/
    │   ├── skill.yaml
    │   ├── SKILL.md
    │   └── api_validate.py
    └── ... (all other skills)
```

## Manifest Schema

The `manifest.json` file is the primary metadata file for plugin distribution:

```json
{
  "name": "betty-framework",
  "version": "1.0.0",
  "description": "Betty Framework - Structured AI-assisted engineering",
  "author": {
    "name": "RiskExec",
    "email": "platform@riskexec.com",
    "url": "https://github.com/epieczko/betty"
  },
  "license": "MIT",
  "metadata": {
    "homepage": "https://github.com/epieczko/betty",
    "repository": "https://github.com/epieczko/betty",
    "documentation": "https://github.com/epieczko/betty/tree/main/docs",
    "tags": ["framework", "api-development", "workflow"],
    "generated_at": "2025-10-23T12:34:56.789012+00:00"
  },
  "requirements": {
    "python": ">=3.11",
    "packages": ["pyyaml"]
  },
  "permissions": ["filesystem:read", "filesystem:write", "process:execute"],
  "package": {
    "filename": "betty-framework-1.0.0.tar.gz",
    "size_bytes": 245760,
    "checksums": {
      "md5": "a1b2c3d4e5f6...",
      "sha256": "1234567890abcdef..."
    }
  },
  "entrypoints": [
    {
      "command": "skill/define",
      "handler": "skills/skill.define/skill_define.py",
      "runtime": "python"
    }
  ],
  "commands_count": 18,
  "agents": [
    {
      "name": "api.designer",
      "description": "Design APIs with iterative refinement"
    }
  ]
}
```

## Build Report Schema

```json
{
  "build_timestamp": "2025-10-23T12:34:56.789012+00:00",
  "plugin": {
    "name": "betty-framework",
    "version": "1.0.0",
    "description": "Betty Framework - Structured AI-assisted engineering"
  },
  "validation": {
    "total_commands": 18,
    "valid_entrypoints": 18,
    "missing_files": [],
    "has_errors": false
  },
  "package": {
    "path": "/home/user/betty/dist/betty-framework-1.0.0.tar.gz",
    "size_bytes": 245760,
    "size_human": "240.00 KB",
    "files_count": 127,
    "format": "tar.gz",
    "checksums": {
      "md5": "a1b2c3d4e5f6...",
      "sha256": "1234567890abcdef..."
    }
  },
  "entrypoints": [
    {
      "command": "skill/define",
      "handler": "skills/skill.define/skill_define.py",
      "runtime": "python",
      "path": "/home/user/betty/skills/skill.define/skill_define.py"
    }
  ]
}
```

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "success",
  "package_path": "/home/user/betty/dist/betty-framework-1.0.0.tar.gz",
  "report_path": "/home/user/betty/dist/betty-framework-1.0.0-build-report.json",
  "build_report": { ... }
}
```

### Success with Warnings

```json
{
  "ok": false,
  "status": "success_with_warnings",
  "package_path": "/home/user/betty/dist/betty-framework-1.0.0.tar.gz",
  "report_path": "/home/user/betty/dist/betty-framework-1.0.0-build-report.json",
  "build_report": {
    "validation": {
      "missing_files": [
        "Command 'api.broken': handler not found at skills/api.broken/api_broken.py"
      ],
      "has_errors": true
    }
  }
}
```

### Failure Response

```json
{
  "ok": false,
  "status": "failed",
  "error": "plugin.yaml not found: /home/user/betty/plugin.yaml"
}
```

## Behavior

### 1. Plugin Loading

Reads and parses `plugin.yaml`:
- Validates YAML syntax
- Extracts plugin name, version, description
- Identifies all command entrypoints

### 2. Entrypoint Validation

For each command in `plugin.yaml`:
- Extracts handler script path
- Checks file existence on disk
- Reports valid and missing handlers
- Logs validation results

**Valid entrypoint**:
```yaml
- name: skill/validate
  handler:
    runtime: python
    script: skills/skill.define/skill_define.py
```

**Missing handler** (reports warning):
```yaml
- name: broken/command
  handler:
    runtime: python
    script: skills/broken/missing.py  # File doesn't exist
```

### 3. File Gathering

Automatically includes:

**Always included**:
- `plugin.yaml` – Plugin manifest
- `skills/*/` – All skill directories referenced in commands
- `betty/` – Core utility package
- `registry/*.json` – All registry files

**Conditionally included** (if exist):
- `requirements.txt` – Python dependencies
- `README.md` – Plugin documentation
- `LICENSE` – License file
- `CHANGELOG.md` – Version history

**Excluded**:
- `__pycache__/` directories
- `.pyc` compiled Python files
- Hidden files (starting with `.`)
- Build artifacts and temporary files

### 4. Package Creation

**tar.gz format**:
- GZIP compression
- Preserves file permissions
- Cross-platform compatible
- Standard for Python packages

**zip format**:
- ZIP compression
- Wide compatibility
- Good for Windows environments
- Easy to extract without CLI tools

### 5. Checksum Generation

Calculates two checksums:

**MD5**: Fast, widely supported
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**SHA256**: Cryptographically secure
```
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
```

Use checksums to verify package integrity after download or transfer.

## Examples

### Example 1: Standard Build

**Scenario**: Build Betty Framework plugin for distribution

```bash
# Ensure plugin.yaml is up to date
/plugin/sync

# Build the package
/plugin/build
```

**Output**:
```
INFO: 🏗️  Starting plugin build...
INFO: 📄 Plugin: /home/user/betty/plugin.yaml
INFO: 📦 Format: tar.gz
INFO: 📁 Output: /home/user/betty/dist
INFO: ✅ Loaded plugin.yaml from /home/user/betty/plugin.yaml
INFO: 📝 Validating 18 command entrypoints...
INFO: 📦 Gathering files from 16 skill directories...
INFO: 📦 Adding betty/ utility package...
INFO: 📦 Adding registry/ files...
INFO: 📦 Total files to package: 127
INFO: 🗜️  Creating tar.gz archive: /home/user/betty/dist/betty-framework-1.0.0.tar.gz
INFO: 🔐 Calculating checksums...
INFO:   MD5:    a1b2c3d4e5f6...
INFO:   SHA256: 1234567890ab...
INFO: 📊 Build report: /home/user/betty/dist/betty-framework-1.0.0-build-report.json
INFO: 📋 Manifest: /home/user/betty/dist/manifest.json
INFO: 📋 Preview file created: /home/user/betty/dist/plugin.preview.yaml
INFO:
============================================================
INFO: 🎉 BUILD COMPLETE
============================================================
INFO: 📦 Package:  /home/user/betty/dist/betty-framework-1.0.0.tar.gz
INFO: 📊 Report:   /home/user/betty/dist/betty-framework-1.0.0-build-report.json
INFO: 📋 Manifest: /home/user/betty/dist/manifest.json
INFO: 👁️  Preview:  /home/user/betty/dist/plugin.preview.yaml
INFO: ✅ Commands: 18/18
INFO: 📏 Size:     240.00 KB
INFO: 📝 Files:    127
============================================================
```

### Example 2: Build as ZIP

**Scenario**: Create Windows-friendly package

```bash
python skills/plugin.build/plugin_build.py --format=zip
```

**Result**: `dist/betty-framework-1.0.0.zip`

### Example 3: Build with Custom Output

**Scenario**: Build to specific release directory

```bash
python skills/plugin.build/plugin_build.py \
  --format=tar.gz \
  --output-dir=releases/v1.0.0
```

**Result**:
- `releases/v1.0.0/betty-framework-1.0.0.tar.gz`
- `releases/v1.0.0/betty-framework-1.0.0-build-report.json`

### Example 4: Detecting Missing Handlers

**Scenario**: Some handlers are missing

```bash
# Remove a handler file
rm skills/api.validate/api_validate.py

# Try to build
/plugin/build
```

**Output**:
```
INFO: 📝 Validating 18 command entrypoints...
WARNING:   ❌ skill/api/validate: skills/api.validate/api_validate.py (not found)
INFO: ⚠️  Found 1 missing files:
INFO:   - Command 'skill/api/validate': handler not found at skills/api.validate/api_validate.py
INFO: 📦 Gathering files from 15 skill directories...
...
INFO: ============================================================
INFO: 🎉 BUILD COMPLETE
INFO: ============================================================
INFO: ✅ Commands: 17/18
INFO: ⚠️  Warnings: 1
```

**Exit code**: 1 (failure due to validation errors)

### Example 5: Build Workflow

**Scenario**: Complete release workflow

```bash
# 1. Update registries
/registry/update

# 2. Sync plugin.yaml
/plugin/sync

# 3. Build package
/plugin/build

# 4. Verify package
tar -tzf dist/betty-framework-1.0.0.tar.gz | head -20

# 5. Check build report
cat dist/betty-framework-1.0.0-build-report.json | jq .
```

## Integration

### With plugin.sync

Always sync before building:

```bash
/plugin/sync && /plugin/build
```

### With Workflows

Include in release workflow:

```yaml
# workflows/plugin_release.yaml
name: plugin_release
version: 1.0.0
description: Release workflow for Betty Framework plugin

steps:
  - skill: registry.update
    description: Update all registries

  - skill: plugin.sync
    description: Generate plugin.yaml

  - skill: plugin.build
    args: ["--format=tar.gz"]
    description: Build tar.gz package

  - skill: plugin.build
    args: ["--format=zip"]
    description: Build zip package
```

### With CI/CD

Add to GitHub Actions:

```yaml
# .github/workflows/release.yml
- name: Build Plugin Package
  run: |
    python skills/plugin.sync/plugin_sync.py
    python skills/plugin.build/plugin_build.py --format=tar.gz
    python skills/plugin.build/plugin_build.py --format=zip

- name: Upload Packages
  uses: actions/upload-artifact@v3
  with:
    name: plugin-packages
    path: dist/betty-framework-*
```

## Validation Rules

### Entrypoint Validation

**Valid entrypoint**:
- Command name is defined
- Handler section exists
- Handler script path is specified
- Handler file exists on disk
- Runtime is specified

**Invalid entrypoint** (triggers warning):
- Missing handler script path
- Handler file doesn't exist
- Empty command name

### File Gathering Rules

**Skill directories included if**:
- Referenced in at least one command handler
- Contains valid handler file

**Files excluded**:
- Python cache files (`__pycache__`, `.pyc`)
- Hidden files (`.git`, `.env`, etc.)
- Build artifacts (`dist/`, `build/`)
- IDE files (`.vscode/`, `.idea/`)

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "plugin.yaml not found" | Missing plugin.yaml | Run `/plugin/sync` first |
| "Invalid YAML" | Syntax error in plugin.yaml | Fix YAML syntax |
| "Unsupported output format" | Invalid --format value | Use `tar.gz` or `zip` |
| "Handler not found" | Missing handler file | Create handler or fix path |
| "Permission denied" | Cannot write to output dir | Check directory permissions |

## Files Read

- `plugin.yaml` – Plugin manifest
- `skills/*/skill.yaml` – Skill manifests (indirect via handlers)
- `skills/*/*.py` – Handler scripts
- `betty/*.py` – Utility modules
- `registry/*.json` – Registry files
- `requirements.txt` – Dependencies (if exists)
- `README.md`, `LICENSE`, `CHANGELOG.md` – Documentation (if exist)

## Files Modified

- `{output-dir}/{plugin-name}-{version}.{format}` – Created package archive
- `{output-dir}/{plugin-name}-{version}-build-report.json` – Created build report
- `{output-dir}/manifest.json` – Created plugin manifest with checksums and entrypoints
- `{output-dir}/plugin.preview.yaml` – Created plugin preview for review

## Exit Codes

- **0**: Success (all handlers valid, package created)
- **1**: Failure (missing handlers or build error)

## Logging

Logs build progress with emojis for clarity:

```
INFO: 🏗️  Starting plugin build...
INFO: 📄 Plugin: /home/user/betty/plugin.yaml
INFO: ✅ Loaded plugin.yaml
INFO: 📝 Validating entrypoints...
INFO: 📦 Gathering files...
INFO: 🗜️  Creating tar.gz archive...
INFO: 🔐 Calculating checksums...
INFO: 📊 Build report written
INFO: 🎉 BUILD COMPLETE
```

## Best Practices

1. **Always Sync First**: Run `/plugin/sync` before `/plugin/build`
2. **Validate Before Building**: Ensure all skills are registered and active
3. **Check Build Reports**: Review validation warnings before distribution
4. **Verify Checksums**: Use checksums to verify package integrity
5. **Version Consistently**: Match plugin version with git tags
6. **Test Extraction**: Verify packages extract correctly
7. **Document Changes**: Keep CHANGELOG.md updated

## Troubleshooting

### Missing Files in Package

**Problem**: Expected files not in archive

**Solutions**:
- Ensure files exist in source directory
- Check that skills are referenced in commands
- Verify files aren't excluded (e.g., `.pyc`, `__pycache__`)
- Check file permissions

### Handler Validation Failures

**Problem**: Handlers marked as missing but files exist

**Solutions**:
- Verify exact path in plugin.yaml matches file location
- Check case sensitivity in file paths
- Ensure handler files have correct names
- Run `/plugin/sync` to update paths

### Package Size Too Large

**Problem**: Archive file is very large

**Solutions**:
- Remove unused skills from plugin.yaml
- Check for accidentally included large files
- Review skill directories for unnecessary data
- Consider splitting into multiple plugins

### Build Fails with Permission Error

**Problem**: Cannot write to output directory

**Solutions**:
- Create output directory with proper permissions
- Check disk space availability
- Verify write access to output directory
- Try different output directory with `--output-dir`

## Architecture

### Skill Category

**Infrastructure** – Plugin.build is part of the distribution layer, preparing plugins for deployment.

### Design Principles

- **Validation First**: Check all handlers before packaging
- **Complete Packages**: Include all necessary dependencies
- **Reproducible**: Same source creates identical packages
- **Verifiable**: Checksums ensure package integrity
- **Transparent**: Detailed reporting of included files
- **Flexible**: Support multiple archive formats

### Package Philosophy

The package includes everything needed to run the plugin:
- **Skills**: All command handlers and manifests
- **Utilities**: Core betty package for shared functionality
- **Registries**: Skill, command, and hook definitions
- **Dependencies**: Python requirements
- **Documentation**: README, LICENSE, CHANGELOG

This creates a self-contained, portable plugin distribution.

## See Also

- **plugin.sync** – Generate plugin.yaml ([SKILL.md](../plugin.sync/SKILL.md))
- **skill.define** – Validate and register skills ([SKILL.md](../skill.define/SKILL.md))
- **registry.update** – Update registries ([SKILL.md](../registry.update/SKILL.md))
- **Betty Distribution** – Plugin marketplace guide ([docs/distribution.md](../../docs/distribution.md))

## Dependencies

- **plugin.sync**: Generate plugin.yaml before building
- **betty.config**: Configuration constants and paths
- **betty.logging_utils**: Logging infrastructure

## Status

**Active** – Production-ready infrastructure skill

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with tar.gz/zip support, validation, and checksums
