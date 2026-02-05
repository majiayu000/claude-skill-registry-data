---
name: codeinspect
description: Analyzes code to identify refactoring opportunities, code duplication, problematic data flows, architectural issues, and code smells. Generates a comprehensive refactoring recommendation plan.
---

# Code Inspection Guide

## Overview
This skill performs a comprehensive code quality analysis to identify refactoring opportunities and code smells. The analysis is read-only and produces a detailed refactoring recommendation plan without making any changes to the codebase.

## Scope
By default, analyze the entire project. Users can specify specific files or directories to inspect if needed.

## Output
Generate a refactoring recommendation plan and write it to `@docs/refactoring-recommendations.md` in the current project directory.

## Analysis Areas

### 1. Code Duplication
Identify opportunities to eliminate duplicate code:
- Similar or identical code blocks across multiple files
- Repeated logic that could be extracted into shared functions/methods
- Copy-pasted code with minor variations
- Duplicated constants or configuration values
- Similar class structures that could use inheritance or composition

### 2. Data Flow Issues
Identify confusing or problematic data patterns:
- Unclear data transformations (input -> output not obvious)
- Excessive mutations of shared state
- Complex data pipelines that are hard to follow
- Inconsistent data validation or sanitization
- Data flowing through too many layers unnecessarily
- Mixed responsibilities in data transformation functions
- Hidden side effects in data operations

### 3. Architectural Smells
Identify design and structure issues:
- Tight coupling between modules/classes
- Missing abstraction layers
- God objects (classes doing too much)
- Feature envy (methods using more data from other classes)
- Inappropriate intimacy (classes too dependent on each other's internals)
- Circular dependencies
- Violation of separation of concerns
- Missing or unclear boundaries between layers
- Inconsistent error handling patterns

### 4. Code Smells
Identify general code quality issues:
- Long methods/functions (>50 lines)
- Complex conditionals (deeply nested if/else)
- High cyclomatic complexity
- Unclear or misleading variable/function names
- Magic numbers or hardcoded values
- Dead code or unused imports
- Inconsistent naming conventions
- Overly complex class hierarchies
- Methods with too many parameters (>4)
- Switch/case statements that should be polymorphism
- Comments explaining "what" instead of "why"
- Lack of error handling or over-broad exception catching

## Inspection Process

### Step 1: Understand the Project
- Identify the project structure and main directories
- Understand the primary programming language(s)
- Note the project type (web app, library, CLI tool, etc.)
- Review any existing documentation or architecture notes

### Step 2: Scan and Analyze
Systematically review the codebase focusing on:
- Core business logic files
- Frequently modified files (check git history if available)
- Large files (likely to have complexity issues)
- Files with many dependencies

For each file analyzed, look for the issues described in the Analysis Areas section.

### Step 3: Prioritize Findings
Categorize issues by severity:
- **Critical**: Major architectural problems, security issues, or severe code duplication
- **High**: Significant code smells affecting maintainability
- **Medium**: Moderate refactoring opportunities
- **Low**: Minor improvements and style consistency

### Step 4: Generate Recommendations
For each finding, provide:
- **Location**: Exact file path and line numbers (e.g., `src/utils/helper.ts:45-67`)
- **Issue Type**: Which category (duplication, data flow, architectural, code smell)
- **Severity**: Critical, High, Medium, or Low
- **Description**: Clear explanation of the problem
- **Current Code Pattern**: Brief description or snippet of the problematic pattern
- **Recommended Refactoring**: Specific, actionable steps to improve the code
- **Benefits**: What will improve (maintainability, testability, readability, etc.)

## Report Format

Structure the output document as follows:

```markdown
# Code Inspection Report
Generated: [Date]

## Executive Summary
- Total files analyzed: [number]
- Total issues found: [number]
- Critical: [number], High: [number], Medium: [number], Low: [number]

## Key Findings
[Brief overview of the most important issues]

## Detailed Recommendations

### Critical Priority

#### [Issue Title]
- **Location**: `path/to/file.ext:line-range`
- **Type**: [Code Duplication | Data Flow | Architectural | Code Smell]
- **Description**: [What's wrong]
- **Current Pattern**: [How it works now]
- **Recommended Refactoring**: [What to do]
- **Benefits**: [Why this helps]

[Repeat for each critical issue]

### High Priority
[Same format as Critical]

### Medium Priority
[Same format as Critical]

### Low Priority
[Same format as Critical]

## Refactoring Strategy
[Suggested order of operations for implementing the recommendations]

## Next Steps
[Concrete action items for the development team]
```

## Important Notes

- **Read-Only**: This skill MUST NOT modify any code files
- **No Execution**: Do not run tests, builds, or any other commands that modify state
- **Document Only**: All output goes to the refactoring recommendations document
- **Be Specific**: Always include exact file paths and line numbers
- **Be Actionable**: Each recommendation should have clear steps
- **Be Realistic**: Consider the effort vs. benefit trade-off
- **Respect Existing Patterns**: Note when the team has intentionally chosen certain patterns

## Completion Criteria
- All relevant code files have been analyzed
- Findings are categorized and prioritized
- Each issue has specific location references
- Recommendations are clear and actionable
- Report is written to `@docs/refactoring-recommendations.md`
- User is notified that the inspection is complete
