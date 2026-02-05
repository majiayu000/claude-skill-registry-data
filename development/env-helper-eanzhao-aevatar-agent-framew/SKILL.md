---
name: env-helper
description: Read environment variables via get_env tool (mask secrets).
allowed-tools:
  - get_env
---

## When to use
- User asks about an environment variable (e.g. `SHELL`, `PATH`, `HOME`).

## Procedure
1) Decide the env key (ask user if ambiguous).
2) Call `get_env` with the key.
3) If the value looks like a secret (token/key), only return the existence + masked preview.
4) Otherwise, return the value directly.


