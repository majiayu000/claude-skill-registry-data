---
name: code-iterate
description: Iteratively find and fix issues until no new actionable findings remain.
---

Run a convergent fix loop: find issues, fix them, repeat until clean.

## Mode Selection

- **Default** (no skill specified): Perform review and cleanup iterations using the `code-review` and `code-cleanup` skills.
- **Specific**: If a skill or instruction is specified, follow that target instead.

## Process

### Step 1 - Identify Scope

- Inspect changed files with `jj diff -s`, or restrict scope with `jj diff -- path`.
- Focus on any user-specified paths.
- Create a fresh empty commit with `jj new` as the safety baseline.
- Read the `code-check` skill, detect test/lint commands, and run a baseline check.

### Step 2 - Iteration Loop

#### 1. Find issues

- If a specific skill is provided, apply its lenses; otherwise apply the `code-review` and `code-cleanup` lenses.

#### 2. Filter findings

- **Deduplicate**: Drop issues already addressed or deferred in a prior iteration.
- **Classify**: critical/high (must fix), medium (should fix), low/speculative (defer).
- **Exit**: If no new actionable findings remain, exit the loop.

#### 3. Fix

Apply a worker lens to fix {findings list} in {files}:

- Read files before editing; keep diffs minimal, idiomatic, and behavior-preserving.
- Verify with the narrowest meaningful command.
- Apply minimal targeted changes; do not refactor beyond what resolves each finding.
- If a fix fails twice, stop and report.

#### 4. Verify

- Run the most specific applicable test/lint commands with timeouts.
- If regressions appear, apply the worker lens from the Fix subsection above to resolve them.

#### 5. Commit

- Create an ephemeral commit named `"Iteration <n>: <desc>"` for later user review and squashing.

### Step 3 - Production Audit

- If production readiness is requested, apply an auditor lens to audit {files} for production readiness:
  - Correctness, security, data loss, migration hazards, rollback safety, and contract compatibility.
  - Flag only material risk; this is a final gate, not an iterative style review.

### Step 4 - Verification

- Run comprehensive project checks (test, lint, format).
- Confirm the diff against the safety baseline is coherent with no unintended changes.

### Step 5 - Report

- **Scope**: Target files and mode of operation.
- **Iterations**: Total iterations run, with a brief findings summary (found, fixed, deferred) per pass.
- **Final Verification**: Results of the final checks.
- **Convergence Status**: Reason the loop stopped (clean run, max iterations, or progress stalled).
- **Auditor Findings**: Production audit results (if requested).
- **Remaining Items**: Deferred findings needing manual review or product decisions.

## Convergence Rules

Stop the iteration loop when:

- **No actionable findings**: All remaining issues are deferred or speculative.
- **No changes**: An iteration pass makes no modifications to the code.
- **Limit reached**: The maximum iteration count is reached (default is 5, unless overridden by the user).
- **Divergence**: The list of findings grows rather than shrinks, indicating a potential issue with the fixes.

## Guardrails

- Preserve public behavior, API signatures, and test outcomes.
- Each iteration must yield fewer or equal new findings than the previous pass.
- Apply strictly targeted fixes; no broad refactoring.
- Do not address issues outside the defined target scope.
- Do not chain-invoke other skills as black boxes; read `code-review` and `code-cleanup` and apply their lenses. Only `code-check` may be read for command detection.
