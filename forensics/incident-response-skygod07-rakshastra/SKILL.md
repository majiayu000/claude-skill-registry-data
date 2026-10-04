---
name: incident-response
description: Incident response methodology, containment, and investigation.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  rakshastra:
    tags: [security, incident-response, containment, remediation]
    related_skills: [forensics, linux-audit]
---

# Incident Response Playbook

## Overview
This skill guides the agent in handling security incidents, aligning with standard incident handling phases (NIST SP 800-61). Focus on containment, evidence collection, and systematic remediation.

## Methodology (9-Phase Sequence)
1. **Recon**: Identify target systems, user access domains, and active IP networks involved in the incident alert. Register using `security_inventory`.
2. **Enumeration**: Enumerate active network connections, process trees, and logged-in users on affected hosts.
3. **Collection**: Extract command histories, process dumps, auth logs, and web server logs to gather forensic footprints.
4. **Evidence**: Formally record parsed web shell paths, unauthorized user logins, or network beacons as Evidence via `security_evidence`.
5. **Analysis**: Link process connections, user accounts, and target resources to construct attack paths in the InfrastructureGraph.
6. **Prioritization**: Execute `security_risk` to determine threat severity, calculate exploitability metrics, and prioritize containment actions.
7. **Recommendation**: Formulate eradication strategies, such as killing malicious processes, revoking SSH keys, or isolating network targets.
8. **Verification**: Confirm containment and eradication by verifying that malicious network sockets are closed and backdoors are purged.
9. **Report**: Compile full root-cause summaries, incident timeline metrics, and recovery proofs in a report via `security_report`.
