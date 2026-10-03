---
name: ls-openclaudia-skills
description: Inventory wrapper for OpenClaudia marketing skills. Use when reviewing
  marketing, growth, SEO, ads, analytics, and content-skill coverage.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: wrapper
    source_url: https://github.com/OpenClaudia/openclaudia-skills
    source_path: <repository inventory>
    source_commit: 221b37d7ab95c14d5343c7b24fd9f9367a3fb400
    source_ref: main
    source_sha256: 175993722ba0f4025f71a4894344ef7f53cd5c9b5c9cab43d6c3f222d87595c0
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Openclaudia Marketing Skills

Use this skill when working on OpenClaudia marketing skills tasks.

## Workflow

- Use this wrapper only to inspect the upstream inventory, triage bundle coverage, and avoid duplicate LocalSetup skill IDs.
- Treat every listed upstream path as inventory evidence, not as an installed, vetted, or executable LocalSetup skill.
- For a candidate import, select one upstream path and run the LocalSetup importer, vetter, normalizer, and sandbox-validation workflow before use.
- Do not expose ad-platform, CRM, analytics, or social account credentials during evaluation.
- Prefer native LocalSetup skills for repeatable CRO, SEO, content, and email workflows.

## Boundaries

- Do not install, invoke, or delegate to upstream skills through this wrapper.
- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## Upstream Coverage

See [upstream coverage](./references/upstream-coverage.md) for the verified 75-file inventory, representative categories, content hashes, and digest method.

## Provenance

- Source: `https://github.com/OpenClaudia/openclaudia-skills`
- Ref: `main` at `221b37d7ab95c14d5343c7b24fd9f9367a3fb400`
- Source path: `<repository inventory>`
- License classification: `MIT`
- Inventoried `SKILL.md` files: `75`
- Source SHA-256: `175993722ba0f4025f71a4894344ef7f53cd5c9b5c9cab43d6c3f222d87595c0`
- Verified: `2026-09-03` from the immutable upstream commit and its non-truncated tree.
