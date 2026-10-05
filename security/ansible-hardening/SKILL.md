---
name: ansible-hardening
description: >
  Codify security hardening into reusable Ansible roles — CrowdSec IDS, fail2ban,
  auditd, Tailscale VPN, Semaphore UI, scoped sudoers, systemd sandboxing, and
  UFW firewall management. Trigger on: "harden with Ansible", "Ansible security",
  "CrowdSec role", "fail2ban role", "auditd role", "Tailscale Ansible", "Semaphore
  role", "sudoers role", "security playbook", "fleet hardening", or any request
  to automate security configurations that were done manually.
---

# Ansible Hardening

Codify manual security work into idempotent Ansible roles. Every hardening step
performed by hand should eventually become a role in this collection.

## Roles Needed (from manual work done 2026-03-21)

### crowdsec
Installs CrowdSec agent + firewall bouncer, configures collections, whitelists LAN.
```yaml
# defaults
crowdsec_lapi_port: 8088          # moved from 8080 for OpenShell
crowdsec_collections:
  - crowdsecurity/sshd
  - crowdsecurity/linux
crowdsec_whitelist_cidrs:
  - "{{ lan_subnet }}"
```

### fail2ban
Installs fail2ban, configures SSH jail.
```yaml
# defaults
fail2ban_maxretry: 3
fail2ban_bantime: 3600
fail2ban_findtime: 600
```

### auditd
Installs auditd, deploys audit rules for sensitive files.
```yaml
# defaults
auditd_watch_paths:
  - { path: /etc/sudoers, key: sudoers_changes }
  - { path: /etc/sudoers.d/, key: sudoers_changes }
  - { path: /etc/ssh/sshd_config, key: ssh_config }
  - { path: /etc/monero/, key: monero_config }
```

### tailscale
Installs Tailscale, configures serve endpoints.
```yaml
# defaults
tailscale_serve_ports: []         # list of {local_port, description}
tailscale_funnel: false           # never enable funnel by default
```
Note: `tailscale up` requires interactive auth — role should detect and prompt.

### semaphore
Installs Semaphore binary, creates config + systemd unit.
```yaml
# defaults
semaphore_version: "2.17.27"
semaphore_port: 3001
semaphore_bind: "127.0.0.1"
semaphore_db: bolt                # bolt or postgres
```

### sudoers-scope
Replaces blanket NOPASSWD with scoped command list.
```yaml
# defaults
sudoers_nopasswd_commands:
  - /usr/bin/systemctl
  - /usr/bin/journalctl
  - /usr/bin/apt
  - /usr/bin/apt-get
  # ... full list from /etc/sudoers.d/admin_user
```

## Implementation Pattern

Each role follows monero-farm conventions:
- `defaults/main.yml` — all variables with safe defaults
- `tasks/main.yml` — idempotent tasks
- `handlers/main.yml` — restart/reload handlers
- `templates/` — config file templates (Jinja2)

## Rules

- Always `--check --diff` before real runs
- Never remove existing security controls — only add/tighten
- Whitelist LAN subnet before enabling firewall bouncers
- Tailscale auth is interactive — can't be fully automated
- Test on a primary host first, then roll to fleet

## Where To Build

These roles belong in your project's `ansible/roles/` directory alongside existing
roles (base, application-specific, monitoring). The security roles extend
the base role's hardening.

Alternatively, create a standalone `ansible-hardening` collection at
`<your-repo-root>/ansible-hardening/` if the scope grows and needs to be reused
across multiple projects.
