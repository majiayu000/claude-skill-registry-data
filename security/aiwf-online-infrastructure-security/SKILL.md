---
name: aiwf-online-infrastructure-security
description: Use for internet-facing infrastructure, DNS, TLS, certificates, reverse proxies, cloud or VPS IAM, containers, firewalls, VPNs, remote administration, exposed ports, service identities, rate limits, backups, monitoring, patching, and online attack-surface review.
---

# AIWF Online Infrastructure Security

## Core Rule

Map the real exposure path before changing infrastructure: DNS, CDN/proxy, public IP, port, protocol, TLS termination, service, identity, data, logs, and recovery owner.

## Workflow

1. Confirm ownership, environment, provider, region, asset criticality, users, and authorized target scope.
2. Inventory domains, certificates, public addresses, ports, ingress/egress, admin paths, identities, secrets, storage, backups, and monitoring.
3. Minimize exposure and privilege. Separate public service access from administrative and machine-to-machine access.
4. Verify TLS and certificate lifecycle, supported protocols, proxy trust, security headers where applicable, and secret rotation paths.
5. Review IAM, MFA, service accounts, firewall/security-group rules, container privileges, image provenance, patch posture, logging, alerts, rate limits, and rollback.
6. Validate from the intended network position and distinguish configured controls from observed runtime controls.
7. Produce a prioritized exposure register with owner, evidence, remediation, rollback, and recheck date.

Read `references/source-register.json` before current vulnerability, protocol, cloud, or patch claims.

## Hard Gates

- Explicit approval and exact targets are required before network scans, external probes beyond ordinary HTTP/TLS inspection, firewall/DNS/IAM changes, public exposure, credential rotation, isolation, or production mutation.
- Never scan third-party ranges, attempt exploitation, evade controls, or claim an asset is secure from a port list alone.
- Do not expose local AI endpoints directly to the internet as a convenience fix.
- Add `aiwf-networking-iot` for reliability/protocol behavior and `aiwf-incident-response-recovery` for active compromise.

## Output

Return the exposure map, observed versus assumed controls, prioritized findings, approval gates, rollback steps, and exact validation evidence.
