---
name: database-documentation
version: 0.0.1
license: MIT
description: >-
  Generate grounded-and-verified, engine-agnostic database documentation that reaches 100% parity with the
  real schema. Introspects the LIVE database as ground truth and cross-validates it against ORM models,
  migrations, generated types, seeds, and application queries, then proves completeness by diffing the docs
  back against the database. Produces ER diagrams (mermaid), per-table data dictionaries, and a
  machine-readable schema.json. Works with PostgreSQL, MySQL, SQL Server, and SQLite across any ORM (Prisma,
  TypeORM, Drizzle, Sequelize, Knex, Django, Rails) or raw SQL. Use when asked to document a database,
  produce an ERD or data dictionary, write db/schema docs, audit schema drift, or refresh existing DB docs.
compatibility: >-
  Best results need read access to the live database (via a DB CLI, docker exec, or a connected DB MCP
  server) and, on platforms that support it, parallel subagents. Degrades gracefully without them.
---

# database-documentation

Document a database so completely and accurately that the docs are **provably** the schema, not a
plausible guess at it. A half-correct schema doc is worse than none: people trust it and write broken code.

## The one principle: grounded AND verified

Every statement in the output must be:
- **grounded** — traceable to a concrete source, preferring the **live database** (introspection of the
  system catalog). ORM models, migrations, generated types, and seeds are *claims about* the database, not
  the database; the catalog is what actually runs.
- **verified** — confirmed by re-introspecting the live database and diffing it against the generated docs
  until the diff is empty or every remaining difference is explicitly justified. Never write "documentation
  is complete" — instead make the diff empty and show it.

A frontier model left to itself reads the ORM, writes confident prose, and ships an **incomplete and
partly hallucinated** schema (missed check-constraint enums, wrong `ON DELETE`, omitted legacy tables,
invented columns). This skill exists to defeat exactly that. Two mechanisms do it: (1) the live DB is the
oracle, and (2) judgment is never one agent's call — independent adversaries hunt for what one pass misses.

## Scope (v1): relational/SQL only

Targets PostgreSQL, MySQL, SQL Server, SQLite. If you detect a document store (MongoDB) or graph database,
**say so and stop on that store** — do not emit relational docs for it (silent mis-documentation is the
worst outcome). Note it as out of scope rather than guessing.

## Workflow

Run these phases in order. Each names its exit artifact. Keep all scratch (intermediate extractions, the
working CSM) in a single `.database-documentation/` scratch dir or your platform scratchpad — the **only durable
deliverables are the docs and `schema.json`**.

### Phase 0 — Discover (read-only)

1. **Fingerprint** the engine + version and the ORM(s): look for `schema.prisma`, `*.entity.ts` +
   datasource, `drizzle.config.*`, `knexfile.*` + `migrations/`, Django `models.py`, Rails `schema.rb`,
   raw SQL DDL. Find the engine + version from the datasource/provider, `docker-compose.yml` image tags,
   and connection URLs in `.env*`.
2. **Find the live-DB reachability path**, trying in this order and stopping at the first that works:
   a connected **DB MCP server** → **`docker compose exec` / `docker exec`** into the DB container (read
   creds from compose env) → a **local DB CLI** (`psql`/`mysql`/`sqlcmd`/`sqlite3`) against host:port from
   `.env`. **Prove it** with one trivial query (`SELECT 1`, list tables) before continuing. If the DB is
   down but a compose file defines it, offer to start it. **Never print credentials**: treat passwords/DSNs
   read from `.env`/compose as secrets — keep them only in the command you execute, and **redact them**
   (`password=***`) in anything you show or write to the docs.
3. **Inventory every other surface**: migrations dir (+count), generated client/`*.d.ts`, seeds/fixtures,
   and grep the app for raw SQL / query-builder calls. Note existing `docs/db/` — if present this is a
   *refresh*: load it to diff for drift and to match house style.
4. **Announce the tier** you reached (see Degradation ladder) so the reader knows the confidence level.

Exit: a short discovery note — engine, ORM, reachability tier, the exact verified live-DB command, surface paths.

### Phase 1 — Extract every surface (parallel where possible)

Extract each available surface **independently** into the Canonical Schema Model shape
(see `references/csm-contract.md`). On platforms with subagents, run one extractor per surface in parallel,
and **do not let them see each other's output** — independent agreement is real evidence; shared context is
groupthink.

**Object-class checklist — extract EVERY class; skipping one is the most common failure.** Copy this list
and confirm each is present in `schema.json` with a live count:

- [ ] tables · [ ] columns (type+nullable+default+comment) · [ ] primary keys · [ ] foreign keys (+ON DELETE/UPDATE)
- [ ] unique constraints · [ ] check constraints · [ ] indexes (+partial/expression) · [ ] enums (+values)
- [ ] **sequences** · [ ] **triggers** · [ ] **views** (+definition) · [ ] routines (functions/procedures)

Sequences, triggers, and routines are routinely forgotten because they are not columns — extract them explicitly.
Capture view / trigger / routine **bodies in full and verbatim** — never abbreviate, summarize, or elide
with `...`; a truncated definition is an incomplete (wrong) doc.
**`schema.json.enums` = DB-NATIVE enum types only.** A string column with a `CHECK (col IN (...))` goes under
that table's `check_constraints` (not `enums`); an app-level-only value set goes in the column description
marked "app-enforced". Putting a non-native enum in `enums` is a hallucination against the live schema.

- **Live introspection (authoritative).** Read the full catalog. See `references/introspection-postgres.md`
  for the exact Postgres queries (and the MySQL/MSSQL/SQLite equivalents); they cover tables, columns
  (type with length/precision, nullability, default, identity, generated, collation, comment), primary
  keys, foreign keys **with `ON DELETE`/`ON UPDATE`**, unique + **check** constraints, indexes (**partial
  predicates and expression columns included**), enums, domains, sequences, views/matviews, triggers,
  routines. Do NOT shell out to any benchmark/oracle script — write and run the introspection yourself.
- **ORM models** → CSM (intent + descriptions; per-ORM notes in `references/`).
- **Migrations** → fold them in timestamp order to reconstruct *final* state (do not eyeball 200 files).
- **Generated types / seeds / app queries** → corroborate; the app-query scan catches tables/columns used
  but absent from the ORM (legacy tables).

Exit: one partial CSM per surface.

### Phase 2 — Reconcile to one CSM (precedence + drift)

Merge into a master CSM, keying tables by physical DB name. Precedence:
1. **Live DB present → it wins, full stop.** Any surface that disagrees produces a **drift finding** (recorded
   in `issues/`), never a silent edit to the docs. The docs describe the live database.
2. **No live DB → consensus of migrations ⊕ ORM** (migrations win structure, ORM wins intent); flag conflicts.

Tag each object's `confidence`: `verified` (live-confirmed) / `consensus` / `single-source` / `conflict`.
Where you have a live DB, cross-check it against itself via two methods (e.g. `information_schema` vs
`pg_catalog`) — the oracle must agree with itself before overruling other surfaces.

Exit: master CSM + a `discrepancies` list.

### Phase 3 — Generate docs + schema.json

Write all output into one **dedicated docs directory** — never scatter files across the repo. Default to
`docs/db/`; if Phase 0 found an existing DB-docs directory (e.g. `docs/db/`, `docs/database/`,
`docs/schema/`, or wherever the repo already keeps them), write there instead to match house style. Create
the directory if absent. Render the CSM (a pure function of it) into it, matching the template in
`references/output-template.md`, **sized to the schema**:
- **≤ ~15 tables** → a single `docs/db/DATABASE.md` (stats header, one mermaid ERD, per-table sections, an Issues section).
- **larger** → under `docs/db/`: `README.md` (index + stats) + `ONBOARDING.md` + `diagrams/<domain>.md` per
  domain (mermaid `erDiagram` with all columns+types + relationship lines, then per-table sections) +
  `diagrams/full-erd.md` (table-level only, so it stays renderable) + `tables/entity-reference.md` + `issues/README.md`.

Emit `schema.json` into that same directory (`docs/db/schema.json`).

Per-table section: 1–2 sentence **evidence-based** description, a `Column | Type | Nullable | Default |
Description` table, then **Indexes:** and **Foreign Keys:** (with `ON DELETE`). Partition domains by ORM
module/folder → name prefix → FK clustering, with a Legacy/Misc catch-all. The `schema.json` follows the
shape in `references/csm-contract.md`.

### Phase 4 — Prove parity (the verified half)

This is not optional and not a vibe. A *claimed* "looks complete" is worthless. Weak models in particular
will assert parity they did not achieve; do not trust the assertion, run the numbers.

1. **Count gate (early tripwire).** For EVERY object class, count it in the live DB and compare to the count
   in your `schema.json`. **The count query MUST select the exact same population your extraction and the CSM
   define** — otherwise a correct doc fails the gate and you will "fix" it by hallucinating. Two rules that
   bite on every real database: indexes **exclude** PK/unique-constraint-backing ones, and routines/objects
   **exclude** extension-owned ones (`pg_depend.deptype='e'`). Use the population-matched count queries in
   `references/introspection-postgres.md` ("Count-gate queries") — NOT a naive `count(*)`, and never a lossy
   view (e.g. `information_schema.check_constraints` is polluted with NOT NULL rows; `reltuples` may be `-1`).
   Print a `class | live | documented | match?` table. A mismatch means investigate — it may be a real
   omission, or your count query selecting the wrong population. **Counts matching is necessary, not
   sufficient** (equal counts hide swapped types / wrong `ON DELETE`).
2. **Identity-diff (the actual proof).** Re-introspect fresh and diff *identities and attributes*, not just
   counts, over every class: tables, columns (name/type/nullable/default), PKs, FKs (+on_delete), uniques,
   checks, indexes (+partial/expression), enums (+values), views, triggers, routines, sequences.
3. For every difference: **fix the docs**, or **justify it** (e.g. "live-only object listed under Drift").
4. Repeat until the count table matches AND the identity-diff is empty or fully justified.
5. Write a **Parity Report** (in `README.md` or `issues/`): the per-class count table + an explicit
   "0 undocumented, 0 invented". **Only write "verified" when the identity-diff (step 2) is empty** — not on
   a count match alone. With no live DB, run the diff against the consensus CSM and label every output file
   "consensus parity (UNVERIFIED against live DB)".

### Phase 5 — Adversarial review (≥3 independent, never one)

Because the agent doing the judging is itself a frontier model with the same blind spots as the agent that
wrote the docs, a single review rubber-stamps. Convene **≥3 context-walled adversaries**, each in a distinct
session with a must-find-fault mandate and a different lens:
- **omission hunter** — sample live tables: is each present with every column? Are legacy tables, every
  enum/CHECK, every index and FK documented?
- **hallucination hunter** — does every documented object/type/default/`ON DELETE`/description trace to a
  real source? Flag anything invented.
- **correctness hunter** — do types, nullability, and FK cardinality match the live DB exactly?

Their union feeds another generation pass. Wherever judgment is needed, it is a panel decision.

## Degradation ladder (announce your tier)

| Tier | Have | Confidence |
|---|---|---|
| T1 | live DB + parallel subagents + adversaries | verified, provable |
| T2 | live DB, single agent | verified, sequential |
| T3 | no live DB, subagents | consensus, unverified |
| T4 | no live DB, single agent | consensus, unverified |
| T5 | one static surface only | low — prominent "UNVERIFIED — no live DB" banner |

Subagents, MCP, and docker are optimizations, never requirements — the same phases run inline without them.
**Never fabricate** data you could not read: missing is flagged, not guessed.

## References
- `references/csm-contract.md` — the `schema.json` shape (the verifiable output contract).
- `references/introspection-postgres.md` — exact catalog queries per engine.
- `references/output-template.md` — the human doc shape to reproduce.
- `references/hard-cases.md` — enums (native/CHECK/app), JSON columns, polymorphic relations, soft-deletes,
  composite keys, partial/expression indexes, views, multi-schema, citext/collation, legacy tables.
