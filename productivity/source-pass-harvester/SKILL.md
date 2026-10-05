---
name: source-pass-harvester
description: Use when mining external JS/TS libraries, runtimes, papers, benchmark suites, bug corpora, or production systems for ideas that should become local tests, fuzzers, benchmarks, or evidence notes.
---

# Source Pass Harvester

Source passes turn external inspiration into local evidence. They are a fetch/cache/classify/transfer loop, not just agent-written notes.

## Workflow

1. Search local evidence memory first:

```sh
npm run docs:perf:search -- <topic terms>
npm run research:list
```

2. Define the question: what weakness or workload are we trying to learn about? If the target project still lacks target-owned contracts, corpus seeds, or benchmark fixtures, use `target-evidence-designer` first.

3. Add or update a repeatable fetcher and source config:

```sh
npx evidence-kit add-source-fetcher --name <topic>
npm run research:fetch -- <topic>
```

Fetchers should cache external repos under `research/repos/<topic>/`, raw data or metadata under `benchmarks/data/<topic>/`, and write `research/repos/<topic>/manifest.json`.

4. Inspect fetched material for test practice, fuzzer structure, benchmark fixture shape, failure handling, package boundaries, startup budgets, and corpus curation.

5. Transfer ideas into local artifacts:
   - tests,
   - fuzzer corpus cases,
   - benchmark fixtures,
   - package-boundary checks,
   - iteration/research notes.

6. Keep runtime dependencies out unless the benchmark proves they are worth it.
7. Record rejected ideas explicitly.

## Decision Filter

Accept an idea only when it is:

- generic enough for the project contract,
- backed by a local test or benchmark,
- not hard-coded to the source project's domain names,
- not adding hidden state or dependencies without a clear contract.

## Output

Create or update a `research/*-sources.md` note and an `iterations/*-source-pass.md` note. Include source names, URLs, commits or hashes, local cache paths, manifest path, commands, accepted transfers, rejected transfers, and artifact paths.
