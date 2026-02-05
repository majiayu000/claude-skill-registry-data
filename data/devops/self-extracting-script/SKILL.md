---
name: self-extracting-script
description: Create self-extracting Bash scripts that embed any payload (archives, executables, configs) using base64 encoding. Use when creating portable single-file installers, deployment packages, or distributing files without external dependencies.
---

# Self-Extracting Script Skill

Generate self-extracting Bash scripts from any payload file. The generated scripts embed the payload as base64 and extract it when executed.

## Quick Start

```bash
# Basic extraction script
python scripts/create_self_extractor.py payload.tar.gz output.sh

# Auto-execute after extraction
python scripts/create_self_extractor.py setup.sh installer.sh --execute

# Custom output filename
python scripts/create_self_extractor.py config.json deploy.sh --output prod_config.json
```

## Features

- Embeds any file type (binary or text) using base64 encoding
- Optional auto-execution of extracted content
- Custom output filenames
- Descriptive headers in generated scripts
- Portable - requires only bash and base64

## Usage

```bash
python scripts/create_self_extractor.py <payload> <output_script> [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `payload` | Path to the file to embed |
| `output_script` | Path for the generated self-extracting script |

### Options

| Option | Description |
|--------|-------------|
| `--execute`, `-e` | Run extracted file after extraction (for scripts) |
| `--output`, `-o` | Custom filename for extracted content |
| `--description`, `-d` | Description to include in script header |

## Examples

### Software Deployment
```bash
python scripts/create_self_extractor.py myapp.tar.gz deploy_myapp.sh \
    --description "MyApp v1.2.3 deployment package"
```

### Auto-Running Installer
```bash
python scripts/create_self_extractor.py install.sh installer.sh --execute
```

### Configuration Distribution
```bash
python scripts/create_self_extractor.py config.yaml setup.sh \
    --output /etc/myapp/config.yaml
```

## How It Works

1. Reads the payload file (binary or text)
2. Base64-encodes the content
3. Generates a Bash script with embedded payload
4. Script uses heredoc to safely store encoded data
5. On execution: decodes payload → writes to file → optionally executes

## Size Considerations

Base64 encoding increases size by ~33%:
- 1 MB → ~1.33 MB
- 10 MB → ~13.3 MB

For payloads >50MB, consider alternative distribution methods.

## Dependencies

**Generation:** Python 3.6+
**Execution:** bash, base64 (standard on most Unix systems)
