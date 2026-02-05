---
name: detecting-command-injection
description: Detects OS command injection vulnerabilities by identifying unsafe system/popen/exec calls with user-controlled input. Use when analyzing command execution, shell operations, or investigating potential command injection points.
---

# Command Injection Detection

## Detection Workflow

1. **Identify command execution points**: Find system(), popen(), execve(), ShellExecute(), CreateProcess() calls
2. **Trace input sources**: Use `xrefs_to` to trace command strings to user input (network, files, environment variables)
3. **Check sanitization**: Verify input validation, character escaping, command argument separation, safe API usage
4. **Assess exploitability**: Can attacker inject special characters (;, &, |, `)? Control command arguments? Execute multiple commands?

## Key Patterns

- Direct system() with unvalidated user input
- popen() with partial sanitization
- execve with insufficient validation
- Indirect command execution via environment variables

## Output Format

Report with: id, type (system/popen/exec), severity, confidence, location, sink, source, command string, sanitization status, exploitability, payload example, mitigation.

## Severity Guidelines

- **CRITICAL**: Direct use of system() with unvalidated user input
- **HIGH**: popen() with partial sanitization
- **MEDIUM**: execve with array but insufficient validation
- **LOW**: Command execution with strict whitelisting

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies