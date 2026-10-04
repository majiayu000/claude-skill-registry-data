---
name: code-qc
description: Run a structured quality control audit on any codebase. Use when asked to QC, audit, review, or check code quality for a project. Supports Python, TypeScript, GDScript, and general projects. Produces a standardized report with PASS/WARN/FAIL verdict, covering tests, imports, type checking, static analysis, smoke tests, and documentation. Also use when asked to compare QC results over time.
---

# Code QC

Structured quality control audit for codebases. Delegates static analysis to proper tools (ruff, eslint, gdlint) and focuses on what AI adds: semantic understanding, cross-module consistency, and dynamic smoke test generation.

## Quick Start

1. Detect project type (read the profile for that language)
2. Load `.qc-config.yaml` if present (for custom thresholds/exclusions)
3. Run the 8-phase audit (or subset with `--quick`)
4. Generate report with verdict
5. Save baseline for future comparison

## Configuration (`.qc-config.yaml`)

Optional project-level config for monorepos and custom settings:

```yaml
# .qc-config.yaml
thresholds:
  test_failure_rate: 0.05    # >5% = FAIL, 0-5% = WARN, 0% = PASS
  lint_errors_max: 0         # Max lint errors before FAIL
  lint_warnings_max: 50      # Max warnings before WARN
  type_errors_max: 0         # Max type errors before FAIL (strict by default)

exclude:
  dirs: [vendor, third_party, generated]
  files: ["*_generated.py", "*.pb.go"]

changed_only: false          # Only check git-changed files (CI mode)
fail_fast: false             # Stop on first failure
quick_mode: false            # Only run Phase 1, 3, 3.5, 6

languages:
  python:
    min_coverage: 80
    ignore_rules: [T201]     # Allow print in this project
  typescript:
    strict_mode: true        # Require tsconfig strict: true
    ignore_rules: []         # eslint rules to ignore
  gdscript:
    godot_version: "4.2"
```

## Execution Modes

| Mode | Phases Run | Use Case |
|------|------------|----------|
| Full (default) | All 8 phases | Thorough audit |
| `--quick` | 1, 3, 3.5, 6 | Fast sanity check |
| `--changed-only` | All, filtered | CI on pull requests |
| `--fail-fast` | All, stops early | Find first issue fast |
| `--fix` | 3 with autofix | Apply automatic fixes |

## Phase Overview

| # | Phase | What | Tools |
|---|-------|------|-------|
| 1 | Test Suite | Run existing tests + coverage | pytest --cov / jest --coverage |
| 2 | Import Integrity | Verify all modules load | `scripts/import_check.py` |
| 3 | Static Analysis | Lint with proper tools | ruff / eslint / gdlint |
| 3.5 | Type Checking | Static type verification | mypy / tsc --noEmit / (N/A for GDScript) |
| 4 | Smoke Tests | Verify business logic works | AI-generated per project |
| 5 | UI/Frontend | Verify UI components load | Framework-specific |
| 6 | File Consistency | Syntax + git state | `scripts/syntax_check.py` + git |
| 7 | Documentation | Docstrings + docs accuracy | `scripts/docstring_check.py` |

## Phase Details

### Phase 1: Test Suite

Run the project's test suite with coverage. Auto-detect the test runner:

```
pytest.ini / pyproject.toml [tool.pytest] → pytest --cov
package.json scripts.test → npm test (or npx vitest --coverage)
Cargo.toml → cargo test
project.godot → (GUT if present, else manual)
```

**Record:** total, passed, failed, errors, skipped, duration, coverage %.

**Verdict contribution:**
- No tests found → **SKIP** (not FAIL; project may be config-only)
- Failure rate = 0% → **PASS**
- Failure rate ≤ threshold (default 5%) → **WARN**
- Failure rate > threshold → **FAIL**

**Coverage reporting (Python):**
```bash
pytest --cov=<package> --cov-report=term-missing --cov-report=json
```

### Phase 2: Import Integrity (Python/GDScript)

**Python:** Run `scripts/import_check.py` against the project root.

**GDScript:** Verify scene/preload references are valid (see gdscript-profile.md).

#### Critical vs Optional Import Classification

Use these heuristics to classify import failures:

| Pattern | Classification | Rationale |
|---------|---------------|-----------|
| `__init__.py`, `main.py`, `app.py`, `cli.py` | **Critical** | Core entry points |
| Module in `src/`, `lib/`, or top-level package | **Critical** | Core functionality |
| `*_test.py`, `test_*.py`, `conftest.py` | **Optional** | Test infrastructure |
| Modules in `examples/`, `scripts/`, `tools/` | **Optional** | Auxiliary code |
| Import error mentions `cuml`, `triton`, `tensorrt` | **Optional** | Hardware-specific |
| Import error mentions missing system lib | **Optional** | Environment-specific |
| Dependency in `[project.optional-dependencies]` | **Optional** | Declared optional |

### Phase 3: Static Analysis

**Do NOT use grep.** Use the language's standard linter.

#### Standard Mode
```bash
# Python
ruff check --select E722,T201,B006,F401,F841,UP,I --statistics <project>

# TypeScript  
npx eslint . --format json

# GDScript
gdlint <project>
```

#### Fix Mode (`--fix`)
When `--fix` is specified, apply automatic corrections:

```bash
# Python — safe auto-fixes
ruff check --fix --select E,F,I,UP <project>
ruff format <project>

# TypeScript
npx eslint . --fix

# GDScript
gdformat <project>
```

**Important:** After `--fix`, re-run the check to report remaining issues that couldn't be auto-fixed.

### Phase 3.5: Type Checking (NEW)

Run static type analysis before proceeding to runtime checks.

**Python:**
```bash
mypy <package> --ignore-missing-imports --no-error-summary
# or if pyproject.toml has [tool.pyright]:
pyright <package>
```

**TypeScript:**
```bash
npx tsc --noEmit
```

**GDScript:** Godot 4 has built-in static typing but no standalone checker. Estimate type coverage manually:

```bash
# Find untyped declarations
grep -rn "var \w\+ =" --include="*.gd" .       # Untyped variables
grep -rn "func \w\+(" --include="*.gd" . | grep -v ":"  # Untyped functions
```

Use the `estimate_type_coverage()` function from `gdscript-profile.md` to calculate coverage per file:
```python
# From gdscript-profile.md
def estimate_type_coverage(gd_file: str) -> float:
    """Count typed vs untyped declarations."""
    # See full implementation in gdscript-profile.md
```

Also check for `@warning_ignore` annotations which may hide type issues.

**Record:** Total errors, categorized by severity.

### Phase 4: Smoke Tests (Business Logic)

Test **backend/core functionality** — NOT UI components (that's Phase 5).

**API Discovery Heuristics:**

1. **Entry points:** Look for `main()`, `cli()`, `app`, `create_app()`, `__main__.py`
2. **Service layer:** Find classes/modules named `*Service`, `*Manager`, `*Handler`  
3. **Public API:** Check `__all__` exports in `__init__.py`
4. **FastAPI/Flask:** Find route decorators (`@app.get`, `@router.post`)
5. **CLI:** Find typer/click `@app.command()` decorators
6. **SDK:** Look for client classes, public methods without `_` prefix

**For each discovered API, generate a minimal test:**
```python
def smoke_test_user_service():
    """Test UserService basic CRUD."""
    from myproject.services.user import UserService
    svc = UserService(db=":memory:")
    user = svc.create(name="test")
    assert user.id is not None
    fetched = svc.get(user.id)
    assert fetched.name == "test"
    return "PASS"
```

**Guidelines:**
- Import + instantiate + call one method with minimal valid input
- Use in-memory/temp resources (`:memory:`, `tempdir`)
- Each test < 5 seconds
- Catch exceptions, report clearly

### Phase 5: UI/Frontend Verification

Test **UI components** separately from business logic.

| Framework | Test Method |
|-----------|-------------|
| **Gradio** | `from project.ui import create_ui` (no `launch()`) |
| **Streamlit** | `streamlit run app.py --headless` exits cleanly |
| **PyQt/PySide** | Set `QT_QPA_PLATFORM=offscreen`, import widget modules |
| **React** | `npm run build` succeeds |
| **Vue** | `npm run build` succeeds |
| **Godot** | Scene files parse without error, required scripts exist |
| **CLI** | `--help` on all subcommands returns 0 |

**Boundary:** Phase 4 tests "does the logic work?" Phase 5 tests "does the UI render?"

### Phase 6: File Consistency

Run `scripts/syntax_check.py` — compiles all source files to verify no syntax errors.

> **Note:** Phase 2 (Import Integrity) tests *runtime* import behavior including initialization code. Phase 6 tests *static* syntax correctness. Both are needed: a file can have valid syntax but fail to import (e.g., missing dependency), or vice versa (syntax error in a module that's never imported).

Check git state:
```bash
git status --short      # Should be clean (or report uncommitted changes)
git diff --check        # No conflict markers
```

### Phase 7: Documentation

Run `scripts/docstring_check.py` (now checks `__init__.py` by default).

Also verify:
- README exists and is non-empty
- Key docs (CHANGELOG, CONTRIBUTING) exist if referenced
- No stale TODO markers in docs claiming completion

## Verdict Logic

```
# Calculate test failure rate
failure_rate = test_failures / total_tests

# Default thresholds (override in .qc-config.yaml)
FAIL_THRESHOLD = 0.05  # 5%
WARN_THRESHOLD = 0.00  # 0%
TYPE_ERRORS_MAX = 0    # Default: strict (any type error = FAIL)

# Verdict determination
if any([
    failure_rate > FAIL_THRESHOLD,
    critical_import_failure,
    type_check_errors > thresholds.type_errors_max,  # Configurable threshold
    lint_errors > thresholds.lint_errors_max,
]):
    verdict = "FAIL"
elif any([
    0 < failure_rate <= FAIL_THRESHOLD,
    optional_import_failures > 0,
    lint_warnings > thresholds.lint_warnings_max,
    missing_docstrings > 0,
    smoke_test_failures > 0,
]):
    verdict = "PASS WITH WARNINGS"
else:
    verdict = "PASS"
```

## Baseline Comparison

Save results to `.qc-baseline.json`:

```json
{
  "timestamp": "2026-02-15T15:00:00Z",
  "commit": "abc123",
  "verdict": "PASS WITH WARNINGS",
  "config": {
    "mode": "full",
    "thresholds": {"test_failure_rate": 0.05}
  },
  "phases": {
    "tests": {"total": 134, "passed": 134, "failed": 0, "coverage": 87.5},
    "imports": {"total": 50, "failed": 0, "optional_failed": 1, "critical_failed": 0},
    "types": {"errors": 0, "warnings": 5},
    "lint": {"errors": 0, "warnings": 12, "fixed": 8},
    "smoke": {"total": 14, "passed": 14},
    "docs": {"missing_docstrings": 3}
  }
}
```

On subsequent runs, report delta:
```
Tests:      134 → 140 (+6 ✅)
Coverage:   87% → 91% (+4% ✅)
Type errors: 0 → 0 (✅)
Lint warnings: 12 → 5 (-7 ✅)
```

## Report Output

Generate in 3 formats:
1. **Markdown** (`qc-report.md`) — full detailed report for humans
2. **JSON** (`.qc-baseline.json`) — machine-readable for CI/comparison
3. **Summary** (chat message) — 10-line digest for Discord/Slack

### Summary Format Example

```
📊 QC Report: my-project @ abc123
Verdict: ✅ PASS WITH WARNINGS

Tests:    134/134 passed (100%) | Coverage: 87%
Types:    0 errors
Lint:     0 errors, 12 warnings
Imports:  50/50 (1 optional failed)
Smoke:    14/14 passed

⚠️ Warnings:
- 3 missing docstrings
- 12 lint warnings (run with --fix)
```

## Language-Specific Profiles

Read the appropriate profile before running:
- **Python**: `references/python-profile.md`
- **TypeScript**: `references/typescript-profile.md`
- **GDScript**: `references/gdscript-profile.md`
- **General** (any language): `references/general-profile.md`
