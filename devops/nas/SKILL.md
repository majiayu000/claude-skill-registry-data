---
name: NAS
slug: nas
version: 1.0.0
description: Configure, secure, and optimize network attached storage with proper backup strategy, remote access, and media serving.
homepage: https://clawic.com/skills/nas
metadata:
  clawdbot:
    emoji: 🗄️
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    displayName: NAS
---

## Quick Reference

| Topic | File |
|-------|------|
| Backup strategy, 3-2-1 rule | `backup.md` |
| Remote access, VPN, security | `security.md` |
| Docker, home lab, apps | `apps.md` |
| Media server, indexing | `media.md` |

## Scope

This skill covers NAS administration for Synology, QNAP, TrueNAS, Unraid, and DIY builds. For enterprise SAN/distributed storage, use specialized infrastructure skills.

## Critical Rules

1. **RAID is not backup** — RAID protects against drive failure, not ransomware, fire, or accidental deletion. Always maintain off-site backup.

2. **3-2-1 backup rule is minimum** — Three copies, two different media types, one off-site. Cloud sync to B2/S3/Glacier counts as off-site.

3. **SMB for Windows/Mac, NFS for Linux** — Wrong protocol = permission chaos. AFP deprecated. Enable only protocols you actually use.

4. **Expose ZERO ports to internet** — No DSM/QTS admin on public IP. Use VPN (WireGuard/Tailscale) or reverse proxy with auth.

5. **Test your backups quarterly** — Untested backup is not a backup. Actually restore files to verify integrity.

6. **Disable admin account** — Create named admin accounts. Default "admin" is first target for brute force.

7. **UPS mandatory** — Power loss during write = corrupted pool. Budget for battery backup that signals clean shutdown.

8. **Snapshots are not backup** — Same disks, same failure domain. Snapshots help with accidental delete, not disaster.

9. **Calculate TRUE storage capacity** — RAID overhead, reserved space, filesystem overhead. 4x8TB drives ≠ 32TB usable.

10. **ARM NAS = limited Docker** — Synology J-series, low-end QNAP run ARM. Many Docker images x86 only. Verify before buying.
