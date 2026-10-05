---
name: code-quality
description: Linting, formatting, and encoding standards for the AegisNex codebase. Covers ruff, mypy, eslint, editorconfig, pre-commit hooks, and how to add new quality checks.
license: Complete terms in LICENSE.txt
---

# Code Quality

You are the code quality enforcer for AegisNex. You ensure that every file committed to the repo meets the project's standards for formatting, type safety, and encoding. You know that consistent code is easier to review, debug, and maintain.

## Encoding standards

### File encoding

All text files must be UTF-8 without BOM. The repo enforces this via:

- `.editorconfig`: `charset = utf-8` for all files
- `.gitattributes`: `* text=auto eol=lf` for line ending normalization

**Never add a BOM to any file.** If you encounter a file with BOM (`\xef\xbb\xbf` at the start), rewrite it without BOM.

### Line endings

All files use LF (`\n`), not CRLF (`\r\n`). The `.gitattributes` file normalizes this on commit. If you are on Windows, your editor should handle this automatically via `.editorconfig`.

### Verify encoding

Check for BOM:
```python
with open("filename", "rb") as f:
    has_bom = f.read(3) == b"\xef\xbb\xbf"
```

Check line endings:
```python
with open("filename", "rb") as f:
    content = f.read()
    has_crlf = b"\r\n" in content
```

## Python quality (ruff + mypy)

### Ruff (linting + formatting)

Ruff is the primary Python linter and formatter. Configuration is in `pyproject.toml` or `ruff.toml` (if present), or use defaults.

**Run locally:**
```bash
ruff check src/ tests/        # lint
ruff format src/ tests/       # format
ruff check --fix src/         # auto-fix
```

**Common ruff rules to follow:**
- `E`: pycodestyle errors (indentation, line length)
- `F`: pyflakes (unused imports, undefined names)
- `I`: isort (import sorting)
- `W`: pycodestyle warnings
- `B`: flake8-bugbear (common bugs)

**Import ordering:** Use `isort` convention (built-in -> third-party -> local). Ruff handles this with the `I` rule.

### Mypy (type checking)

Mypy checks type annotations. Run with:
```bash
mypy src/ --ignore-missing-imports
```

**Common mypy patterns in AegisNex:**
- `Optional[X]` for nullable fields
- `Dict[str, Any]` for loosely-typed data (tool results, API responses)
- `TypedDict` for structured dicts (`AgentState`, `AgentStep`)
- `# type: ignore[assignment]` only with an explanation comment

### Adding a new linting rule

1. Add the rule to ruff config (`pyproject.toml` or `ruff.toml`)
2. Run `ruff check src/` to find violations
3. Auto-fix what you can: `ruff check --fix src/`
4. Fix remaining violations manually
5. Add the check to CI pipeline

## TypeScript/Frontend quality (eslint + prettier)

### ESLint

The frontend uses ESLint with Next.js config. Run:
```bash
cd frontend && npm run lint
```

### Prettier

For consistent formatting:
```bash
cd frontend && npx prettier --write .
```

## Pre-commit hooks

Pre-commit hooks run automatically before each commit. If the repo has a `.pre-commit-config.yaml`:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files    # run on all files
```

**If pre-commit fails:**
1. Read the error output
2. Fix the issues (pre-commit usually tells you which files)
3. `git add` the fixed files
4. `git commit` again

## Adding a new quality check

### Adding a new ruff rule

1. Edit `pyproject.toml`:
```toml
[tool.ruff.lint]
select = ["E", "F", "I", "W", "B", "NEW_RULE"]
```
2. Run `ruff check src/` to find violations
3. Auto-fix: `ruff check --fix src/`
4. Commit the config change and fixes

### Adding a new mypy strict check

1. Edit `pyproject.toml`:
```toml
[tool.mypy]
strict = true
```
2. Run `mypy src/` to find violations
3. Fix type annotations
4. Commit

### Adding a CI quality step

Add to `.github/workflows/pipeline.yml`:
```yaml
- name: Lint
  run: |
    pip install ruff
    ruff check src/

- name: Type check
  run: |
    pip install mypy
    mypy src/ --ignore-missing-imports
```

## File-specific rules

### Python files (*.py)
- 4-space indentation
- LF line endings
- UTF-8 without BOM
- Max line length: 88 (ruff default) or 120 (if configured)
- Trailing newline at end of file

### Config files (*.ini, *.cfg, *.toml, *.yaml, *.yml)
- 2-space indentation
- LF line endings
- UTF-8 without BOM

### TypeScript/JavaScript (*.ts, *.tsx, *.js, *.jsx)
- 2-space indentation
- LF line endings
- UTF-8 without BOM
- Semicolons (if using prettier default)

### Markdown (*.md)
- LF line endings
- UTF-8 without BOM
- Trailing whitespace is preserved (for line breaks)
- Blank line between paragraphs