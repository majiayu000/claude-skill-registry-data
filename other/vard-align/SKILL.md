---
name: vard-align
description: Quick feasibility and novelty check — go/no-go decision for this week's build
type: analysis
version: v0.0
context_intake: scoped
---

# VARD Align

Invoke as `/vard-align`.

Rapid alignment check for a VARD candidate. Validates whether the concept is worth shipping this week and produces a 1-page go/no-go alignment doc.

## Process

1. **Identify candidate:** Read the most recent vard-scan output or `$ARGUMENTS` for the concept to evaluate.
2. **Light interview (1-3 questions):** Ask only what's needed to resolve ambiguity:
   - Target audience or distribution channel unclear?
   - Technical feasibility question?
   - Scope creep risk?
3. **Check dimensions:**
   - **Feasibility:** Can this ship in 1-3 days with available tech? Any blockers?
   - **Novelty:** Does a good-enough version already exist? What's the differentiation?
   - **Distribution fit:** Is there a clear, free or cheap channel to reach users?
   - **Timing:** Is this time-sensitive? Will the window close?
   - **Downside:** What's the worst case if it flops? (Should be: "we lost 2 days")
4. **Verdict:** GO or NO-GO with one-line rationale.
5. **If GO:** Produce a 1-page alignment doc:
   - Concept (2-3 sentences)
   - Target user
   - Core feature (the one thing it does)
   - Tech stack recommendation
   - Ship deadline (date)
   - Success metric (what "traction" means for this experiment)
   - Distribution plan (launch day channels)

## Output

Write alignment doc to `alignment/vard-<slug>.md` if GO. End with:

```md
**Verdict:** GO / NO-GO
**Next work:** <build the app / scan for another candidate>
**Recommended next command:** /vard-ship / /vard-scan
```

## Constraints

- Do not begin implementation.
- Keep the alignment doc to 1 page — resist scope creep.
- If the candidate came from vard-scan, reference it; don't re-research from scratch.
- Do not run expensive external research. Quick web searches are fine.

## Default Shipping Contract

Follow the shared shipping contract convention.
