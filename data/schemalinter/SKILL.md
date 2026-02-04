---
name: schema.linter
description: Validate and lint structured data files (YAML, JSON, TOML) for consistency, required fields, syntax errors, and schema compliance.
---

# schema.linter

## Purpose

Validate configuration files, JSON schemas, and structured data files against defined rules to catch errors before runtime. This is a shared skill applicable across all Carbon ACX file types.

## When to Use

**Trigger Patterns:**
- "Validate all config files"
- "Check schemas for errors"
- "Lint JSON/YAML files"
- "Verify wrangler.toml is valid"
- Pre-commit hook integration

**Do NOT Use When:**
- Validating Python/TypeScript code (use language-specific linters)
- Checking CSV data integrity (use data-specific validation)

## Allowed Tools

- `read_file` - Read config files and schemas
- `python` - Parse and validate YAML/JSON/TOML
- `bash` - Run external validators (yamllint, jsonschema)

**Access Level:** 1 (Local Execution - read-only)

## Expected I/O

**Input:**
- File paths or glob patterns
- Example: `"schemas/**/*.json"`, `"wrangler.toml"`, `"config/*.yaml"`

**Output:**
- Validation report with errors/warnings
- File:line references for each issue
- Suggested fixes when possible

## Dependencies

**Required:**
- Python 3.11+ with PyYAML, jsonschema, toml libraries
- Optional: yamllint, prettier (JSON)

**Configuration:**
- `config.json` - Linting rules and schema paths

## Examples

### Example: Validate JSON Schema

**User:** "Use schema.linter to check all config files"

**Output:**
```
✅ config/layers.json - Valid
✅ config/sectors.json - Valid
❌ config/profiles.json - 2 errors:
   Line 15: Missing required field 'profile_id'
   Line 23: Invalid type for 'vintage' (expected integer, got string)

⚠️  schemas/figure-manifest.schema.json - 1 warning:
   Line 45: Description field is empty

Summary: 2 files valid, 1 file with errors, 1 file with warnings
```

## Limitations

- Cannot fix files automatically (reports only)
- Limited to YAML/JSON/TOML formats
- Custom schema definitions required for validation

## Validation Criteria

- ✅ All files parse without syntax errors
- ✅ Required fields present
- ✅ Types match schema definitions
- ✅ No duplicate keys

## Maintenance

**Owner:** Platform Team
**Review Cycle:** Quarterly
**Last Updated:** 2025-10-18
**Version:** 1.0.0
