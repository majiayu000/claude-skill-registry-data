---
name: silent-execution
description: Automatically wraps verbose commands (pytest, ruff, builds) with silent execution for context-efficient output. Use this proactively when running tests, linters, formatters, or build commands to minimize context usage while preserving error information.
---

# Silent Execution for Context Efficiency

Use silent execution wrappers to run verbose commands with minimal context usage. The wrapper suppresses successful output but preserves complete error information.

## When to Use This Skill

**IMPORTANT**: Use this skill proactively (without user request) whenever running these types of commands:

### Always Wrap These Commands

1. **Test Commands**
   - `pytest` or `python -m pytest`
   - `uv run pytest`
   - Any test runner that produces verbose output

2. **Linting and Formatting**
   - `ruff check` or `ruff format`
   - `pyrefly`, `mypy`, `pylint`
   - `black`, `isort`
   - Any code quality tool

3. **Build Commands**
   - `docker build`
   - `cargo build`
   - `npm run build`
   - `make build`

4. **Installation Commands**
   - `uv sync`
   - `pip install`
   - `npm install`, `yarn install`

5. **Git Remote Operations**
   - `git push`, `git pull`, `git fetch`

### DO NOT Wrap These Commands

- `ls`, `cat`, `grep`, `find` - Output is valuable
- `git status`, `git diff`, `git log`, `git branch` - Output is essential
- Any command where you need to see the output

## How to Use

Replace direct command execution with the smart wrapper script:

### Standard Approach (Less Context Efficient)
```bash
uv run pytest tests/
```

### Silent Execution Approach (Context Efficient)
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run pytest tests/"
```

**Important**: Always wrap the command in double quotes to preserve argument boundaries and handle special characters correctly.

The script will:
- ✅ Show a clean success indicator: `✓ Running tests (45 tests, in 2.3s)`
- ❌ Show full error output on failure with the actual command that failed
- 🎯 Automatically detect which commands need wrapping

## Examples

### Example 1: Running Tests

**Without silent execution:**
```bash
$ uv run pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.11.5, pytest-7.4.3, pluggy-1.3.0
rootdir: /Users/user/project
collected 45 items

tests/test_connection.py ....                                            [  8%]
tests/test_parser.py .........                                           [ 28%]
tests/test_orderbook.py ....................                             [ 72%]
tests/test_integration.py ............                                   [100%]

============================= 45 passed in 2.34s ===============================
```
(Uses significant context for success information)

**With silent execution:**
```bash
$ ${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run pytest tests/"
  ✓ Running tests (45 tests, in 2.3s)
```
(Minimal context usage, same information)

### Example 2: Running Linter

**Without silent execution:**
```bash
$ uv run ruff check .
All checks passed!
```

**With silent execution:**
```bash
$ ${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run ruff check ."
  ✓ Ruff check
```

### Example 3: Command Failure (Full Output Preserved)

**Silent execution on failure:**
```bash
$ ${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run pytest tests/"
  ✗ Running tests
Command failed: uv run pytest tests/
============================= test session starts ==============================
FAILED tests/test_parser.py::test_invalid_message - AssertionError: ...
ERROR tests/test_connection.py::test_reconnect - ConnectionError: ...
=========================== 2 failed, 43 passed in 2.1s =======================
```
(Full error output preserved for debugging)

## Integration with Commands

When implementing commands that run multiple checks, use silent execution throughout:

```bash
# Standard approach (verbose)
uv run pytest tests/
uv run ruff check .
uv run ruff format --check .

# Silent execution approach (context efficient)
${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run pytest tests/"
${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run ruff check ."
${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run ruff format --check ."
```

## How It Works

The `smart_wrap.sh` script:
1. Analyzes the command to determine if it should be wrapped
2. If verbose, redirects output to temporary file
3. On success: Shows clean indicator with key metrics (test count, duration)
4. On failure: Shows full output for debugging
5. If not verbose, runs command normally

The script uses pattern matching to detect verbose commands automatically.

## Verbose Mode

Set `VERBOSE=1` to see all output (useful for debugging):

```bash
VERBOSE=1 ${CLAUDE_PLUGIN_ROOT}/scripts/smart_wrap.sh "uv run pytest tests/"
```

## Important Notes

- **Always use proactively** - Don't wait for user to request it
- Preserves all error information - Never hides failures
- Works with any shell command - Not language-specific
- Reduces context usage by 80-95% for successful operations
- Scripts are located in `scripts/` at plugin root
- Use `${CLAUDE_PLUGIN_ROOT}` for portable paths across installations

## Technical Details

### Scripts

- **`smart_wrap.sh`**: Main wrapper that detects and wraps verbose commands
- **`run_silent.sh`**: Core execution engine with output management

Both scripts are in `scripts/` directory (plugin-level, shared across components).

### Exit Codes

The wrapper preserves exit codes from wrapped commands, so CI/CD pipelines work correctly.

## Best Practices

1. **Use consistently**: Apply to all verbose commands in your workflow
2. **Check the output**: The wrapper shows when commands pass/fail
3. **Trust the wrapper**: It preserves all error information
4. **Context efficiency**: Enables running more checks without context limits
5. **Automatic detection**: The script knows which commands to wrap
