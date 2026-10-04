---
name: woz-update
description: Update the WOZCODE Codex plugin to the latest published version.
allowed-tools: Bash(npx *)
---

# Update WOZCODE Codex Plugin

Update the local WOZCODE Codex plugin installation from the published package:

```bash
npx @wozcode/codex update
```

After the command succeeds, tell the user WOZCODE for Codex was updated successfully and restart Codex if the current session does not pick up the new plugin files.
