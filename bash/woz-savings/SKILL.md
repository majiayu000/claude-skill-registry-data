---
name: woz-savings
description: Show WOZCODE savings report - calls saved, time saved, tokens saved, and lifetime totals.
allowed-tools: Bash(node *)
---

Run the WOZCODE savings report:

```bash
node "${CODEX_HOME:-$HOME/.codex}/plugins/wozcode/scripts/savings-report.js"
```

Relay the full output to the user. Do not summarize or modify it.
