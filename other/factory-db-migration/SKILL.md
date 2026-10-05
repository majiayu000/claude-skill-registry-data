---
name: factory-db-migration
description: The operational discipline for running a destructive change against a production database — schema migrations, data backfills, one-shot RPCs, historical seed imports. Adjacent to `factory-data-layer.md` (schema design) and `factory-deployment.md` (where migrations execute in CI) — this skill is about the runbook around the act of mutating prod. Covers the three-stage write contract (preflight → mutate → verify → rollback), idempotency by natural key, layered backup independence (Layer C from `factory-security.md` / KAI-126 doctrine), human-gated execution, bidirectional update semantics, validation-at-parse-not-at-constraint, and the failure modes a senior DB engineer pattern-matches before opening a migration PR.
---

# Factory DB migration

This skill is the runbook discipline for making a destructive database change. It is invoked **before** the first time a migration, backfill, or seed touches prod — and re-invoked on every periodic re-import.

The factory ships `factory-data-layer.md` for *how schemas are designed* and `factory-deployment.md` for *where migrations execute in CI*. This skill is the third leg: **how to run the change safely once both upstream pieces are in place.** Read all three before proposing a non-trivial prod write.

## How to use this skill

- **Before any first-of-its-kind destructive prod write** — read the Principle of each section. If you can't articulate the principle in your own words, you don't yet understand the change well enough to ship it.
- **During design review** — use the section list as a checklist: do we have preflight? Idempotency proof? Rollback? Pre-write snapshot? Human gates?
- **During incident response** — `factory-pitfalls.md` indexes the failure modes here; jump to the one that matches.

## The data is ground truth — the schema accommodates it

**Principle.** When a constraint rejects historical data, the constraint encoded a wrong belief. The data records what actually happened; the schema is an artifact of someone's understanding of what they thought happened.

**Why.** Constraints exist to prevent invalid future states. They cannot retroactively make the past invalid. When a constraint added in 2026-05 rejects data from 2024, the meaningful question is *"what did 2024 actually look like, and was the constraint added with full domain knowledge?"* — not *"how do we mangle the 2024 data to fit?"* Silently coercing historical data into the new shape destroys information about what the business actually did. That's a category-of-bug worse than the missing constraint.

The pattern: a periodic import surfaces a constraint violation. Before deciding it's a data error, ask: (1) what did the constraint encode? (2) who added it? (3) did they know about the historical reality? If the answer to (3) is no, the constraint is the bug.

**Recipe.**
1. When a constraint fires on a destructive write, **stop**. Don't reach for parse-time validation that drops the offending rows.
2. Audit the constraint's origin commit. What was the rationale? Was it backed by domain confirmation, or a developer's mental model?
3. If the historical reality contradicts the constraint, draft a migration that drops or relaxes it. Document the rationale in the migration file comment.
4. Audit downstream code paths that *depended* on the constraint (server actions, RPCs, dashboard rollups, UI filters). Each may need to keep the rule at its layer even after the DB drops it — for forward-going behavior.
5. File a follow-up ticket for any downstream code that needs to track the schema change separately (unit tests, stale comments, behavior verification).

**Failure mode.** The `cases_invoice_id_channel_chk` constraint (Kairos KAI-140) forbade `stock_bill` cases from linking to invoices. Historical paper-based Stock & Bill orders DO have invoices. First-pass instinct: validate the CSV and reject those rows. That would have silently dropped legitimate historical data. Right move: drop the constraint, keep the forward-going UI/RPC filters, keep commission at $0 for stock_bill regardless of invoice linkage.

## Three-stage write contract — preflight, mutate, verify, rollback

**Principle.** Every destructive write emits four artifacts: a read-only preflight, a transactional mutate, a read-only verify, and a marker-scoped rollback. Each is its own file, runs as its own step, and is human-gated.

**Why.** Destructive writes fail in one of three classes: *preflight* failures (FKs missing, constraints will fire, environment not ready), *mutate* failures (the change itself hits an unexpected constraint, NULL violation, or assertion), and *verification* failures (the change executed but did not produce the expected post-state). Bundling these into one script makes diagnosis impossible — a failure mid-script leaves you unsure which stage failed and whether to advance or roll back. Separating them turns each into a yes/no gate.

The rollback isn't an afterthought; it's the recovery deliverable. **An untested rollback is a wish, not a recovery path.** Always run rollback at least once in local cycle before trusting it for prod.

**Recipe.**
- **Preflight (read-only, separate file):** verify all FKs exist, target tables are reachable, the executing role has the privileges it needs, no constraints will be tripped by the planned data. Emits PASS/FAIL with structural counts, not row values.
- **Mutate (transactional, separate file):** the actual change wrapped in `BEGIN ... COMMIT`. Every assertion fires as `RAISE EXCEPTION` so the transaction aborts cleanly on any throw. No half-applied state. Final `RAISE NOTICE` reports counts (rows new / rows amended / totals) — structural only, never row values.
- **Verify (read-only, separate file):** post-state diff. New-vs-amended-vs-orphaned counts. Per-field amendment breakdowns. Sanity reads against pre-state expectations.
- **Rollback (marker-scoped, separate file):** `DELETE FROM <table> WHERE <marker> = '<this-run>'`. Scoped narrowly enough to remove only this run's rows, never pre-existing data. **The rollback's wrong-scope failure mode is catastrophic** — wrong scope means either you leak rows (rollback too narrow) or you damage pre-existing data (rollback too wide).

**Failure mode.** Single-file "migration" that mixes preflight checks with mutations with verify queries. Hits an error halfway — was the preflight wrong, or did the mutation fail? Was anything written? Unclear. Operator either retries (potential double-write) or rolls back (potentially against nothing). The four-file split turns each into an independent gate.

## Idempotency via natural keys, proven on re-run

**Principle.** A destructive write that may be re-run (periodic imports, retry-on-failure, ETL reconciliation) must be idempotent on a natural key. Re-running against unchanged input produces zero new rows. Re-running with one row changed updates exactly one row, never duplicates.

**Why.** Periodic imports inherently get re-run. The natural key is what the script uses to decide "is this row already here?" If the key is wrong (too narrow, too wide, NULL-unsafe), idempotency breaks — re-runs duplicate cases or fail to amend. **The natural key is a load-bearing claim that must be proven on-write, not asserted in a comment.**

The proof is structural: re-run the same script against the same input and assert `rows_new = 0`. This is a one-line assertion at the end of the mutate; it surfaces idempotency violations as RAISE EXCEPTION rather than letting them accumulate silently.

**Recipe.**
- Choose the natural key carefully — it must uniquely identify a row across the entire dataset *and* be stable across runs (the spreadsheet operator must not be expected to re-key on every run).
- Use NULL-safe equality (`IS NOT DISTINCT FROM`, not `=`) — a `NULL = NULL` is `FALSE` in standard SQL, which silently breaks idempotency when key columns can be blank.
- Test idempotency on local before trusting it on prod: run the script twice, assert `0 new` on the second run. Then change one row and verify exactly one row is amended on the third run.
- Document the tradeoffs the natural key encodes — *"if column X changes between runs, the row will look new"* is acceptable as a tradeoff but must be explicit.

**Failure mode.** Natural key omits `po_number` for a CSV where `patient_identifier` is blank in 80% of rows. Re-runs duplicate every blank-patient case because the key collapses to too-coarse `(facility, date, surgeon)` and matches multiple distinct cases. The duplicates are silent — only surfaced by hand-counting after the fact.

## Bidirectional update semantics for tri-state columns

**Principle.** A spreadsheet-owned column with `yes | no | blank` CSV vocabulary needs a three-branch UPDATE: NULL (blank, no opinion → keep DB), FALSE (explicit no → clear), TRUE (yes → set). A two-branch CASE that conflates *no* with *blank* is one-directional silent data loss.

**Why.** Boolean-derived columns are the natural place to encode operational state that can flip — a charge sheet sent in error and walked back, an invoice marked paid then refunded. The CSV vocabulary distinguishes "I don't know" (blank) from "definitely not" (no). The UPDATE must honor that distinction.

A two-branch CASE that treats both NULL and FALSE the same direction (typically: "keep DB if not TRUE") can only ever set, never clear. The amendment runbook reports `N amended` correctly but the field doesn't actually change. The operator believes the spreadsheet edit landed; it didn't.

**Recipe.**
```sql
column_name = CASE
  WHEN s.csv_field IS NULL  THEN c.column_name              -- blank → keep
  WHEN s.csv_field IS FALSE THEN NULL                       -- explicit no → clear
  WHEN s.csv_field IS TRUE  THEN COALESCE(c.column_name, derived_value)  -- yes → set if not already
END,
```

The TRUE branch typically preserves an app-edited timestamp (the operator may have set a precise value); the FALSE branch unconditionally clears. **Both branches matter.** Don't ship one-way logic just because the test case happened to be set-not-clear.

**Failure mode.** `charge_sheet_sent_at` (Kairos KAI-138) UPDATE was a two-branch CASE that conflated NULL and FALSE. Toggle yes→no in CSV → re-run seed → amendment reports `0 new / 384 amended` → but the toggled row's `charge_sheet_sent_at` stayed set. The bug was only caught by an explicit count-based amendment test (A7 in the runbook); silent in any test that only checked "no→yes" direction.

## Validate at parse, not at constraint

**Principle.** Generators and ETL scripts validate row-level rules at parse time with row indices in the error message. They do not produce SQL that the DB constraint catches at mutate-time. The diagnostic gap between "row 142 has invoice_paid=yes but no invoice_number" (parse-time) and "ERROR: NOT NULL constraint violated on column X" (constraint-time) is enormous.

**Why.** Constraint errors don't tell you which CSV row caused them — they tell you which DB row violated. The operator has to reverse-engineer which spreadsheet row maps to the failing case, which is hard when the natural key is composite and PHI-shielded. Parse-time validation emits `Row 142: invoice_paid=yes requires invoice_number to be set` — the operator opens row 142 in the spreadsheet and fixes it.

This also means parse-time errors are PHI-safe by construction — emit *row indices*, not field values. Constraint errors typically include the offending row's values in `DETAIL:`, which can leak PHI.

**Recipe.**
- Every cross-field invariant the DB constraint enforces also belongs in the parser as a validation rule.
- Errors include the row index (1-indexed for human-friendly diagnostics) and the rule name. Never the value.
- Refuse to emit any SQL until validation passes for all rows — no partial outputs.
- Layer with the DB constraint (defense in depth): even if validation is ever bypassed, the DB still rejects. Each layer enforces the invariant independently.

**Failure mode.** Parser accepts a CSV row with `channel=stock_bill, invoice_number=X` because nothing forbids it at the row level. Generator emits SQL. Mutate-time CHECK constraint fires on `cases_invoice_id_channel_chk`. Operator sees `ERROR: violates check constraint "cases_invoice_id_channel_chk"` — no row index. They have to grep the CSV by hand to find the offender. Time-to-diagnose: 10×.

## Layered backup independence — the pre-write snapshot is non-negotiable

**Principle.** Every destructive prod write is backed by an *independent* restore path that does not rely on the script's own rollback. The minimum is a portable `pg_dump` of the affected tables, taken seconds before the write, stored to a location the migration cannot touch.

**Why.** The script's rollback SQL is itself untested-against-prod the first time it runs there. It assumes the marker scoping is correct, the DELETE order respects FK cascades, and no downstream side effects (triggers, views, downstream-app caches) need separate cleanup. The pre-write snapshot is the recovery path that survives the rollback being wrong.

This connects to the KAI-126 backup doctrine — layered defenses for different failure modes:
- **Layer A** — provider PITR (Supabase / RDS): fast recovery from logical corruption.
- **Layer B** — daily independent dumps to portable object storage: survives provider catastrophe.
- **Layer C** — *per-write* snapshot of affected tables: the rollback-of-last-resort for this specific operation.
- **Layer D** — restore drill (monthly): "an untested backup is a wish, not a backup."
- **Layer E** — access discipline: read-only role for dumps, append-only bucket-write role, separate KMS keys.

A senior design layers these so each failure mode (logical corruption / provider outage / bad migration / forensics) has a matching recovery path with a defined RPO/RTO. See `factory-security.md §Layered backups` and the KAI-126 doctrine comment for the full table.

**Recipe.**
```bash
# Before any destructive prod write — Layer C:
pg_dump --format=custom --compress=9 --no-owner --no-privileges \
  -t public.<table1> -t public.<table2> ... \
  --file=pre-<TICKET-ID>-$(date -u +%Y-%m-%dT%H-%M-%S).pgdump \
  "$PROD_DB_URL_READONLY"

# Manifest sidecar (timestamp + schema HEAD + per-table row counts + SHA-256):
scripts/snapshot-manifest.sh pre-<TICKET-ID>-<ts>.pgdump > pre-<TICKET-ID>-<ts>.manifest.json

# Then run preflight → mutate → verify. If anything goes wrong:
pg_restore --clean --if-exists --no-owner --no-privileges \
  --dbms="$PROD_DB_URL_ADMIN" pre-<TICKET-ID>-<ts>.pgdump
```

**Failure mode.** "We have the rollback SQL, we don't need a backup." The rollback SQL has never run against prod, the operator hits a constraint-cascade they didn't anticipate, and the rollback leaves orphan rows behind. PITR isn't on (cost decision deferred). No Layer C snapshot taken. The corrupt state lives in prod for hours while a forensic recovery is improvised.

## Human gate at every step — LLM hands the command, operator executes

**Principle.** During a multi-step destructive runbook, the LLM **hands the command**; the operator **executes**. This holds even for "safe" structural-only queries (row counts, schema reads). The LLM never auto-runs runbook commands, even via MCP.

**Why.** Two distinct principles, both load-bearing:
- *PHI safety.* Anything that surfaces PHI-bearing columns must not route through the LLM. (See `factory-security.md §PHI never enters the LLM`.)
- *Human gate.* The operator is the one taking the action against prod. Each step is a deliberate approval boundary. If the LLM runs the step, there is no moment of "yes, execute now." The first principle alone would allow MCP for count queries; the second principle does not.

When the operator establishes the contract by asking *"is there an easier interface than terminal?"* — they are asking for a *better-to-use* interface for *their* execution. They are not asking the LLM to take over execution.

**Recipe.**
- The LLM's role during a runbook:
  - Hand the exact command (env vars inlined; assume nothing about shell state).
  - Interpret the structural output the operator pastes back.
  - Generate the next command.
  - Update tasks, write Linear comments, propose code fixes.
- The LLM's forbidden actions during a runbook:
  - Running `psql`, `pg_dump`, `supabase`, or any MCP call against the project DB.
  - Auto-running "safe" count queries to "drive faster."
  - Touching the prod DB in any way that bypasses the operator.
- The operator's responsibility:
  - Run each step in their terminal or Studio.
  - Paste back the *structural summary* only — never the row values. (Counts. Pass/fail. RAISE NOTICE summary lines. Error class names without DETAIL lines.)
  - Refuse to advance to the next step if the current step's output is unexpected.

**Failure mode.** LLM "drives the runbook" via Supabase MCP for non-PHI queries, then leaks PHI when an unexpected error returns row values in the error DETAIL. Worse: the LLM runs a mutate step thinking it was safe and the destructive write completes before the operator knew it was happening. Both happen quietly.

## Defense in depth — each layer enforces the invariant independently

**Principle.** A business rule that must hold (e.g., "stock_bill cases never accrue commission") is enforced at every layer that touches it: schema CHECK / partial index, server action guard, RPC filter, UI eligibility filter. Any single layer alone is one bug from violating the rule.

**Why.** When you drop a DB constraint to accommodate historical data, the corresponding rule does not disappear — it migrates to the layer where it still holds. The constraint may have been wrong about historical state but right about forward-going behavior. Dropping the constraint and leaving the other layers in place is correct; dropping and removing all enforcement is silent regression.

A senior design enumerates the layers explicitly. Before a destructive write that touches an invariant: *which layers enforce this today? Which layers will need to change?* Map all of them before opening the migration PR.

**Recipe.**
- Map the invariant before the change:
  - DB constraint (CHECK, UNIQUE, FK, partial index)
  - RPC body (server-side branching)
  - Server action / API handler
  - UI eligibility filter
  - Aggregation / dashboard rollup
- For each layer, decide: stays, changes, removed.
- Document the decision in the migration PR description under "What does NOT change" — the layers that retain the rule.
- Test the forward-going behavior end-to-end after the migration: UI behavior unchanged, dashboard math unchanged, server actions still guard.

**Failure mode.** Constraint dropped to accept historical data; server-side guards left in place ("they handle the forward-going case"); but the *commission rollup* was relying on the constraint to filter and now silently includes stock_bill cases in the commission total. Off-by-thousands in the next dashboard render.

## Migration testing protocol — local mirror → ephemeral staging → prod

**Principle.** A destructive change runs against a local Postgres that mirrors prod schema **before** it runs against prod. An ephemeral staging environment (PR branch DB, scratch project) is the bridge between local and prod for migrations that involve more than a constraint drop.

**Why.** Local cycle proves the script's *logic* — does the SQL parse, does the natural key work, does idempotency hold, does the rollback restore the pre-state. Staging proves the script's *environment compatibility* — does the prod role have the privileges, does the prod schema match local (Drift! triggers! views! permissions!), does the migration runner ordering work.

Skipping local-to-staging is how you discover that prod has an extra trigger that fires on the new write path, mid-mutate. Skipping staging-to-prod is how you discover that the destination role doesn't have the grants you assumed.

**Recipe.**
1. Local cycle (this skill's §Three-stage write contract): preflight → mutate → idempotent re-mutate → amend → verify → rollback. All gates green.
2. Staging cycle: same script, ephemeral staging DB or PR-branch Neon DB. Same gates. Surfaces drift in schema or privileges.
3. Pre-prod snapshot (Layer C): `pg_dump` of affected tables, manifested.
4. Prod cycle: same script, prod DB, operator at the terminal. One step at a time, structural summaries pasted back.
5. Post-prod verify: explicit cross-check that prod row counts match expectations. Rollback ready but not run.

**Failure mode.** Local-only verification ships to prod. Prod has a `BEFORE INSERT` trigger that local does not (added by an emergency hotfix never backported). The mutate's INSERT loop runs through the trigger, which throws on row 47 of 384 — the BEGIN/COMMIT aborts cleanly, but the operator now thinks the generator has a bug. Several hours of misdirection before the prod-vs-local schema drift is found.

## Migration commit + PR shape

**Principle.** Migration commits follow `factory-commits.md` (Conventional Commits + required Linear ID). The PR body covers: summary, tickets, **gating criteria for the prod run** (separate session), test plan executed end-to-end on local, and a "what does NOT change" section listing the invariant layers that retain the rule.

**Why.** A reviewer looking at a migration PR needs to know: (a) what changed in the schema, (b) what code depends on that schema change, (c) what's deliberately *not* changed (forward-going behavior preserved at higher layers), (d) what gates need to clear before the prod run that uses this migration. Putting all four in the PR body makes the PR reviewable in one pass and durable as a historical record.

**Recipe.** See the PR template in `factory-commits.md` and KAI-138 PR #61 for a reference shape. Key sections:
- **Summary** — bullet list of what shipped.
- **Tickets** — `Closes KAI-X`; `Partially addresses KAI-Y` if residual scope remains.
- **Gating for the prod run (NOT in this PR)** — name the dependencies (snapshot helper, restore drill, anything else from Layer A-E).
- **Test plan** — checklist with concrete numbers from the local cycle: rows new, rows amended, totals, idempotency assertion, rollback verification.
- **What does NOT change** — explicit list of UI / server / dashboard layers that retain the rule. Reviewers don't have to grep to find out.

**Failure mode.** PR body is empty or one-line. Reviewer has to read the diff cold to understand which layers stay vs change. The "did the author audit the downstream code?" question is unanswered. PR sits in review limbo or gets a rubber-stamp approve.

## When this skill is too heavy

If the change is a single-column add with no data backfill and no downstream code depending on the new column, `factory-data-layer.md`'s migration guidance is sufficient — you don't need this skill. The framework here is for **destructive writes** (DELETE, UPDATE-with-data-loss-risk, DROP CONSTRAINT, schema changes with backfill, periodic data imports). Use judgment.

## Related skills

- `factory-data-layer.md` — schema design, ORM choice, migration file naming.
- `factory-deployment.md` — where migrations execute in CI, ephemeral PR DBs, single-tenant deployment.
- `factory-security.md` — KMS-at-rest, PHI handling, the layered backup doctrine (Layer A-E referenced above).
- `factory-commits.md` — commit message shape, Linear ID requirement.
- `factory-pitfalls.md` — cross-skill index of failure modes referenced above.
