---
name: t4-engineering-records
description: Use when working in a T4-team repo (T4 Labs / Slow-Inc) and something notable just happened that a future agent will need the "why" of — you fixed and validated a bug, made a hard-to-reverse architectural decision, shipped a system-affecting change, or hit a bug whose lesson is worth keeping. Helps pick the right record (post-mortem vs ADR vs system-impact entry vs bug-case-catalog) and write it so it stays a reliable index (file:line, commit SHAs, validated-only). Triggers include "write a post-mortem", "record this decision", "log this change", "should this be an ADR".
---

# T4 Engineering Records

## Overview

In an agent-primary repo, the record you write *is* the memory the next agent inherits — it can't ask you later. A record has value only if it is **findable, grounded, and true**: code identifiers (`file:line`, function names, commit SHAs) are the index that lets the next agent grep back to the actual change, and an unverified record is worse than none because it looks authoritative while being wrong.

This skill answers two questions: **which record** to write, and **how** to write it so it stays reliable.

## Which record — decide first

| What just happened | Record | Home |
|---|---|---|
| A bug is **fixed and validated** (reliable repro + known root cause + validated fix) | **post-mortem** | `docs/reports/YYYY-MM-DD-<slug>.md` + a pointer in the impact register |
| A significant, **hard-to-reverse decision** — or a **quality / performance decision** whose rationale or benchmark would otherwise be lost — was made (already in the code, or explicitly planned) | **ADR** | `docs/adr/NNNN-<kebab>.md` + a row in `docs/adr/README.md` |
| Any **system-affecting change** shipped (feature, refactor, security, hotfix) and needs a report-level log | **system-impact register entry** | append to `docs/reports/system-impact-report.md` |
| A notable bug whose **transferable lesson** is worth keeping (for retros / onboarding / decks) | **bug-case-catalog entry** | append to `docs/reports/bug-case-catalog.md` |

Guards:
- **Don't post-mortem a hypothesis.** If the repro isn't reliable, the root cause isn't known, or the fix isn't validated — you don't have a post-mortem yet. List what's missing and stop.
- **A feature/refactor is not a post-mortem** — it's a system-impact entry (+ an ADR if it encodes a decision).
- **A trivial one-liner needs neither** — the PR description is enough.
- **One decision = one ADR.** Overturning a prior decision doesn't edit it — write a new ADR and mark the old one **Superseded by NNNN**. ADR numbers are globally unique across branches.

## How — the rules that keep records reliable

- **Keep code identifiers.** `file:line`, function/symbol names, the offending commit SHA. They are the index; prose without them can't be grepped back.
- **Validated-only, honest coverage.** State how you know it works (the failing test that now passes, the E2E that now succeeds, before→after numbers). If only one config was tested, say so. Never fabricate a number — write "not measured" / "N/A".
- **Blameless, active voice, no hedging.** Describe the gap, never the person. Drop "we believe" / "appears to" — prove it or cut it.
- **Ground ADR claims in the code as it is now**, and cite where. An ADR that describes an intention the code doesn't reflect is a landmine.
- **Leave a pointer, don't duplicate.** A post-mortem gets a one-line pointer in the impact register; an ADR gets a row in the ADR README. The full text lives in one place (single source — see `t4-agent-memory`).

## Templates

See `references/record-templates.md` for drop-in skeletons: post-mortem, system-impact register entry, bug-case-catalog entry, a single ADR, and the ADR README index.

## Cross-skill

- Records are memory — the single-source, freshness, and archive rules live in **t4-agent-memory**.
- When a T4 repo requires bilingual tracker posts, a post-mortem/PRD posted to a GitHub issue follows the bilingual rule in **t4-dev-workflow** (EN + a full Thai mirror).

## Common mistakes

- **Writing a post-mortem before the fix is validated.** That's a hypothesis; refuse until the repro passes.
- **Prose with no `file:line` / commit SHA.** Unindexable — the next agent can't get from your words to the code.
- **Editing an old ADR to reverse it** instead of superseding — erases the decision history.
- **Fabricated or implied-broader coverage.** "Tests pass" when you ran one config reads as full coverage; state the scope.
- **Duplicating the full record in two files** instead of full-text-in-one + pointer-in-the-other.
