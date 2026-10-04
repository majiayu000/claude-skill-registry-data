---
name: persistence-architect
description: >
  Designs the persistence layer of an already-modeled use case — tables, aggregate
  mapping, migrations, queries, indexes, and datasource configuration — into the
  `20-persistencia.md` partial. Use when the request involves modeling the database,
  mapping an aggregate to JPA, writing or reviewing migrations, deciding indexes and
  keys, diagnosing N+1 or slow queries, or tuning the pool and datasource properties.
  Piece of the `/new-feature` pipeline: requires `10-dominio.md` in the given folder and
  stops without it.
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

# Persistence Architect

Designs **how the aggregate reaches disk and comes back**: what tables exist, what
columns and types, what indexes, what migration, what queries, and what the datasource
needs configured. What `domain-modeling` left as an output port, this skill gives body
to.

**Entry rule: without `10-dominio.md`, there's nothing to persist.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md` and `10-dominio.md` and treats them as a
contract. Without the domain partial, it stops and tells you to run `/domain-modeling` —
designing tables before the aggregate has a boundary produces a schema that describes the
form, not the business.

**Two more partials stop it, each under its own condition**, for the same reason: both
carry schema requirements this pass has to honor, and a schema designed without them is a
schema that gets revised. An HTTP-triggered case with no `30-rest.md` → run
`/rest-api-architect` first. A case whose `10-dominio.md` Events block names external
(Kafka) delivery with no `25-mensageria.md` → run `/messaging-architect` first. And a third,
under the same logic: a case whose `25-mensageria.md` chose Form B, or whose trigger is a
schedule, with no `35-jobs.md` → run `/jobs-architect` first. Step 1 states what each list
contains.

**Exit rule: it writes only under `docs/`.** It emits `20-persistencia.md`, and the
migration SQL goes **inside it** as a code block with its target file name and path —
never as a file under `src/`. The migration file and the Java classes come from the
executor agent, which reads the partial and the `templates/` exemplars. Inherits D15 —
`@.claude/decisions/0003-skill-domain-modeling.md`.

**Rule rule: the rules don't live here.** Lazy fetch, `ddl-auto: validate`, migration
immutability, `open-in-view: false`, and the rest are
`@.claude/rules/persistence.md`. This skill applies them and cites them; it doesn't
reproduce them.

## How it's invoked

Two paths, and both matter: `/persistence-architect` by hand, or chained by
`/new-feature` once that orchestrator exists. That's why it does **not** carry
`disable-model-invocation` — that field hides the skill from the model, and a skill the
model can't see is a skill the orchestrator can't call.

The guard against out-of-order firing isn't the frontmatter: it's the **entry rule**
above. Without the previous partial, the skill stops and says what needs to run first.
Recorded in `@.claude/decisions/0007-pipeline-skills-invocation.md`.

## Why this isn't a subagent

It's a procedure whose step 3 goes back to the user to ask what no earlier spec fixes —
which database engine, which queries the use case actually makes, what row volume is
expected. A subagent doesn't see the conversation. Decision recorded in
`@.claude/decisions/0005-persistence-rule-and-design.md`.

Pinned to `opus`: the partial is what the executor implements verbatim. A pinned model does not make this a subagent — the interview needs the conversation, and the pin holding for the rest of the turn keeps `/new-feature` on the model that designed it (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Boundary with neighboring skills

The division is by **moment and artifact**, not technology:

| Piece | When it acts | What it produces |
|---|---|---|
| `use-case-design` | Before the domain exists | `00-caso-de-uso.md` — boundary and canonical names |
| `domain-modeling` | After the mother spec | `10-dominio.md` — aggregate, invariants, ports |
| `rest-api-architect` | Before this one | `30-rest.md` — transport, plus the schema requirements it creates (block 4) |
| `messaging-architect` | Before this one, only when an event leaves over a broker | `25-mensageria.md` — publication form, plus the schema requirements it creates (§ 6: outbox, dedupe table) |
| `jobs-architect` | Before this one, when a job exists — Form B's relay and prune, or a scheduled trigger | `35-jobs.md` — replica count (§ 3), plus the schema requirements it creates (§ 6: scheduling tables, claim requirement, prune operation) |
| **this skill** | After all three, so every requirement is on the table before the first column is named | `20-persistencia.md`, migration SQL inside it |
| `test-architect` | After all of them | `40-testes.md` |

If the aggregate has no written invariants yet, it isn't this skill. If the problem is a
slow query in code that already exists and there's no new use case, skip steps 1 and 2
and go straight to step 6 (diagnosis) — `references/sql-tuning.md`.

## Procedure

1. **Read the specs.** `00-caso-de-uso.md` and `10-dominio.md` from the folder in
   the target above. Without the second, stop. Extract: aggregate root, fields and types,
   value objects, declared output ports, and the component table with NEW/CHANGE/REUSE
   state. Also read `30-rest.md` when the use case has an HTTP trigger — in `/new-feature` it
   always exists by now, because REST runs first. Its block 4 `Schema requirements` list
   is input to this pass: the shared idempotency table (step 4a) and anything else there
   gets designed now, not in a second pass. An HTTP-triggered case whose `30-rest.md`
   doesn't exist yet → stop and tell the caller to run `/rest-api-architect` first.

   Also read `25-mensageria.md`, **mandatory on the same terms as `30-rest.md`**: when
   `10-dominio.md`'s Events block names external (Kafka) delivery and the messaging partial
   isn't in the folder → stop and tell the caller to run `/messaging-architect` first. In
   `/new-feature` it always exists by now, because messaging runs before this skill. Its
   § 6 `Schema requirements` list is input to this pass exactly as block 4 of `30-rest.md`
   is: the shared outbox table under publication Form B (step 4b), a dedupe table for a
   consumer, and anything else listed there gets designed now, not in a second pass.

   A domain partial whose Events block is "none" or in-process means no messaging partial
   exists and none is expected — read nothing, stop for nothing.

   Also read `35-jobs.md` whenever `25-mensageria.md` chose Form B or `00-caso-de-uso.md`'s
   trigger is a schedule — missing → stop and tell the caller to run `/jobs-architect` first;
   in `/new-feature` it exists by now, because jobs runs before this skill. Two blocks of it
   are this pass's input: **§ 3 · Coordination**, whose replica count decides the claim
   strategy in step 4b — read, never asked again — and **§ 6 · Schema requirements**: the
   tables the chosen scheduling technology needs (`shedlock`, `QRTZ_*`, `BATCH_*`,
   `scheduled_tasks`), written here as migrations from the vendor's DDL, the claim requirement
   under Form B, and the prune's bounded delete.

2. **Survey what already exists.** Look for entities, repositories, and migrations in
   the project. A table that already exists gets altered; it isn't recreated. The
   mother spec's REUSE state overrides intuition. Same check for `idempotency_keys`: it's
   shared by the whole application, not per use case — if a prior pass already created
   it, this one reuses it and doesn't touch it again. Same for `outbox_events`: one per
   project, whatever the number of events.

   ```bash
   ls db/migration/ src/main/resources/db/migration/ 2>/dev/null
   grep -rln "@Entity" --include='*.java' src/ 2>/dev/null
   grep -rl "idempotency_keys" db/migration/ src/main/resources/db/migration/ 2>/dev/null
   grep -rl "outbox_events" db/migration/ src/main/resources/db/migration/ 2>/dev/null
   ```

3. **Interview — only what the specs don't fix.** `AskUserQuestion`, at most 4 questions
   per call and **never fewer than 2 real options per question**: one option isn't a
   question — decide it and record the decision in the partial, since the runtime rejects
   the whole batch over a single one (`@CLAUDE.md` § Known pitfalls). Don't re-ask what
   `00-caso-de-uso.md`, `10-dominio.md`, or `30-rest.md` already answered — the
   collection's growth, above all.

   | Axis | Decides |
   |---|---|
   | Engine and version (Postgres, MySQL, Oracle, H2 only in tests) | Column types, migration syntax, whether `CONCURRENTLY` exists |
   | Expected table volume in 12 months | Whether the index is mandatory or premature, whether `SEQUENCE` beats `IDENTITY` |
   | Queries the use case actually makes, and which fields it filters by | Indexes, projections, what needs `JOIN FETCH` |
   | Concurrency on the same aggregate | Optimistic lock (`@Version`) or none |
   | Retention and deletion | Physical `DELETE` or a status column |
   | Table already exists in production | Mandatory expand/contract, destructive migration deferred |

4. **Design the schema.** One table per aggregate root; child entities of the same
   aggregate go into their own tables with a foreign key to the root. A simple value
   object becomes a column or `@Embeddable`, never its own table — if it needs its own
   table and its own identity, it wasn't a value object
   (`@.claude/rules/value-objects.md`). Fix in writing, column by column: name, type,
   nullability, default, `UNIQUE`, foreign key. A type that isn't Hibernate's default
   inference for the field (`char(n)`, `smallint`) names its `@JdbcTypeCode` in the
   same row, and an assigned id names `Persistable` through the shared
   `AssignedIdEntity` (`templates/JpaEntity.java.example`, last block) — both per
   `@.claude/rules/persistence.md` § Mapping and § Identity and keys.

   **4a. Idempotency, when `30-rest.md` requires it and step 2 found no
   `idempotency_keys` table yet.** Not per-aggregate: one table, shared by every
   endpoint that needs `Idempotency-Key`, modeled once and reused afterward. Shape in
   `templates/IdempotencyKeyTable.sql.example` (schema) and
   `templates/IdempotencyKeyStore.java.example` (entity, Spring Data repository, and the
   adapter implementing the port), plus `templates/IdempotentExecution.java.example` (the
   application component that owns the two-transaction shape) — the transactional half
   of the mechanism whose structural half is `rest-api-architect`'s `IdempotencyKeyInterceptor.java.example`.
   Column set and TTL floor come from `@.claude/rules/api-rest.md` § Idempotency; don't
   redecide them here.

   **4b. Outbox, when `25-mensageria.md` fixes publication Form B and step 2 found no
   `outbox_events` table yet.** Exact mirror of 4a, and for the same reason: one table for
   the whole project, shared by every event, modeled once and reused afterward — never one
   outbox per aggregate or per event type. Shape in
   `templates/OutboxEventTable.sql.example` (schema, partial index, retry columns, and the
   prune as a commented `DELETE`) and `templates/OutboxEventStore.java.example` (entity,
   Spring Data repository, and the adapter implementing `OutboxRelayGateway`). The criterion
   that made Form B apply is `@.claude/rules/messaging.md` § Publication timing, and it
   isn't re-litigated here — `messaging-architect` owns it.

   **The column set is this step's, and the exemplar is its starting point** — `event_id`,
   `aggregate_id`, `event_type`, `payload`, `occurred_at`, `published_at`, `attempts`,
   `last_error`, `dead_lettered`, plus the partial index. That set is right for one relay
   instance retrying on every pass. A column the claim strategy or the pacing chosen below
   needs — a lease column, `next_attempt_at` for per-row backoff — is this step's to add, and
   § 1 names it next to the guarantee it serves; nothing else adds one. So is **the pacing those columns
   encode**: whether a row is retried on every pass or backs off per row, the batch size and
   the attempt ceiling are decided here, together with the claim query, because the column set
   is what makes either possible. **How often a pass runs is not** — the poll interval, the
   trigger and the switch are `35-jobs.md`'s (`jobs-architect`), which designs the relay's
   schedule and the prune job. A `25-mensageria.md` § 6 row naming columns instead of a guarantee is a
   requirement written in the wrong vocabulary — take the guarantee from it (at-least-once,
   attempt count, DLQ destination) and report the column names as a divergence.

   **The claim strategy is an explicit decision of this step, and it gets written down.** The
   exemplar's `claimPending` is an unlocked `SELECT`, which is correct for exactly one
   deployment shape and for no other. **The deployment shape is not asked here:** it is the
   replica count of `35-jobs.md` § 3, and its § 6 already names the claim it requires —
   documented single instance for one replica, locked or leased for more. This step picks the
   shape that meets it (lease or `SKIP LOCKED`), and a requirement it cannot meet is a
   divergence that stops the pipeline: two relay instances polling at once read the same rows
   and publish the whole batch twice, every pass. Its own Javadoc says so — "SINGLE RELAY
   INSTANCE IS ASSUMED" — and a real run copied the method, kept the name, and recorded the
   assumption nowhere, so the name promised a claim the query never made. Decide between three,
   and write the choice plus its reason into the partial's § 1 as **Claim strategy**:

   | Strategy | Shape | When it is the answer |
   |---|---|---|
   | Documented single instance | the exemplar as it stands, unlocked read | one relay by deployment constraint, and the constraint is stated — not hoped for |
   | Lease column | `claimed_at` (+ optional owner id), one `UPDATE … WHERE event_id IN (SELECT … FOR UPDATE SKIP LOCKED) RETURNING …` | more than one instance, and the duplicate rate matters. Same shape `idempotency_keys` already uses for its IN_PROGRESS rows |
   | `FOR UPDATE SKIP LOCKED` at claim time | native query, no extra column, rows locked for the transaction that sends | more than one instance, and a lease column is not wanted |

   The two locking answers are **schema or query changes**, so they belong here and nowhere
   else — a comment in the relay is not a decision. And whichever is chosen, the partial says
   what the method name promises: a method called `claimPending` that does not claim is renamed
   or made true, never left to be read as a guarantee.

   **Read that guarantee before choosing the shape.** A guarantee the exemplar's columns
   cannot hold — per-row exponential backoff has nowhere to record the next attempt — is met
   by adding the column, as above, not by stopping. Stop the pipeline and ask only when **no**
   column or query this step may write makes the declared guarantee hold, the same way
   `/new-feature`'s consolidation requires for a divergence its precedence table doesn't
   resolve. Behaviour settled by whoever owns table shape is the exact failure this split
   exists to prevent; behaviour **delivered** by that owner, once declared upstream, is not.

   **A requirement this step places on another partial is a divergence, never an edit.**
   Bounding the producer's send time so the lease outlives any send (`max.block.ms`,
   `delivery.timeout.ms` on `25-mensageria.md`'s producer) is legitimate and often necessary
   — it goes into § 1 as a requirement on that partial, and consolidation resolves it.

   Two boundaries this step does **not** cross. `OutboxRelayGateway` and
   `OutboxEventRecord` are declared in `messaging-architect`'s
   `templates/OutboxRelayPublisher.java.example`, which owns the relay consuming them: this
   step implements the port, it doesn't re-declare it. And the relay component itself, the
   appender, and its broker side — serialization, topic, DLQ routing — are that skill's.

   The line between the three, written once so no run has to guess it: **this step owns the
   table, its mapping, the claim query, and the `app.outbox.*` values the columns encode**
   (batch size, backoff, attempt ceiling, retention window) plus the statement the prune runs.
   **`messaging-architect` owns the relay pass and everything that touches the broker**, and
   states the guarantee those values have to deliver. **`jobs-architect` owns when anything
   runs** — the poll interval, the on/off switch, coordination across instances, the prune
   job's cadence and batch. What lands in `20-persistencia.md` is the table, its mapping, the
   adapter (`OutboxRelayGateway` and `OutboxRetentionGateway`), and the values this step owns.

   **Retention is the one open value, and it gets asked.** The exemplar's `7 days` (matching
   `app.outbox.prune-after: P7D`) is a starting point, not a default to adopt in silence:
   put it to the user with `AskUserQuestion` — the default first, plus real alternatives —
   and write the chosen window and its reason into the partial's § 1. Never a single-option
   question: with nothing to choose between, decide and record instead of asking.

   **The retention property ships with the job that reads it — and now the job always
   exists.** `jobs-architect` designs `OutboxPruneJob` in the same run as the relay's
   schedule, the first time a project chooses Form B, and `35-jobs.md` § 6 hands this step
   the one operation it calls: `OutboxRetentionGateway.deletePublishedBefore(cutoff, limit)` —
   published rows only, never a pending or a dead-lettered one, bounded by `limit`, served by
   the published-at index. This step writes that statement into the adapter and records the
   window in § 1; `app.outbox.prune-after` then ships in the same change as its reader. The
   route through a `Deferred` row is closed for the prune: it was how a decided 7-day window
   ended up enforced by nothing, over a payload carrying personal data (lessons-learned-014
   § 9, `@.claude/rules/personal-data.md` § At rest). "Keep forever" is still an answer —
   recorded in § 1 with its reason, and then `35-jobs.md` has no prune job.

5. **Fix the migration in the partial.** Name per `@.claude/rules/persistence.md`
   § Migrations, with `<N>` following the highest one found in step 2, and the target
   path under the module the blueprint gives the persistence role. The SQL goes as a
   fenced `sql` code block in block 4 of `20-persistencia.md`, headed by that path. Shape in
   `templates/V1__create_table.sql.example`. One migration per logical change; never
   edit one already applied. **Don't create the `.sql` file** — anything under `src/`
   belongs to the executor, which materializes it from this block.

6. **Fix the queries and access plan.** For each output port in `10-dominio.md`: the
   query, the fetch strategy, the index that serves it, and whether it's paginated.
   Every collection read inside a loop is an N+1 and is resolved here, not in code
   review — symptom catalog and fixes in `references/sql-tuning.md`.

7. **Fix the configuration.** The datasource and JPA properties for this project, from
   `templates/application-persistence.yml.example`. The mandatory values are the rule
   (`@.claude/rules/persistence.md` § Configuration); what this skill decides is sizing
   — pool size, timeouts, `batch_size` — based on the volume answered in step 3.

7b. **Decide the design patterns of this layer.** Run
   `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the adapters,
   mappers and queries this case adds, against the specs and what step 2 surveyed — a
   Specification `10-dominio.md` already decided reaching its query here, an adapter that
   would repeat an earlier one's skeleton. The answer goes into `## Design patterns` —
   `none` when nothing matches, and absence is not `none`.

8. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/20-persistencia.md`, from
   `templates/persistence-spec.md.example`. Six numbered blocks plus `## Design patterns`, all mandatory — § 6 · Declared
   dependencies written as `none` when this layer needs nothing the project lacks.

9. **Check the engine has a container.** List the keys inside the `services:` block and
   look for the engine chosen in step 3 — never `grep -A2 "^services:"`, which reads two
   lines and then reports the children of `volumes:` as services
   (lessons-learned-012 § 12):

   ```bash
   awk '/^services:[[:space:]]*$/{s=1;next} /^[^[:space:]#]/{s=0} s&&/^  [A-Za-z0-9_.-]+:[[:space:]]*(#.*)?$/{sub(/[[:space:]]*#.*$/,"");print}' docker-compose.yml
   ```

   Missing (and the engine isn't H2) → **record it** in the partial's § 6 as a pending
   service: the engine, the image tag the spec assumes, and the one-line
   `/docker-architect` invocation that materializes it. Do **not** invoke
   `docker-architect` and do not edit `docker-compose.yml`: that skill is the file's single
   owner, it is class `build`, and `ArchHook.java guard` refuses the call while a design run
   is open — a design run produces a spec, never a container.

10. **Report and stop.** Path of the partial written, divergences from `10-dominio.md`, the
    pending compose service if step 9 found one (and the command that fixes it), and what's
    missing for the folder to be complete (`30-rest.md`, `40-testes.md`). Don't invoke anyone
    else.

## What the partial contains

Six blocks. An empty block is written as "none" — deleting it hides a question nobody
asked.

| Block | Fixes | Form exemplar |
|---|---|---|
| Schema | Tables, columns, types, nullability, `UNIQUE`, foreign keys, indexes | `V1__create_table.sql.example` |
| Mapping | Aggregate → persistence entity, field by field; what's `@Embeddable`; value object translation; `@JdbcTypeCode` and `Persistable` where they apply | `JpaEntity.java.example` |
| Adapter and ports | Each port from `10-dominio.md`, the query serving it, the fetch strategy | `RepositoryAdapter.java.example` · `SpringDataRepository.java.example` |
| Migrations | New files, order, and the expand/contract pair when the table already exists | `V1__create_table.sql.example` |
| Configuration | Datasource and JPA properties, with the decided value and why | `application-persistence.yml.example` |
| Idempotency (only when `30-rest.md` requires `Idempotency-Key`) | The shared table, entity, repository, adapter, and application component — modeled once, reused by every later use case | `IdempotencyKeyTable.sql.example` · `IdempotencyKeyStore.java.example` · `IdempotentExecution.java.example` |
| Outbox (only when `25-mensageria.md` fixes publication Form B) | The shared `outbox_events` table, its mapping, the adapter implementing `OutboxRelayGateway` and `OutboxRetentionGateway`, the **claim strategy** that meets `35-jobs.md` § 3, the retention window and the prune's statement — modeled once, reused by every later event | `OutboxEventTable.sql.example` · `OutboxEventStore.java.example` |
| Declared dependencies | Build dependencies this layer needs and the project does not declare — the only list the executor may act on when it writes `pom.xml` | — |
| Design patterns | Each pattern the adapters, mappers or queries adopt, with its force, its classes and the "When not" checked — step 7b. `none` when none | `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use |
| Deferred | One row per item this partial decided **not** to do in this run: what was decided, what is missing, the norm that requires it (by path), and the intended owner — `checklist` (this run does it) or `backlog` (a later one does). `none` when nothing was deferred, and absence is not `none`. Consolidation resolves each row to a real owner and is what writes the `BACKLOG.md` line | — |

The exemplars in `templates/` are **reference for form**, not files to copy. It's the
executor agent that reads them when generating code.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. Writes inside the
use case folder and nothing else: no migration under `src/`, no service in the compose file,
both refused with exit 2.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md` and `10-dominio.md`
(mandatory — stops without the second), `@.claude/rules/persistence.md`,
`@.claude/rules/architecture-ddd.md` (Adapters and Composition sections),
`@.claude/rules/naming.md`, `@.claude/rules/error-handling.md`,
`@.claude/rules/lombok.md`, `@.claude/rules/value-objects.md`,
`@.claude/rules/api-rest.md` § Idempotency (only when step 4a applies),
`@.claude/rules/messaging.md` § Publication timing (only when step 4b applies), and the
active blueprint's `packages.map`. Also reads two partials whose schema requirements are
this pass's input, each mandatory under its own condition: `30-rest.md` for an
HTTP-triggered case (block 4), and `25-mensageria.md` whenever `10-dominio.md`'s Events
block names external delivery (§ 6 — the shared outbox table under Form B, a dedupe table
for a consumer). And `35-jobs.md` under Form B or a scheduled trigger (§ 3 replica count,
§ 6 tool tables, claim requirement and prune operation). Missing any of them where it's
required stops this skill instead of starting a design that a later pass would have to
revise.

**Writes** `docs/use-cases/UC-NNN-<slug>/20-persistencia.md`. Nothing else — the
migration SQL lives inside it.

**Never writes under `src/`.** Not a migration, not a class, not a property file. The
executor materializes every file there from this partial.

**Does not write Java code.** The entities, adapters, and repositories come from the
executor agent.

**Does not edit `docker-compose.yml`, and does not invoke `docker-architect` either.** When
step 9 finds the chosen engine has no container yet, it records the pending service in the
partial's § 6 with the `/docker-architect` command that creates it. The guard enforces both
halves: the file is outside this class's territory, and a `build`-class skill is unreachable
from inside a design run.

**Does not decide** the use case boundary (`00-caso-de-uso.md`), the domain model
(`10-dominio.md`), the transport (`30-rest.md`), or the tests (`40-testes.md`). Doesn't
touch `.claude/rules/**`.

**Does not collide with `messaging-architect`**: that one decides the publication form and
owns the relay pass, the appender, and the declaration of `OutboxRelayGateway` /
`OutboxEventRecord`. This one owns the `outbox_events` table, its mapping, and the adapter
implementing that port. A form choice is never made here — an outbox requirement that
contradicts `25-mensageria.md` is a divergence to report.

**Does not collide with `jobs-architect`**: that one decides when things run — the relay's
poll interval, the switch, coordination across instances, the prune's cadence — and declares
`OutboxRetentionGateway`. This one implements that port, owns the statement it runs, the
retention window, and the final form of every scheduling table `35-jobs.md` § 6 asks for.

**Does not collide with `domain-modeling`**: that one declares the output port, this one
says how it's served. The port's signature belongs to the other; if it needs to change,
report the divergence instead of rewriting it.
