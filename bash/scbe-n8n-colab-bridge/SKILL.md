---
name: scbe-n8n-colab-bridge
description: Configure and reuse Google Colab local notebook connection settings for SCBE n8n automation and agent handoff workflows.
---

# SCBE N8N Colab Local Bridge

Use this skill when you have a Colab local connection URL (for example `http://127.0.0.1:8888/?token=...`) and want to safely normalize, validate, and wire it into local n8n automation.

## When to use

- You need Colab pivot knowledge or local notebook runs to feed n8n/SCBE workflows.
- You need a repeatable way to store backend URL + token and validate connectivity.
- You want to sync environment variables for scripts and keep them discoverable.
- You are transitioning between notebook sessions and need a known working backend endpoint.

## Quick Start

1. Parse and validate from Colab local connection URL

```bash
python C:\Users\issda\.codex\skills\scbe-n8n-colab-bridge\scripts\colab_n8n_bridge.py `
  --set \
  --name pivot --backend-url "http://127.0.0.1:8888/?token=YOUR_TOKEN" \
  --n8n-webhook "http://127.0.0.1:5678/webhook/scbe-pivot" \
  --probe
```

2. Export environment for this shell

```bash
python C:\Users\issda\.codex\skills\scbe-n8n-colab-bridge\scripts\colab_n8n_bridge.py --env --name pivot
```

3. Quick connectivity check

```bash
python C:\Users\issda\.codex\skills\scbe-n8n-colab-bridge\scripts\colab_n8n_bridge.py --status --name pivot
```

## Behavior

- Stores profile JSON in:
  - `%USERPROFILE%\\.scbe\\colab_n8n_bridge.json`
- Stores tokens via `src/security/secret_store` with Sacred Tongue tokenization for local offline retention.
- `--set` normalizes URL, strips trailing spaces, validates required token.
- `--set --probe` performs API reachability check against `/api` before save.
- `--status` prints a small JSON summary with masked token preview.
- `--env` prints shell-safe export lines for `SCBE_COLAB_BACKEND_URL`, `SCBE_COLAB_TOKEN`, and optional `N8N_WEBHOOK_URL`.

## Script contract

Use these exact commands from the skill path:

- `--set`: create or update profile
- `--status`: report profile and local config
- `--env`: print export statements
- `--probe`: ping Colab API endpoint and confirm token works

## Security note

This operation uses local credentials only.
Avoid printing full tokens into logs, and regenerate tokens if they are ever exposed.

## Related workflow

- After setup, use existing local n8n orchestration scripts:
  - `scripts/system/smoke_n8n_bridge.ps1`
  - `scripts/system/full_system_smoke.py`
