---
name: evo-build-diagnosis
description: Analyzes a Python repository to identify the root causes of build failures, including syntax errors, import errors, test failures, and build configuration issues. Use when diagnosing why a Python project fails to build or pass tests. Scans repository files for syntax errors via ast.parse/compile, parses pytest output and CI logs, checks build configuration files (pyproject.toml, setup.py, setup.cfg), identifies missing dependencies, and produces a structured diagnosis report.
---

# Build Diagnosis Skill

This skill analyzes Python repositories to identify root causes of build failures.

## When to Use

- A Python project fails to build or install
- pytest tests are failing with errors
- CI/CD pipelines report build failures
- You need to diagnose syntax errors, import errors, or configuration issues

## Workflow

1. **Find the repository** using `find_repo_path()` to locate the project root
2. **Scan for syntax errors** using `parse_syntax_errors()` which uses `ast.parse()`/`compile()` on all `.py` files
3. **Check imports** using `check_import_availability()` to verify all dependencies are installed
4. **Analyze build config** using `analyze_build_config()` to parse pyproject.toml/setup.py/setup.cfg
5. **Run tests** using `run_tests_and_capture_failures()` to execute pytest and parse JUnit XML output
6. **Write report** using `write_diagnosis_report()` to produce `failed_reasons.txt`

## Key Functions

All functions are in `scripts/diagnosis.py`:

- `find_repo_path(base_dirs)` - Locates the repository root by searching common paths
- `parse_syntax_errors(repo_path)` - Scans all .py files for syntax errors using compile()
- `run_build_and_capture_errors(repo_path)` - Runs pip install and captures errors
- `run_tests_and_capture_failures(repo_path)` - Runs pytest with --junitxml and parses results
- `analyze_build_config(repo_path)` - Parses pyproject.toml, setup.py, setup.cfg
- `check_import_availability(dependencies)` - Checks if modules can be imported
- `write_diagnosis_report(findings, output_path)` - Writes structured failed_reasons.txt

## Important Notes

- Always use `encoding='utf-8'` when reading Python source files to avoid encoding errors
- AST col_offset values are UTF-8 byte offsets, not character indices
- Use subprocess isolation when running pytest to avoid state pollution
- Check Python version compatibility (3.7-3.12 syntax differences)

## Reference

See `references/domain_reference.md` for detailed domain knowledge.
