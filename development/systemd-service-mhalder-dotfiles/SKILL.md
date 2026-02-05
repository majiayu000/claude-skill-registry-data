---
name: systemd-service
description: Create and debug systemd service unit files. Use when the user says "create a service", "systemd unit", "service won't start", "enable on boot", "systemctl", or asks about running apps as services.
allowed-tools: Bash, Read, Write, Edit
---

# Systemd Service

Create and troubleshoot systemd service unit files.

## Instructions

When creating:
1. Understand the application requirements
2. Determine service type (simple, forking, oneshot)
3. Write unit file with proper dependencies
4. Install and enable the service

When debugging:
1. Check service status: `systemctl status <service>`
2. Check logs: `journalctl -u <service>`
3. Verify unit file syntax: `systemd-analyze verify`
4. Identify and fix issues

## Unit file template

```ini
[Unit]
Description=My Application Service
Documentation=https://example.com/docs
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/myapp
Environment=NODE_ENV=production
ExecStart=/usr/bin/node /opt/myapp/server.js
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/opt/myapp/data

[Install]
WantedBy=multi-user.target
```

## Service types

| Type | Use when |
|------|----------|
| simple | Process stays in foreground (default) |
| forking | Process forks and parent exits (legacy daemons) |
| oneshot | Process exits after doing work (scripts) |
| notify | Process signals ready via sd_notify |

## Debug commands

```bash
# Status and logs
systemctl status myapp
journalctl -u myapp -f
journalctl -u myapp --since "10 min ago"

# Reload after editing unit file
systemctl daemon-reload

# Verify syntax
systemd-analyze verify /etc/systemd/system/myapp.service

# Show dependencies
systemctl list-dependencies myapp
```

## Common issues

| Problem | Check | Solution |
|---------|-------|----------|
| Permission denied | User/Group settings | Create user, set ownership |
| Executable not found | ExecStart path | Use absolute paths |
| Fails immediately | Type setting | Match Type to app behavior |
| Doesn't start on boot | Install section | `systemctl enable` |

## Rules

- MUST use absolute paths in ExecStart
- MUST set appropriate User/Group (never root for apps)
- MUST include restart policy for production services
- Always include security hardening directives
- Always verify syntax before enabling
- Never run application services as root
