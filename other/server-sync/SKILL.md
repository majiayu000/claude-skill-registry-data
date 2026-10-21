---
name: server-sync
description: Reference and safety checklist for the project's sync.sh, which pulls a remote DB and assets into local DDEV. Use for "pull prod data locally", "sync.sh fails", "REMOTE_* env", dry-run safety. For the full refresh workflow use ddev-sync. The reverse direction is server-deploy.
---

# Server Sync — Pull Remote → Local

Pulls the remote content state (database and assets) down to a local DDEV environment using `sync.sh`.

`sync.sh` is a **project-local script** in the project root; this skill does not ship it. If the project has none, stop and ask rather than writing one.

> **Note on "production":** `sync.sh` pulls from the *authoritative content source* — typically production, but may be a pre-prod server during pre-launch phases. The `.env` `REMOTE_*` vars always point to whichever environment holds the master content.

> **Higher-level workflow:** [`ddev-sync`](../ddev-sync/SKILL.md) wraps this in a full "refresh local dev" pipeline — start DDEV, run `sync.sh`, then run the framework build step. Prefer `ddev-sync` for day-to-day refreshes; use `server-sync` when you need the lower-level reference or safety checklist.

> [!WARNING]
> `sync.sh` is highly destructive. It will **drop and overwrite** the local DDEV database and assets. Always confirm the source environment before running.

## Prerequisites / Safety

> [!IMPORTANT]
> **DDEV containers don't inherit host SSH keys.** Run `ddev auth ssh` once per DDEV instance before either of these:
> - **`sync.sh`** — needs authenticated SSH to reach the remote server (see below).
> - **`composer update`/`install` on any SSH-sourced VCS package** (`git@github.com:...`, e.g. a `dynamic/*` module pulled as a VCS repository rather than from Packagist) — `ddev composer` fails to clone/fetch it until `ddev auth ssh` has run.
>
> Symptom without it: `Permission denied (publickey)`, or a stalled SSH prompt with no interactive terminal to answer it.

> [!IMPORTANT]
> **`sync.sh` runs INSIDE the DDEV container** (`ddev exec ./sync.sh`). It connects `mysql` / `mysqldump` to the ddev `db` service host and imports into the container DB, so it must run where that hostname resolves. The script validates `ssh rsync mysqldump mysql gzip gunzip` — note **no `ddev`** in that list.

```bash
# Authorize SSH agent first
ddev auth ssh

# Pull remote → local: runs INSIDE the container
ddev exec ./sync.sh
```

## Environment Configuration (`.env`)

`sync.sh` reads `REMOTE_*` vars from the project `.env`:

```text
REMOTE_USER="username"
REMOTE_HOST="target-host.com"
REMOTE_ASSETS_PATH="/var/www/html/public/assets"
REMOTE_DB_NAME="db_name"
REMOTE_DB_USER="db_user"
REMOTE_DB_PASSWORD="db_password"
REMOTE_DB_HOST="localhost"
```

> [!CAUTION]
> **`REMOTE_*` and `PREPROD_*` must point at DIFFERENT hosts** (this is the canonical copy; [`server-deploy`](../server-deploy/SKILL.md) and [`ddev-sync`](../ddev-sync/SKILL.md) point here). `sync.sh` reads `REMOTE_*` (pull FROM). [`deploy.sh`](../server-deploy/SKILL.md) reads `PREPROD_*` (push TO). If both vars resolve to the same host, you pull from pre-prod *and* deploy to pre-prod — production is never touched. Always verify before migration work:
> ```bash
> grep -E "REMOTE_HOST|PREPROD_HOST" .env    # must be two DIFFERENT hosts
> grep "^REMOTE_" sync.sh                   # sync.sh must read REMOTE_*
> ```

## Command Flags

| Flag | Description |
|------|-------------|
| `--help` | Shows usage information |
| `--dry-run` | Tests the `rsync` without writing to disk or importing the DB. **Note:** the remote `mysqldump` *is* executed and the dump is created even in dry-run mode — only the local import/restore is skipped. See the [dry-run caution](#dry-run-caution) below. Always recommend running `--dry-run` first. |
| `--assets` | Bypasses the database phase. Only syncs `public/assets/`. |
| `--db` | Bypasses the asset rsync phase. Only drops and imports the database. |
| `--exclude=PATTERN` | Exclude specific files or globs from the `rsync` cycle (repeat for multiple patterns). Example: `--exclude=*.log --exclude=_resampled/` |

## Script Internal Logic

1. **DB segment:** Runs `mysqldump` via SSH on the remote server, gzips to `/tmp`, pulls via `rsync`, then pipes through `gunzip` → drops local DB → imports.
2. **Remote cleanup:** Removes the dump from `/tmp` on the remote server.
3. **Assets segment:** Executes `rsync --delete` to map the remote `/assets/` directory down, purging orphaned local files.

## Dry-Run Caution

> [!WARNING]
> **`--dry-run` creates — and, if cleanup is gated incorrectly, leaves — a full DB dump in `/tmp` on the remote server.** The remote `mysqldump` runs before the dry-run gate; only the local import is skipped. If the script's cleanup step is gated on `!dry-run`, every `--dry-run` silently accumulates a complete DB dump on the server — a data-at-rest exposure.
>
> **Fix:** Make the remote cleanup unconditional — the dump is always created, so cleanup must always run:
> ```bash
> # Cleanup — always remove the remote dump (created even in --dry-run)
> ssh ${REMOTE_USER}@${REMOTE_HOST} "rm -f ${REMOTE_DUMP_PATH}"
> ```
> The dry-run gate should guard only the import/restore step. **Audit your local `sync.sh`** to confirm cleanup is not gated on dry-run mode.

## DDEV Lifecycle Gotchas

> [!WARNING]
> **`ddev poweroff` clears the ssh-agent.** After `ddev poweroff` (or a full restart) the ddev-ssh-agent container is removed, so the next `sync.sh` fails with an SSH auth error. Re-run `ddev auth ssh` before syncing. (`deploy.sh` uses host SSH, so it's unaffected.)

> [!WARNING]
> **OrbStack port forwarding goes stale after `ddev mutagen reset` + `ddev restart`.** The `.ddev.site` hostname can return `ERR_CONNECTION_RESET` even though the containers are healthy. Fully re-initialize with `ddev poweroff && ddev start`. A direct `127.0.0.1:<port>` (from `ddev describe`) often still works as a stopgap.
