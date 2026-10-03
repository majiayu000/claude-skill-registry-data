---
name: ls-architecture
description: Guide architecture analysis and decision records. Use for ADRs, tradeoff
  review, boundaries, dependencies, data flow, and LocalSetup-compatible design decisions.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/anthropics/knowledge-work-plugins
    source_path: engineering/skills/architecture/SKILL.md
    source_commit: a84404cb0156a15702c9ecf4d16051346cacce49
    source_ref: main
    source_sha256: de7db3170a3ae1a894c70ef6cb555fe15618ed9b9674d20895eda3d2a0a5f9a2
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Architecture Review

Use this skill when working on architecture review tasks.

## Workflow

- State the decision, context, constraints, options, tradeoffs, and consequences before proposing implementation.
- Prefer small reversible decisions and explicit boundaries over speculative abstractions.
- Record durable architecture outcomes in the repo's established ADR or design-document location.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/anthropics/knowledge-work-plugins`
- Ref: `main` at `a84404cb0156a15702c9ecf4d16051346cacce49`
- Source path: `engineering/skills/architecture/SKILL.md`
- License classification: `Apache-2.0`
- Source SHA-256: `de7db3170a3ae1a894c70ef6cb555fe15618ed9b9674d20895eda3d2a0a5f9a2`
