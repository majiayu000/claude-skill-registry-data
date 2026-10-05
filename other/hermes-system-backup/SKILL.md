---
name: hermes-system-backup
description: "Full Hermes system backup and restore — inventory all components, create a private GitHub backup repo, organize config/scripts/cron/profiles/MCP/state, write restore documentation, and push."
version: 1.1.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [backup, restore, disaster-recovery, hermes, system-audit, migration]
    triggers: [backup, restore, disaster recovery, backup hermes, system backup, migrate hermes, inventory hermes, migration audit, full system audit, pre-migration, reformat audit, drive inventory, before reformat]
    related_skills: [hermes-profile-transfer, imap-watchdog, hermes-agent]
---
# Hermes System Backup & Restore

Full system backup procedure for Hermes Agent. Captures everything needed to restore a Hermes installation from scratch: config, profiles, scripts, cron jobs, MCP servers, plugins, gateway state, memory, and system architecture documentation.

## When to Run

- Initial setup (first time configuring Hermes)
- After significant config changes (new MCP servers, profiles, gateways)
- Before major upgrades or OS reinstalls
- Monthly as maintenance

## Backup Procedure

### 1. Create Private GitHub Repo (Disaster Recovery)

For a recoverable offsite backup, create a private GitHub repo. This is the **ideal for DR** — survives a total machine loss.

For **frequent automated backups** (weekly cron), local disk is faster and simpler — see the Quick Local Backup section below.

```bash
gh repo create hermes-system-backup --private \
  --description "Full Hermes Agent system backup" \
  --gitignore Python
git clone https://github.com/YOUR_USER/hermes-system-backup.git
cd hermes-system-backup
mkdir -p config/profiles cron scripts skills plugins state/memory gateway mcp-servers patches
```

**Always create the repo as private** unless explicitly told public.

### 2. Inventory and Copy Config

```bash
cp ~/AppData/Local/hermes/config.yaml config/
cp ~/AppData/Local/hermes/prefill.json config/
cp ~/AppData/Local/hermes/SOUL.md config/
cp ~/AppData/Local/hermes/models.json config/
```

Extract env var names (not values) from `.env` into `config/env-vars-required.md`:
```bash
grep -oP '^[A-Z_]+(?==)' ~/AppData/Local/hermes/.env | sort > config/env-vars-required.md
```

### 3. Copy All Profile Configs

```bash
for profile in ~/AppData/Local/hermes/profiles/*/; do
  name=$(basename "$profile")
  cp "$profile/config.yaml" "config/profiles/$name.yaml"
done
```

### 4. Copy Scripts

```bash
cp -r ~/AppData/Local/hermes/scripts/ .
# Remove large data files (>100MB) that won't fit on GitHub
rm -rf scripts/*.zip scripts/*_tax_roll* scripts/leepa_2025/ scripts/opportunity_report.json
```

### 5. Copy Cron Jobs

```bash
cp ~/AppData/Local/hermes/cron/jobs.json cron/
```

### 6. Copy State and Gateway Files

```bash
cp ~/AppData/Local/hermes/memories/MEMORY.md state/memory/
cp ~/AppData/Local/hermes/memories/USER.md state/memory/
cp ~/AppData/Local/hermes/channel_directory.json gateway/
cp ~/AppData/Local/hermes/council-state.json gateway/
cp ~/AppData/Local/hermes/gateway_state.json gateway/
cp ~/AppData/Local/hermes/processes.json gateway/
```

### 7. Dump State DB Schema

```bash
sqlite3 ~/AppData/Local/hermes/state.db .schema > state/schema.sql
```

### 8. Copy Plugins

```bash
cp -r ~/AppData/Local/hermes/plugins/ .
```

### 9. Document MCP Servers

Read the `mcp_servers` section from config.yaml and write a markdown table with:
- Server name
- Command and args
- Workdir (for local path servers)
- Timeout
- Env vars required
- Purpose

### 10. Write Architecture Document

Create `architecture.md` with:
- System overview table (profiles count, MCP count, cron count, scripts count, etc.)
- Model configuration
- Gateway platforms and channels
- Memory system provider
- Custom Hermes source patches (tab reuse, etc.)
- Known issues with cron jobs
- File size: 1-2 pages, scannable

### 11. Write Restore Guide

Create `restore-guide.md` with step-by-step instructions:
1. Install Hermes (`pip install hermes-agent`)
2. Copy scripts back to `~/AppData/Local/hermes/scripts/`
3. Restore config.yaml
4. Restore each profile: `hermes profile create NAME --from ~/path`
5. Restore cron jobs from jobs.json
6. Re-add MCP servers from documentation
7. Restore state files (memory, gateway, kanban)
8. Set up .env with required variables
9. Apply custom patches (git cherry-pick)
10. Verify: `hermes doctor`, `cronjob list`

### 12. Write Cron README

Parse jobs.json and produce a schedule table:
- Job name, schedule, type (script/no_agent vs skill/prompt), deliver target, status

### 13. Handle Large Files

GitHub has a 100MB file limit. Before pushing:
```bash
# Find files over 90MB
find . -type f -size +90M -exec ls -lh {} \;
# Remove from Git tracking but keep locally
git rm --cached largefile.zip
```

Use `git filter-branch` to purge large files from history if accidentally committed:
```bash
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/largefile' \
  --prune-empty -- --all
```

Then force push.

### 14. Commit and Push

```bash
git add -A
git commit -m "Hermes system backup YYYY-MM-DD"
git push origin main
```

## Quick Local Backup (Weekly Cron)

For **automated weekly backups** that don't require a GitHub repo, use this simpler local-disk pattern:

```bash
BACKUP_DIR=${USER_HOME}/Backups/hermes
mkdir -p "$BACKUP_DIR"/{config/profiles,cron,state/memory,gateway}

# Config
cp ~/AppData/Local/hermes/config.yaml "$BACKUP_DIR/config/"
cp ~/AppData/Local/hermes/SOUL.md "$BACKUP_DIR/config/"
cp ~/AppData/Local/hermes/auth.json "$BACKUP_DIR/config/"

# Profile configs
for profile in ~/AppData/Local/hermes/profiles/*/; do
  name=$(basename "$profile")
  cp "$profile/config.yaml" "$BACKUP_DIR/config/profiles/$name.yaml" 2>/dev/null
done

# Scripts
cp -r ~/AppData/Local/hermes/scripts/. "$BACKUP_DIR/scripts/" 2>/dev/null

# Cron
cp ~/AppData/Local/hermes/cron/jobs.json "$BACKUP_DIR/cron/" 2>/dev/null

# State
cp ~/AppData/Local/hermes/kanban.db "$BACKUP_DIR/state/" 2>/dev/null
cp ~/AppData/Local/hermes/memories/MEMORY.md "$BACKUP_DIR/state/memory/" 2>/dev/null
cp ~/AppData/Local/hermes/memories/USER.md "$BACKUP_DIR/state/memory/" 2>/dev/null
sqlite3 ~/AppData/Local/hermes/state.db ".schema" > "$BACKUP_DIR/state/schema.sql" 2>/dev/null

# Gateway
cp ~/AppData/Local/hermes/channel_directory.json "$BACKUP_DIR/gateway/" 2>/dev/null
cp ~/AppData/Local/hermes/gateway_state.json "$BACKUP_DIR/gateway/" 2>/dev/null

# Env var names (not values)
grep -oP '^[A-Z_]+(?==)' ~/AppData/Local/hermes/.env 2>/dev/null | sort > "$BACKUP_DIR/config/env-vars-required.md"
```

**Implemented Jun 26, 2026:** Weekly cron job `3133b8d09407` runs this every Sunday at 2AM ET. See `implementation-tracker.md` for up-to-date status.

**Pitfall — C: vs E: drive paths:** Some files (implementation-tracker, customization docs) live on C: drive under `${USER_HOME}\Documents\github\_project\`, while cloned repos and git-mcp DB live on E: drive. Backup scripts must check both. Use absolute paths, not relative, to avoid silent omissions.

## Restore Procedure (from backup)

### Prerequisites
- Python 3.11+, pip, Hermes installed
- GitHub token with repo access
- Gmail App Password (if using IMAP watchdogs)
- API keys for all services (from password manager)

### Quick Restore

```bash
git clone https://github.com/YOUR_USER/hermes-system-backup.git
cd hermes-system-backup

# 1. Restore scripts
cp -r scripts/* ~/AppData/Local/hermes/scripts/

# 2. Restore config
cp config/config.yaml ~/AppData/Local/hermes/
cp config/prefill.json ~/AppData/Local/hermes/
cp config/SOUL.md ~/AppData/Local/hermes/

# 3. Restore profiles
for f in config/profiles/*.yaml; do
  name=$(basename "$f" .yaml)
  hermes profile create "$name"
  cp "$f" ~/AppData/Local/hermes/profiles/"$name"/config.yaml
done

# 4. Restore state
cp state/memory/* ~/AppData/Local/hermes/memories/
cp gateway/* ~/AppData/Local/hermes/

# 5. Restore cron
cp cron/jobs.json ~/AppData/Local/hermes/cron/

# 6. Re-add MCP servers (from mcp-servers/README.md)
# 7. Set up .env with required vars (from config/env-vars-required.md)
# 8. Restore plugins
cp -r plugins/* ~/AppData/Local/hermes/plugins/
```

## Pre-Migration System Audit

When the user asks for a full backup audit before OS migration (Windows -> Linux, or full reformat), the existing Hermes-only backup is insufficient. You need a **system-level audit** covering drives, every git repo, Docker infrastructure, databases, and external config stores.

See `references/system-audit-methodology.md` for the full scan methodology, commands, and classification framework.

### Quick-Start: Seven Audit Phases

1. **Drive layout** — `df -h` on all drives; note OS vs data drives
2. **Hermes core** — state.db, config.yaml, .env, profiles, cron, comms_tracker, kanban
3. **Git repos** — find all repos, check dirty files + unpushed commits + remote URLs
4. **Docker** — images, containers, volumes (especially Postgres DB volumes)
5. **External stores** — n8n, SSH keys, browser profiles, memory systems, freelance automation
6. **Backup classification** — Git-backed / Git+dirty / Not backed up-CRITICAL / Redownloadable
7. **Action plan** — commit+pull all dirty repos, dump DBs, tar volumes, copy state.db

### Docker Volume Backup

Docker volumes contain ALL database state for the application stacks (Twenty CRM, n8n, Mautic, Postgres, etc.). They are **not backed up by git** and are the highest-risk item on reformat.

**For running containers (Postgres):**
```bash
# Dump all databases from a Postgres container
docker exec <container> pg_dumpall -U <user> > backup_$(date +%Y%m%d).sql

# Or per-database
docker exec <container> pg_dump -U <user> <dbname> > database_<dbname>_$(date +%Y%m%d).sql
```

**For standalone volume backup:**
```bash
# Stop the container first, then tar the volume
docker run --rm -v <volume_name>:/data -v $(pwd):/backup alpine \
  tar czf /backup/<volume_name>_$(date +%Y%m%d).tar.gz -C /data .
```

**On Linux Docker Desktop (WSL2):** volumes live at `\\wsl$\docker-desktop-data\version-pack\...`
**On native Linux:** volumes are at `/var/lib/docker/volumes/<volume_name>/_data/`

### Git Repo Dirty-Work Scan

Use this bash one-liner to inventory all repos before migration:

**PITFALL (Windows git-bash): `git -C` does NOT understand MSYS paths** (`/c/Users/...`) — it fails with "cannot change to ... No such file or directory", and with stderr suppressed every repo falsely reports `dirty=0` + `NO-REMOTE`. Always `cd` into the repo in a subshell instead:

```bash
for d in /path/to/repos/*/; do
  if [ -d "$d.git" ]; then
    r=$(basename "$d")
    ( cd "$d" 2>/dev/null || exit 0
      dirty=$(git status --short 2>/dev/null | wc -l)
      unpushed=$(git log --oneline @{u}..HEAD 2>/dev/null | wc -l)
      remote=$(git remote get-url origin 2>/dev/null || echo "NO-REMOTE")
      [ "$dirty" -gt 0 ] || [ "$unpushed" -gt 0 ] || [ "$remote" = "NO-REMOTE" ] && \
        echo "UNSAFE: $r ($dirty dirty, $unpushed unpushed) -> $remote"
    )
  fi
done
```

Sanity-check the scan: if EVERY repo comes back NO-REMOTE/dirty=0, the scan itself is broken — spot-check one known repo by `cd`-ing in and running `git status` by hand.

### Pre-Migration Checklist

Before reformat, execute in order:

1. `git stash` or `git commit` all dirty work in every repo, then `git push`
2. Fix repos with broken/no remotes (add origin with `git remote add origin <url>`)
3. `cp ~/AppData/Local/hermes/state.db /backup/` — the single most important file
4. `cp ~/AppData/Local/hermes/.env /backup/`
5. Dump each running Postgres container with pg_dumpall
6. Tar each Docker volume with alpine sidecar container
7. `cp -r ~/.ssh/ /backup/`
8. `cp ~/.n8n/database.sqlite /backup/`
9. Take Hermes snapshot: `hermes snapshot` (or manually copy state.db after clean shutdown)
10. Save image list: `docker images --format '{{.Repository}}:{{.Tag}}' > /backup/docker-images.txt`
11. Save compose files: `find /e/ -name "docker-compose.yml" > /backup/compose-locations.txt`

## Pitfalls

- **Large files**: Tax roll CSVs, ZIP archives, and data snapshots can exceed GitHub's 100MB limit. Exclude them from the repo and note their location in the README.
- **Env values**: Never commit actual API keys. Only document the variable names.
- **State DB**: The 1.69GB state.db is too large for GitHub. Only back up the schema, not the data. Session history can be regenerated.
- **Skills**: Skills are reinstalled from the hub (`hermes skills install`). Don't back up the entire skills directory — note which skills are installed in the architecture doc instead.
- **Kanban DB**: The kanban.db is small enough to back up (114KB). Copy it alongside other state.
- **Windows paths**: All paths in restore-guide.md should use POSIX-style paths under `/c/Users/...` for git-bash compatibility. Note the MSYS_NO_PATHCONV=1 workaround for Docker commands involving Windows paths.
- **Profile config merge**: When restoring profile configs, ensure all 4 model fields (api_mode, base_url, default, provider) are present. Incomplete model sections silently fall back to bedrock provider.
- **Line endings**: Backup repo on Windows may need `.gitattributes` to normalize line endings. Set `* text=auto` to avoid CRLF/LF warnings.
