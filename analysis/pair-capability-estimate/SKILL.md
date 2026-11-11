---
name: pair-capability-estimate
description: "Estimates a refined user story using the adopted estimation methodology. Reads estimation framework from guidelines and methodology from way-of-working. Idempotent: detects existing estimate, confirms rather than re-estimating. Invocable independently or composed by /pair-process-refine-story."
version: 0.4.1
author: Foomakers
---

# /pair-capability-estimate — Story Estimation

Apply the adopted estimation methodology to size a refined user story. Reads the estimation framework from [guidelines](../../../.pair/knowledge/guidelines/collaboration/estimation/README.md) and the adopted methodology from [way-of-working](../../../.pair/adoption/tech/way-of-working.md).

## Arguments

| Argument | Required | Description                                                                                       |
| -------- | -------- | ------------------------------------------------------------------------------------------------- |
| `$story` | Yes      | Story ID to estimate. The story must be in Refined state with acceptance criteria.                |
| `$method`| No       | Override estimation method: `complexity`, `time`, `ai-assisted`, `forecast`, `hybrid`. If omitted, uses the adopted methodology from way-of-working. |

## Algorithm

### Step 1: Load Story

1. **Check**: Read the story from the PM tool (per [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md)).
2. **Verify**: Story exists and has acceptance criteria. If not refined → **HALT**: "Story must be refined before estimation."

### Step 2: Check Existing Estimate

1. **Check**: Does the story already have an estimate (story points, hours, or sizing label)?
2. **Skip**: If no existing estimate, proceed to Step 3.
3. **Act**: Present the existing estimate:

   > Story #`$story` already estimated: **[estimate value]** ([method used]).
   > Re-estimate? (Only if explicitly requested by developer.)

4. **Verify**: If developer confirms current estimate → exit. If developer requests re-estimation → proceed to Step 3.

### Step 3: Determine Estimation Method

1. **Check**: Is `$method` provided?
2. **Skip**: If provided, use it. Proceed to Step 4.
3. **Act**: Read [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) for the adopted estimation methodology.
4. **Act**: If no methodology adopted, read the [Estimation Method Decision Matrix](../../../.pair/knowledge/guidelines/collaboration/estimation/README.md) and recommend based on project context:
   - Team maturity, data availability, time pressure → select recommended primary method.
   - Present recommendation to developer for approval.
5. **Verify**: Method selected.

### Step 4: Read Estimation Guidelines

1. **Act**: Read the methodology-specific guideline:
   - `complexity` → [complexity-based-estimation.md](../../../.pair/knowledge/guidelines/collaboration/estimation/complexity-based-estimation.md)
   - `time` → [time-based-estimation.md](../../../.pair/knowledge/guidelines/collaboration/estimation/time-based-estimation.md)
   - `ai-assisted` → [ai-assisted-estimation.md](../../../.pair/knowledge/guidelines/collaboration/estimation/ai-assisted-estimation.md)
   - `forecast` → [forecast-based-estimation.md](../../../.pair/knowledge/guidelines/collaboration/estimation/forecast-based-estimation.md)
   - `hybrid` → [hybrid-estimation.md](../../../.pair/knowledge/guidelines/collaboration/estimation/hybrid-estimation.md)
2. **Verify**: Guidelines loaded.

### Step 5: Apply Estimation

1. **Act**: Analyze the story using the selected method:
   - **Complexity-based**: Evaluate story complexity against the team's reference stories. Assign story points using the adopted scale (e.g., Fibonacci: 1, 2, 3, 5, 8, 13, 21).
   - **Time-based**: Break story into tasks, estimate hours per task, sum with buffer. Consider skill level and availability.
   - **AI-assisted**: Analyze story description, AC, and technical analysis. Compare with similar completed stories. Propose estimate with confidence level.
   - **Forecast-based**: Use historical velocity and completion data to predict effort. Apply statistical model with confidence interval.
   - **Hybrid**: Apply multiple methods, compare results, converge on consensus estimate.

2. **Act**: Present the estimate to the developer:

   > **Estimation for #`$story`:**
   >
   > | Factor | Assessment |
   > |--------|-----------|
   > | Method | [method name] |
   > | Estimate | [value + unit] |
   > | Confidence | [High/Medium/Low — reason] |
   > | Key Factors | [complexity drivers, risks, unknowns] |
   >
   > Accept this estimate?

3. **Verify**: Developer approves. If developer disagrees → discuss and adjust.

### Step 6: Record Estimate

1. **Act**: Update the story in the PM tool with the approved estimate.
2. **Verify**: Estimate recorded in the story.

## Output Format

```text
ESTIMATION COMPLETE:
├── Story:      [#ID: Title]
├── Method:     [complexity | time | ai-assisted | forecast | hybrid]
├── Estimate:   [value + unit (e.g., 5 SP, 20h, M(3))]
├── Confidence: [High | Medium | Low]
├── Rationale:  [key factors]
└── Status:     [Recorded | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-refine-story`:

- **Input**: `/pair-process-refine-story` may invoke `/pair-capability-estimate` after AC and technical analysis are complete.
- **Output**: Returns the estimate value and method. `/pair-process-refine-story` includes the estimate in the story sizing section.

When invoked **independently**:

- Full interactive flow. Developer selects or confirms method, reviews and approves estimate.

## Graceful Degradation

- If [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) does not specify an estimation methodology, use the Decision Matrix from the estimation guidelines to recommend one.
- If estimation guidelines are not found, fall back to developer judgment: ask the developer to provide an estimate directly and record it.
- If the PM tool is not accessible, present the estimate and ask the developer to record it manually.
- If the story has no acceptance criteria, warn: "Story lacks AC — estimation may be inaccurate. Consider refining first."

## Notes

- This skill **modifies the PM tool** — it writes the estimate to the story issue.
- **Idempotent**: re-invocation on an already-estimated story confirms the existing estimate without re-doing the analysis. Re-estimation only happens on explicit developer request.
- The estimation method should be consistent within a project. If the team switches methods, record the decision via `/pair-capability-record-decision`.
- Estimation is a collaborative activity — the skill proposes, the developer decides. The skill never overrides developer judgment.
