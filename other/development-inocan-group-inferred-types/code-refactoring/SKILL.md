---
name: "Code Refactoring"
description: "Improve code structure, readability, and maintainability without changing external behavior through systematic refactoring"
category: "implementation"
required_tools: ["Read", "Write", "Edit", "MultiEdit", "Grep", "Glob"]
---

# Code Refactoring

## Purpose
Improve code structure, readability, and maintainability without changing its external behavior or functionality.

## When to Use
- Code is hard to understand or modify
- Duplicated code exists
- Functions are too long or complex
- Code smells are present
- Preparing for new features

## Key Capabilities
1. **Extract Method** - Break long functions into smaller pieces
2. **Rename** - Improve variable/function names for clarity
3. **Remove Duplication** - Consolidate repeated code

## Approach
1. Identify code that needs improvement
2. Ensure tests exist before refactoring
3. Make small, incremental changes
4. Run tests after each change
5. Commit working states frequently

## Example
**Before**:
````python
def process(data):
    result = []
    for item in data:
        if item > 0 and item < 100 and item % 2 == 0:
            result.append(item * 2)
    return result
````

**After**:
````python
def is_valid_even_number(n):
    return 0 < n < 100 and n % 2 == 0

def process(data):
    valid_numbers = filter(is_valid_even_number, data)
    return [n * 2 for n in valid_numbers]
````

## Best Practices
- ✅ Always have tests before refactoring
- ✅ Make small, incremental changes
- ✅ Run tests after each change
- ❌ Avoid: Refactoring and adding features simultaneously