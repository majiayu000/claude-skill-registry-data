---
name: cache-architect
description: >
  Designs the application cache of an already-scoped use case — which reads are served from a
  copy, the key of each (every input that changes the result, the caller included), Caffeine or
  Redis, expiry and size per cache, every writer that must evict, failure and load when the cache
  is gone, serialization and metrics — into the `22-cache.md` partial, as a decorator of an
  outbound port. Use when the request involves a cache, @Cacheable or @CacheEvict, Caffeine,
  Redis as a cache, a stale read, a cache hit ratio, a cache stampede, or a read that must be
  faster than its source. Piece of the `/new-feature` pipeline: requires `00-use-case.md` in
  the given folder with a `Freshness` row that states a tolerance, plus `10-domain.md` — and
  stops without them.
argument-hint: "[path of the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*), Bash(awk:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# Cache Architect

Designs **which reads are answered from a copy, and how the copy stays honest**: the key that
keeps one caller's answer away from another, where the copy lives, how long it may live, who
must throw it away when the data changes, and what happens when the cache is gone. The business
already said how stale an answer may be — that is the `Freshness` row of `00-use-case.md`. This
skill turns that number into a cache, or into the finding that no cache is needed.

**Entry rule: no tolerance, no cache.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-use-case.md` and runs only when its `Freshness` row states a
tolerance — a duration an answer may be old ("a balance up to 30 seconds old"). The row reads
`none` (always current), or is missing → stop and say so: a cache without a stated tolerance is a
staleness bug waiting for its first write, and "the query looks slow" is a reason to measure, not a
tolerance (`@.claude/rules/caching.md` § Boundary). `10-domain.md` is required too: the cache
decorates an outbound port it declares, and without one there is nothing to wrap.

**Exit rule: it doesn't write code.** It emits `22-cache.md`. The Java classes come from the
executor agent, which reads the partial and the `templates/` exemplars.

**Rule rule: the rules don't live here.** Boundary, keys, values, expiry, invalidation, failure,
metrics and tests are `@.claude/rules/caching.md`. This skill applies and cites it; it doesn't
reproduce it.

## How it's invoked

Two paths: `/cache-architect` by hand, or chained by `/new-feature` after persistence and before
tests. That's why it does **not** carry `disable-model-invocation` — a skill the model can't see is
a skill the orchestrator can't call (`@.claude/decisions/0007-pipeline-skills-invocation.md`). The
guard against firing out of order is the entry rule above.

## Why this is a skill and not a subagent

Form 1, motivated by axis 1 of the designer's interview: no piece owned application caching, and
the maintainer chose to design it ahead of a run that shows the defect, on the pitfalls the
official documentation records (`references/pitfalls.md`). The closest rejected form was the same
skill with its norms in `references/` — the executor never loads a design skill's references, so
each partial would restate them. A subagent fails the counter-test on all three points: the
interview is the task, the reference fits in `references/` and `templates/`, and the partial is
short.

Pinned to `opus`: the partial is what the executor implements verbatim, and the pin holding for
the rest of the turn keeps `/new-feature` on the model that designed it
(`@.claude/decisions/0081-skill-model-required-per-class.md`). Design record:
`@.claude/decisions/0144-cache-architect-skill.md` (this repository only).

## Boundary with neighboring skills

| Piece | Decides | Never decides |
|---|---|---|
| `use-case-design` | The `Freshness` tolerance — a business fact, asked in business words | Whether a cache exists, its provider, its expiry |
| `domain-modeling` | The outbound port and the record it returns | That the port is cached |
| `persistence-architect` / `http-client-architect` | The adapter that implements the port, the query or the call behind it | Anything about the copy |
| `jobs-architect` | The replica count (`35-jobs.md` § 3), any warm-up or refresh job | Expiry, keys |
| `messaging-architect` | A broadcast channel, if a deferred two-level cache ever needs one | The cache itself |
| **this skill** | Which reads are cached, each key, provider, expiry and size per cache, every writer that must evict, failure and load, serialization, metrics, the `redis` compose row | The tolerance, the port, the query, the tests |
| `test-architect` | Which test proves each cached read, at what level | — |
| `rest-api-architect` | HTTP response caching (`Cache-Control`, `ETag`) | Anything inside the service |

**The replica count** has one owner per project, and this skill inherits it like
`jobs-architect` does; asked only when no partial recorded it.

## Procedure

1. **Read the specs.** `00-use-case.md` (the `Freshness` row and the Components table),
   `23-search.md` when the cached port is of kind `search index` — its § 6 lag comes out of the
   tolerance first, and only the remainder bounds this cache's expiry; a remainder of zero or less
   means no cache, recorded as such —
   `10-domain.md` (the outbound ports and the records they return), `20-persistence.md` and
   `28-http-client.md` when present (the adapter behind each port), `35-jobs.md` when present.
   Apply the entry rule. List the reads the tolerance covers, each as a port method.

2. **Survey — every answer the project already gave is inherited, never re-asked.**

   ```bash
   # Provider already in the build
   grep -nE "spring-boot-starter-cache|caffeine|spring-boot-starter-data-redis" pom.xml
   # Caches already in the code
   grep -rnE "@(Cacheable|CacheEvict|CachePut|Caching)\b|@EnableCaching|CacheManager" --include='*.java' src/main 2>/dev/null
   # Decisions earlier use cases recorded
   find docs/use-cases -name '22-cache.md' 2>/dev/null
   grep -rn "Replicas\|Claim strategy" docs/use-cases/*/35-jobs.md docs/use-cases/*/20-persistence.md docs/use-cases/*/22-cache.md 2>/dev/null
   ```

   And the active blueprint's `packages.map` entry ending in `.cache` — the package every
   decorator and the cache wiring go to. No such entry → stop and say which line is missing from
   the blueprint, instead of choosing a package inside this use case.

   | Fact | Inherited from | Asked only when |
   |---|---|---|
   | Provider | A dependency in `pom.xml`, or an earlier `22-cache.md` § 2 | Neither exists — first cache of the project |
   | Replica count | An earlier `22-cache.md` § 2, `35-jobs.md` § 3, else `20-persistence.md` § 1 `Claim strategy` | None exists |
   | Cache wiring (`@EnableCaching`, manager, error handler) | Already in the cache package | First cache of the project |

   **A cache annotation outside the cache package is not reuse.** A project that annotated a
   persistence adapter or a service before this skill existed has caching the rule does not
   allow (`@.claude/rules/caching.md` § Boundary). Record it in `## Impact on approved use
   cases` and decide with the user between moving it behind a decorator in this run and deferring
   that with an owner — never a second cache on the same read.

3. **Interview — only what steps 1 and 2 did not settle.** `AskUserQuestion`, at most 4 questions
   per call and **never fewer than 2 real options** per question; an axis with one sensible answer
   is decided and recorded, not asked (`@CLAUDE.md` § Known pitfalls). Every option states its
   cost — the server Redis adds, the drift a local cache accepts.

   | Axis | Decides | Skip when |
   |---|---|---|
   | **Replicas** — how many instances serve this read in production? | Provider (§ 2) | Step 2 inherited it |
   | **Who else writes this data** — another use case, a job, a consumer, a bulk statement, another service? | § 4, one row per writer | The Components tables of every approved case already answer it — read them and list, then ask only "anything else?" |
   | **Does the result depend on who asks** — the caller, the tenant, a role, the locale? | The key (§ 1) — and, when the port does not take that input as a parameter, a divergence: `10-domain.md` is `domain-modeling`'s to change, and the read stays uncached until it does | The port method already takes every such input |
   | **Without the cache** — can the source take the full read rate, or must load be shed? | § 5 | Nothing in the case suggests the source is the bottleneck — record "holds" and why |
   | **Absence** — is "not found" asked often, and may it be served stale? | Whether absence is cached, with its own expiry | The read never returns absence |

4. **Choose the provider.** Apply `references/provider-decision-matrix.md` § 2 to the answers: the
   first row that matches wins; a tie goes to the provider already in `pom.xml`, then to Caffeine.
   **One provider per project** (`@.claude/rules/caching.md` § Boundary) — a case whose needs the
   project's provider cannot meet is a divergence to report and ask about, never a second one added
   silently. Record the winner, the row that decided it, and one line per rejected option — the
   Hibernate second-level cache among them when the read is entity-by-id.

5. **Design each cached read.** One row of § 1 per read, and every column is filled:

   | Column | Content |
   |---|---|
   | Read | The port method — the decorator implements that port |
   | Cache name | One per kind of value, kebab-case, added to `CacheNames` |
   | Key | The SpEL expression, naming every input that changes the result — the caller included when the result depends on it, always as a port parameter, never read from a context |
   | Value | The record the port returns, when it is a record of plain components; otherwise the cache-local `…CacheEntry` record the decorator maps to |
   | Freshness tolerance | Copied from `00-use-case.md` — the bound for § 3; for a search projection, the tolerance minus `23-search.md` § 6's lag |
   | Absence cached | no, or yes with its own expiry |
   | Concurrent misses | `sync`, or per caller — never `sync` with `unless` (the framework refuses it) |

   The form is fixed: `templates/CachedPortAdapter.java.example` — a decorator that implements
   the port, depends on the port, and is wired as its @Primary bean by the delegate's bean name.
   A read hot enough that a miss is felt, with a tolerance that covers serving the old value
   for one refresh, takes `templates/RefreshAheadCache.java.example` instead.

6. **Size expiry and size — § 3.** Per cache: the expiry, never longer than the tolerance; the
   maximum size for a local cache, from the number of distinct keys the case expects; jitter on
   Redis; refresh ahead only per step 5. Never one setting for all caches.

7. **List every writer — § 4.** Every writer of the data each cache holds, from step 3: whether it
   goes through the decorated port (evicts by construction, after commit), evicts explicitly, or
   bypasses the cache — and then the expiry is its staleness bound, written as accepted or
   flagged. A writer in an approved case that must change goes to `## Impact on approved use
   cases`.

8. **Failure, load, serialization, metrics — § 5 to § 7.** The error handler and the client
   timeout every project gets (`CountingCacheErrorHandler`, `application-cache.yml.example`);
   what the source does without the cache, from step 3; for Redis, the typed serializer per cache
   and the format version; the metrics and the alarm each exists for.

9. **Declare dependencies — § 8.** `spring-boot-starter-cache`, plus Caffeine or
   `spring-boot-starter-data-redis`, versions empty — the Boot parent manages them, and a version
   is never written from memory (`@CLAUDE.md` invariant 8). The executor may write `pom.xml` for
   exactly these rows.

9b. **Decide the design patterns of this layer.** Run
   `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the decorators this case
   adds — the Decorator over the port is the shape, recorded as such. The answer goes into
   `## Design patterns` — `none` is not valid when a decorator is written.

10. **Check Redis has a container — Redis only.** List the keys inside the `services:` block:

    ```bash
    awk '/^services:[[:space:]]*$/{s=1;next} /^[^[:space:]#]/{s=0} s&&/^  [A-Za-z0-9_.-]+:[[:space:]]*(#.*)?$/{sub(/[[:space:]]*#.*$/,"");print}' docker-compose.yml
    ```

    Write the answer as a row of `## Compose services`, shaped and decided by
    `@.claude/skills/docker-architect/references/compose-service-decision.md` — `exists` when
    `redis` is listed, otherwise the question that reference owns. An `external` answer makes that
    address the host default of `spring.data.redis.host` in § 9. Caffeine → `none`. Do **not**
    invoke `docker-architect` and do not edit `docker-compose.yml`: a design run produces a spec,
    never a container.

11. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/22-cache.md`, from
    `templates/cache-spec.md.example`. Ten numbered blocks plus `## Compose services` and
    `## Design patterns`, all mandatory, each written as `none` when there is nothing — absence is
    not `none`. § 10 `Deferred` follows the same shape as every other partial's.

12. **Report and stop.** Path of the file written; the provider and the row that chose it; the
    replica count **and where it came from**; each cached read with its key and expiry next to its
    tolerance; every writer of § 4 whose staleness bound is the expiry; the `## Compose services`
    row. A writer nobody could name, or a result that depends on the caller through a port that
    does not take the caller, is a finding. Don't invoke anyone else: `test-architect` runs next and
    reads § 1 and § 4.

## What the partial contains

| Block | Fixes |
|---|---|
| 1 · Cached reads | One row per read, every column of step 5 |
| 2 · Provider | The provider, the matrix row that chose it, the rejected ones in one line each, transaction awareness, and whether it was inherited |
| 3 · Expiry and size | Per cache: expiry next to its tolerance, maximum size, jitter, refresh ahead |
| 4 · Invalidation | Every writer of the cached data, its path, its eviction, its staleness bound |
| 5 · Failure and load | Error handler, client timeout, what the source does without the cache |
| 6 · Serialization | Per cache: serializer and format version (Redis); `none` for a local cache of immutable records |
| 7 · Observability | Metric names, and the alarm each one exists for |
| 8 · Declared dependencies | Coordinates, version empty when managed |
| 9 · Configuration | Every property the cache reads, its value, and which partial owns the value |
| 10 · Deferred | Same shape as every partial. `none` when nothing was deferred |
| Compose services | The `redis` row, or `none` for a local cache |
| Design patterns | The Decorator over each port, with its classes — step 9b |

Plus `## Impact on approved use cases` and `## Implementation order`, as in every partial.

The exemplars in `templates/` are **reference for form**, not files to copy:

| Exemplar | Shape of |
|---|---|
| `templates/CaffeineCacheConfig.java.example` | Local provider; also `CacheSettings`, `CacheNames`, `CountingCacheErrorHandler`, shared by both providers |
| `templates/RedisCacheConfig.java.example` | Distributed provider: typed serializer per cache, format version, jitter, `SCAN`, transaction-aware |
| `templates/CachedPortAdapter.java.example` | The decorator over a persistence port (read + evicting write) and over an HTTP port (read only) |
| `templates/RefreshAheadCache.java.example` | One hot read, refreshed ahead of expiry |
| `templates/application-cache.yml.example` | Redis connection with short timeouts and the password placeholder; `app.cache.*` per cache |
| `templates/cache-spec.md.example` | The partial |

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json`, and `ArchHook.java guard` enforces it. Writes inside the use
case folder and nothing else.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` (mandatory), `10-domain.md`
(mandatory), `20-persistence.md`, `28-http-client.md` and `35-jobs.md` (when present), the
Components tables and `22-cache.md` of earlier cases, `pom.xml`, `docker-compose.yml`, the active
blueprint's `packages.map`, `@.claude/rules/caching.md`, `@.claude/rules/architecture-ddd.md`,
`@.claude/rules/observability.md`, `@.claude/rules/secrets.md`,
`@.claude/skills/docker-architect/references/compose-service-decision.md`, and this skill's
`references/`.

**Writes** `docs/use-cases/UC-NNN-<slug>/22-cache.md`. Nothing else.

**Owns** which reads are cached and the key of each, the cache provider of the project, expiry and
size per cache, the list of writers that must evict, failure and load handling of the cache, the
cache serialization and format version, cache metrics, and the `redis` compose row.

**Does not decide** the freshness tolerance (`00-use-case.md`), the port or the record it
returns (`10-domain.md`), the query or the call behind the port (`20-persistence.md`,
`28-http-client.md`), the replica count when a partial already recorded it, or the tests
(`40-tests.md`). Does not write Java, `pom.xml`, `application.yml` or `docker-compose.yml` — the
executor and `docker-architect` do, from this partial. Doesn't touch `.claude/rules/**`.
