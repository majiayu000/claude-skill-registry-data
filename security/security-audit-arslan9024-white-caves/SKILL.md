---
name: security-audit
description: 'Runs a focused security hardening audit across API, auth, and dependency surfaces with actionable fixes'
---

# Security Audit

Use this skill before release, after major backend changes, or when new integrations are added.

## Scope

- API endpoint protection (auth/role checks, input validation, error leakage)
- OWASP basics (XSS/CSRF/injection exposure patterns)
- Dependency hygiene (vulnerability and outdated package hotspots)
- Security config checks (CORS, headers, token/session handling)

## Workflow

1. Identify security-critical files and routes in the changed scope.
2. Verify auth and permission checks on sensitive endpoints.
3. Validate request sanitization/validation and safe defaults.
4. Check secrets handling and env usage (no secrets in source).
5. Review headers/CORS/session/token handling.
6. Summarize findings by severity and remediation priority.

## Output Format

- **Critical now**: must-fix before merge
- **Fix next**: medium impact / low effort
- **Plan**: medium impact / medium effort

For each finding include:

- file/path
- risk summary
- recommended fix
- quick validation step

## Gotchas

- Avoid broad speculative claims; only report evidence-backed findings.
- Distinguish between real vulnerability and defense-in-depth recommendation.

<!-- Inspired by awesome-copilot security/skills workflow patterns -->
