---
name: secure-flow
description: A comprehensive security skill that integrates with Secure Flow to help AI coding agents write secure code, perform security reviews, and implement security best practices. Use this skill when writing, reviewing, or modifying code to ensure secure-by-default practices are followed.
version: "1.0.0"
framework: "Secure Flow"
purpose: "Embed secure-by-default practices into AI coding workflows"
---

# Secure Flow Skill
This skill provides comprehensive security guidance to help AI coding agents generate secure code, perform security reviews, and implement security best practices. It is based on **Secure Flow**, a security framework that embeds secure-by-default practices into AI coding workflows.

## When to Use This Skill
This skill should be activated when:
- Writing new code in any language
- Reviewing or modifying existing code
- Implementing security-sensitive features (authentication, cryptography, data handling, etc.)
- Working with user input, databases, APIs, or external services
- Configuring cloud infrastructure, CI/CD pipelines, or containers
- Handling sensitive data, credentials, or cryptographic operations
- Performing security assessments, threat modeling, or compliance validation
- Creating security tests or remediating vulnerabilities

## How to Use This Skill
When writing or reviewing code:

1. **Always-Apply Rules**: Some rules MUST be checked on every code operation:
   - Security best practices for authentication and authorization
   - Input validation and sanitization
   - Secure credential management
   - Cryptographic best practices

2. **Context-Specific Rules**: Apply rules from `/rules` directory based on the task:
   - **Code Generation**: Use `secure-flow-create-secure-template.md` when creating new code templates
   - **Security Testing**: Use `secure-flow-create-security-tests.md` when generating security tests
   - **Threat Modeling**: Use `secure-flow-create-threat-model.md` when analyzing security threats
   - **Vulnerability Remediation**: Use `secure-flow-security-remediation.md` when fixing vulnerabilities
   - **API Security**: Use `secure-flow-review-api-auth.md` when reviewing API endpoints
   - **Compliance**: Use `secure-flow-validate-compliance.md` when validating compliance requirements
   - **Docker Security**: Use `secure-flow-harden-dockerfile-fips.md` when hardening containers
   - **CI/CD Security**: Use `secure-flow-gate-critical-vulns.md` when setting up security gates
   - **CISA KEV**: Use `secure-flow-fix-exploitable-vulns.md` when fixing exploited vulnerabilities
   - **AI Security**: Use `secure-flow-explain-ai-threats.md` when working with AI applications

3. **Proactive Security**: Don't just avoid vulnerabilities—actively implement secure patterns:
   - Use parameterized queries for database access
   - Validate and sanitize all user input
   - Apply least-privilege principles
   - Use modern cryptographic algorithms and libraries
   - Implement defense-in-depth strategies
   - Follow secure coding standards and best practices

## Secure Flow Security Rules
The security rules are available in the `rules/` directory.

### Usage Workflow
When generating or reviewing code, follow this workflow:

### 1. Initial Security Check
Before writing any code:
- Check: Will this handle credentials? → Apply secure credential management practices
- Check: What language/framework am I using? → Identify applicable security rules
- Check: What security domains are involved? → Load relevant rule files

### 2. Code Generation
While writing code:
- Apply secure-by-default patterns from relevant Secure Flow rules
- Add security-relevant comments explaining choices
- Follow framework-specific security best practices

### 3. Security Review
After writing code:
- Review against implementation checklists in each rule
- Verify no hardcoded credentials or secrets
- Validate that all applicable security rules have been followed
- Explain which security rules were applied
- Highlight security features implemented

## Available Workflows

### Code Generation & Templates
- **`secure-flow-create-secure-template`** - Generate secure code templates with security best practices built-in

### Security Testing
- **`secure-flow-create-security-tests`** - Create comprehensive security test cases and validation scripts

### Threat Analysis
- **`secure-flow-create-threat-model`** - Generate threat models for applications and systems using STRIDE methodology
- **`secure-flow-explain-ai-threats`** - Explain AI-specific security threats and mitigations

### Vulnerability Management
- **`secure-flow-security-remediation`** - Scan and fix high-impact vulnerabilities in the codebase
- **`secure-flow-fix-exploitable-vulns`** - Fix CISA Known Exploited Vulnerabilities (KEV) found in your codebase
- **`secure-flow-gate-critical-vulns`** - Set up CI/CD checks to block critical vulnerabilities

### API & Service Security
- **`secure-flow-review-api-auth`** - Review and add authentication to API endpoints

### Compliance & Validation
- **`secure-flow-validate-compliance`** - Validate compliance with security frameworks and standards (SOC 2, ISO 27001, HIPAA, PCI DSS)

### Infrastructure Security
- **`secure-flow-harden-dockerfile-fips`** - Make Dockerfiles FIPS compliant with security hardening

## Implementation Checklist
- [ ] Identified applicable security rules for the task
- [ ] Applied secure-by-default patterns
- [ ] Validated input and output handling
- [ ] Verified authentication and authorization
- [ ] Checked for hardcoded credentials
- [ ] Applied framework-specific security best practices
- [ ] Reviewed against security checklists
- [ ] Documented security decisions

