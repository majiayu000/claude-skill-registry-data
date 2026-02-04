---
name: detecting-memory-leaks
description: Detects memory leak vulnerabilities by identifying unfreed memory allocations and missing cleanup in error paths. Use when analyzing long-running processes, resource management, or investigating memory exhaustion issues.
---

# Memory Leak Detection

## Detection Workflow

1. **Identify allocation points**: Find all malloc/calloc/realloc calls, new/delete pairs (C++), map allocation locations
2. **Trace allocation lifecycle**: Use `xrefs_to` to trace allocations, follow pointers through code, identify all free() calls
3. **Check cleanup paths**: Verify every allocation has a corresponding free, check all error handling paths, review exception handling, assess callback cleanup
4. **Assess impact**: How much memory is leaked? How often does it leak? What's the cumulative impact? Can it cause DoS?

## Key Patterns

- Missing free: malloc() without corresponding free(), calloc() without free(), new without delete (C++)
- Exception path leaks: allocations before exception-prone operations, missing cleanup in error handling, leaks in early returns
- Reference cycles: circular references in data structures, reference counting bugs, shared pointer cycles
- Long-lived allocations: allocations that never get freed, caches without size limits, accumulating data structures

## Output Format

Report with: id, type, subtype, severity, confidence, location, allocation (function, address, size), leak path, leak scenario, leak size per call, frequency, exploitability, impact, mitigation.

## Severity Guidelines

- **HIGH**: Large leaks in frequently called functions
- **MEDIUM**: Small leaks or infrequent allocations
- **LOW**: Minor leaks with limited impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies