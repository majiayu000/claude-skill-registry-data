---
name: gstack
description: |
  Root gstack skill.
  Uses ~/.claude/skills/gstack/bin helpers.
allowed-tools:
  - Bash
---

## Preamble (run first)

```bash
_UPD=$(~/.claude/skills/gstack/bin/gstack-update-check 2>/dev/null || .claude/skills/gstack/bin/gstack-update-check 2>/dev/null || true)
```
