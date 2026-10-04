---
name: zoom-out
description: Produces a read-only system map for an unfamiliar code area before changes begin. Use when the user needs broader context, module relationships, caller/callee flow, domain language, ADR constraints, or test surface understanding without editing code.
---

# Zoom Out

Map an unfamiliar code area before changing it.

This skill is read-only. Do not refactor, edit files, create docs, or start implementation while using it.

## Read First

Inspect project context:

- `docs/agents/domain.md`
- `CONTEXT.md`
- relevant ADRs under `docs/adr/`
- `docs/agents/test-commands.md`
- files or modules named by the user
- callers, callees, tests, routes, commands, or API surfaces around the target area

Use fast search when possible:

```powershell
rg --files
rg "<symbol-or-term>"
```

Keep Windows paths with spaces quoted when showing file locations.

## When To Use

Use when:

- the user says they do not know an area,
- a bug or feature touches unfamiliar code,
- implementation risk comes from unclear module relationships,
- a repo has many small files and no obvious entry point,
- the next skill needs orientation before acting.

Do not use this for confirmed implementation tasks unless orientation is still missing.

## Workflow

### 1. Define The Focus

Identify the area to map:

- file,
- folder,
- module,
- route,
- command,
- API endpoint,
- domain term,
- failing test,
- user-visible behavior.

If the focus is too broad, narrow it to the smallest useful area and state the assumption.

### 2. Find Entry Points

Look for how the area is reached:

- public exports,
- route handlers,
- CLI commands,
- UI screens,
- scheduled jobs,
- tests,
- integration points.

List the main entry points before diving into internals.

### 3. Map Callers And Callees

Trace:

- who calls this code,
- what this code calls,
- data flowing in,
- data flowing out,
- side effects,
- error paths,
- state transitions.

Keep the map high signal. Do not list every helper unless it changes understanding.

### 4. Connect Domain Language

Use repo vocabulary.

Report:

- domain terms involved,
- ambiguous terms,
- terms used differently in code and docs,
- missing terms that may need `grill-with-docs`.

Do not invent certainty. Mark uncertainty clearly.

### 5. Check Decisions And Tests

Look for:

- ADRs constraining the area,
- tests covering the behavior,
- test gaps,
- setup docs with verification commands,
- similar patterns elsewhere in the repo.

If no tests are found, say that directly.

### 6. Produce The Map

Use this structure:

```md
## System Map

Focus:
Entry points:
Main flow:
Important modules:
Data/state flow:
Side effects:
Domain terms:
ADR constraints:
Tests and verification:
Uncertainties:
Recommended next step:
```

See `references/module-context-template.md` for a reusable shape.

## Next Step Selection

Recommend one next skill:

- `grill-with-docs` if product/domain decisions are unclear.
- `diagnose` if there is a reproduced or suspected bug.
- `tdd` if behavior is clear and implementation can start.
- `improve-codebase-architecture` if the map shows structural friction.

Do not start the next skill automatically unless the user asked you to proceed.

## Safety Rules

- Do not edit files.
- Do not create docs.
- Do not run destructive git or filesystem commands.
- Do not make refactor changes.
- Do not hide uncertainty.
- Do not rely on file names alone when code references can be checked.

## Verification

Before finishing:

- State which files, docs, and tests were inspected.
- State the main entry points and dependencies.
- State uncertainties or missing context.
- State the recommended next skill and why.

Use `references/code-map-checklist.md` to make sure the map is complete enough.
