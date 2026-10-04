---
name: architecture-review
description: Review a change for architectural drift, guardrail weakening, and ADR impact before shipping.
---

# Architecture Review

This is a repo-specific review checklist for architectural conformance.

## Focus Areas

1. Cross-layer boundaries
   - Are imports still limited to `shared` and explicit service seams?
   - Did any direct cross-layer model import appear?

2. Guardrail integrity
   - Were `.github/workflows/**`, `.pre-commit-config.yaml`, `.claude/**`, `AGENTS.md`, or `scripts/adr_guard/**` changed?
   - If yes, were matching docs updated?
   - Did the change weaken enforcement, broaden skips, or make rules easier to bypass?

3. ADR impact
   - Does the change implement an existing ADR?
   - Does it change the meaning of an existing ADR?
   - Does it need a new ADR or a temporary exception?

4. Shared/public seams
   - Were `shared/**` or `*/services.py` changed?
   - If yes, did tests and docs move with them?

## Commands

```bash
python3 scripts/adr_guard/adr_guard.py --changed --level fast
python3 scripts/adr_guard/adr_guard.py --all --level ci
```

## Findings Format

For each issue, provide:

- severity
- file
- violated rule or drift risk
- why it matters
- exact fix

If no issues are found, say:

`Architecture review: no ADR or guardrail issues found.`
