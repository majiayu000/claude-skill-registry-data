---
name: security-audit
description: Procedure for analyzing code or dependencies for vulnerabilities
---

## Procedure

1. Run `npm audit`.
2. Scan for hardcoded secrets using `grep`.
3. Review authentication/authorization logic in changed files.
4. Check for injection risks (SQLi, XSS) in inputs.
5. Report findings to `docs/findings.md` or fix if critical.
