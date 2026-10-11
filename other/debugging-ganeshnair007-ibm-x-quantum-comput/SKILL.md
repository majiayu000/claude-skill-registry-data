---
name: debugging
description: Reproduce software defects, isolate root causes via stack traces and forensic logs, and apply surgical fixes.
---

# Systematic Debugging

## Methodical Triage Loop
1. **Reproduce:** Capture minimal reproducible command or test case that triggers the defect.
2. **Inspect:** Examine full error trace, correlation logs, and variable state at the point of failure.
3. **Isolate:** Formulate falsifiable hypotheses regarding the root cause.
4. **Fix:** Implement the minimal sufficient correction preserving existing contracts.
5. **Verify:** Rerun reproduction case and full regression suite to prove resolution.
