---
name: architecture-decision
description: "Compare architecture alternatives and create or update an ADR for Clean Architecture, Vertical Slices, Modular Monolith, microservices, or The Standard."
---

# Architecture decision
- Read existing code and ADRs, define the real forcing function: deployment autonomy, consistency, business complexity, team ownership, reliability, scale or compliance.
- Propose a smallest viable option, one credible alternative and a 'do nothing now' option if relevant.
- Compare operating cost, boundary enforcement, testability, migration cost, developer onboarding and rollback.
- Distinguish logical CQRS from MediatR/messaging/separate stores; don't auto-add frameworks.
- If proposing microservices, prove independent deployment/scale/ownership and plan for latency, failure, event contracts, tracing and idempotency.
- If proposing The Standard, use Brokers/Services/Exposers consciously as organizing architecture; don't duplicate an existing slice/application hierarchy.
- Sketch one real use-case call chain, one failure scenario and the changes required for a new feature.
- Create ADR using `templates/ADR.md` if implementation has repository access; require approval for migration/disruptive refactors.
- Output tradeoffs and explicit signals that would prompt revisiting the choice.
