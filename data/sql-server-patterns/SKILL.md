---
name: sql-server-patterns
description: "Inject SQL Server schema-design knowledge into a task before the schema is written — partitioning, hierarchy modelling, SARGability, compression and temporal tables — by routing to .claude/templates/tsql-patterns.md rather than restating it. Distinct from migration-safety-reviewer (will this migration run cleanly on existing data?) and sql-performance-reviewer (is this existing query fast?): this one decides the SHAPE. Use when: user says /sql-server-patterns, asks how to model or index a table, proposes partitioning or a hierarchy, or when data-architect is designing persistence and dotnet-backend-architect is about to write an entity, configuration or migration."
user_invocable: true
---

# /sql-server-patterns — Schema Design Knowledge

The knowledge layer three other actors defer to. It does not review code and it does not
write migrations; it decides what the schema should **look like**, before either exists.

**Where it sits:**

```
/design-first → data-architect            owns the data contract
                  ↑ consults
            /sql-server-patterns           ← this skill: the SHAPE
                  ↓ hands off
        dotnet-backend-architect           writes entity, configuration, migration
                  ↓ audited by
  migration-safety-reviewer + sql-performance-reviewer
```

## Context — why this skill exists

Three shipped assets name this skill as the place schema-design knowledge comes from, and
each one names it to say what they are *not*:

- `migration-safety-reviewer` — *"Distinct from schema-design work (handled via
  `/sql-server-patterns` skill + `dotnet-backend-architect`) — this one asks 'will this run
  cleanly on the current DB without locking, breaking, or losing data?'"*
- `sql-performance-reviewer` — *"Distinct from schema-design work … this one reviews existing
  code against the prod data reality."* And at its step 4: *"Do NOT redesign the contract —
  that's `data-architect`'s job (schema design knowledge is injected via the
  `/sql-server-patterns` skill)."*
- `/debug` — routes *"SQL / index / migration perf → `dotnet-backend-architect` with
  `/sql-server-patterns` skill (+ `sql-performance-reviewer` to audit)."*

Those three boundaries only hold if something occupies the middle. Without it, the reviewers
are told to refuse schema redesign and there is nowhere to send it, so the redesign happens
anyway — inside a review, by an agent explicitly instructed not to do it.

**Hard rule: this skill consults `.claude/templates/tsql-patterns.md`; it never restates it.**
The template says so in its own first paragraph. A pattern copied into this file is a second
copy of a closed set, and the two drift the moment one is corrected — the same defect
`work-item-conventions.json` exists to prevent between `/task` and `/ship`.

## Step 0: Establish the boundary before answering

Decide which question is actually being asked. Answering the wrong one is this area's
characteristic failure, because all four sound like "a database problem".

| The question | Owner | Not this skill because |
|---|---|---|
| What shape should this data have? Partition? Hierarchy? Temporal? | **this skill** | — |
| Does this migration run safely against existing production data? | `migration-safety-reviewer` | the shape is already decided; this is about the transition |
| Is this existing query or index fast enough? | `sql-performance-reviewer` | the shape is already shipped; this is measurement |
| What are the entities, invariants and vocabulary? | `data-architect` | domain modelling precedes storage modelling |

If the answer is one of the lower three rows, say so and route there. **Do not redesign a
shipped schema from inside this skill** — that is a new work item and belongs at `/task`.

## Step 1: Read the pattern reference

```
.claude/templates/tsql-patterns.md
```

It carries five sections, each with runnable T-SQL and an explicit *when to* / *when not to*:

| Section | Decides |
|---|---|
| **Table partitioning** | whether to partition, on what key, and the two rules that make it legal |
| **Hierarchical data — 4 options** | adjacency list vs path enumeration vs nested sets vs `hierarchyid` |
| **SARGable vs non-SARGable predicates** | whether a predicate can use an index at all |
| **Data compression** | `ROW` vs `PAGE`, and per-partition hot/cold tiering |
| **Temporal tables (system-versioned)** | whether history belongs in the engine or the domain |

Read the section that bears on the task and **quote its thresholds back**, rather than
paraphrasing them. The thresholds are the load-bearing part: "partition when the table
exceeds ten million rows *and* is growing *and* queries filter on the key" is a conjunction,
and dropping any clause turns a sound rule into a bad default.

> **Under a plugin install the path differs.** When these assets arrive as an installed
> plugin rather than vendored copies, the template lives in the provider's plugin cache, not
> in the consuming repository. If `.claude/templates/tsql-patterns.md` is not present, say
> the reference is unavailable and stop. **Do not reconstruct the patterns from memory** —
> an invented partitioning threshold is worse than no answer, and this is a known gap the
> README records under Known limitations.

## Step 2: Apply the patterns to the actual task

Four rules that turn a reference into a decision:

1. **Default to not using the fancy pattern.** Partitioning, temporal tables and
   `hierarchyid` all carry ongoing cost. The template gives a *don't* list for each and it is
   the more useful half. A table under a million rows does not want partitioning, and saying
   so is a complete answer.
2. **Name the trade you are making.** Every pattern buys something and charges for it —
   partitioning buys elimination and archival and charges a key constraint on every unique
   index; compression buys space and charges CPU. State both sides, in the contract or the
   handoff, so the reviewer downstream can check the charge was worth it.
3. **Check the predicate before adding the index.** A non-SARGable predicate cannot use an
   index no matter how well chosen, so an index added under one is dead weight that still
   costs write throughput. The SARGability section runs before the indexing decision, not
   after it.
4. **If the pattern is not in the template, it is not established here.** Say the reference
   does not cover it, give the reasoning explicitly as reasoning, and consider whether the
   answer earns a new template section — see Step 4.

## Step 3: Safety — this skill talks about databases, never to them

The destructive-database doctrine binds here in full, and this is the skill most likely to
tempt a violation, because "let me just check the row count" is one keystroke from a
production connection.

- **This skill issues no `CREATE`, `ALTER`, `DROP` or `TRUNCATE` against any real database.**
  It produces T-SQL for a human or an implementer to apply through a migration.
- **Verifying a migration uses a separate disposable database**, never the one named by
  `appsettings.json` or its equivalents. The allow-listed suffixes are `_DryRun`,
  `_MigrationVerify`, `_Sandbox`, `_Scratch`, `_Throwaway`, `_Test_<hex-guid>` and
  `_e2e_<hex-guid>`. `db-destructive-guard.py` recognises these and permits the operation
  only when one is present.
- **Any read against a real database for sizing or cardinality is read-only at the connection
  layer** — `ApplicationIntent=ReadOnly` for SQL Server — and wrapped in
  `BEGIN TRAN; … ROLLBACK;`. `db-research-readonly-guard.py` blocks a connection carrying
  write keywords without that enforcement.
- **Never set `CLAUDE_DESTRUCTIVE_DB_OK`.** That variable is the user's, and an agent setting
  it is an agent disabling its own guard.

Both guards **fail closed**: with no `db-destructive-guard.rules.json` naming this project's
databases, every database is treated as protected. If a legitimate operation is blocked, the
fix is to fill in that rules file, never to bypass the hook.

## Step 4: Hand off, and grow the reference

### Handing off

This skill's output is input to someone else. Give them:

```
SCHEMA DECISION: <the shape chosen, in one line>
PATTERN: <which tsql-patterns.md section, by heading>
TRADE: <what it buys / what it charges>
THRESHOLDS MET: <the conjunction, each clause with the actual number>
REJECTED: <the alternatives considered and why not — especially the do-nothing one>
APPLY VIA: <migration | entity configuration | index only>
AUDIT: <migration-safety-reviewer | sql-performance-reviewer | both>
```

`dotnet-backend-architect` implements it; the named reviewer audits it afterwards. Under
`/design-first` this block belongs in the concept contract's data-shape section, so
`contract-critic` can see the trade before the user approves it.

### Growing the reference

When a task needs a pattern the template does not carry, and the pattern is genuinely
reusable rather than this schema's peculiarity, **append a section to
`.claude/templates/tsql-patterns.md`** in the same change — same shape as the existing five:
runnable T-SQL, an explicit *when to*, and an explicit *when not to*. Then add a row to
Step 1's index here.

Two constraints on that append:

- **Write no project's names into it.** The template is a generic asset. Use neutral table
  names; a schema-shaped fact that belongs to one project belongs in that project.
- **The *when not to* is not optional.** A section without one reads as a recommendation and
  will be applied by default, which is how a million-row table ends up partitioned.

## Anti-patterns (halt immediately)

- **Restating the template's SQL in this file, in a contract, or in a chat answer instead of
  citing the section.** Two copies of one pattern is a drift generator, and the template's own
  first paragraph forbids it.
- **Reconstructing a threshold from memory when the template is unreachable.** An invented
  "partition above a million rows" is confidently wrong and will be believed.
- **Redesigning a shipped schema from inside a review.** Both SQL reviewers are explicitly
  instructed to refuse this and to route here; routing here means a new work item, not an
  in-place redesign.
- **Recommending a pattern without its charge.** Partitioning constrains every unique index
  on the table. A recommendation that omits that is not a recommendation, it is a surprise.
- **Adding an index under a non-SARGable predicate.** It cannot be used and it still slows
  every write.
- **Touching a real database.** This skill produces T-SQL; it does not execute it. Migration
  verification uses a disposable database with an allow-listed suffix.
- **Setting `CLAUDE_DESTRUCTIVE_DB_OK` to get past a guard.** That variable belongs to the
  user.

## When NOT to use this skill

- The database is not SQL Server. The patterns are engine-specific — partition schemes,
  `hierarchyid` and system-versioning have no portable equivalent.
- The question is about an existing query's speed (`sql-performance-reviewer`) or an existing
  migration's safety (`migration-safety-reviewer`).
- The question is domain modelling rather than storage modelling. Entities and invariants come
  first, at `data-architect`; a storage decision made before the domain is settled gets made
  twice.

## Skill integrations

- **Reads** `.claude/templates/tsql-patterns.md` — the single source for every pattern, never
  duplicated here.
- **Consulted by** `data-architect` while designing persistence, so the contract carries the
  schema trade explicitly.
- **Hands off to** `dotnet-backend-architect`, which writes the entity, the EF Core
  configuration and the migration.
- **Precedes** `migration-safety-reviewer` and `sql-performance-reviewer`. Both name this
  skill as the owner of the schema-design question they decline.
- **Routed to by** `/debug` for SQL, index and migration performance work.
- **Bound by** `db-destructive-guard.py` and `db-research-readonly-guard.py`, which enforce
  Step 3 at the tool layer rather than trusting it to be remembered.
