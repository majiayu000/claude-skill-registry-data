---
name: sdd-workflow
description: Use this skill when the user asks to build a new feature or write implementation code. Enforces the Spec-Driven Development (SDD) 4-phase workflow before any code is written.
---

### Spec-Driven Development Workflow (TTA.dev)

**No implementation code may be written before completing the SDD phases.**

#### The 4 Phases

Execute these phases **sequentially**. No phase may be skipped.

1. **`/specify`** — Functional Specification (The "What")
   - User journeys, edge cases, success criteria, out-of-scope
   - Output: Markdown document for user review and approval

2. **`/plan`** — Technical Plan (The "How")
   - Which packages are affected (`tta-dev-primitives`, `tta-observability-integration`, etc.)
   - New modules, classes, functions to create
   - How the feature composes with existing primitives (`>>`, `|`)
   - External dependencies with justification
   - Observability strategy (traces, metrics, logs)

3. **`/tasks`** — Task Breakdown
   - Isolated, testable work units
   - Each task includes acceptance test description
   - Numbered by dependency (topological sort)
   - Format: Markdown checklist

4. **`/implement`** — Test-Driven Implementation
   - **Red**: Write failing test encoding acceptance criteria
   - **Green**: Minimal implementation to pass the test
   - **Refactor**: Clean up while tests stay green
   - Run quality gate before marking task complete

#### Exceptions

- **`/spike`**: User explicitly requests prototype code. Spike code must never be merged without going through the full SDD workflow afterward.

#### Enforcement

- If the user asks for code without a spec, initiate `/specify` first and explain the SDD process.
- Reference this constitution by section (e.g., "Per §2 Phase 1, I need to generate a spec first.").

#### Deep Reference

For the complete SDD Constitution with all tables and detailed guidance, see [`docs/agent-guides/sdd-constitution.md`](../../docs/agent-guides/sdd-constitution.md).
