---
name: ls-resend
description: Guide Resend API integration. Use for sending, domains, contacts, broadcasts,
  webhooks, logs, templates, and API-key handling.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/resend/resend-skills
    source_path: skills/resend/SKILL.md
    source_commit: 298207bbe7a43d1886dc9490ecf880b5442600f9
    source_ref: main
    source_sha256: fe13dcce83b6d074a75bf53b13d2d30865528e1d38494139d6f13b802c63dbca
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Resend Email Api

Use this skill when working on Resend email API tasks.

## Workflow

- Inspect SDK version, API-key source, domain verification, environment separation, and webhook signing before edits.
- Use least-privilege API keys and keep recipients, logs, and webhook payloads out of committed examples.
- Validate request shape, retries, idempotency, rate limits, and event handling for production mail paths.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/resend/resend-skills`
- Ref: `main` at `298207bbe7a43d1886dc9490ecf880b5442600f9`
- Source path: `skills/resend/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `fe13dcce83b6d074a75bf53b13d2d30865528e1d38494139d6f13b802c63dbca`
