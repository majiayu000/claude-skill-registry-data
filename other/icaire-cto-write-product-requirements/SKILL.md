---
name: icaire-cto-write-product-requirements
description: Turn ICAIRE product ideas into clear requirements for technical delivery. Use when defining users, use cases, user stories, acceptance criteria, non-functional requirements, or release checklists.
---

# ICAIRE CTO: Write Product Requirements

Use this skill to convert an ICAIRE product, platform, or internal tooling idea
into requirements that an engineering team can estimate, build, test, and
release.

## Contract

- Start from the user problem, intended users, operating context, and release
  decision the requirements need to support.
- Use BigBrain or the ICAIRE MCP connector for ICAIRE initiatives, stakeholders,
  systems, constraints, and prior decisions when the user has not supplied
  enough source material.
- Write requirements as testable behavior, not vague aspirations.
- Separate functional requirements from non-functional requirements, data needs,
  integrations, security requirements, assumptions, and open questions.
- Include acceptance criteria and release checks that make delivery quality
  verifiable.

## Workflow

1. Identify the product idea, users, goals, workflow, platform surface, deadline,
   and expected implementation team.
2. Gather source material and retrieve current ICAIRE context if the affected
   initiative, stakeholder, system, or constraint is unclear.
3. Define the users, use cases, user journeys, and success outcomes.
4. Write user stories or requirement statements with clear acceptance criteria.
5. Add non-functional requirements covering security, privacy, performance,
   reliability, accessibility, maintainability, analytics, and support where
   relevant.
6. Identify data models, integrations, permissions, administrative controls,
   migration needs, and operational handoff requirements.
7. Produce a release checklist and list unresolved decisions or missing source
   material.

## Guardrails

- Do not invent users, constraints, data classifications, integrations, or
  approvals.
- Do not collapse security and privacy into generic "secure by design" wording;
  make concrete review needs visible.
- Do not write implementation code or architecture unless the user asks for it.
- Do not present open questions as settled requirements.
- Do not update durable memory unless the user explicitly asks for ingestion or
  persistence.

## Output Expectations

Return requirements in a delivery-ready structure. When useful, include:

- product goal
- users and use cases
- user stories or functional requirements
- acceptance criteria
- non-functional requirements
- data, integration, and permission needs
- risks, assumptions, and open questions
- out-of-scope items
- release checklist
