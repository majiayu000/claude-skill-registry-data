---
name: security-methodology
description: This skill should be used when the user mentions "OWASP", "CWE", "CVE", "security compliance", "security scoring", "security maturity model", "vulnerability classification", "risk rating", or "dependency vulnerability scanning". Provides security assessment frameworks and vulnerability classification methodology.
---

# Security Assessment Methodology

## Purpose

Provide standardized security assessment frameworks, vulnerability classification systems, and compliance evaluation methodology for use during security scanning and auditing. Tech-agnostic, applies to any language or framework.

## OWASP Risk Rating

Calculate risk using these factors:

| Risk Factor | Score (0-9) | What to Evaluate |
|-------------|-------------|------------------|
| Threat Agent | 0-9 | Skill level, motive, opportunity, size of threat group |
| Attack Vector | 0-9 | Ease of exploitation (automated=9, requires physical access=1) |
| Security Weakness | 0-9 | Prevalence × detectability |
| Technical Impact | 0-9 | Loss of confidentiality, integrity, availability |
| Business Impact | 0-9 | Financial, reputation, compliance, privacy damage |

**Overall Risk** = Average of factors, weighted by context.

## Security Debt Calculation

| Severity | Remediation Time per Issue | Priority |
|----------|---------------------------|----------|
| Critical | 4 hours | P0, fix immediately |
| High | 2 hours | P1, fix this sprint |
| Medium | 1 hour | P2, fix this quarter |
| Low | 30 minutes | P3, fix when convenient |

**Total Security Debt** = Sum of (count × remediation time) per severity level.

## Security Maturity Model

| Level | Name | Description |
|-------|------|-------------|
| 0 | None | No security measures |
| 1 | Initial | Ad-hoc, reactive security |
| 2 | Managed | Basic security controls in place |
| 3 | Defined | Standardized security processes |
| 4 | Quantified | Metrics-driven security decisions |
| 5 | Optimizing | Continuous security improvement |

## Security Score Breakdown

Rate each dimension 0-10:

| Dimension | What to Evaluate |
|-----------|-----------------|
| Authentication & Authorization | Auth mechanisms, RBAC/ABAC, session management |
| Data Protection | Encryption at rest/transit, data masking, PII handling |
| Input Validation | Sanitization, whitelisting, encoding at boundaries |
| Cryptography | Algorithm strength, key management, randomness |
| Session Management | Token handling, timeout, fixation prevention |
| Error Handling | Information leakage, stack traces, debug exposure |
| Dependency Security | CVE count, update frequency, vulnerable transitive deps |
| Configuration Security | Default credentials, debug mode, unnecessary services |

## Additional Resources

### Reference Files

For detailed vulnerability patterns and compliance frameworks, consult:
- **`references/owasp-top10.md`**: OWASP Top 10 categories with detection patterns
- **`references/security-patterns.md`**: Language-agnostic vulnerability patterns to scan for
- **`references/cwe-cve-reference.md`**: CWE categories and CVE analysis methodology
- **`references/compliance-frameworks.md`**: PCI DSS, GDPR, HIPAA, SOC 2 gap analysis
