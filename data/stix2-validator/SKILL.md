---
name: stix2-validator
description: Validate STIX 2.1 JSON files and bundles against the STIX specification. Use when validating threat intelligence data, checking STIX bundle integrity before ingestion, verifying indicator/malware/attack-pattern objects have required fields, or bulk-validating directories of STIX files. Provides detailed error reports showing which objects failed and why.
---

# STIX 2.1 Validator

Validate STIX 2.1 JSON bundles using the official stix2-validator library.

## Requirements

Install the validator library before use:

```bash
pip install stix2-validator --break-system-packages
```

## Usage

### Validate a Single File

```bash
python scripts/validate_stix.py /path/to/bundle.json
```

### Validate a Directory

```bash
python scripts/validate_stix.py /path/to/stix_files/
```

Add `-r` for recursive subdirectory scanning.

### Options

| Option | Description |
|--------|-------------|
| `--strict` | Enable all optional validation checks |
| `--enforce-refs` | Warn when object references don't resolve within the bundle |
| `-r, --recursive` | Recursively validate files in subdirectories |
| `--json` | Output results as JSON for programmatic use |
| `-q, --quiet` | Suppress success messages, show only errors |

### JSON Output

For integration with other tools, use `--json`:

```bash
python scripts/validate_stix.py bundle.json --json
```

Returns structured output:

```json
{
  "file": "bundle.json",
  "valid": false,
  "errors": [
    {"id": "indicator--abc123", "type": "", "message": "'pattern_type' is a required property"}
  ],
  "warnings": []
}
```

## Error Categories

The validator checks for:

- **Schema errors**: Missing required properties, invalid property types
- **Format errors**: Malformed UUIDs, invalid timestamps, incorrect ID formats
- **Reference errors**: Unresolved object references (with `--enforce-refs`)
- **Semantic errors**: Invalid STIX patterns, constraint violations

## Exit Codes

- `0`: All files valid
- `1`: Validation errors found or file not found
