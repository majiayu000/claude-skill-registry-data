---
name: detecting-integer-overflow
description: Detects integer overflow and underflow vulnerabilities in arithmetic operations used for buffer sizing or allocation. Use when analyzing calculations, size computations, or investigating integer wraparound issues.
---

# Integer Overflow Detection

## Detection Workflow

1. **Identify arithmetic operations**: Find addition, multiplication, subtraction, bit shifts on user-controlled values
2. **Check for overflow protection**: Look for overflow checks before arithmetic, safe arithmetic functions, type conversions
3. **Trace to critical uses**: Follow results to memory allocation sizes, buffer copy lengths, loop bounds, array indices
4. **Assess impact**: Can overflow cause buffer overflow? Bypass security checks? Cause logic errors?

## Key Patterns

- Addition/multiplication without overflow checks
- Subtraction that could underflow
- Integer overflow affecting malloc size
- Loop counter overflow

## Output Format

Report with: id, type (addition/multiplication/underflow), severity, confidence, location, operation, operands, result used for, overflow check status, exploitability, impact, mitigation.

## Severity Guidelines

- **HIGH**: Overflow affects memory allocation size
- **MEDIUM**: Overflow affects loop bounds or array indices
- **LOW**: Overflow with limited security impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies