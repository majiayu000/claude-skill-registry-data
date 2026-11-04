---
description: Comprehensive regulatory and architectural security review of the current repo matching Elite Security Architect standards (NIST SP 800-53 Rev 5, FedRAMP High, DoD IL6, SOC 2, ISO 27001/27040, NIS2). Produces severity-ranked, compliance-mapped findings. Does not auto-fix. Use when the user asks for a security audit, compliance review, or invokes /luismc-audits:security-audit.
model: opus
effort: medium
---

# Regulatory & Architectural Security Audit

Run a rigorous, multi-framework compliance and threat-modeling audit across the repository. This skill **identifies, verifies, and reports. It does not remediate**. Remediation is a deliberate follow-up step. This lets you triage and prioritize findings before any code changes.

## Process

1. **Orient & Scope:** Identify the technical stack (framework, auth patterns, data layers, transit points). Map the boundaries where multi-tenant data or different classification levels meet. Skip irrelevant checks to avoid "N/A" noise.
2. **Trace Code-Level Logic:** Do not rely on static configuration files. Read the actual execution paths for authorization, cryptographic operations, state management, and logging.
3. **Rigorous Verification:** Confirm candidate findings by tracing the exploit pathway from an attacker-controlled input/state to an unvalidated sink. If you cannot definitively verify a finding but it shows a valid defense-in-depth gap, state it explicitly as an unverified structural risk. Do not call it an absolute vulnerability.
4. **Token-Optimized Evaluation:** Use Claude Code's native file-viewing tools to preserve your **Prompt Cache** and keep input costs low. Avoid large code dumps and conversational filler in the output.

## Severity & Regulatory Rubric

Classify findings strictly by this architectural impact schema:

- **P0 (Critical) — High-Impact Exploit or Compliance Breach:** Remotely exploitable without authentication, breaks tenant/user isolation, compromises cryptographic keys, or directly violates **DoD IL6 / FedRAMP High** boundary rules (e.g., clear-text secrets in git history, complete AuthN bypass, unauthenticated raw data egress).
- **P1 (High) — Conditional Exploitation or Regulatory Deficit:** Exploitable with specific preconditions (authenticated session, race conditions, local network presence), or breaches explicit statutory mandates from **NIS2 / ISO 27001** (e.g., missing multi-tenant validation on data mutations, weak hashing/ciphers).
- **P2 (Medium) — Defense-in-Depth Gap:** Weakened or missing structural controls that need a multi-step chain of events to exploit, or missing **SOC 2 Type II / ISO 27040** best practices (e.g., lack of data-at-rest encryption for sensitive fields, inadequate rate limiting).
- **P3 (Low) — Hardening & Hygiene Opportunity:** Standard code hardening or best-practice deviations with no immediate exploit vector or regulatory penalty.

## Compliance Checklist

### 1. Cryptographic Isolation & Data Sovereignty (DoD IL6 / FedRAMP High / NIST SP 800-53)
- **Boundary Leakage:** Ensure clear logical separation between tenants, environments, or data classification zones. Verify that cross-boundary spillage is structurally impossible.
- **Zero-Trust Access Control:** Validate that authorization checks (`AuthZ`) are computed statelessly at every single API, route, or server-side component endpoint. Client-side state hiding must never be trusted.
- **Session Mutation Hardening:** Ensure session tokens and JWTs enforce strong cryptographic signatures and strict expiration windows. Ensure they explicitly block algorithm confusion (e.g., rejecting `alg: none`).

### 2. Storage Security & Cryptographic Sanitation (ISO/IEC 27040 / NIST SP 800-53)
- **Data-at-Rest Protection:** Verify that PII, system secrets, access tokens, and sensitive database columns use robust encryption primitives (FIPS 140-3 validated modules where applicable). Reject legacy or broken ciphers (e.g., 3DES, RC4, MD5).
- **Cryptographic Shredding:** Audit data deletion routines. Ensure that when a resource is deleted, the application invokes verified cryptographic sanitation pathways. These securely destroy or overwrite the underlying decryption keys or file blocks.
- **In-Transit Integrity:** Ensure strict enforcement of TLS 1.2/1.3 across all transit layers. Audit headers for HSTS (`Strict-Transport-Security`) execution.

### 3. Non-Repudiation, Logging, & Info Leakage (SOC 2 Type II / NIS2)
- **Immutable Security Trails:** Audit system loggers. Verify that high-value transactions (privilege escalations, authentication state changes, data exports) generate tamper-evident logs that local application sub-processes cannot modify.
- **Log Sanitation:** Ensure that loggers actively block and scrub PII, raw passwords, authentication tokens, or internal memory stack traces before writing to persistent disks.
- **Production Error Handling:** Ensure that production suppresses verbose framework error pages, database stack traces, and internal routing exceptions, and replaces them with generic handles.

### 4. Supply Chain Resilience & Infrastructure Injection (NIS2 / ISO 27001)
- **Dependency Hardening:** Scan for transitive dependencies or out-of-date packages that contain open CVE vectors. Ensure dynamic inputs fed into third-party binaries are thoroughly sanitized.
- **Injection Prototyping:** Audit all input targets. Block raw string concatenation in SQL queries. Prevent user inputs from touching shell execution hooks (`exec`/`spawn`). Ensure strict sanitization of user-supplied URLs to block Server-Side Request Forgery (SSRF).

### 5. Specialized Tech Stack Controls (PostgreSQL, Redis, Drizzle ORM)
- **Drizzle RLS & Tenant Scoping (FedRAMP High):** Audit all Drizzle query builders (`db.select`, `db.update`, `db.delete`). Confirm that EVERY multi-tenant table mutation explicitly binds a `tenant_id` or `user_id` conditional clause, or verifies that native PostgreSQL Row-Level Security (RLS) is enabled on the schema.
- **Redis State Validation (SOC 2 Type II):** Trace Redis client hooks (`redis.get`, `redis.hget`). Ensure that data extracted from Redis caches or session stores is strictly validated against a compile-time schema runtime (e.g., Zod) before properties are passed to authentication contexts.
- **Data Erasure Execution (ISO 27040):** Verify that when a delete path is called via Drizzle, sensitive columns are cryptographically sanitized, or a database `VACUUM` strategy is considered for hard-purges of local data fragments.

## Output Formatting

**No Conversational Fluff.** Omit greetings, summaries, and post-audit commentary. Go directly to the findings table or list, ordered from highest severity (P0) to lowest (P3). If no issues survive the verification phase, state clearly: `[OK] No regulatory or architectural vulnerabilities detected.`

For each finding, you must output exactly this structural template:

*   **Finding [ID]: [Short, Descriptive Defect Name]**
    *   **Severity:** [P0 / P1 / P2 / P3]
    *   **Regulatory Mapping:** [e.g., NIST SP 800-53 AC-2, ISO/IEC 27040 Sec 6.4, FedRAMP High, NIS2 Art 21]
    *   **Location:** `[File path]:[Line number]`
    *   **Defect Statement:** One sentence explaining the vulnerability or architectural deficit.
    *   **Concrete Failure Scenario:** A specific, technical description of how an attacker or an unauthorized state can exploit this flaw to cause a direct breach or compliance failure.
