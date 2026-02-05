---
name: cask
description: Async via cask, end turn immediately; use only when user explicitly delegates to Codex (ask/@codex/let codex/review); NOT for questions about Codex itself.
---

# Ask Codex (Async)

Send the user’s request to Codex asynchronously.

## Execution (MANDATORY)

```
Bash(cask <<'EOF'
$ARGUMENTS
EOF
, run_in_background=true)
```

## CRITICAL Rules

- Always use `run_in_background=true`.
- After running `cask`, say “Codex processing...” and immediately end your turn.
- Do not wait for results or check status in the same turn.

Details: `~/.claude/skills/docs/async-ask-pattern.md`
