---
name: code-review
description: Review a diff for correctness, edge cases, regressions and maintainability, with blocking findings separated from suggestions.
---

# Code review: find the defect before the style debate

- Read the change's intent first, then the diff. A correct patch in the wrong place is still a defect.
- Check correctness before style: boundary conditions, error paths, null or empty input, authorization, concurrency and data consistency.
- Trace the changed data through its callers and callees. Look for behaviour that changed outside the edited lines.
- Demand tests for new behaviour and regressions. A test that only asserts the implementation exists is not enough.
- Review naming, structure and duplication only where they affect comprehension or future change; do not relitigate preferences.
- Flag security-sensitive changes explicitly and hand them to the secure review playbook rather than improvising a security audit.
- Separate blocking defects from suggestions. State the evidence and the smallest acceptable fix.

---

_NullByte skill pack. Original guidance for this tool; no third-party skill text is bundled._
