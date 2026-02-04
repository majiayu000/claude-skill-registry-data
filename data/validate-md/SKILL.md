---
name: validate-md
description: Validates markdown files with YAML frontmatter against JSON Schema definitions.
allowed-tools: [Bash, Read, Glob]
---

# Validating Markdown Files

## Instructions

1. **Run validation script** for the target directory containing a `schema.yaml` file:
   ```bash
   python validate-md.py <directory>
   ```

2. **Review results**:
   - Success: `✓ OK: filename.md is valid`
   - Errors: Shows validation error, field path, and file location

## Examples

**Example 1: Validate contacts directory**
```bash
python validate-md.py crm/contacts
```

Output:
```
✓ OK: smith-john.md is valid
✓ OK: doe-jane.md is valid
✓ SUCCESS: All 2 files are valid!
```

**Example 2: Validation error - missing required field**
```bash
python validate-md.py crm/opportunities
```

Output:
```
❌ deal-2024-q1.md validation error: 'stage' is a required property
   In file: crm/opportunities/deal-2024-q1.md
```

Fix: Add `stage: qualified` to the frontmatter.

## Scripts

- `validate-md.py` the python validation script

## Required Python Packages

- pyyaml - for parsing YAML frontmatter
- jsonschema - for validating against JSON Schema
