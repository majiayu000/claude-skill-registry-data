---
name: perf-wiki-builder
description: Use when creating or updating JS/TS performance evidence notes, iteration logs, research notes, generated docs/perf indexes, or searchable benchmark/result summaries.
---

# Perf Wiki Builder

The perf wiki is a searchable evidence index over notes and benchmark rows.

## Workflow

1. Search existing memory before adding new notes:

```sh
npm run docs:perf:search -- <topic terms>
```

2. Add or update an iteration note under `iterations/`.
3. Add source maps or research notes under `research/` when external ideas shaped the work. If the note depends on external material, include the fetcher, manifest, cache path, URL, commit, or hash.
4. Ensure benchmark JSON lives under `benchmarks/results/*latest.json`.
5. Generate docs:

```sh
npx evidence-kit docs
```

6. Check generated docs before finishing:

```sh
npx evidence-kit docs --check
```

## Note Shape

Iteration notes should include:

- Goal
- Implemented
- Current Result
- Decision
- Deferred
- Verification

Use verdicts: `accepted`, `rejected`, `regressed`, `needs-revisit`, `measured`, `reference`, or `logged`.

## Rule

Historical notes are evidence, not current truth. For current API or performance claims, check current source and latest benchmark JSON.
