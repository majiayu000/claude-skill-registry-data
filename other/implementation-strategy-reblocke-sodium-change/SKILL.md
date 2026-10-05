---
name: implementation-strategy
description: Use before non-trivial code, workflow, documentation, or repository-structure changes to produce a scoped implementation strategy with risks and verification.
---

# Implementation Strategy

- Read `AGENTS.md`, relevant docs, manifests, tests, and entry points before editing.
- State the goal, success criteria, assumptions, ambiguities, tradeoffs, and the simpler alternative.
- Name the files or subsystems expected to change and the verification commands that will prove success.
- Prefer the smallest behavior-preserving diff; do not change scientific meaning, public APIs, or UI interpretation unless requested.
- For bug fixes, reproduce or characterize the failure first; for refactors, verify behavior before and after.
- If a high-impact ambiguity remains after inspection, ask before editing.
