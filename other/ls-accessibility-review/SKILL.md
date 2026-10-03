---
name: ls-accessibility-review
description: Guide accessibility reviews for UI, documents, and workflows. Use for
  WCAG-oriented audits, keyboard review, semantics, contrast, and remediation planning.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/anthropics/knowledge-work-plugins
    source_path: design/skills/accessibility-review/SKILL.md
    source_commit: a84404cb0156a15702c9ecf4d16051346cacce49
    source_ref: main
    source_sha256: ef42982af0d51238dda2ab16d08626712891bdd41864876c32d1e7b13fb3124f
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Accessibility Review

Use this skill when working on accessibility review tasks.

## Workflow

- Start with the user task and affected disabilities, then inspect semantics, keyboard flow, focus order, labels, and contrast.
- Use automated checks as triage only; manually verify critical flows and assistive-technology behavior where practical.
- Prioritize blockers by user impact and provide concrete remediation steps tied to files or components.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/anthropics/knowledge-work-plugins`
- Ref: `main` at `a84404cb0156a15702c9ecf4d16051346cacce49`
- Source path: `design/skills/accessibility-review/SKILL.md`
- License classification: `Apache-2.0`
- Source SHA-256: `ef42982af0d51238dda2ab16d08626712891bdd41864876c32d1e7b13fb3124f`
