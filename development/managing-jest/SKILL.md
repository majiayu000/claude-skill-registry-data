---
name: managing-jest
description: |
  Use when working with Jest — jest testing framework management and analysis.
  Covers test suite configuration, coverage reporting, snapshot testing review,
  test result parsing, watch mode configuration, and module mocking analysis.
  Use when managing Jest test suites, investigating test failures, reviewing
  code coverage, or analyzing snapshot diffs.
connection_type: jest
preload: false
---

# Jest Testing Framework Management Skill

Manage and analyze Jest test suites, coverage, and configurations.

## Core Helper Functions

```bash
#!/bin/bash

# Run Jest with JSON reporter
jest_run() {
    local args="${1:-}"
    npx jest $args --json --outputFile=jest-results.json 2>/dev/null
}

# Parse Jest results
jest_results() {
    cat jest-results.json 2>/dev/null || echo '{"numTotalTests":0,"testResults":[]}'
}
```

## MANDATORY: Discovery-First Pattern

**Always discover Jest configuration and test structure before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Jest Configuration ==="
if [ -f "jest.config.ts" ]; then
    grep -E "(testMatch|testPathIgnorePatterns|coverageThreshold|transform|moduleNameMapper|setupFiles|preset)" jest.config.ts | head -15
elif [ -f "jest.config.js" ]; then
    grep -E "(testMatch|testPathIgnorePatterns|coverageThreshold|transform|moduleNameMapper|setupFiles|preset)" jest.config.js | head -15
else
    node -e "const pkg = require('./package.json'); console.log(JSON.stringify(pkg.jest || {}, null, 2))" 2>/dev/null | head -15
fi

echo ""
echo "=== Jest Version ==="
npx jest --version 2>/dev/null

echo ""
echo "=== Test File Summary ==="
find . -name "*.test.ts" -o -name "*.test.js" -o -name "*.test.tsx" -o -name "*.test.jsx" -o -name "*.spec.ts" -o -name "*.spec.js" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "Total test files:"
find . -name "*.test.ts" -o -name "*.test.tsx" 2>/dev/null | grep -v node_modules | head -15

echo ""
echo "=== Snapshot Files ==="
find . -name "*.snap" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "Snapshot files:"
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Last Test Run Results ==="
if [ -f "jest-results.json" ]; then
    cat jest-results.json | jq '{
        total: .numTotalTests,
        passed: .numPassedTests,
        failed: .numFailedTests,
        pending: .numPendingTests,
        suites_total: .numTotalTestSuites,
        suites_failed: .numFailedTestSuites,
        duration_sec: (.testResults | map(.perfStats.end - .perfStats.start) | add / 1000 | floor)
    }'

    echo ""
    echo "=== Failed Tests ==="
    cat jest-results.json | jq -r '
        .testResults[] | select(.status == "failed") |
        .testResults[] | select(.status == "failed") |
        "\(.ancestorTitles | join(" > ")) > \(.title)\n  \(.failureMessages[0] | split("\n")[0])"
    ' | head -20
fi

echo ""
echo "=== Coverage Summary ==="
if [ -f "coverage/coverage-summary.json" ]; then
    cat coverage/coverage-summary.json | jq '.total | {
        lines: "\(.lines.pct)%",
        branches: "\(.branches.pct)%",
        functions: "\(.functions.pct)%",
        statements: "\(.statements.pct)%"
    }'
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Parse JSON output rather than console text
- Never dump full snapshots — show only diff summaries

## Anti-Hallucination Rules
- NEVER guess test file names — always discover via filesystem
- NEVER fabricate coverage numbers — parse actual coverage-summary.json
- NEVER assume Jest config location — check jest.config.*, package.json

## Safety Rules
- NEVER update snapshots without explicit user confirmation
- NEVER modify test files without user approval
- NEVER delete coverage reports without user consent

## Output Format

Present results as a structured report:
```
Managing Jest Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

