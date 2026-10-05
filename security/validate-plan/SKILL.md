---
name: mk:validate-plan
version: 1.0.0
preamble-tier: 3
description: Validates an approved plan against 8 dimensions before Phase 3 begins. Catches incomplete acceptance criteria, missing dependencies, and unresolved risks. Use after Gate 1 approval and before Phase 2 (Test). Produces a validation report with pass/fail per dimension.
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
source: new
keywords:
  - validate-plan
  - plan-validation
  - gate-1-pass
  - acceptance-criteria-check
  - 8-dimension-validation
when_to_use: Use after Gate 1 plan approval and before Phase 2 — validates plan against 8 dimensions. NOT for creating plans (see mk:plan-creator).
user-invocable: true
owner: lifecycle
criticality: high
status: active
runtime: claude-code
---

# Plan Validation — 8-Dimension Quality Check

Audits an approved plan against 8 dimensions to catch gaps before implementation begins.
Does NOT replace Gate 1 (human approval), modify plans, or route edits itself. If it
finds an Insert or Split mutation is needed, the planner performs it and returns to
Gate 1 for re-approval; Skip and Reorder changes require notification plus audit log.

> For green-field harness sprints (generator↔evaluator loop), use `mk:sprint-contract` instead. `mk:validate-plan` operates on plans from `mk:plan-creator` (cook flow only).

## When to Use

- After Gate 1 approval, before Phase 2 (Test)
- When `/mk:cook` detects a COMPLEX task (auto-suggested)
- When user wants to stress-test a plan before committing to implementation
- When user says "validate this plan", "check my plan", "is this plan complete"

## 8 Validation Dimensions

| #   | Dimension                   | Pass Criteria                                                        | Common Failure                                               |
| --- | --------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------ |
| 1   | **Scope Clarity**           | In-scope and out-of-scope sections are explicit and non-overlapping  | Vague scope: "improve the auth system" without boundaries    |
| 2   | **Acceptance Criteria**     | Every criterion is binary (pass/fail), not subjective                | Subjective: "should feel fast" vs binary: "response < 200ms" |
| 3   | **Dependencies Resolved**   | All external dependencies identified with status (available/blocked) | Missing: needs DB migration but not listed as dependency     |
| 4   | **Risks Identified**        | At least 1 risk flag with mitigation strategy                        | No risks listed (every plan has risks; zero = not evaluated) |
| 5   | **Architecture Documented** | Technical approach references existing patterns or includes ADR      | "We'll figure out the architecture during implementation"    |
| 6   | **Test Strategy**           | Test approach covers acceptance criteria; edge cases identified      | "We'll add tests after" (violates TDD)                       |
| 7   | **Security Considered**     | Auth, data access, input validation addressed (or explicitly N/A)    | No mention of security for a feature handling user data      |
| 8   | **Effort Estimated**        | Time/complexity estimate with confidence level                       | No estimate or "it depends" without qualification            |

## Workflow

1. **Load plan file** — Read from `tasks/plans/YYMMDD-name/plan.md`
2. **Check each dimension** — Evaluate against pass criteria
3. **Produce validation report** — Pass/fail per dimension with findings
4. **Route result:**
   - All 8 PASS → proceed to Phase 2
   - Any FAIL → return to planner with specific revision requests
   - WARN (partially met) → user decides: proceed or revise

## Output Format

```markdown
## Plan Validation: [Plan Name]

| #   | Dimension               | Status         | Finding            |
| --- | ----------------------- | -------------- | ------------------ |
| 1   | Scope Clarity           | PASS/FAIL/WARN | [specific finding] |
| 2   | Acceptance Criteria     | PASS/FAIL/WARN | [specific finding] |
| 3   | Dependencies Resolved   | PASS/FAIL/WARN | [specific finding] |
| 4   | Risks Identified        | PASS/FAIL/WARN | [specific finding] |
| 5   | Architecture Documented | PASS/FAIL/WARN | [specific finding] |
| 6   | Test Strategy           | PASS/FAIL/WARN | [specific finding] |
| 7   | Security Considered     | PASS/FAIL/WARN | [specific finding] |
| 8   | Effort Estimated        | PASS/FAIL/WARN | [specific finding] |

**Result:** [N]/8 passed | [Action: proceed / revise dimensions X,Y]
```

## Whole-Plan Consistency Sweep (final pre-emit step)

After scoring the 8 dimensions and BEFORE emitting the validation report, run a cross-file consistency check on the plan directory.

**Why:** Distributed plans (`plan.md` + N × `phase-*.md`) drift after edits. One phase gets renamed; another phase still references the old name. Each phase reads as self-consistent but the plan as a whole is contradictory.

**Procedure:**
1. Re-read `plan.md` and every `phase-*.md` in the plan dir
2. Build a delta of: renamed entities, scope changes, dropped features, decision changes
3. Grep every plan file for stale references to renamed/dropped items
4. Reconcile contradictions across files (not only the file that surfaced them)

**Output:** Append a `sweep_failures` block to the validation report. Sweep failures DO NOT auto-FAIL — they surface inconsistencies the human must reconcile before Phase 3.

```
sweep_failures:
  - phase-02.md:18  references `userController` (renamed to `authController` in plan.md:42)
  - phase-04.md:8   declares scope item that plan.md:62 marks out-of-scope
```

**Skip conditions:** plan has only `plan.md` (no phase files); plan dir not found.

**Source:** Adapted from external verification-role guidance for whole-plan consistency sweeps.

## Integration with Cook Workflow

In `/mk:cook`, validation runs automatically for COMPLEX tasks:

```
Gate 1 (plan approved) → mk:validate-plan → Phase 2 (Test)
```

For STANDARD tasks, validation is optional (user-triggered).
For TRIVIAL tasks, validation is skipped.

## Gotchas

- **Not the same as `validate-plan.py`**: The script at `mk:plan-creator/scripts/validate-plan.py` validates plan file *structure* (required sections exist). This skill validates plan *content quality* (are acceptance criteria binary? are risks identified?). Both can run — they check different things.

## Relationship to plan-creator v2.3.1

Note: plan-creator's step-06 now includes an enhanced validation interview with detection keywords and section mapping. mk:validate-plan focuses on 8-dimension structural validation, which is complementary — not a replacement.

## What This Skill Does NOT Do

- Does NOT replace Gate 1 — human approval still required
- Does NOT modify plan files — read-only analysis
- Does NOT generate tests — that's Phase 2 (tester agent)
- Does NOT block Gate 1 — runs after Gate 1, before Phase 2
