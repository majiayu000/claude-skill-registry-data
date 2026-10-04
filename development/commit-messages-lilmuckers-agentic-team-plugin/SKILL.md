---
name: commit-messages
description: Write clear commit messages for software delivery work. Use when preparing git commits and the team needs a consistent style for subject lines, explanatory bodies, and commit scoping.
---

# Commit Messages

Write commits so a future reviewer can understand the intent quickly.

## Format
- Subject line first
- Optional body for rationale, scope, or caveats

## Subject line guidance
- Use imperative mood
- Keep it specific
- Prefer one clear change per commit
- Avoid generic subjects like `misc changes`

## Examples
- `Add staged deployment manifest for framework sync`
- `Define QA approval contract for delivery agents`
- `Scaffold initial orchestrator and builder roles`

## Body guidance
Use a body when the why is not obvious from the diff.

Include:
- motivation
- major scope notes
- important limitations or follow-ups
