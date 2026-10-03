---
name: ls-trail-of-bits
description: Attribution-preserving wrapper for Trail of Bits security skills. Use
  when evaluating security review, audit, fuzzing, and vulnerability-analysis workflows.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: wrapper
    source_url: https://github.com/trailofbits/skills
    source_path: .
    source_commit: cfe5d7b1619e47fb5b38b7e2561dad7e5f1e89af
    source_ref: main
    source_sha256: 6867b487caf10c73043a264b4bcc035f7fd943085b50545c7c0b0c996ad7fe57
    license: CC-BY-SA-4.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Trail Of Bits Security Skills

Use this skill when working on Trail of Bits security skills tasks.

## Workflow

- Do not copy CC-BY-SA-4.0 upstream content into LocalSetup skills without preserving attribution and share-alike obligations.
- Use the upstream bundle as a source map for security workflow gaps and route actual implementation through native skills when possible.
- Security tasks require explicit scope, authorization, and non-destructive validation boundaries.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## Upstream Coverage

See [upstream coverage](./references/upstream-coverage.md) for the compact inventory captured during this import wave.

## Provenance

- Source: `https://github.com/trailofbits/skills`
- Ref: `main` at `cfe5d7b1619e47fb5b38b7e2561dad7e5f1e89af`
- Source path: `.` (upstream repository root; the ordered manifest and aggregate recipe are in [upstream coverage](./references/upstream-coverage.md))
- License classification: `CC-BY-SA-4.0`; governing [upstream LICENSE](https://github.com/trailofbits/skills/blob/cfe5d7b1619e47fb5b38b7e2561dad7e5f1e89af/LICENSE)
- Source SHA-256: `6867b487caf10c73043a264b4bcc035f7fd943085b50545c7c0b0c996ad7fe57`
