---
name: iterative-development
description: TDD iteration loops using Claude Code Stop hooks - runs tests after each response, feeds failures back automatically
when-to-use: When setting up or configuring TDD loops via Stop hooks
user-invocable: false
effort: medium
---

# Iterative Development Skill (Stop Hook TDD Loops)


**Concept:** Claude Code's Stop hook fires right before Claude finishes a response. Exit code 2 feeds stderr back to the model and continues the conversation. This creates a real TDD loop without any plugins.

---

## How It Actually Works

Claude Code has a **Stop hook** that runs when Claude is about to conclude its response. If the hook script exits with code 2, its stderr is shown to the model and the conversation continues automatically.

```
┌─────────────────────────────────────────────────────────────┐
│  1. User asks Claude to implement a feature                 │
├─────────────────────────────────────────────────────────────┤
│  2. Claude writes tests + implementation                    │
├─────────────────────────────────────────────────────────────┤
│  3. Claude finishes its response                            │
├─────────────────────────────────────────────────────────────┤
│  4. Stop hook runs: executes tests, lint, typecheck         │
├─────────────────────────────────────────────────────────────┤
│  5a. All pass (exit 0) → Claude stops, work is done         │
│  5b. Failures (exit 2) → stderr fed back to Claude          │
├─────────────────────────────────────────────────────────────┤
│  6. Claude sees failures, fixes code, response ends         │
├─────────────────────────────────────────────────────────────┤
│  7. Stop hook runs again → repeat until green or max tries  │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** No fake plugins, no `/ralph-loop` command. The hook is real Claude Code infrastructure that runs automatically.

---

## Setup: Stop Hook Configuration

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "scripts/tdd-loop-check.sh",
            "timeout": 60,
            "statusMessage": "Running tests..."
          }
        ]
      }
    ]
  }
}
```

### The TDD Loop Check Script

Create `scripts/tdd-loop-check.sh` in your project:

```bash
#!/bin/bash
# TDD Loop Check - runs after each Claude response
# Exit 0 = all good, Claude stops
# Exit 2 = failures, stderr fed back to Claude to fix

MAX_ITERATIONS=25
ITERATION_FILE=".claude/.tdd-iteration-count"

# Track iteration count
if [ -f "$ITERATION_FILE" ]; then
    count=$(cat "$ITERATION_FILE")
    count=$((count + 1))
else
    count=1
fi
echo "$count" > "$ITERATION_FILE"

# Safety: stop after max iterations
if [ "$count" -ge "$MAX_ITERATIONS" ]; then
    rm -f "$ITERATION_FILE"
    echo "Max iterations ($MAX_ITERATIONS) reached. Stopping loop." >&2
    exit 0
fi

# Skip if no test files exist yet
if ! find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" 2>/dev/null | grep -q .; then
    rm -f "$ITERATION_FILE"
    exit 0
fi

# Run tests
TEST_OUTPUT=$(npm test 2>&1) || {
    echo "ITERATION $count/$MAX_ITERATIONS - Tests failing:" >&2
    echo "$TEST_OUTPUT" | tail -30 >&2
    echo "" >&2
    echo "Fix the failing tests and try again." >&2
    exit 2
}

# Run lint (if configured)
if [ -f "package.json" ] && grep -q '"lint"' package.json; then
    LINT_OUTPUT=$(npm run lint 2>&1) || {
        echo "ITERATION $count/$MAX_ITERATIONS - Lint errors:" >&2
        echo "$LINT_OUTPUT" | tail -20 >&2
        echo "" >&2
        echo "Fix lint errors and try again." >&2
        exit 2
    }
fi

# Run typecheck (if configured)
if [ -f "tsconfig.json" ]; then
    TYPE_OUTPUT=$(npx tsc --noEmit 2>&1) || {
        echo "ITERATION $count/$MAX_ITERATIONS - Type errors:" >&2
        echo "$TYPE_OUTPUT" | tail -20 >&2
        echo "" >&2
        echo "Fix type errors and try again." >&2
        exit 2
    }
fi

# All green - reset counter and let Claude stop
rm -f "$ITERATION_FILE"
exit 0
```

### Python Variant

```bash
#!/bin/bash
# Python TDD Loop Check

MAX_ITERATIONS=25
ITERATION_FILE=".claude/.tdd-iteration-count"

if [ -f "$ITERATION_FILE" ]; then
    count=$(cat "$ITERATION_FILE")
    count=$((count + 1))
else
    count=1
fi
echo "$count" > "$ITERATION_FILE"

if [ "$count" -ge "$MAX_ITERATIONS" ]; then
    rm -f "$ITERATION_FILE"
    echo "Max iterations ($MAX_ITERATIONS) reached." >&2
    exit 0
fi

if ! find . -name "test_*" -o -name "*_test.py" 2>/dev/null | grep -q .; then
    rm -f "$ITERATION_FILE"
    exit 0
fi

TEST_OUTPUT=$(pytest -v 2>&1) || {
    echo "ITERATION $count/$MAX_ITERATIONS - Tests failing:" >&2
    echo "$TEST_OUTPUT" | tail -30 >&2
    exit 2
}

if command -v ruff &>/dev/null; then
    LINT_OUTPUT=$(ruff check . 2>&1) || {
        echo "ITERATION $count/$MAX_ITERATIONS - Lint errors:" >&2
        echo "$LINT_OUTPUT" | tail -20 >&2
        exit 2
    }
fi

if command -v mypy &>/dev/null; then
    TYPE_OUTPUT=$(mypy . 2>&1) || {
        echo "ITERATION $count/$MAX_ITERATIONS - Type errors:" >&2
        echo "$TYPE_OUTPUT" | tail -20 >&2
        exit 2
    }
fi

rm -f "$ITERATION_FILE"
exit 0
```

---

## Additional Hooks for Quality Enforcement

### PreToolUse Hook: Lint Before File Writes

Runs a linter before any Write/Edit lands:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/pre-write-lint.sh",
            "timeout": 10,
            "statusMessage": "Checking code quality..."
          }
        ]
      }
    ]
  }
}
```

### SessionStart Hook: Auto-Inject Context

Runs at session start to inject project info:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'TDD loop active. Tests run automatically after each response. Fix failures to continue.'",
            "statusMessage": "Loading project context..."
          }
        ]
      }
    ]
  }
}
```

---

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│  ITERATION > PERFECTION                                     │
│  ─────────────────────────────────────────────────────────  │
│  Don't aim for perfect on first try.                        │
│  Let the loop refine the work. Each iteration builds on     │
│  previous attempts visible in files and git history.        │
├─────────────────────────────────────────────────────────────┤
│  FAILURES ARE DATA                                          │
│  ─────────────────────────────────────────────────────────  │
│  Failed tests, lint errors, type mismatches are signals.    │
│  The Stop hook feeds them directly to Claude as context.    │
├─────────────────────────────────────────────────────────────┤
│  CLEAR COMPLETION CRITERIA                                  │
│  ─────────────────────────────────────────────────────────  │
│  The hook defines "done": tests pass, lint clean, types ok. │
│  No ambiguity about when to stop.                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Classification

Not all failures should loop. The hook script should distinguish:

| Type | Examples | Action |
|------|----------|--------|
| **Code Error** | Logic bug, wrong assertion, type mismatch | Exit 2 → loop continues |
| **Access Error** | Missing API key, DB connection refused | Exit 0 → stop, report to user |
| **Environment Error** | Missing package, wrong runtime version | Exit 0 → stop, report to user |

The sample scripts above handle this — they only exit 2 for test/lint/type failures, not for environment issues.

---

## When to Use TDD Loops

### Good For
| Use Case | Why |
|----------|-----|
| Feature development | Tests provide clear pass/fail signal |
| Bug fixes | Write failing test, fix, loop until green |
| Refactoring | Existing tests catch regressions |
| API development | Each endpoint independently testable |

### Not Good For
| Use Case | Why |
|----------|-----|
| UI/UX work | Requires human judgment |
| One-shot operations | No iteration needed |
| Unclear requirements | No clear "done" criteria |
| Subjective design | No objective success metric |

---

## Disabling the Loop

To temporarily disable the TDD loop for a session:

1. Remove or rename the Stop hook in `.claude/settings.json`
2. Or set `MAX_ITERATIONS=1` in the script
3. Or delete `scripts/tdd-loop-check.sh`

The hook only fires if the script exists and is configured.

---

## Gitignore Additions

```gitignore
# TDD loop state
.claude/.tdd-iteration-count
```
