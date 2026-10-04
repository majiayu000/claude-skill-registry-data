---
name: security-engineering
description: Cross-stack security review — auditing vulnerabilities across infrastructure, smart contracts, CI/CD pipelines, and AI agent systems, plus auth/sessions/crypto and validating user input at API and infrastructure boundaries. Triggers on mentions of "vulnerability", "pentest", "OWASP", "access control", "injection", "CSRF", "JWT", "smart contract audit", "supply chain", "OIDC", or any review of security-sensitive code paths spanning more than one layer. For PII sanitization see [security](../security/SKILL.md).
when_to_use: |
  Use for cross-stack security review covering API security, infrastructure
  hardening, Web3 smart contract auditing, CI/CD pipeline security (OIDC, supply
  chain), and agentic AI risk (OWASP ASI 2026). Load when a diff touches auth,
  sessions, crypto, smart contracts, CI/CD secrets, or any user-input-to-sensitive-
  sink path.

  Not when: the task is scanning files for committed PII — use
  [security](../security/SKILL.md). Not when the task is a
  general multi-axis code review (correctness, readability, architecture,
  performance) rather than application security engineering — use [code-review-and-quality](../code-review-and-quality/SKILL.md).
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Security Engineering

Cross-stack security rules covering API security, infrastructure hardening, Web3 smart contracts, CI/CD review automation, and agentic AI risks. Aligned to OWASP Top 10:2025, ASVS 5.0, and OWASP Agentic Security Initiative 2026.

When reviewing code, think like a senior security researcher: trace user input through to sensitive operations, prefer fail-closed designs, and never trust the client.

## Universal Rules

- **Validate every input server-side** with Zod (or equivalent) at the API boundary.
- **Parameterize all queries** — Prisma/Drizzle, never string concatenation.
- **Authorize on every request** — deny by default, verify ownership.
- **Hash passwords with Argon2 or bcrypt** — never MD5/SHA1, never plaintext.
- **No hardcoded secrets** — env vars validated at startup, secrets in vault, `.env` in `.gitignore`.
- **TLS everywhere**, encryption at rest on all data stores.
- **Fail-closed** on auth/permission errors. Never expose stack traces to users.
- **Log security events** with sanitization — redact `authorization`, `cookie`, CSRF headers.
- **Least-privilege IAM** — scope to specific actions and resource ARNs, not `*`.
- **OIDC for CI/CD** — no long-lived credentials in GitHub.
- **Smart contracts**: ReentrancyGuard, SafeERC20, signed data must include `chainid + address(this) + deadline`, replay-prevention via `usedHashes`.

## References

- [references/owasp-top-10.md](references/owasp-top-10.md) — OWASP Top 10:2025 quick reference table
- [references/cicd-security.md](references/cicd-security.md) — CI/CD security review methodology, scanned vulnerability categories, supply-chain check
- [references/api-security.md](references/api-security.md) — auth patterns, Zod validation, rate limiting, CORS, headers, log sanitization, error handling
- [references/infrastructure-security.md](references/infrastructure-security.md) — VPC isolation, Cloudflare Zero Trust, secrets management, encryption, IAM principles
- [references/web3-smart-contracts.md](references/web3-smart-contracts.md) — required patterns, signature verification, on-chain rate limits, audit findings, Slither
- [references/code-review-checklist.md](references/code-review-checklist.md) — full checklist by category (input, auth, access control, data, errors, Web3)
- [references/secure-code-patterns.md](references/secure-code-patterns.md) — SQLi, command injection, access control, fail-closed, password storage examples
- [references/agentic-ai-security.md](references/agentic-ai-security.md) — OWASP 2026 ASI01-10 + agent security checklist
- [references/asvs-5.md](references/asvs-5.md) — L1/L2/L3 requirements
- [references/language-specific.md](references/language-specific.md) — JS/TS, Solidity, Python, Go, Bash risks + deep analysis mindset

## Related skills

- [web3-smart-contract-engineering](../web3-smart-contract-engineering/SKILL.md) — Solidity patterns, signature verification, replay protection (consult alongside `references/web3-smart-contracts.md` when auditing contracts)
- [deployment-pipelines](../deployment-pipelines/SKILL.md) — pipeline hardening, OIDC, untrusted-input handling in CI
- [godot-engineer](../godot-engineer/SKILL.md) — multiplayer games have real security concerns: cheating, save tampering, server-side validation, anti-replay. Pull this in for any networked game.
