---
name: "trust-compliance"
description: "Legal, security, privacy, and deliverability requirements every delivered app must satisfy — legal pages, PII/deletion rights, CSP/Trusted-Types/Zod, AI-agent security, RFC7807 errors, email domain auth."
triggers:
  - "security"
  - "privacy"
  - "legal"
  - "compliance"
  - "csp"
priority: 2
pack: "security"
stage: stable
---

# Trust, Security & Compliance — every app must satisfy

## Legal & policy

- Ship real `/privacy`, `/terms`, `/accessibility` pages accurate to the ACTUAL data practices — never boilerplate that lies. Accessibility statement is ADA Title II / WCAG 2.2 AA-ready.
- No dark patterns — honest defaults, no forced continuity, no confirm-shaming (Christ-like ethos).

## Data & PII

- Collect the minimum PII needed; never log secrets or PII in plaintext; keep credentials server-side only.
- Honor user right-to-deletion and data export on request. State retention plainly.

## Security controls (every app)

- CSP Level 3 `strict-dynamic` + per-request nonce · Trusted Types · HSTS. No inline script without a nonce.
- Zod validation at EVERY runtime boundary (env · API in/out · params · forms · webhooks · queue/DO messages · AI outputs) — validation is a security control, not just typing.
- Forms gated by Turnstile. All hyperlinks valid (no dead/hostile links).
- Tenant isolation: `org_id` on every row + query; 404 (never 403) on cross-tenant access.

## AI-agent security

- Treat all model/tool input as untrusted: defend against prompt injection; authorize every tool call; validate + schema-bind every AI output before use (Contract-First AI). Sandbox generated/risky code before it runs.

## Errors (never leak internals)

- User-facing errors use RFC7807 envelopes: `code` + `correlationId` + `errors[]` + what-to-do-next. Never expose stack traces, SQL, or internal identifiers.

## Email domain authentication

- Sending domain publishes SPF + DKIM + DMARC (BIMI where a VMC exists). These records live on the SENDING domain's zone (may differ from the site domain — surface any mismatch before staging).
