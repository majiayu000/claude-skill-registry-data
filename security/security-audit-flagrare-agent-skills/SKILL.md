---
name: security-audit
description: "Focused security review of a change. Finds HIGH-CONFIDENCE, concretely exploitable vulnerabilities in the staged diff (injection, broken authn/authz, secrets and data exposure, unsafe deserialization, crypto misuse, SSRF) and audits dependencies when a lockfile moved, using the repo's own package manager. Runs as Check 7 of /flagrare:implementation-review, and standalone when the user says 'security review', 'security audit', 'check this for vulnerabilities', 'is this safe', 'any security holes', 'threat check', or before shipping anything that touches auth, user input, secrets, or untrusted data. Reports only findings with a concrete exploit path, never theoretical noise."
---

# Security Audit

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook that flags em-dashes in generated `.md`. See `/flagrare:write-docs`.

A focused security pass over a change. The job is narrow on purpose: find the vulnerabilities that a senior security engineer would confidently raise in review, and stay silent about everything else. A security review that flags twenty theoretical issues gets ignored; one that flags the two real ones gets acted on. Noise is the enemy, not thoroughness.

This skill is the single source of security truth for the collection. It runs two ways:

- **As Check 7 of `/flagrare:implementation-review`**, a parallel subagent whose brief pulls in this skill's content, the same way Checks 2 to 4 pull in `/flagrare:testing-philosophy`. Diff-scoped, fast.
- **Standalone** (`/flagrare:security-audit`), when you want a deliberate pass on demand.

---

## The one rule that matters

**Only report a finding you can attach a concrete exploit path to, and only when you are over 80% confident it is actually exploitable.** Everything else in this skill serves that rule.

A finding is worth reporting when you can name the untrusted input, trace it to the dangerous sink, and describe the attack in a sentence. If you cannot do that, it is a hunch, and a hunch in a security report is noise that trains the reader to skip the whole thing.

Score every candidate before reporting it:

| Confidence | Meaning | Action |
|---|---|---|
| 0.9 to 1.0 | Certain exploit path, you could write the payload | Report |
| 0.8 to 0.9 | Clear known-bad pattern with a real trigger | Report |
| 0.7 to 0.8 | Suspicious, needs specific conditions to fire | Report only if HIGH impact |
| below 0.7 | Speculative | Drop it, do not mention it |

---

## What to examine

**Resolve the scope first, because it differs by how the skill was invoked:**

- **As Check 7 of `implementation-review`** (a commit gate): the **staged diff**, `git diff --staged`. That is exactly what is about to be committed.
- **Standalone** (`/flagrare:security-audit`): the change under review, which is rarely staged yet. Resolve it in this order and use the first that is non-empty: an explicit target the user named (a file, a path, "the auth changes"); the **branch diff against its base**, `git diff $(git merge-base HEAD origin/HEAD)...HEAD` plus uncommitted work (`git diff HEAD`); or, failing a base, the full working-tree diff. The point is to never review an empty `git diff --staged` and report "no vulnerabilities" when the actual change is sitting unstaged. If you truly cannot find a change to review, say so rather than reporting clean.

Whichever scope resolves, extend it to the **trust boundary it lands in**: a one-line change to an authorization check pulls in the surrounding auth path, not just the changed line, because the bug is usually in the code the diff assumes rather than the line it edits. Review security implications the change **newly introduces**. Do not audit pre-existing issues the change merely sits near; that is a separate, deliberate effort.

**Input validation and injection**
- SQL / NoSQL injection via unsanitized input reaching a query
- Command injection in system calls or subprocess arguments
- Path traversal in file operations built from user input
- Template injection in server-side templating
- XXE in XML parsing
- XSS: reflected, stored, DOM-based (see the React/Angular precedent below)

**Authentication and authorization**
- Authentication bypass logic
- Authorization gaps: IDOR, tenant-leak (the 403-vs-404 case), a missing ownership check on a resource
- Privilege escalation paths
- Session and JWT flaws

**Secrets and data exposure**
- Hardcoded API keys, passwords, tokens
- Secrets or PII written to logs
- Sensitive data leaking through an API response or debug output

**Crypto and code execution**
- Weak or misused crypto: `Math.random()` for tokens, static IV, ECB mode, weak password hashing
- Certificate validation bypass
- Unsafe deserialization: Python `pickle`, unsafe YAML load, Java/PHP object injection, `eval` on dynamic input
- SSRF where the attacker controls the host or protocol (path-only control does not count, see precedents)

---

## Methodology

Work in three phases. The first two are what separate a real review from pattern-matching on keywords.

**Phase 1: Understand the repo's security model.** Before judging the diff, look at how the codebase already defends itself. What validation and sanitization helpers exist? What auth middleware wraps the endpoints? Is there an ORM that parameterizes queries, or is it raw SQL? A finding only makes sense relative to the existing model: raw string interpolation is damning in a codebase that parameterizes everywhere, and expected in one that has its own escaping layer you have not read yet.

**Phase 2: Compare the change against that model.** Where does the diff deviate from the established secure pattern? New code that rolls its own auth check instead of using the middleware, or builds a query by hand where everything else uses the query builder, is where vulnerabilities enter. Deviation is the signal.

**Phase 3: Trace the data flow.** For each modified file, follow untrusted input from where it enters (request params, headers, uploaded files, external API responses) to where it does something dangerous (a query, a shell, a file path, an HTML render, a deserializer). A vulnerability is a path from a source to a sink with no adequate sanitization in between. If you cannot draw that path, you do not have a finding.

You do not need to run the code to confirm a vulnerability; read it. This pass is read-only for the code-vuln findings (the dependency audit below is the one exception that runs a tool).

---

## Dependency audit

When the staged diff touches a lockfile or manifest, a dependency was added or bumped, and a bump can pull in a version with a known published vulnerability (a CVE). Detect the repo's package manager from the lockfile present and run its native auditor. This is the one place the skill shells out.

| Ecosystem | Lockfile present | Command |
|---|---|---|
| npm | `package-lock.json` | `npm audit` |
| pnpm | `pnpm-lock.yaml` | `pnpm audit` |
| yarn | `yarn.lock` | `yarn npm audit` |
| Python | `poetry.lock`, `uv.lock`, `requirements*.txt` | `pip-audit` |
| Rust | `Cargo.lock` | `cargo audit` |
| Go | `go.sum` | `govulncheck ./...` |
| Ruby | `Gemfile.lock` | `bundle audit` |
| PHP | `composer.lock` | `composer audit` |

**Degrade gracefully.** If the detected auditor is not installed, do not fail the review and do not guess. Report a single advisory finding: "lockfile `<name>` changed and `<tool>` is not available; run your dependency auditor," and name the packages the diff added or bumped so the reader knows what to check.

When running inside `implementation-review` Check 7, scope the audit report to the packages the diff actually changed rather than the whole tree, so the commit gate stays fast and quiet. The full-tree audit is what a standalone run surfaces.

---

## False-positive precedents

These are the calls a security engineer makes automatically and a checklist gets wrong. Applying them is most of what keeps this review credible. Do **not** report:

1. **Denial of service, resource exhaustion, rate limiting.** Out of scope for this pass.
2. **Client-side auth or validation gaps.** Client-side JS/TS is untrusted by design; the server is responsible for validation. A missing check in the browser is not a vulnerability. The same holds for any flow that sends data to a backend: the backend owns validation.
3. **React and Angular XSS** unless the code uses `dangerouslySetInnerHTML`, `bypassSecurityTrustHtml`, or a similar explicit escape hatch. These frameworks auto-escape.
4. **SSRF that only controls the URL path.** SSRF matters when the attacker controls the host or protocol, not when they influence a path segment.
5. **Env vars and CLI flags treated as attacker-controlled.** In a normal deployment these are trusted. An attack that depends on setting an env var is not valid.
6. **Log spoofing / logging non-secret data.** Writing unsanitized input to a log is not a vulnerability. Logging secrets, passwords, or PII is; logging URLs and IDs is assumed safe.
7. **Memory-safety issues in memory-safe languages.** No buffer overflows or use-after-free in Rust, Go, JS, Python, and the like.
8. **Findings in test files or documentation.** Unit tests and `.md` files are not attack surface.
9. **Lack of hardening.** Code is not required to implement every best practice. Flag concrete vulnerabilities, not the absence of defense-in-depth.
10. **Theoretical race conditions and timing attacks.** Report only when concretely and practically exploitable.
11. **Low-impact web quirks** (tabnabbing, open redirects, prototype pollution, XS-Leaks) unless extremely high confidence.

Assume UUIDs are unguessable and do not need validation.

**Where we diverge from the built-in `security-review`:** it excludes dependency CVEs as "managed separately." We keep them, because they are a real and common way vulnerabilities ship, and because the audit is cheap and deterministic. That is the dependency-audit step above, kept separate from the code-vuln pass so the precedents here stay clean.

---

## Output format

Report findings in this shape, most severe first:

```
# Vuln 1: SQL injection: `api/users.ts:42`
- Severity: HIGH
- Confidence: 0.9
- Category: sql_injection
- Description: `userId` from the request query is interpolated directly into the SQL string, with no parameterization.
- Exploit: GET /users?id=1 OR 1=1 returns every user; a UNION payload reads adjacent tables.
- Fix: use the parameterized query builder already used in `api/orders.ts:88`.
```

For the commit-gate synthesis inside `implementation-review`, collapse to the house line format so it sits alongside the other checks:

```
Check 7 · Security
  ✓ No vulnerabilities in the diff
  ✗ `api/users.ts:42` SQL injection (HIGH): `userId` interpolated into query, use the parameterized builder
  ⚠ lockfile changed, `pip-audit` unavailable, run your dependency auditor (added: requests 2.19.1)
```

**Severity:** HIGH is directly exploitable (RCE, data breach, auth bypass). MEDIUM needs specific conditions but has real impact. LOW is a lower-impact or defense-in-depth issue. In the commit gate, HIGH and MEDIUM block; LOW is advisory. Report MEDIUM only when it is obvious and concrete.

---

## Flow position

```
/flagrare:staleness-audit
     ↓
/flagrare:implementation-review    ← Check 7 pulls in THIS skill
     ↓
git commit
```

Or standalone, any time a change touches auth, user input, secrets, or untrusted data, and before shipping anything security-sensitive.

---

## Anti-patterns

- Do not report a finding without a concrete exploit path. If you cannot describe the attack in a sentence, it does not go in the report.
- Do not audit pre-existing issues the diff merely sits near. Review what the change introduces.
- Do not fail the review when the dependency auditor is missing. Degrade to an advisory flag.
- Do not flag client-side auth, framework-safe XSS, or trusted env vars, the precedents exist so the review stays credible.
- Do not run the dependency auditor's full-tree output inside the commit gate, scope it to changed packages there.
- Do not pad the report to look thorough. Two real findings beat twelve maybes.
