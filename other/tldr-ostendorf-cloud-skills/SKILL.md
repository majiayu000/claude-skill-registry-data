---
name: tldr
description: "Summarizes a finished task, answer or session in at most eight bullets, shaped for a pull request body, an issue comment or a short reply. Use when asked for a tldr, a summary, a status update or a pull request description."
---

# tldr

Summarize finished work so it is actionable in under a minute.

## When to use

- Opening a pull request, reporting progress, answering what changed.
- Unfinished work someone else must resume: use `handoff` instead.

## Steps

1. Pick the audience: pull request body, issue comment, or a chat reply.
2. First line: the outcome. What is now true, not what was attempted.
3. Then what changed and why, grouped by behavior or area, never by file.
4. Then what is left and any decision needed. Nothing left: say so.
5. State verification as fact: what ran, what passed, what was not run.
6. Link issues with `#<number>`. Use `Closes #<number>` in a pull request body.
7. At most eight bullets. Cut to fit, never pad to fit.
8. Never write a version, changelog entry or release note.

## Rules

- One fact per bullet. No multi sentence bullets, no paragraphs.
- No tool names, no step counts, no narration of the process.
- No quality adjectives: not robust, not comprehensive, not clean.
- Numbers instead of vague claims.
- Unverified means unverified. Name what was not run.

## Template

```markdown
<One line outcome.>
- <What changed and why>
- Left: <remaining work, or nothing>
- Needs a decision: <question, or none>
```

## Guardrails

- Outcome first, always.
- Eight bullets maximum, grouped by behavior or area.
- Verification stated honestly, including what was skipped.
