---
name: reset-gpt-budget
description: Reset the GPT usage limit for the Codex CLI interactive session running in tmux. Always ask the user for confirmation ("Are you sure you want to reset the GPT usage?") before proceeding. Use when the user says /reset-gpt-budget, asks to reset GPT usage/budget/quota, mentions running out of GPT usage, or wants to free up the usage limit for codex.
metadata:
  hermes:
    tags: [codex, tmux, gpt, usage, budget]
---

# Reset GPT Budget (Codex Usage Limit)

Use the bundled helper to reset the GPT usage limit for the Codex CLI session:

```bash
/home/chihmin/.pi/agent/skills/reset-gpt-budget/scripts/reset-gpt-budget.sh
```

## Workflow

1. **Always ask the user for confirmation** before running the helper:
   > Are you sure you want to reset the GPT usage?

2. If the user confirms, run the helper script.

3. The helper:
   - Ensures a tmux session named `codex-session` exists (starts `codex` if not running).
   - Sends `/usage` to the session and confirms with `y`.
   - Reports success.

## Guardrails

- **Never** reset the GPT usage without explicit user confirmation.
- Only interact with the `codex-session` tmux session.
- Do not kill or recreate the session unless explicitly requested.
- If the session is not found, create a fresh one and wait for the TUI to fully load before sending commands.
