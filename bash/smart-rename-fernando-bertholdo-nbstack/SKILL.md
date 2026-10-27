---
name: smart-rename
description: Manage the smart-session-rename plugin — suggest, anchor, freeze, force, explain.
---

# /smart-rename (v1.5)

When the user invokes `/smart-rename [args]`, run the matching command via the Bash tool and report the output verbatim. Pass `$CLAUDE_TRANSCRIPT_PATH` as the last argument.

## Subcommands

### `/smart-rename` — suggest (consumes 1 budget slot)

**IMPORTANT**: This command calls an inner `claude -p` process that takes 30-90 seconds to complete (the child process must initialize its own plugin stack + create prompt cache). You MUST:
1. Run this Bash command in **foreground** (NOT background)
2. Set the Bash tool **timeout to at least 120 seconds**

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/smart-rename-cli.sh "" "$CLAUDE_TRANSCRIPT_PATH" "${CLAUDE_PROJECT_DIR:-$PWD}"
```

### `/smart-rename <name>` — set domain anchor
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/smart-rename-cli.sh "<name>" "$CLAUDE_TRANSCRIPT_PATH"
```

### `/smart-rename freeze` / `unfreeze`
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/smart-rename-cli.sh freeze "$CLAUDE_TRANSCRIPT_PATH"
${CLAUDE_PLUGIN_ROOT}/scripts/smart-rename-cli.sh unfreeze "$CLAUDE_TRANSCRIPT_PATH"
```

### `/smart-rename force`
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/smart-rename-cli.sh force "$CLAUDE_TRANSCRIPT_PATH"
```

### `/smart-rename explain`
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/smart-rename-cli.sh explain "$CLAUDE_TRANSCRIPT_PATH"
```

### `/smart-rename unanchor`
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/smart-rename-cli.sh unanchor "$CLAUDE_TRANSCRIPT_PATH"
```

If the CLI exits non-zero, report the error message verbatim. Do not retry automatically.
