---
name: mimir-security-analysis
description: Identify security risks, vulnerabilities, and unsafe patterns in code and configuration.
---

# Security Analysis

## Purpose

Analyze systems for security weaknesses, identify vulnerabilities, and recommend mitigation strategies. This is an investigative skill: it examines the existing state before or independent of implementation, producing findings that inform decisions — validating that delivered changes address those findings is the concern of a subsequent security review.

## When to Use

- Before releasing a feature that handles sensitive data or authentication.
- When reviewing code that processes user input or external data.
- When auditing existing systems for security gaps.
- When the security implications of a design decision need to be assessed.

## Workflow

1. **Identify the attack surface.**
   - Map entry points (APIs, user input, file uploads, configuration).
   - Identify sensitive data (credentials, PII, tokens, secrets).
   - Understand trust boundaries and privilege levels.

2. **Review authentication and authorization.**
   - Verify that access controls are enforced at every entry point.
   - Check for common flaws: missing checks, privilege escalation, insecure defaults.
   - Review session management and token handling.

3. **Analyze data handling.**
   - Check for injection vulnerabilities (SQL, command, XSS, template).
   - Verify input validation, sanitization, and output encoding.
   - Review encryption practices for data at rest and in transit.

4. **Review configuration and dependencies.**
   - Check for insecure defaults, debug modes, or hardcoded secrets.
   - Review dependency security (known vulnerabilities, outdated versions).
   - Check logging and error handling for information leakage.

5. **Document findings.**
   - Report vulnerabilities by severity and exploitability.
   - Provide clear remediation steps with references where applicable.
   - Note areas that need further investigation.

## Quality Criteria

- Entry points and trust boundaries are clearly mapped.
- Vulnerabilities are categorized by severity and impact.
- Recommendations are specific and actionable.
- Common vulnerability classes are systematically checked.

## Anti-Patterns

- **Perimeter-only thinking**: Only securing the external boundary while ignoring internal trust.
- **Security theater**: Implementing security measures that look good but don't actually protect.
- **Assuming the user is honest**: Not validating input or checking permissions because "it's internal."
- **Over-reliance on tools**: Depending on automated scanners while ignoring logic flaws.
