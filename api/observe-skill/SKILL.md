---
name: observe-skill
description: >
  Logs the outcome of a skill execution to observations/<skill-name>/runs.md. Trigger on:
  "log this run", "skill worked", "skill failed", "this didn't work", "log the outcome",
  "record this", "note that", or after any skill completes with a clear success, partial,
  or failure outcome. Creates the observations file if it does not exist, then appends
  an entry with date, task description, skill used, outcome, what worked, what failed,
  and any error messages observed.
license: MIT
compatibility: Designed for Claude Code. No external tools required.
metadata:
  category: meta
  version: "0.1"
  source: original
  source_types: original
---

# Observe Skill

## Purpose

Track how skills perform in practice. A skill that works in theory may miss steps, use outdated payloads, or fire on the wrong triggers in real-world conditions. This skill captures that gap by recording execution outcomes to a per-skill log file.

## Trigger Conditions

Activate this skill when the user says any of:

- "log this run"
- "skill worked" / "that worked"
- "skill failed" / "that didn't work" / "this didn't work"
- "log the outcome"
- "record this run"
- After any skill completes and the user describes a result (success, partial, fail)

## Methodology

1. **Identify which skill was just used** — ask if unclear. The skill name must match a directory name under `skills/`.
2. **Determine the outcome** — `success` (goal achieved), `partial` (some steps worked, some didn't), or `fail` (skill produced no useful result).
3. **Collect details**:
   - Date (today's date)
   - Task description (what was the user trying to do?)
   - What specifically worked (payloads, steps, tools that produced results)
   - What specifically failed (steps that produced no result, wrong output, or errors)
   - Any error messages or unexpected responses verbatim
4. **Write the entry** — append to `observations/<skill-name>/runs.md`. Create the file and directory if they don't exist.
5. **Confirm** — show the user the appended entry.

## Entry Format

```
---
date: YYYY-MM-DD
skill: <skill-name>
task: <one-line description of what was attempted>
outcome: success | partial | fail
what_worked: |
  <describe what steps, payloads, or approaches produced results>
what_failed: |
  <describe what steps or payloads did not work>
errors: |
  <paste any error messages or unexpected responses>
notes: |
  <any additional context — target type, environment quirks, etc.>
---
```

## Example Interaction

User: "log this run — bola-idor worked, I found a sequential integer ID on /api/orders and was able to read other users' orders using my own session token"

Response: Creates or appends to `observations/bola-idor/runs.md`:

```
---
date: 2026-03-14
skill: bola-idor
task: Test /api/orders endpoint for horizontal IDOR using sequential integer ID
outcome: success
what_worked: |
  Sequential integer IDs confirmed. Substituting victim's order ID (attacker ID +/- 1-10)
  returned full order details including name, address, and payment last4. Tested with
  attacker's Bearer token — no ownership check.
what_failed: |
  UUID endpoint /api/orders/uuid was not vulnerable — UUIDs not guessable.
errors: |
  None.
notes: |
  REST API, no GraphQL. /api/v1/ also vulnerable. /api/v2/ returns 403 on cross-user ID.
---
```

## Fix Patterns

This is a meta-skill — it has no fix patterns. It generates data that other skills (especially `/amend-skill`) consume.
