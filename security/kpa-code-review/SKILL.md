---
name: kpa-code-review
description: Review uncommitted changes for correctness, regressions, security, spec mismatches, and missing tests
context: fork
agent: Sonnet
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Review the current **uncommitted** changes and report actionable findings.

## Scope

- Review all staged, unstaged, and untracked changes in the working tree.
- Focus on correctness, regressions, security, spec mismatches, and missing tests.
- Do **not** implement fixes; only report issues.

## OpenSpec Alignment (required)

1. Identify related OpenSpec change artifacts:
   - First check active changes in `openspec/changes/` (exclude `openspec/changes/archive/`).
   - Prefer changes that are also modified in the current diff.
   - If none are modified, infer likely related changes from touched feature areas/files.
2. For each related change, review:
   - `proposal.md`
   - `design.md` (if present)
   - `tasks.md` (if present)
   - delta specs in `openspec/changes/<change>/specs/**/spec.md`
3. If no active related change exists, fall back to relevant baseline specs in `openspec/specs/**/spec.md`.

## Review Process

1. Inspect the uncommitted diff (`git status`, staged + unstaged diffs, and untracked files).
2. Map changed code to expected behavior from OpenSpec docs.
3. Report only concrete issues with clear evidence.
4. Call out missing or weak test coverage for changed behavior.

## Output Format

- Start with findings ordered by severity: **Critical**, **High**, **Medium**, **Low**.
- For each finding include:
  - **Severity**
  - **Location** (file path and line or symbol)
  - **Spec Reference** (OpenSpec file/requirement/scenario when applicable)
  - **Issue**
  - **Why it matters**
  - **Recommended fix**
- If no issues are found, explicitly say: `No significant issues found in uncommitted changes.`
