---
name: create-prd-claude-code
description: Write a PRD optimized for AI coding agents (Claude Code, Codex). Includes standard product context plus implementation-specific sections -- file structure, code patterns, API contracts with request/response examples, test cases, migration steps, and sequenced build order. The output is designed so an AI coding tool can build directly from it. Use when an AI coding agent will implement the spec.
---

# Create PRD (AI Coding Agent)

Generate a PRD formatted as an executable build plan for AI coding agents like Claude Code or Codex. This format combines the standard product context (problem, goals, metrics) with implementation-specific sections that an AI coding tool needs to build the feature with minimal back-and-forth.

The key difference from a standard PRD: every section is written to be machine-actionable. Instead of "we need an API endpoint," this format says "create a POST endpoint at `/api/v1/notifications/preferences` that accepts this request body and returns this response."

## When to Use

- You are handing a feature to Claude Code, Codex, or another AI coding agent to build
- You want a spec detailed enough that the AI can start coding without asking clarifying questions
- You need to bridge the gap between product intent and implementation detail in a single document
- You are a PM who works directly with AI coding tools and wants to give them the best possible instructions

## When NOT to Use

- The audience is humans, not AI agents -- use `create-prd` (standard) or `create-prd-engineering`
- You need a concise document for leadership approval -- use `create-prd-one-pager`
- The feature is still in discovery and the solution is not defined enough for implementation detail

## Inputs

Ask the user for:

1. **Feature name** -- What are we building?
2. **Problem statement** -- What user problem does this solve?
3. **Goals and success metrics** -- What does success look like?
4. **Solution description** -- What is the proposed solution? (Must be specific enough to implement.)
5. **Codebase context** -- What repo, language, framework, and key patterns should the AI follow?
6. **Existing code references** -- Key files, modules, or patterns the new code should match
7. **API contracts** -- Endpoints, request/response shapes, error codes (if applicable)
8. **Test expectations** -- What should be tested? What are the expected outcomes?
9. **Constraints** -- Performance requirements, backwards compatibility, migration needs

If the user provides partial input, fill in what you can and mark implementation-critical gaps with `[BLOCKED -- need X before coding]` rather than silent `[TBD]`.

## Outputs

A complete PRD + implementation plan in markdown, following the template in `references/template.md`. The document includes:

- Product context (problem, goals, metrics) -- for the AI to understand intent
- Implementation context (repo, stack, patterns) -- for the AI to match existing code
- File structure -- what files to create or modify
- API contracts with request/response examples -- exact shapes, not descriptions
- Data model changes -- schema additions or modifications
- Build sequence -- ordered steps the AI should follow
- Test cases with expected outcomes -- what to test and what "pass" looks like
- Migration and rollback -- how to deploy safely

## Steps

1. **Gather product context** -- Ask for problem, goals, and success metrics. This grounds the AI in "why" so it makes better implementation decisions.
2. **Map the codebase** -- Ask what repo, language, and framework. If the user provides a repo path, scan it for patterns (directory structure, naming conventions, test framework).
3. **Define the file plan** -- List every file that will be created or modified. For modified files, note what changes.
4. **Write API contracts** -- For each endpoint or interface, write the exact request/response shape as code blocks. Include error cases.
5. **Describe data model changes** -- Schema changes, new tables/columns, migration scripts needed.
6. **Sequence the build** -- Order the implementation steps so the AI can work top-to-bottom without circular dependencies. Earlier steps should not depend on later ones.
7. **Write test cases** -- For each major behavior, write a test case with input, expected output, and the assertion. Include edge cases.
8. **Plan migration and rollback** -- If the feature requires data migration or has deployment risk, document the steps.
9. **Add guardrails** -- Note any patterns the AI should follow, anti-patterns to avoid, and things that must NOT change.
10. **Review with the user** -- Walk through the spec. The key question: "Could an AI coding agent build this feature from this document alone?"

## Example Usage

**User:** "I need a PRD for Claude Code to build a notification preferences API. Users should be able to set per-channel preferences (email, Slack, in-app) for each notification type."

**Agent:** Asks about the codebase (repo, framework, ORM), existing notification system code, database schema, and auth patterns. Then produces a PRD with exact endpoint specs, database migration SQL, file paths to create, test cases, and a step-by-step build order.

**User:** "Write a spec for Codex to add SAML SSO to our Express.js app. Here's the repo: ~/code/auth-service."

**Agent:** Scans the repo for existing auth patterns, middleware structure, and test framework. Produces a PRD that references existing files, matches the code style, and sequences the build so Codex can work through it in order.

## Guardrails

- **Be explicit, not descriptive.** "Create a REST endpoint" is not enough. "Create a POST endpoint at `/api/v1/foo` that accepts `{ bar: string, baz: number }` and returns `{ id: string, created_at: string }`" is what the AI needs.
- **Match existing patterns.** The AI should not introduce new patterns when the codebase already has established conventions. Reference specific existing files as examples.
- **Sequence matters.** If step 3 depends on step 1, say so. AI agents work best when they can go top-to-bottom without backtracking.
- **Test cases are not optional.** Every behavior should have a test case. The AI needs to know what "done" looks like.
- **Mark blockers loudly.** Use `[BLOCKED]` for anything the AI cannot proceed without. Silent `[TBD]` in an AI-targeted spec leads to hallucinated implementations.
- **Do not over-specify style.** Specify structure and behavior, not formatting preferences. Let the AI match the existing codebase style.

## Related Skills

- `create-prd` -- Standard PRD for human audiences
- `create-prd-engineering` -- Detailed engineering spec (for humans, not AI agents)
- `create-prd-one-pager` -- Leadership one-pager
- `create-architecture-diagram` -- Visualize the system before specifying the build
