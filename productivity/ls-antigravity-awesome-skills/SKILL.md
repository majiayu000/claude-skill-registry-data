---
name: ls-antigravity-awesome-skills
description: Inventory wrapper for the Antigravity awesome skills bundle. Use when
  evaluating that large bundle before selecting narrow LocalSetup-native coverage.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: wrapper
    source_url: https://github.com/sickn33/antigravity-awesome-skills
    source_path: <repository inventory>
    source_commit: 432c3e4319b41e55051b5eafad7ca33eadb534d6
    source_ref: main
    source_sha256: 11c199f121f5568daf2fad2bd820e995ec45358be4e7d1956c6ef4299519b965
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Antigravity Awesome Skills Bundle Inventory

Use this skill when working on Antigravity awesome skills bundle inventory tasks.

## Workflow

- Treat this as an upstream inventory and triage surface, not a signal to bulk-install thousands of skills.
- Resolve overlap with existing LocalSetup skills before importing any individual upstream item.
- Run importer, vetter, normalizer, and sandbox checks on the selected source path before any future import.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## Upstream Coverage

See [upstream coverage](./references/upstream-coverage.md) for the compact inventory captured during this import wave.

## Provenance

- Source: `https://github.com/sickn33/antigravity-awesome-skills`
- Ref: `main` at `432c3e4319b41e55051b5eafad7ca33eadb534d6`
- Source path: `<repository inventory>`
- License classification: `MIT`
- Source SHA-256: `11c199f121f5568daf2fad2bd820e995ec45358be4e7d1956c6ef4299519b965`
