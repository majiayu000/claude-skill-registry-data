---
name: tilt-logs
description: Query logs from Tilt local_resource processes with time-based filtering. Use when debugging Tilt services, viewing recent logs, streaming logs in follow mode, or filtering logs by resource name. Triggers on "tilt logs", "check tilt output", "what's happening in [resource]", "debug tilt", or any log inspection for Tilt-managed processes.
---

# tilt-logs

Enhanced log viewing for Tilt with `--since`, `--tail`, and `-f` filtering that native `tilt logs` lacks.

## Quick Reference

```bash
# View logs from specific resource
tilt-logs <resource>

# Filter by time (5m, 1h, 30s, 1d)
tilt-logs <resource> --since 5m

# Last N lines
tilt-logs --tail 100

# Stream logs (follow mode)
tilt-logs -f
tilt-logs <resource> -f

# JSON output for parsing
tilt-logs --json | jq .

# Custom Tilt instance
tilt-logs --host 192.168.1.100 --port 10351
```

## Environment Variables

- `TILT_HOST` - Tilt API host (default: localhost)
- `TILT_PORT` - Tilt API port (default: 10350)

## Common Patterns

**Debug recent failures:**
```bash
tilt-logs <resource> --since 5m
```

**Check startup logs:**
```bash
tilt-logs <resource> --tail 50
```

**Monitor live output:**
```bash
tilt-logs <resource> -f
```

**Parse structured output:**
```bash
tilt-logs --json --since 1h | jq 'select(.level == "error")'
```

## Options

| Flag | Short | Description |
|------|-------|-------------|
| `--since <dur>` | `-s` | Show logs since duration (5m, 1h, 30s) |
| `--tail <num>` | `-n` | Show last N log lines |
| `--follow` | `-f` | Stream new logs |
| `--json` | | Output as JSON lines |
| `--no-color` | | Disable colored output |
| `--host <host>` | | Tilt host |
| `--port <port>` | | Tilt port |
| `--help` | `-h` | Show help |
