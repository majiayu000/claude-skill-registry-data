---
name: hitl-blocker
description: Convert human-only blockers into visible GitHub issues. Use when work is blocked by missing credentials, secrets, DNS, billing, account permissions, approvals, or other user-held external state.
---

# HITL Blocker

Use this before reporting a blocker back to the user.

## Workflow

1. Identify the exact missing human-held item.
2. Create or reuse labels: `HITL task` and `high priority` when launch/work is blocked.
3. Create a GitHub issue in the most relevant repo.
4. Include where to set or obtain the value.
5. Include why it blocks the work.
6. Include the verification command to rerun afterward.
7. Link the failed run, PR, deployment, or command output when available.

## Issue Must Include

- Missing item
- Owner/action needed
- Where to enter it
- Why it blocks launch/work
- Verification after completion

## Guardrails

- Public issues, PRs, comments, and handovers must never include credential values or local credential-file paths. Use `Credential details: [redacted]`.
- Do not bury human-only blockers in chat only.
- Do not keep retrying automation when credentials or account permissions are missing.
