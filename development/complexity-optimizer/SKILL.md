---
name: complexity-optimizer
description: Analyze a software codebase for algorithmic complexity and performance hotspots, then propose or implement safe optimizations without breaking behavior. Use when Codex is asked to scan many files, find inefficient loops, nested iteration, repeated scans, costly rendering/recomputation, N+1 queries, avoidable O(n^2) or O(n) operations, or reduce complexity such as O(n^2) to O(n log n) / O(n), while preserving tests, APIs, outputs, and maintainability.
---

# Complexity Optimizer

## Core Rule

Optimize only when the current behavior is understood and can be preserved. Prefer a small, proven improvement with tests over a broad rewrite with unclear correctness.

## Default Behavior

When the user asks to analyze, scan, audit, review, or "give me a report" for a codebase, produce the full complexity report automatically. Do not require the user to specify report fields.

Default report contents:

- Scope analyzed and detected stack/test commands.
- Top findings ranked by likely impact.
- File and line for each finding.
- Current pattern and why it may be costly.
- Estimated current complexity.
- Recommended change.
- Estimated complexity after the change.
- Risk level.
- Tests, benchmarks, or manual checks needed.
- Clear statement that no files were modified, unless the user explicitly requested implementation.

Only edit files when the user asks to implement, fix, optimize, apply, change, refactor, or otherwise clearly requests code modification. If the user only asks for analysis or a report, do not modify files.

## Workflow

1. Establish the baseline:
   - Identify the language, framework, test command, build command, and performance-sensitive paths.
   - Inspect existing tests before touching code.
   - Run `scripts/analyze_complexity.py <repo>` for a first-pass hotspot list when scanning a repository.

2. Rank opportunities:
   - Prioritize code on hot paths, large input paths, rendering loops, database/API loops, and shared utilities.
   - Separate algorithmic complexity from constant-factor cleanup.
   - Do not patch every warning. Treat scanner output as leads, not proof.
   - For report-only requests, inspect enough surrounding code to estimate current and proposed complexity; do not stop at raw scanner output.

3. Prove behavior:
   - Locate or add focused tests for the function/component being changed.
   - Capture edge cases: empty input, duplicates, ordering stability, null/missing values, errors, permissions, pagination, time zones, and mutation side effects.
   - If tests are absent and behavior is ambiguous, make the smallest refactor or ask for expected behavior before changing semantics.

4. Optimize conservatively:
   - Replace repeated linear lookup with maps/sets when key equality is stable.
   - Replace nested scans with indexing, grouping, two-pointer scans, sweep-line logic, binary search, memoization, batching, or precomputation only when the data shape supports it.
   - In UI code, reduce unnecessary renders with stable props, memoized derived data, virtualization, debounced work, and moving expensive work out of render paths.
   - In data access code, remove N+1 behavior with bulk fetches, joins, preloading, caching, or batching while preserving authorization and filtering.

5. Verify:
   - Run relevant tests and type/lint/build commands.
   - Add a micro-benchmark or measurement when the complexity improvement is non-obvious or performance-critical.
   - Report the original complexity, new complexity, changed files, tests run, and any residual risk.

## First-Pass Scanner

Use the bundled scanner from the skill directory:

```bash
python3 scripts/analyze_complexity.py /path/to/repo --format markdown
python3 scripts/analyze_complexity.py /path/to/repo --format json
```

The scanner flags common patterns in Python, JavaScript, TypeScript, JSX/TSX, Java, Go, C, C++, C#, Ruby, PHP, and Swift files. It intentionally favors readable leads over perfect static analysis.

If the scanner reports nothing, still inspect known hot paths manually. Rendering churn, database query patterns, and framework lifecycle issues often require repository-specific context.

## Optimization Safety Checklist

Before editing:

- Confirm the data sizes are large enough for complexity to matter.
- Confirm the optimization preserves output ordering where callers may rely on it.
- Confirm object identity, mutability, and reference sharing are not part of the public behavior.
- Confirm caches have a valid invalidation strategy.
- Confirm deduplication does not collapse distinct records that share a display label.
- Confirm database batching preserves tenant, permission, soft-delete, pagination, and sorting constraints.

After editing:

- Run the narrow test first, then the broadest relevant test/build command.
- Compare before/after benchmark numbers when a benchmark exists or was added.
- Keep the patch localized. Avoid formatting churn in unrelated files.

## References

- Read `references/optimization-playbook.md` for common O(n^2) to O(n log n) / O(n) transformations and framework-specific patterns.
- Read `references/report-template.md` when preparing the final analysis or audit output.
