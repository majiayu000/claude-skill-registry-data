---
name: credential-audit
description: Auditing secret leakage, password policies, and credential exposure.
version: 1.1.0
author: Rakshastra Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  rakshastra:
    tags: [security, credentials, secrets, password-policy, scanning]
    related_skills: [linux-audit, windows-audit]
---

# Credential Auditing

## Overview
This skill focuses on searching for leaked API keys, tokens, hardcoded passwords, and weak system credential policies.

## Methodology (9-Phase Sequence)
1. **Recon**: Map host filesystems, git repositories, and credential storage endpoints. Log targets via `security_inventory`.
2. **Enumeration**: Search for config filenames containing secrets (`.env`, `credentials.xml`, `config.json`).
3. **Collection**: Extract files containing suspected keys/tokens, and read system password policies.
4. **Evidence**: Validate leaked secret signatures (metadata only, no raw secrets) and record findings as Evidence via `security_evidence`.
5. **Analysis**: Trace where credentials are used and map credential-to-host links in the InfrastructureGraph.
6. **Prioritization**: Execute `security_risk` to grade key exposures based on scope of access and system criticality.
7. **Recommendation**: Formulate key rotation instructions, environment variable updates, and password policy hardening actions.
8. **Verification**: Verify that configuration files are purged, keys are rotated, and old keys return authorization errors.
9. **Report**: Document leaked keys, credential mappings, and revocation proofs in a report via `security_report`.
