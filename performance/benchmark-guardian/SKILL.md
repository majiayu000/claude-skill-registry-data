---
name: benchmark-guardian
description: Use for JS/TS performance-sensitive changes, benchmark additions, benchmark regressions, benchmark result JSON, or any claim that code is faster, smaller, cheaper, or not slower.
---

# Benchmark Guardian

Do not make performance claims from intuition.

## Workflow

1. State the benchmark hypothesis:
   - target behavior,
   - metric,
   - fixture,
   - command,
   - acceptance threshold or baseline.

2. Prefer focused benchmarks while iterating:

```sh
npx evidence-kit add-benchmark --name core --language js
npm run bench:evidence
```

3. Write structured JSON to `benchmarks/results/*latest.json`.

4. Run correctness tests or fuzzers for the same path before saying a performance change is safe.

5. Update evidence docs:

```sh
npm run docs:perf
npm run docs:perf:search -- <benchmark topic>
```

## Result Rules

- Keep timeout, error, unsupported, and bad-result rows visible.
- Report exact command and output file.
- Report fixture-level rows, not only aggregate scores.
- If benchmark scope changed, run `npm run bench:scope` or `npx evidence-kit scope`.
- If the benchmark came from external research, cite the fetch manifest and source note path.

## Final Response

Include the command, output path, key rows, and caveats such as dirty worktree, missing baseline, or local machine noise.
