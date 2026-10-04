---
name: chealth
description: Check CLAUDE.md health against Anthropic best practices — runs deterministic CLI checks then semantic analysis
version: 0.1.1
---

# /chealth — CLAUDE.md Health Check

You are performing a comprehensive health check on this project's CLAUDE.md files. Follow these steps exactly.

## Step 1: Run deterministic checks

Run the chealth CLI to get structured findings:

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" chealth --exit-zero --format json . 2>&1
```

If the CLI is not installed, tell the user:
> chealth plugin not available. Reinstall with: `claude plugin add chealth`

Parse the JSON output. Note all WARN and DANGER findings.

## Step 2: Read all discovered CLAUDE.md files

From the CLI JSON output, read every file listed in the `file-discovery` result's `details.files` array. Also read any `.claude/rules/*.md` files and files referenced by `@import` paths.

## Step 3: Perform semantic checks

Using the best practices in `${CLAUDE_SKILL_DIR}/reference.md` as your reference, evaluate:

1. **Contradiction detection** — Identify rules that conflict with each other, including across files (Rule 11)
2. **Vague instruction assessment** — Evaluate whether instructions are concrete enough to verify (Rule 9)
3. **Instruction effectiveness** — Judge whether Claude would actually follow each instruction (Rule 18)
4. **Scope appropriateness** — Determine if content belongs in root vs subdirectory vs `.claude/rules/` (Rules 2, 15, 20)

## Step 4: Present unified report

Combine deterministic and semantic findings into a single report using this format:

```
## CLAUDE.md Health Report

### Deterministic Checks (chealth CLI)
[For each finding:]
- [PASS|WARN|DANGER] **check-name**: message [Rule N]

### Semantic Analysis
[For each finding:]
- [PASS|WARN|DANGER] **check-name**: description

### Summary
- X checks passed, Y warnings, Z dangers
- [Top recommendation if any WARN/DANGER found]
```

Use PASS/WARN/DANGER severity levels consistently. Semantic findings are advisory — label them as such.