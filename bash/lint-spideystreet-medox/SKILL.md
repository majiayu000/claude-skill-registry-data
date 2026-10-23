---
name: lint
description: Run all project linters (ruff, mypy, sqlfluff) and report results. Invoke with /lint.
disable-model-invocation: true
argument-hint: "[python|sql|all]"
---

# /lint

Run all project linters and report a unified summary.

## Linters

| Tool | Scope | What it checks |
|------|-------|----------------|
| `ruff check` | `src/` `scripts/` `tests/` | Python lint (E, F, I, UP) |
| `ruff format --check` | `src/` `scripts/` `tests/` | Python formatting |
| `mypy` | `src/` | Python type checking |
| `sqlfluff lint` | `dbt/models/` `dbt/tests/` | SQL style & conventions |

## Steps

1. **Parse argument** (optional)
   - `python` → run only ruff + mypy
   - `sql` → run only sqlfluff
   - `all` or no argument → run everything

2. **Run selected linters** — run all applicable commands in parallel:

   **Python linting (ruff check):**
   ```bash
   uv run ruff check src/ scripts/ tests/
   ```

   **Python formatting (ruff format):**
   ```bash
   uv run ruff format --check src/ scripts/ tests/
   ```

   **Python types (mypy):**
   ```bash
   uv run mypy src/
   ```

   **SQL linting (sqlfluff):**
   ```bash
   uv run sqlfluff lint dbt/models/ dbt/tests/ --config dbt/.sqlfluff
   ```

3. **Auto-fix** — if ruff or sqlfluff report fixable violations, ask the user:
   > "N fixable violations found. Apply auto-fix?"

   If yes:
   ```bash
   uv run ruff check --fix src/ scripts/ tests/
   uv run ruff format src/ scripts/ tests/
   uv run sqlfluff fix dbt/models/ dbt/tests/ --config dbt/.sqlfluff
   ```

4. **Report summary** — print a table like:

   ```
   Linter          Status   Issues
   ruff check      PASS     0
   ruff format     FAIL     3 files
   mypy            PASS     0
   sqlfluff        PASS     0
   ```

   Use PASS/FAIL per linter. If all pass, end with: `All linters passed.`
