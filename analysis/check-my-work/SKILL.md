---
name: check-my-work
description: Run after making changes, before committing — reviews the current git diff for impact and risk via cqs review.
---

# Check My Work

Run after making changes, before committing. Reviews your diff for impact and risk.

## Arguments

None — operates on the current git diff.

## Process

1. Run `cqs review --json` via Bash (analyzes current diff). Default covers unstaged changes; if the work is already committed on a branch, use `cqs review --base <ref>` (e.g. `--base main`) to diff against the base instead of raw git plumbing.
2. If no diff, say "No changes to review" and stop
3. Present results as a review checklist

## Output Format

```
## Diff Review

### Changed Functions
<from review: list of modified functions with risk scores>

### Affected Callers
<from review: callers of changed functions that may need updates>

### Tests to Re-run
<from review: tests that exercise the changed functions>

### Risk Assessment
<from review: overall risk level and reasoning>

### Checklist
- [ ] All affected callers still work with your changes
- [ ] Tests listed above pass: `cargo test --features cuda-index -- <test_names>`
- [ ] No new warnings from `cargo clippy --all-targets --features cuda-index`
- [ ] Changes formatted: `cargo fmt`
```

## Rules

- If `cqs review` returns no changed functions, first confirm the diff is genuinely non-code (docs, config) with `git diff --stat`. From a `.claude/worktrees/` lane an empty review despite real `.rs` edits is a RED FLAG — `cqs review` diffs the worktree, so an empty result means either no indexed function changed or something is wrong; do NOT rationalize it away, verify against `git diff` before skipping the impact analysis
- If risk is High, recommend the user review each affected caller manually before committing
- If no tests cover the changed functions, flag prominently
