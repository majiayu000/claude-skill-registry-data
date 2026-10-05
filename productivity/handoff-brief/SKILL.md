---
name: handoff-brief
description: Create a concise, redacted handoff brief for continuing work in a future session or another agent. Adapted from handoff; writes to temp or .scratch by default and preserves evidence and verdict boundaries.
---

# handoff-brief

Source repo: https://github.com/mattpocock/skills
Source path: skills/productivity/handoff/SKILL.md
Source commit: b8be62ffacb0118fa3eaa29a0923c87c8c11985c
Local adaptation note: Adapted from a general handoff document skill into a constrained closeout/handoff artifact with explicit verdicts, evidence confidence, and redaction requirements.

## Purpose

Create a compact continuation document that lets a future session resume without rereading the entire conversation.

Do not duplicate content already captured in PRDs, plans, ADRs, issues, commits, diffs, audit packets, or test logs. Reference those artifacts by path or URL.

## Activation

Use when the user asks for a handoff, compact summary, continuation note, session transfer, or resume-ready brief.

Default write location:
- OS temp directory for ephemeral handoff.
- `.scratch/<task-id>/` only when a repo-local scratch convention exists or the user approves it.

Do not write to repo root by default.

## Required Content

Include:
- Current goal.
- Constraints and forbidden actions.
- Decisions made.
- Changed files, if any.
- Tests/evidence checked.
- Unresolved risks or blockers.
- Recommended next skill.
- Product verdict.
- Implementation verdict.
- Evidence confidence.

## Redaction

Redact secrets and sensitive data:
- API keys, tokens, passwords, cookies, private keys.
- Account IDs, personal data, customer data, or private operational details unless needed and safe to reference.
- Local-only paths may be included when they are necessary for continuation on the same machine.

## Forbidden actions

- Do not include raw secrets or sensitive payloads.
- Do not duplicate large artifacts that already exist elsewhere.
- Do not write to repo root unless explicitly approved.
- Do not edit AGENTS, update CONTEXT.md, create ADR, publish, deploy, git push, or run setup.
- Do not claim completion beyond the available evidence.

## Stop conditions

Stop or ask before writing when:
- The user requested chat-only summary.
- No safe temp or approved scratch location is available.
- The brief would need to include secrets or private data that cannot be safely redacted.
- Existing artifacts already provide a sufficient handoff and only a pointer is needed.

## Output Pattern

```text
Handoff Brief
Location:
Current goal:
Constraints:
Decisions:
Changed files:
Tests/evidence:
Unresolved risks:
Recommended next skill:
Product verdict:
Implementation verdict:
Evidence confidence:
```
