---
name: status
description: 'Show restic backup health — timer state, latest snapshot, freshness, recent log Arguments: [--log-lines <n>].'
---

# restic Backup Status

Answer "are my backups healthy?" at a glance. Read-only.

Parse `[--log-lines <n>]` (default 20) from "$ARGUMENTS".

## Process

1. **Schedule** — is the timer active and when does it run next?
   ```bash
   systemctl list-timers 'restic-*' --no-pager 2>/dev/null \
     || (echo "no systemd timers — checking cron:"; ls -l /etc/cron.d/restic-backup 2>/dev/null)
   ```

2. **Latest snapshot + freshness:**
   ```bash
   set -a; . /root/.restic/r2.env; set +a
   restic snapshots --latest 1
   restic snapshots --json --latest 1   # age = newest `time` across ALL returned groups (one per host/path); warn if > 26h old
   ```

3. **Last run log:**
   ```bash
   tail -n <log-lines> /var/log/restic-backup.log 2>/dev/null
   journalctl -u restic-backup.service -n <log-lines> --no-pager 2>/dev/null
   ```

4. **Report**: timer next-run, newest snapshot time + age (flag if stale), and whether the last run ended cleanly. If anything looks wrong, point to the `troubleshoot` skill.

Do not modify anything — this command only reads. For deeper diagnosis use the `troubleshoot` skill; to run a backup now use `/restic-dev:backup-now`.