---
name: code-metrics-analyzer
description: Calculate code quality metrics - complexity, coverage, maintainability
type: skill
language: python
---

# Code Metrics Analyzer

Measure code quality through various metrics.

## Capabilities
- Calculate cyclomatic complexity
- Measure code coverage
- Analyze lines of code (LOC)
- Count methods/functions per file
- Measure comment density
- Identify complex methods
- Track metrics over time
- Generate quality reports
- Find refactoring candidates

## Tools
`code_metrics.py` - Calculate various code metrics

## Metrics Calculated
- **Cyclomatic Complexity** - Decision point count
- **Cognitive Complexity** - Mental effort to understand
- **LOC** - Lines of code (total, code, comments, blank)
- **Method Count** - Methods per class/file
- **Depth of Inheritance** - Class hierarchy depth
- **Comment Ratio** - Comments vs code
- **Test Coverage** - Percentage tested

## Commands
```bash
# Analyze project
./code_metrics.py analyze --source-dir PaleoRose

# Find complex methods
./code_metrics.py complex --threshold 10

# Generate report
./code_metrics.py report --format html
```

## Output
```
Code Metrics Summary
====================
Total Files: 104
Total LOC: 15,234
Average Complexity: 4.2

Most Complex Files:
1. XRoseTableController.m (complexity: 28)
2. InMemoryStore.swift (complexity: 22)
3. DocumentModel.swift (complexity: 18)

Refactoring Candidates:
- XRoseTableController.configureController (complexity: 15)
- InMemoryStore.readFromStore (complexity: 12)
```
