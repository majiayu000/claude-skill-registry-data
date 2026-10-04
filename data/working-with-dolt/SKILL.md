---
name: working-with-dolt
description: Use when working with Dolt — the version-controlled SQL database that branches, diffs, merges, and clones like Git while speaking the MySQL wire protocol ("Git for data"). Covers the full `dolt` CLI (init, sql, sql-server, branch, merge, diff, commit, remote, backup, gc, fsck, ci, profile, creds, conflicts, cherry-pick, rebase, stash), the dolt system tables/procedures (dolt_diff, dolt_history, dolt_commit, dolt_branch), DoltHub/DoltLab/Hosted Dolt/DoltgreSQL, and how Dolt is the storage engine under Joe's shared beads server (one `dolt sql-server` on port 3308). Provides an offline CLI reference generated verbatim from the pinned `dolt` binary plus the official dolthub.com docs. Invoke for any `dolt <command>`/flag lookup, Dolt concept, SQL-versioning question, or for maintaining/troubleshooting the Dolt server beneath beads. For the `bd`-level beads workflow, use `beads-operations`.
metadata:
  last_updated: "2026-06-22"
---

# Working with Dolt (`dolt`)

Offline reference for [Dolt](https://www.dolthub.com/docs) — "Git for data": a SQL database you can `branch`, `diff`, `merge`, and `clone` like a Git repo, speaking the MySQL wire protocol so existing drivers/ORMs connect unchanged. **Pinned to a known version** (see [`PINNED_VERSION`](PINNED_VERSION)).

The CLI pages in [`references/cli/`](references/cli/) are generated verbatim from the installed pinned `dolt` binary; the conceptual docs in [`references/docs/`](references/docs/) are fetched from the official dolthub.com docs. Every generated/fetched file carries `source`/`fetched_at`/`sha256` frontmatter.

## How to use this skill

1. **CLI reference:** read [`references/cli/_index.md`](references/cli/_index.md) for the command list, then `references/cli/<command>.md` (or `<command>__<subcommand>.md` for groups like `schema`, `table`, `remote`, `conflicts`, `creds`, `docs`, `ci`) for exact synopsis/flags — these are the literal output of `dolt <command> --help` at the pinned version.
2. **Concepts / SQL versioning / install / Hosted / DoltHub:** `grep` [`references/docs/`](references/docs/). Files are slugified by full path, e.g. `introduction__installation__mac.md`, `sql-reference__version-control-features.md`, `concepts__dolt__git.md`. Start from `introduction__what-is-dolt.md`.
3. **Dolt under beads:** [`references/beads-integration.md`](references/beads-integration.md) — how the shared `dolt sql-server` backs beads (port 3308, `~/.beads/shared-server`), server maintenance, Dolt-level troubleshooting, and clean project bootstrap.
4. **If the installed `dolt` differs from `PINNED_VERSION`**, the CLI reference may not match — bump the pin and regenerate (`make update-working-with-dolt`), or run `dolt <cmd> --help` directly.

## Pinning model (what "pinned" means here)

- **CLI pages are version-EXACT.** They are the byte-for-byte `--help` output of the pinned `dolt` binary (`2.1.7`). The binary is `brew pin`'d so weekly upgrades don't drift it.
- **Website docs are a SNAPSHOT, not a version pin.** dolthub.com's docs are not URL-versioned (no `/v2.1.7/` paths), so `references/docs/` reflects the docs *as of the last fetch* — recorded by each file's `fetched_at`/`sha256`. Treat them as "current," and verify version-specific behavior against the live binary.

## Behavioral guidance

- The CLI reference reflects the **pinned** version only. If live `dolt <cmd> --help` disagrees, trust the binary and surface the drift.
- Dolt needs a working data directory and (for history) commits; it is **not** a drop-in for an arbitrary MySQL — it's MySQL-wire-compatible but Git-versioned underneath. Reach for it when you need who-changed-what-when, branchable data, or agent-safe (revertible) writes.
- **For how Joe runs beads on Dolt** (`--shared-server`, the shared server on port 3308, bootstrapping, `bd dolt …`), the `bd`-level recovery checklist lives in `beads-operations`. This skill owns the **Dolt-native** layer; `beads-operations` owns the **`bd`-command** layer. Cross-reference, don't duplicate.

## Reference map

- `references/cli/_index.md` — top-level `dolt --help` command list.
- `references/cli/<command>.md` — per-command `--help` (NAME/SYNOPSIS/DESCRIPTION/OPTIONS).
- `references/cli/<command>__<subcommand>.md` — group subcommands (e.g. `schema__export.md`, `remote.md` has no subpages since its subcommands are positional).
- `references/docs/*.md` — official dolthub.com docs, slugified by path.
- `references/beads-integration.md` — Dolt-as-beads-backend runbook (hand-written).

## Related skills

- `beads-operations` — running/troubleshooting beads day-to-day (`bd` commands, the shared-server conventions, compaction recovery).
- `working-with-beads` — the `bd` CLI reference at its pinned version.
- `working-with-git` — Dolt's version-control model mirrors Git; the Git reference helps with the branch/merge/diff mental model.
