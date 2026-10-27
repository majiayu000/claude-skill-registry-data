---
name: kiro-review
description: Review a task implementation against approved specs, task boundaries, and verification evidence. Use after an implementer finishes a task, after remediation, or before accepting a task as complete.
allowed-tools: Read, Bash, Grep, Glob, Skill
argument-hint: <task-id>
---

> **移植说明**｜本文件是 `kiro` skill 的阶段规范（源自 `kiro-review` skill），由 kiro 总控按需读取并就地执行。
> 文中出现的 `kiro-xxx` / `/kiro-xxx` skill 引用，一律按 `kiro/SKILL.md` 的「阶段解析规则」处理：
> 宿主已注册同名 skill → `Skill(kiro-xxx)`；否则读 `phases/xxx/SKILL.md` 就地执行。
> 相对路径（`rules/`、`templates/`）一律相对本文件所在目录 `phases/review/`。

# kiro-review

## Overview

This skill performs task-local adversarial review. It verifies that the implementation is real, complete, bounded, aligned with approved requirements and design, and supported by mechanical verification evidence.

Boundary terminology continuity:
- discovery identifies `Boundary Candidates`
- design fixes `Boundary Commitments`
- tasks constrain execution with `_Boundary:_`
- review rejects concrete `Boundary Violations`

## When to Use

- After an implementer reports `READY_FOR_REVIEW`
- After remediation for a rejected review
- Before marking a task `[x]`
- Before accepting a task into feature-level validation

Do not use this skill to invent missing requirements or silently reinterpret the spec.

## Inputs

Provide:
- Task ID and exact task text from `tasks.md`
- Relevant requirement section numbers
- Relevant design section numbers
- Spec file paths (`requirements.md`, `design.md`, optionally `tasks.md`)
- The implementer's status report
- The task `_Boundary:_` scope constraints
- Validation commands discovered by the controller
- Relevant steering excerpts when applicable
- Relevant `## Implementation Notes` entries when applicable

## Outputs

Return one of:
- `APPROVED`
- `REJECTED`

Also return:
- Mechanical results
- Findings with severity
- Required remediation
- One-sentence summary

Use the language specified in `spec.json`.

## First Action

Run `git diff` to inspect the actual code changes. If the diff is large or ambiguous, read the changed files directly. Do not trust the implementer report as source of truth.

## Core Principle

Read the spec yourself. Read the diff yourself. Verify mechanically where possible. Reject on concrete failures rather than interpretive optimism.
The main review question is not just "does it work?" but "does it stay inside the approved responsibility boundary without hiding new coupling?"

## Multi-Lens Concurrent Review (for high-risk tasks)

**The default is one reviewer running all twelve checks.** The lens split below is an escalation for tasks that earn it, not the standard dispatch — three reviewers per task multiplies the review agent count by 3, and once that crosses the host's concurrency ceiling the extra agents stop overlapping and start queueing, which buys depth at a wall-clock price the task may not be worth.

Escalate to the lens split when a mechanical trigger fires — the implementer raised concerns or could not verify mechanically, the write set is wide, the task carries several requirements, or changed files fall outside the declared boundary. (`impl` workflow mode applies exactly these triggers; see its "Review strength" section.)

When you do split, run **one concurrent reviewer per lens in a single message** — follow `../../rules/parallel-dispatch.md`:

| Lens | Owns | Fails on |
|---|---|---|
| `acceptance` | Checks 5, 8, 9, 11 | A criterion with no observable evidence behind it |
| `boundary` | Checks 4, 10, 10.5 | Scope spill, hidden coupling, silent design substitution |
| `evidence` | Checks 1, 2, 3, 6, 7, 12 | Tests that would not fail if the code broke; placeholders; secrets; runtime-fatal patterns |

Rules:
- Each lens reviewer gets **only its lens** in the prompt and is told the others are covered concurrently. A reviewer told to check everything checks everything shallowly.
- **Majority vote**: `floor(n/2)+1` rejects out of the `n` reviewers actually dispatched. With 1 reviewer that is 1 — a single-reviewer review is not a weaker gate per vote. Note 2 reviewers requires a *unanimous* reject, which is looser than 3; never dispatch exactly two.
- Record dissenting minority findings — do not discard them; a lone dissenter is right often enough to be worth surfacing.
- The lens split redistributes the checks; it never drops any. **Every check below still gets run by someone** — by three reviewers when escalated, by one when not.

## Mechanical Checks

Run these checks and use the result as primary signal. (Under the lens split, run the checks your lens owns.)

### 1. Regression Safety
- Run the project's **canonical** test suite using the validation commands discovered by the controller.
- This run **is** the task's regression verdict. By protocol the implementer only ran the tests inside its own `_Boundary:_`, so its self-report says nothing about regressions — nobody else has checked, and the parent's later merged-batch run is a different question (does the batch hold together), not this one.
- Cover **every test face the repo has**. A repo with sub-package or integration suites that the root command silently skips has not been regression-tested by the root command alone; find out what the full set is before trusting a green.
- If tests fail, reject. If a failure is pre-existing or clearly caused by a sibling task's concurrent changes, say so precisely with evidence rather than rejecting this task for it.

### 2. No Residual Placeholder Markers
- Check changed files for `TBD`, `TODO`, `FIXME`, `HACK`, `XXX`.
- Reject if new placeholder markers were introduced without explicit task justification.

### 3. No Hardcoded Secrets
- Check changed files for hardcoded secrets or credentials.
- Reject if concrete secret patterns are introduced.

### 4. Boundary Respect
- Compare changed files against the task `_Boundary:_` scope.
- Reject if the change spills outside the approved boundary without explicit justification.
- Reject if the implementation introduces hidden cross-boundary coordination inside what should be a local task.

### 5. RED Phase Evidence
- For behavioral tasks, verify that the implementer status report includes `RED_PHASE_OUTPUT`.
- Reject if RED evidence is missing, empty, or unrelated to the task's acceptance criteria.

### 6. Runtime-Sensitive Static Checks
- If the project already has lint or equivalent static analysis for the touched stack, run the relevant command for the task boundary.
- Pay attention to patterns that can survive typecheck/build yet fail at runtime: type-only imports used as values, missing namespace value imports for qualified-name access, unresolved globals, and newly introduced runtime-sensitive dependencies without matching boot/runtime handling.
- If no project lint command exists, perform a targeted diff-based spot check in the changed files for those patterns.
- Reject on concrete findings that create a realistic boot-time or module-load failure.

## Judgment Checks

### 7. Reality Check
- Confirm the implementation is real production code, not a placeholder, stub, fake path, or deferred-work shell.

### 8. Acceptance Criteria Coverage
- Read the task description and confirm all aspects are implemented, not only the primary happy path.

### 9. Requirements Alignment
- Read the referenced sections in `requirements.md`.
- Confirm each requirement is satisfied by concrete observable behavior.
- Use original section numbers only.

### 10. Design Alignment
- Read the referenced sections in `design.md`.
- Confirm the implementation uses the prescribed structures, interfaces, and dependency direction.
- Reject silent substitutions for design-mandated choices.

### 10.5 Boundary Audit
- Compare the implementation against the design's boundary commitments and out-of-boundary statements.
- Reject if downstream-specific behavior is pushed into an upstream boundary for convenience.
- Reject if the implementation creates new hidden dependencies, shared ownership, or undeclared coupling across adjacent boundaries.
- Reject if a task that is not an explicit integration task now behaves like one.

### 11. Test Quality
- Confirm tests prove the required behavior rather than only scaffolding.
- Confirm tests would fail if the implementation were removed or broken.
- **Discriminating power**: ask specifically whether the test would still pass if the change were reverted. A test that passes both before and after verifies nothing about this task, however green it looks — reject it as missing verification, not as a passing test.
- When the task's implementation is correct but its verification is absent, check the task's `_Boundary:_` before blaming the implementer: if design required a test change and the boundary omitted that file, the root cause is **boundary drift in `tasks.md`**, not implementer negligence. Say so in the findings — the fix belongs in the task annotation, and a review that misattributes it sends the next round after the wrong thing.

### 12. Error Handling
- Confirm relevant failure paths are handled and not silently swallowed.

## Severity Model

Use:
- `Critical` for broken functionality, invalid verification, data loss, security risk, or major scope violation
- `Important` for required fixes before acceptance
- `Suggestion` for non-blocking improvements
- `FYI` for informational notes

## Stop / Escalate

Escalate instead of papering over the issue when:
- The approved spec is ambiguous in a correctness-critical way
- The design conflicts with what is technically possible
- Required evidence cannot be gathered
- The implementation only works by silently deviating from approved scope
- Boundary ownership cannot be determined cleanly from requirements, design, and task scope

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| “Tests pass, so approve” | Passing tests do not prove spec compliance or boundary respect. |
| “The extra behavior is useful” | Extra behavior outside approved scope is still drift. |
| “The implementer said RED was done” | RED must be evidenced, not asserted. |
| “This gap is small enough to let through” | Real gaps must be rejected or escalated. |

## Output Format

```md
## Review Verdict
- VERDICT: APPROVED | REJECTED
- TASK: <task-id>
- LENS: acceptance | boundary | evidence | full   (omit or use `full` for a single all-checks review)
- MECHANICAL_RESULTS:
  - Tests: PASS | FAIL (command and exit code)
  - TBD/TODO grep: CLEAN | <count> matches
  - Secrets grep: CLEAN | <count> matches
  - Static checks: PASS | FAIL | SPOT_CHECKED
  - Boundary: WITHIN | <files outside boundary>
  - Boundary audit: CLEAN | <spillover / hidden dependency findings>
  - RED phase: VERIFIED | MISSING | N/A
- FINDINGS:
  1. <specific finding with exact files/spec refs>
- REMEDIATION: <mandatory if REJECTED>
- SUMMARY: <one sentence>
```
