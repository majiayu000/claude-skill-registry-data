---
name: rest-api-architect
description: >
  Designs the inbound REST adapter for an already-modeled use case — endpoints, DTOs,
  status codes, error map, pagination, idempotency, API versioning, inbound admission, and
  OpenAPI — into the `30-rest.md` partial. Use when the request involves exposing a use case via
  HTTP, designing an endpoint or controller, deciding status and error body, paginating a
  collection, applying `Idempotency-Key`, introducing a `/v2` or deprecating and retiring an API
  version, a rate limit or quota per client, a concurrency cap, a 429, or fixing the OpenAPI
  contract. Piece of the
  `/new-feature` pipeline: requires `10-domain.md` in the given folder and stops
  without it.
argument-hint: "[path to the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# REST API Architect

Designs **how the use case is exposed over HTTP**: what endpoints exist, what DTOs go
in and out, what status each result returns, what error body arises from each domain
exception, how the collection is paginated, and what OpenAPI has to document. What
`domain-modeling` left as an inbound port, this skill gives transport shape to.

**Entry rule: without `10-domain.md`, there's nothing to expose.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `10-domain.md` and treats them as
a contract. Without the domain partial, it stops and tells the caller to run
`/domain-modeling` — designing endpoints before the ports and exceptions exist produces
a contract that describes the screen, not the business.

**Exit rule: writes no code.** It emits `30-rest.md`. The controller, the DTOs, the
mapper, and the `ApiExceptionHandler` come from the executor agent, which reads the
partial and the exemplars in `templates/`. Inherits D15 —
`@.claude/decisions/0003-skill-domain-modeling.md` — and the inconsistency P7 flagged is
closed in `@.claude/decisions/0006-rest-api-architect-design.md`.

**Rule rule: rules don't live here.** Verb semantics, status table, `ProblemDetail`,
`traceId`, pagination, idempotency, and what must be annotated in OpenAPI are
`@.claude/rules/api-rest.md`. This skill applies them and cites them; it doesn't
reproduce them.

## How it's invoked

Two ways, and both matter: `/rest-api-architect` by hand, or chained by `/new-feature`
once that orchestrator exists. That's why it does **not** carry
`disable-model-invocation` — that field hides the skill from the model, and a skill the
model can't see is a skill the orchestrator can't call.

The guard against out-of-order firing isn't the frontmatter: it's the **entry rule**
above. Without the prior partial the skill stops and says what needs to run first.
Recorded in `@.claude/decisions/0007-pipeline-skills-invocation.md`.

## Why this isn't a subagent

It's a procedure whose step 3 goes back to asking the user what no prior spec fixes —
what endpoints the client actually needs, what collection grows without bound, what
`POST` touches money or an external system. A subagent doesn't see the conversation.

Pinned to `opus`: the partial is what the executor implements verbatim. A pinned model does not make this a subagent — the interview needs the conversation, and the pin holding for the rest of the turn keeps `/new-feature` on the model that designed it (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Boundary with neighboring skills

The split is by **moment and by artifact**:

| Piece | Acts when | Produces |
|---|---|---|
| `use-case-design` | Before the domain exists | `00-use-case.md` — boundary and canonical names |
| `domain-modeling` | After the parent spec | `10-domain.md` — aggregate, invariants, ports |
| **this skill** | After the domain partial, unless the `Trigger` names `inbound GraphQL adapter` alone | `30-rest.md` — including the schema requirements transport creates |
| `graphql-api-architect` | After this one, when the `Trigger` names a GraphQL adapter | `31-graphql.md` — the GraphQL shape of the same input ports |
| `persistence-architect` | After this one | `20-persistence.md` — schema, reading this partial's schema requirements |
| `test-architect` | After all of them | `40-tests.md` — pyramid, slices, data |

Doesn't collide with `test-architect`: this skill fixes the HTTP contract's **cases**
(status, `errorCode`, body shape); that one owns the **strategy** for testing the whole
use case. Different artifacts, different owners.

Doesn't collide with `gof-design-patterns`: that skill owns the catalog, this one decides
which row shapes the REST layer of the case being designed (step 8b). Outside a feature run,
a controller that already exists with a growing `if` chain is `/gof-design-patterns`, not this
skill.

## Procedure

1. **Read the specs.** `00-use-case.md` and `10-domain.md` from the folder in
   the target above. Without the second, stop. Extract: canonical names, inbound ports and
   signatures, the exception table with `errorCode`, and the rows of the component
   table marked `Detailed by: rest-api-architect`.

2. **Survey what already exists.** A resource may already have a controller, and the
   use case may just be a new endpoint. The REUSE state from the parent spec rules over
   intuition.

   ```bash
   grep -rln "@RestController" --include='*.java' src/ 2>/dev/null
   # The project's versioning setup — none yet means this is the first REST case (step 7b)
   grep -rln "configureApiVersioning" --include='*.java' src/ 2>/dev/null
   # The project's admission setup — none yet, with an `Admission` row, means step 7c writes it
   grep -rln "AdmissionProperties" --include='*.java' src/ 2>/dev/null
   ```

   The inbound adapter's package isn't the same across every blueprint (`adapter/in/rest`
   in one, `infrastructure/rest` in another): discover it via `@RestController` or via
   `packages.map`, never from a path written from memory. An `ls` against a path this
   project doesn't have returns empty and passes for "no controller yet".

3. **Interview — only what the specs don't fix.** `AskUserQuestion`, at most 4
   questions per call and **never fewer than 2 real options per question**: one option
   isn't a question — decide it and record the decision in the partial, since the runtime
   rejects the whole batch over a single one (`@CLAUDE.md` § Known pitfalls). Don't re-ask
   what `00-use-case.md` or `10-domain.md` already answered.

   | Axis | Decides |
   |---|---|
   | What operations the client needs beyond the use case's own | Whether there's a read `GET`, and how many endpoints come out of this |
   | Does the collection grow without bound | Whether it's paginated — and it is, unless proven otherwise |
   | Does the `POST` create a resource, move money, or touch an external system | Whether `Idempotency-Key` is required |
   | Is there concurrent writing on the same resource | Whether `ETag` + `If-Match` come in (412 and 428) |
   | Is the resource's existence sensitive information | 404 instead of 403, for the whole resource |
   | Is the client internal or public | Weight of `operationId` stability |
   | Does this case change an existing endpoint in a way `@.claude/rules/api-rest.md` § Versioning calls breaking | A mapping at the next version beside the old one, and whether the old version is deprecated now — step 7b |

4. **Fix the endpoints.** One per line: method, the public path a client calls
   (`/api/v1/users`), the `version` its mapping declares (`1+` for a new endpoint), stable
   `operationId`, the inbound port it serves, success status. The controller's mapping carries
   the resource alone; the `/api/v{version}` prefix is step 7b's configuration. Resources and verbs per
   `@.claude/rules/api-rest.md`; class names per `@.claude/rules/naming.md`. An
   endpoint with no inbound port behind it doesn't get written — it's a guessed
   contract. OpenAPI documentation for each operation (`@Operation`, every
   `@ApiResponse`, `@Parameter` with examples, request body example) is extracted into
   its own composed annotation, suffix `OpenApiDocs` — one per operation — shape in
   `templates/OpenApiDocs.java.example`. `@Tag` and the composed annotations go on a
   `<Resource>Api` contract interface (`templates/Api.java.example`) **alone** — no
   Spring mapping or binding annotation there. Those go on the controller that
   implements it (`templates/Controller.java.example`): `@PostMapping`/`@GetMapping`,
   `@Valid`, `@RequestBody`, `@PathVariable`, and any Spring Data Web resolution
   annotation. The split is by kind — documentation on the interface, everything that
   makes the endpoint run on the implementation — not by which file has room.

5. **Fix the DTOs.** Input and output, field by field. DTO validation is **shape**
   only; business rule stays in the aggregate and comes out as 422. No domain type in
   the public signature, no aggregate serialized. The translation in the project's mapper
   mechanism (`@.claude/rules/mapping.md` — `templates/RestMapper.java.example` or
   `templates/RestMapStructMapper.java.example`); the partial never names which.

   **Apply masking, and re-derive it here instead of trusting the previous partial.**
   Every DTO field gets walked through `@.claude/rules/logging.md` § Masking candidates —
   by type and by name — not only the ones `10-domain.md` listed. A match gets
   `@MaskSensitiveData(maskedType = MaskedType.<X>)` and the DTO class implements
   `LogMask`. Where this partial finds a match the domain partial missed, it masks it and
   says so in the divergence line; where it finds a DTO field with no domain counterpart at
   all (a transport-only field), the derivation still applies.

   Two links in series is what failed: `10-domain.md` didn't flag, so nothing was masked,
   and a CPF was logged raw from the first use case onward. The derivation is cheap and the
   rule is the same list on both ends — running it twice costs a pass over the field list.

   This isn't optional because it "looks fine without it": `GlobalHttpMethodLogAspect` logs
   every request and response DTO by default (opt-out, not opt-in) — a DTO that doesn't
   implement `LogMask` logs the field raw the moment the endpoint runs.

   **Also check the DTOs that already exist.** A use case that touches an endpoint whose
   DTOs were written before this rule existed inherits their leaks: run the same derivation
   over them and report each unmasked match in `## Impact on approved use cases`, even when
   this use case doesn't otherwise change them.

6. **Fix the error map.** Each exception from `10-domain.md` to its status and its
   `errorCode`, plus the structural errors that don't come from the domain (bean
   validation, unreadable body), and the 500 with `traceId`. This table is the source
   of block 5 — an exception that doesn't appear here won't have a test.

   **Cross-check shape validation against domain invariants before listing both.** For
   each row that comes from a domain invariant (not idempotency, not a structural
   error), check whether step 5 already put a bean-validation annotation on the same
   DTO field. If it did, the bean-validation 400 fires first and the domain's
   `errorCode` is unreachable through this endpoint — mark the row accordingly (e.g.
   "unreachable via this endpoint: intercepted by `@NotBlank` on `<field>`") instead of
   listing it as if it were a scenario a contract test can actually hit. Don't write the
   two as parallel, equally-reachable cases — a test written against the domain row
   alone will assert a 422 that never happens.

7. **Fix pagination and idempotency.** Offset by default; cursor only when volume or
   mutation of the set demands it. If the `POST` requires `Idempotency-Key`, declare
   both halves: the structural one stays in the adapter
   (`templates/IdempotencyKeyInterceptor.java.example`), and the key's table **is
   handed off to `persistence-architect`** — name it in the partial, don't model it
   here. Shape reference for that other half:
   `@.claude/skills/persistence-architect/templates/IdempotencyKeyTable.sql.example`,
   `.../IdempotencyKeyStore.java.example`, and `.../IdempotentExecution.java.example`.
   The transaction shape is fixed by `@.claude/rules/api-rest.md` § Idempotency — don't
   reopen it per use case: the controller calls `IdempotentExecution`, the command
   carries no key, and `10-domain.md`'s use case signature doesn't change for it.

   **Every `Idempotency-Key` endpoint, including the first one in the project, uses
   `@Idempotent` + `IdempotencyAspect`** (`templates/IdempotencyAspect.java.example`,
   `templates/IdempotencyKeyInterceptor.java.example`'s annotation-based variant,
   `Controller.java.example`): it reuses the same `IdempotentExecution`/`IdempotencyKeyPort`
   — no second port, no second vocabulary — and needs zero code in the controller beyond
   the annotation. When `idempotency_keys` is **NEW** in the project (first time this
   folder decided it's needed), this same pass names `IdempotencyAspect` in the
   dependencies list alongside the table — there is no separate manual path to fall back
   to for a lone first endpoint. (Decision `.claude/decisions/0044-idempotent-first-endpoint.md`:
   the by-hand call this replaced cost ~30 lines of controller-side response
   (de)serialization per endpoint, code the aspect already generalizes, for a cost —
   reflection-based response-type lookup and a body-index argument — that's paid once
   per project regardless of endpoint count.)

   **Write the schema requirements down.** Block 4 closes with a `Schema requirements`
   list: every table or column this transport needs that the domain didn't model — the
   idempotency key table, first of all — or "none". `persistence-architect` runs after
   this skill and reads that list in its first pass; a requirement left in prose here is a
   second persistence pass later.
7b. **Decide or inherit the versioning setup — § 7.** `@.claude/rules/api-rest.md` §
   Versioning decides the strategy; nothing here reopens it. Step 2 found no
   `configureApiVersioning` → this is the project's first REST case: § 7 writes the project
   setup as NEW (`templates/ApiVersioningConfig.java.example`,
   `templates/ApiVersionObservationConvention.java.example`), supported versions `1`, no
   deprecation, and the unsupported-version row in blocks 3 and 5. Found → § 7 reads
   `inherited from UC-NNN`, naming the case whose partial wrote it.

   Then the case's own changes, from step 3's breaking-change axis — each a row of § 7 and a
   CHANGE of `ApiVersioningConfig`:

   | Change | Asked | Written |
   |---|---|---|
   | New version | Only when a change is breaking | The next major in the supported list; a mapping at `<N>+` for each endpoint that breaks, beside the old one; every other endpoint untouched — it reaches the new version through its baseline |
   | Deprecation | Whether the old version is deprecated now, and its sunset date — asked, never assumed. The window is the user's, justified by the measured use of that version (`api.version`) and the consumers known to call it | `Deprecation` and `Sunset` dates and the migration notes' link; the deprecated-version case in block 5 |
   | Sunset | Only when a recorded `Sunset` date has passed | The version out of the supported list and its mappings deleted, in the same change |

   A breaking change with no new version is a divergence to report, never a silent edit of the
   `1+` mapping: every client of v1 would break at once.
7c. **Decide or inherit the admission setup — § 8.** Only when `00-use-case.md`'s
   `Admission` row is not `none` (a missing row reads as `none`): no row, § 8 reads `none` and
   nothing below runs. A limit is never proposed here — `@.claude/rules/inbound-admission.md` §
   When a limit exists. The norm decides the mechanism; nothing here reopens it.

   Step 2 found no `AdmissionProperties` → this is the project's first case with a limit: § 8
   writes the project setup as NEW (`templates/AdmissionConfig.java.example`,
   `templates/application-admission.yml.example`), asking only what no file fixes:

   | Question | Asked | Written |
   |---|---|---|
   | Where the quota is enforced | Only when the row names a quota — `in the application` or `at the edge`, and which edge | `application`, or `edge: <name>`: then no limiter is written, the number and key the edge enforces are recorded, and the IT cannot prove them — said in § 8 |
   | Replicas | How many instances serve the endpoint in production | The count, and each quota divided by it, rounded up — the per-replica number the configuration holds |
   | Wait on 503 | Only when the row names a cap | The `Retry-After` of a full cap, with its reason |

   The caller's key is never asked: it follows from the case's `Access` row and the norm's §
   The caller — the principal, the API key's id, or for a public endpoint the client address,
   through the forwarded headers only when the root `CLAUDE.md`'s `**Transport:` paragraph names
   trusted proxies. Found → § 8 reads `inherited from UC-NNN`; a row the setup lacks (the first
   quota after a cap-only setup) is added as a CHANGE.

   Then the case's own limits, each a row of § 8: a quota names its limiter (the case slug) on
   the handler method through `@InboundQuota`, the per-replica number and the window; a cap names
   its `inbound-<slug>` bulkhead, its size below the scarcest resource the case holds and the reason. Block 3
   gains the 429 `RATE_LIMITED` or the 503 `SERVICE_BUSY` row, block 5 the case that proves it,
   and block 4's dependencies the resilience library when the build does not declare it.

8. **Fix the dependencies.** springdoc, tracing bridge, and validation. **Read `pom.xml`
   first**: a dependency already declared there keeps its version, and nothing is
   resolved. Never a web search for a version. springdoc's
   version **isn't managed by the Spring Boot BOM**: when it's absent, resolve it at runtime and confirm
   compatibility with the project's Boot major —
   `references/best-practices-links.md` § Resolving the springdoc version. No network,
   ask. Never from memory (`@CLAUDE.md`, invariant 8). You don't edit `pom.xml`: you
   declare, the executor applies. With § 8 not `none` and the build lacking them:
   `io.github.resilience4j:resilience4j-spring-boot4` (the `<release>` of its
   `maven-metadata.xml`, read now — not managed by the Boot parent), and, managed by the parent,
   `com.github.ben-manes.caffeine:caffeine` for the setup and `spring-boot-starter-aspectj` for a
   cap. A build that already declares Resilience4j for an outbound call keeps it — one
   resilience library per project.

8b. **Decide the design patterns of this layer.** Run
   `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the controller,
   mappers and handlers this case adds, against the specs and what step 2 surveyed. A
   controller seldom earns one — the usual row is a translation repeated across resources.
   The answer goes into `## Design patterns` — `none` when nothing matches, and absence is
   not `none`.

9. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/30-rest.md`, from
   `templates/rest-spec.md.example`. Eight numbered blocks plus `## Design patterns`, all mandatory.

10. **Report and stop.** File path, divergences from `10-domain.md`, what was handed
    off to another owner (idempotency table), and what's left for the folder to be
    complete (`40-tests.md`). Don't invoke anyone.

## Personal data leaving in a response body

Before the partial is written, run `@.claude/rules/personal-data.md` § How to verify grep 1 against
the response DTOs just designed, and read every hit against the derivation in
`@.claude/rules/logging.md` § Masking candidates — the value-object catalog plus the name list,
one owner, not re-derived here.

Each matching field gets one of three answers in the partial's `Personal data` block: the
**full value** (the receiver's whole purpose needs it, with the receiver named and the reason
given), a **reduced form** (an id, a hash, the last digits), or a **reference** the caller
resolves under its own authorization. A full value with no record does not consolidate.

`@MaskSensitiveData` on the DTO is not the answer to this. It covers the log line; the block
covers the body that leaves the process. A field masked in the logs and returned in clear was
never protected — it was protected in the one place someone happened to look.

## What the partial contains

Ten blocks. A block with no content is written as "none" — deleting it hides a
question nobody asked.

| Block | Fixes | Shape exemplar |
|---|---|---|
| Endpoints | Method, path, `operationId`, port, success status | `Controller.java.example` implementing `Api.java.example` |
| OpenAPI docs | `@Tag` + `@Operation`, `@ApiResponse` per status, `@Parameter` with examples, request body example — one composed `...OpenApiDocs` annotation per operation, declared on the contract interface alone (no mapping/binding annotation there — those are on the controller) | `Api.java.example` · `OpenApiDocs.java.example` |
| DTOs | Input and output, fields, shape validation, translation, `@MaskSensitiveData` on sensitive fields | `Dtos.java.example` · `RestMapper.java.example` · `RestMapStructMapper.java.example` |
| Error map | Exception → status → `errorCode`; `violations` and `traceId` | `ApiExceptionHandler.java.example` · `error-responses.json.example` |
| Pagination, idempotency and dependencies | Mode and limits, both halves of the key, artifacts to add | `PageResponse.java.example` · `page-response.json.example` · `PageCriteria.java.example` (the port's own pagination type — `Pageable` never crosses it) · `IdempotencyKeyInterceptor.java.example` · `IdempotencyAspect.java.example` (every `@Idempotent` endpoint, first one included) |
| Contract test cases | Status, `errorCode`, and body shape per scenario | `@.claude/skills/test-architect/templates/ControllerTest.java.example` |
| Personal data | Every field of a **response** body matching `@.claude/rules/logging.md` § Masking candidates, with the form chosen — full value, reduced, or a reference — and, for a full value, the receiver and the reason. `@.claude/rules/personal-data.md` § In transit calls that the `Recorded decision`, and `@MaskSensitiveData` on the DTO is not it: masking covers the log, this covers the body that leaves the process. `none` when there is none, and absence is not `none` | `@.claude/rules/personal-data.md` § How to verify, grep 1 |
| Versioning | The project setup — NEW in the first REST case, `inherited from UC-NNN` after — and this case's new version, deprecation or sunset, with dates and the justification of the window | `ApiVersioningConfig.java.example` · `ApiVersionObservationConvention.java.example` |
| Admission | `none` without an `Admission` row. Otherwise the project setup — NEW in the first case with a limit, `inherited from UC-NNN` after — where the quota is enforced, replicas, the caller's key, the 503 wait; and this case's quota (limiter, per-replica number, window) and cap (`inbound-<slug>`, size, reason) | `AdmissionConfig.java.example` · `application-admission.yml.example` · `ApiExceptionHandler.java.example` |
| Design patterns | Each pattern the controller, mappers or handlers adopt, with its force, its classes and the "When not" checked — step 8b. `none` when none | `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use |

The exemplars in `templates/` are a **shape reference**, not files to copy. It's the
executor agent that reads them when generating code.

The mapper comes in two exemplars — `RestMapper.java.example`, and `RestMapStructMapper.java.example` beside it — because the mechanism is the project's, not this partial's: the partial says what maps to what, and the executor writes it in the mechanism the root `CLAUDE.md`'s `**Mappers:` paragraph names (`@.claude/rules/mapping.md`).

The contract test exemplar does **not** live here: test-code shape has a single owner,
and it's `test-architect`. This skill fixes the cases; the shape of the class that
verifies them is at
`@.claude/skills/test-architect/templates/ControllerTest.java.example`.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. Writes inside the
use case folder and nothing else; a controller or DTO written under `src/` is refused with
exit 2.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `10-domain.md`
(mandatory — stops without the second), `@.claude/rules/api-rest.md`,
`@.claude/rules/architecture-ddd.md` (Adapters and Composition sections),
`@.claude/rules/naming.md`, `@.claude/rules/error-handling.md`,
`@.claude/rules/code-quality.md`, `@.claude/rules/logging.md` (masking mechanism for
DTO fields `10-domain.md` flagged sensitive), `@.claude/rules/observability.md` § Metrics
(the bound on the per-version tag), the `30-rest.md` that wrote the versioning setup when
an earlier case did, `@.claude/rules/inbound-admission.md` and the partial that wrote the
admission setup when the case has an `Admission` row, the root `CLAUDE.md`'s `**Transport:`
paragraph (trusted proxies, for a public endpoint's key), and the active blueprint's
`packages.map`. Also reads
`20-persistence.md` when it exists (a resumed or hand-run case) — the table's expected
volume decides offset or cursor. In `/new-feature` this skill runs first, so the volume
comes from its own interview ("does the collection grow without bound") and is written in
block 4, where `persistence-architect` reads it instead of asking again.

**Writes** `docs/use-cases/UC-NNN-<slug>/30-rest.md`. Only that file.

**Writes no Java code.** The controller, the DTOs, the mapper, the interceptor, the
`ApiExceptionHandler`, and the contract tests come from the executor agent. It doesn't
edit `pom.xml` nor `.github/workflows/**` — the `openapi.json` diff job belongs to
`project-bootstrap`.

**Doesn't decide** the use case boundary (`00-use-case.md`), the domain model
(`10-domain.md`), the schema or the idempotency key table (`20-persistence.md`), nor
the test strategy (`40-tests.md`). Doesn't touch `.claude/rules/**`.

**Doesn't collide with `domain-modeling`**: that one declares the inbound port, this
one says over which HTTP it's called. The port's signature belongs to the other one; if
it needs to change, report the divergence instead of rewriting it.
