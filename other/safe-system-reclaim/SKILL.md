---
name: safe-system-reclaim
description: "Use for safe system tidy/reclaim without data loss."
version: 1.0.0
author: Hermes Agent
platforms: [windows]
metadata:
  hermes:
    tags: [system-tidy, reclaim, archive-first, docker, hermes, windows, consolidation]
    triggers: [consolidate data, clean everything up, tidy system, reclaim disk safely, cleanup without losing data, keep going on cleanup, professionalize system]
    related_skills: [hermes-operational-audit, local-project-discovery, windows-cron-msys-path-fix]
---

# Safe System Reclaim

Use when the user wants a broad system cleanup while preserving important data and avoiding service interruption. Class-level procedure for Windows Hermes + Docker + multi-drive repos.

## Core policy

1. **Archive or move first. Verify sizes and integrity. Only then remove the source.**
2. Keep revenue/runtime services running unless explicitly authorized to park them.
3. Never delete named Docker volumes, live databases, dirty git clones, or credential files casually.
4. Use reversible parking for runtime clutter: `docker stop` + `docker update --restart=no`; retain volumes.
5. Maintain an execution log and restore map under `~/AppData/Local/hermes/plans/system-tidy-YYYY-MM-DD/`.
6. Report two metrics separately: bytes archived/reclaimed internally vs OS-visible free-space delta. Docker sparse VHDX may delay the latter.
7. When the user says **get started** / **keep going** on a safe path, execute archive-first stabilize + reclaim + reversible park. Irreversible volume/repo wipes still need explicit OK.

## Workflow

### 1. Preflight

- Measure C: and E: free space.
- Inventory running services, Docker containers, named volumes, and critical endpoints.
- Back up `.env`, active config, and any source that will be rewritten.
- Identify canonical project paths and check `git status --porcelain` before touching clones.

### 2. Stabilize automation

- Deduplicate `.env` with a last-non-empty-wins policy; preserve a dated backup and verify required keys remain populated.
- Pin cron provider/model drift with CLI: `hermes cron edit <id> --provider <p> --model <m>` (agent `cronjob update` may reject pin fields).
- Replace fragile `.sh` cron entrypoints with Python `bash -s` wrappers when MSYS path mangling appears.
- For Windows-native Python/Node calls from MSYS, use `C:/...` or `E:/...` paths; do not pass `/c/...` or `/e/...` to native executables.

### 3. Reclaim hot data

- Gzip large logs to E:, then truncate in place so active writers keep their file handles.
- Re-check high-volume logs at the end; if a log refills immediately, diagnose crash loops or noisy ping logging rather than repeatedly deleting it.
- Install missing MCP deps into the **project venv named in config.yaml** when stderr shows ModuleNotFoundError.
- Move data archives out of `scripts/` into a typed `data/` directory and patch consumers with an environment override plus legacy fallback.
- Move old backups, installer archives, curator backups, and corrupt config snapshots to cold storage.
- Prefer Python `pathlib`/`shutil` for large trees if robocopy under MSYS path-doubles (`C:\c\...`).

### 4. Park redundant runtime

- Attribute host ports by PID and executable path before stopping services; service names are not proof of port ownership.
- Park orphan stacks only after confirming their primary server is absent (e.g. Temporal UI/ES/PG without Temporal server).
- Keep named volumes. Do not remove large model volumes without an explicit decision.
- Keep the primary revenue stack and core memory/gateway services running.
- **`docker update --restart=no` alone is not durable** if compose still says `restart: unless-stopped` — Docker Desktop restarts may revive those containers. Also use `docker compose down` (never `-v` when preserving data), remove leftovers, and set compose restart to `"no"`; keep a dated compose backup.
- Docker `daemon.json` log caps apply mainly to new/recreated containers; existing containers retain their previous LogConfig until recreated.

### 5. Clean project sprawl

- Prefer one canonical writable clone and one optional archive.
- A clean stale clone can be zipped to `${MY_REPOS}/Archives/repos/` and removed. If Windows locks `.git/objects/pack`, rename to `_STALE_<name>_DELETE_OK_<date>` and retry later.
- Never remove a dirty clone; reconcile or archive it first.
- Confirm canonical identity with remote URL, branch, last commit, dirty state, and Docker compose working_dir labels.
- Compose project case splits (`bookends` vs `BookEnds`) are one product unless labels prove otherwise.

### 6. Safe Docker band

Only perform the low-risk set by default:

```text
docker container prune -f
docker image prune -f
docker builder prune -f
```

Do not volume-prune model/database volumes. Docker `daemon.json` log caps require a Docker Desktop restart to apply; record that interruption separately.

For a large named volume, require a **complete** offline archive before `volume rm`. File-by-file `cp -a` can take hours or stall; prefer a streaming `tar`/rsync-style copy or Docker data-root relocation. If interrupted, write `BACKUP-INCOMPLETE.txt` and leave the source volume intact. VHDX compact (`wsl --shutdown` + Optimize-VHD/diskpart) is a separate maintenance window and must never run during a volume copy.

### 7. Verification

- Confirm critical containers/endpoints remain healthy.
- Confirm `.env` required keys are non-empty.
- Confirm archives exist and source removals were preceded by size verification.
- Re-stat high-volume logs.
- Write a restore map and list intentionally untouched high-risk items.

## Failure patterns

- `C:Users...` or `C:\c\Users...` = MSYS path invocation failure, not necessarily a missing script.
- A service running does not prove it owns a port; map PID → process path.
- Docker prune can report internal reclaim while `df` barely changes because `docker_data.vhdx` is sparse; do not call the reclaim a failure.
- A multi-GB log that immediately refills indicates active producer noise/crash-loop; fix producer or add rotation.
- Tax-roll data after tidy: `~/AppData/Local/hermes/data/land/leepa_2025/` with `LEEPA_DATA_DIR` override.

## Supporting files

- `references/safe-reclaim-playbook.md` — archive/park/verify sequence and rollback.
- `references/execution-lessons-2026-08-07.md` — validated Windows/Hermes/Docker lessons from a full tidy pass.
- `references/pass3-docker-restart-lessons-2026-08-07.md` — compose restart durability, Docker log-config inheritance, large-volume backup safeguards, and MCP project-venv isolation.
