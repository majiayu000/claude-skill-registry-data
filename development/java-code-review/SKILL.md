---
name: java-code-review
description: >
  Review Java code for bugs, duplicate code, correctness risks, maintainability
  improvements, and missing tests. By default review files modified in git;
  when the user explicitly names files, classes, packages, or a diff, review
  that scope instead. Generate a detailed review.md report with actionable
  comments and fixes.
---

# Java Code Review

Perform a focused, evidence-based review of Java code and write the findings to
`review.md` in the repository root unless the user specifies another location.
This skill reviews code; do not modify production code unless the user
explicitly asks for fixes.

## Establish the review scope

1. If the user explicitly specifies files, classes, packages, commits, or a
   diff, use that scope and do not silently broaden it.
2. Otherwise inspect the git worktree and review modified, added, or renamed
   files. Use `git status --short` and the relevant `git diff` (including
   staged changes when present). For renamed files, review the resulting file
   and the meaningful diff.
3. Include only Java and Java-adjacent files relevant to behavior (for
   example, tests, SQL migrations, configuration, or API schemas) when they
   affect the reviewed Java code. State the selected scope in the report.
4. Read enough surrounding code, callers, tests, configuration, and interfaces
   to validate each finding. Do not report a concern based only on a name or
   a generic best practice.

## Review for

- **Potential bugs:** incorrect conditions, null/empty handling, state or
  transaction errors, exception handling, resource leaks, concurrency issues,
  security or authorization gaps, API/serialization mismatches, persistence
  mistakes, and boundary cases.
- **Duplicate code:** repeated logic, copy-pasted branches, duplicated
  mappings/validation, and abstractions that would reduce meaningful drift.
- **Needs improvement:** unclear or brittle design, excessive coupling,
  misleading names, avoidable complexity, test gaps, performance concerns,
  and violations of established project conventions.

Prioritize correctness and impact over style. Do not flag formatting or an
opinionated alternative unless it creates a concrete maintenance, reliability,
security, or performance problem. Distinguish confirmed issues from risks or
questions, and avoid speculative findings.

## Validate findings

For every finding, trace the relevant control flow and data flow. Check nearby
tests and, when practical, run the narrowest useful test, compile, static
analysis, or reproduction command. Do not change files to make validation pass.
If validation cannot be run, say why. Check whether a suspected issue is
already handled by a caller, framework contract, annotation, or configuration.

## Write `review.md`

Before writing, check whether the requested output file already exists.

- If it exists, ask the user whether to overwrite it or use a new filename;
  do not overwrite without that choice.
- If the user chooses a new filename, use exactly that filename (within the
  repository or requested output location).
- If no report exists, create `review.md`.

The report must be self-contained and include:

```markdown
# Java Code Review

## Scope
<!-- files/diff reviewed, review date, and validation performed -->

## Summary
<!-- concise overall assessment and finding counts by severity -->

## Findings

### [SEVERITY] Short title
- **Location:** `path/to/File.java:line`
- **Category:** Bug | Duplicate code | Improvement
- **Confidence:** High | Medium | Low

**Problem**
Explain the concrete behavior and why it matters, citing the relevant code.

**Suggested fix**
Give a specific implementation approach, including edge cases and tests to
add or update. Do not merely say “refactor” or “add validation.”

## Positive observations
<!-- optional; mention useful safeguards or clear design choices -->

## Validation
<!-- commands run and their outcomes, or why validation was unavailable -->
```

Use severity consistently: **Blocker** (unsafe or clearly broken), **High**
(likely production failure or serious security/data issue), **Medium**
(meaningful bug or maintainability risk), and **Low** (minor but actionable).
Order findings by severity, then by file and line. Include one finding per
distinct problem, avoid duplicates, and use precise line references that still
make sense in the reviewed version. If no findings are found, say so clearly
and still include scope, validation, and positive observations.

## Final response

Tell the user that the report was created and link to the generated file. Give
the finding count and briefly call out any Blocker or High findings. If the
report could not be created because an existing file needs a choice, ask the
overwrite/new-filename question and stop before writing.
