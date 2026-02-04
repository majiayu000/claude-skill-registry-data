---
name: configure-ubuntu
description: Ubuntu server configuration via cloud-init and systemd. Use when writing cloud-init YAML, configuring systemd services, setting up nginx, or troubleshooting VM configuration issues.
---

# Configure Ubuntu Skill

## Purpose

This skill provides guidance for configuring Ubuntu LTS servers via cloud-init automation for any cloud platform (AWS, Azure, GCP, DigitalOcean, etc.).

> **Note:** All examples in this skill currently use **Ubuntu 24.04 LTS**. Update version-specific package names or paths as needed for other LTS releases.

## When to Use This Skill

Use this skill when:
- Writing cloud-init YAML for VM provisioning
- Configuring systemd services
- Setting up nginx reverse proxies
- Troubleshooting cloud-init or systemd issues
- Setting file permissions for service users

## Reference Selection Guide

Choose the appropriate reference based on your task:

| Task | Reference File |
|------|----------------|
| Complete cloud-init configurations | `references/examples/*.yaml` |
| Cloud-init syntax and patterns | `references/cloud-init-patterns.md` |
| systemd service units | `references/systemd-patterns.md` |
| Debugging failures or errors | `references/common-pitfalls.md` |

### Ready-to-Use Examples

| Example | File |
|---------|------|
| SSH bastion host | `references/examples/bastion.yaml` |
| Nginx reverse proxy (HTTP) | `references/examples/proxy-http.yaml` **← default** |
| Nginx reverse proxy (HTTPS, self-signed) | `references/examples/proxy-https.yaml` |
| Nginx reverse proxy (HTTPS, Let's Encrypt) | `references/examples/proxy-https-letsencrypt.yaml` |
| Nginx static file server | `references/examples/static-files.yaml` |
| Python/Flask server | `references/examples/flask.yaml` |
| Node.js server | `references/examples/nodejs.yaml` |
| Java/Spring Boot server | `references/examples/java.yaml` |
| .NET server | `references/examples/dotnet.yaml` |

> **HTTPS Options:**
> - Use `proxy-http.yaml` by default (no SSL)
> - Use `proxy-https.yaml` for self-signed certificates (development/internal)
> - Use `proxy-https-letsencrypt.yaml` for trusted certificates (requires domain name)

### When to Read Multiple References

- **New VM setup:** Start with relevant example, then cloud-init-patterns.md for customization
- **Service won't start:** common-pitfalls.md + systemd-patterns.md
- **SSH access broken:** common-pitfalls.md (Issue #1)
- **Permission denied errors:** common-pitfalls.md (Issues #4, #5, #6)
- **Scheduled tasks:** systemd-patterns.md (Systemd Timers section)
- **Production HTTPS:** proxy-https-letsencrypt.yaml (requires domain name)
- **Static website:** static-files.yaml + proxy-http.yaml (if reverse proxy needed)

---

## Critical Rules (Memorize These)

These rules prevent the most common failures:

1. **NEVER use `users:` directive in cloud-init** — Deletes default SSH user, breaks access
2. **Systemd: NO inline comments** — `After=network.target # comment` fails
3. **Permissions as quoted strings** — Use `'0640'` not `0640` in cloud-init
4. **Wait for cloud-init** — Takes 2-3 minutes; don't deploy until done
5. **Absolute paths in systemd** — Use `/opt/app/venv/bin/python` not `python`
6. **Fix permissions after SCP** — Files copied retain local permissions

---

## Default Choices for Vague Requests

When the request is ambiguous, use these defaults:

| Decision | Default Choice | Rationale |
|----------|----------------|-----------|
| **Application framework** | Flask/Python | Course standard, most examples |
| **Reverse proxy** | HTTP (not HTTPS) | Simpler, use `proxy-http.yaml` |
| **Application port** | 5001 | Avoids conflict with common ports |
| **Proxy port** | 80 (HTTP) or 443 (HTTPS) | Standard web ports |
| **App directory** | `/opt/<app-name>/` | Standard for third-party apps |
| **Config directory** | `/etc/<app-name>/` | Standard for system config |
| **Service user** | `<app-name>` | Same as app, no login shell |
| **Ownership pattern** | `deployuser:servicegroup` | Deploy user writes, service reads |
| **Directory permissions** | 775 | Group can write (venv installs) |
| **Config file permissions** | 640 | Owner writes, group reads |
| **WSGI server** | Gunicorn | Production-ready, simple config |

### Example Defaults

**"Set up a web application server"** → Use:
- `examples/flask.yaml` for application VM
- `examples/proxy-http.yaml` for proxy VM
- Port 5001 for Flask, port 80 for nginx

**"Configure nginx"** → Use:
- `examples/proxy-http.yaml` (reverse proxy, not static files)
- Unless HTTPS explicitly requested, then `proxy-https.yaml`

**"Set up a secure bastion"** → Use:
- `examples/bastion.yaml` (includes UFW + fail2ban)

---

## Environment Variables Pattern

**This is the standard way to handle environment variables (database credentials, API keys, connection strings) on the server.**

### Directory Structure

```
/etc/<app-name>/
└── environment      # All environment variables for the application
```

### Setup in Cloud-init

```yaml
runcmd:
  # Create config directory owned by root, readable by app group
  - mkdir -p /etc/myapp
  - chown root:myapp /etc/myapp
  - chmod 750 /etc/myapp

  # Create environment file with restricted permissions
  - touch /etc/myapp/environment
  - chown root:myapp /etc/myapp/environment
  - chmod 640 /etc/myapp/environment
```

### Reference from systemd

```ini
[Service]
EnvironmentFile=/etc/myapp/environment
```

### Environment File Format

```bash
# /etc/myapp/environment
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
API_KEY=external-service-api-key
DEBUG=false
```

### Why This Pattern?

| Concern | Solution |
|---------|----------|
| **Security** | File owned by `root`, only readable by app group (mode `640`) |
| **Separation** | Config in `/etc/`, code in `/opt/` — different concerns, different locations |
| **Deployment** | Environment file can be updated without redeploying code |
| **systemd integration** | `EnvironmentFile=` loads variables automatically |

---

## Quick Reference Tables

### Default SSH Users by Cloud Provider

| Provider | Default User |
|----------|--------------|
| AWS (Amazon Linux) | `ec2-user` |
| AWS (Ubuntu) | `ubuntu` |
| Azure | `azureuser` |
| GCP | Your Google account username |
| DigitalOcean | `root` |
| Linode | `root` |

### File Permission Patterns

| Purpose | Owner:Group | Mode |
|---------|-------------|------|
| Application code | deployuser:appgroup | 640 |
| Application directory | deployuser:appgroup | 775 |
| Config with secrets | root:appgroup | 640 |
| Config directory | root:appgroup | 750 |
| systemd service files | root:root | 644 |

### Common systemctl Commands

```bash
sudo systemctl daemon-reload    # After editing service files
sudo systemctl enable myapp     # Start on boot
sudo systemctl start myapp      # Start now
sudo systemctl status myapp     # Check status
sudo journalctl -u myapp -f     # Follow logs
```

### Cloud-init Verification

```bash
cloud-init status               # Check status
cloud-init status --wait        # Block until complete
sudo cat /var/log/cloud-init-output.log  # View logs
```

---

## Reference Summaries

### examples/ directory

Ready-to-use cloud-init YAML files for common server types. Copy and customize for your use case.

### cloud-init-patterns.md

Reference documentation for cloud-init syntax:
- Module execution order
- Package management (`packages`, `package_update`)
- Writing configuration files (`write_files`)
- Running commands (`runcmd`)
- Debugging and lifecycle

### systemd-patterns.md

Reference documentation for systemd services:
- Service unit file structure (`[Unit]`, `[Service]`, `[Install]`)
- Service types (`simple`, `forking`, `oneshot`)
- Environment configuration
- Restart policies and resource limits
- **Systemd timers** (scheduled tasks, replacement for cron)
- Managing and debugging services

### common-pitfalls.md

Prevention checklist and solutions for:
- Cloud-init issues (user deletion, timing)
- systemd issues (inline comments, permissions)
- File permission problems
- SSH and networking issues
