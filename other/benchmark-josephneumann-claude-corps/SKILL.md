---
name: benchmark
description: "Use when you need measured performance evidence by running a repeatable command on the current branch and a baseline ref"
allowed-tools: Read, Bash, Glob, Grep
---

# /benchmark $ARGUMENTS

Run a repeatable benchmark command on the current branch and compare it with a baseline ref. This skill is for measurement, not speculation.

If the user wants architectural performance review without running code, use `/multi-review` with `performance-oracle` instead.

## Arguments

```text
/benchmark "<command>" [--baseline <ref>] [--iterations N]
```

Defaults:
- `--baseline origin/main`
- `--iterations 5`
- warmup runs: `1`

Reject the request if no command is provided.

## Safety Rules

- The benchmark command must be repeatable
- Do not use commands that intentionally mutate repo-tracked files
- Build artifacts and caches are acceptable if they are not tracked
- If the command dirties the worktree, stop and report it

## Phase 1: Pre-Flight

1. Record current branch and `git status --short`
2. Verify the worktree is clean enough to benchmark safely
3. Resolve the baseline ref
4. Determine whether the benchmark command depends on repo-local dependencies, generated assets, or setup steps
5. Create a temporary detached worktree for the baseline
6. Establish equivalent runtime environments for current and baseline before timing anything

Use a temporary directory under `/tmp` or equivalent. Never benchmark the baseline by checking out over the user's current branch.

Environment setup rules:
- Read local sources of truth first: `CLAUDE.md`, `README.md`, and project manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, or `Makefile`
- If the benchmark command depends on installed dependencies or generated artifacts, run the same setup flow in both environments before measuring
- Prefer the project's existing setup command if one is documented, for example `pnpm install --frozen-lockfile`, `uv sync`, `cargo fetch`, or `make setup`
- Do not count setup time as benchmark time
- If you cannot establish equivalent environments on both refs, stop and report that the benchmark would be untrustworthy

## Phase 2: Measurement Protocol

For both current branch and baseline:

1. Run 1 warmup execution
2. Run `N` measured executions
3. Capture wall-clock duration for every measured run
4. If the command prints benchmark metrics already, include them in the notes, but wall-clock time is the required common metric

Prefer a consistent timing mechanism for every run. Keep environment conditions as similar as possible across both refs.

## Phase 3: Summarize Results

Compute for current and baseline:
- all measured run times
- median
- min
- max
- percentage delta of median vs baseline

If run-to-run variance is high, say so. Do not overclaim a tiny difference hidden by noise.

## Required Output

```markdown
## Benchmark Summary

Command: ...
Baseline: ...
Iterations: ...

### Current Branch
Runs: [...]
Median: ...
Min/Max: ...

### Baseline
Runs: [...]
Median: ...
Min/Max: ...

### Delta
Current vs baseline median: ...%

### Notes
- command-native metrics if any
- variance caveats
- anything that may have skewed results
```

## Cleanup

Always remove the temporary baseline worktree before exiting, even on failure.

## Failure Handling

- If the benchmark command fails on either ref, report the failing ref and stop
- If the baseline ref cannot be resolved, stop
- If cleanup fails, report it explicitly

## Interpretation Rules

- Measured improvement beats theoretical reasoning
- High variance weakens confidence
- A benchmark proves only the command that was run, not overall product performance
