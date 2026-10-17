---
name: graphql-api-architect
description: >
  Designs the inbound GraphQL adapter of an already-modeled use case — schema-first, Spring for
  GraphQL on the servlet stack — into the `31-graphql.md` partial: the root fields and the input port
  each calls (the same port a REST adapter calls), types and nullability, mutation inputs and
  payloads with `userErrors`, Relay connections with a page ceiling, `@BatchMapping` child fields and
  the batch ports they ask for, the error map, field-level access, personal data per output field,
  and — on the project's first GraphQL case — the depth, complexity, timeout, batch-size,
  introspection, GraphiQL and CORS setup, plus a quota per caller or a concurrency cap when the use
  case states one. Use when the request involves GraphQL, a schema or `.graphqls` file, a query or
  mutation, a resolver, `@QueryMapping`, `@BatchMapping`, DataLoader, N+1 in GraphQL, a connection or
  cursor, GraphQL errors, or a rate limit on the GraphQL endpoint. Piece of the `/new-feature` pipeline:
  requires `10-domain.md` and a `00-use-case.md` whose `Trigger` names a GraphQL adapter in the
  given folder — and stops without them.
argument-hint: "[path of the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*), Bash(curl:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# GraphQL API Architect

Designs **how a use case is exposed over GraphQL**: which root fields exist and which input port
each calls, what the schema promises and what it may answer `null`, how a mutation reports what the
client can correct, how a list that grows is paged, which child fields load in batches and through
which port, what each failure becomes, which field needs its own access check, and — once per
project — the limits every operation runs under. What `domain-modeling` left as an input port, this
skill gives a GraphQL shape, next to or instead of the REST shape `rest-api-architect` gives it.

**Entry rule: no GraphQL trigger, no GraphQL design.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `10-domain.md` and runs only when the `Trigger`
row names `inbound GraphQL adapter` or `inbound REST and GraphQL adapters`. Without `10-domain.md`,
stop and say to run `/domain-modeling`; with a trigger that names no GraphQL adapter, stop and say
so — the protocol is the use case's choice, never this skill's.

**Scope rule: queries and mutations over HTTP, nothing else.** A case that needs a subscription, a
file upload, federation, a repository exposed as a resolver, generated types, or the reactive stack
is outside this skill (`@.claude/rules/api-graphql.md`, the scope paragraph, and
`references/pitfalls.md` § Out of scope). Stop, name which of them the case needs, and record it —
the user decides between narrowing the case with `use-case-design` and deferring it. An operation
callable without authentication is the same: the endpoint stays authenticated, and opening it is a
design decision outside this run.

**Exit rule: it doesn't write code.** It emits `31-graphql.md`. The schema file, the controller, the
records, the resolver and the configuration come from the executor agent, which reads the partial
and the `templates/` exemplars.

**Rule rule: the rules don't live here.** Protocol choice, boundary, schema, batching, pagination,
errors, access, demand limits, evolution, observability and tests are
`@.claude/rules/api-graphql.md`, which cites `@.claude/rules/authorization.md`,
`@.claude/rules/error-handling.md` and `@.claude/rules/personal-data.md`. This skill applies and
cites them; it doesn't reproduce them.

## How it's invoked

Two paths: `/graphql-api-architect` by hand, or chained by `/new-feature` as step 3g, right after the
REST step and before security. That's why it does **not** carry `disable-model-invocation` — a skill
the model can't see is a skill the orchestrator can't call
(`@.claude/decisions/0007-pipeline-skills-invocation.md`). The guard against firing out of order is
the entry rule above.

## Why this is a skill and not a subagent

Form 1, motivated by axis 1 of the designer's interview: a solution-design step that picks the
inbound protocol per case is planned, and without a GraphQL designer that choice had no path and fell
back to REST by omission; the maintainer chose to design it ahead of a run that shows the defect, on
the pitfalls the official documentation and the library's source record (`references/pitfalls.md`) —
seven of them reproduced only by running the exemplars. The closest rejected form was a GraphQL mode
of `rest-api-architect`: its interview reaches verbs, statuses and `Idempotency-Key`, not nullability,
batching, connections or demand limits, and its norm's territory cannot reach a GraphQL package. A
subagent fails the counter-test on all three points: the interview is the task, the reference fits
in `references/` and `templates/`, and the partial is short.

Pinned to `opus`: the partial is what the executor implements verbatim, and the pin holding for the
rest of the turn keeps `/new-feature` on the model that designed it
(`@.claude/decisions/0081-skill-model-required-per-class.md`). Design record:
`@.claude/decisions/0146-graphql-api-architect-skill.md` (this repository only).

## Boundary with neighboring skills

| Piece | Decides | Never decides |
|---|---|---|
| `use-case-design` | The trigger — REST, GraphQL or both — and the `Access` row | The schema |
| `domain-modeling` | The input ports, their read models, the exceptions and `errorCode`s | Anything about GraphQL |
| `rest-api-architect` | The REST operations over the same ports, when the trigger names both | The GraphQL shape |
| **this skill** | Root fields and their ports, types and nullability, inputs, payloads and `userErrors`, connections, batch loads and the batch ports they ask for, the error map, personal data per output field, the project's GraphQL setup, GraphQL dependencies and configuration | The ports, the access rules, the batch query's statement, the tests' code |
| `security-architect` | One access row per root field and per sensitive field, the meta-annotation each uses, the endpoint in the filter chain | Which fields exist |
| `persistence-architect` | The batch port's statement and its index, the order's index | The batch port's existence (§ 5 asks for it) |
| `test-architect` | Which test proves each case of § 10, and the schema snapshot test | — |

Doesn't collide with `gof-design-patterns`: that skill owns the catalog, this one decides which row
shapes the GraphQL layer of the case being designed (step 12b).

## Procedure

1. **Read the specs.** `00-use-case.md` (trigger, `Access`, Components table, response shape),
   `10-domain.md` (input ports and their signatures, read models, exception table with `errorCode`),
   and — when present — `30-rest.md` (the REST operations over the same ports). Apply the entry rule
   and the scope rule. List the operations the case needs, each with the input port it calls.

   **A port that returns an entity, or a read model a field would complete lazily, is a divergence**,
   not something to work around here: `10-domain.md` is `domain-modeling`'s to change, and the
   operation stays undesigned until the port returns a complete read model.

2. **Survey — every answer the project already gave is inherited, never re-asked.**

   ```bash
   # Boot line and whether Spring for GraphQL is already in the build
   grep -m1 -A1 "<artifactId>spring-boot-starter-parent" pom.xml
   grep -nE "spring-boot-starter-graphql" pom.xml
   # GraphQL code and schema files already in the project
   grep -rlnE "@(QueryMapping|MutationMapping|SchemaMapping|BatchMapping)" --include='*.java' src/main 2>/dev/null
   find src/main/resources/graphql -name '*.graphqls' 2>/dev/null
   # Decisions earlier use cases recorded — the project setup lives in the first one's § 6
   find docs/use-cases -name '31-graphql.md' 2>/dev/null
   # The project's admission setup — a REST case may have written it before any GraphQL case
   grep -rln "AdmissionProperties" --include='*.java' src/ 2>/dev/null
   ```

   And the active blueprint's `packages.map` entry ending in `.graphql` — the package every
   controller, record and the wiring go to. No such entry → stop and say which line is missing from
   the blueprint, instead of choosing a package inside this use case.

   The templates' Boot-side packages (`GraphQlSourceBuilderCustomizer`, `@GraphQlTest`) are Boot 4's.
   On a Boot 3 project the design is the same; record the line in the partial's header so the
   executor reads the Boot 3 names from the build, never from the template.

   | Fact | Inherited from | Asked only when |
   |---|---|---|
   | Project setup — limits, introspection, GraphiQL, CORS | The first `31-graphql.md` § 6 | No earlier `31-graphql.md` — first GraphQL case of the project |
   | A type an earlier case declared (`Order`, `Money`) | The schema file and its `31-graphql.md` § 2 | Never — extended additively, never redefined |
   | Project-wide pieces (`GraphQlLimits`, `GraphQlConfig`, `GraphQlExceptionResolver`) | Already in the GraphQL package | First GraphQL case |

3. **Interview — only what steps 1 and 2 did not settle.** `AskUserQuestion`, at most 4 questions
   per call and **never fewer than 2 real options** per question; an axis with one sensible answer is
   decided and recorded, not asked (`@CLAUDE.md` § Known pitfalls). Every option states its cost.

   | Axis | Decides | Skip when |
   |---|---|---|
   | **Which fields and children the client reads** — the screens or callers, and what each selects | § 2, and which children are batch loads | The response shape of `00-use-case.md` already lists them |
   | **Does the list grow without bound** | § 4 — a connection, and its order | Never a plain list for a growing set |
   | **Each output field that matches a masking candidate** — full, reduced or a reference, and who reads it | § 8, and a field-level check | No field matches |
   | **Does an input update part of an object** — may the client clear a field | § 3 — `ArgumentValue` per field | The case creates or acts, never edits fields |
   | **The project setup** — internal or public clients, the origins a browser calls from, the slowest port | § 6 | Inherited |

4. **Fix the operations and the schema — § 1 and § 2.** One root field per operation, each calling an
   input port; a query never mutates, a mutation takes one `input` and returns one payload. Types,
   fields and nullability per `@.claude/rules/api-graphql.md` § Schema, names per
   `@.claude/rules/naming.md`; a type an earlier case declared is extended, never redeclared. Form:
   `templates/schema.graphqls.example` and `templates/GraphQlController.java.example`.

5. **Fix inputs and payloads — § 3.** Shape validation on the input record; every `errorCode` the
   use case can raise that the client can correct goes to `userErrors`, with the input path it
   concerns. A partial update binds each optional field with `ArgumentValue`.

6. **Fix pagination — § 4.** Every list that grows is a connection, forward only unless a client
   pages backwards; the order ends in a unique key; the default and maximum page come from § 6.

7. **Fix the batch loads — § 5.** Every child field that costs I/O, the batch port it needs — keys
   in, map out — and what a missing key answers. A batch port `10-domain.md` does not declare is a
   **requirement** in § 9, never invented as if it existed.

8. **Decide or inherit the project setup — § 6.** First GraphQL case: every limit of
   `@.claude/rules/api-graphql.md` § Demand limits with its value and its reason — form
   `templates/GraphQlConfig.java.example` and `templates/application-graphql.yml.example`. Later
   cases: `inherited from UC-NNN`, and a change only with a reason and a row in
   `## Impact on approved use cases`.

8b. **Admission — § 6's `Admission` rows.** Only when `00-use-case.md`'s `Admission` row is not
   `none`; no row, the rows read `none`. A limit is never proposed (`@.claude/rules/inbound-admission.md`
   § When a limit exists). The project's admission setup — where the quota is enforced, replicas, the
   caller's key, the 503 wait — is asked exactly as `@.claude/skills/rest-api-architect/SKILL.md`
   step 7c asks it, when step 2 found no `AdmissionProperties`; found, or written by a REST case's
   `30-rest.md` § 8, it is `inherited from UC-NNN`. Then the case's limits:

   | Limit | Where | Written |
   |---|---|---|
   | Quota | The whole GraphQL endpoint, per caller, before the document runs — never per field or per cost | The `graphql` entry of `app.admission.quotas`, stated and per-replica. The first case to state one sets it; a later case's different number is a CHANGE with a reason, since every operation shares it. The 429 is HTTP, Problem Details, before any GraphQL response — a row in § 7 and a case in § 10 |
   | Cap | The root field's controller method, `@Bulkhead(name = "inbound-<slug>")` | Size below the scarcest resource the case holds, and why; the `SERVICE_BUSY` row in § 7 and its case in § 10 |

   The pieces are `@.claude/skills/rest-api-architect/templates/AdmissionConfig.java.example` and
   `application-admission.yml.example`, in the GraphQL package's `admission` subpackage when the
   project has no REST adapter.

9. **Fix the error map — § 7.** Each exception of `10-domain.md` the operations can raise, where it
   lands (`userErrors` or top-level), its classification and `errorCode`, per
   `@.claude/rules/api-graphql.md` § Errors. Form: `templates/GraphQlExceptionResolver.java.example`.

10. **Personal data — § 8.** Every output field walked through `@.claude/rules/logging.md` § Masking
    candidates; each match gets the recorded decision `@.claude/rules/personal-data.md` § In transit
    requires. A field in clear for a narrower audience than the operation's needs a field-level
    check — a row for `security-architect` in § 9.

11. **Requirements to other partials — § 9.** The batch ports to `10-domain.md`; one statement per
    batch port and the order's index to `20-persistence.md`; one access row per root field and per
    sensitive field to `32-security.md`. Each a row, never an edit of another partial.

12. **Test cases, dependencies and configuration — § 10, § 11, § 12.** § 10 lists every case
    `@.claude/rules/api-graphql.md` § Tests names, by level — slice, HTTP through the real chain,
    schema snapshot. § 11: the Initializr's `graphql` dependency and its test starter, version empty —
    managed by the Boot parent; read the id against the project's Boot when the build lacks it:

    ```bash
    curl -s "https://start.spring.io/dependencies?bootVersion=<boot from step 2>" \
      -H 'Accept: application/vnd.initializr.v2.2+json' | grep -o '"graphql":{[^}]*}'
    ```

    Never a version from memory (`@CLAUDE.md` invariant 8); no network → ask. The executor may write
    `pom.xml` for exactly these rows. § 12 lists every property, its value and its owner.

12b. **Decide the design patterns of this layer.** Run
    `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the controllers, records
    and mappers this case adds. The answer goes into `## Design patterns` — `none` when nothing
    matches, and absence is not `none`.

13. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/31-graphql.md`, from
    `templates/graphql-spec.md.example`. Thirteen numbered blocks plus `## Design patterns`, all
    mandatory, each written as `none` when there is nothing — absence is not `none`.

14. **Report and stop.** Path of the file written; each root field with its port; every connection
    with its ceiling; every batch load and the port it asks for; every field of § 8 in clear with its
    receiver; § 6 decided or inherited; each § 9 requirement. A port returning an entity, a growing
    list without a connection, or a child field with I/O and no batch is a finding. Don't invoke
    anyone else: the next pipeline step reads § 9.

## What the partial contains

| Block | Fixes |
|---|---|
| 1 · Operations | One row per root field: kind, input port, return, REST counterpart |
| 2 · Schema | Types, fields, nullability and why, the read model behind each |
| 3 · Inputs and payloads | Input fields and shape validation, payload, `userErrors` codes |
| 4 · Pagination | Per connection: directions, order with its unique key, default and maximum page, the cursor's keys |
| 5 · Batch loads | Per child field: the batch port (a requirement when new), key, missing-key answer |
| 6 · Project setup | Every limit with its value and reason — or `inherited from UC-NNN` — and the `Admission` rows: `none`, or the setup and this case's quota and cap (step 8b) |
| 7 · Error map | Situation, where it lands, classification, `errorCode` |
| 8 · Personal data | Per matching output field: form, receiver and reason |
| 9 · Requirements to other partials | Batch ports, statements and indexes, access rows |
| 10 · Contract test cases | Every case, by level |
| 11 · Declared dependencies | The starter and its test starter |
| 12 · Configuration | Every property, its value, its owner |
| 13 · Deferred | Same shape as every partial. `none` when nothing was deferred |
| Design patterns | Each pattern the controllers, records or mappers adopt — step 12b |

Plus `## Impact on approved use cases` and `## Implementation order`, as in every partial.

The exemplars in `templates/` are **reference for form**, not files to copy. Each was compiled and
run against the classpath the Initializr resolved on the day it was written:

The mapper comes in two exemplars — `OrderGraphQlMapper` inside `GraphQlController.java.example`, and `GraphQlMapStructMapper.java.example` beside it — because the mechanism is the project's, not this partial's: the partial says what maps to what, and the executor writes it in the mechanism the root `CLAUDE.md`'s `**Mappers:` paragraph names (`@.claude/rules/mapping.md`).

| Exemplar | Shape of |
|---|---|
| `templates/schema.graphqls.example` | The schema file: nullability, a connection by suffix, a mutation input and payload, `UserError` |
| `templates/GraphQlController.java.example` | The input ports and read models it calls, the adapter records, the mapper, `@QueryMapping`, a connection through `ScrollSubrange` and `Window`, `@MutationMapping` with `userErrors`, two `@BatchMapping`, a guarded `@SchemaMapping` |
| `templates/GraphQlMapStructMapper.java.example` | The same read model → schema type mapper as a MapStruct interface, for a project whose mechanism is MapStruct: generated records, a `Money` from two source fields through a `@Named` method |
| `templates/GraphQlConfig.java.example` | `GraphQlLimits`, depth, complexity, timeout, batch size, the schema inspection that fails the startup |
| `templates/GraphQlExceptionResolver.java.example` | Each family to a classification and `errorCode`; `null` for the rest |
| `templates/application-graphql.yml.example` | Introspection and GraphiQL by profile, CORS, `app.graphql.*` |
| `templates/graphql-spec.md.example` | The partial |

The test shapes are `test-architect`'s: `GraphQlControllerTest.java.example`,
`GraphQlHttpIT.java.example`, `GraphQlSchemaCompatibilityTest.java.example`.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json`, and `ArchHook.java guard` enforces it. Writes inside the use
case folder and nothing else.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` (mandatory), `10-domain.md`
(mandatory), `30-rest.md` (when present), the `31-graphql.md` of earlier cases, `pom.xml`, the schema
files under `src/main/resources/graphql/`, the active blueprint's `packages.map`, the Initializr's
metadata, `@.claude/rules/api-graphql.md`, `@.claude/rules/authorization.md`,
`@.claude/rules/error-handling.md`, `@.claude/rules/personal-data.md`, `@.claude/rules/logging.md`,
`@.claude/rules/naming.md`, `@.claude/rules/architecture-ddd.md`, and this skill's `references/` —
plus, with an `Admission` row, `@.claude/rules/inbound-admission.md` and the partial that wrote the
admission setup.

**Writes** `docs/use-cases/UC-NNN-<slug>/31-graphql.md`. Nothing else.

**Owns** the root fields and the port each calls, the schema's types and nullability, inputs,
payloads and `userErrors`, connections and their ceilings, batch loads and the batch ports they ask
for, the GraphQL error map, the personal-data decision per output field, the project's GraphQL setup,
the GraphQL endpoint's quota and each root field's cap, and GraphQL dependencies and configuration.

**Does not decide** the input ports, their read models or the exceptions (`10-domain.md`), the
trigger or the `Access` row (`00-use-case.md`), the REST operations (`30-rest.md`), the access
rule of each field and the filter chain (`32-security.md`), the batch statements and indexes
(`20-persistence.md`), or the tests (`40-tests.md`). Does not write Java, schema files, `pom.xml`
or `application.yml` — the executor does, from this partial. Doesn't touch `.claude/rules/**`.
