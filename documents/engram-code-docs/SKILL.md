---
name: engram-code-docs
description: Document and review engram code surfaces. Use when adding or changing Rust crates, TypeScript packages, public traits, generated bindings, SDK APIs, adapter ports, examples, or code comments that explain domain behavior.
---

# Engram Code Docs

Use this skill whenever code changes affect public APIs, behavior traits,
adapter boundaries, examples, or generated bindings. Documentation should make
the contract and extension points clear without repeating every field already
specified in `docs/domain-data-model.md`.

## Required Context

Read these before documenting public code:

- `docs/domain-data-model.md` for domain semantics.
- `AGENTS.md` for repo boundaries and validation commands.
- `references/documentation-standards.md` for review rules.

## Workflow

1. Identify the public surface: Rust crates, traits, structs intended for SDK
   use, TypeScript exports, examples, and adapter ports.
2. Add module docs explaining why the module exists and where behavior belongs.
3. Add doc comments for public traits, public functions, adapter contracts, and
   non-obvious invariants.
4. Keep field-level docs focused on ambiguity, policy, compatibility, or
   security. Do not restate obvious names.
5. Link back to contract concepts by name rather than copying long sections from
   `docs/domain-data-model.md`.
6. Run `.codex/hooks/check-code-docs.sh` before handoff.

## Output

Report:

- Public surfaces documented or reviewed.
- Any intentionally undocumented generated or internal code.
- Validation commands run.
