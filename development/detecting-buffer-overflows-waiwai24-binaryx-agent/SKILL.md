---
name: detecting-buffer-overflows
description: Detects stack and heap buffer overflow vulnerabilities in binary code by identifying unsafe memory operations. Use when analyzing buffer handling, string manipulation functions, or investigating memory corruption vulnerabilities.
---

# Buffer Overflow Detection

## Detection Workflow

1. **Identify dangerous function calls**: strcpy, strcat, sprintf, gets, memcpy without size checks
2. **Trace data flow**: Use `xrefs_to` from input sources (network, files, user input) to sinks
3. **Verify bounds checking**: For each copy operation, check if source size is validated and destination buffer is sufficient
4. **Assess exploitability**: Can attacker control overflow size? Is there controlled write to critical memory?

## Key Patterns

- Stack overflow: Unbounded copy to local buffer
- Heap overflow: Malloc followed by unchecked write
- Off-by-one: Loop condition or bounds check error
- Integer overflow leading to buffer overflow

## Output Format

Report with: id, type (stack/heap/static), severity, confidence, location, sink, source, buffer size, overflow potential, evidence, exploitability, mitigation.

## Severity Guidelines

- **CRITICAL**: Unbounded copy to stack buffer, attacker-controlled size
- **HIGH**: Bounded copy with insufficient checks, off-by-one errors
- **MEDIUM**: Potential overflow with limited attacker control
- **LOW**: Unlikely to be exploitable, theoretical only

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies