---
name: self-check
description: |
  Audit Prismstack's own skills using its own 15D quality rubric.
  Trigger: "check our skills", "self audit", "eat our own dog food", "self-check"
  Do NOT use when: checking a user's domain stack (use the product /skill-check for that)
user_invocable: true
---
<!-- Internal maintenance skill — edit this file directly -->

# /self-check: Audit Prismstack With Its Own Rubric

You are Prismstack's internal quality auditor. Your job is to score Prismstack's own 10 product skills using the same 15D rubric we ship to users. Eating our own dog food.

## Phase 1: Load the Rubric

Read `skills/shared/methodology/quality-standards.md` from the Prismstack project root.

Extract all 15 dimensions and their scoring criteria. These are the exact dimensions you will score against — do not invent your own.

If the file is missing or unreadable, stop and report: "Cannot run self-check — quality-standards.md not found."

## Phase 2: Discover All Product Skills

```bash
ls skills/*/SKILL.md
```

Expect 10 product skills. Read each SKILL.md fully. If fewer than 10 are found, note which are missing.

## Phase 3: Score Each Skill on 15D

For each skill, score every dimension 1-5 using the rubric criteria from Phase 1.

Output a summary table:

```
| Skill           | D1 | D2 | D3 | ... | D15 | Total | Avg  |
|-----------------|----|----|----|----- |-----|-------|------|
| domain-plan     |  4 |  5 |  3 | ... |   4 |   58  | 3.87 |
| domain-build    |  3 |  4 |  4 | ... |   3 |   52  | 3.47 |
| ...             |    |    |    |     |     |       |      |
```

For any score below 3, add a one-line explanation of what is lacking.

## Phase 4: Cross-Skill Pattern Analysis

After scoring all 10, look for systemic patterns:

- **Weak dimensions**: Any dimension averaging below 3.0 across all skills? This is a methodology problem, not a skill problem.
- **Strong dimensions**: Any dimension averaging above 4.5? Document what we are doing right.
- **Outlier skills**: Any skill more than 1.0 below the average total? Flag for priority improvement.
- **Consistency**: Are similar skills (e.g., domain-plan vs domain-build) scored similarly on shared dimensions?

## Phase 5: Compare to Last Run

Check if `.claude/skills/self-check/last-results.json` exists.

If it does, load it and compute deltas:
- Per-skill total change (improved / regressed / unchanged)
- Per-dimension average change
- Highlight any dimension that dropped by more than 0.5

If no previous results exist, note: "First run — no baseline for comparison."

## Output

Present in this order:

1. **Score Table** (Phase 3)
2. **Systemic Issues** (Phase 4) — bullet list with severity
3. **Delta Report** (Phase 5) — improvements and regressions since last run
4. **Top 3 Recommendations** — the highest-impact fixes, with which skill and dimension to target

## Save Results

Write results to `.claude/skills/self-check/last-results.json`:

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SS",
  "version": "<from VERSION file>",
  "skills": {
    "domain-plan": { "scores": { "D1": 4, "D2": 5, ... }, "total": 58, "avg": 3.87 },
    ...
  },
  "dimension_averages": { "D1": 3.8, "D2": 4.1, ... },
  "overall_average": 3.72
}
```

Confirm the file was saved so the next run can compare.
