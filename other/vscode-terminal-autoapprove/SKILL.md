---
name: vscode-terminal-autoapprove
description: Guidance on configuring VS Code's terminal auto-approve settings for commands with dynamic arguments.
---

# VS Code Terminal Auto-Approve Configuration

This skill provides domain-specific knowledge on how to configure VS Code to automatically approve terminal commands, especially those with dynamic arguments (like running Python scripts with parameters).

## Overview

VS Code allows auto-approving terminal commands executed via Copilot Chat. This reduces manual confirmations for trusted operations.

## Configuration Steps

### 1. Enable Global Auto-Approve
Add the following to your `settings.json`:
```json
"chat.tools.terminal.enableAutoApprove": true
```

### 2. Configure Rules
Define which commands are auto-approved in the `chat.tools.terminal.autoApprove` object.

#### Simple Command Matching
To approve all instances of a command (e.g., `python`):
```json
"chat.tools.terminal.autoApprove": {
  "python": true
}
```

#### Regex Pattern Matching (Advanced)
To approve only specific scripts or paths:
```json
"chat.tools.terminal.autoApprove": {
  "/^python\\s+skills\\//": true
}
```

## Troubleshooting
- **Command mismatch**: Ensure the command string matches what's typed or called (e.g., `python` vs `python3`).
- **Restart requirement**: Restart VS Code or reload the window after updating `settings.json`.

## References
For more detailed instructions, see [references/how-to-configure-vscode-terminal-autoapprove.md](references/how-to-configure-vscode-terminal-autoapprove.md).
