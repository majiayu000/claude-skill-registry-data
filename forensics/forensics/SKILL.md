---
name: forensics
description: Digital forensics, log analysis, and system artifact examination.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  rakshastra:
    tags: [security, forensics, logs, timeline, incident-response]
    related_skills: [incident-response, linux-audit]
---

# Digital Forensics and Log Analysis

## Overview
This skill covers procedures for investigating post-incident systems, checking system logs, tracking execution timelines, and locating malicious persistence files.

## Methodology (9-Phase Sequence)
1. **Recon**: Map host hardware details, operating systems, and target partition metrics. Log using `security_inventory`.
2. **Enumeration**: Enumerate process maps, logged-in sessions, open network sockets, and shared system mounts.
3. **Collection**: Capture log files, memory images, registry hives, shell histories, and system files.
4. **Evidence**: Validate file hashes, log trace entries, or persistence structures as Evidence via `security_evidence`.
5. **Analysis**: Correlate timestamps, reconstruct attack timelines, and trace lateral movements in the InfrastructureGraph.
6. **Prioritization**: Execute `security_risk` to rank identified backdoors, shells, or exposures by severity.
7. **Recommendation**: Write playbooks to quarantine files, remove registry entries, rotate keys, and block threat IPs.
8. **Verification**: Verify that system persistence folders (cron/autoruns) are clean and hashes match baseline states.
9. **Report**: Format the chain of custody, timeline analysis, and forensic findings in a report via `security_report`.
