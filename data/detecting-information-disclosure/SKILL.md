---
name: detecting-information-disclosure
description: Detects information disclosure vulnerabilities including sensitive data in logs, error message exposure, and memory leaks. Use when analyzing logging practices, error handling, or investigating data leakage issues.
---

# Information Disclosure Detection

## Detection Workflow

1. **Identify sensitive data flows**: Find where sensitive data is handled, trace data through application, identify all output points
2. **Check logging practices**: Analyze log statements, check error messages, review debug output
3. **Assess exposure points**: Identify all user-facing output, check external API responses, review file system artifacts
4. **Evaluate impact**: What information is disclosed? How sensitive is it? Who can access it?

## Key Patterns

- Sensitive data in logs: passwords, keys, stack traces in production logs
- Error message disclosure: detailed errors revealing system info, paths, database queries
- Memory disclosure: uninitialized memory reads, out-of-bounds reads, format string leaks
- Storage disclosure: plaintext storage, weak encryption, insecure file permissions

## Output Format

Report with: id, type, subtype, severity, confidence, location, sensitive data type, disclosure point, vulnerability description, exposure scope, risk, mitigation.

## Severity Guidelines

- **CRITICAL**: Disclosure of cryptographic keys or passwords
- **HIGH**: Disclosure of sensitive user data
- **MEDIUM**: Disclosure of system information
- **LOW**: Disclosure of minor debug information

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies