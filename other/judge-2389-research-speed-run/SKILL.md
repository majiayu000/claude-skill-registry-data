---
name: judge
description: Scores parallel implementations with a 5-criteria worksheet (fitness, justified complexity, readability, robustness, maintainability; 25 points max), hard gates on score=1 or Fitness delta>=2, and Speed-Run efficiency tiebreakers. Invoked automatically by speed-run:showdown and speed-run:any-percent at Phase 4; not for direct user invocation.
---

# Speed-Run Judge

Score implementations using the 5-criteria framework. Fill out ALL sections exactly as shown.

**Terminology:** This skill uses "impl" but works for both:
- Showdown: runner-1, runner-2, runner-3 (same design, different implementations)
- Any%: variant-a, variant-b (different approaches/designs)

## REQUIRED OUTPUT FORMAT

See `references/scorecard-template.md` for the complete output template. Do not summarize or abbreviate any section.

## Scoring Reference

### Scores Meaning
| Score | Meaning |
|-------|---------|
| 5 | Excellent - exceeds expectations |
| 4 | Good - fully meets requirements |
| 3 | Adequate - core works, some gaps |
| 2 | Poor - significant issues |
| 1 | Critical flaw - disqualifying |

### Hard Gates (Automatic)

1. **Fitness Gate:** If Fitness Δ ≥ 2 between impls → Higher fitness WINS immediately
2. **Critical Flaw:** If ANY criterion = 1 → That impl is ELIMINATED

#### Fitness Gate Interpretation

The Fitness Gate triggers the same way in both contexts, but means different things:

| Context | What Fitness Δ ≥ 2 Means |
|---------|--------------------------|
| **Showdown** | One runner *deviated from or misunderstood the design*. All runners should have similar Fitness since they're implementing the same spec. A large gap is a red flag. |
| **Any%** | One approach *genuinely solves the problem better*. Different approaches can legitimately have different Fitness. A large gap means one approach is clearly superior. |

In both cases, higher Fitness wins. The interpretation just explains *why* the gap exists.

### Tiebreaker: Speed-Run Efficiency

When total scores are tied or within 1 point, prefer the implementation that:
1. Used fewer hosted LLM fix cycles (cleaner contract prompts)
2. Had fewer total hosted LLM calls (better task decomposition)
3. Generated code faster (simpler, more focused prompts)

This rewards better use of the speed-run pipeline, not just code quality.

### Feasibility Red Flags

Check before scoring:
- O(n²) or worse on unbounded data
- Unbounded memory growth
- Self-DDoS patterns (polling, no backoff)
- Missing pagination
- Blocking I/O in hot path
- No error recovery

## Process

1. **Read** all implementation code (should already be in context)
2. **Fill out** the worksheet for EACH implementation - do not skip sections
3. **Fill out** the Speed-Run Metrics table
4. **Check** hard gates
5. **Announce** winner with rationale (include token efficiency note)

**CRITICAL:** Use integer scores only (1-5). Do not use half points like 4.5.

**CRITICAL:** Fill out every checkbox. Do not summarize or abbreviate the worksheet.
