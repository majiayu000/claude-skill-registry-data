---
name: Refactoring Test Suites
description: Enforces consistent test quality, structure, and maintainability across any programming language by applying project-wide conventions for test naming, structure, parameterization, and classification. Use for messy test suites, inconsistent naming, improving CI alignment and developer readability, or when the user mentions test cleanup, test organization, or test standardization.
---

# Refactoring Test Suites

Refactor test suites for consistent quality, structure, and maintainability.

## What you should do

1. **Collect project context** – Analyze documentation files like `README.md`, `CONTRIBUTING.md`, and any `/docs/` content to extract expected application behaviors and development conventions. Use this understanding to assess test coverage quality and intent alignment.

2. **Standardize behavioral test naming** – Rename all test cases to describe expected behavior rather than implementation details:
   - Use format: `test_should_X_when_Y` or `test_rejects_X_when_Y`
   - Replace vague names: `testSave` → `test_should_persist_user_data_when_valid_input`
   - Focus on outcomes: `testCalculateTotal` → `test_should_sum_all_item_prices_when_valid_cart`
   - Include error cases: `testInvalidInput` → `test_should_reject_invalid_email_with_clear_error`

3. **Decompose multi-assert tests** – Detect tests containing multiple logic branches or assertion statements:
   - Split into atomic tests with a single clear assertion each.
   - Ensure individual tests are concise, readable, and scoped to one behavior.
   - Assign self-documenting names and a brief summary comment or docstring.

4. **Parameterize repeated logic** – Identify duplicate test structures with variable inputs. Consolidate into parameterized cases using the appropriate mechanism for the language:
   - e.g., table-driven tests, decorators, or loop constructs.
   - Favor clarity in naming, argument structure, and output expectations.

   Python (PyTest) specifics:
   - Prefer `@pytest.mark.parametrize` for clear inputs/outputs.
   - Extract shared setup to fixtures in `conftest.py`.

5. **Classify and relocate tests** – Categorize tests into:
   - **Unit tests**: isolated logic-level validation.
   - **Feature/integration tests**: end-to-end behavior or API workflows.
   Based on classification:
   - Move files to `tests/unit/` or `tests/features/` directories.
   - Create directories as needed and update any test runner configs or imports.
   - Consolidate reusable fixtures or setup logic into shared modules or test utilities.

6. **Eliminate vanity tests** – Identify and remove tests that don't verify meaningful behavior:
   - Remove tests that only verify mocks were called without checking outcomes
   - Delete tests with excessive mocking that don't test real object interactions
   - Eliminate coverage-motivated tests that pass regardless of functionality
   - Replace shallow tests with behavioral tests that would fail if the feature broke
   - Log rationale in commit (e.g., "Remove vanity test, add behavioral verification").

7. **Tag and annotate tests** – For each test:
   - Add metadata tags (e.g., `@unit`, `@integration`, `@smoke`) as supported by the test framework.
   - Normalize inline comments or docstrings to summarize intent.
   - Remove unnecessary or unclear inline commentary.

   Python (PyTest) specifics:
   - Use `@pytest.mark.unit` and `@pytest.mark.feature`.
   - Ensure docstrings summarize expected behavior in one line.

8. **Enforce directory structure and verify coverage** – Create missing folders:

   ```bash
   mkdir -p tests/unit tests/features
   ```

   Run test suites independently:

   ```bash
   test-runner tests/unit/
   test-runner tests/features/
   ```

   Replace `test-runner` with project-specific command (e.g., `pytest`, `go test`, `npm test`).

9. **Format and lint test files** – Apply appropriate formatters and linters for the project's language:

   - Example for JavaScript: `prettier --write tests/ && eslint tests/`
   - Example for Go: `gofmt -w . && golint ./...`
   - Example for Python: `black tests/ && ruff tests/`
   - Log errors and rerun tests to confirm no regressions introduced.

10. **Summarize results and recommend follow-up** – Output a structured summary including:

    - Test files renamed, relocated, or deleted
    - Parameterized test cases added
    - Unit tests promoted or consolidated
    - Directory and tagging structure applied
    - Recommend ongoing practices:
    - Maintain classification boundaries across PRs
    - Periodically audit for redundant tests or format drift