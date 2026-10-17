---
name: before-after-diff-summary
description: Converts a noisy Git diff, patch, pull request, commit range, or set of changed files into a human-readable summary of before-and-after behavior. Use when the user asks what changed, wants release-note or reviewer-friendly change explanations, or needs mechanical edits separated from functional, API, data, configuration, test, documentation, and operational changes.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: code-review
  task_type: review
  audience: developers-and-code-reviewers
  tags:
    - git-diff
    - code-review
    - behavior-change
    - pull-request
    - change-summary
  status: draft
  side_effects: none
---

# Before/After Diff Summary

## Purpose

Translate implementation-heavy changes into a concise explanation of observable behavior before and after the diff, while separating confirmed changes from likely implications and non-behavioral churn.

## When to use this skill

Use this skill when:

- The user asks what a diff, patch, commit, branch, or pull request actually changes.
- A large diff contains formatting, generated files, renames, or refactors that obscure the meaningful changes.
- Reviewers, maintainers, QA, or release-note authors need a behavior-oriented summary.
- The user wants changes grouped by capability or user flow instead of by file.

Do not use this skill when:

- The user wants a defect-focused code review with severity-ranked findings.
- The user asks to implement, revert, or repair the changes.
- Only a commit title or author-written description is available and no changed code, patch, or equivalent evidence can be inspected.
- The task requires a full security, accessibility, performance, or architecture audit.

## Inputs to inspect

- The supplied diff, patch, commit range, staged changes, working-tree changes, or pull-request diff.
- Changed source, configuration, schema, migration, dependency, test, documentation, and fixture files needed to understand context.
- Call sites, public exports, routes, commands, events, storage formats, and feature flags touched by the change.
- Tests that establish old or new behavior.
- Rename, binary, generated-file, and lockfile metadata.

## Workflow

1. Establish the comparison boundary. State the base and target when known, and note whether the evidence is a full diff or a partial excerpt.
2. Inventory the changes by purpose, not file order. Group related edits into behavior units such as one user flow, API contract, data lifecycle, configuration path, or operational process.
3. Filter noise. Mark formatting, import sorting, generated output, lockfile churn, comments, pure renames, and behavior-preserving refactors as non-behavioral unless they affect runtime behavior or compatibility.
4. Reconstruct the previous behavior from removed lines and surrounding code. Do not infer the old state from added lines alone.
5. Reconstruct the new behavior from added lines, updated call sites, tests, and configuration. Trace enough context to explain externally observable effects.
6. Write paired statements for each meaningful unit:
   - **Before:** what users, callers, operators, or tests experienced previously.
   - **After:** what they experience now.
   - **Impact:** why the difference matters and who is affected.
7. Classify each unit when useful: user-visible behavior, public API, data or persistence, configuration, error handling, performance, security, accessibility, tests, documentation, tooling, or internal-only refactor.
8. Separate evidence levels:
   - **Confirmed:** directly demonstrated by the diff and surrounding code.
   - **Likely:** a reasonable consequence that is not fully proven by the available evidence.
   - **Unknown:** requires runtime behavior, external configuration, generated artifacts, or missing context.
9. Check for compatibility implications such as changed defaults, removed exports, schema changes, migration requirements, altered error shapes, new permissions, dependency requirements, or rollout conditions.
10. Produce a concise summary ordered by user or system impact. Avoid narrating every hunk or repeating filenames when several files implement one behavior change.

## Output format

Return:

```md
## Summary

One to three sentences describing the overall behavioral change.

## Before and after

| Area | Before | After | Impact |
|---|---|---|---|
| ... | ... | ... | ... |

## Non-behavioral changes

- ...

## Compatibility and rollout notes

- ...

## Uncertainties

- ...
```

Omit empty sections. For a very small diff, use one short before/after paragraph instead of a table. Cite file paths, symbols, tests, or diff sections when they materially support a claim.

## Quality bar

The task is complete only when:

- The summary explains observable outcomes rather than restating code edits.
- Every meaningful claim is supported by the diff or clearly labeled as likely or unknown.
- Related edits are consolidated into cohesive behavior units.
- Non-behavioral churn is separated from functional change.
- Breaking changes, changed defaults, migrations, and rollout requirements are called out when present.
- The result is understandable without requiring the reader to inspect every changed file.

## Edge cases

- For partial or truncated diffs, state that conclusions are limited to the visible changes.
- For pure refactors, say that no intended behavior change is evident and identify the structural change and remaining regression risk.
- For test-only changes, distinguish newly documented behavior from newly implemented behavior.
- For documentation-only changes, do not claim runtime behavior changed unless code or configuration supports it.
- For generated files and lockfiles, summarize the source-level cause when available instead of enumerating generated churn.
- For renames, distinguish identity-preserving moves from changed imports, public paths, routes, or case-sensitive filenames.
- For migrations or feature flags, explain both rollout state and steady-state behavior.
- For binary changes, report the artifact change and avoid guessing at its contents without inspection.

## Related skills

- `project-status-snapshot`
- `repo-next-steps-review`
