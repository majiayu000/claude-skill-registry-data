---
name: context-injection
description: How delivery leads use hero relevant output to equip specialist agents with relevant conventions, past work, decisions, and known risks.
compatibility: opencode
metadata:
  audience: delivery-leads
  purpose: context-injection
---
## What I do

Teach delivery leads how to generate context blocks with the `hero relevant` command and incorporate them into engineer instructions before delegating work. Context injection is how agents avoid repeating past mistakes, violating conventions, and contradicting architectural decisions.

## When to use me

Load this skill before the delivery phase of any spec — after the spec is written and before delegating to an engineer or specialist agent. If `hero.json` has `auto_context: true`, the workflow handles this automatically, but delivery leads should still understand the output to intervene when needed.

## What context injection is

Context injection bridges the gap between "here's what to build" (the spec) and "here's what you need to know about this codebase" (the context). Without it, an agent writes code in isolation — unaware of conventions, past decisions, and known failure modes in the areas it's touching.

The `hero relevant` command queries the spec corpus index and returns a structured block of relevant information. The delivery lead pastes this block into the engineer's instructions alongside the spec.

## Running hero relevant

### From a spec path

```
hero relevant .hero/planning/features/add-csv-export/spec.md
```

This parses the spec's Changes section, extracts file paths mentioned in it, and looks up context for those files. This is the most common usage — you have a spec and want context for the work it describes.

### From explicit file paths

```
hero relevant --files src/api/users.ts src/db/queries/users.sql
```

Use this when you know the files that will be touched but don't have a spec, or when the spec's Changes section doesn't mention specific files yet.

### Output format

The command returns a markdown block with up to four sections:

```
## Context for this work

### Conventions to follow
- **api-response-format** (scope: src/api/**/*.ts): All API error responses
  use the ApiError class and return { error, code, details }.
- **sql-migration-naming** (scope: **/migrations/*.sql): Migration files
  use the format YYYYMMDDHHMMSS_description.sql.

### API surface (when relevant)
If the spec touches API handler files, run `hero_code endpoints` to get the
endpoint-to-handler mapping. Include this when work involves routing,
middleware, or request/response changes so the engineer knows the full
API surface around the files being modified.

### Past work in this area
- **add-user-search** (completed): Added full-text search to the users
  endpoint. Introduced the SearchQuery type in src/api/types.ts.

### Decisions that apply
- **use-postgres-fts** (accepted): Use PostgreSQL full-text search rather
  than Elasticsearch for search features under 1M documents.

### Known risks
- **login-timeout-race** (bug, completed): Race condition in session
  handling when concurrent requests hit src/api/auth.ts. Fixed by
  adding mutex on session write.
```

Each entry is a summary — enough to inform the agent without overwhelming it. The agent can look up the full spec if it needs more detail.

## Interpreting the sections

### Conventions to follow

These are active convention specs whose scope globs match the files being touched. The agent must follow these unless the spec explicitly says otherwise.

If a convention is listed, the agent should:
- Read the convention's full spec if the summary isn't enough
- Follow the pattern described in the convention
- Flag any case where following the convention conflicts with the spec's requirements

### Past work in this area

Completed specs that previously touched the same files. This tells the agent what was done before, why, and what patterns were established. It prevents the agent from undoing previous work or introducing inconsistencies.

Use past work to:
- Understand the design rationale for existing code
- Identify patterns the agent should continue following
- Spot potential conflicts between the current spec and prior changes

### Decisions that apply

Accepted architectural decision records (ADRs). These are constraints the agent must respect. An accepted decision means the team deliberately chose this path — the agent should not revisit the decision unless the spec explicitly says to.

### Known risks

Bug specs whose root causes involved the same files. These are landmines — the agent needs to know about them to avoid triggering the same failures.

Use known risks to:
- Add defensive checks in areas with past bugs
- Avoid patterns that previously caused failures
- Include regression tests for known failure modes

## Incorporating context into engineer instructions

When delegating to an engineer agent, structure the handoff as:

1. The spec (what to build)
2. The context block (what to be aware of)
3. Any delivery lead commentary (overrides, priorities, sequencing)

The context block goes between the spec and any additional instructions. This lets the agent read the spec first, then calibrate its approach based on context.

Do not strip sections from the context block to save tokens. The block is already summarized — removing sections creates blind spots. If a section is genuinely irrelevant, you can add a note saying "the X section is not relevant to this task because Y" rather than removing it.

## When to override or ignore context

Context is guidance, not law. Override it when:

- **The spec intentionally changes a convention.** If the work is to migrate from one pattern to another, the old convention should not constrain the new work. Add a note: "Convention X is being superseded by this work — do not follow it for new code."
- **A past decision is being revisited.** If the spec explicitly reconsiders an accepted decision, note this and explain why the decision no longer applies.
- **Past work context is stale.** If the referenced past spec is old enough that the code has changed significantly since, note this so the agent verifies current state rather than relying on the summary.

Never silently ignore context. If you're overriding something, say so and explain why. This creates a trail that future context lookups can surface.

## Handling conflicting context

When context sections contradict each other or the spec:

- **Convention vs. spec requirement**: The spec wins. Add a note that the convention needs updating after this work lands, or that this is an intentional exception.
- **Past decision vs. new requirement**: Escalate. If the spec didn't explicitly address the conflict, pause delivery and raise the conflict to the spec author. The decision may need to be superseded with a new decision spec.
- **Two conventions conflict**: This is a convention-authoring bug. Flag it. One convention should be updated to exclude the overlapping scope, or the two should be consolidated.
- **Past work vs. known risk**: Both inform the agent. Past work shows what was done; known risks show what went wrong. They don't conflict — the agent should use both to inform its approach.

## Quality check

Before handing off to the engineer, verify:
- The context block was generated from the correct file paths (not stale or wrong paths)
- No convention listed has been superseded since the last index rebuild
- Any overrides are explicitly noted with rationale
- The combined spec + context is not so large that it will exceed the agent's effective context window
