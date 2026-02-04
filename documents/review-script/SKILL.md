---
name: review-script
description: Review a script for documentation quality, code standards, and reproducibility. Helps ensure code is ready for the methods section. Use when the user types /review_script, after writing a new script, before writing methods, or when passive checks flag undocumented scripts.
---

# Script Review

> Review a script for documentation quality, code standards, and reproducibility.
> Helps ensure code is ready for the methods section.

## Usage
```
/review_script [path]
/review_script scripts/preprocessing.py
/review_script scripts/  # Review all scripts in directory
```

## When to Use
- After writing a new script
- Before running /write_methods
- When passive checks flag undocumented scripts
- During code review or cleanup

## Execution Steps

### 1. Load Script(s)

Read the specified script or all scripts in directory.

### 2. Documentation Checklist

For each script, check:

```markdown
## Documentation Review: [script_name.py]

### Module-Level Documentation
- [ ] Has module docstring explaining purpose
- [ ] Lists author/date (optional but good)
- [ ] Describes inputs/outputs
- [ ] Notes dependencies

### Function Documentation
| Function | Has Docstring | Args Documented | Returns Documented |
|----------|---------------|-----------------|-------------------|
| func1 | ✓/✗ | ✓/✗ | ✓/✗ |
| func2 | ✓/✗ | ✓/✗ | ✓/✗ |

### Inline Comments
- [ ] Complex logic is explained
- [ ] Magic numbers are explained
- [ ] Non-obvious decisions documented
```

### Inline Comment Guidance: Explain WHY, Not WHAT

```python
# ❌ BAD: States the obvious (what the code does)
x = x + 1  # Increment x by 1
data = data.dropna()  # Drop NA values

# ✅ GOOD: Explains reasoning (why we're doing it)
x = x + 1  # Offset for 1-based indexing in output file
data = data.dropna()  # Required by downstream model; NAs cause silent failures

# ❌ BAD: Obvious from context
if threshold > 0.5:  # Check if threshold is greater than 0.5

# ✅ GOOD: Explains the magic number
if threshold > 0.5:  # Optimized cutoff from ROC analysis (see supplementary Fig S2)
```

### 3. Code Quality Checks

```markdown
### Code Quality

**Strengths:**
- [What's done well]

**Issues:**
- 🔴 Critical: [Must fix]
- 🟡 Recommended: [Should fix]
- 🔵 Suggestion: [Nice to have]

### Reproducibility
- [ ] Random seeds set (if applicable)
- [ ] Parameters configurable (not hardcoded)
- [ ] Dependencies importable
```

### 4. Docstring Templates

If missing, suggest adding:

**Python function:**
```python
def process_data(input_file: str, threshold: float = 0.5) -> pd.DataFrame:
    """
    Process raw data file and apply quality filtering.
    
    Reads the input file, removes low-quality samples, and applies
    normalization. Used as first step in the analysis pipeline.
    
    Args:
        input_file: Path to raw data CSV file
        threshold: Quality score cutoff (default: 0.5)
    
    Returns:
        DataFrame with processed samples, shape (n_samples, n_features)
    
    Raises:
        FileNotFoundError: If input_file doesn't exist
        ValueError: If threshold not in [0, 1]
    
    Example:
        >>> df = process_data("data/raw/samples.csv", threshold=0.6)
        >>> print(df.shape)
        (150, 2000)
    """
```

**Python module:**
```python
"""
Preprocessing module for RNA-seq data.

This module handles quality filtering, normalization, and batch
correction for raw count data. It is the first stage of the
analysis pipeline.

Scripts:
    - preprocess.py: Main preprocessing logic
    
Usage:
    python preprocess.py --input data/raw/counts.csv --output data/processed/

Author: [Name]
Date: [Date]
"""
```

**R function:**
```r
#' Process raw data file and apply quality filtering
#'
#' Reads the input file, removes low-quality samples, and applies
#' normalization. Used as first step in the analysis pipeline.
#'
#' @param input_file Path to raw data CSV file
#' @param threshold Quality score cutoff (default: 0.5)
#' @return DataFrame with processed samples
#' @export
#' @examples
#' df <- process_data("data/raw/samples.csv", threshold = 0.6)
process_data <- function(input_file, threshold = 0.5) {
  # Implementation
}
```

### 5. Generate Review Report

```markdown
# Script Review: [script_name]

## Summary
- Documentation: [Good/Needs work/Missing]
- Code quality: [Good/Needs work]
- Reproducibility: [Ready/Needs work]

## Documentation Status

### Module Docstring: [✓ Present / ✗ Missing]
[If missing, suggest content]

### Functions
| Function | Docstring | Quality |
|----------|-----------|---------|
| main() | ✗ Missing | Add description of entry point |
| process() | ✓ Present | Good, but add example |

## Issues Found

### 🔴 Critical (Must Fix)
1. [Issue] - Line [N]
   ```python
   # Current
   [problematic code]
   
   # Suggested
   [improved code]
   ```

### 🟡 Recommended
1. [Issue with suggestion]

### 🔵 Nice to Have
1. [Optional improvement]

## Methods Section Notes

When documenting this script in methods.md, include:
- [Key algorithm/method used]
- [Important parameters: X, Y, Z]
- [Any assumptions made]

## Quick Fixes

Copy-paste these improvements:

[Ready-to-use docstrings and comments]
```

### 6. Offer to Apply Fixes

```
Review complete. Would you like me to:

A) Add the suggested docstrings to [script_name]
B) Review another script
C) Update methods.md with this script's documentation
D) Show me the full suggested improvements

Choice?
```

## Quality Standards

### Documentation Levels

| Level | Description | Minimum For |
|-------|-------------|-------------|
| 1 - Minimal | Module docstring only | Personal scripts |
| 2 - Basic | + Function docstrings | Shared code |
| 3 - Complete | + Examples, types | Publication |
| 4 - Comprehensive | + Tests, edge cases | Package release |

**Target for publication: Level 3**

### Reproducibility Checklist

```markdown
## Reproducibility Review

- [ ] No hardcoded absolute paths
- [ ] All file paths use params.yaml or CLI args
- [ ] Random seeds set and documented
- [ ] Package versions in environment file
- [ ] No reliance on global state
- [ ] Outputs are deterministic
- [ ] Error messages are informative
```

## Related Skills

- `write-methods` - Document script in methods section
- `next` - Get next suggestion

## Notes

- Good documentation now saves hours later
- Write docstrings as if explaining to a colleague
- Comments explain WHY, code explains WHAT
- Update docs when code changes
