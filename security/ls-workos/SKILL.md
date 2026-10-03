---
name: ls-workos
description: Guide WorkOS integration work. Use for AuthKit, SSO, organizations, directory
  sync, audit logs, RBAC, FGA, MFA, and migration tasks.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/workos/skills
    source_path: plugins/workos/skills/workos/SKILL.md
    source_commit: 2c3acef61ea29296cb6e73e0c59fb5e98f0b1847
    source_ref: main
    source_sha256: e0c6d0ca1e4c0ac57707888a2cca6e62497e2696307b19c5be244b51fc836f13
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Workos Integration

Use this skill when working on WorkOS integration tasks.

## Workflow

- Inspect framework, auth boundary, session model, organization model, and SDK version before implementation.
- Keep client IDs, API keys, webhook secrets, and tenant identifiers out of source and logs.
- Validate callback URLs, cookie/security settings, organization membership, and migration rollback paths.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/workos/skills`
- Ref: `main` at `2c3acef61ea29296cb6e73e0c59fb5e98f0b1847`
- Source path: `plugins/workos/skills/workos/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `e0c6d0ca1e4c0ac57707888a2cca6e62497e2696307b19c5be244b51fc836f13`
