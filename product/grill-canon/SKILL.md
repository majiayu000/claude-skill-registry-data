---
name: grill-canon
description: Grill CURRENT and accepted ADRs for staleness, contradiction, and missing decisions. Use when asked to audit the brain, grill the canon, or check whether docs are still truth.
---

# Grill the canon

Subject is the **brain**, not a new feature pitch.

## Read

`START_HERE` → `CURRENT` → `ROADMAP` → `EXPERIMENTS` → accepted ADRs. Open evidence/notes only where CURRENT cites them.

## Frontier (typical first round)

Ask only what is unsettled *in the docs*. Recommended checks:

1. Does CURRENT still match every `status: accepted` ADR?
2. Are experiments or evidence treated as if they were truth?
3. Behavior or positioning with no ADR?
4. Stale `updated:` / superseded ADR still implied by CURRENT?
5. Invented metrics, users, or competitors (forbidden)?
6. Scope creep into non-goals (chat hell, AI review, multiplayer KG, agent HITL)?

Use grilling format: numbered frontier questions, recommended answer, then wait if a **decision** is required. Pure **facts** you can verify in-repo: report as findings, do not quiz the user.

## Output

- Findings (canon vs evidence vs silence)
- Proposed patches (CURRENT and/or ADRs) — apply only after the user confirms
- Do not "fix" product direction by editing truth during the audit unless asked
