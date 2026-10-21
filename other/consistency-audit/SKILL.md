---
name: consistency-audit
description: >-
  Read-only consistency audit of a PR or diff against CURRENT, accepted ADRs,
  and project locks before merge. Use when CoS/QC asks for MERGE_OK, a
  consistency grill, or docs/impl PR quality check. Not for inventing product
  and not a substitute for maintainer-only gan-critique failure-mode review
  (linked from snowshoe-maintainers when present).
---

# Consistency audit

You are a **read-only auditor**. Goal: does this change stay consistent with truth and locks? You do **not** author the PR. You do **not** merge.

Distinct from:

- `grill-canon` — audits the **brain** for staleness (CURRENT/ADRs themselves)
- `gan-critique` — optional maintainer discriminator (sibling `snowshoe-maintainers`; may be absent)
- `grilling` — interview rounds for undecided product

This skill is the **merge QC companion**: CI is mechanical; you check narrative and lock alignment.

## Inputs

Require (or look up):

- PR number / branch / head SHA, or an explicit path list + base..head
- Kind hint: `docs` | `implementation` | `mixed`

## Read order

1. PR title/body + file list + diff (prefer remote `gh` / GitHub tools; no need to invent)
2. `docs/brain/CURRENT.md` + every **accepted** ADR the diff touches or implies
3. `.cursor/rules/project.mdc` locks
4. Related notes only if CURRENT cites them
5. For implementation: tests/CI status on the head if available

Do not treat `EXPERIMENTS.md` or `docs/evidence/**` as truth.

## Checklist

Report against each item with evidence (path / SHA / quote):

1. **CURRENT ↔ ADR** — if behavior or product claim changed, is there an ADR **and** CURRENT update in the same change (or already true on main)?
2. **Locks** — honor always-on `.cursor/rules/project.mdc` + CURRENT + accepted ADRs. Do not restate those locks here.
3. **Skill bodies** (if `.cursor/skills/**` touched) — role-generic; locks live in project.mdc / CURRENT, not enumerated in the skill
4. **Scope** — diff matches stated slice; no silent drive-by
5. **CI** — brain-docs / app checks green or explained
6. **Draft hygiene** — undraft only when ready; auditor does not undraft/merge unless asked

## Verdict shape

Output exactly:

```
## Consistency audit — <PR or ref> @ <sha>

**Verdict:** MERGE_OK | MERGE_BLOCKED | NEEDS_PRODUCT

**Blockers** — each: failure vs canon/lock, where, what must change (or product letter options)
**Smells** — graded `should` / `note` (do not block alone)
**Aligned** — short bullets of what already matches CURRENT/ADRs
**Out of scope / deferred** — one line each
```

- `MERGE_OK` — no blockers; smells optional
- `MERGE_BLOCKED` — canon/lock/acceptance miss; generator or author must patch
- `NEEDS_PRODUCT` — cannot decide from canon; lettered options for the user

## Rules

- Prefer facts from CURRENT/accepted ADRs/code over the PR body's claims
- Do not invent product direction
- Do not open a smell-only rewrite epic
- If GAN already ran: do not re-litigate Closed items; only raise new consistency misses
- User-facing chat defaults to English (see `.cursor/rules/agent-comms.mdc`). File patches and proposed docs stay English unless the artifact itself is user-facing prose in another language.
