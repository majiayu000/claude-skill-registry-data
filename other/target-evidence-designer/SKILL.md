---
name: target-evidence-designer
description: Use when adapting ShapeShift Labs Evidence Kit to a specific JS/TS project by deriving target-owned source lists, correctness contracts, corpus cases, fuzz generators, benchmark fixtures, source-pass plans, or evidence acceptance criteria from that project's own code, docs, tests, issues, or fetched sources.
---

# Target Evidence Designer

Use this skill after the generic evidence harness exists. The goal is to replace placeholders with evidence derived from the target project itself.

## Workflow

1. Inspect the repo contract:

```sh
npx evidence-kit inspect --json
npm run docs:perf:search -- contract benchmark fuzz source
npm run research:list
```

Read public exports, README/API docs, existing tests, issue/regression fixtures, benchmark scripts, and package boundaries. Do not invent a contract that source or docs do not support.

2. Write a short target evidence map:

- public surfaces that users import or execute,
- behaviors the project documentation promises,
- existing tests that already encode contracts,
- known failures or unsupported cases,
- performance claims that maintainers actually care about,
- external sources worth fetching.

3. Create a target-owned evidence plan with five concrete outputs:

- `research/<topic>-sources.json`: primary sources to fetch.
- `research/<topic>-sources.md`: what was inspected and transferred.
- corpus file: seed cases and known failures.
- `test/fuzz/*`: generated cases plus a stable oracle derived from the target contract.
- `benchmarks/*`: fixtures tied to specific target performance claims.

4. Add or update a repeatable fetcher:

```sh
npx evidence-kit add-source-fetcher --name <topic>
npm run research:fetch -- <topic>
```

Use `git`, `url`, `npm`, `file`, or `inline` source entries. Record URL, commit/hash, local path, and why each source exists.

5. Convert target contracts into executable checks before writing random generators. Each check must name:

- the source of truth for the contract,
- the generated or corpus input shape,
- the expected observation,
- the failure artifact to write on mismatch.

6. Promote corpus seeds deliberately from target evidence:

- documented behavior,
- existing tests,
- fetched source material,
- user-reported failures,
- reduced fuzz failures.

7. Design benchmark fixtures from claims the project will make. Each benchmark row needs a category, fixture, metric, status, and output path under `benchmarks/results/*latest.json`. Keep bad-result, unsupported, timeout, and over-budget rows visible.

8. Run focused verification:

```sh
npm run test:evidence
npm run fuzz
npm run bench:evidence
npm run bench:startup:check
npm run bench:package:gates
npm run docs:perf
npm run docs:perf:search -- <topic>
```

## Rules

- Do not stop at a prose plan when a small executable fixture can be added.
- Do not use external source names as local benchmark names unless the benchmark actually measures that source.
- Do not add runtime dependencies from source mining without benchmark and boundary evidence.
- Keep generated corpora small, readable, and replayable; cache large source material under ignored paths.
- Record rejected ideas with reasons, not silence.
