---
name: detecting-arbitrary-write
description: Detects arbitrary write vulnerabilities by identifying unchecked array indexing and out-of-bounds memory writes. Use when analyzing memory write operations, pointer arithmetic, or investigating code execution vulnerabilities.
---

# Arbitrary Write Detection

## Detection Workflow

1. **Identify write operations**: Find all array writes, pointer dereference writes, format string usage with %n, struct member writes
2. **Trace input sources**: Use `xrefs_to` to trace input, follow user data to write points, identify attacker-controlled values
3. **Check bounds validation**: Verify array bounds checks, assess pointer arithmetic safety, check format string validation, review type safety
4. **Assess exploitability**: Can attacker control write address? Can attacker control write value? What can be overwritten? Can code execution be achieved?

## Key Patterns

- Unchecked array indexing: array writes with user-controlled indices, pointer arithmetic writes with user input
- Format string writes: user-controlled format strings with %n, memory writes via printf
- Pointer dereference writes: writing through user-controlled pointers, use-after-free writes, vtable corruption
- Struct/class member writes: writing to wrong struct members, type confusion, vtable/function pointer overwrites

## Output Format

Report with: id, type, subtype, severity, confidence, location, vulnerability, write operation, array base, index source, value source, bounds check, exploitable, attack scenario, potential targets, mitigation.

## Severity Guidelines

- **CRITICAL**: Arbitrary write enabling code execution
- **HIGH**: Arbitrary write with significant impact
- **MEDIUM**: Arbitrary write with limited impact
- **LOW**: Minor arbitrary write issues

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies