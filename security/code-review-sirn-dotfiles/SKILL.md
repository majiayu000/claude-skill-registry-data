---
name: code-review
description: Review code for correctness, quality, conventions, simplicity, security, and overall health. Use when asked for a general or full code review.
---

Run a full code review or quality check by applying specialized lenses.

## Process

### Step 1 - Identify Context

- Run `jj diff -s` to list changed files; use `jj diff -- path` to inspect specific paths.
- Focus on user-specified files or paths when provided.
- Identify the spec source: issue references in commit messages (`#123`, `Closes #45`), PRD/spec files under `docs/`, `specs/`, or `.scratch/`, a user-supplied path, or ask the user. If none is found, skip the spec review axis and note it in the final report.
- Identify standards sources: anything documenting how code should be written (`CONTRIBUTING.md`, `CODING_STANDARDS.md`, `docs/CONTRIBUTING.md`, linter configs encoding conventions) and use these when applying a reviewer lens.

### Step 2 - Apply Review Lenses

Apply a reviewer lens to review {files}:

- Ground findings in file paths and line numbers, prioritize the requested lens, distinguish confirmed findings from speculative risks, and explain why each issue matters.

Review across these axes:

- **correctness/quality** — bugs, logic errors, edge cases, error handling, resource leaks, concurrency, performance traps.
- **security** — OWASP risks, injection flaws, auth/authz, cryptography, sensitive data exposure, dependency risks, secure defaults.
- **convention/simplicity** — assess using the 24 Fowler code smells; read the `martin-fowler-code-smells` reference and apply each relevant smell's fix (smells are heuristics, never hard violations).

Binding Rules:

- **The repo overrides**: a documented repo standard (from {standards_sources}) always wins; where it endorses something `martin-fowler-code-smells` would flag, suppress the smell.
- **Always a judgment call**: each smell is a labeled heuristic, never a hard violation. Skip anything tooling already enforces.

Cite the specific source (file and rule) for any violation of identified repo standards {standards_sources}.

- If a spec is identified, apply a researcher lens to compare {files} against {spec_source}:
  - Prefer official documentation over blog posts; cite sources with URLs.
  - Separate confirmed facts from plausible interpretations; note version requirements.
  - Lead with the single most actionable recommendation.
  - Check for: missing or partially implemented requirements; behavior in the diff not requested by the spec (scope creep); requirements that look implemented but are incorrect.
  - Quote the relevant spec line for each finding.

- For API verification, apply a researcher lens to verify relevant API/library usage in {files} against official documentation and research relevant best practices:
  - Prefer official documentation over blog posts; cite sources with URLs.
  - Separate confirmed facts from plausible interpretations; note version requirements.
  - Lead with the single most actionable recommendation.
  - Cross-check usage against idiomatic patterns and known pitfalls for the API/library.

### Step 3 - Audit

- For production-bound changes, apply an auditor lens to audit {files} for production readiness:
  - Correctness, security, data loss, migration hazards, rollback safety, and contract compatibility.
  - Flag only material risk; this is a final gate, not an iterative style review.

### Step 4 - Synthesize Findings

- Read relevant code yourself to validate and synthesize findings.
- Keep Spec review and Code Quality review on strictly separate axes; never merge or rerank them. A perfectly written implementation of the wrong feature must remain visible as a spec failure.
- Distinguish hard violations of documented standards from judgment calls on baseline code smells.

### Step 5 - Run Verification

Run verification commands only when the user requested full checks:

- Detect test, lint, check, and format commands from project instructions, task runners (`Makefile`, `justfile`, `Taskfile.yml`), wrapper scripts (`bin/`, `.my/bin/`), package manager scripts, or common defaults.
- Run appropriate non-destructive commands with timeouts.
- Report failures; modify files only if explicitly requested.

### Step 6 - Report

#### Axis A: Specification Compliance

_(Skip or note if no spec source was found. Keep strictly separate from code quality.)_

1. **Requirements Gap** — quoted spec lines for missing or partially implemented requirements.
2. **Scope Creep** — behaviors in the diff not requested by the spec.
3. **Incorrect Logic** — quoted spec lines where the code attempts a requirement but does so incorrectly.

#### Axis B: Code Quality Review

1. **Executive Summary**
2. **Critical Issues** (must fix)
3. **Security Analysis**
4. **API / Documentation Verification**
5. **Quality & Logic**
6. **Simplicity & Convention**
   - **Hard Violations**: documented repo standard breaches (cite specific file and rule).
   - **Judgement Calls**: the 24 Fowler code smells from `martin-fowler-code-smells` (heuristics/suggestions, never hard violations; skip if tooling already enforces).
7. **Performance & Best Practices**
8. **Test/Lint Results** (only when run)
9. **Quick Wins**
10. **Action Items** prioritized Critical > High > Medium > Low

Prioritize real, evidenced issues over speculative concerns. Include file paths, line references, or quoted snippets, and provide concrete fixes with verification steps.
