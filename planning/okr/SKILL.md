---
name: okr
description: Set, track, and score OKRs with progress tracking
version: 0.1.0
execution-mode: advisory
argument-hint: "[--action set|update|score|review] [--quarter Q1|Q2|Q3|Q4]"
category: data-science
status: candidate
---
# OKR Tracker

Set, track, and score Objectives and Key Results (OKRs) with structured progress tracking. All OKR data is stored in `_state/okrs.jsonl` as append-only entries. Supports quarterly cycles with mid-quarter check-ins and end-of-quarter scoring.

## When to Use
- At the start of a quarter to define new OKRs
- During weekly or bi-weekly check-ins to update key result progress
- At end of quarter to score and reflect on OKR achievement
- When aligning daily work to strategic objectives

## Execution
1. Parse `$ARGUMENTS` for action (set, update, score, review) and quarter
2. For `set`: prompt for objectives (3-5) and key results (2-4 per objective), write to `_state/okrs.jsonl`
3. For `update`: read current OKRs, update progress percentages on specified key results
4. For `score`: calculate achievement scores (0.0-1.0) per key result and roll up to objective level
5. For `review`: display all OKRs with current progress, highlight at-risk items (below 30% at mid-quarter, below 60% at 3/4 mark)
6. Flag any objectives with no progress updates in the last 14 days

## Output Format
```
OKR Tracker | <action> | <quarter> <year>
==========================================

## Objectives

### O1: <objective title> — Score: <0.0-1.0>
| Key Result | Target | Current | Progress | Status |
|------------|--------|---------|----------|--------|
| KR1: ... | ... | ... | 70% | ON_TRACK |
| KR2: ... | ... | ... | 25% | AT_RISK |

### O2: <objective title> — Score: <0.0-1.0>
| Key Result | Target | Current | Progress | Status |
|------------|--------|---------|----------|--------|
| ... | ... | ... | ... | ... |

## Summary
- Overall score: <weighted average>
- On track: N / Total
- At risk: N / Total
- Last updated: <date>

## Next Action
- ...
```

## Skill Chains
| After this skill... | Consider... |
|--------------------|-------------|
| Quarter review complete | `[weekly-review]` to align weekly plans with OKR gaps |
| OKRs inform sprint planning | `[sprint-status]` to check sprint alignment |
| OKR results for stakeholders | `[investor-update]` to include OKR progress |
