---
name: code-style-reviewer
description: Code style principle-based review - checks SRP (Single Responsibility Principle), DRY (Don't Repeat Yourself), Simplicity First, YAGNI (You Aren't Gonna Need It), and Type Safety. Also evaluates code structure and naming conventions. Automatically used when code review is needed.
allowed-tools: Read, Grep, Glob
---

# Code Style Reviewer

A skill that provides professional code review based on code style principles. Claude directly analyzes code and generates detailed reports focusing on 5 core principles.

## Review Principles

### 1. Single Responsibility Principle (SRP)
Classes, functions, and modules should have only one responsibility. Complex functions should be split into smaller functions.

### 2. DRY (Don't Repeat Yourself)
The same logic should not be repeated. Common logic should be extracted into separate functions or utilities.

### 3. Simplicity First
Prefer simple, easy-to-understand code over complex abstractions. Avoid over-engineering.

### 4. YAGNI (You Aren't Gonna Need It)
Do not add features that are not currently needed. Remove unnecessary code written for future use.

### 5. Type Safety
Minimize the use of `any` type. When using TypeScript, define clear types.

## Instructions

### Review Process

1. **Identify Target Files**
   - Read code files to review using the Read tool
   - Understand file structure and scope

2. **Principle-by-Principle Analysis**
   - Systematically review each file against the 5 principles
   - Use Grep to find repeating patterns
   - Check naming convention consistency

3. **Generate Detailed Report**
   - Write reports organized by file
   - Provide specific improvement suggestions for each issue
   - Mark priorities:
     - **Critical**: Must be fixed
     - **Warning**: Needs improvement
     - **Suggestion**: Worth considering

4. **Provide Code Examples**
   - Present "Problem Code" vs "Improved Code" examples for each issue
   - Clearly explain the reason for the change

## Review Checklist

### Single Responsibility Principle Check
- [ ] Does the function perform only one task?
- [ ] Does the class have only one responsibility?
- [ ] Is complex logic split into smaller functions?
- [ ] Is the function length appropriate? (Recommended: under 20 lines)

### DRY Check
- [ ] Is there repeated code?
- [ ] Has common logic been extracted?
- [ ] Are config values not hardcoded?
- [ ] Can similar code structures be consolidated?

### Simplicity First Check
- [ ] Are there unnecessary abstractions?
- [ ] Are simple expressions used instead of complex syntax?
- [ ] Is there deep nesting? (Recommended: within 3 levels)
- [ ] Is there overly clever code?

### YAGNI Check
- [ ] Is there unused code?
- [ ] Are there unnecessary features added "just in case"?
- [ ] Are there removable parameters?
- [ ] Is there dead code or commented-out code?

### Type Safety Check (TypeScript)
- [ ] Is `any` type used?
- [ ] Do all function parameters have types defined?
- [ ] Are return types explicit?
- [ ] Are `interface` and `type` used appropriately?

### Naming Convention Check
- [ ] Are variable names meaningful and clear?
- [ ] Do function names start with verbs?
- [ ] Are class names nouns in PascalCase?
- [ ] Are constants in UPPER_SNAKE_CASE?
- [ ] Are naming conventions consistent?

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed examples and patterns
See [PRINCIPLES.md](PRINCIPLES.md) for detailed principle explanations

## Review Output Format

```
# Code Style Review Report

## 📄 File: [filename]

### ✅ Good Points
- [Good practices]

### ⚠️ Critical Issues
**Issue 1: [Title]**
- Location: [Line or function name]
- Principle: [Applicable principle]
- Description: [Detailed explanation]
- How to improve:
  ```
  // Before
  [Current code]

  // After
  [Improved code]
  ```

### 📢 Warnings
[Warning-level issues]

### 💡 Suggestions
[Suggestion-level improvements]

## 📊 Overall Assessment
- Overall code quality score: [X/10]
- Most important improvements: [Top 3]
```

## Usage Scenarios

This skill is automatically used in the following situations:

- When code review is requested
- When code quality analysis is requested
- When code structure improvement advice is needed
- When checking style of new files
- When suggesting refactoring for existing code
