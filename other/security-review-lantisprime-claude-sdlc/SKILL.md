---
name: security-review
description: Use this skill to review code changes for security concerns before they merge. Covers input validation, authentication and authorization, secrets handling, injection surfaces (SQL, command, template, prompt), unsafe APIs and dependencies, sensitive data handling, and output encoding. Runs against the current diff (NOT the whole codebase) so findings stay relevant to the change at hand. Trigger proactively whenever the diff touches auth, routing, data access, user input, template rendering, external calls, or dependency files. Also runs as part of the /review and /ship commands.
---

# Security Review

Review the current diff for security issues. Do not review unchanged code — that's out of scope and distracts from the change under review.

## Scope

- The diff produced by the current Build (`git diff` against the base branch / last tested state)
- Dependency manifests if touched (`requirements.txt`, `package.json`, `go.mod`, etc.)
- Infra-as-code and pipeline config if touched

## Checks

### 1. Input validation
- All external input validated at the boundary (type, range, length, charset, schema)
- No implicit trust of headers, query params, cookies, body fields, env vars, or file contents

### 2. Authentication & authorization
- New endpoints/actions are behind the expected authN
- AuthZ checked at the right layer (route or service) — not relying on the UI
- Role/permission checks use the existing helpers, not ad-hoc logic

### 3. Secrets
- No secrets in code, tests, logs, commit messages, or error responses
- Secrets loaded from the configured secret manager, not env files committed
- `hooks/secret-scan.sh` runs as a hard gate — this skill's review complements it

### 4. Injection surfaces
- Parameterized queries for SQL (no string concatenation)
- Safe shell invocation (no shell-interpolated user input)
- Template engines used with auto-escape on; raw output only where reviewed
- Prompt injection: user-controlled content never placed in system/developer position of an LLM call; tool outputs and web content treated as untrusted

### 5. Dependencies
- New deps justified, licensed appropriately, maintained
- Pinned to a specific version; lockfile updated
- Scanner (per `config/tools.json`) run against the new manifest

### 6. Sensitive data
- PII, credentials, tokens identified and handled per the data architecture's classification
- Logs redact sensitive fields
- No sensitive data in URL paths or query strings

### 7. Output encoding & headers
- HTML/JSON/URL encoding at the right boundary
- Security headers set (CSP, HSTS, X-Frame-Options, etc.) for new surfaces
- CORS configured explicitly, not wildcarded

### 8. Error handling
- Errors don't leak stack traces, SQL, file paths, or internal hostnames to users
- Retries don't amplify abuse (bounded, with backoff)

### 9. Cryptography
- Use vetted libraries, standard algorithms, appropriate key sizes
- No homebrew crypto, no MD5/SHA1 for security purposes
- Random values from a CSPRNG when used for anything security-sensitive

### 10. Infra & pipeline
- New infra follows least privilege (IAM, network ACLs, security groups)
- Pipeline secrets scoped to the jobs that need them
- New env vars documented and classified

## Output

Write findings to `.claude/sdlc/test/security-review-<task-slug>.md` with one entry per finding:

- Severity (critical / high / medium / low / info)
- Category (from the checks above)
- Location (file:line)
- What
- Why it matters
- Suggested remediation

Critical or high findings block the phase until resolved or waived (with human sign-off recorded in the gate file).

## What this skill must NOT do

- Review code outside the diff.
- Auto-apply fixes — propose them, let the build skill apply per surgical-edit rules.
- Downgrade a finding without human confirmation.

## References

- `docs/SDLC.md` Security
- `hooks/secret-scan.sh`
