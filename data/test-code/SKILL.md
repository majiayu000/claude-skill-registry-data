---
name: test_code
description: pytestを使用してプロジェクトのテストスイートを実行する
---

# Test Code

This skill handles running the project's tests, including core types and general functionality.

## Usage

To run all tests:
```bash
pytest
```

To run and check core metadata propagation (TimeSeries/Spectrogram matrices):
```bash
pytest tests/ -k "metadata" # or relevant pattern
```

## Focus Areas (Core Verification)
- **Metadata Propagation**: Verify `radian()`, `degree()`, `to_matrix()` keep axes and units.
- **Ufuncs**: Check that arithmetic operations respect units.
- **Collections**: Ensure `List/Dict` to `Matrix` conversion inherits metadata correctly.

## Implementation Patterns

### Physics-First TDD (P-TDD)
When implementing physical logic such as numerical calculations or signal processing, create an **independent verification script** (`scripts/verify_*.py`) before adding it to the `pytest` suite.

1.  **Theoretical Verification**: Execute Parseval's theorem, check known amplitude/frequency peaks, and perform dimensional analysis of units.
2.  **Promotion to Pytest**: After success is confirmed, extract assertions from the verification script and migrate/elevate them to a formal `pytest` file (e.g., `tests/fields/test_*.py`).

This allows environment-dependent `AttributeError`s or logic errors to be isolated in a clean environment before integration into CI.
