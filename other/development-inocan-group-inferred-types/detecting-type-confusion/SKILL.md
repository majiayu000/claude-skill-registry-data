---
name: detecting-type-confusion
description: Detects type confusion vulnerabilities by identifying unsafe type casts, vtable corruption, and polymorphism issues. Use when analyzing object-oriented code, type casting, or investigating C++ memory safety issues.
---

# Type Confusion Detection

## Detection Workflow

1. **Identify type operations**: Find all type casts, virtual function calls, union usage, class hierarchies
2. **Analyze type safety**: Check cast validation, assess vtable integrity, verify union usage correctness
3. **Trace object flow**: Use `xrefs_to` to trace objects, identify type changes, assess type consistency
4. **Assess exploitability**: Can attacker control object type? Is there useful type confusion? Can attacker corrupt vtable?

## Key Patterns

- Unsafe type casting: C-style casts without validation, reinterpret_cast without checks
- Vtable corruption: virtual function calls on corrupted objects, vtable pointer manipulation
- Union misuse: writing to one union member, reading another
- Polymorphism issues: base pointer used as derived without dynamic_cast

## Output Format

Report with: id, type, subtype, severity, confidence, location, vulnerability, cast operation, base type, derived type, validation, vtable access, exploitability, attack scenario, impact, mitigation.

## Severity Guidelines

- **CRITICAL**: Type confusion with code execution
- **HIGH**: Type confusion with data corruption
- **MEDIUM**: Type confusion with limited impact
- **LOW**: Type confusion with minor issues

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies