---
name: ls-incident-response
description: Guide incident response, triage, mitigation, communication, and postmortems.
  Use for outages, regressions, security incidents, and production failures.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/anthropics/knowledge-work-plugins
    source_path: engineering/skills/incident-response/SKILL.md
    source_commit: a84404cb0156a15702c9ecf4d16051346cacce49
    source_ref: main
    source_sha256: 9eaa7a974c90395ac7116e82710f74546f38e69f735d78f684ee13fd79646e9a
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Incident Response

Use this skill when working on incident response tasks.

## Workflow

- Stabilize first: confirm impact, owner, severity, timeline, current mitigation, and communication channel.
- Separate diagnosis from mitigation; avoid broad changes during an incident unless rollback is ready.
- After resolution, record root cause, contributing factors, detection gap, action items, and validation evidence.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/anthropics/knowledge-work-plugins`
- Ref: `main` at `a84404cb0156a15702c9ecf4d16051346cacce49`
- Source path: `engineering/skills/incident-response/SKILL.md`
- License classification: `Apache-2.0`
- Source SHA-256: `9eaa7a974c90395ac7116e82710f74546f38e69f735d78f684ee13fd79646e9a`
