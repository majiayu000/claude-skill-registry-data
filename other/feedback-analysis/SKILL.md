---
name: feedback-analysis
description: >
  Patterns for analyzing multi-agent feedback data: quality scoring, defect
  pattern detection, root-cause tracing, baseline comparison, and prompt
  evolution. Used by metrics-collector, root-cause-tracer, learning-engine,
  and improvement-planner agents.
  Keywords: feedback, quality score, baseline, regression, pattern, root cause,
  backpatch, telemetry, improvement, self-learning, evolution.
---

# Feedback Analysis Patterns

Standardizes how the feedback loop agents analyze agent output quality,
detect recurring patterns, trace defects to root causes, and propose
improvements for future runs.

## When to Activate
- When computing quality scores for agent outputs
- When analyzing defect logs for recurring patterns
- When tracing defects backward through phases
- When comparing metrics against baselines
- Used by: metrics-collector, root-cause-tracer, improvement-planner, learning-engine

## Quality Score Computation

Score = Completeness(25%) + ReviewSeverity(30%) + GuardrailPass(20%) + Rework(15%) + Downstream(10%)

```python
def compute_quality_score(agent_data):
    completeness = produced_files / expected_files  # 0.0-1.0
    review_severity = max(0, 1.0 - (critical_high_count * 0.2))  # 0.0-1.0
    guardrail_pass = passed_gates / total_gates  # 0.0-1.0
    rework = {0: 1.0, 1: 0.5}.get(retries, 0.0)  # 0.0-1.0
    downstream = max(0, 1.0 - (assumption_flags * 0.15))  # 0.0-1.0

    return (completeness * 0.25 +
            review_severity * 0.30 +
            guardrail_pass * 0.20 +
            rework * 0.15 +
            downstream * 0.10)
```

## Root-Cause Tracing

For each HIGH/CRITICAL defect, trace backward:
1. Testing → found the defect
2. Implementation → did the code match the spec?
3. Detailed Design → was the spec correct?
4. Architecture → was the architecture sound?

The "origin phase" is where the defect was introduced.
The "escape phase" is the earliest phase that should have caught it.

## Story-Gap Detection (Rule #16 — NEW)

Silent omissions are MORE DAMAGING than bugs. Detect them by comparing plans against artifacts:

1. **Story-gap analysis**: Compare `story-design-map.json` against actual `src/` files
2. **Per-feature completion %**: Count implemented stories / planned stories per feature
3. **Story-type blind spots**: Track which story types are consistently skipped (file-upload, browser-API, cross-cutting)
4. **Guardrail false negatives**: Guardrails that PASSED when issues existed (MISSING ≠ STUBBED)
5. **Phase-lead compliance**: Did leads execute ALL waves including frontend?

New backpatch categories: `story-gap`, `guardrail-false-negative`, `phase-lead-noncompliance`, `execution-gap`, `design-to-code-gap`, `type-safety-gap`

## Pattern Detection

Look for:
- Same defect category appearing 3+ times → systemic issue
- Same service appearing in 5+ defects → service needs attention
- Same agent with quality < 0.7 across runs → agent needs prompt improvement
- Same guardrail failing across runs → threshold may need adjustment
- Same feature consistently under-implemented across runs → chronic-incomplete-feature (NEW)
- Same story type consistently skipped across runs → story-type-blind-spot (NEW)
- Same guardrail producing false negatives → ineffective-guardrail (NEW)
- Phase lead skipping waves across runs → phase-lead-skip-tendency (NEW)

## Prompt Patching Safety Rules

- APPEND-ONLY: Never delete existing agent instructions
- Use `## Learned Patterns` section (clearly marked as auto-generated)
- Each pattern entry needs: ID, confidence, source run, description
- Require 2+ run occurrences before applying (except CRITICAL)
- Max 10 patches per agent per run
- Max 3 new skills per run
- Max 2 new guardrails per run

## Baseline Management

- Create initial baselines from first run
- Compare current metrics vs baseline on every subsequent run
- Flag regressions >10%
- Reset baselines every 5 runs to prevent normalization
- Never lower baselines without explicit justification

## Common Mistakes
- Mining patterns from a single run (noisy, unreliable)
- Treating all defects equally (only trace HIGH/CRITICAL for root cause)
- Only analyzing DEFECTS — missing the bigger problem of SILENT OMISSIONS (stories never built)
- Trusting guardrail PASS results without verifying what they actually check (false negatives)
- Assuming phase leads executed all waves without reading the run manifest
- Only reviewing what EXISTS without cross-referencing against what was PLANNED
- Over-patching agent prompts (leads to prompt bloat — consolidate)
- Ignoring MEDIUM findings (they become HIGH if they recur)

---



# Feedback Analysis Patterns

Standardizes how the feedback loop agents analyze agent output quality,
detect recurring patterns, trace defects to root causes, and propose
improvements for future runs.

## When to Activate
- When computing quality scores for agent outputs
- When analyzing defect logs for recurring patterns
- When tracing defects backward through phases
- When comparing metrics against baselines
- Used by: metrics-collector, root-cause-tracer, improvement-planner, learning-engine

## Quality Score Computation

Score = Completeness(25%) + ReviewSeverity(30%) + GuardrailPass(20%) + Rework(15%) + Downstream(10%)

```python
def compute_quality_score(agent_data):
    completeness = produced_files / expected_files  # 0.0-1.0
    review_severity = max(0, 1.0 - (critical_high_count * 0.2))  # 0.0-1.0
    guardrail_pass = passed_gates / total_gates  # 0.0-1.0
    rework = {0: 1.0, 1: 0.5}.get(retries, 0.0)  # 0.0-1.0
    downstream = max(0, 1.0 - (assumption_flags * 0.15))  # 0.0-1.0

    return (completeness * 0.25 +
            review_severity * 0.30 +
            guardrail_pass * 0.20 +
            rework * 0.15 +
            downstream * 0.10)
```

## Root-Cause Tracing

For each HIGH/CRITICAL defect, trace backward:
1. Testing → found the defect
2. Implementation → did the code match the spec?
3. Detailed Design → was the spec correct?
4. Architecture → was the architecture sound?

The "origin phase" is where the defect was introduced.
The "escape phase" is the earliest phase that should have caught it.

## Story-Gap Detection (Rule #16 — NEW)

Silent omissions are MORE DAMAGING than bugs. Detect them by comparing plans against artifacts:

1. **Story-gap analysis**: Compare `story-design-map.json` against actual `src/` files
2. **Per-feature completion %**: Count implemented stories / planned stories per feature
3. **Story-type blind spots**: Track which story types are consistently skipped (file-upload, browser-API, cross-cutting)
4. **Guardrail false negatives**: Guardrails that PASSED when issues existed (MISSING ≠ STUBBED)
5. **Phase-lead compliance**: Did leads execute ALL waves including frontend?

New backpatch categories: `story-gap`, `guardrail-false-negative`, `phase-lead-noncompliance`, `execution-gap`, `design-to-code-gap`, `type-safety-gap`

## Pattern Detection

Look for:
- Same defect category appearing 3+ times → systemic issue
- Same service appearing in 5+ defects → service needs attention
- Same agent with quality < 0.7 across runs → agent needs prompt improvement
- Same guardrail failing across runs → threshold may need adjustment
- Same feature consistently under-implemented across runs → chronic-incomplete-feature (NEW)
- Same story type consistently skipped across runs → story-type-blind-spot (NEW)
- Same guardrail producing false negatives → ineffective-guardrail (NEW)
- Phase lead skipping waves across runs → phase-lead-skip-tendency (NEW)

## Prompt Patching Safety Rules

- APPEND-ONLY: Never delete existing agent instructions
- Use `## Learned Patterns` section (clearly marked as auto-generated)
- Each pattern entry needs: ID, confidence, source run, description
- Require 2+ run occurrences before applying (except CRITICAL)
- Max 10 patches per agent per run
- Max 3 new skills per run
- Max 2 new guardrails per run

## Baseline Management

- Create initial baselines from first run
- Compare current metrics vs baseline on every subsequent run
- Flag regressions >10%
- Reset baselines every 5 runs to prevent normalization
- Never lower baselines without explicit justification

## Common Mistakes
- Mining patterns from a single run (noisy, unreliable)
- Treating all defects equally (only trace HIGH/CRITICAL for root cause)
- Only analyzing DEFECTS — missing the bigger problem of SILENT OMISSIONS (stories never built)
- Trusting guardrail PASS results without verifying what they actually check (false negatives)
- Assuming phase leads executed all waves without reading the run manifest
- Only reviewing what EXISTS without cross-referencing against what was PLANNED
- Over-patching agent prompts (leads to prompt bloat — consolidate)
- Ignoring MEDIUM findings (they become HIGH if they recur)
