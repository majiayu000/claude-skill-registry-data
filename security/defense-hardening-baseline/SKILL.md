---
name: defense-hardening-baseline
description: >
  Turn offensive findings into concrete hardening — the fix side of each vuln class, plus config
  baselines. Load for blue-team/remediation tasks, "how do we fix/prevent", secure config
  review, or writing the remediation section of a report. Signals: "harden", "remediation",
  "secure baseline", "prevent".
domain: defense
type: reference
stability: learning
modes: [defense]
severity: info
tools: [cis-benchmarks, scout-suite, kube-bench]
schema_version: 1
---

# Hardening baselines & remediation

## When it applies
You need the defensive counterpart: how to fix a class of bug, or how to configure a system so
the class can't occur. Pairs with every offensive skill's "why it works".

## Why it works
Most vuln classes have a small set of correct, well-known mitigations. Applying the right control
at the right layer (input handling, authz at the data layer, safe defaults) removes the class,
not just the instance.

## Remediation by class (the fix that actually works)
- **Injection (SQLi/cmd/LDAP)**: parameterized queries / prepared statements; never build code
  from input; least-privilege DB users.
- **XSS**: context-aware output encoding + a strict CSP (nonce-based, no `unsafe-inline`).
- **Access control (IDOR/BOLA)**: authorize at the *object* layer on every request; deny by default.
- **SSRF**: allowlist egress, block link-local/metadata, enforce IMDSv2, resolve+validate then pin.
- **Deserialization**: don't deserialize untrusted input; use data-only formats; allowlist types.
- **Auth/JWT**: verify signatures/alg, short expiry, rotate, MFA; secrets out of code/URLs.
- **Upload**: validate server-side by content, store outside webroot, random names, no exec.
- **Secrets**: vault/manager, scan CI, rotate on exposure.

## Config baselines
- Cloud: CIS Benchmarks; scan with ScoutSuite/Prowler; enforce IMDSv2, block public buckets.
- Kubernetes: `kube-bench` (CIS), least-privilege RBAC, no privileged pods, network policies.
- Hosts: CIS baselines, patch cadence, disable unused services.

## How to use
For a finding, cite the specific control here in the report's remediation, and (blue-team) turn
it into a config check or a detection (→ `defense-detection-sigma`).

## References
OWASP Cheat Sheet Series; CIS Benchmarks; cloud provider security baselines.
