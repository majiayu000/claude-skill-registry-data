---
name: orbit-pm-rice
description: Generate a RICE-scored backlog from any audit's findings — Reach × Impact × Confidence ÷ Effort. Reads `/orbit-gauntlet`, `/orbit-uat-compare`, `/orbit-pm-ux-audit` outputs, ranks every action item by RICE score, formats as PM-ready prioritised backlog. Use when the user says "RICE", "prioritise backlog", "PM scoring", "what should we fix first".
---

# 🪐 orbit-pm-rice — RICE-scored backlog from audit findings

Audits produce findings. Findings ≠ priorities. RICE scoring turns "47 issues" into "fix these 6 first."

---

## Quick start

```bash
claude "/orbit-pm-rice Read reports/qa-report-*.md and reports/pm-ux/*.json. Output a RICE-scored backlog ranked top to bottom."
```

Output: `reports/rice-backlog-<timestamp>.md` (and Markdown table importable to ClickUp / Linear / Notion).

---

## What RICE means

| Letter | Meaning | Example |
|---|---|---|
| **R**each | How many users hit this per quarter? | 18,000 active sites × 90% homepage views = 16,200 |
| **I**mpact | Per-affected-user, how much does it matter? | MASSIVE / HIGH / MED / LOW = 3 / 2 / 1 / 0.25 |
| **C**onfidence | How sure are we Reach + Impact are right? | 100% / 80% / 50% (anything <50% needs more research) |
| **E**ffort | Person-weeks of work | XS=0.5 / S=1 / M=2 / L=4 / XL=8 |

**RICE score** = (Reach × Impact × Confidence) ÷ Effort. Higher = ship sooner.

---

## How findings map to RICE

For each finding from any Orbit audit:

```
Finding: "Settings page shows white-on-white text on Midnight admin scheme"
Reach:     30% of users (admin-scheme switchers) × site count = ~5,400
Impact:    HIGH (visible bug, looks broken)
Confidence: 100% (reproducible in screenshot)
Effort:    XS (CSS swap)
RICE:      (5400 × 2 × 1) ÷ 0.5 = 21,600 ← high priority
```

vs.

```
Finding: "block.json apiVersion 1 deprecated, migrate to 3"
Reach:     100% (every site running this block) = 18,000
Impact:    LOW (works today, breaks in WP 7.0+ only)
Confidence: 80%
Effort:    L (each block needs render.php migration + retest)
RICE:      (18000 × 0.25 × 0.8) ÷ 4 = 900 ← lower priority
```

---

## Output format

```markdown
# RICE Backlog — my-plugin v2.5 audit · 2026-04-29

| Rank | Item | R | I | C | E | RICE | Note |
|---|---|---|---|---|---|---|---|
| 1 | Fix Midnight admin scheme white-on-white | 5400 | HIGH (2) | 100% | XS (0.5) | 21,600 | Per /orbit-designer-dark-mode finding 3 |
| 2 | Migrate 3 widgets to Container layout | 18000 | MED (1) | 80% | M (2) | 7,200 | Per /orbit-elementor-compat |
| 3 | Add nonce check to admin/save AJAX | 18000 | MASSIVE (3) | 100% | XS (0.5) | 108,000 | Per /orbit-wp-security — CRITICAL, override RICE |
| ...

## Severity overrides
RICE is for *prioritisation*. Critical / High security / data-loss findings always block release regardless of RICE — they're not negotiable.
```

---

## Common pitfalls

### Inflating Reach
"All our users hit this" = lazy. Use telemetry / GSC / GA / sales funnel data for real reach.

### Subjective Impact
LOW vs MED vs HIGH vs MASSIVE — needs anchoring. Use these definitions:
- MASSIVE: would cause refunds / 1-star reviews / churn
- HIGH: visible bug, user notices, may complain
- MED: bug or polish, user notices but doesn't escalate
- LOW: only experts / heavy users notice

### Confidence < 50% = research first
If the team isn't sure of Reach + Impact, don't score — ship more discovery first.

### Effort isn't dev-weeks of one person — include reviews + testing
A "1-day" change with code review + QA + release prep is more like 2-3 days.

---

## Pair with

- `/orbit-pm-release-notes` — turn the top RICE items into the release announcement
- `/orbit-pm-feedback-mining` — use review feedback to inform Impact scores
- `/orbit-pm-roadmap` — long-form roadmap from RICE backlog

---

## Sources & Evergreen References

### Canonical docs
- [Intercom — RICE Scoring](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) — origin (Sean McBride, 2017)
- [ProductPlan — RICE Framework](https://www.productplan.com/glossary/rice-scoring-model/) — practical guide
- [Lenny's Newsletter — Prioritisation](https://www.lennysnewsletter.com/p/the-best-frameworks-for-prioritization) — modern variants

### Last reviewed
- 2026-04-29
