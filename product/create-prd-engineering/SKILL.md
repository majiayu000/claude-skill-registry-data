---
name: create-prd-engineering
description: Write a detailed PRD for engineering teams covering functional requirements, technical constraints, data models, API contracts, edge cases, acceptance criteria per story, release stages, and cross-functional tracking. Use when the engineering team needs a comprehensive build spec.
---

# Create PRD (Engineering)

Generate a detailed Product Requirements Document for engineering teams. This is the engineering team's build spec -- it goes deeper than a standard PRD on functional requirements, technical constraints, data models, API contracts, edge cases, and acceptance criteria. Designed to be the document engineers pull stories from and reference during implementation.

## When to Use

- You are writing requirements that engineering will break into stories and build from
- The feature involves data model changes, API contracts, or cross-service integration that need to be specified up front
- You need acceptance criteria per story so QA and engineering agree on "done"
- You want to track release stages (Alpha, Beta, GA) with entrance criteria

## When NOT to Use

- You need a cross-functional overview for mixed audiences -- use `create-prd` (standard)
- You are handing this to an AI coding agent to build -- use `create-prd-claude-code`
- You need a concise one-pager for leadership -- use `create-prd-one-pager`
- The feature is still in early discovery and requirements are not stable enough for this level of detail

## Inputs

Ask the user for:

1. **Feature name** -- What are we building?
2. **Problem statement** -- What problem does this solve? Include user impact and business impact.
3. **Goals and success metrics** -- What does success look like? Include baselines if available.
4. **Functional requirements** -- What must the system do? Be specific about behaviors, not just capabilities.
5. **Technical context** -- What systems, services, or data stores are involved? Any known constraints?
6. **Design references** -- Wireframes, mockups, or design specs (if available)
7. **Dependencies** -- Other teams, services, or features this depends on
8. **Release plan** -- What stages (Alpha, Beta, GA) and what are the criteria to advance?

If the user provides a design doc or markdown spec, read it for context.

## Outputs

A comprehensive engineering PRD in markdown, following the template in `references/template.md`. The document includes:

- Metadata and stakeholders
- Problem statement with user and business impact
- Goals, non-goals, and success metrics with baselines
- Functional requirements organized by area
- Technical constraints and architecture notes
- Data model changes
- API contracts
- Edge cases and error handling
- User stories with acceptance criteria
- Release stage plan with entrance criteria
- Cross-functional tracking (design, docs, support, analytics)
- Risks and open questions

## Steps

1. **Gather context** -- Ask for the inputs above. If a design doc or markdown spec exists, read it.
2. **Write the problem statement** -- Cover both user pain and business impact. Engineers build better when they understand why something matters.
3. **Define functional requirements** -- Organize by feature area. Each requirement should describe a behavior: "When X happens, the system does Y." Avoid vague requirements like "the system should be fast."
4. **Document technical constraints** -- Performance targets, backwards compatibility, security requirements, rate limits, data retention policies. Be specific.
5. **Specify data model changes** -- New tables, modified schemas, indexes, foreign keys. If migrations are needed, note them.
6. **Write API contracts** -- Endpoints, methods, request/response schemas, error codes. Include enough detail that a developer can implement without guessing.
7. **Map edge cases** -- What happens when input is invalid? When a dependency is down? When rate limits are hit? When the user has no data? Cover the unhappy paths.
8. **Write user stories with acceptance criteria** -- Each story should be independently deliverable. Acceptance criteria use Given/When/Then format and cover both happy and unhappy paths.
9. **Plan release stages** -- Map the work to Alpha, Beta, and GA with clear entrance criteria for each stage.
10. **Track cross-functional needs** -- Does design need to deliver mocks? Does documentation need updating? Does support need runbooks? Track each dependency.
11. **Review with the user** -- Walk through the spec. Key question for engineering review: "Can you break this into sprint stories and start building?"

## Example Usage

**User:** "I need an engineering PRD for adding webhook support to our platform. Teams should be able to register webhook URLs and receive event notifications."

**Agent:** Asks about the event system architecture, expected event types, delivery guarantees, retry logic, and auth model. Produces a full engineering PRD with data model for webhook registrations, API contracts for CRUD + delivery, edge cases for failed deliveries, and acceptance criteria.

**User:** "Write an engineering PRD for migrating from REST to GraphQL for our dashboard API. Here's the design doc: docs/graphql-migration.md."

**Agent:** Reads the design doc, maps the existing REST endpoints, and produces a PRD with the GraphQL schema, migration plan per endpoint, backwards compatibility approach, and release stages.

## Guardrails

- **Requirements are behaviors, not wishes.** "The system should be performant" is not a requirement. "P95 latency for the search endpoint must be under 200ms for queries returning fewer than 100 results" is.
- **Every story needs acceptance criteria.** If you cannot write Given/When/Then for a story, the story is not defined.
- **Edge cases are not optional.** The unhappy paths are where most bugs live. Cover invalid input, missing data, service failures, and concurrency.
- **Do not design the architecture.** Describe constraints and requirements. Let engineering design the solution. If you have opinions, put them in a "Suggested Approach" section clearly marked as non-binding.
- **Track cross-functional dependencies explicitly.** A PRD that assumes design will deliver mocks "when they are ready" without a tracked commitment is a PRD that will slip.
- **Mark unknowns.** Use `[TBD -- owner: Name, target: Date]` so unknowns are visible and trackable.

## Related Skills

- `create-prd` -- Standard PRD for cross-functional audiences
- `create-prd-claude-code` -- PRD optimized for AI coding agents
- `create-prd-one-pager` -- Leadership one-pager
- `create-architecture-diagram` -- Visualize the system architecture
- `decision-brief` -- When a technical decision needs stakeholder approval
