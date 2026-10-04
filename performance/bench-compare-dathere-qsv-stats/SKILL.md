---
name: bench-compare
description: Run before/after benchmarks comparing current branch against master
disable-model-invocation: true
---

# Benchmark Comparison

Compare performance of the current branch against master using hyperfine.

## Workflow

1. Note the current branch name and ensure working tree is clean (stash if needed)
2. Build the library in release mode on the current branch: `cargo build --release`
3. Run the user-specified benchmark or test command with hyperfine, e.g.:
   ```
   hyperfine --warmup 3 --min-runs 10 'cargo test --release <test_name>'
   ```
4. Record the result (mean, stddev, min, max)
5. Switch to master: `git checkout master`
6. Build release: `cargo build --release`
7. Run the same benchmark with hyperfine
8. Record the result
9. Switch back to the original branch (and pop stash if used)
10. Report a comparison table:

| Branch | Mean | Stddev | Min | Max |
|--------|------|--------|-----|-----|
| master | ... | ... | ... | ... |
| current | ... | ... | ... | ... |
| **Change** | **+/- %** | | | |

## Arguments

The user should provide:
- The benchmark command or test name to run
- Optionally: number of warmup runs and min runs (defaults: 3 warmup, 10 runs)

## Notes

- Always build with `--release` for meaningful benchmarks
- If the user doesn't specify a command, ask what to benchmark
- Use `hyperfine --export-markdown` if the user wants a shareable report
