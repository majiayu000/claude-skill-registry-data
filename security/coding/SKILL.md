---
name: coding
description: Use when five specialized coding agents (linter, perf, refactor, security,
  test) that enforce quality gates across the development lifecycle. From lint enforcement
  through performance profiling, refactoring, security auditing, and test coverage.
  Use when working with coding agents.
domain: agents
author: oyi77
license: Apache-2.0
subdomain: coding-agents
tags:
- agent
- ai-agent
- automation
- coding
- linter
- perf
- refactor
- security
- test
- quality
- money
triggers:
- coding agents
- linter agent
- performance profiling agent
- refactor agent
- security audit agent
- test coverage agent
- quality gate pipeline
argument-hint: "[module or codebase path]"
version: 1.0.0
category: agents
---
## Overview

This skill is the hub for five specialized coding agents — linter, perf, refactor, security, and test — each owning one discipline on the same codebase. Load it when a change touches quality across multiple dimensions and you want each concern handled by an expert pass. It routes each agent in sequence so the passes compose instead of collide.



# Coding Agents

## Money-Making Overview

| Agent | Revenue Impact | Avg. Savings | Best For |
|---|---|---|---|
| **Linter Agent** | Enforces standards at scale | $300–1,000/project | Bulk rule application, migration, cleanup |
| **Perf Agent** | Cuts infra costs 20–40% | $2,000–20,000/year | Bottleneck profiling, query tuning, cost reduction |
| **Refactor Agent** | Reduces maintenance debt 50% | $3,000–15,000/refactor | Complexity reduction, modernization, splitting monoliths |
| **Security Agent** | Prevents P1 production incidents | $5,000–50,000/incident | Bug bounty, vulnerability scanning, pentest automation |
| **Test Agent** | Cuts regression bugs 80% | $2,000–8,000/release | Coverage gaps, regression tests, e2e flows |

**Combined ROI:** A single pass through all five agents on a medium codebase (50K LOC) saves **$15,000–50,000** by preventing production bugs, reducing cloud costs, and slashing maintenance overhead.

---

## When to Use

**Linter first** — before every PR, after merge conflicts, when adopting new rules, migrating linters.

**Perf when it hurts** — app is slow, memory is growing, queries lag, infra costs too high, capacity planning.

**Refactor before features** — make the change easy before making the easy change. High cyclomatic complexity, duplicated code, monolithic files.

**Security before deploy** — every commit touching auth, payments, PII, or external APIs requires a security gate.

**Test always** — new features (TDD), regression tests for bugs, coverage gaps, integration tests, e2e.

### When NOT to Use

- Trivial one-liner changes — just make the edit.
- Real-time human judgment — agents cannot decide product or business trade-offs.
- Agent lacks access to required tools, credentials, or data.

---

## Combined Capabilities

```
                    ┌──────────────┐
                    │  Linter       │  ← Style enforcement → Convention rules
                    │  Agent        │  ← Bulk fixes → Migration
                    └──────┬───────┘
                           │ clean code
                    ┌──────┴───────┐
                    │  Perf         │  ← Profiling → Benchmarking
                    │  Agent        │  ← Bottleneck identification → Optimization
                    └──────┬───────┘
                           │ profiled
                    ┌──────┴───────┐
                    │  Refactor     │  ← Complexity reduction → Pattern extraction
                    │  Agent        │  ← Dead code removal → Modernization
                    └──────┬───────┘
                           │ restructured
                    ┌──────┴───────┐
                    │  Security     │  ← Vulnerability scan → Exploit validation
                    │  Agent        │  ← Bug bounty → POC generation
                    └──────┬───────┘
                           │ hardened
                    ┌──────┴───────┐
                    │  Test         │  ← Unit tests → Integration tests
                    │  Agent        │  ← E2E tests → Coverage enforcement
                    └──────────────┘
```

### Gate Matrix

| Gate | When | Tool | Fail Criteria |
|---|---|---|---|
| **Lint** | Pre-commit, pre-PR | eslint, ruff, revive, prettier | Any error-level rule violation |
| **Perf** | Pre-release, monthly | py-spy, valgrind, k6, lighthouse | P95 > threshold, memory leak detected |
| **Refactor** | Before feature work | cyclomatic-complexity, sloc | Complexity > 15 per function |
| **Security** | Pre-deploy, bug bounty | semgrep, trufflehog, zap | Any P1/P2 vulnerability |
| **Test** | Post-commit, pre-merge | pytest, vitest, go test | Coverage < 80%, any test failure |

---

## Concrete Action Flow

### Full Quality Pipeline

```bash
# 1. LINT: Clean up before PR
agent linter-agent \
    --path "src/" \
    --config ".eslintrc.cjs" \
    --fix \
    --require "no-unused-vars, no-console"

# 2. PERF: Profile the hot path
agent perf-agent \
    --profile "GET /api/users/:id" \
    --benchmark "1000 req/s" \
    --target "p95 < 200ms" \
    --output perf-report.md

# 3. REFACTOR: Clean up before feature work
agent refactor-agent \
    --target "src/legacy/users.ts" \
    --complexity-threshold 15 \
    --remove-dead-code \
    --modernize "callbacks->async"

# 4. SECURITY: Audit before deploy
agent security-agent \
    --target "https://staging.example.com" \
    --scan "xss, sqli, ssti, ssrf" \
    --output security-report.json

# 5. TEST: Fill coverage gaps
agent test-agent \
    --path "src/services/" \
    --target-coverage 85 \
    --type "unit, integration" \
    --output coverage-report.json
```

### Quick Bug Fix Cycle

```bash
# 1. LINT the fix area first
agent linter-agent --path "src/buggy-file.ts" --fix

# 2. REFACTOR if the code is messy
agent refactor-agent --path "src/buggy-file.ts" --complexity-threshold 10

# 3. Add regression TEST
agent test-agent \
    --bug "SESSION-123" \
    --regression \
    --path "src/buggy-file.ts"

# 4. SECURITY check the change
agent security-agent --diff "$(git diff)"
```

---

## First Action in 60 Minutes

1. **Run linter-agent** on your entire `src/` directory with `--fix`. This removes noise immediately.
2. **Run security-agent** on your staging environment or a recent diff. One quick scan surfaces the top risks.
3. **Run test-agent** with `--coverage-report` to see where you are most exposed.
4. **Run perf-agent** on your slowest endpoint (check your APM or logs for P99).
5. **Run refactor-agent** on the file with the highest churn (git blame reveals it).

**Total time:** ~50 min. You will walk away with: clean code, known vulnerabilities patched, coverage gaps mapped, one bottleneck fixed, and one messy file cleaned.

---

## Real Code Examples

### Python: Full Quality Gate CI Script

```python
#!/usr/bin/env python3
"""CI quality gate: lint → perf → refactor → security → test."""

import json, subprocess, sys
from pathlib import Path

def gate(name: str, *args) -> dict:
    """Run a coding agent gate."""
    cmd = ["agent", f"{name}-agent", "--json", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def quality_pipeline(changed_files: list[str]):
    results = {}

    # Gate 1: Lint
    results["lint"] = gate("linter",
        *[f"--path={f}" for f in changed_files],
        "--fix", "--strict")
    if results["lint"].get("errors", 0) > 0:
        print("LINT FAILED — fixing...")
        sys.exit(1)

    # Gate 2: Security (lightning scan)
    results["security"] = gate("security",
        "--scan=secrets,injection",
        "--diff", subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True, text=True).stdout)
    if any(f["severity"] in ("P1", "P2")
           for f in results["security"].get("findings", [])):
        print("SECURITY FAILED — aborting")
        sys.exit(1)

    # Gate 3: Refactor (complexity check)
    results["refactor"] = gate("refactor",
        *[f"--path={f}" for f in changed_files],
        "--complexity-threshold=12",
        "--dry-run")
    if results["refactor"].get("high_complexity", 0) > 0:
        print(f"REFACTOR: {results['refactor']['high_complexity']} complex functions")

    # Gate 4: Coverage check
    results["test"] = gate("test",
        "--coverage-only",
        "--min-coverage=80")
    if results["test"].get("coverage", 0) < 80:
        print(f"COVERAGE: {results['test']['coverage']}% — below 80%")
        sys.exit(1)

    print("All quality gates passed")
    return results

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else ["src/"]
    quality_pipeline(files)
```

### Bash: One-Shot Quality Report

```bash
#!/bin/bash
# quality-report.sh — run all 5 agents and produce a summary

DIR="${1:-src}"
REPORT="quality-report-$(date +%Y%m%d).md"

echo "# Quality Report $(date)" > "$REPORT"
echo "" >> "$REPORT"

echo "## Lint" >> "$REPORT"
agent linter-agent --path "$DIR" --report --output /tmp/lint.json
jq -r '.summary' /tmp/lint.json >> "$REPORT"

echo "## Performance" >> "$REPORT"
agent perf-agent --path "$DIR" --quick-check --output /tmp/perf.json
jq -r '.hotspots[] | "- \(.file):\(.line) — \(.message)"' /tmp/perf.json >> "$REPORT"

echo "## Refactor Candidates" >> "$REPORT"
agent refactor-agent --path "$DIR" --list-candidates --output /tmp/refactor.json
jq -r '.candidates[] | "- \(.file) — complexity \(.complexity)"' /tmp/refactor.json >> "$REPORT"

echo "## Security" >> "$REPORT"
agent security-agent --path "$DIR" --quick-scan --output /tmp/security.json
jq -r '.findings[] | "- \(.severity): \(.message)"' /tmp/security.json >> "$REPORT"

echo "## Test Coverage" >> "$REPORT"
agent test-agent --coverage-only --output /tmp/test.json
jq -r '. | "- Coverage: \(.coverage)%"' /tmp/test.json >> "$REPORT"

echo "Report written to $REPORT"
```

---

## Verification

- Run the five-agent set (linter, perf, refactor, security, test) on one module and confirm each pass reported concrete findings in its own discipline.
- Introduce a known style violation, a slow loop, and an XSS sink, and confirm each respective agent flags its own issue.
- Verify passes compose: after all five, the module still builds and the original test suite passes.
- Confirm no agent silently skipped its scan (each produced a report).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "My code doesn't have lint errors" | Linter catches the 15 things your editor highlights that you ignore |
| "I will profile when it's slow" | By then the bottleneck is in production costing money |
| "Refactoring is a waste of time" | High complexity = high bug rate. Refactoring pays for itself |
| "I am careful enough, no security issues" | Every developer has blind spots — adversarial review catches them |
| "Tests take too long to write" | Test agent writes tests 10x faster than manual TDD |
| "The existing test coverage is fine" | If you don't measure it, you don't know. Measure then act |
| "I run all these tools locally" | Agents combine + orchestrate + explain results. Tools alone don't |

---

## Output Format

### Linter Agent Output
```json
{
  "files_scanned": 142,
  "errors": 0,
  "warnings": 3,
  "auto_fixed": 27,
  "failed_rules": ["no-console"],
  "summary": "3 warnings remain (all intentional console.log statements)"
}
```

### Perf Agent Output
```json
{
  "endpoints_benchmarked": 5,
  "bottlenecks": [
    { "endpoint": "GET /api/reports", "p95": "3.2s",
      "cause": "N+1 query in reports controller",
      "fix": "Eager load associated users" }
  ],
  "optimization_savings": "~35% p95 reduction predicted",
  "capacity": { "current_rps": 200, "recommended": "Add read replica at 500 rps" }
}
```

### Refactor Agent Output
```json
{
  "files_analyzed": 34,
  "high_complexity": 5,
  "candidates": [
    { "file": "src/processors/payment.ts", "complexity": 28,
      "recommendation": "Split into: validation, calculation, notification processors" }
  ],
  "dead_code_found": 12,
  "unused_deps": 3
}
```

### Security Agent Output
```json
{
  "findings": [
    { "file": "src/api/users.ts", "line": 55, "severity": "P1",
      "type": "SQL injection",
      "evidence": "Raw string interpolation in query",
      "fix": "Use parameterized query" }
  ],
  "scan_details": { "endpoints": 22, "vulnerable": 3, "secure": 19 },
  "poc": "pocs/sqli-users.html"
}
```

### Test Agent Output
```json
{
  "tests_added": 18,
  "coverage_before": 64,
  "coverage_after": 86,
  "test_types": { "unit": 14, "integration": 3, "e2e": 1 },
  "regression_tests": 5,
  "all_passing": true
}
```

---

## Verification Checklist

- [ ] All coding agents executed without errors
- [ ] Lint: zero errors after auto-fix; warnings justified
- [ ] Perf: P95 within threshold, bottlenecks identified with fixes
- [ ] Refactor: high-complexity files documented; dead code removed
- [ ] Security: no P1/P2 findings; P3 findings acknowledged
- [ ] Tests: coverage >= 80%; all tests passing
- [ ] Documentation: config changes, rule additions/removals recorded
- [ ] CI gate: quality pipeline integrated into CI workflow
- [ ] Cost impact: perf optimizations projected to reduce infra costs


## Workflow
See the parent skill for authoritative workflow documentation.

## Sub-Skills & Specialized Playbooks

| Sub-skill | File | Use when |
|---|---|---|
| linter-agent | [SKILL.md](linter-agent/SKILL.md) | Detecting and fixing code style violations while enforcing project conventions and consistent formatting. |
| perf-agent | [SKILL.md](perf-agent/SKILL.md) | Profiling actual bottlenecks before optimizing and verifying improvements with benchmarks. |
| refactor-agent | [SKILL.md](refactor-agent/SKILL.md) | Restructuring code for readability, maintainability, and extensibility without changing external behavior. |
| security-agent | [SKILL.md](security-agent/SKILL.md) | Auditing code for vulnerabilities before they reach production. |
| test-agent | [SKILL.md](test-agent/SKILL.md) | Writing comprehensive test suites for happy paths, errors, edge cases, and integration points. |
