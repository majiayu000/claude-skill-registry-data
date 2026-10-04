---
name: managing-just
description: |
  Use when working with Just — just command runner management. Covers justfile
  analysis, recipe discovery, variable management, recipe dependencies, and
  cross-platform configuration. Use when managing justfiles, discovering
  available recipes, debugging recipe execution, or organizing project commands.
connection_type: just
preload: false
---

# Just Command Runner Management Skill

Manage and analyze justfiles, recipes, variables, and command execution.

## MANDATORY: Discovery-First Pattern

**Always check current justfile configuration and available recipes before modifying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Just Version ==="
just --version 2>/dev/null

echo ""
echo "=== Available Recipes ==="
just --list 2>/dev/null | head -25

echo ""
echo "=== Justfile Location ==="
just --justfile 2>/dev/null
just --summary 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Recipe Details ==="
just --show --unsorted 2>/dev/null | head -30

echo ""
echo "=== Variables ==="
just --evaluate 2>/dev/null | head -15

echo ""
echo "=== Justfile Contents ==="
cat justfile 2>/dev/null || cat Justfile 2>/dev/null | head -30
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- List recipes with their descriptions
- Show recipe dependencies
- Report variable values concisely

## Common Operations

### Show Recipe

```bash
#!/bin/bash
RECIPE="${1:?Recipe name required}"
echo "=== Recipe: $RECIPE ==="
just --show "$RECIPE" 2>/dev/null
```

### Dry Run

```bash
#!/bin/bash
RECIPE="${1:?Recipe name required}"
echo "=== Dry Run: $RECIPE ==="
just --dry-run "$RECIPE" 2>&1 | head -15
```

## Safety Rules

- **Use `just --dry-run`** to preview commands before executing destructive recipes
- **Review recipe dependencies** to understand full execution chain
- **Environment variables** in justfiles should not contain secrets -- use .env files
- **Test cross-platform recipes** on all target platforms before committing

## Output Format

Present results as a structured report:
```
Managing Just Report
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

