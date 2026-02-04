---
name: detecting-null-pointer-dereference
description: Detects null pointer dereference vulnerabilities by identifying unchecked pointer usage and missing validation. Use when analyzing pointer operations, input validation, or investigating crash vulnerabilities.
---

# Null Pointer Dereference Detection

## Detection Workflow

1. **Identify pointer dereferences**: Find all pointer dereferences (*ptr, ptr->field), array accesses (ptr[index]), function calls with pointer parameters, pointer operations
2. **Trace pointer sources**: Use `xrefs_to` to trace pointers, find where pointers originate, identify pointer assignments, track pointer values
3. **Check null validation**: Verify null checks before dereference, assess check completeness, identify missing validation paths, check validation logic correctness
4. **Assess impact**: Can attacker control pointer value? Is dereference reachable? What's the crash potential? Can it lead to security issues?

## Key Patterns

- Missing null checks: pointer dereference without null check, function calls with unchecked pointers, array access through null pointers, member access through null pointers
- Conditional dereference: dereference after partial null check, dereference in only some code paths, dereference after pointer assignment, dereference in loop conditions
- Function parameter issues: unchecked function parameters, assumptions about non-null parameters, missing validation in public APIs, null pointers from external sources
- Return value issues: dereferencing potentially null return values, assuming malloc/new never returns null, missing checks on function returns, dereferencing failed allocations

## Output Format

Report with: id, type, subtype, severity, confidence, location, dereferenced_pointer, dereference_type, dereference_operation, pointer_source, null_check, vulnerability, exploitable, attack_scenario, impact, mitigation.

## Severity Guidelines

- **HIGH**: Null dereference in critical code paths
- **MEDIUM**: Null dereference causing crashes
- **LOW**: Null dereference with limited impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies