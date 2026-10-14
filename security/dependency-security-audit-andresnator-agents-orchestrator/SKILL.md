---
name: dependency-security-audit
description: >
  Trigger: dependency audit, CVE scan, vulnerable libraries, runtime support.
  Audit dependency and runtime risk with read-only evidence.
license: MIT
metadata:
  author: andresnator
  version: "2.1.2"
  status: testing
---

# Dependency Security Audit

## Contract

Audit dependency advisories plus declared runtime support. Do not inspect application security, secrets, logging, compliance, or exploits.

- Run only explicitly authorized read-only audit or inventory commands. Never install tools, fix, upgrade, edit manifests/lockfiles.
- Advisory findings require current tool output plus CVE/GHSA/OSV identifier. Dependency trees and manifests prove versions only, never vulnerability status.
- Missing or denied audit tooling uses `method: inventory-only`; list observed versions and required authoritative check, but no vulnerability or EOL verdict.
- Quote command, file, line; never guess versions or advisories.

Command and fallback rules live in `references/ecosystem-commands.md`.

## Output

| Dependency/runtime | Finding | Severity | Evidence | Method | Advisory/check |
|---|---|---|---|---|---|

`Severity` is `critical`, `high`, `medium`, `low`, or `unknown`. Close with ecosystems inspected, commands run, inventory-only gaps, explicit out-of-scope notes. Maximum seven findings.
