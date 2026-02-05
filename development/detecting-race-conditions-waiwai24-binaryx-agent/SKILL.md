---
name: detecting-race-conditions
description: Detects race condition vulnerabilities including TOCTOU, double-checked locking issues, and shared state problems. Use when analyzing concurrent operations, file access patterns, or investigating timing-related vulnerabilities.
---

# Race Condition Detection

## Detection Workflow

1. **Identify critical operations**: Find file access sequences (check then use), shared state access patterns, synchronization primitives
2. **Trace execution paths**: Use `xrefs_to` to identify potential interleaving points and race windows
3. **Check synchronization**: Verify locks protect critical sections, check for atomic operations, assess lock ordering
4. **Assess exploitability**: Can attacker control timing? Is there a useful race window? What's the impact?

## Key Patterns

- TOCTOU (Time-of-Check to Time-of-Use)
- Double-checked locking issues
- Unprotected shared variables
- Non-atomic operations on shared data
- Signal handler issues

## Output Format

Report with: id, type, subtype, severity, confidence, location, vulnerability, check operation, use operation, race window, exploitability, attack scenario, impact, mitigation.

## Severity Guidelines

- **CRITICAL**: Race allowing privilege escalation
- **HIGH**: Race allowing file access bypass
- **MEDIUM**: Race causing data corruption
- **LOW**: Race with minor impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies