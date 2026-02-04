---
name: update-nexus
description: Update Nexus system files from upstream repository. Load when user says "update nexus", "sync nexus", "get nexus updates", "check for updates", "upgrade nexus". Safely pulls system updates while protecting user data.
---

# Update Nexus

> **Purpose**: Sync system files from the upstream Nexus repository while protecting user data
>
> **Trigger**: "update nexus", "sync nexus", "get updates", "check for updates"
>
> **Duration**: 1-2 minutes

---

## What This Does

Updates these **system files** from upstream:
- `00-system/` - Core framework, skills, documentation
- `CLAUDE.md` - Entry point
- `README.md` - Project readme

Protects these **user folders** (NEVER touched):
- `01-memory/` - Your goals, learnings, config
- `02-projects/` - Your projects
- `03-skills/` - Your custom skills
- `04-workspace/` - Your files
- `.env`, `.claude/` - Your secrets and settings

---

## Workflow

### Step 1: Check for Updates

Run the update check:
```bash
python 00-system/core/nexus-loader.py --check-update
```

**Parse the JSON response:**
- If `checked: false` with error → Display error, exit gracefully
- If `update_available: false` → Display "Already up-to-date!", exit
- If `update_available: true` → Continue to Step 2

### Step 2: Show What Will Change

Display to user:
```
UPDATE AVAILABLE

Current version: {local_version}
New version:     {upstream_version}

Files to update ({changes_count}):
{list changed_files, max 20}

PROTECTED (will NOT be touched):
- 01-memory/    (your goals & config)
- 02-projects/  (your projects)
- 03-skills/    (your custom skills)
- 04-workspace/ (your files)
```

### Step 3: Confirm with User

Ask: **"Proceed with update? (yes/no)"**

- If no → Exit with "Update cancelled"
- If yes → Continue to Step 4

### Step 4: Perform Sync

Run the sync command:
```bash
python 00-system/core/nexus-loader.py --sync --force
```

**Parse the JSON response:**
- If `success: false` → Display error message, suggest fixes
- If `success: true` → Continue to Step 5

### Step 5: Display Results

On success, display:
```
UPDATE COMPLETE!

{local_version} → {upstream_version}

Updated paths:
{list files_updated}

Backup saved to: {backup_path}

To commit this update:
  git add . && git commit -m "Update Nexus to v{upstream_version}"
```

---

## Error Handling

| Error | User Message |
|-------|--------------|
| "Not a git repository" | "This folder isn't a git repo. Initialize with: git init" |
| "Could not reach upstream" | "Can't connect to GitHub. Check your internet connection." |
| "Uncommitted changes detected" | "You have uncommitted changes. Commit them first:\n  git add . && git commit -m 'Save changes'" |
| "Could not read upstream version" | "The upstream repo might not be set up correctly. Check the URL in user-config.yaml" |

---

## Advanced: Dry Run

To preview changes without applying:
```bash
python 00-system/core/nexus-loader.py --sync --dry-run
```

This shows what WOULD change, but doesn't change anything.

---

## Notes

- **Backup**: Before any sync, your current system files are backed up to `.sync-backup/{timestamp}/`
- **Safe**: User data folders are NEVER in the sync paths - they cannot be touched
- **Upstream Remote**: Automatically added on first use (named "upstream")
- **Default URL**: https://github.com/beamanalytica/Nexus-v4.git (can override in user-config.yaml)
