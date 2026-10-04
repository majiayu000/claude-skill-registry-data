---
name: bdb-shipping-skill
description: "Use before starting any significant build or before shipping: problem-framing pre-flight, one-way/two-way door classification, ADR-lite decision logging, and post-ship outcome loop. Complements godmode-shipping (technical gate) and bdbresilience (error recovery)."
category: engineering-method
---

# BDB Shipping Skill — Pre-Flight, Door Classification, ADR-lite, Post-Ship Loop

This skill fills the four decision-quality gaps that neither `godmode-shipping` nor `bdbresilience` covers:

- `godmode-shipping` → technical release gate (tests, checklist, feature flags, rollback, CI). Load it for that.
- `bdbresilience` → error recovery, 429-backoff, distributed locking, fault taxonomy. Load it for that.
- This skill → problem framing, reversibility classification, decision logging, outcome verification. Load it for this.

---

## Routing Table

| Situation | Skill to load |
|---|---|
| Running pre-launch checks, CI gate, WCAG, feature flags | `godmode-shipping` |
| Handling transient errors, rate limits, concurrent locks | `bdbresilience` |
| Starting a significant build — framing the problem | **this skill** |
| Making a one-way or two-way door decision | **this skill** |
| Recording a significant architectural choice | **this skill** |
| Confirming a ship actually delivered value | **this skill** |

Significant build means any work that takes more than one commit, touches a public contract, or requires a decision that is not immediately reversible. For a one-liner fix or a pure chore, skip this skill.

---

## 1. Pre-Build Problem-Framing (Pre-Flight)

Run these five questions before the first file is written. The answers go into the ADR-lite entry (section 3) or, for smaller work, into the commit message or PR description. A question with no answer is a blocker — do not proceed until it is answered.

**Q1 — What problem does this solve?**
State the user-visible or system-visible problem in one sentence. If you cannot write that sentence, the problem is not understood yet.

**Q2 — Why now, not next sprint?**
Name the forcing function: a deadline, a blocking dependency, a cost that compounds if delayed. "It would be nice" is not a forcing function.

**Q3 — What is explicitly out of scope?**
List at least one thing that is tempting but excluded. Scope creep almost always enters through an unguarded boundary. Write the boundary down.

**Q4 — What does success look like, measurably?**
Name a metric, a threshold, or an observable outcome that confirms the work delivered its value. "It works" is not measurable. "Error rate on /api/export drops below 0.1%" or "user can complete onboarding in under 3 steps" is.

**Q5 — Is this reversible?**
Classify the change (see section 2). If it is a one-way door, written justification is required before proceeding.

---

## 2. One-Way / Two-Way Door Classification

Before any irreversible change, name the door type. Gate accordingly.

### Two-Way Doors — can proceed normally
Changes that can be undone with low cost and no external impact:
- UI layout, copy, styling changes
- Internal refactors with no API surface changes
- Configuration behind a feature flag
- Adding a new optional endpoint (additive-only)
- Internal test infrastructure changes

Two-way door work proceeds when pre-flight (section 1) passes. No extra gate.

### One-Way Doors — require written justification and explicit GO
Changes that cannot be undone without significant cost, coordination, or external impact:
- Public API contract changes (breaking or removing a field, endpoint, or behavior)
- Database schema changes (especially dropping columns, changing types, removing tables)
- Published npm package versions (`npm publish` / `npm version`)
- Pricing or billing model changes
- Security model changes (auth scheme, permission structure, encryption at rest)
- Removing or renaming a public CLI command or config key
- Any change that alters an external integration contract other parties depend on

**Gate for one-way doors:**
1. Write one sentence stating: what is changing, why it cannot be reversed, and what the migration/recovery path is for any party depending on it.
2. Paste that sentence into the ADR-lite entry (section 3) under `Reversibility`.
3. Wait for explicit GO before executing. The GO rule from AGENTS.md applies: a plan is read-only until the user replies with the literal word GO.

### When the classification is unclear
Default to one-way. The cost of an unnecessary GO gate is one conversation turn. The cost of treating a one-way door as reversible is potentially irreversible.

---

## 3. ADR-lite Decision Log

Record any significant architectural or product decision — including every one-way door — using this format. Lightweight by design: one file per significant choice, stored in `docs/decisions/` or `production_artifacts/decisions/`. File name: `YYYY-MM-DD-<slug>.md`.

```markdown
# ADR: <title, max 60 characters>

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | superseded-by ADR-YYYY-MM-DD-<slug>

## Context
One sentence: the situation that made this decision necessary.

## Options Considered
- Option A: <what it is and why it was considered>
- Option B: <what it is and why it was considered>
- (add more; delete this line if only one option was viable)

## Decision
<Which option was chosen, in one or two sentences.>

## Reversibility
- Type: one-way | two-way
- Migration path (one-way only): <what a party depending on the old behavior must do>

## Revisit Trigger
<The specific event or metric that would make this decision worth re-examining.
Examples: "If p95 latency on this path exceeds 200ms after the migration",
"If a second consumer needs to read this field", "After Q1 usage data is available.">
```

Store the file. Reference it from the PR description. You do not need a framework, a tool, or a meeting — just the file.

---

## 4. Post-Ship Outcome Loop

Define the check-back before the ship, not after. At the time of shipping, record this alongside the ADR-lite entry or in the PR description:

**Check-back trigger:** When will you look? Choose one:
- Time-based: "Check in N days." (N = 7 for most features; 1 for anything touching the critical path.)
- Metric-based: "Check when [metric] reaches [threshold]."

**Success signal:** What observable outcome confirms the work delivered its stated value (from Q4 above)?

**Rollback signal:** What observable outcome triggers rollback consideration? Be specific: name the metric and threshold. "Something seems wrong" is not a signal. "Error rate on the affected endpoint exceeds 1% over a 15-minute window" is.

**Who checks?** Default: the person who shipped it. If that person is unavailable, name a fallback now.

Post-ship check is not optional for one-way door changes. For two-way door changes it is recommended but can be skipped if the change is trivially observable (e.g., a style change that is visible on first load).

---

## 5. Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll define success after I ship." | Success defined post-hoc matches whatever shipped, not what the user needed. Write it before. |
| "This is just a small refactor, the door classification doesn't apply." | Classification is fastest on small changes. The blast radius of a wrong call on a large change makes the small effort worthwhile. |
| "I'll write the ADR after the decision is stable." | A decision that has already shipped is not a decision — it is a fact. Write it when options are still open. |
| "The rollback trigger is obvious, I don't need to write it down." | Obvious rollback signals are still missed under incident pressure. Write the number before the incident. |
| "The post-ship check-back is someone else's job." | If no one is named, no one owns it. Name someone before shipping. |

---

## 6. Verification Checklist

Before calling this skill's work done:

- [ ] All five pre-flight questions answered (section 1)
- [ ] Door type classified — one-way or two-way (section 2)
- [ ] If one-way: written justification present and GO received before execution
- [ ] ADR-lite entry created for any significant decision or one-way door change, stored in `docs/decisions/` or `production_artifacts/decisions/`
- [ ] Post-ship check-back defined: trigger, success signal, rollback signal, owner (section 4)
- [ ] ADR-lite entry referenced from the PR description or commit message
