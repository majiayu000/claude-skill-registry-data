---
name: woz-status
description: Show current Woz authentication status.
allowed-tools: Bash(node *)
---

Check the current Woz authentication status:

```bash
node "${CODEX_HOME:-$HOME/.codex}/plugins/wozcode/scripts/wozcode-cli-codex.js" status
```

Relay the output to the user.
