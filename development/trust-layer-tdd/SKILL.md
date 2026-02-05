---
name: trust_layer_tdd
description: Enforce test-first changes and debug based on failing tests.
metadata:
  short-description: Trust layer (TDD)
---

## Purpose
Require proof of correctness for changes.

## Steps
1. Create tests before editing behavior.
2. Use failures to trigger the debug protocol.
3. Iterate until tests are green.

## Guardrails
- Reject new code without passing tests.
