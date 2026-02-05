---
name: code-metrics
description: Code metrics calculation methodology for static analysis
---

# Code Metrics Calculation

## Objective

Calculate comprehensive code metrics for quality assessment.

## Metrics Definitions

### Complexity Metrics

1. **Cyclomatic Complexity**
   - Count: decisions + 1
   - Decisions: if, else, for, while, case, catch, &&, ||, ?:
   - Thresholds: 1-10 (good), 11-20 (moderate), 21+ (high risk)

2. **Cognitive Complexity**
   - Base: control flow structures
   - Nesting penalty: +1 per nesting level
   - Thresholds: 1-15 (good), 16-30 (moderate), 31+ (refactor)

3. **Nesting Depth**
   - Maximum depth of nested structures
   - Thresholds: 1-3 (good), 4-5 (moderate), 6+ (refactor)

### Size Metrics

1. **Lines of Code (LOC)**
   - Physical lines (including blanks)
   - Logical lines (statements)
   - Comment lines

2. **Function Length**
   - Lines per function/method
   - Thresholds: 1-30 (good), 31-50 (moderate), 51+ (long)

3. **File Length**
   - Total lines per file
   - Thresholds: 1-300 (good), 301-500 (moderate), 501+ (large)

### Coupling Metrics

1. **Afferent Coupling (Ca)**
   - Number of modules depending on this module
   - High Ca = widely used, risky to change

2. **Efferent Coupling (Ce)**
   - Number of modules this module depends on
   - High Ce = high dependency, harder to maintain

3. **Instability (I)**
   - Formula: Ce / (Ca + Ce)
   - Range: 0 (stable) to 1 (unstable)

### Duplication Metrics

1. **Duplicate Lines**
   - Exact match blocks > 6 lines
   - Percentage of codebase

2. **Similar Blocks**
   - Token-based similarity > 85%
   - Parameterized duplicates

## Calculation Process

1. Parse source files into AST
2. Visit all nodes and calculate metrics
3. Aggregate at function, class, file, module levels
4. Compare against thresholds
5. Generate scores (0-100)

## Scoring Formula

```
Quality Score = 100 - (
  complexity_penalty * 0.3 +
  size_penalty * 0.2 +
  coupling_penalty * 0.2 +
  duplication_penalty * 0.3
)
```

Where penalties are percentage of violations.
