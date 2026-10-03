---
name: ls-email-best-practices
description: Guide email product, transactional, marketing, deliverability, accessibility,
  compliance, and lifecycle decisions.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/resend/resend-skills
    source_path: skills/email-best-practices/SKILL.md
    source_commit: 298207bbe7a43d1886dc9490ecf880b5442600f9
    source_ref: main
    source_sha256: f1b957138619784e2c22f7ae689bde6e903a8134ee52d626d8846809382ef0c8
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Email Best Practices

Use this skill when working on email best practices tasks.

## Workflow

- Classify the message type first: transactional, lifecycle, marketing, operational, or support.
- Check consent, unsubscribe requirements, accessibility, content clarity, deliverability, and rate limits.
- Keep secrets, recipient data, and suppression lists out of source and logs.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/resend/resend-skills`
- Ref: `main` at `298207bbe7a43d1886dc9490ecf880b5442600f9`
- Source path: `skills/email-best-practices/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `f1b957138619784e2c22f7ae689bde6e903a8134ee52d626d8846809382ef0c8`
