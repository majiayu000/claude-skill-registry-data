---
name: securing-code
description: |-
  Use when writing or reviewing code that handles external input, manages access, touches data or crypto, or changes dependencies. Triggers: endpoints, auth/authz, DB/ORM, file handling, secrets, "is this secure?", "security review". NOT for formatting, pure UI, or explaining code.
---

# Securing Code

## When to Use

- Implementing any feature, endpoint, service, or component
- Writing auth, session management, or access control logic
- Handling file uploads, secrets, crypto, or sensitive data
- Reviewing code changes for security issues
- Checking a diff, branch, or PR for security correctness

## When Not to Use

- General code review without a security focus — `code-review` invokes this skill internally for its security lens
- Explaining code without modifying it
- Formatting or linting only
- Writing documentation unrelated to security controls

## Invocation Notice

- Tell the user when this skill is running: `securing-code`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

---

## Tier 1 — Core Principles (Apply to Every Task)

These apply regardless of task type — implementation or review.

### Secure Design Principles

- **Assume breach** — design as if the system will be compromised; no single point of trust
- **Validate all external input** — reject anything invalid; never try to "fix" bad input
- **Validate first, then escape** — for the output context; use sanitization only when escaping is not possible, via a hardened library; prefer allowlists over blocklists
- **Fail closed** — on error, roll back completely and deny access; never fail open
- **Least privilege** — grant minimum permissions necessary at every layer
- **Defense in depth** — layer controls; never rely on a single protection
- **Zero trust** — verify on every request, not just once at login

### Code Generation Requirements

All of the following must be satisfied when generating or modifying code:

01. **Parameterized queries** for all database access (SQL and NoSQL) — never concatenate user input
02. **Framework-native auth** — use framework or third-party auth/session/access-control; do not build custom authentication
03. **Per-request authorization** — enforce on every endpoint, AJAX call, page, and resource request including object-level checks
04. **Secret management** — load secrets from a secret manager; never hardcode keys, tokens, or passwords
05. **Approved cryptography** — AES-256-GCM for encryption, SHA-256/SHA-3 for hashing, Argon2id for passwords, Ed25519/ECDSA P-256 for signatures
06. **Context-aware output encoding** — encode all user-controlled data before rendering (HTML, JS, URL, CSS contexts)
07. **Safe error handling** — catch all exceptions, log details internally, show generic messages to users; fail closed with full rollback
08. **Rate limiting** — apply on all endpoints; no wildcard boundaries (`*`); no unlimited operations
09. **No unsafe deserialization** — never deserialize untrusted data; never pass user input to system calls
10. **Memory-safe languages preferred** — if C/C++, apply bounds checking and safe functions
11. **Security headers and cookies** — set security headers; use `Secure`, `HttpOnly`, `SameSite=Lax` (Strict for high-risk sessions); if `SameSite=None`, pair with `Secure` + CSRF defenses
12. **CSRF protection** — enable when the framework supports it for state-changing operations; add manually if not
13. **Deployment hygiene** — never run as root in production; initialize all variables; treat compiler warnings as errors

### High-Risk Changes — Confirm Before Implementing

The following categories have a large blast radius or affect the trust model.
Surface them and get explicit user approval before writing code, even if the user's request implies them:

- New or modified authentication / session flow (login, MFA, password reset, OAuth callback)
- New CORS configuration or relaxing an existing one (added origins, `credentials: true`, wildcard)
- New external service integration (third-party API, webhook receiver, OAuth provider)
- New file upload, download, or user-controlled storage path
- New category of sensitive data being stored (PII, payment, health, credentials)
- Granting elevated permissions, new roles, or service-account scope expansions
- Disabling, loosening, or bypassing rate limits, security headers, CSP, or framework auto-escaping
- Changes to cryptographic primitives, key rotation, or token lifetimes

For these, state what is changing and the risk, then wait for confirmation.
A user request to "add login" is permission for the feature, not for a specific auth design — confirm the design first.

### Response Behavior

- **State security assumptions** before writing code (auth model, data classification, framework)
- **Flag skipped requirements** — anything simplified or omitted for brevity is a gap attackers find
- **Append "Security Notes"** to all code responses: what the code does to meet each requirement, and what the developer still needs to configure (headers, secrets, IAM, logging)
- **Never propose insecure shortcuts** "for simplicity" or "for now"
- **Document exceptions explicitly** — if a business requirement forces a deviation, state it and propose the safest alternative

### Counter-Rationalizations

Push back on these framings — from the user or yourself — when they appear as justification for skipping a control:

| Rationalization                                  | Reality                                                                           |
| ------------------------------------------------ | --------------------------------------------------------------------------------- |
| "It's an internal tool, security doesn't matter" | Internal tools get compromised; attackers pivot through the weakest link.         |
| "We'll add security later"                       | Retrofitting is far harder than building it in; "later" usually means "in prod".  |
| "No one would try to exploit this"               | Automated scanners find everything reachable; obscurity is not a control.         |
| "The framework handles it"                       | Frameworks provide tools, not guarantees — they still have to be wired correctly. |
| "It's just a prototype / spike / demo"           | Prototypes ship. The auth shortcut becomes the production auth.                   |
| "This endpoint isn't exposed publicly"           | Network boundaries change; SSRF, misconfig, and lateral movement reach it anyway. |

---

## Routing

### Implementation Tasks

1. Apply Tier 1 above (always)

2. Open `references/tier2-implementation.md` and follow the checklist for your task type:

   | Task                                | Section |
   | ----------------------------------- | ------- |
   | General feature / component         | §2.1    |
   | REST or GraphQL API endpoint        | §2.2    |
   | Auth, sessions, or access control   | §2.3    |
   | Secrets, crypto, or data protection | §2.4    |
   | Supply chain or CI/CD               | §2.5    |

3. For security-complex domains, also load the matching Tier 3 reference:

   | Domain                  | Reference                              |
   | ----------------------- | -------------------------------------- |
   | Input handling          | `references/tier3-input-validation.md` |
   | File upload / download  | `references/tier3-file-upload.md`      |
   | Database-heavy features | `references/tier3-database.md`         |
   | Auth / session flows    | `references/tier3-threat-modeling.md`  |
   | C / C++ / embedded      | `references/tier3-memory-safety.md`    |

### Review Tasks

1. Apply Tier 1 above (always)
2. Load `references/tier2-review.md` for the review workflow and checklist
3. Load relevant Tier 3 references for the domains covered by the change (same routing table as Implementation Tasks above)
4. Use `references/owasp-2025.md` to verify coverage against all 10 OWASP categories

---

## References

- `references/tier2-implementation.md` — task-specific implementation checklists (§2.1–§2.5)
- `references/tier2-review.md` — code review workflow, OWASP-mapped checklist, output format
- `references/tier3-input-validation.md` — allowlist validation, output encoding, CSP
- `references/tier3-file-upload.md` — file upload validation, storage, retrieval
- `references/tier3-database.md` — injection prevention, DB access control, encryption
- `references/tier3-error-handling.md` — safe error handling, security event logging
- `references/tier3-memory-safety.md` — C/C++ memory safety, compiler flags, sanitizers
- `references/tier3-language-specific.md` — Python, JS/Node, Java, C#/.NET forbidden patterns and safe alternatives
- `references/tier3-threat-modeling.md` — STRIDE, trust boundaries, risk rating
- `references/owasp-2025.md` — OWASP Top 10 2025 with control mapping to skill tiers
