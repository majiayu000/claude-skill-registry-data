---
name: server-ops-lord
description: Lord skill for server administration mastery — SSH hardening, firewalls, reverse proxies + TLS, monitoring, logs, backups/DR, container hosts, self-hosted panels (Coolify/Dokploy/Portainer), Proxmox, Tailscale/WireGuard, troubleshooting, Linux + Windows Server.
triggers:
  - server ops lord
  - server
  - nginx
  - caddy
  - reverse proxy
  - firewall
  - fail2ban
  - hardening
  - server hardening
  - backup
  - restore
  - uptime
  - monitoring server
  - logrotate
  - systemd service
  - docker host
  - coolify
  - dokploy
  - portainer
  - cockpit
  - proxmox
  - tailscale
  - wireguard
  - lets encrypt
  - certbot
  - bare metal
  - dedicated server
  - shared hosting
  - سيرفر
  - خادم
  - استضافة
  - سيرفرات
personas:
  - SRE
  - DEVOPS
  - SEC
  - ARCH
tech_stack:
  - nginx-1
  - caddy-2
  - openssh-10
  - coolify-4
  - proxmox-9
  - tailscale
  - docker-29
lord: true

---

# Server Ops Lord

[SKILL] server-ops-lord
[OBJ] Administer any server (VPS/dedicated/bare-metal/LXC/shared) to production-grade: secure by default, observable, backed up, recoverable. Works the layer BELOW orchestration — the host itself.

[RULES]
1. [REQ] Baseline First — Every new server gets the standard order: create sudo user (never daily-driver root) → SSH keys-only (`PasswordAuthentication no`, `PermitRootLogin no`) → firewall (ufw/nftables, default-deny inbound) → fail2ban/sshd jail → `unattended-upgrades` → timezone+NTP → hostname+FQDN. Never expose an unhardened box.
2. [REQ] SSH Doctrine — Ed25519 keys, per-purpose keypairs; `~/.ssh/config` aliases; agent forwarding OFF by default; prefer Tailscale SSH or WireGuard to close public :22 entirely; keep one bastion pattern for fleets; change-port is cosmetic — real security is keys+MFA+allowlist.
3. [REQ] Firewall — Default deny inbound, allow only service ports; rate-limit SSH; document every open port (file or UFW comment); verify with `ss -tulpn` from the box AND an external scan (nmap from outside).
4. [REQ] Reverse Proxy + TLS — Caddy 2 default for auto-HTTPS/simple sites; nginx for high-control/high-traffic; Traefik when docker-label-driven. TLS via ACME (Let's Encrypt/ZeroSSL); `ssl_ certificates` never manual-copied — automate renewals; redirect 80→443; HSTS after verification; proxy headers (`X-Forwarded-For/Proto`, timeouts, body limits, WebSocket upgrade when needed).
5. [REQ] Storage/Backups — 3-2-1 rule (3 copies, 2 media, 1 off-site); restic/borg encrypted incremental to object storage; TEST restores monthly (`restic restore` drill) — an untested backup is a hope, not a backup; separate DB dumps (`pg_dump`/`mysqldump` consistent snapshots) before file-level copies; exclude caches/logs.
6. [REQ] Monitoring — Minimum: uptime-kuma (external probes) + node_exporter/metrics or netdata (host telemetry) + disk/RAM/CPU alerts; Prometheus+Grafana for fleets; alert on symptoms (error rate, latency, disk>80%, cert expiry <14d) not causes; alert channel that actually reaches a human.
7. [REQ] Logs — journald persistent (`Storage=persistent`), logrotate on every app's logs; never delete logs to "fix" disk space — rotate/vacuum (`journalctl --vacuum-time=7d`); centralize with Loki/Grafana-agent or Vector on fleets.
8. [REQ] Containers on Hosts — docker rootless or daemon with minimal caps; `restart: unless-stopped`; json-file `max-size`/`max-file` log rotation; non-root images; pinned tags; `docker compose` for host-local stacks; Portainer/Dokploy only as UI — never as the source of truth for compose files.
9. [REQ] Panels — Coolify v4 for self-hosted PaaS (git-push deploys, DBs, static sites, remote servers via SSH); Dokploy alternative; Cockpit for host admin GUI. A panel is an accelerator, not a substitute for knowing the primitives underneath.
10. [REQ] Virtualization — Proxmox VE 9 for bare-metal: LXC for service isolation (lighter than VMs), VM only when kernel isolation needed; ZFS or thin-LVM; snapshots before risky ops; PBS (Proxmox Backup Server) for dedup backups; cluster only ≥3 nodes (qdevice otherwise).
11. [REQ] Updates/Upgrades — Patch cadence: security auto + scheduled window for the rest; snapshot/LVM-snapshot before kernel or distro upgrades; reboot windows announced; verify service health post-patch (smoke checklist).
12. [REQ] Troubleshooting Method — Reproduce → isolate layer (network `ping/mtr/ss`, service `systemctl status`/`journalctl -u`, resource `htop/iostat/df -h/du`, kernel `dmesg`) → hypothesis → change ONE variable → verify → document root cause. Never cargo-cult config from forums.
13. [REQ] Secrets/Access — Secrets via env files with 600 perms or a vault — never in compose args, scripts, or git; sudo via `/etc/sudoers.d/` drops with `visudo -f`; least privilege per service account; `auditd` on sensitive boxes.
14. [REQ] Windows Server — OpenSSH Server + PowerShell Remoting over SSH transport; WinRM only where required; winget/Choco for packages; Task Scheduler for cron equivalents; same doctrine (keys, firewall, updates, monitoring agent) applies.
15. [REQ] Shared/Panels Hosting — cPanel/Plesk/DirectAdmin = constrained environment: honor their abstractions (don't fight the panel), use its backup/SSL tooling, note its PHP-FPM/DB quirks; escalate to VPS when limits bite.
16. [REQ] Remote Access — Tailscale/WireGuard mesh for admin-plane; public exposure only for service ports; never RDP/SSH open to the internet; `tailscale serve`/`funnel` for ad-hoc sharing instead of port-forwarding.
17. [REQ] DR & Decommission — Written runbook per server (services, ports, data paths, DNS, dependencies); decommission = snapshot → verify elsewhere → then destroy; keep DNS TTLs low before migrations.
18. [PROHIBIT] Never run a public server without firewall + key-only SSH + fail2ban — bots find :22 within minutes.
19. [PROHIBIT] Never store backups on the same host/disk they protect.
20. [PROHIBIT] Never `chmod 777`, never `docker run --privileged` without justification, never disable SELinux/AppArmor to "fix" denials — write the correct policy.
21. [PROHIBIT] Never apply config you can't explain — every directive must answer "what does this break if removed".
22. [PROHIBIT] Never expose panel/admin ports (Coolify :8000, Portainer :9000, Cockpit :9090, Proxmox :8006) publicly — VPN/allowlist only.
23. [CMD] Context7: `/nginx/nginx`, `/caddyserver/caddy`, `/coollabsio/coolify`, `/tailscale/tailscale`, `/prometheus/prometheus`, `/grafana/grafana` — query before writing configs; flags and directives drift.
24. [CMD] Diagnostics: `ss -tulpn`, `journalctl -u <svc> -f`, `systemctl status`, `df -h`/`du -sh`, `iostat -x 2`, `free -m`, `dmesg -T`, `curl -Iv`, `openssl s_client -connect`, `fail2ban-client status`.
25. [REQ] Handoff Evidence — Every server task ends with: open-ports list, service map, backup+restore proof, monitoring dashboards link, and the runbook updated.

[WORKFLOWS]
1. New VPS to production — provision → baseline (user/SSH/ufw/fail2ban/updates) → Tailscale admin-plane → reverse proxy + TLS → app deploy → monitoring+alerts → backup job → restore drill → runbook.
2. Service down incident — external probe confirms → host checks (load/disk/mem) → `journalctl -u` errors → recent change correlation → fix or rollback → postmortem note in runbook.
3. Migrate a service between servers — lower DNS TTL → provision target → replicate data (rsync/backup-restore) → cutover proxy or DNS → soak period → decommission old with snapshot.
4. Hardening audit — `ss -tulpn` inventory vs expected → sshd_config review → updates pending → backup proof → panel exposure check → report + fix list.
