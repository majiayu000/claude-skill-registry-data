---
name: detecting-off-by-one
description: Detects off-by-one errors by identifying incorrect loop conditions, array indexing mistakes, and boundary condition problems. Use when analyzing loops, array access, or investigating fencepost errors.
---

# Off-by-One Detection

## Detection Workflow

1. **Identify array operations**: Find all array accesses, loop iterations, buffer allocations, string operations
2. **Analyze boundary conditions**: Check loop termination conditions, array index ranges, buffer size calculations
3. **Check edge cases**: Test boundary conditions, verify fencepost cases, assess null terminator handling
4. **Assess impact**: Can off-by-one cause overflow/underflow? What's the security impact?

## Key Patterns

- Loop bound errors: using <= instead of <, or < instead of <=
- Array index errors: accessing array[size] instead of array[size-1]
- String handling errors: missing null terminator, incorrect buffer size
- Allocation errors: allocating size instead of size+1

## Output Format

Report with: id, type, subtype, severity, confidence, location, vulnerability, loop condition, array access, array size, error type, exploitability, attack scenario, impact, mitigation.

## Severity Guidelines

- **HIGH**: Off-by-one causing buffer overflow
- **MEDIUM**: Off-by-one causing information disclosure
- **LOW**: Off-by-one with minor impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies