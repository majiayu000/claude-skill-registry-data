---
name: multi-agent-review
description: Multi-agent review orchestration dispatching parallel specialist reviewers with line-level evidence collection.
---

# Multi-Agent Review Skill

## Review Lanes
- **Reviewer A (Correctness):** Logic defects, state leaks, unhandled exceptions, race conditions.
- **Reviewer B (Security):** Auth, secrets, injection, privilege escalation, OWASP Top 10.
- **Reviewer C (Architecture):** Separation of concerns, modularity, dependency boundaries.
- **Reviewer D (Adversarial):** Hostile payload tracing, edge cases, bypassed validations.
- **Reviewer E (Tests):** Test coverage, boundary value analysis, regression protection.
