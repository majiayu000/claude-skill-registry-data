---
name: account-recovery
description: Guidance and guardrails for secure account recovery workflows including identity verification and password reset.
license: Educational sample
allowed-tools:
  - reset_password
metadata:
  security_level: high
  id_verification: 2-step
---

# Account Recovery Skill

Follow strict identity verification before any password operations. Provide user-friendly guidance and avoid sensitive data exposure. Document actions succinctly.

## Decision Hints

- If user mentions '잠김/locked' → advise on unlock or reset
- Always provide post-action next steps
