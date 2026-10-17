---
name: test-architect
description: >
  Designs the tests for an already-modeled use case — what test exists at what level,
  what data, what error cases — into the `40-tests.md` partial, and installs the
  architecture tests in a project that doesn't yet have them. Use when the request
  involves writing or designing tests, coverage, ArchUnit, boundary tests, integration
  tests, or "this is missing tests". Piece of the `/new-feature` pipeline: in design
  mode requires `10-domain.md` in the given folder and stops without it.
argument-hint: "[path to the UC-NNN-<slug> folder, or empty to install ArchUnit]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Agent
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# Test Architect

Two things, and the argument decides which:

| Mode | When | Produces |
|---|---|---|
| **design** | the target above is a `UC-NNN-<slug>` folder | `docs/use-cases/UC-NNN-<slug>/40-tests.md` |
| **setup** | the target above is empty | ArchUnit installed in the project (version in the POM, `ArchitectureTest.java` with the translated packages) and the coverage gate wired up (JaCoCo's `check` execution) — done by delegating to the `archunit-installer` agent |

They're not two disguised pieces: they share the rule, the vocabulary, and the
exemplars. Setup mode runs **once per project**; design mode runs once per use case.

**Design mode entry rule: without `10-domain.md`, there's nothing to test.** Reads
`00-use-case.md` and `10-domain.md` and treats them as a contract. Without the
domain partial, it stops and tells the caller to run `/domain-modeling` — designing
tests before the invariants exist produces tests for the form, not the business.

**Exit rule: writes no test code.** Design mode emits `40-tests.md`; the files in
`src/test/**` come from the executor agent, which reads the partial and the exemplars
in `templates/`. Inherits D15 — `@.claude/decisions/0003-skill-domain-modeling.md`.

Setup mode is the declared exception, and the only one: it produces
`ArchitectureTest.java` and two entries in the POM — the ArchUnit dependency and
JaCoCo's `check` execution — by delegating to the `archunit-installer` agent. It isn't
code for a use case — it's whole-project verification infrastructure, which no partial
describes, and running it inline would pin the whole session's context to a `curl` call
and up to three `./mvnw` builds it doesn't need to see. Split recorded in
`@.claude/decisions/0030-archunit-installer-split.md`.

**Rule rule: rules don't live here.** Pyramid, slices, doubles, names, data, database
engine, and coverage are `@.claude/rules/testing.md`. This piece applies them and cites
them; it doesn't reproduce them.

## How it's invoked

Two ways, and both matter: `/test-architect` by hand, or chained by `/new-feature` once
that orchestrator exists. That's why it does **not** carry
`disable-model-invocation` — that field hides the piece from the model, and what the
model can't see the orchestrator can't call.

The guard against out-of-order firing isn't the frontmatter: it's the entry rule above.
Without the domain partial, design mode stops and says what needs to run first.
Recorded in `@.claude/decisions/0007-pipeline-skills-invocation.md`.

## Why design mode isn't a subagent, and setup mode is

Step 3 of design mode goes back to asking the user what no prior partial fixes — which
error scenarios deserve their own test, what data represents the real case. A subagent
doesn't see the conversation, so design mode stays inline. Recorded in
`@.claude/decisions/0008-testing-rule-and-design.md`.

Setup mode has the opposite shape — no interview, purely mechanical, and its own Bash
output (a Maven Central lookup, up to three `./mvnw` builds) is the kind of thing that's
cheap to isolate and expensive to keep. It delegates to the `archunit-installer` agent.
Recorded in `@.claude/decisions/0030-archunit-installer-split.md`.

Pinned to `opus`: the partial is what the executor implements verbatim. A pinned model does not make this a subagent — the interview needs the conversation, and the pin holding for the rest of the turn keeps `/new-feature` on the model that designed it (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Boundary with neighboring pieces

| Piece | Acts when | Produces |
|---|---|---|
| `use-case-design` | Before the domain exists | `00-use-case.md` |
| `domain-modeling` | After the parent spec | `10-domain.md` — invariants and exceptions |
| `persistence-architect` | After the domain | `20-persistence.md` — queries and indexes to check |
| `rest-api-architect` | In parallel | `30-rest.md` — **the HTTP contract's cases** |
| **this piece** | After all of them | `40-tests.md` |

The single point of contact, and it must be respected: the HTTP contract's cases —
status, error code, body shape — belong to `30-rest.md` (D16). This partial **cites
them and doesn't rewrite them**; what it adds is the level they run at, the data, and
what's left to cover outside of transport.

## Procedure — design mode

1. **Read the partials.** `00-use-case.md` and `10-domain.md` are mandatory;
   without the second, stop. Read `20-persistence.md`, `30-rest.md`, `31-graphql.md`, `28-http-client.md`,
   `29-ai.md`, `23-search.md`, `35-jobs.md` and `22-cache.md` when they exist. Extract: each invariant and its matching exception, each port, each query,
   the HTTP contract's case table, and each job of `35-jobs.md` § 1 — a job is tested through
   the inbound port it calls, never by waiting for a scheduler, and the test profile's
   switches (`@.claude/rules/scheduling.md` § Triggers) get one context test proving no
   trigger runs under it.

   **`32-security.md`, when it exists, fixes cases this partial must test — all of § 10.**
   Every protected endpoint is proven three ways (no credential, without the authority, with
   it) and every public one with no credential, through the real filter chain
   (`@.claude/rules/authorization.md` § Tests) — shape in `templates/SecuredControllerTest.java.example`,
   never filters switched off. Every ownership row gets a use-case unit test with another
   actor, asserting the not-found outcome. The security test starters go into § 5 when the
   build does not declare them yet — the ones the Initializr's `security` and
   `oauth2-resource-server` ids add for the project's Boot version; without them `jwt()` and
   `@WithMockUser` have no MockMvc integration.

   **`31-graphql.md`, when it exists, fixes cases this partial must test — all of § 10, at the level
   each row names** (`@.claude/rules/api-graphql.md` § Tests). The mapping, the errors, the page
   ceiling, the cursor round trip and **one batch port call per request with every parent key**
   in a `@GraphQlTest` slice with the input ports mocked and `@WithMockUser` — the slice has no
   filter chain and no method security, so no access case goes there
   (`templates/GraphQlControllerTest.java.example`). Access, the demand limits and introspection
   over HTTP through the real server and chain, with `HttpGraphQlTester` and the `JwtDecoder`
   replaced so fixed bearer strings decode to fixed tokens; a limit lowered for that class only when
   the schema cannot reach it otherwise (`templates/GraphQlHttpIT.java.example`). The schema
   compatibility test once per project, its snapshot at `src/test/graphql/` — outside the test
   classpath (`templates/GraphQlSchemaCompatibilityTest.java.example`). Every case asserts the
   error's classification, not only that there are errors. `spring-boot-starter-graphql-test` goes
   into § 5 when the build does not declare it — managed by the Boot parent.

   **`25-messaging.md`, when it exists, adds one test: the AsyncAPI contract gate** — the served
   document at `/springwolf/docs` against the snapshot committed at `src/test/asyncapi/`, outside
   the test classpath, once per project (`templates/AsyncApiContractIT.java.example`;
   `@.claude/rules/messaging.md` § Contract documentation). It runs in `verify` like any `IT`, needs
   no broker (`spring.kafka.listener.auto-startup=false`), and fails on the first run naming the copy
   that creates the snapshot. The case is written in § 3 with the operation ids § 1 of the messaging
   partial derived, so a reader sees which names are contract. It adds nothing to § 5: Springwolf is
   the messaging partial's declared dependency, and the test uses `MockMvc`, the Jackson 3
   `JsonMapper` and AssertJ the project already has. A case-level test of the adapters against a real
   broker is a separate row and stays where it was.

   **`28-http-client.md`, when it exists, fixes cases this partial must test — all of § 9.**
   Every outbound adapter is tested through its port against a real socket, never
   `MockRestServiceServer` (`@.claude/rules/http-client.md` § Tests) — shape in
   `templates/HttpClientAdapterIT.java.example`: one `IT` class per remote system, the attempt
   count asserted on the stub server, the family and `errorCode` asserted on the exception, and
   the read timeout lowered only for that class. `wiremock-spring-boot` goes into § 5 when the
   build does not declare it — not managed by the Boot parent, so its version is the `<release>`
   of its `maven-metadata.xml`, read at design time; never from memory.

   **The document family, when `20-persistence.md` stores an aggregate in MongoDB:** the
   persistence integration test runs against a single-node replica set
   (`templates/MongoPersistenceIT.java.example` — `.withReplicaSet()`, the image through
   `DockerImageName.parse`), imports the schema initializer, and proves that every unique index of
   § 1 exists, that a duplicate business key is a conflict, that an update raises the version, that
   an older shape is upcast, and that a failed transaction leaves nothing written.

   **An audited aggregate, when `20-persistence.md` § Audit is not `none`:** an integration test
   against the real engine that **commits** — `@SpringBootTest` with `TransactionTemplate`, never a
   rolled-back `@DataJpaTest`, which sees no history and passes for the wrong reason
   (`templates/AuditHistoryIT.java.example`). Cases, each only where § Audit has the item: the
   stamps on the live row with `created` kept on update; for `history`, create, update and delete
   read back through the read port, newest first, each with its actor; a job's or consumer's actor
   as `system:<name>`; a write with no authentication failing; each bulk write § Audit lists
   leaving no revision; the prune keeping the current version. The context starting is itself the
   check that the `_aud` migrations match the mapping (`ddl-auto: validate`).

   **`23-search.md`, when it exists, fixes cases this partial must test** — against the real engine
   (`templates/SearchIndexIT.java.example`, the same image and tag as the compose service): the
   alias exists at startup, each § 3 query finds by its match fields and pages by its cursor, a
   tombstone is never returned; for an indexer case, an older event is acknowledged as stale and a
   delete followed by a late write stays deleted; for a rebuild case, an event written during the
   rebuild survives the alias swap. Refresh only in the test's fixture.

   **`29-ai.md`, when it exists, fixes cases this partial must test — all of § 8, at the level
   each row names.** No case calls a real model (`@.claude/rules/ai.md` § Tests). Answers: through
   the adapter with a scripted stub `ChatModel` that records every prompt — never a Mockito mock,
   which answers `null` to the schema-validation retry nobody stubbed — and the production
   `ChatClient` bean method around it (`templates/AiAdapterContractTest.java.example`). Wiring:
   against WireMock speaking the provider's protocol, the starter's base URL pointed at it, the
   port's timeout and the SDK's retries lowered for that class only, the attempt count asserted
   (`templates/AiProviderIT.java.example`). A store: against the real `pgvector/pgvector` engine
   through the project's migration, with a `@Primary` stub `EmbeddingModel` returning fixed vectors
   of the store's real dimension count (`templates/VectorStoreIT.java.example`). `wiremock-spring-boot`
   goes into § 5 as for `28-http-client.md`; the pgvector image tag is pinned like every other
   container's, and `ArchHook.java compose` compares it with the compose file's.

   **`22-cache.md`, when it exists, fixes cases this partial must test — three per cached read
   of § 1.** Through the port, against the real provider (a Redis container when § 2 chose
   Redis — `@ServiceConnection` on a `redis` container, never the in-memory map provider): a
   second read does not reach the delegate; every write § 4 routes through the port evicts, and
   only after the commit; two callers never share an entry when the key names the caller
   (`@.claude/rules/caching.md` § Tests) — shape in `templates/CachedAdapterIT.java.example`.
   Caching stays on in every test, and the caches are cleared between tests that share a context.
   The Redis image tag is pinned like every other container's, and `ArchHook.java compose`
   compares it with the compose file's.

   **`30-rest.md` § 8 or `31-graphql.md` § 6, when either states a limit, fixes the admission
   cases** — through the real server and chain, never a web slice: the bulkhead aspect is not part
   of one. A quota: spent → 429 with `Retry-After` and `RATE_LIMITED`, another caller keeps theirs,
   an anonymous request answers 401 and spends nothing. A cap: full → 503 with `Retry-After`,
   `SERVICE_BUSY` and `traceId`, and on an `@Idempotent` handler the rejected call claims no key.
   GraphQL: a spent quota is HTTP 429 before any port runs, a full cap the root field `null` with
   `SERVICE_BUSY` (`@.claude/rules/inbound-admission.md` § Tests) — shape in
   `templates/AdmissionIT.java.example`, with the limits lowered for that class only. With `Quota
   enforced: edge` the quota cases are not written here: the edge is not in the test.

2. **Survey what already exists.**

   ```bash
   ls src/test/java 2>/dev/null
   grep -rln "@SpringBootTest\|@DataJpaTest\|@WebMvcTest" --include='*.java' src/test/ 2>/dev/null
   grep -rL '@ActiveProfiles("test")' $(grep -rl "@SpringBootTest" --include='*.java' src/test/ 2>/dev/null) 2>/dev/null
   ```

   The last command lists every `@SpringBootTest` that runs without the test profile
   (`@.claude/rules/testing.md` § Slices and context). Each one becomes a change in this
   partial — `@ActiveProfiles("test")` added — in § Impact on approved use cases when an
   approved case wrote it, in § 1 otherwise. The generator's own `*ApplicationTests` is
   usually the first,
   and the case that adds a project's first job is usually the one that finds them.

   A data factory that already exists gets reused. Two factories for the same
   aggregate is exactly the duplication the rule forbids.

3. **Interview — only what the partials don't fix.** `AskUserQuestion`, at most 4
   questions per call and **never fewer than 2 real options per question**: one option
   isn't a question — decide it and record the decision in the partial, since the runtime
   rejects the whole batch over a single one (`@CLAUDE.md` § Known pitfalls).

   | Axis | Decides |
   |---|---|
   | What error scenarios deserve their own test | An invariant with no named test is an invariant nobody guarantees |
   | What data represents this business's real case | Distinguishes a test that documents from a test that just pads |
   | Is there concurrency or time in the use case | Whether a fixed clock and an optimistic-locking test come in |
   | Does the use case touch an external system | Whether there's a double, and at which boundary |

4. **Distribute by level.** Each behavior at **one** level, per the pyramid table in
   `@.claude/rules/testing.md`. An aggregate invariant is always a domain unit test.
   Mapping and SQL are always integration. A behavior appearing at two levels is a bug
   in the distribution, not thoroughness.

   **A unique business key requires its own integration test.** For each `UNIQUE` that
   `20-persistence.md` declares over a business key, name a test in the adapter that
   saves the same value twice and **asserts the domain exception's `errorCode`, not
   just its type**. It's the only test that tells apart an adapter that translates the
   violation from one that lets it leak: without a flush inside the adapter the
   exception is born at commit, the client gets a 500 instead of a 409, and a test that
   only checks the type still passes
   (`@.claude/rules/persistence.md` § Boundary). Exemplar:
   `templates/PersistenceIT.java.example`.

   **A DTO field the masking derivation matches requires its own masking test** — derive
   it from `@.claude/rules/logging.md` § Masking candidates, don't wait for `30-rest.md` to
   have marked it. A unit test that calls the DTO's masked `toString()` (or serializes it
   the way `GlobalHttpMethodLogAspect` would) and asserts the raw value is absent. Name it
   alongside the DTO's own test class, not as a separate file.

   The architecture test now covers the structural half — a DTO with a matching field
   implements `LogMask` and marks the field (§ Masking candidates, installed by setup
   mode). This test covers what the structural one cannot: that the mask actually hides the
   value. Both, not one: an annotation with the wrong `maskedType` passes ArchUnit and still
   logs a readable CPF.

5. **Name each test.** Class and method per the rule's naming conventions, with the
   `IT` suffix on integration ones — without it failsafe doesn't run them and `verify`
   exits 0 without executing them. Before naming, group the cases of each class: those
   that differ only in their input — every malformed value a parser rejects, every
   route a filter lets through — are one parameterized method, listed once in § 2 with
   its inputs (`@.claude/rules/testing.md` § Names and shape). Shape:
   `templates/DomainTest.java.example` for a value object,
   `templates/IdempotencyKeyInterceptorTest.java.example` for an adapter component.

6. **Fix the data and the doubles.** Which factory, which fields matter in the
   scenario, which port gets substituted and with what value. Fixed clock wherever
   there's time involved.

   **Name the test dependencies** in § 5 of the partial: every library a test uses that
   the build does not declare yet — Awaitility for a test that waits on something
   asynchronous (`@.claude/rules/testing.md` § Asynchronous effects), a Testcontainers
   module per engine or broker started. Check the build file first; a dependency already
   there is not repeated. The executor adds exactly these and nothing else.

7. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/40-tests.md`, from
   `templates/test-spec.md.example`. Five blocks, all mandatory.

8. **Report and stop.** File path, invariants from `10-domain.md` left without a
   named test (if any, it's a gap to close before implementing), and what's left for
   the folder to be complete. Don't invoke anyone.

## Procedure — setup mode (install ArchUnit and wire up the coverage gate)

Run once business classes already exist. Not before: in a freshly generated project,
every rule about zero classes fails vacuously, and the build is born red for having
nothing to check. That's why `project-bootstrap` doesn't do it.

The coverage gate comes in through the same door and for the same reason: over zero
classes it either passes vacuously, which proves nothing, or breaks the build for
having nothing to measure. `project-bootstrap` leaves JaCoCo instrumenting and
reporting, without the `check` execution — this mode is the one that adds it. Record:
`@.claude/decisions/0011-bootstrap-without-business-code.md`.

**This mode delegates its execution.** Invoke the `archunit-installer` agent with the
project root. It resolves the ArchUnit version, writes `ArchitectureTest.java`,
translates the packages, wires the JaCoCo `check` execution, runs the builds, and pins
the Testcontainers image tag — all isolated from this conversation, since none of it
needs an interview. Reasoning and full procedure:
`@.claude/agents/archunit-installer.md`. Record of the split:
`@.claude/decisions/0030-archunit-installer-split.md`.

Read the agent's returned summary and report it as-is. If it flags a Testcontainers
tag mismatch against `docker-compose.yml`, **report it with the `/docker-architect`
invocation that fixes it** and stop — don't invoke that skill from here. The installer agent
deliberately doesn't touch that file (single owner), and `ArchHook.java guard` refuses a
`build`-class call while this skill's phase is open.

The mismatch is also checked mechanically, so it doesn't depend on the agent noticing:
`java .claude/hooks/ArchHook.java compose` compares every `image:` of the compose file
with every `DockerImageName.parse` under `src/test`, and `/arch-doctor` folds the same
check in. Run it after this mode pins the tag.

## What the partial contains

Five blocks. A block with no content is written as "none" — deleting it hides a
question nobody asked.

| Block | Fixes | Shape exemplar |
|---|---|---|
| Distribution by level | Each behavior, the level it's tested at, and why | `DomainTest.java.example` |
| Cases per test class | Class name, each method's name, what it asserts | `UseCaseTest.java.example` · `ControllerTest.java.example` · `SecuredControllerTest.java.example` (when `32-security.md` exists) · `GraphQlControllerTest.java.example`, `GraphQlHttpIT.java.example`, `GraphQlSchemaCompatibilityTest.java.example` (when `31-graphql.md` exists) · `AsyncApiContractIT.java.example` (when `25-messaging.md` exists) · `HttpClientAdapterIT.java.example` (when `28-http-client.md` exists) · `CachedAdapterIT.java.example` (when `22-cache.md` exists) · `AiAdapterContractTest.java.example`, `AiProviderIT.java.example`, `VectorStoreIT.java.example` (when `29-ai.md` exists) · `SearchIndexIT.java.example` (when `23-search.md` exists) · `PersistenceIT.java.example`, or `MongoPersistenceIT.java.example` for an aggregate of the document family · `AuditHistoryIT.java.example` (when `20-persistence.md` § Audit is not `none`) · `IdempotencyKeyInterceptorTest.java.example` (when `30-rest.md` requires `Idempotency-Key`) · `AdmissionIT.java.example` (when `30-rest.md` § 8 or `31-graphql.md` § 6 states a limit) |
| Data and doubles | Factories, meaningful fields, substituted ports, clock | `TestFixtures.java.example` |
| Coverage and gaps | Invariants with no test, and what's deliberately left uncovered | `@.claude/rules/testing.md` § Coverage |
| Test dependencies | Test-scoped libraries the build doesn't declare yet — the executor's only license to add them | `@.claude/rules/testing.md` § Asynchronous effects |

The HTTP contract's cases aren't repeated here: they're cited from `30-rest.md`. The
**shape** of the class that verifies them belongs to this skill —
`templates/ControllerTest.java.example`. Cases there, shape here; one owner for each
thing.

External sources in `references/best-practices-links.md`: JUnit, AssertJ, Mockito,
Testcontainers, ArchUnit, JaCoCo, and Spring's testing docs.

The exemplars in `templates/` are a **shape reference**, not files to copy. The
`java-spring-boot-developer` executor reads them when generating a use case's code;
`ArchitectureTest.java.example` is the one exception — the `archunit-installer` agent
reads it and writes the real file, once per project.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. That covers both
modes: design mode writes inside the use case folder, and setup mode writes nothing itself —
every file `ArchUnit` needs is written by the `archunit-installer` agent, which the guard
bypasses as an executor.

**Unfiltered Bash:** setup mode verifies with `./mvnw` goals that depend on the build shape, plus `curl` for the Testcontainers image tag and `java …ArchHook.java` — a fixed list trails the build. Writes stay under `guard`/`guard bash`, and a force push is blocked by `guard bash` (`guard.force_push`).

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `10-domain.md`
(mandatory in design mode — stops without the second), `20-persistence.md`,
`30-rest.md`, `31-graphql.md`, `32-security.md`, `28-http-client.md`, `29-ai.md`, `23-search.md`, `35-jobs.md` and `22-cache.md` when they
exist, `@.claude/rules/search.md` § Tests when `23-search.md` does, `@.claude/rules/ai.md` § Tests when `29-ai.md` does, `@.claude/rules/scheduling.md` when `35-jobs.md` does, `@.claude/rules/caching.md` § Tests
when `22-cache.md` does, `@.claude/rules/authorization.md` § Tests
when `32-security.md` does, `@.claude/rules/http-client.md` § Tests when `28-http-client.md` does,
`@.claude/rules/testing.md`,
`@.claude/rules/error-handling.md`, `@.claude/rules/naming.md`,
`@.claude/rules/code-quality.md`, `@.claude/rules/architecture-ddd.md`,
`@.claude/rules/logging.md` (masking test requirement for fields `30-rest.md` marked
sensitive), and the active blueprint's `packages.map`.

**Writes** `docs/use-cases/UC-NNN-<slug>/40-tests.md` in design mode, directly. Setup
mode writes nothing itself — it delegates to `archunit-installer`, which writes
`<main-module>/src/test/java/**/ArchitectureTest.java`, the ArchUnit entries in the
POM, the `jacoco-maven-plugin`'s `check` execution, and — the one exception, a single
line, not a file — the pinned image tag in the Initializr-generated
`TestcontainersConfiguration.java`. Nothing else in `src/test/**`. Contract of that
agent's own reads and writes: `@.claude/agents/archunit-installer.md`.

**Does not edit `docker-compose.yml`**, neither directly nor through the agent, and does not
invoke `docker-architect` either. A tag mismatch against the compose-side service comes back
in the agent's summary, and this skill reports it with the `/docker-architect` command that
resolves it — single owner of that file, see its Contract.

**Owns the coverage gate**, since
`@.claude/decisions/0011-bootstrap-without-business-code.md`. `project-bootstrap`
remains the owner of the POM and writes JaCoCo instrumenting and reporting; the `check`
execution, which is what turns a report into a gate, comes in here — alongside
ArchUnit, because both depend on code existing for them to apply to. Ownership is this
skill's; the writing happens in the delegated agent's isolated context.

**Doesn't write the use case's tests.** The files in `src/test/**` come from the
executor agent. Doesn't edit the other partials and doesn't touch `.claude/rules/**`.

**Doesn't duplicate `rest-api-architect`**: the HTTP contract's cases belong to
`30-rest.md`. This partial cites them and adds level, data, and gaps.
