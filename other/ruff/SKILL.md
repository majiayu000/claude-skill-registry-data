---
name: ruff
description: Fix all Python lint violations and enforce consistent formatting in one command.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: automation
  since: "2026-02-25"
---

## What I do

I run ruff to auto-fix all fixable lint violations and enforce consistent code formatting in one step:

- **Auto-fix lint violations** — unused imports, line length, style issues, import sorting, and more
- **Enforce formatting** — consistent code style via ruff's Black-compatible formatter
- **Surface unfixable issues** — show exactly which violations need manual attention, with rule codes and locations
- **Configure ruff** — add a minimal `[tool.ruff]` section to `pyproject.toml` if ruff isn't yet configured

## When to use me

- You want to clean up a Python file or entire project before committing
- CI is failing on lint or format checks and you want to auto-fix everything fixable
- You want to see what violations remain after auto-fix so you know what to fix manually
- You're setting up ruff in a project that doesn't have it configured yet

## Example usage

```
/ruff
/ruff check
/ruff format
/ruff init
"fix linting"
"fix all lint issues"
```

---

## Workflow

### Fixing lint violations automatically

Run `ruff check --fix` to auto-fix all fixable lint violations in the current directory:

```bash
ruff check --fix .
```

ruff fixes violations it can safely transform automatically — including:
- Unused imports (`F401`)
- Import sorting (`I001`) — replaces isort
- Unnecessary f-strings, redundant open modes, and other style issues
- pyupgrade-style modernisations (e.g. `Union[X, Y]` → `X | Y` for Python 3.10+)

**Interpreting output**:
- ruff prints each fixed violation: `Fixed 1 error.` or `Found 3 errors (3 fixed, 0 remaining).`
- Exit code 0: all violations fixed or none found
- Exit code 1: violations remain that could not be auto-fixed (see [Understanding unfixable violations](#understanding-unfixable-violations))

**Example output**:
```
Found 5 errors (5 fixed, 0 remaining).
```

---

### Enforcing consistent formatting

Run `ruff format` to apply consistent code style across all Python files:

```bash
ruff format .
```

ruff's formatter is Black-compatible — it produces the same output as Black for the vast majority of code. It handles:
- Line length normalisation (default 88 characters)
- Quote normalisation (double quotes by default)
- Trailing comma handling
- Blank line normalisation

**Formatting is separate from linting**: `ruff check --fix` fixes lint rules; `ruff format` fixes style. Run both for a complete cleanup:

```bash
ruff check --fix . && ruff format .
```

This is the recommended default invocation — lint first, then format. The order matters because formatting after linting ensures the final output is consistently styled even when lint fixes change code structure.

---

### Understanding unfixable violations

After running `ruff check --fix .`, any remaining output represents violations that require manual attention:

```bash
ruff check .    # dry run: show all current violations without fixing
```

**Example output**:
```
src/main.py:42:5: E501 Line too long (96 > 88 characters)
src/utils.py:18:1: F841 Local variable `result` is assigned to but never used
tests/test_api.py:7:1: S101 Use of `assert` detected
```

**Reading the output**: `file:line:col: RULE-CODE message`

**Common unfixable rules**:

| Rule | Name | Fix |
|---|---|---|
| `E501` | Line too long | Manually break the line or raise `line-length` in config |
| `F841` | Unused variable | Remove or use the variable |
| `F811` | Redefinition of unused name | Remove duplicate definition |
| `S101` | Assert detected | Replace with proper exception in production code |
| `B006` | Mutable default argument | Use `None` default + `if arg is None: arg = []` pattern |
| `PLR0913` | Too many arguments | Refactor to use a dataclass or config object |

When unfixable violations are found, the skill shows the count, lists each with its rule code and location, and explains how to resolve the most common ones.

---

### Configuring ruff in pyproject.toml

If ruff is not yet configured in the project, add a `[tool.ruff]` section to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"    # match your Python version

[tool.ruff.lint]
select = ["E", "F", "I", "B", "S"]   # pycodestyle + pyflakes + isort + bugbear + bandit
ignore = ["S101"]                      # ignore assert in tests

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101", "PLR2004"]  # allow assert and magic values in tests
```

**Alternatively**, use a standalone `ruff.toml` at the project root (same format, without `[tool.ruff]` prefix):

```toml
line-length = 88
target-version = "py311"

[lint]
select = ["E", "F", "I"]
```

**Rule set guidance**:

| Code | Ruleset | Replaces |
|---|---|---|
| `E`, `W` | pycodestyle | flake8 E/W |
| `F` | pyflakes | flake8 F |
| `I` | isort | isort |
| `B` | flake8-bugbear | flake8-bugbear |
| `S` | flake8-bandit | bandit |
| `UP` | pyupgrade | pyupgrade |
| `RUF` | ruff-specific | — |

Start with `["E", "F", "I"]` as a minimal set and add more as your project adopts stricter standards.

---

## Tips for Success

1. **Run `ruff check --fix . && ruff format .` as your standard cleanup** — this covers both lint and format in one pass. Alias it or add it to a Makefile target.

2. **Dry run before fixing**: `ruff check .` (no `--fix`) shows all violations without modifying files — useful to understand the scope before applying changes.

3. **ruff replaces multiple tools** — ruff covers flake8, isort, pyupgrade, and parts of pylint. If you're migrating, you can remove those tools from `pyproject.toml` dev dependencies once ruff is configured.

4. **Add ruff to pre-commit**: ruff runs in milliseconds on large codebases, making it ideal for pre-commit hooks. The official hooks are available at `github.com/astral-sh/ruff-pre-commit`.

5. **CI auto-patch**: In CI, run `ruff check --fix . && ruff format . && git diff --exit-code` to fail the build if unfixed violations or unformatted files are committed.

6. **Check ruff is installed**: `ruff --version`. Install with `pip install ruff`, `uv add --dev ruff`, or `brew install ruff`.

7. **`E501` (line too long) is often not worth fixing manually** — consider raising `line-length` in `[tool.ruff]` to 100 or 120 if your codebase has many long lines and reformatting isn't feasible.
