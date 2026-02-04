---
name: verification-harness
description: Validate outputs using rule-based checks (required strings, regex, length, ranges). Use when you need deterministic verification or regression checks.
---

# Verification Harness

Use this skill to validate outputs with deterministic checks.

## Workflow

1) Define a ruleset (use references/ruleset.example.json).
2) Run the verifier against a file or stdin.
3) Review the report and address failing checks.

## Scripts

- Run: python scripts/verify_output.py --input output.txt --rules references/ruleset.example.json
