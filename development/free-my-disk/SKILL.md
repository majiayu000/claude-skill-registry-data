---
name: free-my-disk
description: Safely audit and reclaim disk space on macOS and Ubuntu/Linux hosts, including remote servers over SSH. Use when the user says their Mac, Linux box, VPS, or server disk is full, asks what can be safely deleted, wants to clean caches, developer artifacts, Docker storage, apt/Homebrew/npm/pnpm/yarn/pip/uv caches, journal/log files, Xcode data, editor extensions, node_modules, Trash, crontab/systemd timer disk checks, or asks for a repeatable free-space cleanup workflow.
---

# Free My Disk

## Core Rule

Prefer a read-only audit before deleting anything. Classify findings into safety tiers, explain likely impact, and only delete after the user clearly asks to clean. Never delete personal documents, project archives, photos, mail, source repositories, Docker volumes, databases, app containers, or production data unless the user explicitly names them.

## Quick Audit

Detect the platform first:

```bash
uname -a
df -h /
```

For macOS, run the bundled read-only script first when possible:

```bash
bash scripts/audit_macos_disk.sh
```

Use `PROJECT_SCAN=1 bash scripts/audit_macos_disk.sh` to include common project roots such as `~/projects`, `~/code`, `~/src`, and `~/work`. Use `FULL_SCAN=1 bash scripts/audit_macos_disk.sh` only when the user wants a deeper scan and the disk has enough free space for a slower traversal.

For Ubuntu/Linux, run the bundled read-only script first when possible:

```bash
bash scripts/audit_linux_disk.sh
```

Use `PROJECT_SCAN=1 bash scripts/audit_linux_disk.sh` to include common user and project roots such as `~/projects`, `~/code`, `~/src`, `~/work`, and `/opt`. Use `FULL_SCAN=1 bash scripts/audit_linux_disk.sh` only when the user wants a deeper scan.

For a remote host, replace `my-server` with the actual hostname or SSH config alias, then copy or stream the script over SSH:

```bash
ssh my-server 'bash -s' < scripts/audit_linux_disk.sh
ssh my-server 'PROJECT_SCAN=1 bash -s' < scripts/audit_linux_disk.sh
```

If the script is not suitable, gather the same facts manually:

```bash
df -h /
du -sh ~/Library/Caches ~/.npm ~/.pnpm-store ~/.yarn ~/.cache ~/Library/Logs ~/.Trash 2>/dev/null
du -sh ~/Library/Containers/com.docker.docker ~/Library/Developer ~/Downloads 2>/dev/null
find ~ -xdev -type f -size +1G -print 2>/dev/null | head -100
```

On Linux, prefer these manual checks:

```bash
df -h /
df -ih /
sudo du -xhd 1 / 2>/dev/null | sort -h | tail -30
du -sh ~/.cache ~/.npm ~/.pnpm-store ~/.yarn ~/.cache/pip ~/.local/share/uv ~/.local/share/Trash 2>/dev/null
sudo journalctl --disk-usage 2>/dev/null || true
docker system df 2>/dev/null || true
find "$HOME" -xdev -type f -size +1G -print 2>/dev/null | head -100
```

Use `du -xhd 1 <dir> | sort -h | tail` for large directories. Prefer targeted scans over full-home scans when the disk is very full. On remote Linux servers, include inode pressure with `df -ih /`; many tiny logs or cache files can fill inodes before bytes.

## Safety Tiers

Treat these as usually safe to clean on macOS:

- Homebrew old versions and cache: `brew cleanup`, then optionally remove `~/Library/Caches/Homebrew/*`.
- Package manager caches: `npm cache clean --force`, `pnpm store prune`, `yarn cache clean`.
- Reinstallable dependencies the user names: `node_modules`, `.venv`, build outputs, `.next`, `dist`, `target`.
- User logs: files under `~/Library/Logs`.
- Trash: `~/.Trash`, only after confirming nothing important is there.

Treat these as usually safe to clean on Ubuntu/Linux:

- Apt package cache: `sudo apt-get clean` and `sudo apt-get autoclean`.
- Unused distro packages: `sudo apt-get autoremove --purge`, after reviewing the package list.
- Package manager caches: `npm cache clean --force`, `pnpm store prune`, `yarn cache clean`, `pip cache purge`, `uv cache clean`.
- Systemd journal vacuuming by size or time, for example `sudo journalctl --vacuum-time=14d` or `sudo journalctl --vacuum-size=500M`.
- Reinstallable dependencies the user names: `node_modules`, `.venv`, build outputs, `.next`, `dist`, `target`.
- User trash and caches: `~/.local/share/Trash` and `~/.cache`, after checking they are not application state.

Treat these as safe but with workflow impact:

- VS Code/Cursor extensions under `~/.vscode/extensions` and `~/.cursor/extensions`; deleting them uninstalls extensions.
- Xcode DerivedData and simulator caches; deleting them slows the next build or simulator boot.
- Python/uv/pip caches and tool environments; deleting them may require reinstalling tools.
- Agent or editor histories such as `.claude/projects`, `.codex/sessions`, `.cursor/projects`; deleting them may remove local history.
- Large rotated logs under `/var/log`; truncate or rotate named logs rather than deleting active log files.
- Snap, Flatpak, conda, and language runtime caches; deleting them may require redownloading packages or rebuilding environments.

Treat these as high impact:

- Docker Desktop `Docker.raw`: never delete directly. Use Docker prune commands and Docker Desktop compaction/reset behavior.
- Docker volumes: do not run `docker volume prune` unless the user explicitly accepts losing persistent container data. On servers, assume volumes may contain databases, Grafana/InfluxDB state, uploads, or other service data.
- `~/Downloads`, project archives, media, iCloud Drive, Mail, Photos libraries, and app containers: report size and ask.
- APFS local snapshots: report them, but avoid deleting snapshots unless the user explicitly asks and understands the backup/update implications.
- Linux service data under `/var/lib`, `/srv`, `/opt`, `/home/*`, database directories, backups, and container bind mounts: report size and ask before changing.
- Kernel or boot cleanup under `/boot`: prefer package-manager removal of old kernels; do not manually delete kernel files unless recovering from a blocked package manager and the user accepts the risk.

## Remote Linux Example

Treat remote servers as production-like Ubuntu/Linux hosts unless the user says otherwise. In examples, replace `my-server` with the actual hostname or SSH config alias.

1. Start read-only and capture host pressure:

```bash
ssh my-server 'df -h /; df -ih /; uname -a; sudo journalctl --disk-usage 2>/dev/null || true; docker system df 2>/dev/null || true'
```

2. Run the Linux audit script:

```bash
ssh my-server 'PROJECT_SCAN=1 bash -s' < scripts/audit_linux_disk.sh
```

3. For a large root filesystem, inspect one level at a time:

```bash
ssh my-server 'sudo du -xhd 1 / 2>/dev/null | sort -h | tail -30'
ssh my-server 'sudo du -xhd 1 /var 2>/dev/null | sort -h | tail -30'
```

4. Clean low-risk server candidates first when asked:

```bash
ssh my-server 'sudo apt-get clean && sudo apt-get autoclean'
ssh my-server 'sudo journalctl --vacuum-time=14d'
ssh my-server 'docker system prune -af && docker builder prune -af && docker system df'
```

Skip `docker volume prune`, `/var/lib/docker/volumes`, database directories, and application data unless the user explicitly accepts losing or rebuilding that data.

## Scheduled Monitoring

Do not create or edit crontab, launchd jobs, systemd timers, or Codex automations unless the user asks for scheduled monitoring or cleanup. Default scheduled jobs to read-only audit/reporting. Do not schedule destructive cleanup commands such as `rm -rf`, `docker system prune`, `docker volume prune`, `apt-get autoremove`, or journal vacuuming unless the user explicitly accepts the exact command, cadence, and impact.

Before adding a schedule, ask concise questions. If an interactive user-input tool such as `AskUserQuestion` or `request_user_input` is available, use it; otherwise ask in chat:

- Target: local macOS, local Linux, or remote SSH host?
- Mode: read-only audit/report only, or user-approved low-risk cleanup?
- Cadence and output: daily/weekly/monthly, preferred time, log path, and alert threshold?

For Linux servers, prefer a report-only crontab entry with absolute paths and a dedicated log directory:

```bash
mkdir -p "$HOME/.local/state/free-my-disk"
crontab -l > /tmp/free-my-disk.cron 2>/dev/null || true
grep -v 'free-my-disk audit' /tmp/free-my-disk.cron > /tmp/free-my-disk.new
printf '0 8 * * * PROJECT_SCAN=1 /absolute/path/to/audit_linux_disk.sh >> "$HOME/.local/state/free-my-disk/audit.log" 2>&1 # free-my-disk audit\n' >> /tmp/free-my-disk.new
crontab /tmp/free-my-disk.new
rm /tmp/free-my-disk.cron /tmp/free-my-disk.new
```

For macOS, prefer scheduled audit logs with `launchd` only if the user wants persistent local scheduling; otherwise run the audit on demand. For remote hosts, install the schedule on the remote host only after confirming the SSH target and where logs should live.

## Cleanup Workflow

1. State current free space from `df -h /`.
2. Report candidates by tier with sizes and impact.
3. Clean low-risk macOS caches first when asked:

```bash
brew cleanup
npm cache clean --force
pnpm store prune
yarn cache clean
```

4. Remove user-named reinstallable directories with `rm -rf` only after repeating the exact paths.
5. For Docker, start Docker Desktop if needed, then run:

```bash
docker system prune -af
docker builder prune -af
docker system df
```

Skip `docker volume prune -f` unless the user explicitly requests volume deletion.

6. On Ubuntu/Linux, clean low-risk system caches first when asked:

```bash
sudo apt-get clean
sudo apt-get autoclean
sudo apt-get autoremove --purge
sudo journalctl --vacuum-time=14d
npm cache clean --force
pnpm store prune
yarn cache clean
pip cache purge
uv cache clean
```

Review `apt-get autoremove` output before accepting removal if the host is production-like.

7. Recheck:

```bash
df -h /
df -ih /
docker system df 2>/dev/null || true
```

Summarize what was cleaned, what was intentionally skipped, the new free-space number, and any follow-up impact such as reinstalling editor extensions or dependencies.
