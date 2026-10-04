---
name: interviewing
description: Use when the user gets an interview invitation, moves into an interview process, wants to track interview stages, capture post-interview notes, draft follow-up messages, or update an application to interviewing.
---

## Overview

Manage the interview stage of an application. This skill owns tracker advancement to `interviewing`, interview logs, follow-up notes, and handoff to `interview-coach` for deep preparation.

Use `interview-coach` when the user only wants a prep brief. Use `interviewing` when there is process state to track.

## Workflow

> **State layer:** reads and updates `applications.md`, writes per-application interview notes, and may invoke `interview-coach`. See [state-layer contract](../_shared/state-layer.md).

### 1. Identify the application

Run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"` if state files are missing.

Gather:

- Company.
- Role.
- Application id if known.
- Interview stage: recruiter screen, hiring manager, technical, panel, presentation, final, or other.
- Date/time, format, interviewer names/functions, and recruiter notes if available.
- Job posting or application folder if available.

If no tracker row exists, offer to create one directly at `status: interviewing`. This is allowed by [state-layer section 4](../_shared/state-layer.md#4-status-enum). When inserting, populate `comp_expected`, `source`, and `next_action_date` (default: the next interview date if known, otherwise today + 7 days) from conversation. See [state-layer §3](../_shared/state-layer.md#3-applicationsmd-schema) for the back-compat read/write rules.

If a row exists at `saved` or `applied`, ask whether to advance it to `interviewing`. Never regress a later status. When advancing, also update `next_action_date` to the next concrete commitment (interview date, take-home due date, or follow-up window).

### 2. Create or update the interview log

Write or append `my-documents/applications/{id}/interview-log.md`.

Suggested structure:

```markdown
# Interview Log - {Company}, {Role}

## Current Status

- Stage:
- Next interview:
- Format:
- Contacts:
- Open questions:

## Timeline

### YYYY-MM-DD - {Stage}

**Before:** What is known going in.

**After:** Notes, signals, concerns, and follow-up actions.

**Follow-up:** Sent / not sent / not needed.
```

Keep the log practical and private. It can contain candid notes that should not appear in the candidate-facing prep brief.

### 3. Prepare if needed

If the user needs preparation, invoke `interview-coach` with:

- Company and role.
- Application id.
- Stage and interviewer context.
- Job posting or known requirements.
- Any prior company research report.

Save or update `my-documents/applications/{id}/interview-prep.md` through `interview-coach`.

### 4. Capture post-interview notes

After an interview, ask for:

- What they were asked.
- Where they felt strong or weak.
- New information about the role, team, scope, work model, compensation, or process.
- Red flags or green flags.
- Follow-up commitments.

Append this to `interview-log.md`. If new facts affect company fit, suggest a fresh `company-research` pass or add interview questions for the next stage.

### 5. Draft follow-up

If the user wants a follow-up message, draft a short note grounded in the actual conversation.

Save to:

```text
my-documents/applications/{id}/follow-up.md
```

Rules:

- Thank them for specific discussion points.
- Reconnect one proof point to the role.
- Mention promised materials only if actually promised.
- Keep it concise. No generic "I remain very excited" filler unless it sounds like the user.

### 6. Close the run

Show:

- Tracker row status.
- Files created or updated.
- Next interview action.
- Any open questions to ask the company.

If the user reports an offer, rejection, withdrawal, or acceptance, offer to advance the tracker to `offer`, `closed`, or `hired` according to the state-layer rules.

Then the reward beats from [state-layer §11](../_shared/state-layer.md#11-progress-and-reward):

- **What this unlocked** — e.g. "Your interview notes are captured, so follow-up drafting and future prep for this company build on them."
- **Momentum pulse** — since this run touched the tracker, print the momentum line (`node "{job_hunt_skills_root}/scripts/profile-strength.mjs" --pulse`, or derive it natively). An interviewing count on the board is real progress in a demoralizing process — surface it. If the user advanced a status, reprint the pulse so the move is visible.

## Common Mistakes

- **Skipping tracker confirmation.** Do not advance statuses without user confirmation.
- **Mixing private notes into prep brief.** Keep candid process notes in `interview-log.md`.
- **Generic follow-up.** Use the actual conversation.
- **Forgetting next actions.** Every interview-stage update should leave the user with the next concrete step.

## Reference

[`guides/sustainable-search.md`](../../guides/sustainable-search.md) — follow-up cadence (same-day thank-you, one-week check-in, two-week intervals on long processes), how to handle silence, and the "burn zero bridges" rejection response. Use it to anchor `next_action_date` on the tracker.
