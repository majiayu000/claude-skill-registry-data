---
name: commit-standards
description: Commit message formatting standards. Use when creating commits or PRs to ensure consistent, high-level messages.
---

## Format

```
<TASKNUMBER|MAINT>: <short description>

- <high-level change 1>
- <high-level change 2>
```

## Rules

- First line: task number, colon, short description (under 72 chars)
- Use `MAINT` as the prefix when the change isn't tied to a task/defect number — never invent one
- Describe WHAT changed and WHY, not HOW
- NO implementation details (no function names, query syntax, line counts)
- NO technical specifics

See [examples.md](examples.md) for good vs bad examples.
