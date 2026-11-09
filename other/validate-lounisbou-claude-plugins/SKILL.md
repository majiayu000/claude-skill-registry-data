---
name: validate
description: |
  Use before running norms:check to validate CONTRIBUTING.md structure. Detects contradictory rules,
  empty entries, vague non-enforceable statements, and missing scope definitions that would cause
  agents to produce unreliable findings.
---

# Validate Norms

## Overview

Validates `CONTRIBUTING.md` structure before norm-checking agents use it. Catches problems that cause agents to produce contradictory, false-positive, or unenforceable findings.

**Core principle:** A norm that agents can't enforce consistently is worse than no norm — it generates noise that drowns real issues.

## When to Use

- Before running `/norms:check` on a project for the first time
- After editing `CONTRIBUTING.md`
- When norms agents produce contradictory or noisy findings

## Validation Checks

Run ALL checks against `CONTRIBUTING.md`. Each check produces PASS, WARNING, or ERROR.

When this prompt ends with a `<norms-validate-scan>` block, the plugin has already run the lexical part of checks 2, 3, 5 and 6 with exact line numbers. Report those findings as given, and spend your own reading on checks 1 and 4 and on rules buried in prose (check 6).

### Check 1: Contradictions

Search for rules within the same section that conflict:

- "always X" vs "but also Y" where X and Y are mutually exclusive
- "use tabs" / "use spaces" in the same section
- "always try/catch" / "let errors propagate"

**Detection:** Look for "but also", "actually", "however", "except" within a section — these signal informal amendments that may contradict earlier rules.

```
ERROR: Contradiction in [section]
- Rule A: "<text>"
- Rule B: "<text>"
- Why: These are mutually exclusive. Agents cannot enforce both.
- Fix: Pick one authoritative rule and remove or scope the other.
```

### Check 2: Empty or Incomplete Rules

Search for:

- Empty bullet points (`- ` with no text)
- Rules with only whitespace
- Sections with headers but no rules

```
ERROR: Empty rule in [section]
- Line: <line number>
- Fix: Add the intended rule text or remove the empty entry.
```

### Check 3: Vague / Non-Enforceable Rules

Flag rules containing subjective qualifiers that agents cannot check:

- "properly", "clearly", "cleanly", "well", "good", "appropriate"
- "when needed", "as necessary", "where possible"
- "or whatever", "etc.", "and so on"

```
WARNING: Non-enforceable rule in [section]
- Rule: "<text>"
- Problem: Contains "<qualifier>" — agents cannot measure this.
- Fix: Replace with a concrete, measurable criterion.
  Example: "handle errors properly" -> "wrap external API calls in try/catch and log the error with context"
```

### Check 4: Missing Scope

Flag rules that apply to specific contexts but don't define boundaries:

- "use camelCase" — for what? Variables? Functions? Classes? All?
- "validate inputs" — which inputs? User input? API input? Internal?

```
WARNING: Missing scope in [section]
- Rule: "<text>"
- Problem: Does not specify where it applies.
- Fix: Add explicit scope. Example: "use camelCase for local variables and function parameters"
```

### Check 5: No Examples

Check if ANY rule in the file includes a concrete code example (good or bad). Rules with examples are dramatically easier for agents to enforce.

```
WARNING: No examples found
- Impact: Agents must infer intent — enforcement will be inconsistent.
- Fix: Add at least one good/bad example per section.
```

### Check 6: Structural Issues

- Missing `#` header for top-level sections
- Inconsistent list markers (mixing `-` and `*`)
- Rules buried in prose paragraphs (agents expect bullet lists)

```
WARNING: Structural issue
- Location: <line or section>
- Problem: <description>
- Fix: <suggestion>
```

## Output Format

```markdown
# Norms Validation Report

## Summary

| Check          | Status    | Count   |
| -------------- | --------- | ------- |
| Contradictions | PASS/FAIL | N found |
| Empty rules    | PASS/FAIL | N found |
| Vague rules    | PASS/FAIL | N found |
| Missing scope  | PASS/FAIL | N found |
| No examples    | PASS/FAIL | -       |
| Structural     | PASS/FAIL | N found |

## Verdict: PASS / NEEDS FIXES

<If NEEDS FIXES: list each issue with the format above>
<If PASS: "CONTRIBUTING.md is ready for agent enforcement.">
```

## Quick Reference

| Smell         | Signal Words                      | Severity |
| ------------- | --------------------------------- | -------- |
| Contradiction | "but also", "actually", "however" | ERROR    |
| Empty rule    | blank bullet `- `                 | ERROR    |
| Vague         | "properly", "clearly", "whatever" | WARNING  |
| No scope      | applies broadly, no qualifier     | WARNING  |
| No examples   | zero code blocks in file          | WARNING  |
| Bad structure | prose instead of lists            | WARNING  |

## Common Mistakes

| Mistake                        | Impact                                    | Fix                                                 |
| ------------------------------ | ----------------------------------------- | --------------------------------------------------- |
| Treating all findings as ERROR | Overwhelms user                           | Only contradictions and empty rules are ERROR       |
| Suggesting rewrites            | Not your job — just flag                  | Flag the problem, suggest direction, let user write |
| Skipping Check 1               | Contradictions cause worst agent behavior | Always check first                                  |
| Validating code style          | This validates CONTRIBUTING.md, not code         | Stay focused on document structure                  |
