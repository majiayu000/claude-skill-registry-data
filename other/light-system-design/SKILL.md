---
name: light-system-design
description: >-
  Design or modernize a software system from an evidence-backed current-state
  inventory through quality attributes, architecture options, API and schema
  contracts, migration/rollback plans, ADRs, and verification. Use for
  greenfield or existing monoliths, modular monoliths, services, system/API/
  database design, schema migration review, data-flow reliability, tenant/PII
  controls, or architecture evolution. Existing systems stay read-only until
  the user selects an option and authorizes exact mutations. Unknown facts stay
  UNKNOWN. This is an off-DAG engineering skill: do not emit findings or invent
  STAGE_GATES, ROUTES, stages, or back-edges.
---

# System design lifecycle

Own system boundaries, runtime interfaces, operational data stores, system
migrations, and architecture decisions. Do not equate a diagram, SQL file, or
OpenAPI document with a working, safe, or scalable system.

Read
[`references/system-design-resource-map.md`](references/system-design-resource-map.md)
before any existing-system task. It defines the lifecycle, artifact contract,
decision stop, evidence states, access tiers, and cross-skill ownership. Read
[`references.md`](references.md) only for the database/API/reliability branch
that applies to the selected system.

## Non-negotiable boundary

1. Treat repository, configuration, schema, API, dependency, and deployment
   intake as read-only access. It is not authorization to rewrite them.
2. Preserve absent facts as `UNKNOWN`. Do not infer traffic, SLOs, consistency,
   budget, compliance, migration windows, or team capability from the phrase
   “system design.”
3. Present at least a recommendation, a viable alternative, and explicit
   rejection/exit conditions. Stop before choosing the database, topology,
   compatibility policy, or migration strategy for the user.
4. Bind any later mutation to a user-selected option and exact authorized
   action IDs. Keep before/after locators, SHA-256, verification, and rollback.
5. Never mutate a production database or configuration. Apply only to a
   disposable environment explicitly placed in scope; otherwise deliver a
   reviewed plan and scripts.
6. Describe `schema_lint.py` as a lexical heuristic. It is not a SQL parser,
   query planner, lock simulator, schema diff engine, or zero-downtime proof.
7. Keep `VERIFIED` for checks that actually ran and retain their command,
   return code, locator, and hash. Use `PLANNED`, `UNKNOWN`, or `UNAVAILABLE`
   otherwise.
8. Keep this skill off the research DAG. Emit no `light.findings.v1`; add no
   `STAGE_GATES`, `ROUTES`, stage number, or back-edge; do not attach `_shared`.

## Choose the mode

| Situation | Mode |
|---|---|
| New system with no implementation | greenfield requirements and option design |
| Existing repository/system | read-only intake, then current-state inventory |
| Existing monolith or services changing gradually | modernization with compatibility and rollback |
| API-only change | contract and consumer compatibility branch |
| Schema-only change | dialect/version/context-specific migration branch |
| User supplied a completed package | review and evidence verification |

## Phase 1 — Intake and protection

Capture or preserve as `UNKNOWN`:

- users, business goal, critical use cases, data classification;
- load range, latency, availability, durability, and consistency targets;
- team/operations capability, budget, deployment environment, compliance, and
  migration window;
- topology: greenfield, monolith, modular monolith, or services;
- components, owners, interfaces, stores, dependencies, write paths, trust
  boundaries, failure modes, versions, source locators, and freshness;
- existing clients, schema history, deployment/runtime constraints, and
  compatibility promises.

For an existing system, create an intake manifest from
[`templates/system-intake.template.json`](templates/system-intake.template.json)
and run:

```text
python scripts/architecture_lifecycle.py intake <root> \
  --manifest <system-intake.json> --out <evidence-dir>
```

Keep `--out` outside the source root. Read all emitted artifacts and verify
`source_unchanged=true`.

## Phase 2 — Requirements and current state

Produce:

- context and quality-attribute scenarios with a measurable stimulus,
  environment, response, and target or `UNKNOWN`;
- capacity estimates for request rate, storage growth, fan-out, latency budget,
  and any dominant resource; if unknown, write `UNKNOWN` plus the measurement
  plan rather than inventing numbers;
- current-state → target-state mapping with explicit gaps. For greenfield,
  current state can be `none`, but the gap list still records missing evidence;
- architecture fitness functions: observable signals, thresholds, verification
  command/probe, and evidence state. A quality attribute without a fitness
  function is still only prose;
- a component/interface/store inventory with owner and fact provenance;
- synchronous/asynchronous data flows, transaction boundaries, delivery
  semantics, idempotency/deduplication, backpressure, timeout/retry, and failure
  handling;
- risk, assumption, unknown, and stale-fact registers.

Do not silently convert a code search into an architecture truth. Mark each
fact as declared, observed, inferred, or unknown.

## Phase 3 — Options and decision stop

Present at least:

1. a recommended option with reasons;
2. a viable alternative;
3. conditions under which each should not be used;
4. cost/complexity, migration risk, compatibility window, rollback, operations,
   and exit criteria;
5. unresolved facts that could reverse the recommendation.

Then stop. Ask the user to select an option and authorize exact action IDs.
Do not prewrite the user's choice or generate the chosen schema/API/migration/
ADR as if approval already existed.

Before presenting the decision, validate that requirements, capacity estimates,
current/target state, fitness functions, at least two genuinely different
options, hard-constraint and fitness evidence, tradeoffs, rejection conditions,
reversal costs, and migration/deprecation stance are present:

```text
python scripts/design_readiness.py --input templates/design-readiness.example.json \
  --as-of 2026-07-05
```

In `proposal`, PASS means only `ready_for_user_decision=true`; it never writes
the selection, and the report emits a canonical `option_packet_sha256` for each
option. In `authorized`, the selection must be paired with a
`light.system-design.v2.authorization` whose option digest still matches,
whose approved action IDs are a subset of that option, whose target is
explicitly disposable, whose rollback cannot be waived, and whose date is not
later than `--as-of`. The walking skeleton
(`entry/core_path/state_boundary/observable_result/failure_probe/verification/action_ids`)
may contain only approved actions before `ready_for_implementation=true`.

For each option, state whether migration/deprecation is applicable. If it is
applicable, the option must be replacement-first. Consumer inventory is a list
of stable consumer/interface IDs, owners, usage status, evidence state,
evidence locator/date, or an explicit measurement plan. Telemetry is a
structured metric/source/evidence record. Rollout is a sequence of phases with
entry, exit, and rollback conditions; rollback has a trigger, action, and
verification. A deprecation compatibility window has start, end, and removal
conditions. Plain strings do not satisfy these fields. If migration is not
applicable, record why; do not leave it blank.

Use
[`templates/decision-authorization.template.json`](templates/decision-authorization.template.json)
after the user responds. Copy the selected digest emitted by
`design_readiness.py`; a changed requirement, state model, fitness function, or
selected option changes that digest and requires fresh authorization.

## Phase 4 — Build the architecture package

After authorization, produce only the selected scope:

- context and quality attributes;
- component/boundary and data-flow views;
- API/event contracts and consumer compatibility policy;
- schema and current-to-target change plan;
- rollout, backfill, rollback, and deprecation plan;
- ADR with alternatives and consequences;
- security/privacy design controls and items for specialist review;
- verification plan and delivery evidence.

Use
[`templates/architecture-package.template.md`](templates/architecture-package.template.md).
Treat bundled SQL/OpenAPI files as dialect/version-labeled examples, never as
production defaults.

## Phase 5 — Contract, schema, and migration checks

### API contract

Define versioning, authn/authz boundary, error model, pagination, idempotency,
compatibility window, and deprecation. Validate OpenAPI with:

```text
python scripts/contract_validate.py --spec openapi.yaml \
  --examples examples.json --json
```

`VALIDATED` requires `openapi-spec-validator` plus successful example-schema
checks. `STRUCTURE_ONLY` or `UNAVAILABLE` is not contract validation.

### Schema and migration

Keep four tasks separate:

1. design-time schema review;
2. current-to-target diff/drift;
3. migration SQL risk lint;
4. rollout/backfill/rollback execution tests.

Run the heuristic linter only with an explicit dialect and relevant context:

```text
python scripts/schema_lint.py --ddl migration.sql \
  --dialect postgresql --server-version 18 \
  --context migration-context.json --json
```

For authoritative diff/drift, use a real engine/tool selected for the project
(for example Atlas, Skeema, Alembic, Flyway, Liquibase, or Prisma) and preserve
its command/output. Do not claim this skill implements those engines.

Generate an ER view from a schema spec:

```text
python scripts/er_diagram.py --in schema.yaml --strict --out schema.mmd
```

If Mermaid rendering is unavailable, report syntax/structure verification only.

## Phase 6 — Verify, rehearse, and deliver

Verify as applicable:

- contract and example request/response;
- schema creation and migration on the selected database/version;
- data preservation, compatibility window, rollback, and reapply;
- load assumptions rather than invented load results;
- timeout/retry/circuit-breaker and failure drills;
- logs, metrics, traces, SLOs, deployment, and rollback observability;
- tenant isolation and PII controls with specialist review still pending.

Record authorization binding, source-intake binding, implemented action IDs,
artifact hashes, and verification entries in the package manifest, then run:

```text
python scripts/architecture_lifecycle.py verify-package \
  --package package-manifest.json --json
```

Deliver only when the package distinguishes `VERIFIED`, `PLANNED`, `UNKNOWN`,
and `UNAVAILABLE`; every `VERIFIED` entry is evidence-backed; the manifest
binds the copied authorization file, option digest, approved action IDs, and
implemented action IDs; and existing-system packages bind the read-only
`intake-integrity.json` hash. Artifact and verification locators in the
manifest are resolved relative to the manifest's directory and must stay inside
that package directory; `../`, absolute paths to outside evidence, or
current-working-directory-dependent locators are not a portable delivery
package.

## Cross-skill ownership

- `system-design`: system boundaries, runtime interfaces, operational schema,
  system migration, reliability choices, ADRs.
- `project-structure`: visible file tree and authorized file moves. Borrow its
  protection discipline; never send schema migration back to it.
- `data-engineering`: research-data quality, lineage, transformations, splits,
  and data release. A service database is not a research dataset pipeline.
- `frontend-design`: interaction and interface implementation. This skill owns
  backend/API boundaries, not UI.
- `research-ethics`: final ethics/privacy judgment. This skill proposes design
  controls and review items only.
- `orchestrator`: may consume delivered state; it receives no invented gate.

## Validation

Run every script self-test:

```text
python scripts/architecture_lifecycle.py --selftest
python scripts/schema_lint.py --selftest
python scripts/er_diagram.py --selftest
python scripts/contract_validate.py --selftest
python scripts/design_readiness.py --selftest
```

Before delivery, verify:

- [ ] Existing-system intake was read-only.
- [ ] Unknown requirements and stale facts stayed explicit.
- [ ] Capacity/load/storage estimates are explicit; unknowns have measurement
      plans instead of invented numbers.
- [ ] Current-state → target-state gaps are recorded, even for greenfield
      (`current_state=none`).
- [ ] Every quality attribute has a fitness function and each option has a
      fitness result with evidence or an honest UNKNOWN/UNAVAILABLE warning.
- [ ] Options, tradeoffs, rejection conditions, and a real user decision exist.
- [ ] Authorization digest still matches the selected option packet; approved
      action IDs are in scope, the target is explicitly disposable, and
      rollback remains required.
- [ ] Package manifest binds the authorization file hash, option digest,
      implemented action IDs, and read-only intake integrity or an explicit
      greenfield/not-applicable reason.
- [ ] At least two interfaces/options were compared; the first idea was not silently accepted.
- [ ] The authorized design has the thinnest end-to-end walking skeleton and a failure probe.
- [ ] Migration/deprecation stance is explicit; applicable migrations are
      replacement-first with consumer inventory, telemetry, rollout, rollback,
      and compatibility window.
- [ ] Mutations match authorized action IDs and a disposable target.
- [ ] API/schema/migration claims state dialect, version, context, and limits.
- [ ] Every `VERIFIED` item has command, return code, locator, and SHA-256.
- [ ] Every verification entry carries action IDs that are inside the
      implemented and approved scope.
- [ ] Package artifact/evidence locators are manifest-relative and do not
      escape the package directory.
- [ ] Rollback and compatibility were exercised or remain visibly planned.
- [ ] Cross-skill and off-DAG boundaries remain intact.
