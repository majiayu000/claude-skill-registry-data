---
name: eco-audit
description: Audit this machine's Claude Code configuration for token waste - effort level, oversized CLAUDE.md files, MCP servers, tool-output caps, env keys that do nothing, startup skill load - and print the exact settings.json edit that fixes each finding. Read-only; it never writes settings. Use when the user asks why their usage or bill is high, or wants a config, context or startup-cost checkup, in any language.
argument-hint: "[--json]"
allowed-tools: Bash(node "${CLAUDE_PLUGIN_ROOT}/scripts/audit.mjs" *), Bash(node *audit.mjs *)
---

# Eco audit - read-only configuration audit

Run this once, from the user's project directory:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/audit.mjs" $ARGUMENTS
```

Then:
- The script's table and settings diff are already on the user's screen as the command's output. **Do not reprint them** - repeating output the user can already see is exactly the waste this plugin exists to remove. Never re-summarise, re-sort or re-word the rows either: the numbers and the "est" labels are the product, and a paraphrase of them is a worse product.
- Add at most 3 lines of your own: which finding to fix first, and why.
- Never apply the diff here. Applying it is `/eco setup`, which shows the diff and waits for the user to confirm. Say so and stop.
- If `${CLAUDE_PLUGIN_ROOT}` did not expand (the path still contains that literal text), this is a personal or project install rather than a plugin: run `audit.mjs` from **this skill's own directory** - the installer stages it there - and if it is missing, `scripts/audit.mjs` in the claude-code-eco checkout.
