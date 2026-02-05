---
name: detecting-suspicious-assert
description: Detects suspicious use of assertions for security checks that can be disabled in production builds. Use when analyzing assertion usage, security checks, or investigating assert-related vulnerabilities.
---

# Suspicious Assert Detection

## Detection Workflow

1. **Identify assert operations**: Find all assert() calls, locate assertion macros, identify static_assert usage, map assertion patterns
2. **Analyze assert purpose**: Determine assert intent, check if used for security, assess criticality of check, review assert context
3. **Check for bypass potential**: Verify if asserts are disabled, assess release build behavior, check for compile-time flags, review build configuration
4. **Assess security impact**: Can assert be bypassed? What's the security impact? Is critical check disabled? What's the exploit potential?

## Key Patterns

- Asserts for security checks: using assert() for input validation, using assert() for security checks, using assert() for authentication, using assert() for authorization
- Asserts that can be disabled: critical checks using assert(), security-critical validations using assert(), resource allocation checks using assert(), bounds checks using assert()
- Asserts with side effects: asserts with function calls, asserts with assignments, asserts modifying state, asserts with non-pure expressions
- Incorrect assert usage: asserts on user-controlled data, asserts that can be bypassed, asserts in release builds, asserts in production code

## Output Format

Report with: id, type, subtype, severity, confidence, location, vulnerability, assert_statement, assert_type, check_purpose, disabled_in_release, exploitable, attack_scenario, impact, mitigation.

## Severity Guidelines

- **HIGH**: Assert used for critical security checks
- **MEDIUM**: Assert used for important validation
- **LOW**: Assert used for debugging only

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies