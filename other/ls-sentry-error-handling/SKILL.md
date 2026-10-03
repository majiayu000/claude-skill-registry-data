---
name: ls-sentry-error-handling
description: Guide Sentry error handling and observability work. Use for SDK setup,
  issue triage, instrumentation, alerts, releases, and privacy review.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/getsentry/sentry-for-ai
    source_path: skills/sentry-workflow/SKILL.md
    source_commit: bef529f88175f0f9bbce6d203f93383e394d1467
    source_ref: main
    source_sha256: baa8dee53af3be96de34d298b7e577e2d9d54ae6a1e31b8f6e8635d18fe008a2
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Sentry Error Handling

Use this skill when working on Sentry error handling tasks.

## Workflow

- Inspect framework, SDK version, DSN handling, release/environment tags, source maps, and sampling before changes.
- Avoid sending secrets, PII, tokens, request bodies, or oversized payloads to Sentry.
- Validate captured errors, traces, release association, alert rules, and regression workflow after instrumentation.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/getsentry/sentry-for-ai`
- Ref: `main` at `bef529f88175f0f9bbce6d203f93383e394d1467`
- Source path: `skills/sentry-workflow/SKILL.md`
- License classification: `Apache-2.0` (declared by the pinned `SKILL.md`; the repository-root `LICENSE` is `MIT` and is not the file-level classification).
- Source SHA-256: `baa8dee53af3be96de34d298b7e577e2d9d54ae6a1e31b8f6e8635d18fe008a2`
