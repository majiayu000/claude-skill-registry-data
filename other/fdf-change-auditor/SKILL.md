---
name: fdf-change-auditor
description: Audit implementation changes for correctness and reliability. Use when validating provided diffs or ranges and producing evidence-backed findings before closure.
---

# FDF Change Auditor

Audit changed code with high precision and low noise.

## Contract

1. Follow the active Verify-phase rules from the conductor-selected rule matrix.
2. Prefer high-confidence findings; label assumptions and uncertainty explicitly.

## Audit Scope

1. Audit the provided diff or range.
2. If no diff/range is provided, follow active Verify-phase rule policy for default scope.

## Process

1. Verify behavior correctness.
2. Inspect edge cases and failure behavior.
3. Inspect quality dimensions required by active Verify-phase rules.
4. Suggest the minimal safe remediation set.
