---
name: progress-monitor-plan
description: "Create ONE progress-monitoring schedule for an IEP goal or MTSS intervention. Do NOT use to write the goal (use iep-goal)."
---

# progress-monitor-plan

Designs a progress-monitoring schedule with probe type, frequency, decision rules, and data collection method for a single IEP goal or intervention target.

> **Read first — boundaries (`references/security-and-safety.md` §2).** A monitoring plan is a
> **draft for the IEP or MTSS team**, not a decision. It must be validated against the student's
> **actual** IEP/504 plan and local and state policy before anyone collects data against it. This
> atom does **not** set, alter, or approve goals, does **not** make eligibility or placement
> determinations, and does **not** decide whether an intervention continues — those belong to the
> team (`references/assumptions-protocol.md`). **Never request, infer, or include real student
> data — placeholders only.**

## Input

```json
{
  "goal": "By [Date], [Student Name] will read 80 words correct per minute on grade-level passages.",
  "current_level": "45 WCPM",
  "target_level": "80 WCPM",
  "timeline_weeks": 36
}
```

## Output

```json
{
  "tool": "progress-monitor-plan",
  "plan": {
    "probe_type": "Oral Reading Fluency (ORF) — 1-minute timed passage",
    "frequency": "Biweekly",
    "aimline": "~1 WCPM gain per week",
    "decision_rule": "If 3 consecutive data points fall below the aimline, team meets to adjust intervention",
    "data_collection": "Chart WCPM on a line graph; compare to aimline",
    "review_dates": ["Week 9", "Week 18", "Week 27", "Week 36"]
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Generating IEP goals (use iep-goal)
- Administering assessments or recording data
- Making placement decisions

## Pipeline note
Follows `references/method.md` at the Generation step (monitoring plan). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — monitoring plans must be approved by the IEP/MTSS team.
