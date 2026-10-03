---
name: ls-composio
description: Inventory wrapper for Composio skills. Use when evaluating Composio tool
  integrations, OAuth scopes, and connected-account automation.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: wrapper
    source_url: https://github.com/composiohq/skills
    source_path: <repository inventory>
    source_commit: c4b270016aa8c832bb6d5824175da1bb94690b89
    source_ref: main
    source_sha256: 7ad8678bfba65b7534bf59592b234bc68396713ccf1c263d6da7c9ab50be36f7
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Composio Skill Bundle

Use this skill when working on Composio skill bundle tasks.

## Workflow

- Treat OAuth grants, connected-account scopes, tokens, and third-party side effects as high-risk surfaces.
- Prefer narrow tool scopes and explicit user approval before actions in external SaaS accounts.
- Vetting must include credential storage, revocation path, audit logs, and dry-run support where available.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## Upstream Coverage

See [upstream coverage](./references/upstream-coverage.md) for the compact inventory captured during this import wave.

## Provenance

- Source: `https://github.com/composiohq/skills`
- Ref: `main` at `c4b270016aa8c832bb6d5824175da1bb94690b89`
- Source path: `<repository inventory>`
- License classification: `MIT`
- Source SHA-256: `7ad8678bfba65b7534bf59592b234bc68396713ccf1c263d6da7c9ab50be36f7`
