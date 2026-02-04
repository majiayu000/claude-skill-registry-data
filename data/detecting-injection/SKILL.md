---
name: detecting-injection
description: Detects various injection vulnerabilities including SQL injection, LDAP injection, XPath injection, and code injection. Use when analyzing database queries, dynamic code generation, or investigating injection attacks.
---

# Injection Detection

## Detection Workflow

1. **Identify injection points**: Find database query construction, locate dynamic code generation, identify template rendering, map all user input usage
2. **Trace user input**: Use `xrefs_to` to trace data, follow input to injection points, check for sanitization, identify bypass opportunities
3. **Check sanitization**: Verify input validation, check for parameterized queries, assess escaping mechanisms, look for whitelist/blacklist usage
4. **Assess exploitability**: Can attacker inject malicious content? What's the impact of injection? Are there mitigations?

## Key Patterns

- SQL injection: string concatenation in SQL queries, dynamic query construction, missing parameterized queries, stored procedure injection
- LDAP injection: user input in LDAP filters, unsafe LDAP query construction, special character handling issues, DN manipulation
- XPath injection: user input in XPath expressions, unsafe XPath construction, XML entity injection, blind XPath injection
- Code injection: eval() or similar dynamic code execution, template injection, server-side template injection (SSTI), deserialization attacks

## Output Format

Report with: id, type, subtype, severity, confidence, location, vulnerability, injection_point (function, address, query), source, injection_technique, exploitable, attack_scenario, payload_example, mitigation.

## Severity Guidelines

- **CRITICAL**: SQL injection with full database access
- **HIGH**: Other injection with data access
- **MEDIUM**: Limited injection impact
- **LOW**: Potential injection with minor impact

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies