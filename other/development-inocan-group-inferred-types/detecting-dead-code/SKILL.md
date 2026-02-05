---
name: detecting-dead-code
description: Identifies unreachable functions, unused variables, and abandoned code in binary programs. Use when optimizing binary size, analyzing code coverage, or investigating abandoned functionality.
---

# Dead Code Detection

## Detection Workflow

1. **Build call graph**: Use `disasm` to build control flow, identify all functions, map function call relationships
2. **Identify entry points**: Find main/entry functions, locate exported functions, identify callback registrations, map interrupt handlers
3. **Trace reachability**: Perform forward reachability analysis from entry points, mark all reachable functions and blocks, identify unreachable code
4. **Analyze dead code**: Categorize dead code types, assess security implications, identify potential vulnerabilities, estimate size reduction

## Key Patterns

- Unreachable functions: functions with no callers, functions only called from dead code, functions after infinite loops, functions after exit() calls
- Unreachable blocks: basic blocks after return statements, code after unconditional jumps, blocks with no incoming edges, code guarded by always-false conditions
- Unused data: global variables never referenced, string constants never used, data sections with no references, debug symbols in production builds
- Conditional dead code: code in always-false branches, debug-only code in release builds, platform-specific code for other platforms, feature flags permanently disabled

## Output Format

Report with: id, type, subtype, severity, confidence, location, dead_code_type, reason, callers, references, size_estimate, security_implications, potential_vulnerabilities, recommendation.

## Severity Guidelines

- **MEDIUM**: Dead code containing security vulnerabilities
- **LOW**: Dead code with no security impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies