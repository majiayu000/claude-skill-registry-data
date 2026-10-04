---
name: VPS
description: Provision, secure, and manage virtual private servers with practical hosting guidance.
metadata: {"clawdbot":{"emoji":"🖧","os":["linux","darwin","win32"]}}
---

# VPS Management Rules

## Choosing a VPS
- Match location to users — latency matters more than raw specs for user-facing apps
- ARM instances cost 20-40% less with equivalent performance for most workloads — check compatibility first
- Shared vCPU is fine for most apps — dedicated CPU only for sustained compute-heavy workloads
- Bandwidth overage fees can exceed server cost — check limits before choosing plan

## Initial Setup Priority
- Update system packages immediately after first boot — fresh images are often months behind on security patches
- Create non-root user with sudo before disabling root — locking yourself out requires provider console access
- SSH key authentication before disabling password login — test the key works first
- Firewall rules before exposing services — default is often all ports open

## SSH Hardening
- Change SSH port from 22 — reduces automated scanning noise by 99%
- Disable root login via SSH — force sudo for audit trail
- Disable password authentication — keys only, no exceptions
- Install fail2ban — bans IPs after failed attempts, essential for any public server

## Firewall Basics
- Default deny incoming, allow outgoing — only open what you need
- Allow SSH (your custom port) before enabling firewall — or you're locked out
- HTTP/HTTPS (80/443) only if running web services
- Keep firewall rules minimal — every open port is attack surface

## Resource Management
- Enable swap even with enough RAM — prevents OOM kills during traffic spikes
- Monitor disk usage — logs and Docker images fill disks silently
- Set up basic monitoring (uptime, disk, memory) — know when things break before users tell you
- Reboot periodically to apply kernel updates — unattended-upgrades doesn't cover everything

## Backups and Snapshots
- Provider snapshots are not backups — they're tied to the provider, not portable
- Test restore process before you need it — untested backups are wishful thinking
- Automate backups — manual backups get forgotten
- Keep at least one backup offsite — provider outages take everything with them

## Networking
- Static IP is usually default — but verify before relying on it for DNS
- IPv6 is free and increasingly expected — enable it unless you have specific reasons not to
- Private networking between VPS instances avoids public internet for internal traffic
- Document your IP addresses — easy to lose track with multiple servers

## Cost Awareness
- Stopped instances still cost money for storage — delete unused servers
- Reserved instances save 30-50% for long-term use — commit if you're sure
- Bandwidth is often the surprise cost — especially for media-heavy apps
- Multiple small VPS often beats one large one — isolation and redundancy

## Provider-Specific
- Hetzner, DigitalOcean, Linode, Vultr all work similarly — skills transfer between them
- Provider firewalls (security groups) act before OS firewall — configure both
- Provider console access works when SSH is broken — know how to access it
- Some providers charge for IPv4 addresses separately — check before assuming you have one

## Common Mistakes
- Not updating for months — security vulnerabilities accumulate
- Running everything as root — no audit trail, maximum blast radius
- No firewall because "nobody knows my IP" — scanners find everything
- Oversizing from day one — start small, scale when needed
- Ignoring provider status pages — outages explain mysterious issues
