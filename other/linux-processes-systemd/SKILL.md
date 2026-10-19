---
name: linux-processes-systemd
description: >
  Manage Linux processes, write systemd services and timers, inspect journald
  logs, configure resource limits, and debug failing daemon processes. Use when
  creating .service unit files, replacing cron with systemd timers, inspecting
  process states and signals, setting MemoryMax or CPUQuota, or diagnosing systemd crashes.
compatibility: >
  Agent Skills-compatible coding agents administering Linux systems running systemd.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, systemd, services, timers, journald, processes, cgroups, daemons"
  topics: "operating-systems, devtools"
---

# Linux Processes and systemd Service Management

Modern Linux distributions manage processes, background daemons, cron equivalents, and resource constraints through **systemd**. This skill covers writing robust unit files, configuring timers, managing journal logs, enforcing cgroup resource limits, and debugging failed services.

## Core Rules

1. **Always reload daemon configuration after editing unit files**: Run `sudo systemctl daemon-reload` whenever modifying files in `/etc/systemd/system/`.
2. **Never run custom services as root without justification**: Always specify an unprivileged `User=` and `Group=` in the `[Service]` block.
3. **Configure automatic restarts with backoff**: Use `Restart=on-failure` and `RestartSec=5s` to handle transient network or resource hiccups gracefully without entering tight restart loops.
4. **Use systemd timers instead of legacy cron**: Timers provide microsecond accuracy, missed-run catchup (`Persistent=true`), and direct integration with journald logging.
5. **Always verify unit syntax**: Run `systemd-analyze verify <unit-file>` before starting a newly authored service.

---

## 1. Canonical systemd Service Unit

Place custom service files in `/etc/systemd/system/<name>.service`:

```ini
[Unit]
Description=Background Task Worker Service
Documentation=https://docs.example.com/worker
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/app

# Environment configuration
Environment=NODE_ENV=production
EnvironmentFile=-/etc/default/app-worker

# Execution command (must be absolute path)
ExecStart=/opt/app/bin/worker --concurrency=4
ExecReload=/bin/kill -HUP $MAINPID

# Resilience & Restarts
Restart=on-failure
RestartSec=5s
TimeoutStopSec=30s

# Sandboxing and Least Privilege (Hardening)
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/app /tmp
PrivateTmp=true
NoNewPrivileges=true

# Resource Limits (cgroups v2)
MemoryMax=1G
CPUQuota=150%

[Install]
WantedBy=multi-user.target
```

---

## 2. Replacing Cron with systemd Timers

A systemd timer consists of two files: a `.service` file that describes *what* to run, and a matching `.timer` file that describes *when* to run it.

### `backup.service`
```ini
[Unit]
Description=Nightly Database Backup

[Service]
Type=oneshot
User=postgres
ExecStart=/usr/local/bin/backup-database.sh
```

### `backup.timer`
```ini
[Unit]
Description=Run database backup every night at 02:00 UTC

[Timer]
OnCalendar=*-*-* 02:00:00 UTC
# Catch up on missed runs if system was offline/powered down:
Persistent=true
# Random delay to prevent thundering herd in clusters:
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

Enable and start the timer:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer

# List active timers and next trigger times
systemctl list-timers
```

---

## 3. Querying Logs with `journalctl`

Journald stores binary structured logs linked to systemd units and PIDs:

```bash
# View recent logs for a specific service in real-time (follow)
journalctl -u worker.service -f

# View logs from current boot only
journalctl -u worker.service -b

# View error-level logs and above for the service
journalctl -u worker.service -p err..emerg

# View logs within a specific time window
journalctl -u worker.service --since "2026-10-15 14:00:00" --until "2026-10-15 15:00:00"

# Show full metadata (PID, UID, cgroup) for an entry
journalctl -u worker.service -n 1 -o verbose
```

---

## 4. Debugging Failed Services

When `systemctl start <service>` reports a failure:

```bash
# 1. Inspect unit state and exit code
systemctl status <service>

# 2. Inspect kernel and unit logs with error context
journalctl -xeu <service> --no-pager

# 3. Check for syntax errors in unit definition
systemd-analyze verify /etc/systemd/system/<service>.service

# 4. Check if security directives (ProtectSystem, PrivateTmp) block execution
# Run in debug mode if necessary
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Forgetting `systemctl daemon-reload` | Service runs old configuration from disk cache | Always reload daemon after editing unit files |
| Relative paths in `ExecStart` | Service fails to start (`(code=exited, status=203/EXEC)`) | Use absolute paths (`/usr/bin/python3`, `/opt/app/start.sh`) |
| Running services as `root` | Full system compromise if service is breached | Set `User=` and `Group=` to dedicated accounts |
| Missing `Type=oneshot` for scripts | systemd expects persistent daemon and hangs or reports failure | Use `Type=oneshot` for batch scripts/tasks |
| Unbounded memory consumption | OOM killer terminates critical databases or OS daemons | Configure `MemoryMax=` in unit file |

---

## 6. Verification Checklist

- [ ] Unit passes `systemd-analyze verify <unit-file>`.
- [ ] Non-root `User=` and `Group=` specified.
- [ ] `systemctl daemon-reload` executed after edits.
- [ ] Service successfully starts (`systemctl status` shows `active (running)`).
- [ ] Timer appears in `systemctl list-timers` with correct upcoming schedule.
- [ ] Journal logs confirm clean start without permission denied errors.
