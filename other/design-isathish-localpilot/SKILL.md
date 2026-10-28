---
name: design
description: Produce a technical design before building — architecture, module/file layout, data model, API surface, key decisions with trade-offs, and an ordered implementation plan. USE WHEN the user asks "how should we build this", "architecture", "design doc", "data model", "plan the implementation", or a feature touches more than ~3 files or introduces a new dependency/service.
---

# Design

Goal: decide *how* before touching code, in a document short enough to read in two minutes, then turn it into a checklist the agent can execute.

## 1. Learn the codebase first
- Map the project: `list_dir` the root and main source folders; read the package manifest, README and the entry point.
- Find the conventions you must follow: how modules are organised, naming, error handling, testing framework, state management, how config/env is read. Use `grep_search` for the patterns (e.g. an existing service/route/component) and read one good example end to end.
- Locate everything the change touches with `find_symbol` / `find_references` so the design lists real file paths.
- Reuse before you add: check for an existing utility, dependency or pattern before proposing a new one.

## 2. Decide
For each significant choice write the options considered and why one wins. Typical decisions: where the logic lives, data model / schema changes, API shape (REST/GraphQL/RPC, request/response types, errors), state & caching, background work, auth/permissions, migration & backward compatibility, observability.

Prefer: the smallest change that fits existing patterns · boring, well-supported libraries already in the lockfile · pure functions with thin I/O edges · explicit types at boundaries · feature flags for risky rollouts.

## 3. Write the design doc
`docs/design/<feature-slug>.md` (or the repo's existing docs folder), ~60–150 lines:

```markdown
# <Feature> — design
Links: requirements → `docs/requirements/<slug>.md`

## Summary
One paragraph: what we build and the shape of the solution.

## Architecture
Text or a mermaid diagram of components and data flow. Name the real modules/files.

## File / module changes
| Path | Change | Notes |
|------|--------|-------|
| src/… | new | … |

## Data model
Types / tables / schemas, with migration notes.

## API / interfaces
Signatures, routes, events, CLI flags — exact names.

## Decisions & trade-offs
- D1: <choice> — because … Alternatives: … Rejected because …

## Risks & mitigations
## Testing strategy
Unit / integration / e2e: what each layer proves.
## Rollout
Flags, migrations order, monitoring, rollback.
```

## 4. Turn it into a plan
- Call `manage_todos` with ordered, independently verifiable steps (each step = one commit-sized change, ending with "verify: build/tests/diagnostics").
- Front-load the risky or unknown parts (spikes) so surprises surface early.
- Open the design doc for the user with `show_markdown`, then summarise in chat: the chosen approach in 3–5 bullets, the file list, and the first step. Offer to start `implement`.

## Rules
- No speculative abstractions: design for the stated requirements plus the next obvious one, not "someday".
- Every path in the doc must exist or be marked `new`.
- If the user already stated a preference (framework, library, style), follow it and don't relitigate.
