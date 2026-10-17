---
name: coverage-improvement
description: Use when working to raise code coverage, target specific uncovered lines, or close the gap against the workspace's configured coverage thresholds and aspirational targets.
---

# Improving Code Coverage

Systematic approach to identifying and covering untested code using
MCP tools.

## Step 1: Identify Coverage Gaps

Use `test_coverage` to see project-wide coverage gaps:

- Files below threshold with exact uncovered line ranges
- Per-metric values (statements, branches, functions, lines)
- Current thresholds and targets

For a specific file, use `file_coverage({ filePath: "src/foo.ts" })`
to get per-metric values and uncovered line ranges.

## Step 2: Understand Existing Tests

Use `test (action: for_file)({ filePath: "src/foo.ts" })` to find which test
files already cover the source file. Then use
`test (action: get)({ fullName: "Suite > test name" })` to understand
individual test scope and history.

## Step 3: Write Targeted Tests

Focus on the uncovered lines from step 1:

1. Read the source file at the uncovered line ranges
2. Identify untested code paths (branches, error handlers, edge cases)
3. Write tests targeting those specific paths
4. Run with `run_tests({ files: ["path/to/test.ts"] })`

## Step 4: Verify Improvement

1. Use `file_coverage` to check the file's updated coverage
2. Use `test_coverage` to verify project-wide improvement
3. Use `test_trends` to confirm coverage direction is improving

## Prioritization

Focus on files with the largest coverage gaps first. Files near
the threshold ("at-risk" files) are the highest priority since
a small regression could push them below the threshold.

## Recording Progress

Use `note (action: create)` to document:

- Which files you improved and by how much
- Untested paths that were intentionally deferred
- Coverage targets agreed upon with the team
