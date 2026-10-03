---
name: ls-seo-geo-claude-skills
description: Provenance inventory for pinned upstream SEO/GEO Claude skills covering
  search, generative-engine optimization, schema, content, backlink, and rank categories.
  Use to inspect recorded paths and hashes or plan one candidate's future gated import;
  this wrapper does not evaluate or execute those workflows.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: wrapper
    source_url: https://github.com/aaron-he-zhu/seo-geo-claude-skills
    source_path: <repository inventory>
    source_commit: 1608176f6c18de6aec62a9abf6a2074bf82c9f67
    source_ref: main
    source_sha256: 1ee5e247bf057956b14951ad1c910fb9873487fb66a9880027e9e5de579e1028
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Seo And Geo Skill Bundle

Use this wrapper only to inspect provenance for the pinned upstream bundle and plan
a future single-skill import. It does not include, compare, recommend, install,
invoke, delegate to, or execute the upstream SEO/GEO workflows.

## Workflow

- Use the inventory to identify one upstream path for importer intake; filenames are discovery labels, not vetted capability summaries.
- Do not infer functionality, requirements, safety, freshness, or suitability from a path name or hash. Inspect the selected candidate through `ls-skill-importer`, `ls-skill-vetter`, `ls-skill-normalizer`, and `ls-skill-sandbox-tester` before evaluating its fit.
- Avoid credential exposure for analytics, search-console, rank-tracking, or third-party SEO services.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## Upstream Coverage

See [upstream coverage](./references/upstream-coverage.md) for the compact inventory captured during this import wave.

## Provenance

- Source: `https://github.com/aaron-he-zhu/seo-geo-claude-skills`
- Ref: `main` at `1608176f6c18de6aec62a9abf6a2074bf82c9f67`
- Source path: `<repository inventory>`
- Pinned upstream files' license classification: `Apache-2.0`
- Source SHA-256: `1ee5e247bf057956b14951ad1c910fb9873487fb66a9880027e9e5de579e1028`
