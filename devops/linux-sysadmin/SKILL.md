---
name: linux-sysadmin
description: "This skill provides expert Linux system administration for Ubuntu 24.04 production servers with Angie (Nginx fork), PM2, PostgreSQL 16, Redis 7, Docker, UFW, and Yandex Cloud/Yandex Console operational tasks. Activate proactively
  whenever the user mentions: server health, nginx, angie, reverse proxy, SSL, certificates, ACME, ports, firewall, ufw, backup, disk space, memory, CPU, processes, pm2, docker, postgres, redis, logs,
  security, updates, cron, systemd, domain setup, Yandex Cloud, Yandex Console, yc CLI, cloud networking, IAM, quotas, managed services, or any server management task. Also activate when troubleshooting: site down, slow server, connection refused, disk full, OOM, service crash."
stacks:
  - sysadmin
tags:
  - sysadmin
  - linux
  - devops
category: devops
color: green
displayName: Linux SysAdmin
---

# Linux SysAdmin

## Use this skill when

- Managing Ubuntu 24.04 production servers
- Configuring or troubleshooting Angie (Nginx fork) as a reverse proxy
- Managing SSL/TLS certificates via Certbot or Angie's built-in ACME
- Configuring UFW firewall rules
- Managing services via PM2 (Node.js apps) or systemd
- Diagnosing: site down, slow server, disk full, OOM, connection refused, service crash
- Managing PostgreSQL 17, Redis 7, or Docker on the server
- Setting up backups, cron jobs, or log rotation
- Working with Yandex Cloud, Yandex Console, `yc` CLI, IAM, cloud networking, quotas, billing, or managed services as part of server operations

## Do not use this skill when

- The target OS is not Ubuntu/Debian Linux
- The task is purely about application code — use the appropriate app skill
- Infrastructure is managed by Kubernetes or cloud-managed services (ECS, GKE)

## Instructions

1. Check service status before making changes (`systemctl status`, `pm2 status`, `docker ps`).
2. Back up config before editing: `cp file file.bak.$(date +%s)`.
3. Test config before applying: `angie -t`, `docker compose config`.
4. Apply changes and verify: check status, curl endpoint, tail logs.
5. Document the rollback path.

## Yandex Cloud And Console

`yandex-cloud-docs` is a sysadmin-only companion skill. When the task involves Yandex Cloud, Yandex Console, `yc` CLI, IAM roles, cloud networking, quotas, billing, managed databases, Object Storage, Compute Cloud, or Yandex Cloud documentation:

1. Explicitly invoke `$yandex-cloud-docs` before giving current Yandex Cloud instructions or changing cloud-facing configuration.
2. Use official Yandex Cloud docs/MCP evidence for current behavior, limits, roles, CLI flags, and Console paths.
3. Do not let non-sysadmin agents load `yandex-cloud-docs`; route Yandex Cloud operational questions through Linux SysAdmin/sysadmin context.
4. Keep secrets out of prompts, logs, screenshots, and summaries. Never expose service account keys, OAuth tokens, IAM tokens, billing IDs, or private resource IDs.

## Safety Rules

These are non-negotiable. Violating them risks downtime or data loss.

1. **Test before reload**: `angie -t` before `systemctl reload angie` — always
2. **Backup before edit**: `cp file file.bak.$(date +%s)` for any config in `/etc/`
3. **Confirm destructive ops**: deleting files, dropping databases, resetting firewall — ask first
4. **Verify after changes**: check service status, curl endpoint, tail logs
5. **Document rollback**: every change must have a "how to undo" note
6. **Reload over restart**: `systemctl reload` preserves connections; `restart` drops them

## Server Stack

| Component | Version | Config | Service |
|-----------|---------|--------|---------|
| **Angie** | 1.11.3 | `/etc/angie/` | `angie.service` |
| **PostgreSQL** | 17 | `/etc/postgresql/17/main/` | `postgresql.service` |
| **Redis** | 7 | `/etc/redis/redis.conf` | `redis-server.service` |
| **PM2** | latest | `ecosystem.config.js` per project | `pm2-ubuntu.service` |
| **Docker** | latest | `/etc/docker/daemon.json` | `docker.service` |
| **UFW** | active | `/etc/ufw/` | ports 2222/80/443 |
| **SSH** | port 2222 | `/etc/ssh/sshd_config` | `sshd.service` |
| **Certbot** | latest | `/etc/letsencrypt/` | `certbot.timer` |

## Diagnostic Playbook

When something is wrong, follow this escalation path top-down:

1. Service running? → `systemctl status SVC` / `pm2 status` / `docker ps`
2. Port listening? → `ss -tlnp | grep :PORT`
3. Logs say what? → `journalctl -u SVC -n 50` / `pm2 logs APP` / `docker logs CTR`
4. Resources OK? → `free -h` / `df -h` / `top -bn1 | head -20`
5. Network OK? → `curl -I localhost:PORT` / `ufw status`
6. Dependencies OK? → `pg_isready` / `redis-cli ping`
7. Config valid? → `angie -t` / `docker compose config`
8. Permissions OK? → `ls -la` / `namei -l PATH`

### Common Scenarios

**Site is down**: check HTTP code with curl → verify Angie is running → check port 443 listening → verify app (PM2 or Docker) is running → check Angie error log → check upstream errors.

**Server is slow**: check load average vs CPU count → check memory pressure and swap usage → check disk full → identify CPU hog with top → check I/O with iostat → check PostgreSQL long-running queries in `pg_stat_activity`.

**Disk full**: identify which mount is full with `df -h` → find biggest directories with `du -xsh /* | sort -rh` → check log sizes → check Docker disk usage with `docker system df` → check journal size → clean up with `journalctl --vacuum-time=7d`.

**Can't SSH**: check UFW rules for port 2222 → verify sshd is listening → check if IP is banned by fail2ban → verify `~/.ssh/authorized_keys` permissions (700/600).

## Angie (Web Server)

Angie is a Russian fork of Nginx by ex-Nginx developers. Config syntax is 100% Nginx-compatible. Binary: `angie`. Unique features: built-in ACME, REST API, HTTP/3, Prometheus metrics.

Key commands: `angie -t` (test config), `systemctl reload angie` (apply changes gracefully), `systemctl status angie`, `ls /etc/angie/sites-enabled/`, `tail -50 /var/log/angie/error.log`.

For detailed Angie configuration, ACME setup, API endpoints, and templates: read `references/angie.md`.

## Service Management

- **systemd**: `systemctl start|stop|restart|reload|status SERVICE` / `journalctl -u SERVICE -n 100`
- **PM2**: `pm2 status` / `pm2 logs APP` / `pm2 reload APP` (zero-downtime) / `pm2 save`
- **Docker**: `docker ps` / `docker logs --tail 100 CTR` / `docker compose up -d` / `docker system df`

For detailed service management, PostgreSQL, and Redis: read `references/services.md`.

## SSL/TLS

Two approaches on this server:

**Certbot (current setup)**: `certbot certonly --webroot` for initial cert, `certbot renew --dry-run` to test auto-renewal, `systemctl status certbot.timer` to verify the timer is active.

**Angie built-in ACME (recommended migration)**: Angie obtains and renews Let's Encrypt certificates automatically — no Certbot needed. Uses `acme_client` + `acme` directives and `$acme_cert_*` variables instead of file paths. Full ACME guide in `references/angie.md`.

## Firewall (UFW)

Default policy: deny incoming, allow outgoing. Only ports 2222/80/443 are open.

Key operations: view rules (`ufw status verbose` / `ufw status numbered`), open port (`ufw allow 80/tcp`), rate-limit SSH (`ufw limit 2222/tcp`), restrict to IP (`ufw allow from IP to any port 2222`), delete rule by number (`ufw delete RULE_NUMBER`).

## Security Essentials

Quick checks: `grep "PermitRootLogin\|PasswordAuthentication" /etc/ssh/sshd_config` / `ufw status verbose` / `fail2ban-client status sshd` / count pending security updates.

For full security hardening checklist, SSH config, fail2ban, kernel sysctl: read `references/security.md`.

## Backup Quick Reference

- **PostgreSQL**: `pg_dumpall -U postgres | gzip` to dated file in `/var/backups/postgresql/`
- **Redis**: `redis-cli BGSAVE` then copy `dump.rdb` to `/var/backups/redis/`
- **Configs**: tar `/etc/angie/`, `/etc/postgresql/`, `/etc/redis/`, `/etc/ssh/sshd_config`, `/etc/letsencrypt/`
- **Cleanup**: `find /var/backups -type f -mtime +14 -name "*.gz" -delete`

## Log Locations

| Log | Path |
|-----|------|
| System | `/var/log/syslog` |
| SSH/sudo | `/var/log/auth.log` |
| Web access | `/var/log/angie/access.log` |
| Web errors | `/var/log/angie/error.log` |
| Database | `/var/log/postgresql/*.log` |
| Firewall | `/var/log/ufw.log` |
| Intrusion | `/var/log/fail2ban.log` |
| Node.js apps | `~/.pm2/logs/` |

## Health Score

Start at 100, deduct per issue found:

| Severity | Deduction | Examples |
|----------|-----------|---------|
| Critical | -20 | Service down, disk >95%, SSL expired, breach |
| Major | -10 | Resource >80%, cert <7d, frequent errors |
| Minor | -5 | Warnings, non-critical log errors |
| Info | -2 | Outdated packages, cleanup needed |

Score ranges: 90–100 Excellent / 70–89 Good / 50–69 Fair / 30–49 Poor / below 30 Critical.

## Output Format

Always return structured results with three sections:

- **Status** line: `OK`, `WARNING`, or `CRITICAL`
- **What was done**: bulleted list of actions taken
- **Current state**: output of the verification command (service status, curl response, etc.)
- **Rollback**: how to undo the change if needed

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.

## References

- [references/angie.md](references/angie.md)
- [references/services.md](references/services.md)
- [references/security.md](references/security.md)
