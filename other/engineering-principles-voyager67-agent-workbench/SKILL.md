---
name: engineering-principles
description: Apply the default engineering bar to non-trivial coding work. Use when planning or changing software; keep trivial edits proportionate.
---

# Engineering Principles

Use these as a quality bar, not as a rigid ceremony. Scale the process to the risk and size of the task.

1. **Understand before acting.** Inspect the relevant code, tests, conventions, user goal, and constraints. Surface material ambiguity instead of silently inventing requirements.
2. **Prefer the smallest complete solution.** Avoid speculative features, unnecessary abstractions, new dependencies, and broad rewrites.
3. **Make traceable changes.** Each meaningful edit should support the requested outcome. Preserve unrelated user work and existing conventions.
4. **Prove behavior.** Choose tests and checks that exercise the changed path. Inspect results rather than assuming a command passed.
5. **Debug causes, not symptoms.** Reproduce the issue, trace the failing path, and validate the causal explanation before fixing.
6. **Keep security in scope.** Protect secrets, validate trust boundaries, and seek approval before destructive or externally visible actions.
7. **Report honestly.** Separate completed work, attempted checks, unverified assumptions, and remaining risks. Never invent test results or performance gains.

For an obvious one-line change, do not run a full project ceremony. For high-risk changes, increase verification and request human review at the relevant decision points.
