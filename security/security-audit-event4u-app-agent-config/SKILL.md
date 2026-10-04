---
model_tier: high
name: security-audit
description: "Security audit — vulnerability scan, pentest review, attack-surface sweep; explicit request only, not regular feature work. Pre-implementation threat pass → threat-modeling."
domain: quality
parallelizable: files
workspaces:
  - engineering
packs:
  - engineering-base
---

# security-audit

## Mission

Find real security vulnerabilities in code before they are exploited. This skill is
**proactive** — it audits code for security weaknesses, not just responds to incidents.

For writing secure code patterns (policies, auth, CSRF), use the `security` skill instead.

## When to use

Use this skill when:

- Auditing a codebase or module for security risks
- `analysis-autonomous-mode` routes here after detecting risky patterns
- Reviewing code that handles user input, authentication, or authorization
- Checking for vulnerabilities before a release or deployment

Do NOT use when:

* Writing new auth/policy code — route to [`security`](../security/SKILL.md)
* Hunting for functional bugs — route to [`bug-analyzer`](../bug-analyzer/SKILL.md) (proactive mode)
* Investigating performance — route to [`performance-analysis`](../performance-analysis/SKILL.md)
* You need a pre-implementation threat model for a new feature — route to
  [`threat-modeling`](../threat-modeling/SKILL.md)
* You need end-to-end authorization analysis for one route/action — route to
  [`authz-review`](../authz-review/SKILL.md)

## Procedure: Security audit

### 0. False-positive gate — restate the claim before reporting

Before any finding enters the report, restate it as one falsifiable sentence
naming all three of:

1. **Privilege level** — what access the attacker already has (anonymous,
   authenticated user, tenant admin, CI runner).
2. **Execution context** — where the vulnerable code runs (request handler,
   queue worker, sandboxed template, build step).
3. **Attacker precondition** — the concrete state or input the attacker must
   control to trigger it.

If any of the three cannot be named concretely, the item is **not a finding
yet** — trace further or drop it with a one-line reason.

**Rationalizations to Reject:**

| Rationalization | Reality |
|---|---|
| "It looks dangerous" | Pattern-recognition is not analysis — trace the full data flow from entry to sink first |
| "This is clearly critical" | Complete a devil's-advocate pass — models systematically overrate severity |
| "Report it just in case" | Over-reporting erodes trust; an unverifiable finding is noise, not diligence |
| "Same pattern as a known CVE" | Same pattern ≠ same preconditions — verify the preconditions hold in THIS codebase |

**Standard vs. Deep verification routing:**

- **Standard** — traced data flow + all three claim elements named → report
  with the normal field list.
- **Deep** — severity would be High/Critical, OR the precondition chain
  crosses a trust boundary you did not personally trace → run a
  devil's-advocate pass first: actively try to refute the finding (existing
  middleware? framework default? type system? config?). Report only what
  survives; findings the pass killed are listed one-line under
  *Rejected candidates* so the triage is auditable.

### 1. Map attack surface

Identify all entry points where untrusted data enters:

- HTTP request parameters, headers, cookies
- File uploads
- API payloads (JSON, XML, form data)
- Webhook callbacks
- Queue job payloads from external sources
- Import files (CSV, Excel, XML)
- URL path segments and query strings

### 2. Trace trust boundaries

For each entry point, trace where user input flows:

```
User Input → Controller → Validation → Service → DB/File/External
                 ↓              ↓           ↓
            Is it sanitized?  Complete?  Used safely?
```

### 3. Check vulnerability categories

| Category | What to look for |
|---|---|
| **SQL Injection** | Raw queries with concatenation, missing parameter binding |
| **XSS** | Unescaped template output (Blade `{!! !!}`, JSX `dangerouslySetInnerHTML`, Jinja `|safe`), JSON responses with HTML |
| **CSRF** | Missing middleware, API endpoints without token verification |
| **Auth bypass** | Missing policy checks, broken gate logic, `withoutMiddleware()` |
| **IDOR** | Direct object access without ownership verification |
| **Mass assignment** | Missing `$fillable`/`$guarded`, `request()->all()` in create/update |
| **File upload** | Missing type validation, path traversal, executable uploads |
| **SSRF** | User-controlled URLs passed to HTTP client |
| **Deserialization** | Unserializing user input, unsafe queue payloads |
| **Secret exposure** | Hardcoded credentials, secrets in logs, `.env` in public dir |
| **Rate limiting** | Missing throttle on auth endpoints, password reset, API |
| **Header injection** | User input in response headers, email headers |
| **Insecure defaults / fail-open** | Guards that allow on error (`catch { return true }` in an authz check), default-allow matchers, debug mode defaulting on, permissive CORS/`verify=false` fallbacks, feature flags whose missing value grants access |

Worked example (fail-open): `if (!$gate->check($user)) { … }` wrapped in a
`try/catch` that logs and **continues** fails open — an exception in the gate
grants access. Finding shape: Category *Insecure defaults*, Evidence the
catch block `file:line`, Fix *fail closed — rethrow or deny on gate error*.

### 3b. Out of scope — route, do not guess

The table above names vulnerability **classes**, which are stable. This package
carries no cryptographic parameter, key size, work factor, cipher suite, or TLS
version floor: a value copied here reads authoritative long after it stops being
true. Report the finding, route the fix to
<https://cheatsheetseries.owasp.org/> — Cryptographic Storage, Transport Layer
Security, Password Storage, XML External Entity Prevention — and never name a
value from memory. Rationale and reopening condition:
[ADR-238](../../../docs/decisions/ADR-238-security-content-routes-to-external-authority.md).

### 4. Framework-specific checks

→ Laravel-specific checks: see [`laravel`](../laravel/SKILL.md) § Security audit checks.

### 5. Dependency audit

- Check `composer.lock` for known vulnerable packages
- Check `package-lock.json` for frontend vulnerabilities
- Identify outdated packages with known CVEs
- Check if security patches are available

## Output format

1. Emit one entry per vulnerability using the field list below; one finding = one block, never merge.
2. Category must map to an OWASP Top 10 (or LLM Top 10) bucket; Severity must use Low / Medium / High / Critical with a single Exploitability tag.
3. Close with a *Recommended Fix Order* ranked by exploitability × blast radius and tag each line with Confidence.

For each vulnerability:

- **Vulnerability:** concise title
- **Category:** OWASP category (Injection, Broken Auth, etc.)
- **Location:** file and line
- **Severity:** Low / Medium / High / Critical
- **Exploitability:** How easy to exploit (trivial / requires auth / complex)
- **Impact:** What an attacker could achieve
- **Evidence:** code reference showing the weakness
- **Fix:** concrete mitigation
- **Confidence:** Low / Medium / High

After the findings, add a **Rejected candidates** section: one line per
look-dangerous-but-benign pattern the Step-0 gate killed, with the traced
reason ("raw SQL string is a static migration constant — no user input
reaches it"). An audit that rejects nothing has usually skipped the gate.

## Integration with other skills

- **analysis-autonomous-mode** — routes here when security concerns are detected
- **security** — complementary: security is about writing secure code, this is about finding holes
- **universal-project-analysis** — provides context about packages and framework usage
- **bug-analyzer** — some bugs have security implications (chain when found)
- **untrusted-input-defense** / **lethal-trifecta-guard** (rules) — prompt-injection / agent-config defense; consult when the audited code ingests untrusted content or wires an autonomous egress path

## Gotcha

- Don't report theoretical vulnerabilities without a concrete attack vector — false positives erode trust.
- The model tends to flag framework-handled security as issues (e.g., Laravel's CSRF or Rails' `protect_from_forgery` is already handled).
- Always check if a finding is already mitigated by middleware or configuration before reporting it.

## Do NOT

- Do NOT report theoretical risks that require impossible preconditions
- Do NOT ignore user input flows — always trace from entry to usage
- Do NOT assume frameworks handle everything — verify middleware and config
- Do NOT confuse code quality issues with security vulnerabilities
- Do NOT skip dependency checking — known CVEs are real risks

## See also

- [`docs/threat-model.md`](../../../docs/threat-model.md) — package attack surface and trust boundary documentation.
