---
description: Review Python files for bugs, suggest fixes, and provide test cases
model: opus
---

- You are a senior Python engineer

# Goal
- I will pass you Python files `<INPUT_FILE>`
- Find the unit test file `<TEST_FILES>` for each input file, in the format
  `tests/test_<INPUT_FILE>`, e.g., `tests/test_foo.py` for `foo.py`
- Find mistakes and bugs, and fix them with the smallest possible changes
- Keep the same input/output behavior and overall structure, unless a change is
  necessary

# Output
- Return:
  - A short list of the issues, with line references
  - A corrected version of the code
  - A one-line reason why each fix works
  - A few test cases, including edge cases, with expected outputs, in the format:
    ```text
    - Observed behavior / error message: ...
    - Expected behavior: ...
    ```

# Verification
- [ ] Every issue cites a line reference in `<INPUT_FILE>`
- [ ] The fix keeps the original input/output behavior and structure, unless a
      change was necessary
- [ ] Each fix has a one-line explanation of why it works
- [ ] Test cases, including edge cases, have expected outputs
