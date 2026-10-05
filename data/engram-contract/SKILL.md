---
name: engram-contract
description: Maintain Engram contract and domain-model integrity. Use when editing docs/domain-data-model.md, contracts/schemas/*.json, ADRs/RFCs that affect public data shapes, Rust/TypeScript type generation, compatibility rules, or contract-freeze decisions.
---

# Engram Contract

Use this skill whenever work could change the portable domain contract. The goal is to keep Engram contract-first: storage, APIs, Rust types, TypeScript bindings, and generated schemas must derive from the accepted domain model instead of drifting into separate interpretations.

## Required Context

Read these files before changing contract-affecting behavior:

- `docs/domain-data-model.md`
- `contracts/v1/**/*.md`
- `contracts/v1/**/*.json`
- `docs/specs/*.md`
- `docs/architecture.md`
- `docs/adr/*.md` when the change touches architecture policy
- `docs/rfcs/*.md` when the change touches scope or extension points
- `references/contract-checklist.md`

## Workflow

1. Identify whether the change is pre-acceptance, compatible post-acceptance, or breaking.
2. Keep domain language storage-neutral. Do not add SQL, vector-store, Node.js, or Rust-specific concepts to the portable contract.
3. Preserve opaque identifiers. Do not encode tenant, storage location, timestamps, or authorization semantics in IDs.
4. Check that every durable record has scope, provenance, timestamps, and policy implications where applicable.
5. Update JSON schemas only when they intentionally track the domain model.
6. Keep accepted v1 examples valid against accepted v1 schemas.
7. Document deferred compatibility questions in `docs/domain-data-model.md` rather than hiding them in code comments.
8. Run `.codex/hooks/check-contracts.sh` before handoff.

## Output

When reporting contract work, include:

- The contract surface changed.
- Whether the change is compatible or breaking.
- Any schema or generated-type follow-up required.
- Validation commands run and their result.
