---
name: root-calculator
description: Performs mathematical root calculations including square root, cube root, and nth roots. Use when user asks to calculate square root, cube root, nth root, or uses keywords like 'sqrt', 'root of', 'calculate root'.
---

# Root Calculator

This skill performs mathematical root calculations including square roots, cube roots, and nth roots of numbers.

## When to Use This Skill

Activate this skill automatically when the user:
- Asks to calculate a square root (e.g., "square root of 16", "sqrt(25)")
- Asks to calculate a cube root (e.g., "cube root of 27")
- Asks to calculate an nth root (e.g., "4th root of 81", "5th root of 32")
- Uses math keywords like "sqrt", "root of", "calculate root"

## How to Use

When the user requests a root calculation:

1. **Parse the request** to identify:
   - The number to calculate the root of
   - The root type (square, cube, or nth root)

2. **Perform the calculation** using Python:

   For **square root**:
   ```python
   import math
   result = math.sqrt(number)
   ```

   For **cube root**:
   ```python
   result = number ** (1/3)
   ```

   For **nth root**:
   ```python
   result = number ** (1/n)
   ```

3. **Handle edge cases**:
   - Negative numbers with even roots: Explain that the result is a complex number
   - For negative numbers with odd roots: Use `abs(number) ** (1/n) * (-1 if number < 0 else 1)`
   - Very large or very small numbers: Use scientific notation if needed

4. **Present the result** clearly:
   - Show the calculation performed
   - Display the result with appropriate precision (typically 4-6 decimal places)
   - For perfect roots, show the exact integer result

## Examples

### Example 1: Square Root
```
User: "What's the square root of 144?"
Claude: The square root of 144 is 12.
```

### Example 2: Cube Root
```
User: "Calculate the cube root of 27"
Claude: The cube root of 27 is 3.
```

### Example 3: Nth Root
```
User: "What's the 4th root of 81?"
Claude: The 4th root of 81 is 3.
```

### Example 4: Non-Perfect Root
```
User: "Square root of 50"
Claude: The square root of 50 is approximately 7.0711.
```

### Example 5: Negative Number (Odd Root)
```
User: "Cube root of -8"
Claude: The cube root of -8 is -2.
```

### Example 6: Negative Number (Even Root)
```
User: "Square root of -16"
Claude: The square root of -16 is not a real number. In the complex number system, it equals 4i.
```

## Error Handling

- **Invalid input**: If the user's request is unclear, ask for clarification
- **Negative numbers with even roots**: Explain that the result is complex (not a real number)
- **Division by zero**: If n=0 in nth root, explain this is undefined
- **Very large results**: Use scientific notation for readability

## Notes

- Use Python's `math` module for square roots for better precision
- For other roots, use the exponentiation operator `**`
- Round results appropriately (typically 4-6 decimal places for non-perfect roots)
- Always show the exact integer if the result is a perfect root
