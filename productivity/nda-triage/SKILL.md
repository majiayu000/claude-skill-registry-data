---
model_tier: inherit
name: nda-triage
description: "Use when triaging an inbound NDA fast — GREEN/YELLOW/RED so only the hard ones reach a lawyer. Triggers on 'check this NDA', 'can we sign this NDA', 'is this NDA standard'."
status: active
tier: senior
council_depth: deep
domain: process
recommended_for_user_types: [legal]
workspaces:
  - legal-review-prep
packs:
  - legal-review-prep
trust:
  level: advisory
install:
  removable: true
---

# nda-triage

## When to use

- An inbound NDA lands and the question is *which bucket* — standard, needs-counsel, or full-review — so only the hard ones reach a lawyer's desk.
- A counterparty sends "our standard NDA" and someone needs a fast read before scheduling counsel time.
- A volume of NDAs needs first-pass sorting; triage is the throttle that protects attorney bandwidth.

Do NOT redline here (route to [`contract-review`](../contract-review/SKILL.md)), and do NOT treat a triage signal as clearance — see `legal-safety-floor`. If the document is really a data-processing agreement, route to [`dpa-review`](../dpa-review/SKILL.md).

## Procedure

### Step 0: Establish jurisdiction + thresholds (no defaults)

1. Read the governing-law clause. If it is **not EU or DE**, STOP — hard refusal: *"This pack covers EU/DE law only. Consult licensed local counsel for this jurisdiction."* Never guess for out-of-scope law.
2. Read the triage thresholds from `legal-practice-profile` (mutual-vs-one-way stance, max term length, required carve-outs, governing-law allow-list, indemnity/penalty caps). This skill ships **NO** default NDA positions — they vary too much. Until the profile is configured, use `[configure]` placeholders in the verdict and flag every unset threshold.
3. Tag the output with `Jurisdiction: EU` or `Jurisdiction: DE`.

### Step 1: Triage to GREEN / YELLOW / RED

Score the NDA against the profile thresholds, not against memory:

- **GREEN — standard-approve** — mutual/one-way matches stance, term within `[configure]` max, all required carve-outs present, governing law on the allow-list, no penalty/liquidated-damages clause. *Standard shape only.*
- **YELLOW — counsel review** — one or two threshold deviations (longer term, missing a carve-out, one-way where mutual expected, broad definition of confidential info). A lawyer reads it; not a full review.
- **RED — full review** — penalty/indemnity clauses, IP-assignment riding inside the NDA, perpetual/unbounded term, governing law on the edge of scope, non-standard structure. Full attorney review before any signing conversation.

A non-lawyer cannot define what RED is — the profile + this rubric do.

### Step 2: GREEN × non-lawyer → attorney gate (load-bearing)

If the verdict is **GREEN** and the practice-profile role is **non-lawyer**, the skill **never self-approves signing**. It MUST:

1. STOP — do not advance to "you may sign".
2. Emit `attorney-brief.md` — a one-page brief (counterparty, term, mutual/one-way, carve-outs present/absent, why it scored GREEN, the thresholds checked).
3. Refuse to proceed without an **explicit yes from a licensed attorney**. A non-lawyer GREEN is a triage signal, never a clearance.

For a **lawyer** role, GREEN still emits the verdict but the attorney *is* the gate.

### Step 3: Emit the triage verdict

Produce `triage-verdict.md` carrying the `Jurisdiction:` tag, the bucket, the deviations found, the route, and the mandatory work-product line. Route per bucket: YELLOW/RED → [`contract-review`](../contract-review/SKILL.md) for redlines. Never issue a final legal call (`legal-safety-floor`).

## Related Skills

**WHEN to use this**

- The task is a fast first-pass *sort* of an inbound NDA into approve / counsel / full-review.
- The goal is to protect attorney bandwidth by filtering the easy ones.

**WHEN NOT to use this**

- Redlining or clause-by-clause negotiation — route to [`contract-review`](../contract-review/SKILL.md).
- The document is a data-processing agreement (Art. 28 / controller-processor) — route to [`dpa-review`](../dpa-review/SKILL.md).
- General contract risk reading (MSA / SOW) — route to [`contracts-cognition`](../contracts-cognition/SKILL.md).

## When the agent should load this

- "Kannst Du diese NDA kurz prüfen?"
- "Ist diese Geheimhaltungsvereinbarung Standard oder müssen wir die anwaltlich prüfen lassen?"

## Output

1. **`triage-verdict.md`** — `Jurisdiction:` tag, GREEN/YELLOW/RED bucket, threshold deviations found, route (contract-review / dpa-review), and the mandatory work-product line.
2. **`attorney-brief.md`** *(GREEN × non-lawyer, mandatory)* — one-page brief: counterparty, term, mutual/one-way, carve-outs, why GREEN, thresholds checked; ends pending an explicit attorney yes.

Every output carries:

```
> ⚠️ Attorney review required on material use. This is a draft for a licensed attorney, not legal advice and not a legal conclusion.
```

## Gotcha

- A GREEN for a non-lawyer is **not** permission to sign — it routes into the attorney gate (Step 2). Self-approving signing is the canonical failure this skill exists to prevent.
- Shipping a default term length / carve-out set is wrong: NDA norms vary by counterparty, sector, and house style. Read `legal-practice-profile`; use `[configure]` until set.
- Out-of-scope governing law is a hard refusal, not a best-effort guess — a stale read for a jurisdiction the pack doesn't cover is worse than none.
- A penalty / liquidated-damages clause or IP-assignment hidden inside an NDA is RED regardless of how "standard" the rest looks.
- A missing `Jurisdiction:` tag or work-product line fails the legal disclaimer/jurisdiction linters — never drop either.

## Do NOT

- Do NOT self-approve a GREEN NDA for a non-lawyer; emit the attorney brief and wait for an explicit yes.
- Do NOT apply a default NDA position; read thresholds from `legal-practice-profile` or mark `[configure]`.
- Do NOT triage an out-of-scope (non-EU/DE) NDA; refuse and route to local counsel.
- Do NOT redline — route depth to [`contract-review`](../contract-review/SKILL.md).
- Do NOT issue a final legal conclusion (`legal-safety-floor`).

## Runnable example

Inbound mutual NDA, non-lawyer (ops) role, profile configured.

- Step 0 — governing law = `DE` (in scope). Thresholds loaded: mutual expected, max term 3y, carve-outs {independently-developed, publicly-known} required, no penalty clause. Tag `Jurisdiction: DE`.
- Step 1 — mutual ✓, term 2y ✓, both carve-outs present ✓, no penalty clause ✓ → **GREEN**.
- Step 2 — role is non-lawyer → attorney gate fires. Emit `attorney-brief.md` (counterparty, 2y mutual, carve-outs present, scored GREEN against the 3y/mutual/no-penalty thresholds). Refuse to advance to "you may sign" without an explicit attorney yes.
- Step 3 — `triage-verdict.md`: `Jurisdiction: DE`, bucket GREEN, no deviations, route = attorney gate (not contract-review), plus the work-product line.
