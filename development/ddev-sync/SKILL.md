---
name: ddev-sync
description: Start DDEV, sync a remote database and assets into the local dev environment, and run the framework build step. Use when the user says "ddev sync", "sync remote database", "pull remote data", "set up local dev", or asks to sync a DDEV project with a remote environment.
---

# Skill: DDEV Sync & Dev Build

**Goal:** Fully synchronize a remote database and assets into the local DDEV environment — start DDEV, install dependencies, pull DB + assets from the authoritative remote via SSH, and run the framework build step.

## Prerequisites

DDEV must run the PHP version your framework requires. Check your framework's requirements and set `php_version` in `.ddev/config.yaml` before syncing.

## Deployment Model

- **The authoritative environment is the source of truth for content.** This is typically the live production server, but may be a pre-prod/staging server during pre-launch phases. Database and assets always flow **down** from the authoritative source to local (and optionally to lower environments). They are never pushed **up** to the authoritative source from local.
- **`sync.sh`** pulls the authoritative DB + assets into local DDEV. It is a one-way **down-sync** tool.
- **`deploy.sh`** pushes local DB + assets to a target environment (typically staging/pre-prod). It is never used against the authoritative source.
- Content is managed on the authoritative environment, then synced to local and lower environments as needed.

> **Clarification:** In `.env`, `REMOTE_*` always points to the authoritative source — whichever environment that is. During pre-launch, this may be a pre-prod server rather than production. If `REMOTE_HOST` points to a staging URL, that is intentional.

## Terminology

| Term | Meaning | Script |
|------|---------|--------|
| **Code deploy** | Deploys application code (PHP/CSS/JS) via CI/CD | `dhq deploy` (DeployHQ), or your CI pipeline |
| **Content sync** | Pulls DB + assets FROM the authoritative source to local | `sync.sh` (via `ddev exec ./sync.sh`) |
| **Content push** | Pushes local DB + assets TO a target environment | `deploy.sh` (via `bash deploy.sh`) |

> "Deploy" alone is ambiguous — always qualify as "code deploy" or "content push."

---

## When to Use

Automatically activate when the user:

- Asks to "sync" or "pull" remote data into local dev
- Says "ddev sync", "sync remote database", or "pull remote assets"
- Requests to "set up local dev environment" for a DDEV project
- Mentions syncing remote database and assets

---

## Prerequisites

Verify the following before proceeding:

1. **Project has DDEV configuration:**
   ```bash
   test -f .ddev/config.yaml
   ```
2. **Sync script exists** in project root:
   ```bash
   test -f sync.sh
   ```
3. **Dev build script** (optional — falls back to `ddev sake dev/build` if not present).

---

## Workflow

### Phase 1: Start DDEV & Install Dependencies

1. **Start the DDEV container:**
   ```bash
   ddev start
   ```

2. **Install composer dependencies:**
   ```bash
   ddev composer install
   ```

3. **Add SSH keys to the DDEV SSH agent:**
   ```bash
   ddev auth ssh
   ```

4. **Expose vendor module web directories:**
   ```bash
   ddev composer vendor-expose
   ```

### Phase 2: Sync Remote Data

> **⚠️ WARNING:** `sync.sh` will **drop and overwrite** your local database and assets with production data. Any local content changes (uncommitted DB changes, uploaded files) will be **permanently lost**. Ensure you've committed any work-in-progress before proceeding.

> [!IMPORTANT]
> Confirm `sync.sh` pulls from the **authoritative content source** (typically production; pre-prod during pre-launch):
> `grep REMOTE_HOST .env` — should be the environment that holds master content.
> `REMOTE_*` must differ from `PREPROD_*`; see the host check in
> [`server-sync`](../server-sync/SKILL.md#environment-configuration-env).

5. **Sync remote database and assets** (will prompt for confirmation — answer `Y`):
   ```bash
   ddev exec ./sync.sh
   ```

### Phase 3: Rebuild Dev Environment

6. **Run the dev build** (flushes caches, rebuilds database):
   ```bash
   # Use devbuild.sh if available (project-specific build wrapper)
   # Otherwise run the framework's standard build command.
   # Example (SilverStripe): ddev sake dev/build
   if test -f devbuild.sh; then
     ddev exec ./devbuild.sh
   else
     # Replace with your framework's build/migrate command:
     ddev exec ./vendor/bin/sake dev/build   # SilverStripe example
   fi
   ```

### Phase 4: Major-version upgrades — run the migration tasks

After `dev/build`, a synced DB from a *different major version* contains
source-version data in the target schema. It is NOT ready to serve. Run the
project's migration runbook:

```bash
ls .claude/commands/ | grep -i migrat      # project /command
ls .agent/skills/ 2>/dev/null              # project-specific skill
```

If none exists, consult your framework's migration documentation and formalize a
project-specific runbook (strongly recommended — each project's task list differs).
For SilverStripe, see the `ss-data-migration` / `silverstripe-3-to-4-upgrade` skills.

Do NOT assume the site is ready just because pages render — many frameworks have
lazy-migration patterns where pages resolve but relational data is still unmigrated.

---

## Important Notes

- **`sync.sh` typically requires SSH authentication.** Ensure `ddev auth ssh` has completed successfully before running the sync step.
- **The sync script usually prompts for confirmation.** Be prepared to confirm when prompted.
- **After a full sync, flush application caches** if templates or config changes aren't reflecting. For SilverStripe: append `?flush=all` to any page URL.
- **Asset permissions** may need adjustment after sync — check file/folder ownership inside the container if assets fail to load.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ddev: command not found` | Install DDEV: https://ddev.com/install/ |
| SSH auth fails inside container | Run `ddev auth ssh` again and verify keys are loaded |
| Sync script not found | Verify `sync.sh` exists in project root |
| Assets appear broken after sync | Run `ddev composer vendor-expose` and check file permissions |
| Changes not appearing after sync | Flush application caches. For SilverStripe: append `?flush=all` to URL, or run `ddev exec ./devbuild.sh flush=1` if `devbuild.sh` exists (otherwise `ddev exec ./vendor/bin/sake dev/build "flush=1"`) |
| `Mutagen sync completed with problems … unable to relocate staged file: file exists` | Mutagen is trying to sync user-uploaded assets. Set `upload_dirs` so the assets dir is bind-mounted instead — see [Mutagen `upload_dirs` conflicts](#mutagen-upload_dirs-conflicts-after-prod-sync) below. |

## Mutagen `upload_dirs` conflicts after prod sync

On Mutagen-enabled DDEV projects, the **first prod asset sync after a fresh start** frequently fails with:

```
Mutagen sync completed with problems
  <file>: unable to create file: unable to relocate staged file: file exists
```

The conflicting files are user-uploaded assets (e.g. `assets/SecureUploads/<file>.docx`, resampled image
variants under `_resampled/`). The site won't serve until it's resolved, and it recurs on **every** prod
sync — a standing trap during the sync → migrate → VR loop.

**Fix:** set `upload_dirs` in `.ddev/config.yaml` so Mutagen **bind-mounts** the assets dir instead of
syncing it through Mutagen:

```yaml
upload_dirs:
  - assets
  # add ../node_modules too if it's a large sibling dir that doesn't need Mutagen sync
```

Then:

```bash
ddev mutagen reset && ddev restart
ddev mutagen st <project>   # confirm it shows: ok: watching
```
