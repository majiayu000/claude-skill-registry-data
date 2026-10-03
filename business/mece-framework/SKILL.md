---
name: mece-framework
description: Categorize the factors of a problem so they don't overlap (Mutually Exclusive) and nothing is missed (Collectively Exhaustive). Outputs nested Markdown bullets. Use for problem structuring, "make sure I've thought of everything", or step 1 of a strategic analysis.
---

# MECE Framework

## Concept

MECE — **M**utually **E**xclusive, **C**ollectively **E**xhaustive — is the foundation of structured problem solving:

- **Mutually Exclusive:** No factor belongs in two categories.
- **Collectively Exhaustive:** Every relevant factor is captured.

Non-MECE breakdowns look rigorous but aren't — overlapping categories double-count, and missing categories blind you to root causes.

## Required output format

Nested Markdown bullets. Top-level bullets are categories in **bold**; nested bullets are the specific factors under each category.

```markdown
- **Category 1**
  - Sub-factor A
  - Sub-factor B
- **Category 2**
  - Sub-factor C
  - Sub-factor D
```

## Defaults & flex points

| Default | When to flex |
|---|---|
| 3–6 top-level categories | If the problem has only 2 real categories, use 2 — don't pad. If it has 7, use 7. |
| 2–5 sub-factors per category | Use as many as the problem actually contains. |
| Categories specific to the problem | Generic "People/Process/Technology" buckets are a smell — only use them if they genuinely fit. |

**Rule that doesn't flex:** the categories must be MECE. Test each one — could a factor reasonably belong to two? Then merge or split. Could relevant factors not fit anywhere? Then add a category.

## Example — logistics

**Problem:** A regional courier company's on-time delivery rate fell from 94% to 81% in six months.

```markdown
- **Network capacity**
  - Vehicle fleet utilization (peak hour saturation)
  - Driver headcount vs. demand
  - Hub sortation throughput
- **Routing & dispatch**
  - Algorithm changes after the Q2 system migration
  - Address-data quality (geocoding errors)
  - Manual route overrides by dispatchers
- **Demand pattern shift**
  - New high-volume customer added in Q1
  - Seasonal swing into peak retail months
  - Same-day delivery share rising
- **Workforce**
  - Driver turnover and onboarding ramp time
  - Overtime caps from new labor agreement
  - Sick days / absenteeism trend
- **External**
  - Construction zones in two metro areas
  - Two consecutive months of unusual weather
```

Notice: every category is specific to a courier business. No "People/Process/Technology." Every sub-factor is concrete enough to investigate.

## Common mistakes

- **Overlap.** A category like "Operational issues" overlaps with everything else; rename to something specific.
- **Generic buckets.** "External factors" is a placeholder, not a category. Name what's external.
- **List-as-categorization.** A flat list of 12 factors with no grouping isn't MECE — it's just inventory.

## When to use this skill alone vs. as part of the full analysis

- **Standalone:** when the user just wants to make sure they're thinking comprehensively before going off to investigate.
- **As part of full analysis:** invoke `strategy-consultant` — MECE is step 1 of 5.

---

## Acknowledgment & License

Adapted from **Analyst Academy** on YouTube — [5 Consulting Frameworks to Solve Any Problem](https://www.youtube.com/watch?v=uCmTk06aM70). MIT-licensed; see [LICENSE](../../LICENSE).
