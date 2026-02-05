---
name: Plugin Publish
description: Publish bundled plugin packages to local, marketplace, or GitHub Releases with dry-run and validation modes
---

# plugin.publish

## Overview

**plugin.publish** is the publication tool that distributes your bundled Betty Framework plugin packages to various targets. It validates package integrity via SHA256 checksums and handles publication to local directories, Claude Marketplace endpoints, or GitHub Releases with automatic creation support. Includes `--dry-run` and `--validate-only` modes for safe testing.

## Purpose

Automates secure plugin distribution by:
- **Validating** SHA256 checksums to ensure package integrity
- **Publishing** to local directories for testing and archival
- **Uploading** to Claude Marketplace API endpoint (simulated, ready for production)
- **Creating** GitHub Releases automatically using gh CLI
- **Tracking** publication metadata for auditing and governance
- **Testing** with dry-run mode before actual publication
- **Validating** packages without publishing using validate-only mode

This ensures consistent, traceable, and secure plugin distribution across all deployment targets.

## What It Does

1. **Validates Package**: Verifies the .tar.gz file exists and is readable
2. **Calculates Checksums**: Computes MD5 and SHA256 hashes for integrity verification
3. **Validates SHA256**: Compares against expected checksum from manifest.json
4. **Loads Metadata**: Extracts plugin info from manifest.json (name, version, author, etc.)
5. **Publishes to Target**:
   - **local**: Copies to `dist/published/` with metadata
   - **marketplace**: POSTs JSON metadata to Claude Marketplace API (simulated)
   - **gh-release**: Creates GitHub Release using gh CLI (with auto-create option)
6. **Supports Modes**:
   - **--dry-run**: Shows what would be done without making changes
   - **--validate-only**: Only validates checksums without publishing
   - **--auto-create**: Automatically creates GitHub Release using gh CLI
7. **Generates Metadata**: Creates publication records for auditing
8. **Reports Results**: Returns publication status with paths and checksums

## Usage

### Basic Usage (Local Target)

```bash
python skills/plugin.publish/plugin_publish.py dist/betty-framework-1.0.0.tar.gz
```

Publishes with defaults:
- Target: `local` (dist/published/)
- Checksum validation: Auto-detected from manifest.json

### Via Betty CLI

```bash
/plugin/publish dist/betty-framework-1.0.0.tar.gz
```

### Publish to Specific Target

```bash
# Publish to local directory
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=local

# Publish to Claude Marketplace (simulated)
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace

# Prepare GitHub Release (files only, manual creation needed)
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=gh-release

# Create GitHub Release automatically using gh CLI
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=gh-release \
  --auto-create
```

### Dry Run and Validation Modes

```bash
# Dry run - show what would happen without making changes
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace \
  --dry-run

# Validate only - check checksums without publishing
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --validate-only

# Dry run with GitHub Release
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=gh-release \
  --auto-create \
  --dry-run
```

### With Explicit Checksum Validation

```bash
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=local \
  --sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### With Custom Manifest Path

```bash
python skills/plugin.publish/plugin_publish.py \
  /tmp/betty-framework-1.0.0.tar.gz \
  --target=release \
  --manifest=/tmp/manifest.json
```

### With Custom Marketplace Endpoint

```bash
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace \
  --endpoint=https://api.example.com/plugins/upload
```

## Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `package_path` | Positional | Required | Path to the .tar.gz package file |
| `--target` | Option | `local` | Publication target: `local`, `marketplace`, or `gh-release` |
| `--sha256` | Option | Auto-detect | Expected SHA256 checksum for validation |
| `--manifest` | Option | Auto-detect | Path to manifest.json |
| `--endpoint` | Option | Claude Marketplace | Marketplace API endpoint URL (for `marketplace` target) |
| `--dry-run` | Flag | False | Show what would be done without making changes |
| `--validate-only` | Flag | False | Only validate checksums without publishing |
| `--auto-create` | Flag | False | Automatically create GitHub Release using gh CLI (for `gh-release` target) |

## Publication Targets

### Local Target

**Purpose**: Copy package to local published directory for testing, archival, or internal distribution.

**Output Location**: `dist/published/`

**Generated Files**:
- `{package-name}.tar.gz` - Copied package file
- `{package-name}.tar.gz.publish.json` - Publication metadata

**Use Cases**:
- Local testing before remote publication
- Internal company archives
- Offline distribution
- Backup copies

**Example**:
```bash
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=local
```

**Output**:
```
dist/published/
├── betty-framework-1.0.0.tar.gz
└── betty-framework-1.0.0.tar.gz.publish.json
```

### Marketplace Target

**Purpose**: Upload plugin metadata to Claude Marketplace API endpoint (currently simulated).

**Output Location**: `dist/published/marketplace/`

**Generated Files**:
- `{package-name}.tar.gz.marketplace-publish.json` - Simulation log with request/response

**Use Cases**:
- Publish to Claude Code Marketplace
- Upload to custom plugin repository
- Submit to enterprise plugin registry

**Current Implementation**: SIMULATED
- Generates complete HTTP POST request with JSON metadata
- Returns mock successful response
- No actual network request made
- Ready for real implementation (add requests library)

**Example**:
```bash
# Standard marketplace publication (simulated)
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace

# With custom endpoint
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace \
  --endpoint=https://marketplace.claude.ai/api/v1/plugins

# Dry run first to see what would happen
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace \
  --dry-run
```

**JSON Metadata Structure**:
```json
{
  "plugin": {
    "name": "betty-framework",
    "version": "1.0.0",
    "description": "...",
    "author": { ... },
    "license": "MIT",
    "homepage": "...",
    "repository": "...",
    "tags": [...],
    "betty_version": ">=0.1.0"
  },
  "package": {
    "filename": "betty-framework-1.0.0.tar.gz",
    "size_bytes": 524288,
    "checksums": {
      "md5": "...",
      "sha256": "..."
    }
  },
  "submitted_at": "2025-10-24T12:00:00.000000+00:00"
}
```

### GitHub Release Target

**Purpose**: Create GitHub Releases with auto-generated release notes and automatic upload support.

**Output Location**: `dist/published/releases/`

**Generated Files**:
- `{package-name}.tar.gz` - Copied package file
- `RELEASE_NOTES_v{version}.md` - Auto-generated release notes
- `{package-name}.tar.gz.release.json` - Release metadata

**Use Cases**:
- GitHub Releases publication (manual or automatic)
- Public open-source distribution
- Versioned releases with auto-generated notes
- Official product releases

**Modes**:
1. **Preparation Only** (default): Prepares files for manual release creation
2. **Automatic Creation** (`--auto-create`): Uses gh CLI to create release automatically

**Examples**:
```bash
# Prepare release files only (manual upload needed)
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=gh-release

# Automatically create GitHub Release using gh CLI
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=gh-release \
  --auto-create

# Dry run to see what would be created
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=gh-release \
  --auto-create \
  --dry-run
```

**Requirements for Auto-Create**:
- GitHub CLI (`gh`) must be installed
- Must be authenticated: `gh auth login`
- Must have write access to repository
- Tag must not already exist

**Output**:
```
dist/published/releases/
├── betty-framework-1.0.0.tar.gz
├── RELEASE_NOTES_v1.0.0.md
└── betty-framework-1.0.0.tar.gz.release.json
```

## Operating Modes

### Dry Run Mode (`--dry-run`)

**Purpose**: Test publication without making any changes

**Behavior**:
- Validates package and checksums
- Shows all operations that would be performed
- Does NOT create files, directories, or network requests
- Does NOT create GitHub Releases
- Returns success if all validation passes

**Use Cases**:
- Test before actual publication
- Verify configuration is correct
- Preview what will happen
- CI/CD validation steps

**Example**:
```bash
# Test local publication
python skills/plugin.publish/plugin_publish.py \
  dist/betty-1.0.0.tar.gz \
  --target=local \
  --dry-run

# Test marketplace publication
python skills/plugin.publish/plugin_publish.py \
  dist/betty-1.0.0.tar.gz \
  --target=marketplace \
  --dry-run

# Test GitHub Release creation
python skills/plugin.publish/plugin_publish.py \
  dist/betty-1.0.0.tar.gz \
  --target=gh-release \
  --auto-create \
  --dry-run
```

**Output Example**:
```
🔍 DRY RUN MODE - No changes will be made
📦 Publishing to local directory...
  Would create directory: /home/user/betty/dist/published
  Would copy: /home/user/betty/dist/betty-1.0.0.tar.gz
  To:      /home/user/betty/dist/published/betty-1.0.0.tar.gz
  Would write metadata to: /home/user/betty/dist/published/betty-1.0.0.tar.gz.publish.json
✅ Dry run completed successfully
```

### Validate Only Mode (`--validate-only`)

**Purpose**: Validate package integrity without publishing

**Behavior**:
- Validates package file exists
- Calculates MD5 and SHA256 checksums
- Compares against expected checksums from manifest.json
- Exits immediately after validation
- Does NOT publish to any target

**Use Cases**:
- Verify package integrity before distribution
- CI/CD checksum validation
- Security audits
- Package verification after download

**Example**:
```bash
# Validate package checksums
python skills/plugin.publish/plugin_publish.py \
  dist/betty-1.0.0.tar.gz \
  --validate-only
```

**Output Example**:
```
🔍 VALIDATE ONLY MODE ENABLED

📦 Package: dist/betty-1.0.0.tar.gz
🎯 Target:  local
📄 Manifest: dist/manifest.json

🔍 Validating package checksums...
🔐 Calculating checksums...
  MD5:    d41d8cd98f00b204e9800998ecf8427e
  SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
✅ SHA256 checksum validation: PASSED

================================================================================
✅ VALIDATION SUCCESSFUL
================================================================================

Package is valid and ready for publication.
To publish, run without --validate-only flag:
  python skills/plugin.publish/plugin_publish.py dist/betty-1.0.0.tar.gz --target=local
```

**Note**: `--validate-only` takes precedence over `--dry-run` if both are specified.

## Output Files

### Publication Metadata (Local Target)

**File**: `{package-name}.tar.gz.publish.json`

**Structure**:
```json
{
  "published_at": "2025-10-24T12:00:00.000000+00:00",
  "target": "local",
  "package": {
    "filename": "betty-framework-1.0.0.tar.gz",
    "path": "/home/user/betty/dist/published/betty-framework-1.0.0.tar.gz",
    "size_bytes": 524288,
    "checksums": {
      "md5": "d41d8cd98f00b204e9800998ecf8427e",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  },
  "metadata": {
    "name": "betty-framework",
    "version": "1.0.0",
    "description": "Betty Framework is RiskExec's system...",
    "author": {
      "name": "RiskExec",
      "email": "platform@riskexec.com"
    },
    "license": "MIT"
  }
}
```

### Marketplace Publication Simulation Log

**File**: `{package-name}.tar.gz.marketplace-publish.json`

**Structure**:
```json
{
  "simulated_at": "2025-10-24T12:00:00.000000+00:00",
  "target": "marketplace",
  "endpoint": "https://marketplace.claude.ai/api/v1/plugins",
  "request": {
    "method": "POST",
    "url": "https://marketplace.claude.ai/api/v1/plugins",
    "headers": {
      "Content-Type": "application/json",
      "X-Plugin-Name": "betty-framework",
      "X-Plugin-Version": "1.0.0",
      "X-Package-SHA256": "..."
    },
    "json": {
      "plugin": { ... },
      "package": { ... },
      "submitted_at": "..."
    }
  },
  "response": {
    "status": 200,
    "body": {
      "success": true,
      "message": "Plugin published successfully",
      "plugin": {
        "id": "betty-framework-1.0.0",
        "name": "betty-framework",
        "version": "1.0.0",
        "published_at": "2025-10-24T12:00:00.000000+00:00",
        "download_url": "...",
        "listing_url": "https://marketplace.claude.ai/plugins/betty-framework"
      },
      "checksums": { ... }
    }
  },
  "dry_run": false,
  "note": "This is a simulated request. No actual HTTP request was made. To enable real publication, add requests library implementation."
}
```

### GitHub Release Notes

**File**: `RELEASE_NOTES_v{version}.md`

**Auto-generated Content**:
```markdown
# betty-framework v1.0.0

## Release Information

- **Version:** 1.0.0
- **Released:** 2025-10-24
- **Package:** `betty-framework-1.0.0.tar.gz`

## Checksums

Verify the integrity of your download:

```
MD5:    d41d8cd98f00b204e9800998ecf8427e
SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

## Installation

1. Download the package: `betty-framework-1.0.0.tar.gz`
2. Verify checksums (see above)
3. Extract: `tar -xzf betty-framework-1.0.0.tar.gz`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: Follow instructions in README.md

## Description

Betty Framework is RiskExec's system for structured, auditable AI-assisted engineering...

## GitHub CLI Commands

To create this release using GitHub CLI:

```bash
# Create release
gh release create v1.0.0 \
  --title "betty-framework v1.0.0" \
  --notes-file RELEASE_NOTES.md \
  betty-framework-1.0.0.tar.gz
```

## Manual Upload

1. Go to: https://github.com/YOUR_ORG/YOUR_REPO/releases/new
2. Tag version: `v1.0.0`
3. Release title: `betty-framework v1.0.0`
4. Upload: `betty-framework-1.0.0.tar.gz`
5. Add checksums to release notes
6. Publish release
```

### Release Metadata

**File**: `{package-name}.tar.gz.release.json`

**Structure**:
```json
{
  "prepared_at": "2025-10-24T12:00:00.000000+00:00",
  "target": "gh-release",
  "version": "1.0.0",
  "name": "betty-framework",
  "package": {
    "filename": "betty-framework-1.0.0.tar.gz",
    "path": "/home/user/betty/dist/published/releases/betty-framework-1.0.0.tar.gz",
    "size_bytes": 524288,
    "checksums": {
      "md5": "...",
      "sha256": "..."
    }
  },
  "release_notes_path": "/home/user/betty/dist/published/releases/RELEASE_NOTES_v1.0.0.md",
  "github_cli_command": "gh release create v1.0.0 --title \"betty-framework v1.0.0\" --notes-file ...",
  "metadata": {
    "name": "betty-framework",
    "version": "1.0.0",
    "description": "...",
    "author": { ... },
    "license": "MIT"
  },
  "dry_run": false,
  "auto_created": true,
  "github_release_url": "https://github.com/user/repo/releases/tag/v1.0.0"
}
```

**Note**: The `auto_created` field is `true` if `--auto-create` was used and succeeded, and `github_release_url` will contain the actual release URL.

## Checksum Validation

### Automatic Validation

By default, `plugin.publish` automatically detects and validates checksums from `manifest.json`:

```bash
python skills/plugin.publish/plugin_publish.py dist/betty-framework-1.0.0.tar.gz
```

**Process**:
1. Looks for `dist/manifest.json`
2. Extracts `package.checksums.sha256`
3. Calculates actual SHA256 of package file
4. Compares and validates

### Manual Validation

Explicitly provide expected SHA256:

```bash
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### Validation Output

**Success**:
```
🔍 Validating package checksums...
🔐 Calculating checksums...
  MD5:    d41d8cd98f00b204e9800998ecf8427e
  SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
✅ SHA256 checksum validation: PASSED
```

**Failure**:
```
🔍 Validating package checksums...
🔐 Calculating checksums...
  MD5:    d41d8cd98f00b204e9800998ecf8427e
  SHA256: abc123...
❌ SHA256 checksum validation: FAILED
  Expected: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  Actual:   abc123...
```

## Workflow Integration

### Complete Build and Publish Pipeline

```bash
# Step 1: Build plugin
python skills/plugin.build/plugin_build.py

# Step 2: Validate package integrity
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --validate-only

# Step 3: Dry run to test publication
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=local \
  --dry-run

# Step 4: Publish to local for testing
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=local

# Step 5: Publish to Claude Marketplace (simulated)
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace

# Step 6: Create GitHub Release automatically
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=gh-release \
  --auto-create
```

### Safe Publication Workflow (Recommended)

```bash
# 1. Validate first
python skills/plugin.publish/plugin_publish.py \
  dist/betty-1.0.0.tar.gz \
  --validate-only

# 2. Dry run to preview
python skills/plugin.publish/plugin_publish.py \
  dist/betty-1.0.0.tar.gz \
  --target=marketplace \
  --dry-run

# 3. Actual publication
python skills/plugin.publish/plugin_publish.py \
  dist/betty-1.0.0.tar.gz \
  --target=marketplace
```

### Automated CI/CD Integration

```yaml
# .github/workflows/publish.yml
name: Publish Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Build plugin
        run: python skills/plugin.build/plugin_build.py

      - name: Validate package
        run: |
          python skills/plugin.publish/plugin_publish.py \
            dist/betty-framework-*.tar.gz \
            --validate-only

      - name: Publish to Claude Marketplace
        run: |
          python skills/plugin.publish/plugin_publish.py \
            dist/betty-framework-*.tar.gz \
            --target=marketplace

      - name: Create GitHub Release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          python skills/plugin.publish/plugin_publish.py \
            dist/betty-framework-*.tar.gz \
            --target=gh-release \
            --auto-create
```

### CI/CD with Dry Run Testing

```yaml
# .github/workflows/test-publish.yml
name: Test Publication

on:
  pull_request:
    branches: [main]

jobs:
  test-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build plugin
        run: python skills/plugin.build/plugin_build.py

      - name: Validate package
        run: |
          python skills/plugin.publish/plugin_publish.py \
            dist/betty-framework-*.tar.gz \
            --validate-only

      - name: Test local publish (dry run)
        run: |
          python skills/plugin.publish/plugin_publish.py \
            dist/betty-framework-*.tar.gz \
            --target=local \
            --dry-run

      - name: Test marketplace publish (dry run)
        run: |
          python skills/plugin.publish/plugin_publish.py \
            dist/betty-framework-*.tar.gz \
            --target=marketplace \
            --dry-run

      - name: Test GitHub Release (dry run)
        run: |
          python skills/plugin.publish/plugin_publish.py \
            dist/betty-framework-*.tar.gz \
            --target=gh-release \
            --auto-create \
            --dry-run
```

## Error Handling

### Package Not Found

```
❌ Package file not found: /path/to/missing.tar.gz
```

**Solution**: Verify package path and run `plugin.build` first.

### Invalid Target

```
❌ Invalid target: prod. Must be one of: local, marketplace, gh-release
```

**Solution**: Use one of the valid target values: `local`, `marketplace`, or `gh-release`.

### Checksum Validation Failed

```
❌ SHA256 checksum validation: FAILED
```

**Solution**: Package may be corrupted. Rebuild using `plugin.build`.

### Manifest Not Found

```
⚠️  Manifest not found: /path/to/manifest.json
⚠️  No expected checksum provided - skipping validation
```

**Solution**: Provide `--manifest` path or place manifest.json in package directory.

## Advanced Usage

### Publishing to Multiple Targets

```bash
#!/bin/bash
PACKAGE="dist/betty-framework-1.0.0.tar.gz"

# Validate first
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --validate-only

# Publish to all targets
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=local
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=marketplace
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=gh-release --auto-create

echo "Published to all targets successfully!"
```

### Custom Endpoint Configuration

```bash
# Development marketplace endpoint
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace \
  --endpoint=https://dev.marketplace.claude.ai/api/v1/plugins

# Production marketplace endpoint
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --target=marketplace \
  --endpoint=https://marketplace.claude.ai/api/v1/plugins
```

### Safe Publication with Validation

```bash
#!/bin/bash
PACKAGE="dist/betty-framework-1.0.0.tar.gz"

# Step 1: Validate checksums
echo "Validating package..."
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --validate-only || exit 1

# Step 2: Dry run for all targets
echo "Running dry runs..."
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=local --dry-run || exit 1
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=marketplace --dry-run || exit 1
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=gh-release --auto-create --dry-run || exit 1

# Step 3: Actual publication
echo "Publishing..."
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=local
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=marketplace
python skills/plugin.publish/plugin_publish.py "$PACKAGE" --target=gh-release --auto-create

echo "All publications completed successfully!"
```

### Verification After Publication

```bash
# Local verification
cd dist/published
sha256sum -c <<< "e3b0c44... betty-framework-1.0.0.tar.gz"

# Extract and inspect
tar -tzf betty-framework-1.0.0.tar.gz | head -20

# Validate manifest
cat betty-framework-1.0.0.tar.gz.publish.json | jq .
```

## Dependencies

- **Python**: 3.11+
- **Standard Library**: os, sys, json, yaml, hashlib, shutil, pathlib, datetime
- **Betty Modules**: betty.config
- **Future**: requests (for actual remote publication)

## Related Skills

- **plugin.build**: Build plugin packages before publishing
- **plugin.sync**: Synchronize plugin.yaml from skill registry
- **registry.update**: Update skill registry entries
- **audit.log**: Log publication events for governance

## Security Considerations

### Checksum Validation

Always validate SHA256 checksums before publication:
- Detects package corruption
- Prevents tampering
- Ensures integrity across distribution channels

### Publication Tracking

All publications are logged with:
- Timestamp (UTC)
- Target destination
- Checksums
- Package metadata

This creates an audit trail for governance and compliance.

### Remote Publication (When Implemented)

For actual remote publication:
- Use HTTPS endpoints only
- Authenticate with API tokens (not in source code)
- Verify TLS certificates
- Implement retry logic with exponential backoff
- Log all API responses

## Troubleshooting

### Issue: Checksum mismatch after build

**Symptom**: SHA256 validation fails immediately after building

**Causes**:
- Manifest.json not generated by plugin.build
- Package file modified after build
- Incorrect manifest path

**Solution**:
```bash
# Rebuild package
python skills/plugin.build/plugin_build.py

# Verify manifest exists
ls -la dist/manifest.json

# Publish with explicit manifest
python skills/plugin.publish/plugin_publish.py \
  dist/betty-framework-1.0.0.tar.gz \
  --manifest=dist/manifest.json
```

### Issue: Marketplace publication not actually uploading

**Symptom**: No network error but file not on marketplace

**Cause**: Marketplace publication is currently SIMULATED

**Solution**: This is expected behavior. The simulation creates a complete request structure in:
```
dist/published/marketplace/{package}.marketplace-publish.json
```

For actual HTTP upload, add requests library implementation in `publish_marketplace()`.

### Issue: GitHub Release fails

**Symptom**: `gh release create` command fails

**Causes**:
- GitHub CLI not installed
- Not authenticated with GitHub
- Tag already exists
- No write access to repository

**Solutions**:
```bash
# Install GitHub CLI
# macOS: brew install gh
# Linux: sudo apt install gh

# Authenticate
gh auth login

# Check existing releases
gh release list

# Delete existing tag if needed
gh release delete v1.0.0
git push --delete origin v1.0.0
```

## Best Practices

1. **Use validate-only first**: Always run `--validate-only` before publishing to verify package integrity
2. **Dry run before publishing**: Use `--dry-run` to test publication workflows without making changes
3. **Test locally first**: Publish to `--target=local` before marketplace or GitHub Release
4. **Review release notes**: Check auto-generated notes in `dist/published/releases/RELEASE_NOTES_*.md`
5. **Keep publication metadata**: Retain `.json` files for audit trails and compliance
6. **Use version tags consistently**: Follow semantic versioning (e.g., v1.0.0 format)
7. **Automate via CI/CD**: Use GitHub Actions for consistent, reproducible releases
8. **Verify gh CLI setup**: Test `gh auth status` before using `--auto-create`
9. **Backup published packages**: Keep copies for disaster recovery
10. **Use safe publication workflow**: Validate → Dry run → Local → Remote → Release

## Future Enhancements

- [ ] Actual HTTP POST implementation for marketplace target (add requests library)
- [ ] Support for multiple marketplace endpoints (dev, staging, prod)
- [ ] Digital signature support for package verification (GPG signing)
- [ ] Publication rollback mechanism for failed releases
- [ ] Automatic changelog generation from git commits
- [ ] Publication analytics and download tracking
- [ ] Multi-target parallel publication (async)
- [ ] Package verification after publication (download and verify checksums)
- [ ] Support for pre-release and draft GitHub Releases
- [ ] Integration with artifact registries (JFrog, Nexus)
- [ ] Webhook notifications on successful publication
- [ ] Support for package mirroring across multiple registries

---

**Generated by**: Betty Framework
**Version**: 0.1.0
**Last Updated**: 2025-10-24
