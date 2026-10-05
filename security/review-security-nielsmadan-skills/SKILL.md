---
name: review-security
description: Security audit for vulnerabilities, secrets, and unsafe patterns. Use before releases, after adding auth code, or when reviewing third-party integrations.
argument-hint: '[--staged | --unpushed | --changed | --all]'
effort: xhigh
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Security

Security audit for common vulnerabilities and unsafe patterns.

## Usage

```
/review-security              # Review context-related code
/review-security --staged     # Review staged changes
/review-security --unpushed   # Review files changed across all unpushed commits
/review-security --changed    # Review unstaged changes
/review-security --all        # Full codebase audit (parallel agents)
```

## Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related code | Files from the current conversation context: any files the user has discussed, opened, or that you have read/edited in this session. If no conversation context exists, ask the user to specify files or use `--staged`/`--changed`/`--all`. |
| `--staged` | Staged changes | `git diff --cached --name-only` |
| `--unpushed` | Files changed across unpushed commits | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD` |
| `--changed` | Unstaged changes | `git diff --name-only` |
| `--all` | Full codebase | Glob source files, parallel agents |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope.

**Do NOT skip checks:**
- "This code is internal only" -- Internal code gets compromised too
- "This is just a prototype" -- Prototypes become production code
- "I already checked for the obvious issues" -- The non-obvious ones are the dangerous ones

## Gotchas
- Dependency audit commands (`pip-audit`, `safety check`, `bundle audit`, `govulncheck`) must be installed separately. If missing, they silently produce no output rather than erroring.
- `--staged`, `--unpushed`, and `--changed` review the full file content, not just the diff. Pre-existing vulnerabilities in the file are flagged even if the staged/unstaged/unpushed change is unrelated.

## Workflow

1. **Determine scope** based on flags (see Scope table above)
2. **Review each file** against the Security Checklist below, prioritizing categories in this order:
   1. Injection (OWASP 2021 A03) — highest exploitation likelihood
   2. Sensitive Data Exposure (OWASP 2021 A02) — hardcoded secrets are easy wins
   3. Broken Authentication (OWASP 2021 A07) — auth bugs have outsized impact
   4. Security Misconfiguration (OWASP 2021 A05) — config issues are common in PRs
   5. Dependency Vulnerabilities — run audit commands last (they take time)
3. **Parallelize** if scope has >5 files: spawn one sub-agent per checklist category, each scanning all files. Merge results and deduplicate.

   Dispatch workers that return findings without editing files. Disable delegation tools where supported; read-only access alone does not prevent delegation. Any coordinating role needs explicit subtasks, a descendant limit, and a stopping condition in its brief.
4. **Check dependencies** using the ecosystem-specific commands in the Dependency Vulnerabilities section
5. **Classify severity** for each finding:
   - **Critical**: Exploitable vulnerability with direct user/data impact (e.g., SQL injection on a public endpoint, hardcoded production secret)
   - **High**: Vulnerability requiring specific conditions to exploit but with serious impact (e.g., XSS in admin panel, missing rate limiting on login)
   - **Medium**: Security weakness that increases attack surface (e.g., overly permissive CORS, debug mode flag)
   - **Suggestion**: Defense-in-depth improvement (e.g., adding CSP headers, tightening cookie flags)
6. **Report findings** grouped by severity using the Output Format below

## Security Checklist

> References below use OWASP Top 10 2021 category numbers (A01–A10).

For code examples, grep patterns, false-positive rules, and dependency audit commands, see `references/security-checklist.md`.

### Injection (OWASP A03)

- [ ] No string concatenation in SQL queries (use parameterized queries)
- [ ] No unsanitized user input passed to shell commands
- [ ] No direct HTML insertion from user content (use textContent or a sanitizer)

### Broken Authentication (OWASP A07)

- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] Rate limiting on login endpoints
- [ ] Session tokens are secure (HttpOnly, Secure, SameSite)
- [ ] No credentials in URLs or logs
- [ ] Account lockout after failed attempts

### Sensitive Data Exposure (OWASP A02)

- [ ] No hardcoded secrets, API keys, or passwords in source code (use environment variables)
- [ ] No sensitive fields (passwords, tokens) written to logs
- [ ] Grep source files for secret patterns — see `references/security-checklist.md` for patterns and false-positive filtering rules

### Security Misconfiguration (OWASP A05)

- [ ] Debug mode disabled in production
- [ ] No default/test credentials
- [ ] Error messages don't expose internals
- [ ] CORS properly configured (not `*` for sensitive APIs)
- [ ] Security headers set (CSP, X-Frame-Options, etc.)

### Dependency Vulnerabilities

Run ecosystem-specific audit commands — see `references/security-checklist.md` for commands by ecosystem.

Report any Critical or High severity vulnerabilities.

## Output Format

```markdown
## Security Review: {scope}

### Critical (fix immediately)
- {file}:{line} - {vulnerability type}: {description}
  **Fix:** {remediation}

### High Priority
- {file}:{line} - {issue}
  **Fix:** {remediation}

### Medium Priority
- {file} - {issue}

### Dependency Vulnerabilities
| Package | Severity | CVE | Fix Version |
|---------|----------|-----|-------------|
| {pkg} | Critical | CVE-XXXX-XXXX | {version} |

### Suggestions
- {improvement}
```

## Examples

**Staged changes introduce SQL injection:**
> /review-security --staged

Reviews staged files and catches a login handler using string concatenation to build a SQL query with user input. Reports it as Critical with a fix showing parameterized queries.

**Pre-release audit finds hardcoded secret:**
> /review-security --all

Parallel agents scan the full codebase by security category. Finds a hardcoded API key in a config file and a JWT secret committed as a string literal, along with an overly permissive CORS policy allowing all origins.

## Troubleshooting

### False positive on an intentional security pattern
**Solution:** If the flagged code is deliberate (e.g., a test fixture with hardcoded credentials, or a localhost-only CORS wildcard), add a comment like `// SECURITY: intentional - <reason>` so future audits can skip it with context.

### Obfuscated or generated code blocks the audit
**Solution:** Exclude generated files (e.g., `*.min.js`, `dist/`, `generated/`) from the scope and audit only the source inputs. For vendored code, check the upstream project's security advisories rather than scanning the minified output.

## Notes

- Focus on exploitable vulnerabilities, not theoretical risks
- Always provide remediation guidance
- For `--all`, use parallel agents per category for speed
- Check both source code and configuration files
- Dependency checks require package manager files (package.json, requirements.txt, etc.)
