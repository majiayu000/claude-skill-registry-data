---
name: explore
description: Adversarially explore a request before formalizing work. Retrieve repository, memory, and external prior art; use Context7 for explicitly required technologies; expose conflicts, edge cases, user actions, decisions, and gaps.
---

# Explore

Turn an idea or problem into a trustworthy recommendation. Do not implement or create a formal change until the request is coherent enough to specify.

## Stages

1. Frame intent, outcome, constraints, and explicitly required technologies.
2. Retrieve internal prior art from active and archived changes, repository code/docs/tests, and relevant project memories. Treat memories as context and revalidate them against current state.
3. When a new library, framework, language, API, or specific function is explicitly required, consult Context7 for version-relevant documentation. Use broader web research when Context7 lacks coverage or ecosystem evidence is needed.
4. Inspect current callers, consumers, contracts, integrations, configuration, and tests.
5. Run an adversarial pass: try to disprove the approach by checking conflicts, edge cases, security, permissions, failure states, concurrency, migrations, compatibility, accessibility, performance, observability, and testability.
6. Identify user-only actions, external approvals, credentials, provisioning, irreversible choices, and unresolved decisions. Resolve them now or split dependent work.
7. Compare alternatives and recommend one with explicit trade-offs.
8. Produce a durable exploration record and route to feature authoring or stop with the recommendation.

## Output

Record intent, internal prior art, memory context, Context7 findings, external evidence, current state, adversarial findings, user actions/decisions, alternatives, recommendation, open questions, proposed scope, and verification concerns.

Never treat an old memory, search result, or worker claim as proof without current evidence.
