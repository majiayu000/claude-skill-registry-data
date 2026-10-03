---
name: contract-guard
description: >-
  Guard external contracts before changing them. Use BEFORE modifying anything
  consumed outside the current codebase or by clients you do not control:
  public/exported APIs, REST/GraphQL endpoints and their request/response
  shapes, published package entry points, database schemas read by other
  services, event/message payloads, webhooks, or generated client types. Also
  use when reviewing a diff that touches such surfaces. Prevents silently
  shipping breaking changes to external consumers.
---

# Contract Guard

External consumers cannot be refactored by you. Any interface they depend on is a **contract**: change it deliberately and compatibly, or version it — never silently.

## When this applies

Trigger this skill before editing (or when reviewing edits to):

- Exported symbols of a published package or shared library
- HTTP/GraphQL/gRPC endpoints: paths, methods, params, request/response shapes, status codes, error formats
- Database schemas other services or reports read
- Event, queue, or webhook payloads
- OpenAPI/GraphQL/protobuf schema files and generated clients
- File formats or CLI output that downstream tooling parses

If the change only touches code whose callers all live in this repo and are updated in the same change, this skill does not apply — refactor freely.

## Workflow

### 1. Inventory the contract surface

Before editing, establish who consumes the thing you're about to change:

- Search the repo for callers; check whether the symbol/endpoint is exported, published, or documented publicly.
- Look for contract artifacts: OpenAPI/GraphQL schemas, protobuf files, generated client packages, versioned API docs, consumer contract tests (e.g. Pact).
- Ask: "can every consumer be updated in this same change?" If **no** (external clients, mobile apps with old versions, other teams, published packages) → the surface is guarded.

State the finding explicitly: `Contract surface: <what> — consumers: <who/unknown>`.

### 2. Classify the intended change

Use `references/breaking-change-taxonomy.md` for the full table. Summary:

- **Compatible (safe):** adding optional fields, adding new endpoints/methods, widening accepted input, adding enum *handling*, new optional params with defaults.
- **Breaking:** removing/renaming anything; changing a field's type or nullability; adding a required input; narrowing accepted values; changing error shapes, status codes, sort order, pagination, or semantics callers rely on; changing serialization defaults.
- **Ambiguous:** behavior changes that were arguably bugs — treat as *potentially breaking*, flag for human decision.

### 3. Breaking → stop and choose a compatibility strategy

Never apply a breaking change in place. Options, in order of preference:

1. **Expand–migrate–contract**: add the new field/endpoint/column alongside the old, migrate consumers, remove the old one later (separately).
2. **Version the surface**: `/v2` endpoint, new event version, semver **major** bump for packages.
3. **Deprecate with a window**: mark deprecated, keep serving, document the removal date.
4. **Negotiate**: if consumers are known and coordinated, an agreed synchronized change — recorded, not assumed.

If none is possible in scope, **do not make the change** — report the conflict and the recommended strategy instead.

### 4. Verify with contract evidence

Claims of compatibility need proof, not inspection:

- Run existing contract tests (Pact, schema validation) — add one when the surface has none and you're touching it.
- Diff schema artifacts old-vs-new (e.g. `oasdiff` for OpenAPI, `buf breaking` for protobuf, migration dry-run for SQL) when tooling exists.
- Compile/type-check in-repo consumers and any reachable generated clients.
- For serialized payloads: round-trip a captured real payload from before the change through the new code.

### 5. Sign off with a compatibility statement

Every change touching a guarded surface ends with an explicit statement in the PR/commit/summary:

> Contract impact: [none | compatible additions | breaking — strategy: <versioning/expand-contract/deprecation>]. Evidence: <tests/diff command run>.

## Constraints

- Absence of a schema file does not mean absence of a contract — consumers bind to observed behavior.
- "The tests pass" is insufficient when no test encodes the external contract; say so and add one.
- Renames are removals. A rename of anything externally visible is a breaking change, full stop.
- Do not resolve ambiguity in favor of convenience; flag `Potentially breaking — review required` with the evidence.

## Verification

- [ ] Contract surface and consumers stated before the edit
- [ ] Change classified against the taxonomy
- [ ] Breaking changes have an explicit compatibility strategy (or were not made)
- [ ] Contract evidence produced (test, schema diff, consumer compile, or payload round-trip)
- [ ] Compatibility statement included in the final summary
