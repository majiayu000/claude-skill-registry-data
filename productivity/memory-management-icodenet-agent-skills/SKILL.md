---
name: memory-management
description: >-
  Resolves project shorthand, acronyms, nicknames, and internal names using
  durable memory and docs. Use when the goal contains unexplained acronyms,
  nicknames, or team jargon that must be decoded before planning. Do not use for
  general research synthesis (use synthesize-research).
---

# Memory Management

Decode shorthand so plans use the team's real names and constraints.

## Workflow

1. **Extract terms** — acronyms, nicknames, ticket IDs, service aliases from the goal.
2. **Resolve** — check project memory notes, `AGENTS.md` / `CLAUDE.md`, domain glossaries (`CONTEXT.md`), ADRs, and recent docs. See `references/resolution-order.md`.
3. **Disambiguate** — if a term maps to multiple meanings, state candidates and pick with evidence (or ask only if blocked).
4. **Normalize** — rewrite the goal/plan using canonical names.
5. **Capture (optional)** — if a stable new alias was confirmed, propose a one-line memory entry for the user to keep — do not invent long-lived memory without confirmation when project rules require it.

## Constraints

- Prefer written project sources over model prior knowledge for internal names.
- Do not invent expansions for unknown acronyms; mark `[UNKNOWN: term]` and continue with unblocked work.
- Keep memory entries short and factual.

## Verification

- [ ] All critical shorthand resolved or marked unknown
- [ ] Plan uses canonical names
- [ ] Sources cited for non-obvious expansions
