---
name: managing-make
description: |
  Use when working with Make — gNU Make build system management. Covers Makefile
  analysis, target discovery, dependency graphs, variable inspection, and build
  debugging. Use when managing Makefiles, understanding target dependencies,
  debugging build failures, or optimizing parallel builds.
connection_type: make
preload: false
---

# GNU Make Build System Management Skill

Manage and analyze Makefiles, build targets, dependencies, and variables.

## MANDATORY: Discovery-First Pattern

**Always check current Makefile configuration and target structure before modifying builds.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Make Version ==="
make --version 2>/dev/null | head -2

echo ""
echo "=== Makefile Targets ==="
make -pRrq : 2>/dev/null | awk -F: '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$)/ {split($1,a," ");print a[1]}' | sort -u | head -20

echo ""
echo "=== Makefile Includes ==="
grep -E '^include\s|^-include\s' Makefile 2>/dev/null | head -10

echo ""
echo "=== Default Goal ==="
make -pRrq : 2>/dev/null | grep '.DEFAULT_GOAL' | head -1
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Key Variables ==="
make -pRrq : 2>/dev/null | grep -E '^[A-Z_]+\s*=' | head -15

echo ""
echo "=== Target Dependencies ==="
grep -E '^[a-zA-Z0-9_-]+\s*:' Makefile 2>/dev/null | head -15

echo ""
echo "=== Phony Targets ==="
grep '.PHONY' Makefile 2>/dev/null | head -5
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- List targets with their direct dependencies
- Show key variable definitions
- Report build errors concisely

## Common Operations

### Dry Run

```bash
#!/bin/bash
TARGET="${1:-all}"
echo "=== Dry Run: $TARGET ==="
make -n "$TARGET" 2>&1 | head -20
```

### Debug Build

```bash
#!/bin/bash
TARGET="${1:-all}"
echo "=== Build Debug ==="
make -d "$TARGET" 2>&1 | grep -E 'Considering\|Must remake\|Successfully' | head -20
```

## Safety Rules

- **Use `make -n`** (dry run) to preview commands before running destructive targets
- **Parallel builds** (`make -j`) can expose missing dependencies -- test before enabling
- **Never override system variables** (CC, CXX) without understanding downstream effects
- **Review recursive make** calls for correctness -- they can miss dependency changes

## Output Format

Present results as a structured report:
```
Managing Make Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

