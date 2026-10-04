---
name: windows-audit
description: Windows host and Active Directory security auditing.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [windows]
metadata:
  rakshastra:
    tags: [security, windows, auditing, active-directory, hardening]
    related_skills: [compliance-check, credential-audit]
---

# Windows Security Auditing

## Overview
This skill provides guidance on auditing Windows hosts and Active Directory configurations to discover weak system controls, local privilege escalation routes, and credential exposure.

## Methodology (9-Phase Sequence)
1. **Recon**: Identify target Windows domain controllers, domain bounds, and host systems. Log them using `security_inventory`.
2. **Enumeration**: Query local admin groups, Active Directory members, password policies, and domain trusts.
3. **Collection**: Retrieve registry settings, auto-run paths, service paths, Defender configurations, and event logs.
4. **Evidence**: Validate and record unquoted service paths, disabled firewall profiles, or weak group permissions as Evidence via `security_evidence`.
5. **Analysis**: Correlate OS version patch levels with missing KBs (CVEs) and map Windows Active Directory relationships in the InfrastructureGraph.
6. **Prioritization**: Execute `security_risk` to compute Windows/AD vulnerability scores against business asset criticality.
7. **Recommendation**: Detail mitigation registry edits, group policy changes, service path quotes, or user privileges.
8. **Verification**: Query registry keys or run PowerShell validation to confirm defender/firewall features or quote paths are corrected.
9. **Report**: Compile Windows audit details, Active Directory trees, and verification status in a report via `security_report`.

## Commands Reference
- `net localgroup administrators` (Check local admins)
- `Get-MpComputerStatus` (PowerShell: Check Defender status)
- `Get-NetFirewallProfile` (PowerShell: Check Firewall status)
- `wmic service get name,displayname,pathname,startmode | findstr /i "auto"` (Check auto-start services)
