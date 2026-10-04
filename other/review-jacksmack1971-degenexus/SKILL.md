---
name: review
description: Conduct a DegenExus five-axis code review with contract-driven specialist routing and schema-checkable evidence.
disable-model-invocation: true
argument-hint: "[diff, file, PR, or scope]"
---

# Review Workflow

Use `code-reviewer` for baseline correctness, readability, architecture, security, and performance review. Add specialists from `.claude/rules/synergy-contract.yml` when the changed files match a risk surface.

## Required Inputs

- Current diff or explicit scope.
- `.claude/rules/synergy-contract.yml` for routing.
- `.claude/rules/evidence-schema.yml` for output fields.
- `.claude/rules/02-agent-synergy.md` for human-readable routing context.

## Review Rules

1. Read tests first, then implementation, then docs/config.
2. Categorize findings as Critical, Important, or Suggestion.
3. Cite file/line evidence and concrete remediation.
4. Explain every applicable specialist invoked or skipped.
5. Include at least three edge cases, with one prompt-injection/security edge when relevant.
6. Emit the minimum gate fields from `.claude/rules/evidence-schema.yml`.
