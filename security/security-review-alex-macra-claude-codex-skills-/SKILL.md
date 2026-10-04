---
name: security-review
description: "Security review of a codebase or a target you are authorized to test: OWASP Top 10, secrets, auth, input validation, supply chain, infra hygiene. Use for a security audit, vulnerability or CVE check, pentest-style review, hardening, secret-leak hunts, or is-this-secure questions."
license: MIT
metadata:
  display-name: "Security Review"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "security owasp audit hardening"
---

# Security review

For a general break-it pass use `adversarial-review`.

## Authorization gate (read first)
Before testing any *running* system, confirm scope and authorization in writing:
- Is this our system, a CTF, a personal lab, or a paid pentest engagement?
- What targets / IPs / domains are in scope? What is explicitly out of scope?
- What testing methods are allowed? (DoS, social eng, supply chain - usually out of scope by default.)
- What is the rules-of-engagement for findings disclosure?

If any of this is unclear, **stop and ask the user** before sending packets. Codebase review needs no such gate - read freely.

## Two modes

- **Mode A - Codebase review (static).** You're reading source. Look for vulnerable patterns, not exploits.
- **Mode B - Live target testing (dynamic).** You're poking a running system. Authorized only - see gate above.

Per-category commands, grep patterns, and OWASP specifics live in `references/checklist.md` - work from it during the pass.

## Decision rules

- Any string-built SQL, shell command, or template fed user input is a blocker - parameterized queries and arg arrays only.
- Validate every external input at the boundary with a schema; type coercion is not validation.
- Authorization is per-request, not per-session: every endpoint checks "can THIS user access THIS resource?" - IDOR is one missing check away.
- Secrets live in env or a secret store; hardcoded fallback credentials and committed `.env` files are blockers.
- Use library crypto primitives only - never roll your own, never `Math.random()` for tokens, never fast hashes for passwords.
- `Access-Control-Allow-Origin: *` with credentials is a blocker; JWTs are verified (signature, `alg`, `exp`) before their claims are read.
- Server-side fetches of user-supplied URLs are SSRF until proven otherwise - allowlist hosts and block metadata/link-local ranges.
- JSON is safe to deserialize; every richer format on untrusted input needs scrutiny.
- Untrusted LLM input is data, not instructions - delimit it, and never act on model output without verification.

## Codebase review categories

Work through each; detail in the reference checklist.

Secrets & credentials / Input validation / Injection / Authn & Authz / XSS & output encoding / CSRF & CORS / SSRF / Crypto / Deserialization / Supply chain / Logging & monitoring / LLM-specific (when applicable).

## Live target categories (authorized only)

Recon / Auth surface / Web app / API / Infra.

## Reporting findings

Severity: Blocker (correctness, security, data loss) / Should-fix (compounding design debt) / Nit.

For each finding give:
- **Severity** - from the ladder above, with reasoning.
- **Location** - file path + line, or URL + parameter.
- **Reproduction** - concrete steps or a curl one-liner.
- **Impact** - what an attacker gets.
- **Remediation** - the specific fix, not "improve security."

## Out of bounds (do not assist)

- Targets the user has not shown authorization for.
- Mass exploitation, ransomware, destructive payloads.
- Detection-evasion for malicious purposes.
- Supply-chain compromise of third-party packages.
- DoS / DDoS testing without explicit written approval.
