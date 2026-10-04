---
name: notebook-refactor
description: Extract Jupyter notebook cells into tested Python modules while preserving the exploration workflow. Use when converting prototyping notebooks into production code.
---

# Notebook Refactoring Skill

Convert Jupyter notebook exploration code into clean, tested Python modules.

## Process

### 1. Analyze the Notebook

Read the notebook and identify:

- **Data loading cells** -> `src/data/` module
- **Preprocessing/transformation cells** -> `src/data/` or `src/preprocessing/` module
- **Model definition cells** -> `src/models/` module
- **Training loop cells** -> `src/training/` module
- **Evaluation/metrics cells** -> `src/evaluation/` module
- **Visualization cells** -> keep in notebook (these are exploratory)
- **Configuration values** (magic numbers, paths) -> `src/config/` or config file

### 2. Extract Functions

For each group of cells:

1. Identify inputs and outputs of the cell block
2. Extract into a function with:
   - Type-annotated parameters for all inputs
   - A clear return type
   - A docstring explaining what it does and why
3. Replace hardcoded values with parameters
4. Remove `display()`, `print()` debugging statements
5. Keep the notebook cell but replace the code with an import + function call

### 3. Write Tests

For each extracted function, write tests that:

- Use small, deterministic test fixtures (not the full dataset)
- Test the function's contract (input types -> output types/shapes)
- Test edge cases (empty input, single row, missing values)
- Use `np.testing.assert_allclose` for numerical outputs
- Do NOT test exact numerical values from model operations (non-deterministic)

### 4. Update the Notebook

After extraction, the notebook should:

- Import from the new modules instead of defining functions inline
- Still be runnable end-to-end
- Serve as a high-level walkthrough / documentation of the pipeline
- Keep exploratory visualizations and analysis inline

### 5. Refactoring Checklist

Before marking complete:

- [ ] All extracted functions have type hints
- [ ] All extracted functions have tests
- [ ] Notebook still runs end-to-end with imports
- [ ] No hardcoded paths or magic numbers remain
- [ ] No unused imports in extracted modules
- [ ] `pyproject.toml` or `setup.py` updated if new packages are needed
