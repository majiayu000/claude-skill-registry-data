---
skill_name: doctor
activation_code: DOCTOR_V1
version: 1.0.0
phase: any
category: utility
command: /doctor
aliases: ["/diagnose", "/health", "/fix-hooks"]
description: |
  Diagnostic and repair tool for dev-system. Checks hooks, settings files,
  path alignment, and common errors. Can auto-fix many issues.
tier: focused
model: haiku
---

# Dev-System Doctor Skill
# Copyright (c) 2025 James J Ter Beest III. All Rights Reserved.

## Description

Comprehensive diagnostic tool that identifies and repairs dev-system issues.
Particularly useful when hook errors appear in chat sessions.

## Activation Criteria

- User types `/doctor`, `/diagnose`, `/health`, or `/fix-hooks`
- User says "run diagnostics", "check hooks", "fix errors"
- Hook errors are detected in the session
- After failed skill activations

## Usage

```
/doctor              - Run full diagnostic
/doctor --fix        - Auto-fix issues where possible
/doctor --verbose    - Show detailed output
/doctor --json       - Output as JSON for programmatic use
```

## What It Checks

### 1. Environment
- Bash version (≥4.0 required)
- jq installation
- timeout command availability
- CLAUDE_PROJECT_DIR setting

### 2. Settings Files
- Local `.claude/settings.json` validity
- Global `~/.claude/settings.json` validity
- Conflicts between local and global
- Hook path configurations

### 3. Hook Files
- All referenced hooks exist
- All hooks are executable
- hook-utils.sh library present
- Syntax errors in hook scripts

### 4. Functional Tests
- Sample hooks produce valid JSON
- Hooks don't timeout
- Hooks handle errors gracefully

### 5. Path Alignment
- Portable path patterns used
- No hardcoded absolute paths
- CLAUDE_PROJECT_DIR fallbacks

### 6. Common Errors
- UTF-8 BOM in files
- Windows line endings (CRLF)
- Missing shebangs
- Bash syntax errors

## Auto-Fix Capabilities

With `--fix`, the doctor can automatically repair:

| Issue | Fix Applied |
|-------|-------------|
| Non-executable hooks | `chmod +x` |
| UTF-8 BOM | Remove BOM bytes |
| Windows line endings | Convert to Unix |
| Invalid settings backup | Create `.backup` file |

## Output Formats

### Standard Output

```
╔═══════════════════════════════════════════════════════════════════════╗
║  Dev-System Doctor v1.0.0                                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Project: /path/to/project                                            ║
╚═══════════════════════════════════════════════════════════════════════╝

[CHECK] Environment
  ✓ Bash 5.2.0 (≥4.0 required)
  ✓ jq installed (jq-1.7)
  ...

==========================================
Summary
==========================================
Errors:   0
Warnings: 1

⚠ Passed with 1 warning(s)
```

### JSON Output (`--json`)

```json
{
  "version": "1.0.0",
  "timestamp": "2025-01-04T12:00:00+00:00",
  "project_dir": "/path/to/project",
  "summary": {
    "errors": 0,
    "warnings": 1,
    "fixes_applied": 0,
    "fixes_available": 1
  },
  "results": [...]
}
```

## Integration with Error Detection

The doctor can be triggered automatically when hook errors occur:

1. **PostToolUse hook** detects error patterns in tool output
2. **Context injection** suggests running `/doctor`
3. **User confirms** and doctor runs diagnostics

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Errors found (some fixable) |
| 2 | Critical errors (manual intervention) |

## Implementation

```bash
# Run from project directory
./scripts/dev-system-doctor.sh [--fix] [--verbose] [--json]
```

## Related

- `validate-hooks.sh` - Detailed hook validation (CI-focused)
- `/cc-setup` - Initial project setup
- `/resume` - Session recovery
