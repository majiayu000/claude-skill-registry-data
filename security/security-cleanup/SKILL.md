---
name: security-cleanup
description: Applies fixes for security findings produced by /security-review. Use when the
  user wants to fix security issues found by /security-review or when they ask
  to clean up, remediate, or apply fixes for security findings.
---

# Security Cleanup (A01:2025–A10:2025 + LLM01:2025–LLM10:2025)

## What this checks

Applies fixes for security findings. Pair with `/security-review` to
detect issues, then `/security-cleanup` to fix them.

## Vulnerable patterns

This skill remediates, not detects. Run `/security-review` first.

## Procedure

1. Get the findings: from the user's message, a recent `/security-review`
   output, or — if none are available — run `/security-review` first to
   produce them.

2. For each finding (highest severity first):
   - Read the cited file at the cited line
   - Read `.claude/skills/<skill>/SKILL.md` for the correct fix pattern
   - Apply the fix using the Edit tool
   - Use the language's idiomatic safe API (Go `html/template`, Python
     `Environment(autoescape=True)`, Java `PreparedStatement`, etc.)

3. After all findings are processed, summarize what was fixed.

**Rules:**
- Never change observable behavior beyond removing the vulnerability
- If unsure about the correct fix, say so and skip that finding
- One Edit per finding — don't refactor surrounding code

## Verification

- [ ] Each fix addresses the specific finding cited
- [ ] No fix introduces new vulnerabilities or changes business logic
- [ ] Summary lists all findings and their disposition

## References

- CWE-693 ([Protection Mechanism Failure](https://cwe.mitre.org/data/definitions/693.html))
- [OWASP Web Top 10:2025](https://owasp.org/www-project-top-ten/)
- [OWASP LLM Top 10:2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
