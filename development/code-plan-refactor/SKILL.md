---
name: code-plan-refactor
description: Create safe targeted refactoring plans. Use when asked to plan simplification, cleanup, extraction, renaming, deletion, or module movement without applying changes. For small in-place fixes, use `code-cleanup` instead.
---

Generate a safe refactoring plan only; do not apply code changes.

## Process

### Step 1 - Identify Context

- Inspect changed files with `jj diff -s`; restrict with `jj diff -- path`.
- Focus on user-specified files, paths, abstractions, or pain points.
- Clarify the desired outcome and non-goals.

### Step 2 - Research and Scout

Apply a scout lens to analyze affected code areas, call sites, tests, abstractions, dependency edges, and local conventions for {task}:

- Map relevant files, conventions, and call paths; cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs; stay read-only and task-relevant.

- For cross-module refactors, apply an architect lens to analyze module boundaries, ownership, dependency direction, and structural invariants for {task}:
  - Map current boundaries, ownership, and dependency direction first.
  - Recommend the smallest architecture that preserves invariants.
  - Avoid speculative generality.

Apply a planner lens to design a minimal behavior-preserving refactoring plan for {task}, including ordering, stop points, alternatives, and tradeoffs:

- Prefer simple, boring solutions; preserve existing project patterns.
- Make tradeoffs and assumptions explicit; scope to the current problem.

Apply a reviewer lens to review the proposed refactor for correctness, behavior preservation, simplicity, and project-convention risks:

- Ground findings in file paths and line numbers; prioritize the requested lens.
- Distinguish confirmed findings from speculative risks; explain why each issue matters.

### Step 3 - Adjudicate Decisions

- For high-impact or conflicting design decisions, apply an oracle lens to adjudicate the conflicting refactoring recommendations for {task}:
  - Identify the decision; state assumptions and constraints.
  - Pick the smallest safe path that preserves future options.
  - State an explicit confidence level (high/medium/low) for the adjudication and its key assumptions.
  - Note what evidence would change the recommendation.

### Step 4 - Audit

- For production-bound refactors, apply an auditor lens to audit the refactoring plan for {task} for production risks:
  - Data loss, migration hazards, rollback safety, contract compatibility, and correctness/security risk.
  - Flag only material risk; this is a final gate, not iterative style review.

### Step 5 - Validate Findings

- Read relevant code yourself and validate findings.

### Step 6 - Design Refactor

- Identify safe transformations (extraction, rename, simplification, deletion, inlining, module movement).
- Simplify design: prefer deleting or inlining code over adding new layers; ensure every abstraction earns its complexity.
- When deciding whether to split or combine modules, read the `john-ousterhout-software-design` reference and apply its "better together OR better apart" and deep-modules / information-hiding principles; do not split into shallow modules or leak information across boundaries.
- When choosing refactorings, read the `martin-fowler-code-smells` reference and match each smell to its primary fix; treat smells as heuristics, not hard violations, and skip what tooling already enforces.
- Break the work into small, behavior-preserving steps with verification after each.
- Identify where characterization tests are required before refactoring starts.
- Do not apply any code changes.

### Step 7 - Report

Provide a structured report with:

1. **Context Analysis** — relevant code structure, patterns, call sites, dependency edges, behavior-preservation constraints.
2. **Risk Analysis** — risky transformations and mitigation strategies; tests/checks needed before changes.
3. **Simplicity Constraint**:
   - Deletion, inlining, or no-code alternatives.
   - Over-engineering risks.
   - Minimal viable scope.
4. **Refactoring Plan**:
   - Numbered, concrete steps with target files.
   - Verification procedures per step.
   - Rollback or stop points.

Prioritize actionable, specific guidance over abstract advice.
