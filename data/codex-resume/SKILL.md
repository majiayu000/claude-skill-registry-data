---
name: codex-resume
description: Use to resume a previous Codex conversation. Triggers on "continue codex", "resume codex", "pick up where codex left off", "continue the codex session".
---

# Codex Resume Skill

Resume a previous Codex conversation session.

## When to Use

- User wants to continue a previous Codex discussion
- Following up on earlier Codex analysis
- Adding to a previous query

## Execution

1. Check if user specified a session ID
2. If no session ID: Run `codex resume --last`
3. If session ID provided: Run `codex resume <session-id>`
4. Continue the conversation

## Response Format

```
**Resuming Codex Session:**
[Session ID being resumed]

**Continued Conversation:**
[Codex's response]

**Session ID:** [id] (for future resumption)
```

## Notes

- Sessions are automatically created by each `codex exec` call
- Session IDs appear in the output of each Codex call
- `--last` resumes the most recent session
