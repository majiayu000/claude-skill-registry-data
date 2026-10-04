---
name: woz-logout
description: Clear stored Woz credentials and log out.
allowed-tools: Bash(node *)
---

Log out of Woz by clearing stored credentials:

```bash
node "${CODEX_HOME:-$HOME/.codex}/plugins/wozcode/scripts/wozcode-cli-codex.js" logout
```

Confirm that the user has been logged out.
