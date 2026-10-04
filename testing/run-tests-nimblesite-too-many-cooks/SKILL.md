---
name: run-tests
description: Run tests for Too Many Cooks packages. Detects which packages to test based on changed files.
argument-hint: "[mcp|extension|all]"
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Run Tests

## Step 1: Determine what to test

If `$ARGUMENTS` specifies a package, use that. If no args specified, assume everything

## Step 2: Run tests

**MCP server (integration):**
```bash
bash scripts/test-mcp.sh
```

**VSCode extension + MCP e2e:**
```bash
bash scripts/test-vsix-e2e.sh
```
On headless Linux, prefix with `xvfb-run -a`.

**All:**
```bash
bash scripts/test-mcp.sh && bash scripts/test-vsix-e2e.sh
```

## After running

1. Report PASS/FAIL per package
2. If failures occur, read the output and diagnose
3. You are NOT ALLOWED to modify tests. You must fix the bugs without modifying the tests
