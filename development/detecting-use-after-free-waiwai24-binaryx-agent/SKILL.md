---
name: detecting-use-after-free
description: Detects use-after-free vulnerabilities by identifying pointer dereferences after memory deallocation. Use when analyzing memory management, cleanup code, or investigating dangling pointer issues.
---

# Use-After-Free Detection

## Detection Workflow

1. **Identify free operations**: Find all free(), realloc(), delete calls and note the pointer being freed
2. **Trace pointer usage**: Use `xrefs_to` to find all dereferences of the pointer
3. **Check control flow**: Analyze paths through code to identify usage after free
4. **Assess exploitability**: Can attacker control freed memory? Is there a useful use-after-free? Can memory be reallocated?

## Key Patterns

- Pointer dereference after free()
- Double free vulnerabilities
- Invalid pointer access after realloc()
- Reference counting issues

## Output Format

Report with: id, type, subtype, severity, confidence, location, freed pointer, free operation, use operation, use-after-free status, distance, exploitability, attack scenario, impact, mitigation.

## Severity Guidelines

- **CRITICAL**: Use-after-free with code execution
- **HIGH**: Use-after-free with data corruption
- **MEDIUM**: Use-after-free causing crashes
- **LOW**: Use-after-free with limited impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies