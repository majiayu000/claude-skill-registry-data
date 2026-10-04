---
name: compliance-check
description: Compliance auditing and framework validations.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  rakshastra:
    tags: [security, compliance, auditing, standards]
    related_skills: [linux-audit, docker-audit]
---

# Compliance Auditing

## Overview
This skill outlines standard verification checklists to test if systems comply with industry benchmarks (CIS benchmarks, NIST controls, PCI-DSS, etc.).

## Methodology (9-Phase Sequence)
1. **Recon**: Map host systems, operating environments, and regulatory requirements (PCI, CIS, HIPAA). Register using `security_inventory`.
2. **Enumeration**: Enumerate system policies, active audit features, and password expiration configurations.
3. **Collection**: Retrieve system logs configuration, kernel parameters, group policy outputs, or ssh parameters.
4. **Evidence**: Validate and record failed compliance control tests as Evidence via `security_evidence`.
5. **Analysis**: Link failed controls to possible threat vectors in the InfrastructureGraph (e.g. anonymous access mapping).
6. **Prioritization**: Execute `security_risk` to rank failed compliance checkpoints based on composite risk and business context.
7. **Recommendation**: Detail specific system commands, policy settings, or GPO steps to achieve compliance.
8. **Verification**: Run compliance scans or check policy flags again to verify that controls are successfully remediated.
9. **Report**: Compile compliance summaries, checklist statistics, and validation proofs in a report via `security_report`.
