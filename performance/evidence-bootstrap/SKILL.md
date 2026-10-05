---
name: evidence-bootstrap
description: Use when adding ShapeShift Labs Evidence Kit to a JS/TS project, initializing the full tests/fuzzers/benchmarks/package-boundary/perf-wiki harness, or helping an AI agent establish maximum evidence coverage in another repository.
---

# Evidence Bootstrap

Use this skill to install the full evidence loop immediately. Do not defer research ingestion, fuzzing, benchmarks, scope checks, package-boundary gates, startup checks, perf search, or perf docs unless the target project cannot run them.

## Workflow

1. Inspect the target repo:

```sh
npx evidence-kit inspect --json
```

If using this repository directly:

```sh
node /path/to/agent-evidence-kit/src/cli.mjs inspect --json
```

2. Initialize the full harness:

```sh
npx evidence-kit init --language js
```

Use `--language ts` for TypeScript projects. Use `--dry-run` first if the worktree is dirty or unfamiliar.

3. Read the generated files and adapt only the project-specific adapters and budgets. Keep the seed/cases/out/check flags intact.

4. Replace placeholder evidence with a target-owned evidence plan. If the target contract is not obvious, use `target-evidence-designer` before deep fuzz or benchmark work.

5. Run:

```sh
npm run test:evidence
npm run bench:evidence
npm run docs:perf
npm run research:list
npm run docs:perf:search -- evidence
npm run evidence:full
```

6. Configure at least one source-pass topic when source mining is relevant:

```sh
npm run research:fetch -- source-pass
```

7. Record the outcome in `iterations/`. Include what passed, what failed, what was fetched, what was kept, what was rejected, and what remains deferred.

## Rules

- Start with all generated gates present.
- Use repeatable fetchers and manifests before writing source-pass conclusions.
- If the package has no public export surface yet, keep the generated package-boundary gate pointed at source entry files until exports exist.
- Do not claim speed, safety, or broad coverage unless a current command backs that exact claim.
- Promote any reduced failure into the target project's corpus file.
