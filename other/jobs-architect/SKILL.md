---
name: jobs-architect
description: >
  Designs the scheduled and background jobs of an already-scoped use case — which scheduling
  technology (@Scheduled, ShedLock, Quartz, Spring Batch, db-scheduler, JobRunr), trigger and
  cadence, coordination across instances, overlap and missed-run policy, on/off property and
  job metrics — into the `35-jobs.md` partial. Owns the transactional outbox's relay schedule
  and its prune job. Use when the request involves a cron or recurring job, a scheduled task,
  a batch run, a background job, ShedLock, Quartz, Spring Batch, a job running twice across
  replicas, a job that must catch up after downtime, or pruning/retention of a table. Piece of
  the `/new-feature` pipeline: requires `00-caso-de-uso.md` in the given folder plus a
  schedule trigger, a Form B outbox in `25-mensageria.md`, or a deferred scheduled job — and
  stops without one of them.
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

# Jobs Architect

Designs **what runs on its own clock and how it stays correct when nobody is watching**: which
scheduling technology the project uses, what fires each job and how often, what keeps two
instances from running the same pass, what happens to a run missed during downtime, and how
anyone finds out a job stopped. What `use-case-design` accepted as a "job, schedule" trigger,
and what `messaging-architect`'s Form B needs to actually deliver, this skill gives a schedule
to.

**Entry rule: a job needs something to run and a reason to run on a clock.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md` and runs only when at least one holds:

| Source | Condition | What it designs |
|---|---|---|
| `00-caso-de-uso.md` | The trigger is a schedule, a recurring run, a batch, or a background job | That job, calling the inbound port `10-dominio.md` declared — so `10-dominio.md` is required too |
| `25-mensageria.md` | § 2 chose **Form B** (transactional outbox + relay) | The relay's schedule and the prune job — once per project, reused by every later case |
| Any partial's `Deferred` block | A row names a scheduled job as the missing piece | That job |

None holds → stop and say so: a use case triggered by a request or a message has no schedule to
design, and designing one anyway is scope nobody asked for.

**Exit rule: it doesn't write code.** It emits `35-jobs.md`. The Java classes come from the
executor agent, which reads the partial and the `templates/` exemplars.

**Rule rule: the rules don't live here.** Trigger shape, gating, coordination, lock bounds,
bounded passes and job metrics are `@.claude/rules/scheduling.md`. This skill applies and cites
it; it doesn't reproduce it.

## How it's invoked

Two paths: `/jobs-architect` by hand, or chained by `/new-feature` after messaging and before
persistence. That's why it does **not** carry `disable-model-invocation` — a skill the model
can't see is a skill the orchestrator can't call (`@.claude/decisions/0007-pipeline-skills-invocation.md`).
The guard against firing out of order is the entry rule above.

## Why this is a skill and not a subagent

Form 1, motivated by axis 9 of the designer's interview: the outbox's prune job was left
without an owner in two runs (lessons-learned-014 § 9), because scheduling was split between an
exemplar comment in `messaging-architect` and a `Deferred` row in `persistence-architect`, and
no piece decided the technology at all. The closest rejected form was extending those two skills
— it left every job not born from the outbox without an owner and split one concern,
coordination across instances, over two skills that would each re-derive the replica count. A
subagent fails the counter-test on all three points: the interview is the task, the reference
fits in `references/` and `templates/`, and the partial is short.

Pinned to `opus`: the partial is what the executor implements verbatim, and the pin holding for
the rest of the turn keeps `/new-feature` on the model that designed it
(`@.claude/decisions/0081-skill-model-required-per-class.md`). Design record:
`@.claude/decisions/0087-jobs-architect-skill.md` (this repository only).

## Boundary with neighboring skills

| Piece | Decides | Never decides |
|---|---|---|
| `use-case-design` | That the trigger is a schedule, and the job's boundary | Technology, cadence, coordination |
| `domain-modeling` | The inbound port the job calls | When it is called |
| `messaging-architect` | The relay's **form** (outbox + relay, or none), its broker side, and the delivery guarantee it owes | The relay's schedule, its coordination, the prune |
| **this skill** | Technology, trigger and cadence (the relay's poll interval included), coordination across instances, overlap and missed-run policy, on/off property, job metrics, **the prune job** | Tables, columns, claim query, retention window, the statements a job runs |
| `persistence-architect` | The outbox table, the claim query and its strategy, attempt ceiling and batch size, the retention window, the prune's `DELETE`, the final form of every tool table this skill asks for | When any of it runs |
| `test-architect` | Which test proves each job, at what level | — |

Two facts cross that line, one in each direction, and each has one owner:

- **The replica count** is this skill's § 3. Persistence reads it to choose the claim strategy;
  it does not ask again.
- **The retention window** is persistence's. This skill names the property the prune job reads
  (`app.outbox.prune-after`); the value and its reason are `20-persistencia.md` § 1's. Because
  the job and the property are designed in the same run, the property ships with its reader —
  `@.claude/rules/scheduling.md` § Retention.

## Procedure

1. **Read the specs.** `00-caso-de-uso.md`, `10-dominio.md` when the trigger is a schedule,
   `25-mensageria.md` when it exists, and the `Deferred` block of every partial already in the
   folder. Apply the entry rule; list the jobs this run designs.

2. **Survey — every answer the project already gave is inherited, never re-asked.**

   ```bash
   # Technology already in the build
   grep -nE "shedlock|spring-boot-starter-quartz|spring-boot-starter-batch|db-scheduler|jobrunr" pom.xml
   # Jobs already in the code
   grep -rnE "@Scheduled|@SchedulerLock|implements Job\b|@Recurring|RecurringTask|JobBuilder" --include='*.java' src/main 2>/dev/null
   grep -rln "@EnableScheduling" --include='*.java' src/main 2>/dev/null
   # Decisions earlier use cases recorded
   find docs/use-cases -name '35-jobs.md' 2>/dev/null
   grep -rn "Claim strategy\|Replicas" docs/use-cases/*/20-persistencia.md docs/use-cases/*/35-jobs.md 2>/dev/null
   ```

   And the active blueprint's `packages.map` entry ending in `.scheduling` — the package every
   trigger goes to. No such entry → stop and say which line is missing from the blueprint,
   instead of choosing a package inside this use case.

   | Fact | Inherited from | Asked only when |
   |---|---|---|
   | Scheduling technology | A dependency in `pom.xml`, or an earlier `35-jobs.md` § 2 | Neither exists — first job of the project |
   | Replica count | An earlier `35-jobs.md` § 3, else an earlier `20-persistencia.md` § 1 `Claim strategy` (documented single instance → 1; lease or `SKIP LOCKED` → more than one) | Neither exists |
   | Relay and prune jobs | A relay trigger already in `src/main` or an earlier `35-jobs.md` naming them | The project's first Form B — later cases reuse them and record the reuse |
   | Delivery guarantee the relay owes | `25-mensageria.md` § 2 / § 6 | Never — that partial owns it |

   **The relay in its pre-split shape is not reuse.** A project generated before
   `@.claude/decisions/0087-jobs-architect-skill.md` has `@Scheduled` on an `OutboxRelay` and a
   `SchedulingConfig` inside the messaging adapter. Adding `OutboxRelayJob` next to it gives two
   triggers over the same rows and two registrations of the same meters. Record it in
   `## Impact on approved use cases` and decide with the user between migrating it in this run
   (pass behind `RelayOutboxEvents`, old trigger and config deleted, the job takes the meters)
   and deferring the migration with an owner, leaving the old relay untouched — never both
   shapes at once. `templates/OutboxRelayJob.java.example`, note on the pre-split shape.

   A later case that inherits the technology and finds its jobs already built writes a short
   partial that says so, row by row, citing where each answer came from. That is not a skipped
   run: it is the record that nothing new is scheduled.

3. **Interview — only what step 2 did not settle.** `AskUserQuestion`, at most 4 questions per
   call and **never fewer than 2 real options** per question; an axis with one sensible answer
   is decided and recorded, not asked (`@CLAUDE.md` § Known pitfalls).

   | Axis | Decides | Skip when |
   |---|---|---|
   | **Replicas** — how many instances run this application in production? | Coordination (§ 3); the claim strategy persistence will pick | Step 2 inherited it |
   | **Kind** — polling pass, calendar-anchored job, bulk run over many rows, fire-and-forget background task, schedule created at runtime from data | The column family in the matrix | `00-caso-de-uso.md` already says it |
   | **Missed run** — after downtime, is the missed fire skipped or caught up? | Whether a persistent scheduler (misfire) or a watermark is needed | The job is a polling pass: the next pass is the catch-up |
   | **Volume and restart** — how many rows per run, and if it fails halfway, does a rerun from zero cost something? | Spring Batch or not | Volume is one batch per pass |
   | **Retry per execution** — does a failed run need its own backoff, or is the next scheduled run the retry? | Whether the tool must carry retry | Polling pass — the next pass retries |
   | **Operator control** — must someone pause, trigger by hand, or inspect runs without a deploy? | Whether a dashboard is a requirement (JobRunr) or actuator is enough | Nobody asked for it in `00-caso-de-uso.md` |
   | **License** — only when JobRunr is still a candidate after the rows above | LGPL OSS, or rule it out | JobRunr already eliminated |

   Every question states the cost in its option text — the tables a tool adds, the license, the
   dependency — the same way `messaging-architect` puts the schema-registry cost inside its
   question. A tool chosen from its name alone is how a project ends up with Quartz's eleven
   tables for one nightly job.

4. **Choose the technology.** Apply `references/tool-decision-matrix.md` § 2 to the answers:
   the first tool that satisfies every must-row wins; a tie goes to the one already in
   `pom.xml`, then to the one with less infrastructure. **One technology per project**
   (`@.claude/rules/scheduling.md` § Boundary) — a case whose needs the project's current tool
   cannot meet is a divergence to report and ask about, never a second scheduler added
   silently. Record the winner, the rows that decided it, and one line per rejected tool.

5. **Design each job.** One row of § 1 per job, and every column is filled:

   | Column | Content |
   |---|---|
   | Job | Class name, in the `.scheduling` package — e.g. `OutboxRelayJob` |
   | Kind | From step 3 |
   | Calls | The inbound port — the trigger has no other dependency on business code |
   | Trigger | `fixedDelay`, `fixedRate` (with the reason), or `cron` with its `zone` |
   | Cadence property | e.g. `app.outbox.poll-interval: PT1S` — the placeholder is the only reader |
   | On/off property | e.g. `app.outbox.enabled`, default on, `false` in the test profile |
   | Coordination | From § 3 — claim, lock, or single-instance constraint |
   | Missed run | skipped / caught up, and how |
   | Per pass | batch bound, and what one failing item does to the rest |

   **Form B's two jobs** have fixed shapes, in `templates/OutboxRelayJob.java.example` and
   `templates/OutboxPruneJob.java.example`:

   - **Relay.** Calls the relay's inbound port (`RelayOutboxEvents`, declared in
     `messaging-architect/templates/OutboxRelayPublisher.java.example`). Always `@Scheduled`,
     whatever step 4 chose for the other jobs (`references/tool-decision-matrix.md` § 3). Coordination follows
     the replica count: one instance → the claim may stay unlocked, **and § 6 says so** as a
     requirement to persistence (documented single instance); more than one → § 6 requires a
     locked or leased claim, and no lock goes around the trigger — the claim partitions the
     work, and a lock on top would make every instance but one idle
     (`references/tool-decision-matrix.md` § 3).
   - **Prune.** Cron, off-peak, explicit zone, deleting in batches until a pass deletes fewer
     than the batch. Reads `app.outbox.prune-after`, whose value `persistence-architect`
     decides. Calls `PruneOutboxEvents`, whose service loops over one outbound operation —
     `OutboxRetentionGateway.deletePublishedBefore(cutoff, limit)`, declared in this skill's
     exemplar and implemented by persistence — named in § 6 as a requirement, never as SQL.

   Every other job takes its shape from the template of the chosen technology:

   | Technology | Exemplar |
   |---|---|
   | `@Scheduled` alone | `templates/ScheduledJob.java.example` |
   | `@Scheduled` + ShedLock | `templates/ShedLockJob.java.example` |
   | Quartz, JDBC clustered | `templates/QuartzJob.java.example` |
   | Spring Batch (fired by one of the above) | `templates/SpringBatchJob.java.example` |
   | db-scheduler | `templates/DbSchedulerTask.java.example` |
   | JobRunr | `templates/JobRunrJob.java.example` |
   | Kubernetes `CronJob` / external | none — record the decision; the job is a use case with a CLI or HTTP entry, and the schedule is platform configuration |

   Configuration shape for all of them: `templates/application-jobs.yml.example`.

6. **Fix observability.** Per job: the execution timer and the last-success gauge
   `@.claude/rules/scheduling.md` § Observability requires, with their metric names. Under Form B
   the relay's two delivery metrics (`outbox.events.dead_lettered`, `outbox.pending.age.seconds`)
   keep the names and alarms `messaging-architect` gave them; `OutboxRelayJob` is where they are
   recorded, from each pass's outcome, because every pass goes through it. This block lists them
   and does not rename them.

7. **Hand persistence what it needs — § 6, requirements only.** This skill runs **before**
   `persistence-architect`, so § 6 is input to that skill's first pass:

   - the tables the chosen technology needs (`shedlock`, `QRTZ_*`, `BATCH_*`,
     `scheduled_tasks`, JobRunr's) — named by what they are, with the vendor's DDL as the
     source; persistence writes the migration, and the tool's own schema initialization stays
     off;
   - under Form B, the **claim requirement** derived from § 3 (documented single instance, or
     locked/leased) — persistence picks between lease and `SKIP LOCKED` and writes it as its
     `Claim strategy`;
   - under Form B, the prune's bounded delete operation.

   Never a column name, never DDL — the same discipline `messaging-architect` step 4a keeps
   for the outbox.

8. **Declare dependencies — § 7.** Coordinates from the matrix, version column empty whenever
   the Boot parent manages it, and never a version from memory (`@CLAUDE.md` invariant 8). Where
   the artifact differs per Boot major (db-scheduler, JobRunr), read the parent version in
   `pom.xml` and name the matching artifact. `@Scheduled` alone needs none. The executor may
   write `pom.xml` for exactly these rows.

8b. **Decide the design patterns of this layer.** Run
   `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the jobs this case
   adds, against the specs and what step 2 surveyed — several jobs sharing one
   claim-process-mark skeleton is the usual symptom. The answer goes into `## Design
   patterns` — `none` when nothing matches, and absence is not `none`.

9. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/35-jobs.md`, from
   `templates/jobs-spec.md.example`. Nine numbered blocks plus `## Design patterns`, all mandatory, each written as `none` when
   there is nothing — absence is not `none`. § 9 `Deferred` follows the same shape as every other
   partial's: what was decided, what is missing, the norm requiring it by path, and the owner.

10. **Report and stop.** Path of the file written; the technology and the rows that chose it;
    the replica count **and where it came from** (inherited, or asked in this run); the content
    of § 6 (each requirement handed to `persistence-architect`) and of § 7 (each dependency);
    and, when a job exists whose failure nothing would notice — no gauge, no alarm — that as a
    finding. Don't invoke anyone else: `persistence-architect` runs next and reads § 3 and § 6
    in its first pass.

## What the partial contains

| Block | Fixes |
|---|---|
| 1 · Jobs | One row per job, every column of step 5 |
| 2 · Technology | The tool, the matrix rows that decided it, the rejected ones in one line each, and whether it was inherited |
| 3 · Coordination | Replica count and its source; per job, claim / lock / single-instance constraint; lock bounds when a lock exists |
| 4 · Execution guarantees | Missed-run policy, idempotency of the body, bounds per pass, per-item failure handling |
| 5 · Observability | Metric names per job, and the alarm each one exists for |
| 6 · Schema requirements | Tool tables, the Form B claim requirement, the prune's delete operation — requirements, never DDL. `none` when none |
| 7 · Declared dependencies | Coordinates, version empty when managed. `none` when none |
| 8 · Configuration | Every property a job reads, its value, and which partial owns the value |
| 9 · Deferred | Same shape as every partial. `none` when nothing was deferred |
| Design patterns | Each pattern the jobs adopt, with its force, its classes and the "When not" checked — step 8b. `none` when none |

Plus `## Impact on approved use cases` and `## Implementation order`, as in every partial.

The exemplars in `templates/` are **reference for form**, not files to copy.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json`, and `ArchHook.java guard` enforces it. Writes inside the use
case folder and nothing else.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md` (mandatory), `10-dominio.md` (when the
trigger is a schedule), `25-mensageria.md` (when present), every partial's `Deferred` block,
earlier cases' `35-jobs.md` and `20-persistencia.md` § 1, `pom.xml`, the active blueprint's
`packages.map`, `@.claude/rules/scheduling.md`, `@.claude/rules/architecture-ddd.md`,
`@.claude/rules/observability.md`, and `references/tool-decision-matrix.md`.

**Writes** `docs/use-cases/UC-NNN-<slug>/35-jobs.md`. Nothing else.

**Owns** the scheduling technology of the project, each job's trigger and cadence — the relay's
poll interval included — coordination across instances and the replica count it rests on,
overlap and missed-run policy, on/off properties, job metrics, and the outbox prune job.

**Does not decide** the relay's form or its broker side (`25-mensageria.md`), any table, column,
claim query, retention window or statement (`20-persistencia.md`), the use case boundary
(`00-caso-de-uso.md`), or the tests (`40-testes.md`). Does not write Java, `pom.xml`, or
`application.yml` — the executor does, from this partial. Doesn't touch `.claude/rules/**`.
