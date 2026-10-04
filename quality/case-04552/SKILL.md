---
name: json-linter
description: Validates JSON syntax across the workspace. Use this skill to check for syntax errors in configuration files, memory files, or data assets.
---




### Cleanup Review

`python scripts/_cleanup.py` is an optional cleanup helper for the `JSON Linter` skill. It may recursively remove /var/tmp/skill_output. Show the exact paths first, explain whether they are skill-private temporary paths or user state, and run the cleanup only after the user confirms.

# JSON Linter

A simple utility to recursively scan the workspace for `.json` files and validate their syntax using `JSON.parse()`.

## Usage

```bash
# Scan the entire workspace (from current working directory)
node skills/json-linter/index.js

# Scan a specific directory
node skills/json-linter/index.js --dir path/to/dir
```

## Output

JSON report containing:
- `scanned_at`: Timestamp
- `total_files`: Number of `.json` files scanned
- `valid_files`: Number of valid files
- `invalid_files`: Number of invalid files
- `errors`: Array of error objects:
  - `path`: Relative path to file
  - `error`: Error message (e.g., "Unexpected token } in JSON at position 42")

## Example Output

```json
{
  "scanned_at": "2026-02-14T21:45:00.000Z",
  "total_files": 150,
  "valid_files": 149,
  "invalid_files": 1,
  "errors": [
    {
      "path": "config/broken.json",
      "error": "Unexpected token } in JSON at position 42"
    }
  ]
}
```
