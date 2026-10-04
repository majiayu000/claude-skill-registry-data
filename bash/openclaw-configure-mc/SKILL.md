---
name: openclaw-configure-mc
description: Connect Mission Control to an OpenClaw gateway
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# Configure Mission Control

Connect Mission Control to an OpenClaw gateway and set up the operational surface.

## Process

1. Verify Mission Control is running (`curl http://localhost:8000/health`)
2. Verify OpenClaw gateway is running (`openclaw status`)
3. Read OpenClaw config for gateway URL, port, and auth token
4. Run the fleet setup module (`python3 -m gateway.setup`)
5. Verify: gateway registered in MC, board created, agents registered
6. Check Mission Control UI is accessible

## Rules

- Use the project's setup module, don't curl APIs manually
- All configuration should be in the project's scripts, not ad-hoc
- If MC isn't running, start it via `make mc-up` or `docker compose up -d`