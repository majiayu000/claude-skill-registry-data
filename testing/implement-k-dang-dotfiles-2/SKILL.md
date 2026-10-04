---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
disable-model-invocation: true
---

Implement the work described by the user in the PRD or issues.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly and single test files throughout implementation. At the end, run the smallest relevant suite that covers the changed behavior: changed specs, directly affected public seams, and relevant component integration specs. Run the full test suite only when it is reasonably bounded; for large suites, leave full-suite execution to CI and report the exact focused suites run plus any coverage omitted.

Once done, use /matt-code-review to review the work.
