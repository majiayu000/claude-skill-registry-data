---
name: security-router
description: "Routes ambiguous security work to one leaf skill. Do not use when a specific security review or fix is already clear."
---

# Security Router

Route security work to the narrowest skill that can produce evidence.

## Workflow

1. Confirm the work is on authorized code/config.
2. Identify whether the request is review-only or patch-producing.
3. Pick one primary skill and read its `SKILL.md`.
4. Use existing Codex Security plugin skills when available.
5. Keep outputs evidence-based: files, lines, exploit path, validation status,
   confidence, and proof gaps.

## Routing

- PR, branch, commit, or working-tree security review ->
  `security-diff-review`.
- One concrete vulnerability or scan finding to fix -> `fix-security-finding`.
- System, service, feature, or repo threat modeling -> `threat-model`.
- CVE/advisory/dependency exposure triage -> `dependency-advisory-audit`.
- Secrets, environment, config defaults, token leakage, or credential handling ->
  `secrets-and-config-review`.
- Authorization, roles, tenant isolation, ownership, object access ->
  `authz-boundary-review`.
- Parsers, archive handling, file loaders, YAML/JSON/XML/pickle, SSRF/path
  traversal through parsing -> `deserialization-parser-review`.
- Lockfiles, install scripts, CI/CD provenance, package publishing ->
  `supply-chain-review`.

## Rule

If a downstream Codex Security skill exists, read it and follow it. If it is not
available in the current runtime, use the selected local skill's fallback
contract and clearly mark any validation gaps.
