---
name: sqlfluff
description: Dialect-aware SQL linting and formatting for projects with standalone .sql files
when-to-use: When writing, reviewing, or changing SQL in .sql files, migrations, or dbt models — not for SQL embedded as string literals in application code
user-invocable: true
paths: ["**/*.sql"]
allowed-tools: [Read, Glob, Grep, Bash]
effort: low
---

# sqlfluff — SQL linting

On-demand. Loads when you touch `.sql`, not every session (ADR-0012, principle #15).

## Run it

```bash
uvx sqlfluff lint --config .sqlfluff path/to/file.sql     # no install needed
uvx sqlfluff lint --dialect postgres file.sql             # if the project has no .sqlfluff
```

`uvx` is deliberate: no dependency to install, pin, or unwind. If the project has a
`.sqlfluff`, use it — it encodes decisions someone already made.

## Read the output like this, or you will waste a session

**sqlfluff's default output is mostly noise, and the noise is load-bearing to understand.**
Measured on settempo (2026-07-21, the corpus that produced ADR-0012): 206 violations, of
which **185 (89%) were whitespace and indentation.** The shipped `.sqlfluff` sets
`exclude_rules = layout` for exactly this reason. If you find yourself reading `LT01`/`LT02`
complaints, you are running without the project config.

Of the 21 that survived the layout filter, **14 were wrong**:

| Rule | What it said | Why it was wrong |
|---|---|---|
| `RF05` special chars in identifier | flagged `create policy "Users own their shows"` | Quoted, space-containing policy names are **idiomatic Supabase RLS**. Not a defect. |
| `PG01` index locking | demanded `CONCURRENTLY` on every `CREATE INDEX` | It was a **fresh-install script** — tables created empty in the same file. `CONCURRENTLY` cannot run inside a transaction, and there is nothing to lock. The advice was actively harmful. |

**So: do not treat a sqlfluff finding as a defect until you have read the surrounding SQL.**
The rule does not know whether it is looking at a migration against a live table or a
schema bootstrap, and that distinction inverts `PG01` completely.

## Where it genuinely earns its keep

- **Parse validity** — it will not lint what it cannot parse, so a clean run is real evidence the SQL is syntactically valid for that dialect.
- **Dialect portability** — catches syntax valid in one engine and not another.
- **Query-shaped SQL under frequent edit** — dbt models, analytics. This is its strong case.

## Where it does not

- **SQL embedded in application code** as Python/TS string literals. sqlfluff sees `.sql` files and templated SQL. Tessera's own SQL is all inline literals, which is why the framework repo gets nothing from this tool.
- **Write-once DDL.** A schema file nobody edits accrues no benefit from a linter.

## The commit gate

`scripts/sql/lint.sh` runs from `.githooks/pre-commit`. It is **warn-only** and silent unless
the commit stages `.sql`. It never blocks. It *does* shout if sqlfluff could not run at all —
a linter that silently skips looks exactly like one that passed.

To make it blocking for a project that has earned it: tune `.sqlfluff` until the findings are
real, then change the script's final `exit 0` to `exit 1`. Do not do this while false
positives remain — a gate that cries wolf gets bypassed, and then it protects nothing.

## Dialect

Set `dialect` in `.sqlfluff` per project. There is no sane default — guessing wrong makes
every rule lie. Supabase/Postgres projects want `postgres`.
