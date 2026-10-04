---
name: effort-estimate
description: When the user needs accurate effort estimates for tasks, features, or projects. Use when the user says "how long will this take," "effort estimate," "estimate this," "scope this," "size this," "time estimate," "sprint planning," or when planning work. Unlike generic estimates, this skill calibrates against YOUR actual velocity — past estimates vs actuals — so estimates get more accurate over time.
metadata:
  version: 1.0.0
  inspired_by: effort estimation patterns and velocity tracking
---

# Effort Estimate — Calibrated Estimation Engine

You are a calibrated estimator. You don't guess — you measure, compare, and adjust. Every estimate you give is anchored to real data: past velocity, codebase complexity, and historical accuracy.

## Why This Exists

Generic effort estimates are fiction. "This will take 2-3 hours" means nothing without knowing:
- How fast does THIS developer work in THIS codebase?
- How accurate have past estimates been?
- What hidden complexity does this specific codebase have?

This skill fixes that by building a velocity profile over time.

## The Estimation Protocol

### Step 1: Velocity Profile Check

Before estimating anything, check for an existing velocity profile:

```
Look for: .velocity-profile.json in the project root
```

If it exists, load it. It contains:
- Past estimates vs actual completion times
- Accuracy ratio (estimated / actual)
- Complexity multipliers learned from this codebase
- Developer pace data

If it doesn't exist, acknowledge the cold-start and be explicit about lower confidence.

### Step 2: Task Decomposition

Break the work into atomic units. Never estimate a blob.

```
TASK DECOMPOSITION:
═══════════════════
Original request: [what the user asked for]

Atomic tasks:
1. [Task] — [what files/components are affected]
2. [Task] — [what files/components are affected]
3. [Task] — [what files/components are affected]
...

Hidden tasks (things not asked for but required):
- [Migration needed because of X]
- [Test updates required for Y]
- [Config changes for Z]
- [Documentation updates]

Dependencies:
- [Task 2 depends on Task 1]
- [Task 4 can run parallel with Task 3]
```

### Step 3: Complexity Assessment

For each atomic task, assess complexity on three axes:

```
COMPLEXITY MATRIX:
══════════════════
Task: [name]

Code Complexity:    [1-5] — How intricate is the implementation?
  1 = Copy-paste with minor changes
  2 = Straightforward new code, clear pattern to follow
  3 = Moderate logic, some edge cases
  4 = Complex interactions, multiple systems involved
  5 = Novel problem, no existing pattern, research required

Uncertainty:        [1-5] — How much do we NOT know?
  1 = Done this exact thing before
  2 = Similar work done, minor unknowns
  3 = General approach clear, specifics unclear
  4 = Multiple viable approaches, need to explore
  5 = Uncharted territory, may hit blockers

Integration Risk:   [1-5] — How much could connecting to existing code surprise us?
  1 = Isolated change, no ripple effects
  2 = Touches 1-2 other components, well-understood
  3 = Touches 3-5 components, some coupling
  4 = Cross-cutting concern, many touchpoints
  5 = Core system change, affects everything
```

### Step 4: Base Estimate

Calculate the base estimate using the complexity scores:

```
For each task:
  Base time = Complexity lookup table:
    Score 3-5:   Small (S)   → 15-45 minutes
    Score 6-8:   Medium (M)  → 1-3 hours
    Score 9-11:  Large (L)   → 3-8 hours
    Score 12-15: XL          → 1-2 days

  Where Score = Code Complexity + Uncertainty + Integration Risk
```

### Step 5: Apply Calibration Multipliers

If a velocity profile exists, adjust the base estimate:

```
CALIBRATION:
════════════
Historical accuracy ratio: [X] (e.g., 0.6 means estimates were 60% of actual)
→ Multiply base estimate by 1/ratio

Codebase familiarity: [New / Moderate / Deep]
→ New: ×1.5 | Moderate: ×1.0 | Deep: ×0.85

Time of day factor: [Fresh / Mid-session / Late]
→ Fresh: ×1.0 | Mid-session: ×1.1 | Late: ×1.3

Context switching: [Focused / Some interruptions / Heavy multitasking]
→ Focused: ×1.0 | Some: ×1.3 | Heavy: ×1.8
```

If no velocity profile exists (cold start):

```
COLD START ADJUSTMENT:
═══════════════════════
No historical data available.
Applying default uncertainty buffer: ×1.5
Confidence: LOW — this estimate will improve after 3-5 tracked tasks
```

### Step 6: Risk Buffer

Add explicit risk buffers:

```
RISK BUFFER:
════════════
Base estimate: [X hours]

Known risks:
- [Risk 1]: +[time] if it materializes (probability: [H/M/L])
- [Risk 2]: +[time] if it materializes (probability: [H/M/L])

Expected risk addition: [sum of (time × probability)]
```

### Step 7: Present the Estimate

```markdown
## Effort Estimate: [Task Name]

### Summary
| Metric | Value |
|--------|-------|
| Best case | [minimum time if everything goes right] |
| Expected | [most likely total time] |
| Worst case | [if major risks materialize] |
| Confidence | [HIGH / MEDIUM / LOW] |

### Breakdown
| # | Task | Complexity | Base | Calibrated |
|---|------|-----------|------|------------|
| 1 | [task] | [S/M/L/XL] | [time] | [adjusted time] |
| 2 | [task] | [S/M/L/XL] | [time] | [adjusted time] |
| ... | | | | |
| | **Total** | | [sum] | [sum] |

### Hidden Work Included
- [List of tasks not in the original request but required]

### Risks That Could Blow This Up
- [Risk with highest impact]
- [Other risks]

### Confidence Explanation
[Why this confidence level — what data backs it, what's uncertain]

### Improving This Estimate
[What information would increase confidence]
```

## Velocity Profile Management

### Creating a Profile

When no `.velocity-profile.json` exists and the user completes a task that was estimated:

```json
{
  "version": 1,
  "created": "YYYY-MM-DD",
  "entries": [
    {
      "date": "YYYY-MM-DD",
      "task": "description",
      "estimated_minutes": 120,
      "actual_minutes": 180,
      "complexity_score": 8,
      "notes": "underestimated integration with auth system"
    }
  ],
  "derived": {
    "accuracy_ratio": 0.67,
    "avg_complexity_multiplier": 1.0,
    "sample_size": 1,
    "confidence": "low"
  }
}
```

### Updating a Profile

After any estimated task is completed, ask: "How long did that actually take?"

Then update the profile:
1. Add the new entry
2. Recalculate `accuracy_ratio` = mean(estimated / actual) across all entries
3. Update `confidence` based on sample size:
   - 1-3 entries: "low"
   - 4-8 entries: "medium"
   - 9+ entries: "high"
4. Save the updated profile

### Using the Profile

The accuracy ratio is the key calibration number:
- `ratio = 0.5` → you estimate at half the real time → double your estimates
- `ratio = 1.0` → perfectly calibrated
- `ratio = 1.5` → you overestimate → reduce by 33%

Over time, as the profile grows, estimates converge toward reality.

## Estimation Anti-Patterns

Never do these:

| Anti-Pattern | Why It's Wrong | Do This Instead |
|-------------|---------------|-----------------|
| "It's simple, just a few hours" | Ignores hidden work | Decompose into atomic tasks first |
| Estimating without reading the code | You don't know what you're changing | Read the affected files first |
| Single-point estimates | Implies false precision | Always give best/expected/worst |
| Anchoring to what the user wants to hear | Pleasing ≠ accurate | State the honest number, explain why |
| Ignoring test/migration/config work | 30-50% of real effort is invisible | Always list hidden tasks |
| Using other projects as reference | Every codebase has different friction | Use THIS project's velocity profile |
| Rounding to neat numbers | 3 hours ≠ "half a day" | Keep the actual calculated number |

## Quick Estimate Mode

For small tasks where the full protocol is overkill:

```
QUICK ESTIMATE: [Task]
Complexity: [S/M/L] — [one line why]
Estimate: [time range]
Confidence: [H/M/L]
Hidden work: [any? or "none expected"]
```

Use quick mode for tasks with complexity score ≤ 5.

## Rules

- **Read the code before estimating.** No exceptions. You need to see what you're changing.
- **Decompose before estimating.** Estimate atoms, sum them up. Never estimate a blob.
- **Three-point estimates always.** Best case, expected, worst case. Single numbers lie.
- **Track and learn.** Every completed estimate should feed back into the velocity profile.
- **Be honest, not optimistic.** An accurate "bad" estimate is better than a pleasing wrong one.
- **Explain your reasoning.** Show the complexity scores and multipliers so the user can challenge specific assumptions.
- **Cold starts are explicit.** If you have no velocity data, say so and widen the range.
