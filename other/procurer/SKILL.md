---
name: procurer
category: commerce
version: 0.1.0
description: |
  Grounded procurement research for any real-world need. Turn a problem
  ("reduce bedroom noise from the avenue", "add air conditioning", "hire an
  accountant", "buy a TV mount", "replace the kitchen sink") into 3–5 ranked
  alternatives spanning DIY-retail → mid-retail → specialty → contractor →
  consultant/turnkey, each with cited price bands (low / typical / high),
  confidence scores, locale-aware currency, and a final recommendation
  with budget. Output is decision-shaped (recommendation + budget envelope),
  not research-shaped (knowledge artifact).
when_to_use: |
  Invoke whenever the user is making a decision that requires calibrated
  cost estimates across alternatives. Common triggers:
    - "How much would it cost to <fix / acquire / replace / improve> X?"
    - "What are my options for <problem>?"
    - "Who could I hire to <task>?"
    - "Is it cheaper to DIY or get someone?"
    - "Give me a budget for <project>."
    - User describes a problem and *implicitly* needs a budget to decide.
  Use proactively when the user describes a problem without asking for cost
  — surface alternatives + bands so they can decide.
not_for:
  - Pure knowledge research with no decision attached → use `deep-research`.
  - Technology / library / API selection → use `technical-research`.
  - Authoring or refining a deployed Life-runtime tenant rules-package
    (e.g. `materiales-intel.v1` for a constructora tenant). That is module
    configuration; see the rules-package skeleton at
    `freelance/_pending-constructora/rules-package/`.
author: broomva
tags:
  - procurement
  - research
  - cost-estimation
  - decision-support
  - grounded
compounding:
  - deep-research
  - technical-research
  - bookkeeping
---

# procurer — Grounded Procurement Research

## What this skill is

The procurer skill turns **a real-world need** into **a grounded cost-calibration report** with cited alternatives, price bands, confidence, and a recommendation. It is the agent's reflex when the user is about to decide how to spend money or effort on a problem and needs calibration before committing.

Concretely, the output of one procurer pass is:

1. A clear restatement of the need (and the underlying problem if the user named only a symptom).
2. **3–5 ranked alternatives**, each placed on a provider-archetype tier (DIY-retail → mid-retail → specialty product → contractor → consultant / turnkey).
3. For each alternative: a **cost band** (low / typical / high) with the currency normalized to the user's locale, plus **cited sources** (provider URL + page title + fetched-at timestamp) and a **confidence score** (0–1).
4. **Cross-cutting notes**: tax/VAT handling, locale-specific suppliers, lead times, hidden costs, deal-breakers.
5. **A recommendation** — which alternative(s) to pursue, in what order, with the budget envelope.

The output is decision-shaped: the user should be able to read it and act, not need to do further synthesis.

---

## When to invoke (the reflex)

The procurer reflex fires on any of these signals:

| Signal | Example |
|---|---|
| Explicit cost question | "How much does X cost?" / "Give me a budget for Y." |
| Options request | "What are my options for fixing the noise?" / "Should I get a mini-split or a window unit?" |
| Hire-someone question | "Who could install this?" / "Should I get a consultant?" |
| Problem with no cost asked | User describes a problem, no budget request — surface alternatives + bands anyway so they can decide. |
| Multiple-vendor comparison | "Compare suppliers for varilla #4." |
| Build-vs-buy / DIY-vs-pro | "Should I do this myself or hire someone?" |

**Anti-trigger**: if the user is researching a topic with no decision attached (e.g., "explain how acoustic windows work"), use `deep-research` instead. The line: *is there a budget envelope at the end?*

---

## The 5-stage procedure

### Stage 1 — Decompose the need into ranked alternatives

Before any search, restate the need in plain terms and **separate the symptom from the failure mode**. A "noisy window" is the symptom; the failure mode is usually *seal leakage* (~90% of the energy on residential sliders) before it's *glass mass deficiency*. Cheap fixes target the dominant failure mode; expensive fixes replace the system.

Use one of the canonical decomposition patterns (see `references/decomposition-patterns.md`):

- **Incremental → augmentation → replacement** (most physical / fix-it problems).
- **DIY → service → managed** (when responsibility transfer is a real lever).
- **Standard → custom → bespoke** (when specificity drives cost).
- **Single-vendor → multi-vendor → integrator** (sourcing complexity).

Produce a list of **3–5 alternatives** ordered by cost and disruption. State the *thesis* of each — what problem it actually solves, not just what it is.

### Stage 2 — Map provider archetypes per alternative

For each alternative, identify which **provider archetypes** apply (see `references/provider-taxonomy.md`):

| Tier | Archetype | Examples |
|---|---|---|
| T1 | DIY-retail | Big-box / hardware store / marketplace / online retail. Consumables and parts the user installs. |
| T2 | Mid-retail / specialty product | Specialty store with installation optional. |
| T3 | Specialty product / fabricator | Manufacturer / branded supplier / custom-fab shop. |
| T4 | Contractor / installer | Service that does the work end-to-end with materials it sources. |
| T5 | Consultant / engineer / turnkey | Advisory or full-service end-to-end management. |

Not every alternative spans every tier. Capture which tiers are relevant per alternative.

### Stage 3 — Choose the search mode

Based on the user's urgency, budget headroom, and decision stakes, choose **fast / standard / deep**. See `references/mode-tiers.md` for full contracts.

| Mode | Searches | Providers cited per alt | Latency target | When |
|---|---|---|---|---|
| **fast** | 1 per alt | 1–2 (T1 only) | < 1 min total | "Just give me a rough number." |
| **standard** | ≥3 per alt | 3–5 (cover ≥2 tiers) | ~3–5 min | Default for most decisions. |
| **deep** | ≥6 per alt | 5–7 (cover ≥3 tiers) | best-effort | "I'm actually deciding now, need the full picture." |

Default to **standard** unless the user explicitly signals "quick" or "thorough."

### Stage 4 — Search with grounding discipline

For each `(alternative, provider archetype)` pair, run grounded web searches. The discipline (see `references/grounding-discipline.md`) is non-negotiable:

1. **Citation required.** Every price must carry `source_url`, `source_title`, `fetched_at` (ISO-8601 UTC). No bare numbers.
2. **No fabrication.** If no public price exists for that pair, say so explicitly and leave it empty. Never fill from training data.
3. **Confidence (0–1).**
   - `≥ 0.90` — exact product page, SKU + unit explicit.
   - `0.70 – 0.89` — listing exists but unit/spec requires interpretation, or quote-on-request signals.
   - `< 0.70` — category/inferred from comparable item; flag explicitly.
4. **Unit & currency normalization.** Quote in the user's locale currency with the right thousand/decimal conventions. Be explicit about tax (IVA/VAT inclusive vs. add).
5. **Sanity bands.** If a price falls > 2× the median for that category, flag it in notes — don't drop it (the human decides).
6. **Diversity bias.** For `standard` and `deep`, prefer at least two tiers — a Tier-1 retail anchor plus a Tier-3+ specialty or contractor benchmark.
7. **Locale-aware suppliers.** Use locale-appropriate domains/brands. Default to user's stated region; ask if unclear.

When the agent has a `WebSearch` / `WebFetch` tool, use it. When it doesn't, mark the report as **unsourced calibration** — provide ranges from prior knowledge but explicitly note the absence of fresh citations and recommend the user run a sourced pass before committing.

### Stage 5 — Render the report

Produce the report using `references/report-template.md`. The skeleton:

```
# <Need restated in one line>

## Problem framing
<2-4 sentences: what's the actual failure mode, not just the symptom>

## Alternatives

### Alternative A — <name>  (Tier T1 → T3)
**Thesis**: <what this actually solves>
**Cost band (locale)**: low – typical – high
**Confidence**: 0.X
**Providers cited**: <N> — see footnotes [1] [2] [3]
**Notes**: <lead time, hidden costs, deal-breakers, tax handling>

### Alternative B — ...
### Alternative C — ...

## Cross-cutting notes
- Tax / VAT / IVA treatment
- Locale-specific supplier shortlist
- Common hidden costs
- Lead times

## Recommendation
**Start with**: <Alternative X>
**Total budget envelope**: <low – high>
**Rationale**: <2-3 sentences>
**If that doesn't work**: <Alternative Y as fallback>

## Sources
[1] <url> — <title> — fetched <iso8601>
[2] ...
```

Then optionally call `scripts/validate_report.py <report.md>` to lint structural completeness (≥3 alternatives, every alternative has cost band + confidence + ≥1 citation, recommendation present, currency consistent).

---

## Grounding rules (binding)

These rules bind every procurer run regardless of mode:

1. **No price without a citation.** A number alone is not procurement research — it's a hallucination risk.
2. **No alternative without a thesis.** Don't list options; list options *with the problem each solves*.
3. **No recommendation without a budget envelope.** "Go with X" is incomplete; "Go with X, $A–$B inclusive of installation" is decision-shaped.
4. **No locale assumption.** If the user hasn't stated their region, ask before searching — supplier networks and tax handling diverge sharply.
5. **Flag the dominant failure mode early.** If 80% of the user's problem can be solved by a 5% intervention (Tier-1 fix), say so before they spend Tier-4 money. Honesty about *what actually causes the problem* is the most valuable output.

---

## Resources

### references/
- `decomposition-patterns.md` — four canonical patterns for breaking a need into alternatives.
- `provider-taxonomy.md` — the 5-tier provider archetype model, with examples across domains.
- `grounding-discipline.md` — citation / confidence / locale / tax rules in full.
- `mode-tiers.md` — fast / standard / deep search contracts with budgets and SLA targets.
- `report-template.md` — the report skeleton and a fully-filled exemplar.

### scripts/
- `validate_report.py` — structural linter for a generated procurement report. Checks alternatives count, citation completeness, confidence range, recommendation presence, currency normalization. Exit non-zero on failure.

### assets/examples/
- `window-noise-attenuation.md` — full worked example: bedroom window noise on a Bogotá avenue, three tiers of remediation.
- `construction-materials-co.md` — generalized Colombian construction materials reference (CO suppliers, families, IVA handling) — lifted from the materiales-intel.v1 rules-package pattern.

---

## Compounding with other skills

- **`deep-research`** — when the user wants to learn about a topic before deciding, run deep-research first, then procurer for the cost layer.
- **`technical-research`** — for software/library choice with a cost dimension, do technical-research for the technical evaluation, then procurer for SaaS pricing / consultancy / implementation costs.
- **`bookkeeping` (P8)** — procurement reports that produce reusable knowledge (e.g., "the CO porcelanato market spans $35k–$120k/m²") should be filed into the entity graph via `bookkeeping file`.

---

## Closing handoff

The skill ends when the report renders. The agent's last message to the user is the report itself plus a one-line action prompt: *"Want me to deep-dive any alternative, refresh citations, or proceed with a specific provider?"*

Procurer never spends the money. It calibrates the spend.
