---
name: ls-react-email
description: Guide React Email template development. Use for JSX email components,
  styling, previews, rendering, i18n, and provider handoff.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/resend/resend-skills
    source_path: skills/react-email/SKILL.md
    source_commit: 298207bbe7a43d1886dc9490ecf880b5442600f9
    source_ref: main
    source_sha256: 6316bdbe822e49f93a709e81bc011569d1a1ea20f7de78cd33ea8a0501ad79b7
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# React Email

Use this skill when working on React Email tasks.

## Workflow

- Inspect the project mailer stack, package versions, preview command, and rendering path before editing templates.
- Prefer table-safe, client-compatible layouts and inline-compatible styling over app-style CSS assumptions.
- Render previews and test representative clients or snapshots before shipping template changes.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/resend/resend-skills`
- Ref: `main` at `298207bbe7a43d1886dc9490ecf880b5442600f9`
- Source path: `skills/react-email/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `6316bdbe822e49f93a709e81bc011569d1a1ea20f7de78cd33ea8a0501ad79b7`
