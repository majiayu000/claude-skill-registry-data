---
name: linting
description: "Linting: enforce repo config; distinguish defects from style preference in review."
---

# linting

Lint gates defects, not taste: repo config rules, defects block, preferences don't.

## Activate when

- Adding lint config, interpreting findings, or reviewing lint-related review comments.

## Do NOT activate for

- Formatting (see formatting); type errors (see type-checking).

## Inspection

Read the repo lint config first (which rules, which severity, what's suppressed and why). Never invent rules the repo doesn't have.

## Decision rules

- Defect-class findings (bugs, security, correctness, dead code) block; style findings follow the repo config silently.
- In review, distinguish "rule violation" from "personal preference" — only the first is a defect.
- Suppressions (`eslint-disable`, `# noqa`, `//nolint`) require a reason comment and narrowest scope; blanket file suppressions are defects.
- New rules need team agreement + autofix path where possible; warning-only rules that never gate are noise — promote or delete.

## Procedure

1. Run the repo linter before pushing; fix defect-class first.
2. Justify each suppression inline; remove stale ones opportunistically.
3. Verify: lint gate green, no new suppressions without reasons, review comments cite rule names not taste.

## Failure modes

- Personal-preference review wars; warn-only gates nobody reads; suppression without reason; lint config copied from another project unexamined.

## Escalation

Security-relevant findings → security/secure-baseline; systemic cleanup → core/refactoring.

## References

- Related: `../formatting/`, `../../core/code-review/`.
