---
name: end-chat
description: "Close an AiGov session by writing a worklog entry, updating STATUS.md, and printing a PR-ready summary with verification and risks. Use when the user asks to wrap up, end the session, or prepare a PR summary."
---

## Write worklog
Create `/docs/worklog/YYYYMMDD-HHMM_<slug>.md`.
Include: brief context, before->after, commands run, results, and next step.

## Update STATUS.md
Add: what changed, why, and what's next.
Include a link to the new worklog entry.

## Output (PR-ready)
- PR title
- Summary bullets
- Verification commands (or "Not run")
- Risks / follow-ups

## Claude artifacts
If any `docs/reviews/*` or `docs/worklog/*` entries were created this session (especially from Claude), link them explicitly in the end-of-session summary and ensure STATUS.md references the newest one.
