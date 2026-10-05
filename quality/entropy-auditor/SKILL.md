---
name: entropy-auditor
description: Audit and reduce AI-generated codebase entropy. Use when a repo needs duplicate logic detection, dead-code checks, oversized file review, inconsistent pattern cleanup, stale TODO review, dependency drift checks, or a technical debt register.
---

# Entropy Auditor

## Purpose

Detect codebase drift that agents tend to amplify: duplicate logic, dead code, oversized files, inconsistent patterns, one-off abstractions, stale TODOs, and dependency sprawl.

## Inspect First

- source tree and module layout
- recent diffs when available
- dependency manifests
- test layout
- existing technical debt docs
- lint/dead-code tools already configured

## Procedure

1. Run cheap scans first.
   - Duplicate names or similar files.
   - Oversized files.
   - Stale TODO/FIXME comments.
   - Unused dependencies where the stack has a tool.
   - Inconsistent patterns across similar modules.

2. Separate findings by severity.
   - P0: correctness, security, data loss.
   - P1: architecture or testing gaps that can cause regressions.
   - P2: maintainability, docs drift, unnecessary dependency.
   - P3: style and low-risk cleanup.

3. Create or update cleanup docs.
   - `docs/quality/technical-debt.md`
   - `docs/quality/golden-patterns.md`
   - Use `golden-pattern-extractor` when preferred examples or reusable templates need deeper extraction.

4. Add automation.
   - Add `scripts/audit-entropy`.
   - Prefer `assets/templates/audit-entropy.sh.tmpl` as the starting point for shell-based audits.
   - Add deterministic checks where signal is high.
   - Avoid noisy checks that train agents to ignore validation.
   - Exclude generated, dependency, and build directories such as `.git`, `node_modules`, `.bun`, `dist`, `build`, `.next`, `.turbo`, `.cache`, `coverage`, and `vendor`.
   - Do not let the audit script report its own TODO/FIXME search strings.
   - Make oversized-file thresholds configurable, with a documented default.
   - Use `agent-reviewer` for diff-level risk review before cleanup PRs are proposed.
   - Include stale handoff, missing feature evidence, weak termination proof, and repeated unpromoted review feedback in the cleanup loop when present.

5. Recommend cleanup PRs.
   - Keep cleanup separate from feature work unless the debt blocks the feature.
   - Prefer small focused cleanup batches.

## Audit Output

Use this structure in docs or final reports:

```markdown
## Findings

- P1: <finding>
  Evidence: <path or command>
  Fix: <specific action>

## Golden Patterns

- <pattern name>: <path to best example>

## Deferred Debt

- <item>, owner/update trigger if known
```

## Validation

- Run `./scripts/audit-entropy`.
- Run changed quality scripts.
- Confirm findings point to real files and actionable fixes.

## Completion Criteria

- The repo has a lightweight debt register.
- Agents have preferred patterns to copy.
- Entropy checks are useful enough to keep in validation.
