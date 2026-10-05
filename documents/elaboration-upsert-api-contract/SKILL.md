---
name: elaboration-upsert-api-contract
description: >
  Produce a machine-readable API specification (OpenAPI 3.x in YAML) for the
  slice being built, so the build and tests consume a contract instead of
  prose. Use when designing or changing a REST endpoint, when the user says
  "design the API for this", "write the OpenAPI spec", "define the contract for
  MN-42", "what should the request/response shape be", or before code
  generation begins on a slice that exposes or changes an HTTP surface. This is
  the L3 keystone: the contract lives in the repo. Do NOT use to author an ADR
  (that is governance-author-adr), to write feature docs, to generate the
  implementation (that is create-code-generation), or for non-HTTP work.
---

# Elaboration: API design

Owned by the **Architect** persona (the L3 keystone of the workflow). Invoked as `/elaboration-upsert-api-contract`.

Turn the agreed slice into a **machine-readable contract**: an OpenAPI 3.x document in YAML under
`specs/`. Downstream steps (code generation, QE) consume this spec rather than re-deriving the shape
from prose, which is what moves the slice from prompt-driven to contract-gated work. The spec is the
single source of truth for paths, payload shapes, status codes, and auth on this slice.

## Before drafting

Read the repo's API conventions so the spec matches what already ships:
- `docs/conventions/api.md` - the detailed REST reference.
- `AGENTS.md` constitution clauses **C06** (PascalCase JSON wire format) and **C07** (thin
  controllers, one domain each, non-error outcomes return 200, errors via `ProblemDetails`).

Respect the repo documentation rules: **no source line numbers** anywhere (reference code by file
path + symbol name), and **no em-dashes** (use commas, colons, parentheses, or " - ").

## Design rules this spec must encode

- **Base standard: Zalando RESTful API Guidelines defaults** - OpenAPI-first, plural verb-free
  resource names, JSON/UTF-8, authenticated endpoints, semantic versioning, `problem+json` for errors.
- **Deviation (C06): JSON property names are PascalCase, not snake_case.** The `System.Text.Json`
  default and all existing API + Portal consumers are locked to PascalCase; flipping the wire format
  would break the whole surface. Schema property names in the spec MUST be PascalCase. Only deviate
  per-property where the serialized name must differ (e.g. CosmosDB system fields `id`, `ttl`).
  **C06 governs JSON body properties only.** Query and path parameters use snake_case (e.g.
  `page_size`, `environment_type`, `subscription_id`, bound via `[FromQuery(Name = "...")]`), per
  `docs/conventions/api.md`. Never PascalCase a parameter; use snake_case for new parameters, but
  match the wire name a parameter already ships with (some endpoints expose camelCase like `runType`),
  since renaming a live parameter is a breaking change.
- **Status codes (C07):** non-error business outcomes return **200 OK** with the outcome in the body.
  Reserve non-200 for actual errors (auth, validation, server), and model those error responses as
  RFC 7807 `application/problem+json` (`ProblemDetails`).
- **One domain per spec/controller.** Do not fold an unrelated resource into this slice's spec.

## The spec file is plain OpenAPI YAML (no front-matter)

`specs/<feature>.openapi.yaml` is a **plain OpenAPI document**. Do **not** put a markdown `---`
front-matter block at the top of it: a leading `---` starts a second YAML document in the same file
and breaks OpenAPI parsers and generators.

The spec joins the artifact graph indirectly, via an already front-matter'd artifact:
- Add a `relates.spec:` edge on the **story's repo doc or its ADR** pointing at the spec path, per the
  front-matter schema in `docs/ai-sdlc/artifact-graph.md` (example: `specs/cloudspace-compare.openapi.yaml`).
- The linter (`governance-check-graph`) validates that every `relates.spec` path resolves to a real
  file, so the edge must point at the spec you actually wrote.
- Link the spec to the work item via `governance-enrich-ticket`.

## Workflow

1. **Confirm scope.** Restate the resource, the operations (which verbs/paths), and the slice
   boundary. Name the work item key this serves. If the resource overlaps an existing controller's
   domain, say so and confirm a dedicated spec is correct (C07, one domain each).
2. **Draft the OpenAPI spec.** Define `paths`, request/response schemas with **PascalCase**
   body properties (but **snake_case** query and path parameters), `problem+json` error responses,
   and the security scheme. Where the slice reuses an
   existing type or endpoint, **verify it against the actual code (file path + symbol) before
   asserting it exists** - do not invent a schema name or route. State unverified shapes as open
   questions, not facts. (On Claude Code you can read the relevant source directly to confirm.)
3. **Write `specs/<feature>.openapi.yaml`** as plain OpenAPI YAML with no `---` front-matter. Create
   the `specs/` directory if it does not exist.
4. **Wire the graph edge.** Add or update `relates.spec:` on the story's repo doc or its ADR to point
   at the new spec, and suggest backlinking the spec onto the work item via `governance-enrich-ticket`.
5. **Confirm before writing.** Show the proposed spec (and the front-matter edge change) and get
   agreement before creating the files.

## Guardrails

- **Verify before asserting.** Reused types, endpoints, and auth policies must be checked against the
  code first; if you cannot confirm one, mark it as a decision or open question, not a fact.
- **PascalCase JSON bodies (C06); never PascalCase parameters.** Body properties are PascalCase; new query/path parameters are snake_case (e.g. `page_size`), but match the existing wire name of a shipped parameter (some are camelCase like `runType`) rather than renaming it. See `docs/conventions/api.md`.
- **Errors are `problem+json`; success is 200 (C07).** Do not model business outcomes as 4xx.
- **No front-matter inside the OpenAPI file.** The graph edge lives on the story doc or ADR, not the spec.
- **No line numbers, no em-dashes, no pasted artifacts.** Link to the spec; do not inline it into other docs.
- **Confirm before writing**, and keep one domain per spec.

## Next steps

- `/create-code-generation` (Developer) - consume this spec to drive the TDD build of the slice.
- `/governance-enrich-ticket` (any) - link the spec onto the work item and add a dated decision-log line.
- `/governance-author-adr` (Architect) - only if a load-bearing API decision was made (e.g. a new
  boundary or a deviation worth recording).
- `/governance-check-graph` (Lead) - confirm the `relates.spec` edge resolves once it is wired.
