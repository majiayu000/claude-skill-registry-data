---
name: openapi-gen
description: Generate and validate Python clients from OpenAPI specs. Use for generation, validation, or troubleshooting.
allowed-tools: Bash, Read, Glob, Grep
---

# OpenAPI Client Generation

## Workflow

1. Activate: `source .venv/bin/activate`
2. Generate: `pyopenapi-gen <spec> --project-root <path> --output-package <pkg> --force --verbose`
3. Validate:
   - Check warnings in output
   - Test: `python -c "from <pkg> import *"`
   - Type check: `mypy <path>/<pkg> --ignore-missing-imports`

## Options

| Option             | Purpose                             |
| ------------------ | ----------------------------------- |
| `--force`          | Overwrite existing files            |
| `--no-postprocess` | Skip Black/mypy (faster iteration)  |
| `--core-package`   | Shared core for multi-client setups |
| `--verbose`        | Show detailed progress              |

## Common Issues

| Symptom         | Fix                                                 |
| --------------- | --------------------------------------------------- |
| Import error    | Check --project-root and --output-package alignment |
| Missing module  | Check --verbose for cycle warnings                  |
| Type error      | Review OpenAPI spec                                 |
| Empty dataclass | Ensure schema has `type` field                      |

## Multi-Client Setup

For shared core module:

```bash
# First client with core
pyopenapi-gen api1.yaml --project-root . --output-package clients.api1 --core-package clients.core

# Additional clients sharing core
pyopenapi-gen api2.yaml --project-root . --output-package clients.api2 --core-package clients.core
```
