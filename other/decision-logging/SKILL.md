---
name: decision-logging
description: While working, keep a log of every decision the agent makes that the user did not explicitly specify. Use on any multi-step task, or when the user asks for a decision log / "why did you do X".
---

# Decision Logging

Every choice the user did not explicitly dictate gets a log entry, written at the moment you decide — not batched at the end.

## Log

- File: `DECISIONS.md` in the project root (create on first entry). Append chronologically.

```markdown
## <short title>
- Decision: what you chose
- Why: reasoning / what you observed
- Rejected: alternatives that lost, and why
```

## Counts

- Naming things, picking an approach/library/flag, choosing scope or defaults, **resolving ambiguity by assuming** (most important).

## Doesn't count

- Anything the user explicitly specified, mechanical consequences, trivial syntax.

## Rules

- If you change an earlier decision, append a new entry referencing it — never rewrite history.
- At completion, summarize the entries the user should review; keep it under 10 lines.
