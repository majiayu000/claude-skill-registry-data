---
name: python-cleanup
description: Perform comprehensive dead code and clean-up analysis in Python projects using static analysis, coverage, dependency checks, and security scanning. Use when asked to clean up code, find unused code, analyze dependencies, or improve code quality.
---

# Python Dead Code & Clean-Up Analysis

This skill provides a comprehensive toolkit for analyzing and cleaning up Python codebases, going far beyond basic linting to identify dead code, unused dependencies, security issues, and modernization opportunities.

## Overview

This skill combines multiple tools into a phased approach for code clean-up:

1. **Dead Code Detection** - Find unused functions, variables, imports
2. **Dependency Analysis** - Detect unused/undeclared/misplaced dependencies
3. **Coverage Analysis** - Identify code never executed by tests
4. **Linting & Modernization** - Update syntax, fix style issues
5. **Security Scanning** - Find vulnerabilities and secrets
6. **Complexity Analysis** - Identify overly complex code
7. **Project Hygiene** - Clean build artifacts and temp files

## Quick Start

### Phase 1: Quick Sweep (5 minutes)

Run these commands to get an overview of issues:

```bash
# 1. Quick linting and formatting (already in project)
uv run ruff check . --statistics

# 2. Dead code detection (high confidence only)
uv run vulture src tests --min-confidence 80

# 3. Unused imports check
uv run ruff check . --select F401 --select F841

# 4. Check for unused dependencies
uv run deptry .

# 5. Security scan
uv run bandit -r src -f screen --severity-level medium
```

### Phase 2: Deep Analysis (15-30 minutes)

For thorough analysis when you have more time:

```bash
# 1. Full coverage report (find untested code)
uv run pytest --cov=src --cov-branch --cov-report=html --cov-report=term-missing

# 2. Complexity analysis
uv run radon cc src -s -n B  # Show functions with complexity >= B

# 3. Dead code with lower confidence threshold
uv run vulture src tests --min-confidence 60 --sort-by-size

# 4. Type checking coverage
uv run mypy src --html-report mypy-report

# 5. Full security audit
uv run pip-audit  # Check for vulnerable dependencies
```

### Phase 3: Automated Fixes (with human review)

Tools that can automatically fix issues (always review changes before committing):

```bash
# 1. Auto-fix linting issues
uv run ruff check . --fix

# 2. Format code
uv run ruff format .

# 3. Upgrade to modern syntax (Python 3.12+)
uv run pyupgrade --py312-plus $(git ls-files '*.py')

# 4. Remove unused imports (CAUTION: review before committing)
uv run autoflake -r --in-place --remove-all-unused-imports --remove-unused-variables src

# 5. Clean build artifacts
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
```

## Detailed Tool Guide

### 1. Dead Code Detection

#### Vulture - Static Analysis for Unreachable Code

**What it finds:**
- Unused functions, methods, classes
- Unused variables
- Unreachable code after returns/breaks

**Usage:**
```bash
# High confidence only (fewer false positives)
uv run vulture src tests --min-confidence 80

# Show all potential issues
uv run vulture src tests --min-confidence 60

# Sort by file size (tackle big wins first)
uv run vulture src tests --min-confidence 80 --sort-by-size
```

**Interpreting results:**
- 80-100% confidence: Usually safe to remove
- 60-79% confidence: Review carefully (may be used dynamically)
- <60%: Often false positives (skip these)

**Common false positives:**
- Pydantic model fields (used by framework)
- FastAPI route handlers (called by framework)
- Test fixtures (used by pytest)
- Agent tools (registered in ToolRegistry)
- Abstract methods in base classes

**Create whitelist for false positives:**
```python
# vulture_whitelist.py
# This file tells Vulture about intentional "unused" code

_.field_name  # Pydantic field used by model
MyClass.abstract_method  # Used by subclasses
test_fixture  # pytest fixture
```

Then run: `uv run vulture src tests vulture_whitelist.py --min-confidence 80`

#### Coverage.py - Dynamic Analysis (Most Reliable)

**Why it's better:** Shows code that's *actually* never executed in tests, not just statically unreachable.

**Usage:**
```bash
# Run tests with coverage tracking
uv run pytest --cov=src --cov-branch --cov-report=html --cov-report=term-missing

# View detailed HTML report
open htmlcov/index.html  # or: xdg-open htmlcov/index.html

# Find files with <80% coverage
uv run pytest --cov=src --cov-fail-under=80
```

**Interpreting results:**
- Red lines in HTML report = never executed
- Yellow bars = branch not taken (if/else, match/case)
- Green = fully covered

**Workflow:**
1. Run coverage report
2. Find red lines (0% coverage)
3. Ask: "Is this intentionally unused?" (maybe old feature)
4. If yes, consider removing
5. If no, add tests

### 2. Dependency Analysis

#### deptry - Unused/Undeclared Dependencies

**What it finds:**
- Dependencies in `pyproject.toml` but never imported (unused)
- Imports used in code but not declared (undeclared)
- Development dependencies used in production code (misplaced)

**Usage:**
```bash
# Check all dependencies
uv run deptry .

# Ignore specific imports (e.g., conditional imports)
uv run deptry . --ignore-obsolete DEP1,DEP2

# Generate report
uv run deptry . --json-output deptry-report.json
```

**Common issues found:**
- Leftover dependencies from removed features
- Transitive dependencies you're using directly (should declare explicitly)
- Dev tools accidentally imported in production code

**Fix workflow:**
1. Run `deptry .`
2. For **unused**: Remove from `pyproject.toml` with `uv remove package-name`
3. For **undeclared**: Add with `uv add package-name`
4. For **misplaced**: Move to correct dependency group in `pyproject.toml`

#### pip-audit / safety - Vulnerable Dependencies

**Usage:**
```bash
# Check for known vulnerabilities (recommended)
uv run pip-audit

# Show only high severity
uv run pip-audit --severity high

# Generate report
uv run pip-audit --format json > security-audit.json
```

**Action items:**
- **HIGH/CRITICAL**: Upgrade immediately
- **MEDIUM**: Schedule upgrade in next sprint
- **LOW**: Upgrade when convenient

### 3. Linting & Modernization

#### Ruff - Fast Linter & Formatter

**What it does:** Replaces Flake8, isort, pyupgrade, and more with a single fast tool.

**Usage:**
```bash
# Check for issues
uv run ruff check .

# Auto-fix safe issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Show statistics
uv run ruff check . --statistics

# Check specific rules
uv run ruff check . --select F401  # unused imports
uv run ruff check . --select BLE001  # blind exception catches
```

**Already configured in this project:** See `pyproject.toml` for project-specific rules (110 char line length, etc.)

#### pyupgrade - Modern Python Syntax

**What it does:** Automatically upgrades code to use modern Python features (f-strings, type hints, walrus operator, etc.)

**Usage:**
```bash
# Upgrade all Python files to 3.12+ syntax
uv run pyupgrade --py312-plus $(git ls-files '*.py')

# Preview changes without modifying files
uv run pyupgrade --py312-plus --diff file.py
```

**Examples of upgrades:**
```python
# Before
"{0} {1}".format(a, b)
dict(a=1, b=2)

# After (automatically converted)
f"{a} {b}"
{"a": 1, "b": 2}
```

#### autoflake / unimport - Remove Unused Imports

**CAUTION:** These tools can be aggressive. Always review changes before committing.

**Usage:**
```bash
# Preview changes (safe)
uv run autoflake -r --remove-all-unused-imports --remove-unused-variables src

# Apply changes (review with git diff after)
uv run autoflake -r --in-place --remove-all-unused-imports --remove-unused-variables src

# Alternative: unimport
uv run unimport --check --diff .
uv run unimport --remove .
```

**When to skip:**
- Imports used for side effects (e.g., `import monkey_patch_module`)
- Imports required for type checking (`from typing import TYPE_CHECKING`)
- Star imports that bring in many names (`from module import *`)

### 4. Type Checking

#### mypy / pyright - Static Type Analysis

**What it finds:**
- Type errors and inconsistencies
- Uncovered code (no type hints)
- Type: ignore comments (may indicate unused code)

**Usage:**
```bash
# Run mypy (already configured in project)
uv run mypy src

# Generate HTML report with coverage
uv run mypy src --html-report mypy-report
open mypy-report/index.html

# Check for type coverage
uv run mypy src --html-report mypy-report | grep "covered"
```

**Interpreting results:**
- Red in HTML report = no type hints
- Green = fully typed
- Aim for >80% type coverage in new code

### 5. Security Scanning

#### bandit - Static Security Analysis

**What it finds:**
- SQL injection vulnerabilities
- Command injection
- Unsafe YAML loading
- Hard-coded passwords
- Insecure random number generation

**Usage:**
```bash
# Scan with medium+ severity
uv run bandit -r src -f screen --severity-level medium

# Show only high severity issues
uv run bandit -r src --severity-level high

# Generate JSON report
uv run bandit -r src -f json -o bandit-report.json

# Skip specific tests (if false positives)
uv run bandit -r src --skip B101,B601
```

**Common issues:**
- `B101`: Use of `assert` in production code
- `B110`: Try/except pass (swallowing errors)
- `B605`: Shell injection vulnerabilities
- `B608`: SQL injection risks

#### detect-secrets - Credential Scanning

**Usage:**
```bash
# Scan for secrets in code
uv run detect-secrets scan > .secrets.baseline

# Audit findings
uv run detect-secrets audit .secrets.baseline

# Check new changes only
uv run detect-secrets-hook $(git diff --name-only)
```

**What it catches:**
- API keys
- Private keys
- Passwords in code
- AWS credentials
- Database connection strings

### 6. Complexity Analysis

#### radon - Cyclomatic Complexity

**What it measures:** How many independent paths exist through code (higher = harder to test/maintain).

**Usage:**
```bash
# Show functions with complexity >= B (moderate)
uv run radon cc src -s -n B

# Show all complexity scores
uv run radon cc src -s -a

# Show maintainability index
uv run radon mi src -s
```

**Complexity grades:**
- **A (1-5)**: Simple, easy to test
- **B (6-10)**: Moderate complexity, acceptable
- **C (11-20)**: High complexity, consider refactoring
- **D (21-30)**: Very high, needs refactoring
- **E (31-40)**: Extremely high, refactor urgently
- **F (41+)**: Unmaintainable, rewrite

**Action items:**
- A-B: No action needed
- C: Add tests, consider simplifying
- D+: Refactor (break into smaller functions)

#### xenon - Complexity Enforcement

**Usage:**
```bash
# Fail if any function has complexity >= C
uv run xenon --max-absolute B --max-modules B --max-average A src

# Show violations
uv run xenon --max-absolute C src
```

**Integrate into CI:**
```yaml
# .github/workflows/ci.yml
- name: Check code complexity
  run: uv run xenon --max-absolute B src
```

### 7. Project Hygiene

#### Clean Build Artifacts

**Usage:**
```bash
# Remove all Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Remove test/coverage artifacts
rm -rf .pytest_cache htmlcov .coverage

# Remove mypy cache
rm -rf .mypy_cache

# Remove build artifacts
rm -rf build dist
```

#### Clean Unused Virtual Environments

**Usage:**
```bash
# Show UV cache size
uv cache dir
du -sh $(uv cache dir)

# Clean UV cache (safe - will redownload as needed)
uv cache clean
```

## Workflow Examples

### Example 1: Weekly Code Clean-Up

Run this weekly to keep codebase healthy:

```bash
# 1. Update dependencies
uv sync --upgrade

# 2. Check for vulnerabilities
uv run pip-audit

# 3. Run linting with auto-fix
uv run ruff check . --fix
uv run ruff format .

# 4. Check for unused dependencies
uv run deptry .

# 5. Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# 6. Check complexity
uv run radon cc src -s -n C  # Show high-complexity functions

# 7. Commit fixes
git add -A
git commit -m "chore: weekly code cleanup - linting, formatting, dependency updates"
```

### Example 2: Pre-Merge Checklist

Before merging a large feature branch:

```bash
# 1. Check for unused code added in this branch
git diff main...HEAD --name-only '*.py' | xargs uv run vulture --min-confidence 80

# 2. Verify all new dependencies are declared
uv run deptry .

# 3. Check test coverage of new code
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# 4. Ensure no new security issues
uv run bandit -r src --severity-level medium

# 5. Check type coverage
uv run mypy src

# 6. Format everything
uv run ruff format .
```

### Example 3: Deep Clean (After Removing Features)

When you've removed a major feature:

```bash
# 1. Find all dead code (low confidence threshold to catch everything)
uv run vulture src tests --min-confidence 60 | tee dead-code-report.txt

# 2. Run coverage to confirm it's never executed
uv run pytest --cov=src --cov-branch --cov-report=html

# 3. Check for unused dependencies
uv run deptry .

# 4. Remove unused imports
uv run autoflake -r --in-place --remove-all-unused-imports src

# 5. Check if any tests break
uv run pytest

# 6. Review all changes carefully
git diff

# 7. Commit if tests pass
git add -A
git commit -m "refactor: remove dead code after feature X removal"
```

### Example 4: Modernization Sprint

Upgrade entire codebase to modern Python:

```bash
# 1. Upgrade syntax to Python 3.12+
uv run pyupgrade --py312-plus $(git ls-files '*.py')

# 2. Fix linting issues created by upgrade
uv run ruff check . --fix

# 3. Format everything
uv run ruff format .

# 4. Run tests to ensure nothing broke
uv run pytest

# 5. Type check
uv run mypy src

# 6. Commit modernization
git add -A
git commit -m "refactor: modernize codebase to Python 3.12+ syntax"
```

## Integration with Pre-Commit Hooks

Add these checks to `.pre-commit-config.yaml` to run automatically on every commit:

```yaml
repos:
  # Fast linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Modern Python syntax
  - repo: https://github.com/asottile/pyupgrade
    rev: v3.19.0
    hooks:
      - id: pyupgrade
        args: [--py312-plus]

  # Remove unused imports
  - repo: https://github.com/PyCQA/autoflake
    rev: v2.3.1
    hooks:
      - id: autoflake
        args: [--remove-all-unused-imports, --in-place]

  # Dead code detection (high confidence only)
  - repo: https://github.com/jendrikseipp/vulture
    rev: 'v2.11'
    hooks:
      - id: vulture
        args: [src, tests, --min-confidence=80]

  # Dependency checks
  - repo: https://github.com/fpgmaas/deptry
    rev: '0.20.0'
    hooks:
      - id: deptry

  # Security scanning
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks:
      - id: bandit
        args: [-r, src, --severity-level, medium]

  # Secret detection
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]
```

Install and run:
```bash
# Install pre-commit
uv add --dev pre-commit

# Install hooks
uv run pre-commit install

# Run on all files
uv run pre-commit run --all-files
```

## CI/CD Integration

### GitHub Actions Workflow

Create `.github/workflows/code-quality.yml`:

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Lint
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy src

      - name: Dead code check
        run: uv run vulture src tests --min-confidence 80

      - name: Dependency check
        run: uv run deptry .

      - name: Security scan
        run: uv run bandit -r src --severity-level medium

      - name: Check for vulnerabilities
        run: uv run pip-audit

      - name: Run tests with coverage
        run: uv run pytest --cov=src --cov-fail-under=80

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

## Tool Installation

All tools mentioned in this skill can be installed with:

```bash
# Core tools (likely already installed in project)
uv add --dev ruff mypy pytest pytest-cov

# Dead code detection
uv add --dev vulture

# Dependency analysis
uv add --dev deptry pip-audit

# Modernization
uv add --dev pyupgrade autoflake

# Complexity analysis
uv add --dev radon xenon

# Security
uv add --dev bandit detect-secrets

# Pre-commit framework
uv add --dev pre-commit
```

Or install all at once:
```bash
uv add --dev ruff mypy pytest pytest-cov vulture deptry pip-audit pyupgrade autoflake radon xenon bandit detect-secrets pre-commit
```

## Project-Specific Configuration

### For Egregora (This Project)

**Already configured:**
- ✅ Ruff (linting + formatting) - see `pyproject.toml`
- ✅ mypy (type checking) - see `pyproject.toml`
- ✅ pytest (testing + coverage) - see `pyproject.toml`
- ✅ pre-commit hooks - run with `uv run pre-commit run --all-files`

**To add:**
```bash
# Install missing tools
uv add --dev vulture deptry pip-audit pyupgrade radon bandit

# Quick sweep
uv run vulture src tests --min-confidence 80
uv run deptry .
uv run bandit -r src --severity-level medium

# Deep analysis
uv run pytest --cov=egregora --cov-report=html --cov-report=term-missing
uv run radon cc src/egregora -s -n B
```

**Egregora-specific considerations:**
- **Privacy-first architecture**: Never use tools that upload code to external services
- **Pydantic-AI agent tools**: Vulture may flag these as unused (they're registered in ToolRegistry)
- **Pipeline stages**: Each stage should have >90% coverage (critical data flow)
- **TENET-BREAK comments**: Don't flag these as unused (they're documentation)
- **VCR cassettes**: Coverage may be lower in integration tests (that's OK, they use recorded responses)

## Decision Tree: Which Tool When?

### "I want to find unused code"
→ Start with **coverage.py** (most reliable): `pytest --cov=src --cov-report=html`
→ Then use **vulture** (catches more): `vulture src tests --min-confidence 80`

### "I want to check dependencies"
→ Use **deptry**: `deptry .`
→ Then **pip-audit**: `pip-audit`

### "I want to improve code quality"
→ Start with **ruff**: `ruff check . --fix && ruff format .`
→ Then **mypy**: `mypy src`
→ Then **radon**: `radon cc src -s -n C`

### "I want to modernize syntax"
→ Use **pyupgrade**: `pyupgrade --py312-plus $(git ls-files '*.py')`
→ Then **ruff** to clean up: `ruff check . --fix`

### "I want to check security"
→ Use **bandit**: `bandit -r src --severity-level medium`
→ Then **pip-audit**: `pip-audit`
→ Then **detect-secrets**: `detect-secrets scan`

### "I want everything (weekly clean-up)"
→ Run the comprehensive workflow in Example 1 above

## Best Practices

### 1. Always Review Automated Changes
- ✅ Run tools with `--diff` or `--check` first
- ✅ Review `git diff` carefully before committing
- ✅ Run tests after automated fixes
- ❌ Never blindly commit automated changes

### 2. Start Conservative, Get Aggressive
- ✅ Start with high confidence thresholds (Vulture: 80+)
- ✅ Review results carefully
- ✅ Create whitelists for false positives
- ✅ Lower thresholds once you trust the process

### 3. Combine Static + Dynamic Analysis
- ✅ Use both Vulture (static) and coverage (dynamic)
- ✅ Coverage is ground truth (if tests are comprehensive)
- ✅ Vulture catches things coverage misses (test coverage gaps)

### 4. Fix High-Impact Issues First
- ✅ Security vulnerabilities (bandit HIGH/CRITICAL)
- ✅ Type errors (mypy)
- ✅ Unused dependencies (deptry)
- ✅ High complexity code (radon D+)
- ⏸️ Low-confidence Vulture warnings (do later)

### 5. Integrate into Development Workflow
- ✅ Add key checks to pre-commit hooks
- ✅ Run full analysis in CI/CD
- ✅ Schedule weekly clean-up sprints
- ✅ Review reports in code reviews

## Troubleshooting

### "Vulture shows false positives"

**Solution:** Create a whitelist file:
```python
# vulture_whitelist.py
# Pydantic model fields
_.field_name
_.another_field

# Test fixtures
my_fixture

# Abstract methods
BaseClass.abstract_method
```

Then run: `vulture src tests vulture_whitelist.py --min-confidence 80`

### "Autoflake removed imports I need"

**Problem:** Imports used for side effects or type checking were removed.

**Solution:**
```python
# Prevent removal with noqa comment
import needed_for_side_effects  # noqa: F401

# Or use explicit export
__all__ = ['needed_for_side_effects']
```

### "Coverage is too low in integration tests"

**Problem:** Integration tests use VCR cassettes, so some code paths aren't hit.

**Solution:** This is expected. Check coverage separately:
```bash
# Unit tests only (should be high)
pytest tests/unit/ --cov=src

# Integration tests (may be lower, OK)
pytest tests/integration/ --cov=src --cov-append
```

### "deptry shows false positives for transitive dependencies"

**Problem:** deptry flags dependencies you don't import directly.

**Solution:** Either:
1. Add explicit dependency (better): `uv add package`
2. Ignore in `pyproject.toml`:
   ```toml
   [tool.deptry]
   ignore_obsolete = ["transitive-dep"]
   ```

### "Too many issues to fix at once"

**Solution:** Use phased approach:
1. **Week 1:** Fix security issues (bandit, pip-audit)
2. **Week 2:** Fix type errors (mypy)
3. **Week 3:** Remove dead code (vulture high confidence)
4. **Week 4:** Clean dependencies (deptry)
5. **Week 5:** Refactor complex code (radon)

## Cost/Benefit Analysis

### High ROI (Do These First)
- ✅ **Ruff auto-fix**: Free code quality improvements (2 min)
- ✅ **pip-audit**: Catch security issues before exploits (5 min)
- ✅ **deptry**: Remove unused dependencies → faster installs (5 min)
- ✅ **pyupgrade**: Modern syntax → better readability (10 min)

### Medium ROI (Weekly/Monthly)
- ⏸️ **Vulture**: Find dead code → smaller codebase (30 min + review time)
- ⏸️ **Coverage**: Improve test coverage → catch bugs (varies)
- ⏸️ **radon**: Refactor complex code → better maintainability (varies)

### Low ROI (Occasional)
- ⏸️ **bandit LOW severity**: May be false positives (60 min)
- ⏸️ **Vulture low confidence**: High false positive rate (60 min)
- ⏸️ **xenon**: Complexity enforcement (use radon instead)

## Summary

This skill provides a comprehensive toolkit for Python code clean-up:

**Quick wins (5-10 min):**
- `ruff check . --fix && ruff format .`
- `deptry .`
- `pip-audit`

**Weekly maintenance (30 min):**
- Coverage report
- Vulture dead code scan
- Complexity analysis
- Security scan

**Deep clean (2-4 hours):**
- Remove dead code
- Refactor complex functions
- Modernize syntax
- Update dependencies

**Key principle:** Always combine multiple tools for best results. No single tool catches everything.

### Tool Quick Reference

| Tool | Purpose | Confidence | Speed | False Positives |
|------|---------|------------|-------|-----------------|
| **coverage.py** | Find untested code | ⭐⭐⭐⭐⭐ | Medium | Very Low |
| **vulture** | Find unused code | ⭐⭐⭐⭐ | Fast | Medium |
| **deptry** | Check dependencies | ⭐⭐⭐⭐⭐ | Fast | Low |
| **ruff** | Lint & format | ⭐⭐⭐⭐⭐ | Very Fast | Very Low |
| **mypy** | Type checking | ⭐⭐⭐⭐⭐ | Medium | Low |
| **bandit** | Security issues | ⭐⭐⭐⭐ | Fast | Medium |
| **pip-audit** | Vulnerabilities | ⭐⭐⭐⭐⭐ | Fast | Very Low |
| **radon** | Complexity | ⭐⭐⭐⭐⭐ | Fast | Very Low |
| **pyupgrade** | Modernize syntax | ⭐⭐⭐⭐⭐ | Fast | Very Low |

**Legend:**
- ⭐⭐⭐⭐⭐ Highly reliable, use always
- ⭐⭐⭐⭐ Very useful, use regularly
- ⭐⭐⭐ Helpful, use occasionally

---

## When to Invoke This Skill

Invoke this skill when:
- User asks to "clean up code" or "find dead code"
- User wants to "analyze dependencies" or "check for unused imports"
- User asks to "improve code quality" or "run static analysis"
- User wants to "modernize Python syntax"
- User asks for "security scan" or "vulnerability check"
- User wants to "analyze test coverage"
- Before major refactoring to identify cruft
- After removing major features
- During code review of large PRs
- Weekly/monthly maintenance tasks

This skill complements existing tools (ruff, mypy, pytest) by providing additional layers of analysis beyond basic linting.
