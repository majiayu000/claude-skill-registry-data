---
name: ls-valyu
description: Guide Valyu search integration. Use for Valyu-powered deep search, retrieval
  workflows, source grounding, and API-key handling.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/valyuAI/skills
    source_path: valyu-deep-search/SKILL.md
    source_commit: be57c51696fa74a0fce129e3dc165c93c599a0c9
    source_ref: main
    source_sha256: 5944ee465ae669346c334ba483b0850a1330dfc1abc5456d7eb00161ed54e0c5
    license: NO_REPO_LICENSE_FOUND
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Valyu Deep Search

Use this skill when working on Valyu deep search tasks.

## Workflow

- Treat API keys, search queries, and retrieved private data as sensitive.
- Use explicit query scopes, citation requirements, freshness constraints, and result filters.
- Verify source quality and avoid presenting retrieved content as fact without provenance.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## License Boundary

The upstream repository snapshot did not expose a top-level license file during this run. This skill is LocalSetup-native guidance and does not copy upstream body text or bundled assets.

## Provenance

- Source: `https://github.com/valyuAI/skills`
- Ref: `main` at `be57c51696fa74a0fce129e3dc165c93c599a0c9`
- Source path: `valyu-deep-search/SKILL.md`
- License classification: `NO_REPO_LICENSE_FOUND`
- Source SHA-256: `5944ee465ae669346c334ba483b0850a1330dfc1abc5456d7eb00161ed54e0c5`
