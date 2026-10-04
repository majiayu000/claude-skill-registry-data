---
name: to-prd
description: Converts an existing conversation, clarified plan, or feature idea into a local-first PRD draft. Use when the user wants a PRD, product spec, requirements document, or durable feature plan before issue slicing or implementation.
---

# To PRD

Turn the current context into a product requirements document that can drive issues, prototypes, tests, and implementation.

Do not start a new interview by default. Synthesize what is already known, then ask only for critical missing product decisions.

## Read First

Gather context from:

- current conversation,
- clarified plan from `grill-with-docs` if present,
- `docs/agents/domain.md`,
- `CONTEXT.md`,
- relevant ADRs under `docs/adr/`,
- existing plans, specs, and README files,
- relevant code only when needed to avoid stale assumptions.

If setup docs exist, read:

- `docs/agents/issue-tracker.md`
- `docs/agents/test-commands.md`

## Output Location

Default to a local markdown PRD.

Recommended locations, in order:

1. `docs/agents/prds/<slug>.md`
2. `docs/prds/<slug>.md`
3. `docs/<slug>-prd.md`

If the repo already has a PRD convention, use it.

Before writing any file:

- propose the target path,
- summarize what will be written,
- ask for approval.

GitHub or remote issue publishing is optional and requires explicit user request.

## Workflow

### 1. Identify Source Material

State what input the PRD is based on.

Examples:

- conversation context,
- clarified plan,
- existing issue,
- design note,
- prototype finding,
- repo docs.

If the source is too thin, ask the smallest question that unlocks the PRD.

### 2. Synthesize Product Intent

Write a short internal summary before drafting:

- problem,
- target users or actors,
- desired outcome,
- core behavior,
- constraints,
- known non-goals.

Use domain language from repo docs.

### 3. Check Implementation Reality

Do a light repo check when implementation assumptions matter.

Look for:

- existing modules or routes,
- similar features,
- test locations,
- API or CLI surfaces,
- constraints from ADRs.

Do not turn the PRD into a file-by-file implementation plan. Keep code paths out unless they are essential context.

### 4. Ask Only Critical Questions

Ask when a missing answer would make the PRD misleading.

Good reasons to ask:

- user impact is unclear,
- success criteria conflict,
- scope boundary is ambiguous,
- release gate cannot be defined,
- technical constraint changes the product promise.

Avoid asking for details that can be inferred from docs or code.

### 5. Draft PRD

Use this structure:

```md
# <Feature Name> PRD

## Problem Statement

## Goals

## Non-goals

## User Stories

## Requirements

## Technical Approach

## Risks

## Acceptance Criteria

## Verification Notes

## Release Gate
```

See `references/prd-template.md` for section prompts.

### 6. Include Implementability

The PRD should help future implementation without becoming brittle.

Include:

- likely surfaces or modules at a high level,
- test strategy direction,
- migration or compatibility concerns,
- data or API contract implications,
- constraints from ADRs,
- local verification commands if known.

Avoid:

- stale exact file paths unless necessary,
- private implementation details,
- code snippets unless they encode a durable decision,
- remote publish assumptions.

### 7. Review Quality

Check the draft against `references/prd-quality-checklist.md`.

Look for:

- clear problem,
- bounded goals,
- explicit non-goals,
- testable acceptance criteria,
- release gate,
- risks and unknowns,
- no hidden implementation scope.

### 8. Write After Approval

After user approval, create or update only the approved PRD path.

If the file exists:

- read it first,
- preserve existing content,
- ask before replacing or restructuring.

## Safety Rules

- Do not publish to GitHub or any remote tracker unless explicitly asked.
- Do not overwrite existing PRDs without approval.
- Do not make destructive git or filesystem suggestions.
- Keep local markdown as the default output.
- Keep Windows paths quoted when showing commands.

## Verification

Before finishing:

- List the PRD path written or proposed.
- State source material used.
- Confirm the PRD has all required sections.
- List open questions or assumptions.
- Recommend next step: usually `to-issues`, `prototype`, or `tdd`.
