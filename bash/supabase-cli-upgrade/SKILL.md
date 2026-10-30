---
name: supabase-cli-upgrade
description: Guide for upgrading the Supabase CLI version pinned in .mise.toml. Covers finding the latest version, verifying caveats, testing experimental-flag-dependent commands, and updating the inline guidance. Use when the user asks to upgrade or bump the Supabase CLI.
---

# Supabase CLI upgrade

The Supabase CLI is pinned in `.mise.toml` as `aqua:supabase/cli`. The
pin is deliberate: the CLI version determines Docker image versions,
config.toml shape, `supabase status -o json` key names, and the
behavior of subcommands the repo's scripts depend on. A floating
`latest` could break any of those under a routine `mise install`.

## Step 1: Find the latest version

mise has no built-in version lister for aqua-backed tools. Check the
upstream GitHub releases API:

```
https://api.github.com/repos/supabase/cli/releases/latest
```

The response JSON includes `tag_name` (e.g. `v2.115.0`). Strip the
leading `v` for the mise pin.

## Step 2: Read the current caveats in .mise.toml

Before bumping, read the comment block above the
`aqua:supabase/cli` pin. It documents every known incompatibility
and verification requirement. As of this writing there are three
caveats:

1. **dev-start verification.** `mise run dev-start` drives a local
   stack whose reproducibility is tied to the CLI version. After
   bumping, confirm dev-start still reaches Vite (stack starts, status
   keys read, schema applies).

2. **Realtime JWT bug (#4219).** The CLI's bundled realtime image
   rejects the modern `sb_publishable_` key as `MalformedJWT` because
   it tries to verify it as a JWT. `scripts/dev-local.mjs` works
   around this by writing the legacy anon JWT as the local client key.
   If a future CLI bundles a realtime image that accepts opaque keys,
   flip `dev-local.mjs`'s `readStatus` to prefer `PUBLISHABLE_KEY` and
   re-test realtime locally. Issue #4219 was stale-closed as
   "not_planned" without a fix; check whether it has been reopened or
   a new fix landed before assuming the workaround is still needed.

3. **Storage subcommands require --experimental.** `supabase storage
   ls` and `supabase storage cp` require `--experimental` as of
   2.115.0. `scripts/backup.mjs` and `scripts/restore.mjs` pass
   `--experimental` on every storage call. If a future CLI stabilizes
   these subcommands (drops the flag) or changes their output format
   (e.g. `storage ls` stops printing one-bucket-per-line with trailing
   slashes), the scripts break.

If you discover a NEW caveat during the upgrade, add it to the comment
block in `.mise.toml` so the next session sees it. The comment block
is the canonical record of upgrade concerns - do not let it go stale.

## Step 3: Bump the pin

Edit `.mise.toml`: update the version string and the comment that says
"X.Y.Z is the latest; verify dev-start on it before trusting the pin."

Install the new version:

```sh
mise install aqua:supabase/cli@<new-version>
```

Verify the mise-managed version (the bare command may still point at
the old install due to PATH - this is a known shim issue, not a failed
install):

```sh
mise exec -- supabase --version
```

## Step 4: Verify each caveat

Run every command the repo's scripts depend on. Do not skip any.

### 4a: Local stack (dev-start caveat)

```sh
mise run dev-start
```

Confirm: stack starts, Vite reaches the browser, realtime connects
(thread list updates live). If realtime silently stops, check whether
the new CLI bundles a different realtime image - see caveat 2 above.

### 4b: Storage subcommands (experimental flag caveat)

```sh
mise exec -- supabase storage ls ss:/// --local --experimental
```

Confirm: output is one bucket name per line with trailing slashes:
```
attachments/
recipe-images/
...
```

If the output format changed, update `listBuckets()` in
`scripts/backup.mjs` to parse the new format.

```sh
mise exec -- supabase storage cp -r ss:///attachments /tmp/test-bucket --local --experimental
```

Confirm: files download. Then clean up the test directory.

If `--experimental` is no longer needed (the subcommand stabilized),
remove `--experimental` from all calls in `scripts/backup.mjs` and
`scripts/restore.mjs`, and update the caveat in `.mise.toml`.

### 4c: DB dump (backup/restore dependency)

```sh
mise exec -- supabase db dump --local --dry-run
mise exec -- supabase db dump --local --data-only --dry-run
```

Confirm: both produce pg_dump scripts without errors. Check the
`--exclude-schema` list has not changed in a way that would exclude
schemas nak needs (public, auth, storage, cron).

### 4d: DB query (restore/sync dependency)

```sh
mise exec -- supabase db query --local -c 'select 1'
```

Confirm: returns a result. The `-f` flag (file input) is used by
`scripts/restore.mjs` and `scripts/sync.mjs` - test that too:

```sh
mise exec -- supabase db query --local -f supabase/schema.sql
```

### 4e: Functions serve/deploy

```sh
mise run functions-serve   # quick smoke
mise run functions-deploy  # only against linked, not local
```

### 4f: Backup and restore end-to-end

```sh
mise run backup
# verify the archive appears in backups/
mise run restore
# verify the data came back (check threads in the app)
```

## Step 5: Update the comment block

After verification, update the `.mise.toml` comment block:

- Update "X.Y.Z is the latest" to the new version.
- Update any caveats that changed (e.g. if #4219 was fixed, note it
  and remove or update the realtime caveat).
- Add any new caveats discovered during verification.
- If `--experimental` was dropped from storage subcommands, update
  the storage caveat and the scripts.

## Step 6: Run the gate

```sh
mise run check
```

The gate does not exercise the Supabase CLI directly, but it confirms
the `.mise.toml` edit did not break anything else (knip, lint, build).

## What NOT to do

- Do not change the pin to `latest` or a floating range. Every version
  spec in `.mise.toml` is an exact pin because a floating spec needs a
  GitHub releases-list API call the sandbox proxy blocks.
- Do not skip the verification steps. "It installed fine" does not mean
  "the local stack works" or "storage cp still downloads files."
- Do not remove a caveat without verifying it is actually fixed. A
  stale-closed GitHub issue is not a fix.
