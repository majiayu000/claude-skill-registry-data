---
name: cm-planning
description: "You MUST use this before any creative work or multi-step task. Explores intent and writes execution-ready plans before coding."
token_budget: 1500
compressed: true
deprecated: false
---

# Planning — Brainstorm + Execution-Ready Plans

## TL;DR
- **Use before** any feature, behavior change, or task needing 3+ actions.
- **Brainstorm** intent, 2–3 approaches, recommendation, scope, and interfaces.
- **Write** `openspec/changes/<name>/{design.md,tasks.md}`.
- **Emit** `.cm/handoff/plan.json` with complete `task_specs`; `first_tasks`-only handoffs remain readable for backward compatibility.
- **Next**: `cm-tdd` or `cm-execution`.

## Phase A: Decide What to Build

1. Ask only questions that change scope or architecture. State assumptions and mark each `verified` or `needs confirmation`.
2. Present 2–3 approaches with concrete tradeoffs and recommend one.
3. Separate must-have, optional, handled edges, and explicit non-goals.
4. Map data flow, file responsibilities, public interfaces, and dependencies. UI work also uses `cm-design-system`.

Stop if intent, ownership, or an interface is ambiguous. Do not silently choose an interpretation.

## Phase B: Write the Plan

Create `design.md` with context, chosen architecture, file map, interfaces, risks, and verification strategy. Create `tasks.md` using the template below.

### Task boundary

A task is the smallest independently testable deliverable that a reviewer can approve or reject without deciding another task. Each task owns a complete red–green cycle and ends at a commit boundary. Fold setup, configuration, migrations, and documentation into the deliverable that needs them; never create empty setup-only or docs-only tasks.

Each step is exactly one 2–5 minute action: write one failing test, run it and observe the expected failure, add minimal implementation, run it and observe the pass, then commit. Never use 15–30 minute checklist items.

### Required task template

````markdown
### Task 1: Validate rich plan handoffs

**Goal:** Reject incomplete task specs while preserving legacy `plan@1` payloads.
**Deliverable:** A validator and focused tests that can pass review independently.
**Files:**
- Modify: `src/handoff/io.ts`
- Test: `test/handoff.test.ts`
**Dependencies:** Existing `validateHandoff(obj: unknown)` behavior.
**Interfaces:** Produces optional `PlanHandoff.data.task_specs`; consumes `PlanTaskSpec`.
**Acceptance criteria:** A complete rich handoff round-trips; a missing `deliverable` is rejected; a legacy handoff remains valid.

- [ ] **Step 1 — Write the failing validation test** in `test/handoff.test.ts` with `expect(() => validateHandoff(fixture)).toThrow(/missing key: deliverable/)`.
- [ ] **Step 2 — Prove RED.** Run `npx vitest run test/handoff.test.ts`. Expected: FAIL at `rejects incomplete rich plan task specs` because no error is thrown.
- [ ] **Step 3 — Implement the minimum validation** in `src/handoff/io.ts` for required rich-task fields without changing legacy required keys.
- [ ] **Step 4 — Prove GREEN.** Run `npx vitest run test/handoff.test.ts`. Expected: PASS, all handoff tests and zero failures.
- [ ] **Step 5 — Commit boundary.** Run `git add src/handoff/io.ts test/handoff.test.ts && git commit -m "feat: validate rich plan handoffs"`.
````

Every task must specify: goal, independently reviewable deliverable, exact create/modify/test paths, dependencies, consumed/produced interfaces with exact names and types, literal acceptance criteria, step-level test phase, exact command and expected result, and commit boundary. Repeat context needed by a fresh agent; never require it to reread the full plan.

## No Placeholders

Never write `TODO`, `TBD`, “add tests,” “handle edge cases,” “appropriate error handling,” “similar to Task N,” or an undefined type/function. Code steps include the concrete code or signature; verification steps include the exact command and observable evidence.

## Self-Review Before Handoff

1. **Coverage:** map every requirement and non-goal to a task; add any missing coverage.
2. **Placeholder scan:** search `tasks.md` for every banned phrase above and replace vague instructions.
3. **Interface/type consistency:** compare all produced and consumed names, signatures, field names, and task dependencies.
4. **Boundaries:** confirm every task has its own deliverable, test cycle, review decision, and commit; merge setup/docs fragments into their owning task.

Fix findings inline before emitting the handoff.

## Emit Handoff + Continuity

Write `.cm/handoff/plan.json`:

```json
{
  "schema": "plan@1",
  "emitted_at": "2026-08-04T00:00:00.000Z",
  "emitted_by": "cm-planning",
  "data": {
    "goal": "Validate execution-ready plan handoffs",
    "decisions": ["Keep task_specs optional for plan@1 compatibility"],
    "first_tasks": ["1.1"],
    "openspec_path": "openspec/changes/rich-plan-handoff/",
    "task_specs": [{
      "id": "1.1",
      "goal": "Validate complete task specifications",
      "deliverable": "A backward-compatible validator with focused coverage",
      "files": [
        { "path": "src/handoff/io.ts", "action": "modify" },
        { "path": "test/handoff.test.ts", "action": "modify" }
      ],
      "dependencies": ["validateHandoff(obj: unknown)"],
      "interfaces": {
        "consumes": ["PlanTaskSpec from src/handoff/contracts.ts"],
        "produces": ["PlanHandoff.data.task_specs?: PlanTaskSpec[]"]
      },
      "acceptance_criteria": ["Rich handoffs round-trip and legacy handoffs remain valid"],
      "steps": [
        {
          "id": "1.1.1",
          "action": "Add the failing incomplete-task validation test",
          "files": ["test/handoff.test.ts"],
          "test_cycle": {
            "phase": "red",
            "command": "npx vitest run test/handoff.test.ts",
            "expected_result": "FAIL because incomplete task_specs are accepted"
          }
        },
        {
          "id": "1.1.2",
          "action": "Implement required-field validation and rerun the focused test",
          "files": ["src/handoff/io.ts"],
          "test_cycle": {
            "phase": "green",
            "command": "npx vitest run test/handoff.test.ts",
            "expected_result": "PASS with all handoff tests and zero failures"
          }
        }
      ],
      "verification": {
        "command": "npx vitest run test/handoff.test.ts",
        "expected_result": "All handoff tests pass with zero failures"
      },
      "commit_boundary": "Commit the contract, validator, and focused tests together"
    }]
  }
}
```

Update `.cm/CONTINUITY.md`: Active Goal, first three Next Actions, Current Phase `planning`, and key decisions. Downstream execution reads each `task_specs` entry directly; it must not need the full plan to start that task.
