---
name: http-client-architect
description: >
  Designs the outbound HTTP adapter of an already-modeled use case — which client (HTTP interface
  with @HttpExchange over RestClient, RestClient directly, OpenAPI Generator, WebClient for a
  stream, OpenFeign as legacy), the engine and its pool (Apache HttpClient 5, JDK HttpClient,
  Reactor Netty), timeouts, the retry allowlist and the one retrying layer, circuit breaker and
  bulkhead, outbound authentication (OAuth2 client credentials, token relay, API key, Basic, mutual
  TLS, HMAC signing), how each failure maps to the integration exception families, and the
  WireMock test cases — into the `28-http-client.md` partial. Use when the request involves
  calling an external API, a third-party or partner service, a payment gateway, a REST client, an
  HTTP client, RestClient, RestTemplate, WebClient, Feign, @HttpExchange, a timeout or retry on a
  remote call, a circuit breaker, or "the provider is down". Piece of the `/new-feature` pipeline:
  requires `10-domain.md` in the given folder with a port of kind `external HTTP`, and stops
  without it.
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

# HTTP Client Architect

Designs **how this service calls another one over HTTP**: which client and which engine, how long
it waits, what it retries and where, how it authenticates, what each failure becomes inside the
domain, and which cases prove it. What `use-case-design` recorded under External calls and
`domain-modeling` declared as a port of kind `external HTTP`, this skill turns into an adapter
the executor can write without deciding anything.

**Scope: servlet applications.** The adapter runs on a servlet project's threads. `WebClient` is in
scope only to consume a stream the provider pushes; a WebFlux application has no norm in this
project and is out of scope — say so and stop when the project's web starter is the reactive one.

**Entry rule: without an outbound port there is nothing to implement.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `10-domain.md` and treats them as a contract.
It runs only when `10-domain.md` § Ports declares at least one port of kind `external HTTP`.
Without `10-domain.md` it stops and tells the caller to run `/domain-modeling`; with it but no such
port, it stops and says the case makes no outbound HTTP call. A port of that kind with no External
calls block in `00-use-case.md` (written before the block existed) is not a reason to stop: ask
step 3's questions and record the answers as a divergence.

**Exit rule: writes no code.** It emits `28-http-client.md`. The adapter, the shared translator,
the engine configuration and the properties come from the executor agent, which reads the partial
and the exemplars in `templates/`.

**Rule rule: rules don't live here.** Timeouts, the retry allowlist, one retrying layer, the
tolerant reader, outbound credentials, SSRF and the mandatory test cases are
`@.claude/rules/http-client.md`. The integration families are `@.claude/rules/error-handling.md`;
their statuses are `@.claude/rules/api-rest.md` § Errors — 500 family. This skill applies and cites
them; it doesn't reproduce them.

## How it's invoked

Two paths: `/http-client-architect` by hand, or chained by `/new-feature` as step 3c — after REST and
security, before messaging, jobs and persistence. That's why it does **not** carry
`disable-model-invocation` — a skill the model can't see is a skill the orchestrator can't call
(`@.claude/decisions/0007-pipeline-skills-invocation.md`). The guard against firing out of order is
the entry rule above.

## Why this is a skill and not a subagent

Form 1, motivated by axes 2 and 9 of the designer's interview: an outbound call is decided per use
case — which provider, which client, which retry, which credential — behind an engine and a failure
taxonomy decided once per project, and no piece owned either. The closest rejected form was the norm
and the taxonomy alone, with the executor building the adapter: nothing would interview the
provider, and persistence would never learn about the stored idempotency key. A subagent fails the
counter-test on all three points: the interview is the task, the reference fits in `references/`
and `templates/`, and the partial is short.

Pinned to `opus`: the partial is what the executor implements verbatim, and a retry or timeout
designed wrong multiplies load on a provider or charges a customer twice
(`@.claude/decisions/0081-skill-model-required-per-class.md`). Design record:
`@.claude/decisions/0121-http-client-architect-skill.md` (this repository only).

## Boundary with neighboring skills

| Piece | Decides | Never decides |
|---|---|---|
| `use-case-design` | The business fact External calls: which system, what for, what the provider documents about idempotency and quota, and the authentication scheme it demands | Client, timeout, status |
| `domain-modeling` | The outbound port, its domain types, its kind `external HTTP`, the domain outcomes of each remote answer (a decline is a rule violation), and a state for an unknown outcome when the case needs one | HTTP types, retries |
| **this skill** | Client, engine and pool, timeouts, retrying layer and policy, breaker and bulkhead, outbound authentication wiring, the failure table per operation, project-wide setup, properties, the contract test cases | Tables and columns, the reconciliation job's schedule, test shape |
| `persistence-architect` | The final form of a stored idempotency key or a pending-outcome column this skill asks for | Why it exists |
| `jobs-architect` | The schedule and coordination of a reconciliation pass this skill asks for | What the pass calls |
| `security-architect` | The inbound filter chain — including when the OAuth2 client starter would turn Boot's default chain on | Outbound credentials |
| `test-architect` | The test shape for every case § 9 lists | Which cases exist |

Two facts cross that line, and each has one owner:

- **The idempotency key** is `10-domain.md`'s: a value on the aggregate, created with the operation.
  This skill says the provider honors it and that the adapter sends it; if the domain partial has no
  such field while the call is a non-idempotent POST, that is a requirement upstream (§ 10), never
  a key generated in the adapter.
- **The 5xx rows** of the error map come from the integration families, mapped once in
  `ApiExceptionHandler`. `30-rest.md` keeps the domain rows; this partial never adds a status.

## Procedure

1. **Read the specs.** `00-use-case.md` (External calls, trigger, side effects) and `10-domain.md`
   (§ Ports with their kind, the domain types, the outcomes and states). Without `10-domain.md`,
   stop. Apply the entry rule. Read `30-rest.md` too when it exists — the trigger's own deadline
   bounds the outbound timeouts.

2. **Survey — every answer the project already gave is inherited, never re-asked.**

   ```bash
   # Clients, engines and resilience already in the build
   grep -nE "spring-boot-starter-(restclient|webclient|webflux|security-oauth2-client|aspectj)|httpclient5|resilience4j|openfeign|openapi-generator|wiremock" pom.xml build.gradle* 2>/dev/null
   # Outbound wiring already in the code
   grep -rnE "@HttpExchange|@ImportHttpServices|RestClient|WebClient|@FeignClient|RestTemplate|ClientHttpRequestFactoryBuilderCustomizer|HttpFailureTranslator|IntegrationException|@Retryable|@EnableResilientMethods" --include='*.java' src/main 2>/dev/null
   # Decisions earlier use cases recorded
   find docs/use-cases -name '28-http-client.md' 2>/dev/null
   grep -rnE "spring\.http\.(clients|serviceclient)|spring\.security\.oauth2\.client|resilience4j\.|app\.http\." src/main/resources 2>/dev/null
   # Inbound security on disk — decides the OAuth2 client starter's impact
   grep -rnE "SecurityFilterChain" --include='*.java' src/main 2>/dev/null
   ```

   And the active blueprint's `packages.map`: the entry ending in `.http` is where the adapters go,
   one subpackage per remote system, plus `shared` for the project-wide pieces. Never a package
   chosen inside this use case.

   | Fact | Inherited from | Asked only when |
   |---|---|---|
   | Engine, pool sizes, eviction | The pinned factory, the engine customizer on disk, or an earlier § 3 | No outbound call exists yet |
   | Integration families, translator, retry predicate | `domain.exception` and the `shared` subpackage on disk, or an earlier § 6 | Never asked — NEW the first time, REUSE afterwards |
   | Client of a provider already called | The adapter on disk or an earlier § 2 | Never — a second client for the same provider is a divergence |
   | Credential of a provider already called | The registration or interceptor on disk, or an earlier § 4 | Never |
   | Retrying layer for this trigger | The trigger: an HTTP request retries nowhere upstream; a Kafka listener and a job retry on their own (`messaging.md`, `scheduling.md`) | The trigger is new and its retry policy is not on disk |

   **The OAuth2 client starter's side effect.** When § 4 needs it and the survey found no
   `SecurityFilterChain`, adding it turns on Boot's default chain and every endpoint but health
   answers 401. That is a row in § 10 to `32-security.md` and an impact the user decides now —
   never a silent change of behavior.

3. **Interview — only what step 2 did not settle.** `AskUserQuestion`, at most 4 questions per call
   and **never fewer than 2 real options** per question; an axis with one sensible answer is decided
   and recorded. Every option states its cost — a dependency, a table, a job.

   | Axis | Decides | Skip when |
   |---|---|---|
   | **Provider contract** — documentation link, published OpenAPI document (and whether it is usable), API versioning | § 1, § 2 | Inherited |
   | **Idempotency** — does the provider honor an `Idempotency-Key` on writes, for how long; is the operation naturally idempotent | `@IdempotentCall`, § 10 key requirement | Read-only operations |
   | **Latency and quota** — measured or published p99/p99.9, rate limit, the load balancer's idle timeout | Timeouts, pool, bulkhead | Inherited for the provider |
   | **Failure tolerance** — may the use case fail fast when the provider is down, or must it degrade (and to what, decided by the business) | Breaker, bulkhead, fallback | — |
   | **Authentication** — the scheme `00-use-case.md` recorded, plus what it needs: registration, scopes, key location, certificate source, signing spec link | § 4, through `references/client-decision-matrix.md` § 3 | Inherited for the provider |
   | **Unknown outcome** — when a write times out after the retries, may the case stop there, or must the result be reconciled later | § 10 to `10-domain.md` and `35-jobs.md` | Read-only, or naturally idempotent writes |

   Never ask about statuses (`@.claude/rules/api-rest.md` decides), class names, or library versions
   (the Boot parent and `maven-metadata.xml` decide).

4. **Choose the client — § 2.** Per dependency, `references/client-decision-matrix.md` § 1: the
   first row that matches wins. Record the winner, the row, one line per rejected client, and the
   exemplar. OpenFeign is chosen only by row 1, and the row says whether this case migrates it.

5. **Fix each operation — § 1.** One row per port method: dependency (the group id), method and path
   with the provider's documentation link, idempotent or not and why, where the key comes from, the
   read timeout with the number it was derived from, and every domain outcome the operation maps
   (a 404 that means absent, a 422 that means declined, a 409 that means duplicate) — read by the
   Problem Details `type` when the provider sends one. Everything else falls to the integration
   families; the row says nothing about them.

6. **Fix the engine and pool — § 3.** Once per project: NEW in the first outbound case, REUSE
   afterwards, CHANGE when this provider needs a larger per-route limit. `references/client-decision-matrix.md`
   § 2 picks the engine; size the pool by Little's law from step 3's numbers; eviction and
   time-to-live below the provider's idle timeout. The factory property is always pinned.

7. **Fix outbound authentication — § 4.** Per dependency, `references/client-decision-matrix.md` § 3.
   Name the exemplar, every environment variable behind a secret, and — for HMAC — the provider's
   signing spec, copied with its link. Mutual TLS uses a bundle; where the bundle's material comes
   from is transport security's decision, recorded as a requirement when no bundle exists yet.

8. **Fix retry and resilience — § 5.** One retrying layer, named: the adapter's `@Retryable`, or the
   trigger's own retry (a listener's error handler, a job's next run) — never both. Attempts, backoff,
   jitter and maximum delay; what is retried follows the predicate and `@IdempotentCall`, not a
   per-case list. Breaker and bulkhead only when step 3 named a slow or unstable dependency, with
   their numbers; a fallback only when the business named one, and never one that reports success.

9. **Fix the project-wide setup — § 6.** Each component with NEW / REUSE / CHANGE and its exemplar:

   | Component | Exemplar |
   |---|---|
   | Integration families | `IntegrationExceptions.java.example` |
   | Translator, retry predicate, `@IdempotentCall`, `ResilientHttpCall`, `@EnableResilientMethods` | `HttpFailureTranslator.java.example` |
   | Engine | `ApacheHttpClient5Config.java.example` · `JdkHttpClientConfig.java.example` · `ReactorNettyConfig.java.example` |
   | Outbound authentication | the row of step 7 |
   | 502 / 503 + `Retry-After` / 504 handlers | `rest-api-architect/templates/ApiExceptionHandler.java.example` — CHANGE the first time |
   | `Clock` bean, for HMAC signing | NEW when absent |

10. **Fix configuration — § 7.** Every property — `spring.http.clients.*`, the group's
    `spring.http.serviceclient.<group>.*`, the OAuth2 registration, the SSL bundle, `app.http.*`,
    `resilience4j.*` — its value, and the environment variable behind each secret, never a literal.
    Shape in `templates/application-http-client.yml.example`.

11. **Declare dependencies — § 8.** Only what step 2 did not find. Version column empty where the
    Boot parent manages it; otherwise the `<release>` of the artifact's `maven-metadata.xml`, read
    now with `curl` and written in the row (`@CLAUDE.md` invariant 8). With a Spring Cloud BOM in the
    build and Resilience4j declared, the row says to import `resilience4j-bom` ahead of it
    (`references/client-decision-matrix.md` § 5). The test support is `test-architect`'s § 5.

12. **List the contract test cases — § 9.** Per port method, the mandatory cases of
    `@.claude/rules/http-client.md` § Tests that apply, with the expected family, `errorCode` and
    attempt count. `test-architect` turns them into tests with its own exemplar.

13. **Hand the other partials what they need — § 10, requirements only.** A non-idempotent write
    whose key the domain does not hold → the key on the aggregate (`10-domain.md`) and its column
    (`20-persistence.md`). An unknown outcome that must be reconciled → the state on the aggregate
    and a reconciliation pass (`35-jobs.md`). The OAuth2 client starter in a project without a chain
    → `32-security.md`. Named by what they are, never DDL or a cron.

13b. **Decide the design patterns of this layer.** Run
    `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over what this case adds — an
    anti-corruption layer per provider is the usual shape, a growing `if` over provider names the
    usual symptom. The answer goes into `## Design patterns` — `none` when nothing matches, and
    absence is not `none`.

14. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/28-http-client.md`, from
    `templates/http-client-spec.md.example`. Eleven numbered blocks plus `## Design patterns`, all
    mandatory, each `none` when empty — absence is not `none`.

15. **Report and stop.** File path; the client and engine per dependency and whether they were
    inherited; the retrying layer; the authentication scheme; § 8 and § 10 as lists. Don't invoke
    anyone: messaging, jobs and persistence run next, and they read § 10 in their first pass.

## What the partial contains

| Block | Fixes |
|---|---|
| 1 · Operations | Per port method: dependency, remote call with the documentation link, idempotency and key source, read timeout and its origin, the domain outcomes |
| 2 · Client | The client per dependency, the matrix row, the rejected ones, exemplars |
| 3 · Engine and pool | Engine, pinned factory, pool sizes and their arithmetic, lease timeout, eviction, engine retry off |
| 4 · Outbound authentication | Scheme per dependency, where each credential lives, the exemplar |
| 5 · Retry and resilience | The retrying layer, attempts and backoff, breaker, bulkhead, fallback |
| 6 · Project-wide setup | Each shared component with NEW / REUSE / CHANGE |
| 7 · Configuration | Every property, its value, the environment variable behind each secret |
| 8 · Declared dependencies | Coordinates, version empty when managed or read from `maven-metadata.xml` |
| 9 · Contract test cases | Per port method, the mandatory cases with family, `errorCode` and attempts |
| 10 · Requirements to other partials | Key, state, column, reconciliation pass, security impact — requirements only |
| 11 · Deferred | Same shape as every partial's `Deferred` |
| Design patterns | Each pattern adopted — step 13b. `none` when none |

Plus `## Impact on approved use cases` and `## Implementation order`, as in every partial.

The exemplars in `templates/` are a **shape reference**, not files to copy. They target the servlet
stack and the Spring Framework generation the project's Boot parent manages; every one of them was
compiled against Boot 4.1.1, and the integration test exemplar ran green against the default
adapter. The sources they follow are in `references/http-client-reference-links.md`.

The mapper comes in two exemplars — `PaymentGatewayMapper` inside `HttpExchangeAdapter.java.example`, and `HttpClientMapStructMapper.java.example` beside it — because the mechanism is the project's, not this partial's: the partial says what maps to what, and the executor writes it in the mechanism the root `CLAUDE.md`'s `**Mappers:` paragraph names (`@.claude/rules/mapping.md`).

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json`, and `ArchHook.java guard` enforces it. Writes inside the use
case folder and nothing else; an adapter written under `src/` is refused with exit 2.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `10-domain.md` (mandatory — stops
without the second), `30-rest.md` and `32-security.md` when present, earlier cases'
`28-http-client.md`, `pom.xml` (or the Gradle build), `src/main/resources/application*.yml`, the
outbound wiring on disk, the active blueprint's `packages.map`, `@.claude/rules/http-client.md`,
`@.claude/rules/error-handling.md`, `@.claude/rules/api-rest.md`, `@.claude/rules/architecture-ddd.md`,
`@.claude/rules/logging.md`, `@.claude/rules/observability.md`, and `references/`. Reads Maven
Central's `maven-metadata.xml` for an unmanaged dependency's version.

**Writes** `docs/use-cases/UC-NNN-<slug>/28-http-client.md`. Nothing else.

**Owns** each operation's client, timeouts, retry policy and failure table; the project's HTTP
engine and pool; the retrying layer of each outbound call; breaker and bulkhead; the outbound
authentication wiring; and the project-wide outbound setup.

**Does not decide** the use case boundary or its External calls fact (`00-use-case.md`), the
port, its domain types, the idempotency key field or the unknown-outcome state (`10-domain.md`),
tables and columns (`20-persistence.md`), the reconciliation schedule (`35-jobs.md`), the inbound
chain (`32-security.md`), or the test shape (`40-tests.md`). Does not write Java, `pom.xml` or
`application.yml` — the executor does, from this partial. Doesn't touch `.claude/rules/**`. Does not
design reactive (WebFlux) applications.
