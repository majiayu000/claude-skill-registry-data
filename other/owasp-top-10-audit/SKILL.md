---
name: owasp-top-10-audit
description: Production-grade skill package for Owasp Top 10 Audit in security-shield.
version: 1.0.0
domain: security-shield
triggers:
  - "owasp-top-10-audit"
  - "owasp top 10 audit"
---

# Owasp Top 10 Audit (`owasp-top-10-audit`)

> **Domain:** `security-shield`  
> **Progressive Disclosure:** Loaded just-in-time when trigger conditions match.  
> **Harness:** Antigravity Native  

## Trigger Conditions
- Activated when the task involves **Owasp Top 10 Audit** or domain **security-shield**.
- Explicitly requested via `/owasp-top-10-audit` slash command or agent delegation.

## Step-by-Step Instructions
1. **Analyze Context:** Review existing code, configuration, and constraints before applying modifications.
2. **Formulate Plan:** Outline the precise changes required, respecting project rules and token budget.
3. **Execute Incrementally:** Apply atomic changes adhering to clean architecture and target language standards.
4. **Run Verification:** Execute automated tests or compliance linters to validate correctness.
5. **Record Learning:** Persist any newly discovered patterns or architectural decisions into memory.

## Reference Resources & Checklist
- [ ] Confirm inputs are sanitized and free of injection vulnerabilities.
- [ ] Keep token footprint minimal; avoid unnecessary large file reads.
- [ ] Ensure backward compatibility with existing project interfaces.

## Verification Criteria
- [ ] Automated tests pass with 0 failures.
- [ ] Code conforms to relevant `rules/` standards.
- [ ] AgentShield security scan reports 0 Critical and 0 High severity issues.
