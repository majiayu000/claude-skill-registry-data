---
name: ls-workos-widgets
description: Guide WorkOS Widgets integration. Use for Admin Portal, user-management,
  profile, domain verification, and SSO connection widgets.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/workos/skills
    source_path: plugins/workos/skills/workos-widgets/SKILL.md
    source_commit: 2c3acef61ea29296cb6e73e0c59fb5e98f0b1847
    source_ref: main
    source_sha256: 5a4cc1736bea0f5b8c12752e7c8dbb2f6a88b9e4404916361f1f5d321cfec08d
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Workos Widgets

Use this skill when working on WorkOS widgets tasks.

## Workflow

- Choose widget flow and framework adapter before editing UI code.
- Fetch scoped widget tokens server-side and keep token generation out of browser bundles.
- Validate authorization, organization context, styling integration, and error states before release.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/workos/skills`
- Ref: `main` at `2c3acef61ea29296cb6e73e0c59fb5e98f0b1847`
- Source path: `plugins/workos/skills/workos-widgets/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `5a4cc1736bea0f5b8c12752e7c8dbb2f6a88b9e4404916361f1f5d321cfec08d`
