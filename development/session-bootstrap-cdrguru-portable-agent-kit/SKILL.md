---
name: session-bootstrap
description: Initialize a new local session log from the conversation.compact.md.template at the start of a work session.
metadata:
  short-description: Initialize conversation.compact.md for a new session
---

# Session Bootstrap

## When to use
Use at the start of a new session to create a local, gitignored session log.

## Procedure
1. Copy the template to create a local session log:

```bash
cp .agent/conversation.compact.md.template conversation.compact.md
```

2. Add the objective, constraints, and next actions to the new file.
3. Remember that `conversation.compact.md` is gitignored and stays local.

## Inputs and outputs
- Inputs: `.agent/conversation.compact.md.template`
- Outputs: `conversation.compact.md` in the repo root

## Constraints
- Do not commit `conversation.compact.md`
- ASCII-only

## Examples
- $session-bootstrap
