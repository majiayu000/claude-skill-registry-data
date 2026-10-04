---
name: linux-audit
description: Linux host security auditing and hardening assessment.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [linux]
metadata:
  rakshastra:
    tags: [security, linux, auditing, hardening, compliance]
    related_skills: [network-scan, compliance-check]
---

# Linux Host Security Auditing and Hardening

## Overview
This skill guides the security audit of Linux hosts, identifying unauthorized access points, outdated services, loose file permissions, and misconfigured system controls.

## Methodology (9-Phase Sequence)
1. **Recon**: Map host environment details, distribution, architecture, and network parameters. Log the host using `security_inventory`.
2. **Enumeration**: List listening TCP/UDP ports, active running processes, and mounted filesystems.
3. **Collection**: Extract `/etc/passwd`, SUID/SGID file lists, SSH config (`/etc/ssh/sshd_config`), and `/etc/fstab`.
4. **Evidence**: Validate and record insecure file permissions, exposed SUID binaries, or raw ssh access as Evidence via `security_evidence`.
5. **Analysis**: Correlate OS/kernel versions with known CVEs. Map local dependencies and access points in the InfrastructureGraph.
6. **Prioritization**: Execute `security_risk` to grade privilege escalation and service exposure risks against host business criticality.
7. **Recommendation**: Outline specific commands to remediate risks, e.g. chmod commands, ssh config replacements, sysctl configurations.
8. **Verification**: Execute `ss`, check permissions, or query ssh configurations to verify the patch is active.
9. **Report**: Format hardening results, graph connections, and verification results in a final report via `security_report`.

## Commands Reference
- `ss -tulpn` (List active listening ports with processes)
- `find / -perm -4000 -type f 2>/dev/null` (Find SUID files)
- `find / -perm -o+w -type f 2>/dev/null` (Find world-writable files)
- `systemctl list-units --type=service --state=running` (List active services)
- `sestatus` or `apparmor_status` (Check MAC enforcement status)
