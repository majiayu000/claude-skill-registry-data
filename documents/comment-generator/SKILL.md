---
name: comment-generator
description: Generate code comments and docstrings. Use when user asks to "add comments", "document this code", "explain with comments", or "add docstrings".
allowed-tools: [Read, Edit]
---

# Comment Generator Skill

Automatically generates clear, helpful comments for code.

## When to Use

This skill activates when the user wants to add comments to their code:
- "Add comments to this function"
- "Document this code"
- "Add docstrings to my Python class"
- "Explain this with inline comments"

## Instructions

### Step 1: Identify Language

Determine the programming language from:
- File extension
- Syntax patterns
- User specification

### Step 2: Choose Comment Style

**JavaScript/TypeScript:**
```javascript
/**
 * Calculates the sum of two numbers
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} The sum
 */
function add(a, b) {
  return a + b;
}
```

**Python:**
```python
def add(a, b):
    """
    Calculates the sum of two numbers.

    Args:
        a (int): First number
        b (int): Second number

    Returns:
        int: The sum of a and b
    """
    return a + b
```

**Java:**
```java
/**
 * Calculates the sum of two numbers
 * @param a First number
 * @param b Second number
 * @return The sum
 */
public int add(int a, int b) {
    return a + b;
}
```

### Step 3: Comment Structure

For functions/methods:
1. **Summary**: What it does (one line)
2. **Parameters**: Each parameter explained
3. **Returns**: What it returns
4. **Throws/Raises**: Any exceptions (if applicable)
5. **Examples**: Usage example (if complex)

For classes:
1. **Summary**: What the class represents
2. **Attributes**: Key properties
3. **Usage**: How to instantiate and use

For complex logic:
1. **Inline comments**: Explain why, not what
2. **Section comments**: Mark major sections
3. **TODO/FIXME**: Note improvements needed

### Step 4: Write Clear Comments

✅ **Good comments:**
- Explain WHY, not just WHAT
- Use clear, simple language
- Are concise but complete
- Add value (don't state the obvious)

❌ **Bad comments:**
```javascript
// Add a and b
function add(a, b) {
  return a + b;  // Return the sum
}
```

✅ **Better:**
```javascript
/**
 * Combines two monetary values, useful for calculating totals
 * Handles floating point precision for currency
 */
function add(a, b) {
  return Math.round((a + b) * 100) / 100;  // Round to 2 decimals
}
```

## Examples

### Example 1: Simple Function

**Input:**
```javascript
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Output:**
```javascript
/**
 * Calculates the total price of all items in a collection
 * @param {Array<{price: number}>} items - Array of items with price property
 * @returns {number} Total price of all items
 * @example
 * const total = calculateTotal([{price: 10}, {price: 20}]); // Returns 30
 */
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Example 2: Complex Function

**Input:**
```python
def process_data(data, filters=None):
    if not filters:
        filters = []
    result = []
    for item in data:
        valid = True
        for f in filters:
            if not f(item):
                valid = False
                break
        if valid:
            result.append(item)
    return result
```

**Output:**
```python
def process_data(data, filters=None):
    """
    Filters a dataset using multiple filter functions.

    Applies each filter function to every item in the dataset.
    Only items that pass all filters are included in the result.

    Args:
        data (list): Collection of items to filter
        filters (list of callable, optional): Filter functions that return True/False.
                                             Defaults to empty list (no filtering).

    Returns:
        list: Filtered dataset containing only items that passed all filters

    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> is_even = lambda x: x % 2 == 0
        >>> is_positive = lambda x: x > 0
        >>> process_data(data, [is_even, is_positive])
        [2, 4]
    """
    if not filters:
        filters = []

    result = []

    for item in data:
        valid = True

        # Apply each filter - item must pass all filters
        for f in filters:
            if not f(item):
                valid = False
                break  # Skip remaining filters if one fails

        if valid:
            result.append(item)

    return result
```

## Tips

### For Beginners
- Start with function/method summaries
- Add parameter descriptions
- Include simple examples

### For Intermediate
- Add type information
- Document exceptions
- Include edge cases

### For Advanced
- Add algorithmic complexity
- Document thread safety
- Include performance notes

## What NOT to Comment

❌ Don't comment obvious code:
```javascript
// Increment i
i++;
```

❌ Don't duplicate code in comments:
```javascript
// Set name to "John"
name = "John";
```

❌ Don't leave outdated comments:
```javascript
// TODO: Fix this next week
// (Written 2 years ago)
```

## Remember

- Comments should add value
- Update comments when code changes
- Explain complex logic
- Document public APIs thoroughly
- Keep private code comments minimal but helpful
