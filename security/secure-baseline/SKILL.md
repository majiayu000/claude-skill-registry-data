---
name: secure-baseline
description: "Baseline security review for web apps and APIs using OWASP Top 10 and ASVS. Use when reviewing code, adding auth/handling input, or before release. Produces severity-ranked findings with evidence, never silent patches."
---

# secure-baseline

OWASP-grounded baseline review. Read-only: report findings with remediation; do not silently patch what you audit.

## Activate when

- Reviewing a PR, module, or full codebase for vulnerabilities.
- Adding authentication, file handling, crypto, payments, or third-party integrations.
- Preparing a release.

## Do NOT activate for

- Post-incident forensics or pentest execution (different scope; see agent-security for agent-specific review).
- Scanner-only CVE sweeps (see secrets-supply-chain).

## Procedure

1. Scope: changed files first, then reachable sinks (DB, shell, FS, network, template, deserializer).
2. Walk the OWASP checklist in `references/` (injection, broken access control, crypto failures, insecure design, misconfiguration, vulnerable components, auth failures, integrity failures, logging gaps, SSRF).
3. For each candidate finding demand evidence: file:line, tainted source-to-sink path, and why existing controls fail. Rate confidence HIGH/MEDIUM/LOW; report HIGH first, mark LOW as needs-confirmation.
4. Map each finding to CWE + OWASP category with a concrete fix and a regression test idea.
5. Verify: re-read the diff after any fix; confirm no secrets in code/history and no error path leaks internals.

## Severity

- Blocker: exploitable injection, IDOR on sensitive data, auth bypass, RCE/SSRF, secret exposure.
- High: missing authorization check, weak crypto, insecure default.
- Maintainability: defense-in-depth hardening.
- Optional: style-level nits (never blockers).

## References
- Deeper API checks: `../../backend/api-security/`; secrets/CI: `../secrets-supply-chain/`.
- Implementation integration: this review runs against the implementation (not isolated docs), then hands findings back for fixes; `../../core/code-review/` re-verifies the final diff including the security fixes.
