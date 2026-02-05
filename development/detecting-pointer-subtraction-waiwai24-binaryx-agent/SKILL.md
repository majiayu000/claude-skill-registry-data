---
name: detecting-pointer-subtraction
description: Detects unsafe pointer subtraction operations that can lead to incorrect size calculations and integer underflow. Use when analyzing pointer arithmetic, size calculations, or investigating buffer sizing issues.
---

# Pointer Subtraction Detection

## Detection Workflow

1. **Identify pointer subtractions**: Find all pointer subtraction operations, locate size calculations using pointers, identify pointer arithmetic for bounds, map memory operations using pointer math
2. **Analyze pointer relationships**: Verify pointers are from same array, check pointer alignment, assess pointer validity, verify pointer types
3. **Check result usage**: Trace subtraction result to usage, check for integer underflow, assess impact on memory operations, verify bounds checking logic
4. **Assess security impact**: Can underflow cause overflow? Can it bypass security checks? What's the potential impact? Is it exploitable?

## Key Patterns

- Size calculation errors: using pointer subtraction for size calculation, subtracting pointers from different arrays, incorrect pointer arithmetic for buffer sizes, size calculation without alignment consideration
- Integer underflow: pointer subtraction causing underflow, unsigned integer wraparound, negative results treated as large positive, size calculations going negative
- Bounds checking issues: using pointer subtraction for bounds checks, incorrect comparison results, off-by-one in pointer arithmetic, misaligned pointer operations
- Memory operations: memcpy with pointer-subtracted size, malloc with pointer-subtracted size, loop bounds from pointer subtraction, array indexing from pointer subtraction

## Output Format

Report with: id, type, subtype, severity, confidence, location, vulnerability, subtraction_operation, start_pointer, end_pointer, result_type, risk, exploitable, attack_scenario, impact, mitigation.

## Severity Guidelines

- **HIGH**: Pointer subtraction causing buffer overflow
- **MEDIUM**: Pointer subtraction causing logic errors
- **LOW**: Minor pointer arithmetic issues

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies