---
name: security-misconfiguration
description: Detects insecure defaults, overly permissive CORS, exposed debug endpoints,
  and missing security headers. Use when writing server configuration, setting
  environment variables, configuring CORS policies, enabling debug modes,
  setting up default credentials, or deploying application infrastructure.
  Also invoke when writing security headers middleware.
---

# Security Misconfiguration Security Check (A02:2025)

## What this checks

Protects against insecure defaults, overly permissive policies, and missing hardening
that expose the application to cross-origin attacks, credential stuffing, and
information disclosure via error pages or debug endpoints.

## Vulnerable patterns

- Wildcard CORS origin combined with credentials enabled — every site on the web gets cookie-authenticated access
- Debug or verbose-error mode hardcoded on, exposing tracebacks, route lists, or interactive consoles in production
- Wildcard or empty host/origin allowlist accepted in production configuration
- HTTP server with no security-headers layer registered — `Strict-Transport-Security`, `X-Content-Type-Options`, and a framing/CSP control missing. For hardcoded secrets see `hardcoded-secrets`.

## Fix immediately

Flag the vulnerable code, explain the risk, and suggest a fix establishing these
properties. Translate to the language and framework of the audited file — use that
stack's documented middleware or configuration helpers; do not import recipes from a
different stack.

1. **CORS that allows credentials uses an explicit origin allowlist.** Never a wildcard, never a reflected `Origin` header. Browsers block wildcard-plus-credentials in spec, but misconfigured middleware still ships it.
2. **Debug and verbose-error flags default to off in production.** Their values are sourced from environment or config, not hardcoded on. A production-only assertion that fails loudly when debug is left enabled catches misconfigured deploys.
3. **Every HTTP server registers a security-headers layer before routes.** Baseline: `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, and a framing or CSP control. An upstream proxy may own these instead — but only if that ownership is documented at the call site.
4. **Host and origin validation uses an explicit allowlist**, never a wildcard or an empty default. Trusted-origin and CSRF-trusted-origin lists are attacker-reachable when unset.

## Verification

Confirm the following *properties* hold (language-agnostic):

- [ ] For every CORS configuration present in the code, if credentials are allowed then the allowed-origins value is an explicit allowlist — never a wildcard (`*`) or a reflected `Origin` header
- [ ] For every debug/development flag present in the code, the value is sourced from an environment variable or config and defaults to off in production
- [ ] For every HTTP server or router present in the code, a security-headers layer is registered before routes, setting at minimum `Strict-Transport-Security`, `X-Content-Type-Options`, and a framing/CSP control — unless the code comments explicitly document that an upstream proxy owns these headers
- [ ] Host or trusted-origin allowlists are explicit values, not wildcards or empty defaults

## References

- CWE-16 ([Configuration](https://cwe.mitre.org/data/definitions/16.html))
- CWE-732 ([Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html))
- [OWASP A02:2025 Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
