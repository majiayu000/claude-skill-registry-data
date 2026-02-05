---
name: code-quality-reviewer
description: Comprehensive code quality review focusing on DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid), and Clean Code (Easy to Read) principles. Use when reviewing code changes, analyzing code quality, or assessing code maintainability for any feature, bug fix, or refactoring task.
allowed-tools: Read, Grep, Glob
---

# Code Quality Reviewer

## Overview

This skill provides systematic code quality review focusing on three core principles that determine maintainability, readability, and long-term sustainability of code:

- **DRY (Don't Repeat Yourself)**: Eliminate code duplication and consolidate common logic
- **KISS (Keep It Simple, Stupid)**: Prefer simple, straightforward solutions over complex ones
- **CLEAN CODE (Easy to Read)**: Write self-documenting code that's easy to understand

The skill applies to all code changes: features, bug fixes, refactoring, and chores.

## Review Process

### Step 1: Gather Code Context
- Read the modified files to understand the changes
- Search for related code patterns in the codebase
- Identify the scope and impact of the changes

### Step 2: Analyze Code Quality
- Check for code duplication (DRY principle)
- Evaluate code complexity and simplicity (KISS principle)
- Assess readability and clarity (CLEAN CODE principle)

### Step 3: Identify Issues
- Document specific violations with file paths and line numbers
- Categorize issues by severity and principle
- Suggest concrete improvements

### Step 4: Provide Recommendations
- Include refactored code examples where applicable
- Explain the benefits of the proposed changes
- Link to related principles for context

## Quality Review Checklist

### DRY (Don't Repeat Yourself)
- [ ] Check for duplicated logic across functions/methods
- [ ] Look for repeated code patterns in similar components
- [ ] Identify common operations that could be extracted to utilities
- [ ] Verify helper functions are reused appropriately
- [ ] Check for duplicate error handling patterns
- [ ] Identify repeated conditional logic

### KISS (Keep It Simple, Stupid)
- [ ] Evaluate function complexity (line count, nested levels)
- [ ] Check for overly complex conditional logic
- [ ] Identify unnecessary abstraction layers
- [ ] Review parameter lists for excessive arguments
- [ ] Check for over-engineered solutions
- [ ] Verify the simplest solution is being used

### CLEAN CODE (Easy to Read)
- [ ] Verify meaningful variable and function names
- [ ] Check function/method documentation and comments
- [ ] Evaluate consistent code formatting and style
- [ ] Review logical code organization and flow
- [ ] Check for self-documenting code (clear intent)
- [ ] Identify cryptic or magic values that need explanation

## Output Format

Present findings in this structured format:

```
## Code Quality Review: [File Name]

### 🔴 Critical Issues
- [Issue 1 with line numbers and explanation]
- [Issue 2 with line numbers and explanation]

### 🟡 Moderate Issues
- [Issue 1 with line numbers and explanation]
- [Issue 2 with line numbers and explanation]

### 🟢 Minor Issues / Suggestions
- [Issue 1 with line numbers and explanation]
- [Issue 2 with line numbers and explanation]

### ✅ Positive Observations
- [What was done well]
- [Strengths in the implementation]

### 📋 Summary
[Brief summary of overall code quality assessment and key recommendations]

### 💡 Related Principles
- See [PRINCIPLES.md](PRINCIPLES.md) for detailed explanations
- See [EXAMPLES.md](EXAMPLES.md) for code examples
```

## When This Skill Activates

This skill is automatically invoked when you:
- Ask for code review or quality assessment
- Request feedback on code changes
- Ask about code maintainability or readability
- Request refactoring suggestions
- Question code complexity or duplication
- Review pull requests or commits
- Work on code cleanup or optimization

## Usage Scenarios

### Scenario 1: Reviewing Feature Code
```
"Can you review this new user authentication module for code quality?"
→ Skill reviews for DRY principles (reusing auth logic), KISS simplicity,
  and CLEAN CODE readability
```

### Scenario 2: Bug Fix Assessment
```
"I fixed this performance issue. Is the code quality acceptable?"
→ Skill checks if the fix is simple, well-documented, and doesn't
  introduce duplication
```

### Scenario 3: Refactoring Validation
```
"I'm thinking about refactoring this helper function. Any concerns?"
→ Skill analyzes if current code violates any principles and validates
  refactoring approach
```

## Key Differences from Style Review

Unlike style review (formatting, naming conventions), quality review focuses on:
- **Logical structure and maintainability**
- **Code duplication and reusability**
- **Complexity assessment**
- **Readability of implementation patterns**

A style reviewer checks if code follows conventions; a quality reviewer checks if code is maintainable.
