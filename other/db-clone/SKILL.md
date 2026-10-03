---
name: db-clone
layer: stack
description: Copy one Cloudflare D1 database into another of the same app's environments — refresh STAGING from prod, seed a PREVIEW from staging, or (guarded) push staging up to prod. Full mirror via scripts/db-clone.mjs. Use when asked to "clone a db", "refresh staging from prod", "copy prod data to staging", "seed a preview db", or to reconstitute a wiped staging DB. NOT for per-collection seeding (use the app's seedData/seed endpoints) or for schema migrations (use db-migrations).
allowed-tools: Bash, Read, Grep, Glob
---

# db-clone — mirror one D1 database into another

Wraps **`scripts/db-clone.mjs`** (`pnpm db:clone`): exports a **source** Cloudflare
D1 database and imports it into a **target**, making the target an **exact mirror**
(every target table dropped, then re-imported). Database names are discovered from
each app's `wrangler.jsonc`, so it works for any app + any pair of its environments.

```bash
node scripts/db-clone.mjs --app <app> --from <env> --to <env> [--dry-run] [--yes]
# or: pnpm db:clone --app <app> --from <env> --to <env>
```

`<env>` is `prod` (the wrangler.jsonc top level) or any key under `env.*`
(`staging`, `preview`, …).

**Mobile / no-laptop:** there's also a `db-clone` GitHub Action
(`.github/workflows/db-clone.yml`) — *Actions → Run workflow → app/from/to* from
the GitHub app. It reuses the repo's `CLOUDFLARE_*` secrets (no Cloudflare site
needed); a prod target requires the `confirm_target_db` input (passed as
`--confirm`), and the pre-clone backup is uploaded as an artifact. For
non-interactive runs the script takes `--confirm <db>` in place of the typed
prompt.

## When to use this — and when NOT to

| Situation | Use |
|-----------|-----|
| "Is the data still there?" / "how many rows / bookings / users" — *check before cloning* | **`pnpm db:counts --app <app> --env <env>`** (read-only) or the `db-counts` Action |
| "Make staging look exactly like prod" / "refresh staging" / "seed a preview from staging" | **this skill** |
| "Reconstitute the wiped staging DB" (and prod still has the data) | **this skill** (`--from prod --to staging`) |
| Load a *specific* org / CSV import into a fresh DB | the app's `seedData/` + seed endpoints — NOT this |
| The source/target data is gone everywhere | re-seed from `seedData/`, don't clone |
| Add/alter a table (schema change) | the **db-migrations** skill |

A clone copies **all** data as-is; it is not a substitute for seeding curated
fixtures or for migrations.

## Hard rules (the judgment this skill encodes)

1. **Always `--dry-run` first.** Read back the resolved names (e.g.
   `velo-db → velo-staging-db`) and the ordered plan before doing anything real.
   The dry run needs no Cloudflare credentials.
2. **Cloning OVERWRITES the target.** Confirm the direction out loud
   (`--from` = the keeper, `--to` = the one wiped). Source == target is refused.
3. **Prod-as-target is the dangerous path** — treat it like the "never deploy to
   prod casually" rule. The script forces a **typed confirmation** (retype the
   target db name) and takes a **timestamped backup** to `.db-backups/` first.
   Don't pass `--yes` to a prod target unless the human explicitly asked for an
   unattended run. The default direction is **prod → staging**, never the reverse.
4. **A real run needs creds in the env:** `CLOUDFLARE_ACCOUNT_ID` +
   `CLOUDFLARE_API_TOKEN` (account → D1 Edit). Without them, only `--dry-run`
   works. `wrangler whoami` should resolve before a real run.
5. **Verify after.** Once imported, confirm with a row count, e.g.
   `npx wrangler d1 execute <target> --remote --command "SELECT (SELECT COUNT(*) FROM user) users, (SELECT COUNT(*) FROM organization) orgs"`.

## Flow

1. `--dry-run` to confirm names + direction.
2. (prod target only) typed confirmation + automatic backup to `.db-backups/`.
3. Export source → drop all target tables → import dump.
4. Row-count check on the target.

See `writeups/guides/db-clone-guide.md` for the full reference.
