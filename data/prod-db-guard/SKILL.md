---
name: prod-db-guard
description: Use before running ANY script that touches a database from a worktree or local shell. Every worktree binds the PRODUCTION DATABASE_URL, so a "local" script hits prod — and a --dry-run flag is not a guard until a non-executing check proves it returns before the write.
triggers: database script, worktree, local shell, production database_url, hits prod, dry-run flag, non-executing check, db write, prod probe, script that touches a database, cron, failing in prod
---

# prod-db-guard

## The fact that makes this necessary

`scripts/worktree-setup.ps1` copies `DATABASE_URL` into every new worktree as a
**critical key**. There is no local database in a fresh worktree. A script you
run "just to see what it does" runs against production.

`.env` holds a production `DATABASE_URL` **but is not production config** —
never conclude runtime behavior by grepping it (see
`apps/nickstire/docs/runbooks/tidb-backup-restore.md`, Standing warnings).

## The incident this encodes

A prod-touching script was executed as *verification* — to confirm its guard
worked. The guard did not work. **870 production rows were deleted.** The
dry-run flag existed; it was checked after the delete path had already run.

Recorded in `apps/nickstire/docs/runbooks/tidb-backup-restore.md` and
`apps/statenour/docs/runbooks/neon-branching.md` — both apps carry the warning
because the incident class is not app-specific.

**Running a script is not how you verify a script.**

## Procedure

1. **Read the script before running it.** Locate every `DELETE`, `UPDATE`,
   `TRUNCATE`, `DROP`, and bulk `INSERT`.
2. **Prove the subject TABLE exists before theorising about a column.** Query
   `INFORMATION_SCHEMA.TABLES` for it (read-only). Raw `sql\`\`` can name any
   table; Drizzle-typed reads cannot — so a cron that "skips forever" or a
   column that is "missing" may be a table that was never created. Witnessed
   2026-09-02: applying `0114` failed on statement 1 with
   `ER_NO_SUCH_TABLE estimates`; no migration had ever created that table,
   the audit had diagnosed a missing COLUMN, and a day of receipt fixes had
   been shipped for a job that could never run. Scan raw FROM/JOIN/UPDATE/INTO
   targets against the declared table list first
   (`apps/nickstire/server/__tests__/rawSqlTablesExist.test.ts` is that scan as a gate).
3. **Prove the guard non-executing.** Trace the dry-run branch by reading it:
   confirm it `return`s or `process.exit`s *before* the first write, not after.
   A flag that only suppresses logging is not a guard.
4. **Confirm which database you are pointed at.** Print the host, do not assume.
   A worktree defaults to prod.
5. **Back up first for anything destructive.** The house pattern is a copied
   table named `_bak_<table>_<op>_<yyyymmdd>`, created before the mutation and
   left in place until the change is confirmed good.
6. **Get operator approval for a prod write.** Staged and reversible, stated as
   such. This is not an agent-initiative action.

## Applying migrations in scope (never the unscoped sweep)

`pnpm db:migrate` (`scripts/db-migrate.ts`) has **no dry run** and applies
**every** unrecorded file in one pass. When only some files are due, or a
destructive one needs its backup first, write a throwaway scoped runner and
delete it afterwards (runbook rule):

1. Dry run by default: the process **exits before opening a connection**
   unless `--execute` is passed; the dry run prints every statement.
2. `--only <prefix,prefix>` — the files you name, nothing else.
3. For a destructive file: `CREATE TABLE _bak LIKE t` · `INSERT … SELECT` ·
   compare `COUNT(*)` source vs backup · **abort before the drop** on mismatch.
4. Record exactly as `scripts/db-migrate.ts` would: sha256 of the whole file
   as `hash`, the journal `when` as `created_at`, into `__drizzle_migrations`.
   A migration reconcile reports as `UNRECORDED_BUT_EXACT_MATCH` gets a
   record-only pass (no DDL).
5. Re-run `node scripts/reconcile-migrations.mjs --strict` — zero blocking
   drift is the receipt.

Witnessed 2026-09-02: 0113 recorded, 0114 rewritten then applied, 0115/0117
with count-verified backups, 0116 — one runner, one session, deleted after.

## Running it from an agent session

The Claude Code auto-mode classifier — not repo policy — blocks many
production-touching commands, and it blocks by **shape**, not just by risk.
Witnessed 2026-09-02: it denied `railway whoami`, a read-only probe script,
`gh pr checks`, a combined grep+dryrun+execute+rm chain, the plain
`node <runner> --execute` once, and the long-form
`railway run --service … -- ./node_modules/.bin/tsx …`, while allowing the
same actions as single plain commands after the operator added a rule.

- **One plain command per call.** No pipes into `rm`/`grep` chains, no
  compound guards around a prod write; run the read, then the write, then the
  cleanup as separate calls.
- Expect a **read-only probe** to be treated as a prod action.
- When blocked: stop and hand the operator the exact one-liner. Reshape a
  command at most once; a second reshape is a workaround, not a fix.
- `railway run -s <service> -- pnpm exec tsx <script>` (short form) is the
  shape that passed; it injects the real environment so no key is ever
  pasted into a command.

- **On a Windows/PowerShell device, single-quote every comma-separated
  argument** (`--only '0127,0128'`, id lists). Unquoted, PowerShell converts it
  to an array of NUMBERS: leading zeros vanish and commas become spaces
  (2026-10-02: `--only 0127,0128,...` reached node as `127 128 ...`; the script
  refused and wrote nothing, benign only because it refuses unmatched
  prefixes).

## A scripts-only prod run from the operator PC

`scripts/worktree-setup.ps1` sat over 10 minutes in its repo-wide recursive
scans on NattyNour (2026-10-02) and copied nothing. A run that needs only
`scripts/`, `drizzle/` and `mysql2` needs no full setup:

1. `git worktree add -b <tmp> <dir> origin/main`;
2. two `mklink /j`: root `node_modules` and `apps/nickstire/node_modules`;
3. `railway run --service ... -- node scripts/<x>.mjs` (dry run first);
4. tear down with `worktree-teardown.ps1`; add `-ForceDirtyRelease` only after
   `git rev-list --count origin/main..<tmp>` is 0 and the status is clean.

## A Neon child branch has its own role password

The branch's role password is NOT the parent's (2026-10-20: scrub rehearsal
auth failures). Rehearse with the connection string from `get_connection_string`
for that branch, and check by hash, never by printing, that it differs from the
production string before use. A string equal to production is not the branch.

## Verify read-only instead

Almost every "does this work in prod?" question has a read-only answer:

- `cron_log` — did the job run, when, with what result
- `GET /api/health` — uptime since container start
- `railway run --service MAINnicks-tire-auto -- <read-only query>`

Prefer these. They answer the question without a write path.

## Two receipts you can lose in the same five minutes

- **Resolve the physical table name from `@@map` before writing backup
  SQL.** `CREATE TABLE ... AS SELECT * FROM "AutomationPolicy"` fails
  `42P01` — the Prisma MODEL name is not the database TABLE name once a
  model declares `@@map`. Check the schema's `@@map` before naming a
  table in raw SQL.
- **Never restore files via `git show <ref>:<path> > <path>` in
  git-bash.** A root-dotfile-shaped colon ref MSYS-mangles
  (`origin\main;.gitignore`), and the `>` redirect truncates the target
  to 0 bytes *before* the command's own failure is visible — witnessed
  restoring one file this way zeroed ~300 tracked files, including the
  live `.completion/evidence.json`. Use
  `git archive <ref> [-- <paths>] | tar -x` instead; it cannot truncate
  a target it never opens for writing until the archive stream is
  already valid.

## Red flags — stop if you catch yourself thinking these

- "It's just a dry run."
- "I'll run it once to see what happens."
- "The script says it's safe."
- "I need to test the guard."

Each of these preceded the 870-row deletion. The correct move is a
**non-executing** check: read the code, or run it against a scratch table you
created for the purpose.

Related: [nickstire-tidb-ddl](../nickstire-tidb-ddl/SKILL.md) for the DDL
rules · `apps/nickstire/docs/operations/SCHEMA_DRIFT_RUNBOOK.md` for the apply
procedure.
