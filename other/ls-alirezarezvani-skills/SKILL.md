---
name: ls-alirezarezvani-skills
description: Inventory wrapper for the alirezarezvani Claude skills bundle. Use when
  triaging its broad skill catalog and large script surface before any targeted import.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: wrapper
    source_url: https://github.com/alirezarezvani/claude-skills
    source_path: <repository inventory>
    source_commit: 1bd5b1a0b51c91f6e3335592c2b41ffb9b543002
    source_ref: main
    source_sha256: cbc675c01e0a1d43470626a00a8ba105691d2e4d251bea515bf319088ccccc7d
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Large Claude Skills Bundle

Use this skill when working on large Claude skills bundle tasks.

## Workflow

- Do not bulk-import this repository; it contains a very large mixed skill surface.
- Select one candidate at a time, then run importer, vetter, normalizer, and sandbox checks before adoption.
- Check for overlap with LocalSetup-native process, engineering, compliance, marketing, and ops skills.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## Upstream Coverage

See [upstream coverage](./references/upstream-coverage.md) for the compact inventory captured during this import wave.

## Provenance

- Source: `https://github.com/alirezarezvani/claude-skills`
- Ref: `main` at `1bd5b1a0b51c91f6e3335592c2b41ffb9b543002`
- Source path: `<repository inventory>`
- License classification: `MIT`
- Source SHA-256: `cbc675c01e0a1d43470626a00a8ba105691d2e4d251bea515bf319088ccccc7d`
