---
name: write-hook
description: Create Claude Code hooks for static analysis and code quality. Provides pre-built linting, formatting, and type-checking hooks. Use when setting up project quality gates, enforcing code standards, or adding pre-commit style checks.
---

# Hook Creator

Create hooks that enforce code quality through static analysis.

## Core Principles

1. **Exit code 2 blocks** - Use to prevent bad code from being written
2. **Fast checks only** - Hooks run synchronously; keep under 5 seconds
3. **JSON stdin/stdout** - Hooks receive context, can output structured responses
4. **Fail safe** - Non-zero (except 2) continues execution with warning
5. **Use Python** - Wrap shell commands in Python for cross-platform compatibility

## Quick Start

Add a static check hook:

```bash
python3 scripts/add_hook.py <hook-name> --type <lint|format|typecheck|custom>
```

Options:
- `--type`, `-t`: Hook template type (default: `custom`)
- `--path`, `-p`: Output directory (default: `.claude/hooks`)
- `--event`, `-e`: Hook event (default: `PostToolUse`)

## Hook Structure

```
.claude/
├── hooks/
│   ├── eslint_check.py       # Linting hook
│   ├── prettier_check.py     # Formatting hook
│   └── typecheck.py          # Type checking hook
└── settings.json             # Hook configuration
```

## Configuration Format

**Important:** Hooks must be configured in `.claude/settings.json` (not `settings.local.json`). The `settings.json` file is shared with the team via version control, ensuring consistent hook behavior across all collaborators.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/eslint_check.py",
          "timeout": 30
        }]
      }
    ]
  }
}
```

## Static Check Patterns

### 1. Linting (ESLint, Ruff, etc.)

```python
#!/usr/bin/env python3
import json, subprocess, sys

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

if not file_path.endswith(('.js', '.ts', '.tsx')):
    sys.exit(0)

result = subprocess.run(
    ['npx', 'eslint', '--format', 'compact', file_path],
    capture_output=True, text=True
)

if result.returncode != 0:
    print(f"ESLint errors:\n{result.stdout}", file=sys.stderr)
    sys.exit(2)  # Block the action
```

### 2. Formatting Check

```python
#!/usr/bin/env python3
import json, subprocess, sys

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

result = subprocess.run(
    ['npx', 'prettier', '--check', file_path],
    capture_output=True, text=True
)

if result.returncode != 0:
    # Auto-fix instead of blocking
    subprocess.run(['npx', 'prettier', '--write', file_path])
    print(f"Auto-formatted: {file_path}")
```

### 3. Type Checking

```python
#!/usr/bin/env python3
import json, subprocess, sys

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

if not file_path.endswith(('.ts', '.tsx')):
    sys.exit(0)

result = subprocess.run(
    ['npx', 'tsc', '--noEmit', '--pretty', 'false'],
    capture_output=True, text=True
)

if result.returncode != 0:
    # Filter errors for this file only
    errors = [l for l in result.stdout.split('\n') if file_path in l]
    if errors:
        print('\n'.join(errors[:5]), file=sys.stderr)
        sys.exit(2)
```

## Event Selection Guide

| Event | Use Case | Blocking |
|-------|----------|----------|
| `PreToolUse` | Validate before write | Yes |
| `PostToolUse` | Check after write | Yes |
| `UserPromptSubmit` | Add linting context | Yes |

## Exit Codes

| Code | Meaning | Effect |
|------|---------|--------|
| 0 | Success | Continue, stdout shown in verbose |
| 2 | Block | Action blocked, stderr fed to Claude |
| Other | Warning | Continue, stderr shown in verbose |

## Verification

After creating a hook, verify it works:

```bash
# Test with sample input
echo '{"tool_input":{"file_path":"test.ts"}}' | .claude/hooks/your_hook.py
echo $?  # Should be 0 (pass) or 2 (block)
```

Check:
- Exit code 0 for valid files, 2 for violations
- Errors go to stderr, info to stdout

## Best Practices

1. **Filter by extension** - Only run checks on relevant files
2. **Cache dependencies** - Avoid npm/pip on every check
3. **Limit output** - Show first 5-10 errors, not all
4. **Auto-fix when safe** - Format instead of block

## References

- [static-checks.md](references/static-checks.md) - Complete hook examples
- [events.md](references/events.md) - Hook events reference
