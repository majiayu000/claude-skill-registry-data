---
name: friction-driven-skill-improvement
version: 1.1.0
description: Captures friction signals during writing sessions (corrections, re-explanations, skill mismatches, manual workarounds, automation opportunities) as one-line log entries, and drafts skill improvement proposals at session end. Use when friction is detected during a session, at session end, or when the user asks for improvement proposals.
---

# Friction-Driven Skill Improvement

## Purpose
Capture friction arising in paper-writing sessions (user corrections, re-explanations, manual workarounds) without interrupting the dialogue, and draft skill improvement proposals at session end. Provides traceability from observed friction to skill changes, serving as input to DSR process-evidence records ([`design-science-research`](../design-science-research/SKILL.md) Step 3).

## When to Use
- When a friction signal is detected mid-session (Step 1 capture only; no analysis or proposals)
- At session end (Steps 2-3 alongside [`session-research-handoff`](../session-research-handoff/SKILL.md))
- When the user explicitly asks for improvement proposals

## Friction Signal Taxonomy

| Code | Signal | Definition | SE counterpart |
| :--- | :--- | :--- | :--- |
| CORRECTION | Correction | User corrected the agent's output or understanding | Defect report |
| REEXPLAIN | Re-explanation | The same instruction had to be repeated or rephrased | Unmet requirement |
| MISMATCH | Skill mismatch | A skill was invoked but did not produce the expected output | Test failure |
| WORKAROUND | Manual workaround | User resorted to a manual workaround | Workaround |
| AUTOMATION | Automation opportunity | A recurring routine task has no corresponding skill | Automation opportunity |

## Procedure

### Step 1: Real-Time Capture (during session)
On detecting a friction signal, append one line to the friction log immediately. **Do not interrupt the dialogue. Do not ask for confirmation or approval.**

- Placement follows the repository's artifact index rule: `docs/<paper-id>/design/logs/friction-log.md` for classified layouts, `docs/<paper-id>/design/friction-log.md` for flat layouts (`docs/design/` in single-paper repositories)
- If the log does not exist, create it from this template:

```markdown
# Friction Log

> **Class**: log (append-only)
> **Created**: YYYY-MM-DD
> **Operation**: Append one line per detected friction signal, per the friction-driven-skill-improvement skill

| Timestamp | Code | Target skill/phase | Situation | Severity |
| :--- | :--- | :--- | :--- | :--- |
```

- Append exactly one line:

```markdown
| YYYY-MM-DD HH:MM | Code | Target skill/phase | Situation (one line) | Severity (high/med/low) |
```

### Step 2: Batch Analysis at Session End
0. **Retroactive reconstruction (v1.1.0)**: if the friction log does not exist or has zero entries for the session, reconstruct friction signals by reviewing the conversation history and append them (mark timestamps as approximate and note the reconstruction in the log header). Uncaptured friction is lost when the session ends — do not skip this step.
1. Read the session's friction log entries and extract recurring patterns per skill or phase
2. Distinguish one-off events from recurring ones
3. Include high-severity one-off events as proposal candidates

### Step 3: Drafting Improvement Proposals
**Only recurring patterns or high-severity one-offs become proposals** (do not proposalize every friction event; avoid noise).

- Create as a proposal-class artifact at `design/proposals/<skill-name>-improvement-proposal.md` (same placement rule as Step 1)
- Proposals remain in proposal class; **skill modifications are applied only after explicit user approval**
- Template:

```markdown
# Improvement Proposal: <skill-name>

> **Class**: proposal (pending decision)
> **Created**: YYYY-MM-DD
> **Source log**: relevant friction-log.md entries (referenced by timestamp)

## Background (observed friction)
(Quote the relevant log entries with recurrence count and severity)

## Problem
(State the skill definition defect in 1-2 sentences)

## Proposed change
(Which sections of SKILL.md to change, and how. Be specific)

## Expected effect
(Which friction signals this resolves. Do not claim causal proof of effect)

## Impact
(Spillover to other skills or paper projects)
```

### Step 4: Post-Approval Implementation
Only after the user approves a proposal:

1. Modify the skill and bump the frontmatter `version` per semver
2. Record the change, source log entries, and approval date in the proposal file
3. Update the version mapping table (artifact version ↔ manuscript section ↔ commit) per [`design-science-research`](../design-science-research/SKILL.md) Step 4

## Invariants
- Capture never interrupts the dialogue (one-line append only; no confirmation or approval requests)
- Proposals remain in proposal class. Skill modifications require user approval
- The friction log records facts; it does not evaluate or criticize user statements
- Not every friction event becomes a proposal (recurring or high-severity only)

## Outputs
- `docs/<paper-id>/design/logs/friction-log.md` (friction log, append-only)
- `docs/<paper-id>/design/proposals/<skill-name>-improvement-proposal.md` (improvement proposal)
