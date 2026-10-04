---
name: network-scan
description: Network scanning, port discovery, and reconnaissance.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  rakshastra:
    tags: [security, reconnaissance, network, scanning, port-scan]
    related_skills: [linux-audit, credential-audit]
---

# Network Scanning and Reconnaissance

## Overview
This skill guides the agent in conducting network discovery, port scanning, and service enumeration. Safe and non-destructive mapping of target networks helps establish infrastructure visibility.

## Methodology (9-Phase Sequence)
1. **Recon**: Identify target subnet bounds, host ranges, and active interfaces. Log target assets using `security_inventory`.
2. **Enumeration**: Perform port scans (TCP/UDP) on live hosts to discover active ports, service banners, and protocol versions.
3. **Collection**: Extract network service configuration banners, routing tables, and interface definitions for analysis.
4. **Evidence**: Formally record confirmed active open ports, misconfigured network mappings, or unexpected public exposures as Evidence via `security_evidence`.
5. **Analysis**: Correlate open ports with potential service vulnerabilities (CVEs) and map network paths in the InfrastructureGraph.
6. **Prioritization**: Run `security_risk` to compute composite scores for network exposure based on exposure factors and business criticality.
7. **Recommendation**: Formulate actionable mitigation steps, such as firewall rule updates, port closure commands, or proxy configurations.
8. **Verification**: Re-scan target ports to confirm firewalls/rules have been applied and exposure is closed.
9. **Report**: Document the findings, graph linkages, and verification status in a final security report via `security_report`.

## Commands Reference
Common scanning actions run via terminal:
- `nmap -sn 192.168.1.0/24` (Ping sweep/Host discovery)
- `nmap -sS -sV -O -p- 192.168.1.50` (SYN stealth scan, service/OS detection on all ports)
- `nmap -sU -p 53,67,123,161 192.168.1.50` (UDP scan on common ports)
