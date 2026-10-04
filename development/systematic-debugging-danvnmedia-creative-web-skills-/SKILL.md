---
name: systematic-debugging
description: Use for any bug, failing test, build/runtime failure, unexpected behavior, or performance regression; require reproduction, evidence, causal hypothesis, minimal experiment, root-cause fix, and regression verification before completion.
---
# Systematic Debugging

**No symptom patch before root-cause investigation.**

1. Read the first meaningful error/stack trace completely.
2. Reproduce and write exact steps, inputs, environment, and frequency.
3. Inspect recent changes and a similar working path.
4. Trace state/data across component boundaries; add temporary diagnostics when needed.
5. State one causal hypothesis: `X causes Y because evidence Z`.
6. Test one variable with the smallest experiment.
7. Once confirmed, create a failing regression test or deterministic reproduction.
8. Implement one root-cause fix. Avoid opportunistic refactors.
9. Run the narrow regression, then broader relevant checks, then runtime verification if applicable.
10. After two blind fixes, stop guessing. After three failed causal fixes, reconsider architecture with the human.
