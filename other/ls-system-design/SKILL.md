---
name: ls-system-design
description: Guide system design work. Use for requirements, APIs, data models, service
  boundaries, scalability, reliability, security, and tradeoff analysis.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/anthropics/knowledge-work-plugins
    source_path: engineering/skills/system-design/SKILL.md
    source_commit: a84404cb0156a15702c9ecf4d16051346cacce49
    source_ref: main
    source_sha256: 8f28eca99f2208872fc2483fcc93326b628f4f73116e91309a95e05da86a0ab5
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# System Design

Use this skill when working on system design tasks.

## Workflow

- Clarify functional requirements, non-functional requirements, constraints, and failure modes before drawing components.
- Model data, interfaces, trust boundaries, operations, observability, and migration path.
- Prefer diagrams and ADRs that match the repo's architecture documentation conventions.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/anthropics/knowledge-work-plugins`
- Ref: `main` at `a84404cb0156a15702c9ecf4d16051346cacce49`
- Source path: `engineering/skills/system-design/SKILL.md`
- License classification: `Apache-2.0`
- Source SHA-256: `8f28eca99f2208872fc2483fcc93326b628f4f73116e91309a95e05da86a0ab5`
