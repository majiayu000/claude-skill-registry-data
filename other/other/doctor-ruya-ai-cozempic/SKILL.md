---
name: doctor
description: Run health checks on Claude Code configuration and sessions. Use when troubleshooting Claude Code issues.
allowed-tools: Bash(cozempic *)
---

Run cozempic health checks:

```bash
cozempic doctor
```

Checks for:
- **Trust dialog hang** — Windows resume bug where `.claude.json` trust entry causes hangs
- **Oversized sessions** — sessions that may trigger compaction issues
- **Stale backups** — old `.bak` files consuming disk space
- **Disk usage** — total Claude Code storage footprint

To auto-fix detected issues:
```bash
cozempic doctor --fix
```
