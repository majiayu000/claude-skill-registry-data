---
name: ha-sync
description: Sync zen-ui plugin to local Home Assistant. Use when user asks to sync, deploy, or push to HA.
---

# HA Sync

Run from the zen-ui project root:

```bash
just sync-build   # Build and sync
just sync         # Sync only (if already built)
```

After syncing, remind user to hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R).
