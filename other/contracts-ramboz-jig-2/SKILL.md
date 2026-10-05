---
name: contracts
description: >
  Team baseline for external-interface contract artifacts: OpenAPI, JSON
  Schema, AsyncAPI, .proto, and GraphQL SDL, with spectral, ajv, buf, and
  graphql-inspector validation. Nudges devs toward contract-first artifacts;
  never writes them and never scaffolds a contracts/ directory. Auto-triggers
  for what contract should I use for this API, do we have an OpenAPI spec, add
  a JSON schema for this, recommend a schema for this endpoint, validate this
  API contract, or what's the right artifact for events. Defers to any other
  installed skill whose description identifies it as handling
  external-interface contract artifacts, API schema design, or contract-first
  workflow. Do not use for internal module-boundary refactoring, scaffolding a
  contracts/ directory, or auto-generating schemas from code.
user-invocable: true
---

> Spec 022 promoted this skill from a deliberate stub
> ([ADR-0002](../../docs/decisions/adr-0002-contracts-stays-deferred.md))
> to jig's **team baseline** for external-interface contract artifacts,
> following the reframing in
> [ADR-0005](../../docs/decisions/adr-0005-contracts-as-judgment-skill.md).
> Like `/jig:pr-review` (spec 012), `/jig:arch-review` (spec 014), and
> `/jig:vision-elicitation` (spec 017), it ships as SKILL.md only — no
> `.py` helper. The skill recommends the canonical industry-standard
> schema per external surface and points at the ecosystem tools that
> validate it. It does **not** write schemas, **not** scaffold a
> `contracts/` directory, and **not** enforce contracts via PreToolUse
> hooks. Enforcement is structural via the spec-author's first-pass
> attention and the independent-review reviewer prompt's second-pass
> check — both wired in slice 022-02.

## What this skill does

For each external surface a project exposes (HTTP API, event bus, RPC,
GraphQL, internal data shapes, CLI output, config), this skill
recommends:

1. **The canonical artifact** — what to put on disk (e.g.,
   `openapi.yaml`, `*.schema.json`, `*.proto`, `schema.graphql`).
2. **The validation tool** — what runs in CI to keep code and artifact
   in sync (e.g., `spectral lint`, `ajv validate`, `buf lint`,
   `graphql-inspector diff`).
3. **The codegen tool** — what produces typed clients / server stubs /
   TS types from the artifact, when ecosystem-appropriate (e.g.,
   `openapi-typescript`, `quicktype`, `buf generate`).

The skill is **breadth over depth**: catch the right artifact per
surface, leave language-specific niceties (Zod vs JSON Schema vs
Pydantic vs TypeBox for internal shapes) to a richer user-installed
contracts skill or to the dev's judgment. The recommendations are a
nudge; the dev decides whether to follow them.

## When to use vs. when to defer

- **Any other installed contracts skill.** Codex user location:
  `$HOME/.agents/skills/contracts/` — but the deferral is **category-based,
  not name-based**, so a skill named anything (`contracts`,
  `schema-design`, `contract-first`, `api-contracts`, etc.) whose
  description claims external-interface contract artifacts, API schema
  design, or contract-first workflow will be preferred. If one is
  present, **defer to it.** Codex can select
  the more specific skill by description; if you want to be sure,
  explicitly invoke that skill.
- **`/jig:arch-review`** — sibling jig skill that reviews the
  **design** of an API surface (the proposal, the trade-offs, the
  failure modes). This skill is downstream: once the design is locked,
  formalize the resulting interface as a contract artifact. Reach for
  `/jig:arch-review` to debate whether the API should exist; reach for
  this skill once it does.
- **`/jig:adr-workflow`** — if the dev decides to systematically opt
  out of the canonical recommendation for a surface (e.g., "we'll keep
  our bespoke env-contract checker, not migrate to a JSON Schema +
  ajv triple"), capture the rationale in an ADR. This skill nudges;
  ADRs document the choice when the nudge is declined.
- **The deferred ADR-0002 stub concept** (internal module-boundary
  enforcement, cross-module Python imports, kitchen-sink scaffolding).
  Not this skill. ADR-0002 stays in force for the internal-boundary
  problem; ADR-0005 carved out external-interface artifacts as the
  separate concern this skill addresses.

Rule of thumb: **external interface a caller depends on → this skill.
Internal Python imports → not this skill.**

## Per-surface artifact recommendations

The table below is the canonical reference. Each row prescribes the
recommended artifact + validation tool + codegen tool (where the
ecosystem affords one). Rationale: the most portable artifact with the
richest ecosystem tooling, biased toward stack-agnostic choices when
possible.

| Surface | Recommended artifact | Validation | Codegen | Rationale |
|---|---|---|---|---|
| **HTTP API** | OpenAPI 3.x (`openapi.yaml`) | `spectral lint`, `redocly lint` | `openapi-typescript`, `openapi-generator`, `orval` | De facto industry standard; richest ecosystem; vendor-neutral. |
| **Event bus / async messaging** | AsyncAPI (`asyncapi.yaml`) | `asyncapi/parser`, `spectral` (AsyncAPI ruleset) | `asyncapi/generator` (clients, docs, code) | Same shape as OpenAPI from the same maintainers; portable across Kafka / NATS / MQTT / WebSocket. |
| **RPC** | Protocol Buffers `.proto` (or Smithy for AWS-native) | `buf lint`, `buf breaking` | `buf generate` (Go / TS / Java / Python / etc.) | Schema-first by design; codegen is the primary workflow, not an afterthought. |
| **GraphQL** | SDL (`schema.graphql`) | `graphql-inspector diff`, `spectral-graphql` | `graphql-codegen` | Native to the GraphQL toolchain; SDL is the single source of truth across server and client. |
| **Internal data shapes** | JSON Schema (`*.schema.json`) | `ajv validate` | `quicktype`, `json-schema-to-typescript` | Portable across ecosystems; most language-agnostic. Stack-coupled alternatives (Zod for TS, Pydantic for Python, TypeBox for TS+JSON-Schema export) acceptable when the team has already standardized. |
| **Config / env vars** | JSON Schema (per config file) or bespoke env-contract pattern | `ajv validate`, custom env-contract checker | `quicktype` (when JSON Schema) | JSON Schema for structured config files; for env-var sprawl, a bespoke env-contract pattern (markdown reference table + `.env.example` seed + stdlib-only checker script + CI gate) is a worked-example-friendly alternative — see [ADR-0005](../../docs/decisions/adr-0005-contracts-as-judgment-skill.md) Context §1 for the case study that motivated this row. |
| **CLI output** | JSON Schema for `--json` / `--format json` output | `ajv validate` in shell-test fixtures | `quicktype` | Lets downstream pipes assume the shape; reproducible test fixtures. |

**Notes on the table:**

- One canonical artifact per surface — firmer nudge than a menu, with
  stack-coupled alternatives called out inline (rather than as
  separate rows) so the table stays scan-friendly.
- Internal data shapes is the row most likely to draw push-back: Zod /
  Pydantic / TypeBox have real ergonomic wins inside their respective
  stacks. The recommendation is JSON Schema because (a) it's portable
  across stacks, (b) the JSON-Schema → TS-types codegen path is
  already mature via `quicktype`. If a team is single-stack and
  committed, opting into Zod / Pydantic with optional JSON-Schema
  export (e.g., `zod-to-json-schema`) is a reasonable opt-out.
- Smithy is listed as an RPC alternative because AWS-native projects
  often standardize on it; for everything else, `.proto` wins on
  ecosystem maturity.

## When to opt out

**The skill nudges; it does not refuse edits.** Slice 022-02 will wire
two structural touchpoints that make declared surfaces visible to the
spec-author at init time (`/jig:vision-elicitation` Appendix A) and to
the independent reviewer at slice-review time (`review.py` prompt
template). Even with those wired, no part of jig blocks a commit or
rejects a slice for skipping an artifact — the wizard skips on empty
answer, the reviewer flags a *suggestion*, and `migrate.py report`
*recommends* per surface without auto-rewriting.

Legitimate opt-out scenarios:

- **Migration of a project with a working bespoke pattern.** If a
  project already ships a contract-shaped artifact (e.g., the
  `env-contract.md` + `.env.example` + stdlib-checker triple from
  aso-shallow-validator), don't force a migration. The pattern works;
  the recommendation table is for new surfaces.
- **One-off internal tool with a single consumer that will never
  expand.** A throwaway script's `--json` output doesn't need a JSON
  Schema. The skill's value is at the surface that has (or will have)
  more than one caller.
- **Pre-existing different artifact in active use.** RAML, JSON-RPC
  schemas, Avro, hand-rolled IDLs — if the team has invested and the
  tooling works, no migration. The skill's recommendations are for
  surfaces that don't yet have an artifact.
- **Pre-product-market-fit prototype.** Contract artifacts are
  durability-shaped. If the interface is being thrown away next sprint,
  defer.

When the opt-out is structural (a whole project commits to a
non-canonical pattern), capture the rationale in an ADR via
`/jig:adr-workflow`. The nudge is informed by the table; the
documented exception is informed by the ADR.

## Worked examples

Two worked examples ship as sibling files, intentionally on different
**external surfaces** (HTTP API vs. internal data envelope) to
demonstrate the recommendation pattern (artifact + validation tool +
CI gate + optional codegen) applies regardless of surface shape:

- [worked-example-openapi-http.md](worked-example-openapi-http.md) —
  formalizing a prose HTTP API contract (the
  aso-shallow-validator §5 case) into an OpenAPI 3.x spec, wiring
  `spectral` as the CI gate, and generating typed clients via
  `openapi-typescript`. Surface: HTTP API.
- [worked-example-json-schema-envelope.md](worked-example-json-schema-envelope.md)
  — pinning an internal data envelope with JSON Schema, validating
  with `ajv` in tests, and noting the stack-coupled alternatives
  (Zod / Pydantic / TypeBox) where they're idiomatic. Surface:
  internal data shape.

Both worked examples use JS/Node tooling in the code blocks — that's
the most universally-installed ecosystem for `spectral` / `ajv` /
`openapi-typescript` / `quicktype`. The recommendations themselves
are stack-agnostic; the same artifacts apply equally in Go (`protoc`
+ `buf`), Python (`jsonschema` + Pydantic), Rust (`utoipa` +
`serde_json`), etc. The recommendation table is the stack-neutral
map; the worked examples are one concrete instantiation each.

## Gotchas

- **The skill recommends, devs author. Never auto-generate the
  artifact from prose docs.** Auto-conversion is too lossy for a
  one-shot tool: prose contracts encode informal assumptions
  (idempotency rules, cache hints, error remediation) that don't map
  to schema fields. The dev (or an LLM driving the migration with
  prompt context) writes the artifact; the skill flags the gap.
- **The recommendation table is the canonical reference. Don't deviate
  silently.** If a project picks a different artifact per surface, the
  choice belongs in an ADR — visible to future contributors. Quiet
  deviations look like accidents to the next reviewer.
- **Ecosystem tools have version churn; the skill won't pin
  versions.** `spectral`, `ajv`, `buf`, `graphql-inspector` and their
  generators all move. The skill names them; the dev pins them in
  their project's lockfile.
- **The two worked examples are intentionally JS/Node and
  stack-agnostic.** The abstraction lives in the per-surface table,
  not in the worked-example implementations. If your stack is
  different (Go + protoc, Python + jsonschema, Rust + utoipa), the
  table still applies; the worked-example commands change.
- **This is not a CI tool.** The skill recommends which CI gate to
  wire (`spectral`, `ajv`, `buf`); it doesn't run the gate. The dev
  configures their CI to call the tool against the artifact.
- **Fallback mode** (if the routing-dogfood ever fails): the SKILL.md
  frontmatter gets `disable-model-invocation: true` and the skill
  becomes explicit-invocation-only (`/jig:contracts`). In that mode no
  auto-trigger fires — the user types the slash command. If you see
  `disable-model-invocation: true` in this skill's frontmatter, that's
  why.

## Relationship to other skills

- **`/jig:vision-elicitation`** — slice 022-02 grows Appendix A to ask
  what external surfaces the project exposes at scaffold-init time,
  with hand-off to this skill's recommendation table. Declared
  surfaces become visible to the next two integration points.
- **`/jig:independent-review`** — slice 022-02 extends the reviewer
  prompt template with a "slice touches a declared contract surface?
  artifact updated in the same change-set?" check. Conditional — only
  fires when surfaces have been declared.
- **`/jig:migrate`** — slice 022-02 grows `migrate.py report` output
  with a "Contract surfaces detected" section that flags existing
  artifacts on disk + prose API contracts + env-contract-style
  patterns + hand-typed boundary types. Recommends per surface; never
  auto-rewrites.
- **`/jig:adr-workflow`** — captures structural opt-outs from the
  recommendation table when a project deliberately chooses a
  non-canonical artifact.
- **`/jig:arch-review`** — orthogonal sibling. Reviews the design of
  the API surface; this skill formalizes the resulting interface as
  an artifact. Use arch-review first (does the API make sense?) then
  this skill (what artifact should it have?).
- **`/jig:pr-review`** — orthogonal. A PR-shape diff review may
  surface contract drift (response shape changed without artifact
  update); this skill is the place to look up which artifact should
  govern.
