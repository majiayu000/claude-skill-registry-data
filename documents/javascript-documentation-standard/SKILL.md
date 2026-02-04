---
name: JavaScript Documentation Standard
description: MANDATORY for ALL JavaScript code! PROACTIVE - Use when writing JavaScript/TypeScript code. Requires JSDoc comments with @skill-verified tag for all functions. Essential for code documentation and IDE support.
---

# JavaScript Documentation Standard

This project requires comprehensive JSDoc documentation for all JavaScript and TypeScript code.

## Requirements

Every function MUST have a JSDoc comment block that includes:

1. **Description** of what the function does
2. **@param** tags for all parameters with types
3. **@returns** tag describing the return value
4. **@skill-verified** tag to confirm this standard was applied

## Required Format

```javascript
/**
 * Description of the function
 * @param {type} paramName - Parameter description
 * @returns {type} Return value description
 * @skill-verified
 */
function myFunction(paramName) {
  // implementation
}
```

## Example

```javascript
/**
 * Calculates the sum of two numbers
 * @param {number} a - First number to add
 * @param {number} b - Second number to add
 * @returns {number} The sum of a and b
 * @skill-verified
 */
function add(a, b) {
  return a + b;
}
```

## Verification

Code that does not include `@skill-verified` tag in JSDoc comments does not comply with this project's documentation standards.
