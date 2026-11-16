---
name: systematic-debugging
description: Diagnose a bug or failing test by proving its root cause before changing code. Use when behavior is incorrect, flaky, or unexpectedly different.
---

# Systematic Debugging

1. **Reproduce:** capture command or user path, inputs, environment, expected result, and actual result.
2. **Preserve evidence:** inspect the complete error, logs, failing assertion, and relevant diff. Avoid exposing secrets or personal data.
3. **Trace:** follow the failing value/control flow from entry point to failure; inspect boundaries, state, concurrency, and error handling.
4. **Hypothesize:** rank a small number of plausible causes by evidence.
5. **Experiment:** run a minimal reproducer or one-variable-at-a-time checks that distinguish hypotheses.
6. **Explain:** state the mechanism that caused the failure, or explicitly state what remains unknown.
7. **Fix narrowly:** change the causal path and add a regression test where practical.
8. **Verify:** rerun the reproducer and relevant checks; inspect for regressions.

Avoid random edits, speculative dependency upgrades, broad exception swallowing, and retries/sleeps without evidence of a transient failure. A workaround is not a proven root-cause fix; label it accurately.
