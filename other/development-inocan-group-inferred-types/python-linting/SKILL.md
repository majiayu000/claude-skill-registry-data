---
name: python-linting
description: Python linting and type checking using ruff (formatting + linting) and pyright (type checking). Covers common errors, configuration, fixing violations, and when to use noqa. Use when fixing linting errors, configuring ruff/pyright, or understanding Python code quality tools.
allowed-tools:
  - Read
  - Bash
---

# Python Linting & Type Checking

## The Modern Python Tooling Stack (2025)

### Two Tools You Need

| Tool | Purpose | Speed | What It Catches |
|------|---------|-------|-----------------|
| **Ruff** | Linter + Formatter | ⚡ <100ms | Style, imports, simple bugs, patterns |
| **Pyright** | Type Checker | 🏃 1-2s | Type safety, attribute errors, None-safety |

**Ruff replaces:** pylint, black, isort, flake8, pycodestyle, pydocstyle
**Pyright replaces:** mypy (faster, better errors)

---

## What Each Tool Catches

### Ruff (Linter + Formatter)

**Style Issues:**
- Line length violations (80 char default)
- Import sorting (PEP 8 order)
- Naming conventions (snake_case, PascalCase)
- Whitespace, indentation

**Simple Bugs:**
- Unused imports, variables, functions
- Undefined names (F821)
- Syntax errors

**Code Patterns:**
- Complexity warnings (PLR0912 - too many branches)
- Code simplifications (SIM rules)
- Security patterns (SQL injection, shell injection)

**Ruff CANNOT catch:**
- Type mismatches
- Missing attributes/methods
- Wrong function arguments
- None-safety violations

### Pyright (Type Checker)

**Type Safety:**
- Type mismatches: `dict[str, Any]` passed where `str` expected
- Return type errors
- Parameter type errors

**Attribute/Method Errors:**
- Missing attributes: `obj.nonexistent_attr`
- Wrong method names: `cache.lookup_asset_by_id()` doesn't exist
- Missing methods on class

**Function Signature Errors:**
- Missing required parameters
- Wrong parameter types
- Extra parameters passed

**None-Safety:**
- `dict | None` passed where `dict` required
- Potential None-pointer errors

**Pyright CANNOT catch:**
- Style violations
- Import sorting
- Code formatting

---

## Usage

### Development Workflow

```bash
# 1. Fast feedback (run constantly)
ruff check --fix .    # Lint + auto-fix (instant)
ruff format .         # Format code (instant)

# 2. Before commit (thorough check)
pyright .            # Type check (1-2s)
pytest               # Run tests
```

### Command Reference

#### Ruff Commands
```bash
# Check for issues
ruff check .
ruff check path/to/file.py

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
ruff format path/to/file.py

# Check formatting without changing
ruff format --check .

# Show what's wrong
ruff check --output-format=full
```

#### Pyright Commands
```bash
# Check entire project
pyright .

# Check specific file
pyright path/to/file.py

# Check with different strictness
pyright --level basic .
pyright --level standard .
pyright --level strict .

# Watch mode (for development)
pyright --watch
```

---

## Configuration

### Ruff Config (`ruff.toml` or `pyproject.toml`)

**Minimal config:**
```toml
# ruff.toml
line-length = 80
target-version = "py311"

[lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "PLR", # pylint refactor
]
ignore = []

[format]
quote-style = "single"
indent-style = "space"
```

**Fallback config:** `~/.claude/configs/ruff.toml` (if project doesn't have ruff.toml)

### Pyright Config (`pyrightconfig.json`)

**Minimal config:**
```json
{
  "include": ["src", "fisio"],
  "exclude": ["**/node_modules", "**/__pycache__", ".venv"],
  "typeCheckingMode": "basic",
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "pythonVersion": "3.11"
}
```

**Fallback config:** `~/.claude/configs/pyrightconfig.json` (if project doesn't have pyrightconfig.json)

---

## Common Patterns

### Fixing Type Errors

**Problem:** `dict[str, Any] | Any` passed where `str` expected
```python
# Bad
option_id = get_from_dict(obj, 'id')
result = function(option_id)  # Type error!
```

**Fix:** Cast to string
```python
# Good
option_id = get_from_dict(obj, 'id')
result = function(str(option_id))
```

**Problem:** Calling non-existent method
```python
# Bad (pyright error: method doesn't exist)
asset = self.cache.lookup_asset_by_id(asset_id)
```

**Fix:** Use correct method name
```python
# Good (check actual class definition)
asset = self.cache.lookup_and_parse('assets', '_id', asset_id)
```

**Problem:** None-safety violation
```python
# Bad (value could be None)
def process(data: dict | None):
    return len(data)  # Type error!
```

**Fix:** Handle None case
```python
# Good
def process(data: dict | None):
    return len(data or {})
```

### Suppressing Warnings

**Ruff suppressions:**
```python
# Suppress specific rule for one line
x = very_long_expression  # noqa: E501

# Suppress for entire file
# ruff: noqa: E501

# Suppress with explanation (preferred)
def complex_function():  # noqa: PLR0912
    # WHY: Business logic requires 15 branches for state machine
    pass
```

**Pyright suppressions:**
```python
# Suppress type error for one expression
db = None  # type: ignore[arg-type]

# Suppress specific error type
value: str = get_value()  # type: ignore[assignment]
```

**WHY comment required:** Always explain suppressions - future you needs to know why.

---

## CI/CD Integration

```yaml
# .github/workflows/lint.yml
steps:
  - name: Lint with Ruff
    run: ruff check .

  - name: Format check
    run: ruff format --check .

  - name: Type check with Pyright
    run: pyright .
```

**Time:** ~2-5 seconds total (vs 20-60s with old tools)

---

## Migration Guide

### From pylint to ruff

**Old:**
```bash
pylint --rcfile=pylintrc.toml src/
```

**New:**
```bash
ruff check src/
```

**Config migration:**
- Most pylint rules have ruff equivalents
- Check ruff docs for rule mapping: https://docs.astral.sh/ruff/rules/

### From mypy to pyright

**Old:**
```bash
mypy --config-file=mypy.ini src/
```

**New:**
```bash
pyright src/
```

**Config migration:**
```python
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True

# pyrightconfig.json (equivalent)
{
  "pythonVersion": "3.11",
  "reportAny": true,
  "reportUnusedVariable": true
}
```

---

## Troubleshooting

### Ruff Issues

**Problem:** "All checks passed" but code still has issues
**Solution:** Ruff only does linting, not type checking. Run pyright for type errors.

**Problem:** Too many errors to fix
**Solution:** `ruff check --fix .` auto-fixes most issues.

**Problem:** Import sorting conflicts
**Solution:** Ruff handles this automatically, just run `ruff format`.

### Pyright Issues

**Problem:** "Cannot find implementation" errors for external modules
**Solution:** These are expected if modules don't have type stubs. Ignore them.

**Problem:** False positives on dynamic code
**Solution:** Use `# type: ignore` with explanation.

**Problem:** Too strict
**Solution:** Use `"typeCheckingMode": "basic"` instead of "strict".

---

## Speed Comparison

**Your codebase:**
```
Ruff:    0.017s (17ms)   ⚡ Instant
Pyright: 1.289s (1.3s)   🏃 Fast enough
```

**Old tools (removed):**
```
Pylint:  10-30s  🐌 Replaced by ruff
Mypy:    5-10s   🐌 Replaced by pyright
Black:   2-3s    🐌 Replaced by ruff format
Isort:   1-2s    🐌 Replaced by ruff
```

**Total improvement:** 20-40x faster

---

## Remember

1. **Ruff is NOT a type checker** - it catches style and simple bugs
2. **Pyright is NOT a linter** - it catches type errors
3. **You need BOTH** - they're complementary, not redundant
4. **Ruff runs first** - fix style issues before type checking
5. **Pyright is thorough** - catches bugs ruff can't

---

## When in Doubt

**"My IDE shows an error but ruff doesn't catch it"**
→ That's a type error. Run pyright.

**"Pyright passes but code looks messy"**
→ That's a style issue. Run ruff format.

**"Should I keep pylint/mypy?"**
→ No. Ruff and pyright replace them completely.
