---
name: prior-art-grep
description: Use BEFORE adding any new table, queue, tool, feature flag, cron, env var, or registry entry. Run a fixed grep set and write the answer down before building. This repo has standing "no second implementation" rules that are easy to violate by accident.
triggers: new table, queue, tool, feature flag, cron, env var, registry entry, grep set, prior art, second implementation, duplicate store, schema models
---

# Prior-Art Grep

Cheap, mechanical, and it has already fired twice in one session.

## The base rate

Two near-misses in a single wave (2026-08-28):

- A tool was nearly rebuilt under a new name while the original existed.
- A `next_action` table was nearly added when **`PostTurnOutbox` already
  provided it** — a durable queue with claim/retry/dead-letter and
  `nextAttemptAt` as a scheduling primitive. Caught by research, not by
  the author.

The second would have violated the standing rule that there is **no third
queue beside `PostTurnOutbox` and `WorkItem`**.

## Run this before building, and paste the result

```bash
# schema models — the two apps use DIFFERENT stacks and different keywords
git grep -nE "^model " -- apps/statenour/prisma/schema.prisma     # statenour = Prisma/Postgres
git grep -n  "mysqlTable(" -- apps/nickstire/drizzle/schema.ts    # nickstire = Drizzle/TiDB (MySQL)

# tool names + catalog
git grep -rn "<candidate-name>" -- apps/statenour/lib/ai
# cron manifest
git grep -rn "<candidate-name>" -- apps/statenour/config apps/nickstire/server
# feature flags / env — search the whole repo, NOT just templates
git grep -n "<CANDIDATE_ENV>"
```

⚠ **`pgTable(` returns nothing for nickstire** — all 146 declarations in
`apps/nickstire/drizzle/schema.ts` are `mysqlTable`, because nickstire is
TiDB. A Postgres-shaped search there is a guaranteed false "no prior art".

⚠ **Do not scope the env search to `.env.example` files.** There is no root
template, and `apps/worker` has **none at all** while consuming variables
directly in source (`apps/worker/src/scheduler.ts`, `apps/worker/src/index.ts`).
A template-only search reports "Prior art: none" for variables already running
in production. Search the repo, then check the three real templates
(`apps/statenour/`, `apps/nickstire/`, `camera-bridge/bridge/`) to see whether
the variable is *documented* as well as used.

⚠ **`git grep` exits 1 for an unmatched PATHSPEC exactly as it does for a
genuine no-match.** A typo'd or non-existent path therefore reads as
"nothing found" and gets recorded as "Prior art: none". Confirm the path
exists (`git ls-files <path>`) before believing an empty result.

⚠ **The schema file can outlive the table.** For every table you are about
to read from or build on, list the newest migrations and grep them for
`drop table` / `retire` before trusting `schema.prisma` or `schema.ts` —
Drizzle keeps a table's definition around after the migration that dropped
it (witnessed: the camera plan named `vehicles.licensePlate` as the plate
store from three audit agents quoting the schema, after
`drizzle/0117_retire_dead_vehicles_table.sql` had already retired that
table — caught only because the migrations directory was checked for
naming conventions, not by the grep set above).

Then write ONE line before you build:

> Prior art: none / `<file:line>` — reusing / `<file:line>` — insufficient
> because \<reason\>.

"Insufficient because" must name a concrete missing capability, not a
preference for a fresh start.

## The searches that miss

A grep is only as good as the shape you searched for. Known blind spots
in this repo:

- **Dynamic `import()`** hides a dependency from three plain greps. The
  first dependency-cruiser scan caught `lib/services/ultron-ticker.ts`
  dynamically importing an otherwise-unused route (`void maturityMod`) —
  a shape greps had missed.
- **Case.** Use `grep -i`. A case-sensitive sweep for `"new ownership"`
  missed the capitalized `"New ownership"` and shipped it to production
  (2026-09-03, fixed in #2099).
- **Line-number windows.** When a claim rests on what a structure does
  NOT contain, read the whole structure by its delimiters —
  `sed -n '/const typeMap/,/};/p'`, never `sed -n '140,165p'`. A window
  that clips a map's head manufactures a false "no such mapping".
- **Comments.** Filter them before believing a hit, covering block and JSX
  forms as well: `grep -vE '^[^:]+:[0-9]+: *(//|/\*|\*|\{/\*|#)'`. An
  alternation missing `/*` and `{/*` keeps the very hits it should drop.
  See `assert-the-consumer`.

## Confidence

Medium — two instances, one session. Kept because the cost is one command
and the failure it prevents is a duplicate durable store.

Related: `assert-the-consumer` · `plan-gate` (gate a pasted plan's claims
the same way) · `statenour-verify`.
