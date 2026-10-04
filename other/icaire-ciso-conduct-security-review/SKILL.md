---
name: icaire-ciso-conduct-security-review
description: Review ICAIRE software, vendors, access, data handling, hosting, and deployment risk. Use when producing security risk registers, severity ratings, affected systems, evidence, recommended fixes, or go/no-go notes.
---

# ICAIRE CISO: Conduct Security Review

Use this skill to review security and operational risk for ICAIRE software,
vendors, access models, data handling, hosting, or deployment decisions.

## Contract

- Start from the system, vendor, deployment, access pattern, or data flow under
  review.
- Use BigBrain or the ICAIRE MCP connector for ICAIRE systems, initiatives,
  stakeholders, prior decisions, and operational context when the user has not
  supplied enough source material.
- Identify assets, users, data types, trust boundaries, hosting or vendor
  dependencies, and operational controls before rating risk.
- Rate each risk with a clear severity, evidence, affected system or process,
  recommended fix, owner or review party when known, and go/no-go implication.
- Distinguish confirmed findings from assumptions, missing evidence, and items
  needing legal, procurement, or technical review.

## Workflow

1. Identify the review target, requested decision, deadline, deployment stage,
   and audience for the security review.
2. Gather supplied architecture notes, vendor material, access lists, data flow
   descriptions, policies, logs, or deployment details.
3. Retrieve current ICAIRE context if the affected system, owner, initiative,
   stakeholder, or data sensitivity is unclear.
4. Map assets, data types, users, access paths, integrations, hosting locations,
   third parties, and operational responsibilities.
5. Evaluate risks across access control, identity, data handling, privacy,
   hosting, vendor posture, secrets, logging, monitoring, backup, incident
   response, and deployment controls.
6. Assign severity and recommend practical fixes, mitigations, acceptance
   conditions, or escalation paths.
7. Produce a decision note: approve, approve with conditions, block, or needs
   more evidence.

## Guardrails

- Do not claim formal compliance, legal approval, or audit certification unless
  source evidence explicitly supports it.
- Do not invent vendor controls, hosting regions, security policies, data
  classifications, or access permissions.
- Do not treat missing evidence as low risk; mark it as unknown and state what
  proof is needed.
- Do not bury go/no-go concerns in a long narrative.
- Do not update durable memory unless the user explicitly asks for ingestion or
  persistence.

## Output Expectations

Return a security review artifact. When useful, include:

- review target and scope
- assets, users, data, and trust boundaries
- risk register
- severity ratings
- affected system, process, vendor, or data flow
- evidence and confidence
- recommended fixes or mitigations
- owners or review parties when known
- go/no-go note
- missing evidence and review needs
