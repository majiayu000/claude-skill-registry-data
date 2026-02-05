---
name: debugger
description: Use when the root cause is unclear. Trace the failure back through the call stack and isolate the first bad state.
---

## Workflow

1. Identify the first observable failure (error, wrong output, crash).
2. Walk backwards: failure site → immediate caller → upstream inputs.
3. At each step, record the state you expect vs what you observe.
4. Find the first divergence (the earliest place state becomes invalid).
5. Fix the earliest divergence, not the downstream symptom.
6. Validate by re-running the original scenario and one adjacent edge case.

## Notes

- Prefer adding temporary logs/assertions to confirm hypotheses, then remove them.
