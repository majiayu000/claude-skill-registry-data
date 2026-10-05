---
name: obsidian-backup
description: >-
  Run the vault data-safety runbook: 3-2-1 backup, the never-deleted originals archive, the
  schedulers that keep it running, and the restore or new-machine migration procedure. Verifies
  by reading state rather than trusting exit codes. Triggers: "make a backup", "verify the
  backup", "the backup looks broken", "restore the vault".
license: MIT
---

# Obsidian backup & restore (data-safety runbook)

> 🧒 **When reporting to Anton:** always end with a child-simple "In plain words" recap in his language (plain words, no jargon) — his standing request. See memory `eli5-always`.

This skill is the operational runbook for Anton's vault data-safety system. The **rules** (always preserve originals; always back up offsite to Google Drive) live in memory — `preserve-originals-rule`, `vault-offsite-backup` — and in the import skills (`obsidian-ingest` Rule 0, `telegram-reimport` Step 0). **Don't re-derive or duplicate them here.** This file says *what to run, where things are, and how to recover*.

## The system at a glance — 4 layers

1. **Originals (Rule 0).** Every import's raw source is copied verbatim to `$OBSIDIAN_ROOT/_originals/<key>\<date>__<name>\` (sha256 manifest), **never deleted**. Script: `archive_original.py`.
2. **3-2-1 backup.** Vault → one **git bundle** (full history) + `_originals` copy-only → to **Google Drive** (offsite/cloud) **and** `<LOCAL_BACKUP_DIR>` (separate disk). Script: `backup_to_drive.py`.
3. **Nightly automation.** Windows Task Scheduler job `Obsidian Backup to Drive` runs the backup daily 03:00 (runs even when Claude is closed).
4. **Weekly watchdog.** Claude routine `obsidian-backup-healthcheck` (Mon ~10:00) runs `backup_healthcheck.py` and Telegrams Anton — heartbeat if fine, alert (and may self-heal) if broken.

### Where everything is (this machine)

| Thing | Path |
|---|---|
| Vault (git repo) | `$OBSIDIAN_VAULT` |
| Originals (permanent) | `$OBSIDIAN_ROOT/_originals/` (+ `README.txt`) |
| Scripts | `$IMPORTS_ROOT/{archive_original,backup_to_drive,backup_healthcheck}.py` (+ `backup_to_drive.cmd`, log `backup_to_drive.log`, verdicts in `backup_health\`) |
| **Offsite copy (cloud)** | `<GDRIVE_ROOT>\Obsidian-Backup\` — Google account **owner.personal@example.com** (G: shortcut → this folder; Google uploads to cloud) |
| **Local copy (2nd disk)** | `<LOCAL_BACKUP_DIR>\` |
| Each copy holds | `vault\Owner-Knowledge-<date>.bundle` (last 14 kept) · `_originals\` · `MIGRATE.md` · `last-backup.txt` |

Path is machine-specific (`Google Drive on HP Palo Alto`); on another machine, `backup_to_drive.py` auto-detects `E:\Google Drive on*`.

## Common tasks

All commands run with `$env:PYTHONUTF8=1` in PowerShell.

**Back up now** (commit vault → bundle+verify → Drive + C:):
```
python $IMPORTS_ROOT/backup_to_drive.py
```
Good habit after big imports (alongside the brain reindex). Google finishes uploading in the background.

**Check the backup is healthy now:**
```
python $IMPORTS_ROOT/backup_healthcheck.py
```
Prints `STATUS OK` / `STATUS PROBLEM`; full verdict at `$IMPORTS_ROOT/backup_health/health-latest.md`.

**Archive an import original** (Rule 0 — also auto-done by the import skills):
```
python $IMPORTS_ROOT/archive_original.py "<source path>" --source <key> --label "<note>"
```

**Restore / migrate** — see the next section.

**Manage the nightly Windows task:**
```
Get-ScheduledTaskInfo -TaskName 'Obsidian Backup to Drive'   # last/next run, result
Start-ScheduledTask   -TaskName 'Obsidian Backup to Drive'   # run now
Disable-ScheduledTask -TaskName 'Obsidian Backup to Drive'   # pause
```

**Manage the weekly watchdog routine:** the `Scheduled` section in the sidebar, or the `scheduled-tasks` MCP (`list_scheduled_tasks` / `update_scheduled_task` taskId `obsidian-backup-healthcheck`). After (re)creating it, click **Run now** once to pre-approve PowerShell + Telegram.

## Restore & migrate (the disaster runbook)

The backup folder (Drive **or** C:) is self-describing — it contains `MIGRATE.md`. The vault lives entirely inside the newest `vault\Owner-Knowledge-<date>.bundle` (full git history in one file).

**Migrate the whole vault to a NEW computer:**
1. Install Git + Obsidian. Sign into Google Drive `owner.personal@example.com` so `Obsidian-Backup\` syncs down (or copy it from `<LOCAL_BACKUP_DIR>`).
2. Take the **newest** bundle in `Obsidian-Backup\vault\`.
3. `git clone "Owner-Knowledge-<date>.bundle" Owner-Knowledge` → the result is the full vault repo with history.
4. Open that folder as an Obsidian vault. Copy `_originals\` across too (it's just files).

**Restore a single file / folder:**
```
git clone "<newest>.bundle" tmp_restore
# copy the file out of tmp_restore\ ... OR an older version:
git -C tmp_restore log --oneline -- "<path>"
git -C tmp_restore restore --source <hash> -- "<path>"
```
(For an in-place vault you can also recover from the live repo: `git -C $OBSIDIAN_VAULT restore --source <hash> -- <path>` — see [[vault-backup-rule]].)

## Troubleshooting — "the backup looks broken"

`backup_healthcheck.py` pinpoints which check failed. Map:

- **Stale / missing bundle, but task still Enabled** → the daily job just didn't run (PC was off, etc.). Fix: run `backup_to_drive.py` once. (The watchdog does this automatically.)
- **Windows task MISSING or DISABLED** → re-enable (`Enable-ScheduledTask -TaskName 'Obsidian Backup to Drive'`) or re-register:
  ```
  $action   = New-ScheduledTaskAction -Execute '$IMPORTS_ROOT/backup_to_drive.cmd'
  $trigger  = New-ScheduledTaskTrigger -Daily -At '3:00AM'
  $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1) -MultipleInstances IgnoreNew
  Register-ScheduledTask -TaskName 'Obsidian Backup to Drive' -Action $action -Trigger $trigger -Settings $settings -Force
  ```
  (Registering a scheduled task needs Anton's explicit OK — it can trip the persistence guard.)
- **Bundle FAILED `git bundle verify` (corruption)** → do NOT trust it. Keep the older good bundles (we retain 14), check the vault repo health (`git -C $OBSIDIAN_VAULT fsck`), then run a fresh `backup_to_drive.py`. Don't delete the bad bundle until a good one exists.
- **`_originals` lagging in a target** → re-run `backup_to_drive.py` (robocopy is copy-only, it'll catch up).
- **Drive not uploading** → confirm Google Drive for Desktop is running and signed into `owner.personal@example.com`; the local `Obsidian-Backup\` is on E: and syncs from there.

## Invariants (never violate)

- **Never delete anything under `_originals\`** — ever. It's the upstream source of truth.
- Originals/backups of originals are **copy-only** (robocopy `/E /XO`, never `/MIR`) — deletions must never propagate.
- The **git bundle is the migration artifact** — keep it self-contained (`--all`), verify before trusting.
- Don't sync the live vault folder (or live `.git`) into Drive directly — we back up the *bundle*, on purpose (avoids corruption / conflict copies / ransomware propagation).
- The standing rules are in memory ([[preserve-originals-rule]], [[vault-offsite-backup]]); reference them, don't fork them.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
