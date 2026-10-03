---
name: ls-deploy-checklist
description: Guide deployment readiness checks. Use before releasing apps, services,
  packages, LocalSetup changes, or infrastructure updates.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/anthropics/knowledge-work-plugins
    source_path: engineering/skills/deploy-checklist/SKILL.md
    source_commit: a84404cb0156a15702c9ecf4d16051346cacce49
    source_ref: main
    source_sha256: 85ca53dc471970e3e12c36ec814ebf5f6cb9419016c55adb05ff34789bae3be9
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Deployment Readiness

Use this skill when working on deployment readiness tasks.

## Workflow

- Confirm diff scope, config/secrets, migrations, generated artifacts, rollback, monitoring, and user impact.
- Run the smallest relevant validation first, then broader checks for shared runtime or package surfaces.
- For LocalSetup publish work, include generated docs/version sync and publish-preflight before pushing.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/anthropics/knowledge-work-plugins`
- Ref: `main` at `a84404cb0156a15702c9ecf4d16051346cacce49`
- Source path: `engineering/skills/deploy-checklist/SKILL.md`
- License classification: `Apache-2.0`
- Source SHA-256: `85ca53dc471970e3e12c36ec814ebf5f6cb9419016c55adb05ff34789bae3be9`
