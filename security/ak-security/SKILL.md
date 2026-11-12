---
name: ak-security
description: "Audit code and dependencies for vulnerabilities, OWASP issues, leaked secrets and vulnerable packages, with optional STRIDE and auto-fix."
when_to_use: "Invoke for a security review, CVE dependency check or leaked-credential removal."
category: workflow
keywords: [security, secrets, vulnerabilities, dependencies, STRIDE, OWASP, audit, red-team, penetration-testing, vulnerability-discovery]
argument-hint: "[scope] [--secrets-only] [--deps-only] [--fix] [--red-team] [--iterations N]"
metadata:
  author: agentkit
  attribution: "Security audit pattern adapted from autoresearch by Udit Goenka (MIT)"
  version: "2.0.2"
---

# ak-security — Security Scan & Threat Audit

Comprehensive security scanner and threat audit framework. Combines fast targeted checks (secrets, dependencies, `.env` exposure, code vulnerability patterns) with structured STRIDE + OWASP threat modeling, multi-persona red-team discovery (`--red-team`), and optional iterative auto-remediation (`--fix`).

## When to Use

- "security scan", "check for secrets", or audit dependencies
- Before a release or major deployment
- After adding auth, payment, or data-handling features
- Periodic security review or compliance check (SOC 2, GDPR, PCI-DSS prep)

## When NOT to Use

- Purely cosmetic changes (CSS, copy edits)
- No user-facing code, credentials, or data handling involved

---

## Modes

| Mode | Invocation | Behavior |
|------|-----------|----------|
| Fast secret scan | `/ak-security [scope] --secrets-only` | Scan secrets and credentials; skip deps/code/STRIDE |
| Fast dependency audit | `/ak-security [scope] --deps-only` | Audit package dependencies for CVEs; skip code/STRIDE |
| Comprehensive audit (default) | `/ak-security [scope]` | Stack detection → `.env` check → secrets → deps → code patterns → STRIDE + OWASP |
| Red-team discovery | `/ak-security [scope] --red-team` | Iterate 4 attacker personas (Adversary, Supply Chain, Insider, Infra) → STRIDE/OWASP sweep |
| Bounded red-team | `/ak-security [scope] --red-team --iterations N` | Cap red-team persona discovery to N iterations total |
| Audit + Fix | `/ak-security [scope] --fix` | Comprehensive audit → fix confirmed findings iteratively |
| Red-team + Fix | `/ak-security [scope] --red-team --fix` | Full persona discovery → fix confirmed Critical/High |
| Fast scan + Fix | `/ak-security [scope] --secrets-only --fix` | Scan secrets → remediate confirmed leaks via env vars |

### Flag Precedence & Scope Defaults
- **Scope default:** when `[scope]` is omitted, scans the entire project root (`.`). Exclude `.git/`, `node_modules/`, `dist/`, `vendor/`, `__pycache__/`. For large repos in default mode, fast layers run across all files, while deep STRIDE/OWASP focuses on high-risk surfaces (`auth/`, `api/`, `config/`, database layers).
- **Fast flags short-circuit:** `--secrets-only` and `--deps-only` take precedence over `--red-team`. If combined, fast flags win and skip red-team with a note.
- **Combined fast flags:** `--secrets-only --deps-only` runs both secret detection and dependency audit while skipping code patterns and STRIDE.

### Legacy Compatibility

```text
ak-security-scan                → /ak-security
ak-security-scan --secrets-only → /ak-security --secrets-only
ak-security-scan --deps-only    → /ak-security --deps-only
ak-security-scan <dir>          → /ak-security <dir>
```

---

## Audit & Scan Methodology

### 1. Scope Resolution, Assets & Stack Detection
- Identify protected assets, actors, trust boundaries and exposure before assigning severity. A risky API name alone is not an exploit; verify reachable failure paths and current controls. Load only relevant checklists.
- Check for manifest: `package.json` (Node.js), `requirements.txt`/`pyproject.toml` (Python), `go.mod` (Go), `Cargo.toml` (Rust), `pom.xml`/`build.gradle` (Java).
- Resolve scope (defaults to project root). Exclude `.env.example`, test fixtures, documentation (`*.md`), `node_modules/`, `dist/`.

### 2. .env Exposure Check
Check whether `.env` files are accidentally tracked or unignored in git:
```bash
git ls-files --error-unmatch .env .env.local .env.production 2>/dev/null
grep -n "\.env" .gitignore 2>/dev/null
```

### 3. Secret & Credential Scanning
Scan source files for hardcoded API keys, passwords, tokens, and private keys.
- Reference: `references/secret-patterns.md` (high and medium confidence patterns).
- False-positive exclusion: skip placeholders (`YOUR_API_KEY`, `TODO`, `placeholder`, env reads).
- Rate severity: CRITICAL (exposed prod key), HIGH (real credential), MEDIUM (possible credential). <!-- cruft-lint-allow — severity rating scale, not instruction emphasis -->

### 4. Dependency Audit
Run the stack's dependency audit tool and categorize findings by severity:
- Node.js: `npm audit --json 2>/dev/null`
- Python: `pip-audit --format json 2>/dev/null`
- Go: `govulncheck ./...`
- Rust: `cargo audit`
- Ruby: `bundle audit check --update`
- Java: `mvn dependency-check:check`

### 5. Vulnerability Code Pattern Analysis
Search for dangerous patterns using search_files capability:
- SQL injection (string concatenation / template literals in queries)
- XSS (`innerHTML`, `dangerouslySetInnerHTML`, unescaped template tags)
- Command injection (`exec`/`spawn`/`os.system` with dynamic input)
- Path traversal (user input in file paths without normalization)
- Insecure randomness (`Math.random` for security tokens)
- Dangerous functions (`eval`, `new Function`, unsafe deserialization)
- Reference: `references/vulnerability-patterns.md`.

### 6. STRIDE Analysis (Skipped in --secrets-only / --deps-only)
Evaluate threats systematically:
- **S**poofing — auth weaknesses, session flaws
- **T**ampering — input validation, integrity controls
- **R**epudiation — audit logging gaps
- **I**nformation Disclosure — data leakage, secret exposure
- **D**enial of Service — rate limits, resource exhaustion
- **E**levation of Privilege — broken access control, IDOR

### 7. OWASP Top 10 Check (Skipped in --secrets-only / --deps-only)
Map findings to OWASP categories (A01–A10). See `references/stride-owasp-checklist.md`.

### 8. Finding Categorization
Deduplicate by root cause across code patterns, STRIDE, OWASP and personas. Attach path, reproducible evidence, impact, assumptions and mitigation to each finding. Record disproven concerns as non-issues with their verification source. Assign severity using the definitions below.

---

## Output Format

```markdown
# Security Audit Report

**Project:** {name}
**Scope:** {scope}
**Mode:** {mode}
**Files checked:** {count}

## Summary
| Category | Critical | High | Medium | Low | Info |
|----------|----------|------|--------|-----|------|
| Secrets  | X | X | X | - | - |
| Deps     | X | X | X | X | - |
| Code     | X | X | X | X | - |
| STRIDE   | X | X | X | X | X |

## Findings

| # | Severity | Category | File:Line | Description | Fix Recommendation |
|---|----------|----------|-----------|-------------|-------------------|
| 1 | Critical | Secret   | src/config.js:42 | Hardcoded AWS key | Move to env var and rotate key |
| 2 | High     | A03 Inj  | api/users.ts:45 | SQL string concatenation | Use parameterized queries |
```

If `--auto` mode is active in the cook workflow, save the report to `{CK_REPORTS_PATH}` or `plans/reports/security-{date}.md`.

---

## Red-Team Discovery Mode (--red-team)

When `--red-team` is provided, the audit runs a **multi-persona iterative discovery loop** before the standard STRIDE/OWASP sweep.

### Persona Execution Order
1. **Security Adversary** — external attacker; auth bypass, injection, IDOR, privilege escalation
2. **Supply Chain Attacker** — dependency/CI poisoning; CVEs, unsigned artifacts, loose CI permissions
3. **Insider Threat** — authenticated low-privilege user; horizontal/vertical escalation, bulk export
4. **Infrastructure Attacker** — environment foothold; SSRF, secrets in env, container misconfig

Each persona phase follows the autoresearch iteration protocol. See `references/red-team-personas.md` for full persona catalog, attack vectors, and TSV schema.

---

## Fix Mode (--fix)

When `--fix` is provided, apply fixes iteratively after the audit:

1. Sort findings by severity (Critical → High → Medium → Low).
2. For each finding:
   - For code vulnerabilities: apply one targeted fix, then run tests/lint guard to verify no regression.
   - For hardcoded secrets: replace secret with an environment variable reference, add rotation instruction, and never rewrite git history automatically.
   - Commit: `security(fix-N): <short description>`.
3. Stop early if guard fails — report the failure instead of proceeding.
4. Uses `ak-autoresearch` guard pattern for regression prevention. Use `--iterations N` to cap fix iterations.

---

## Severity Definitions

| Severity | Description | Fix Priority |
|----------|-------------|-------------|
| Critical | Exploitable now, data breach or RCE risk | Immediate — block release |
| High | Exploitable with moderate effort, significant impact | This sprint |
| Medium | Limited exploitability or impact | Next sprint |
| Low | Theoretical risk, defense-in-depth improvement | Backlog |
| Info | Best practice suggestion, no direct risk | Optional |

---

## Security Policy

- Redact secret values in reports to an opaque marker (e.g. `<REDACTED_AWS_KEY>`, `<REDACTED_PASSWORD>`), preserving only a public issuer prefix (such as `AKIA`, `ghp_`, `sk_`, `sk-`, `xox`) when it aids triage, because revealing partial secrets or character counts widens exposure and lets an attacker confirm candidate values. Never emit raw secret lengths or trailing characters. Reference environment variables by name only (`$NAME`), and redact the entire `user:password@` segment in connection strings.
- Do not execute a secret or credential found during scanning, because running it authenticates as the victim and can trigger unwanted side effects or owner alerting.
- Report-only is the default behavior so that a human reviews every security-sensitive change; `--fix` is an explicit opt-in that requires guard verification before applying edits.
- Recommend immediate rotation whenever a real credential or live key is detected, because removing it from code does not invalidate a compromised token.
- Do not rewrite git history automatically during fixes, because history mutations can disrupt team branches and require explicit authorization.

## Scope Declaration

This skill handles: Secret detection, dependency auditing, code vulnerability patterns, STRIDE threat modeling, OWASP Top 10 analysis, red-team persona discovery loops, and guarded auto-remediation.
This skill does NOT handle: Live active network penetration testing, DDoS simulation, physical security, or hardware security.

---

## Integration with Other Skills

- Run after `ak-predict` when the security persona flags concerns
- Use this skill’s explicit `--fix` mode for guarded remediation of confirmed findings
- Use `ak-scenario` with `--focus authorization` for deeper auth flow testing
- Pair with `ak-plan` to schedule Medium/Low findings as sprint tasks

---

## Example Invocations

```bash
# Fast secret scan — project-wide
/ak-security --secrets-only

# Fast dependency audit — project-wide
/ak-security --deps-only

# Comprehensive audit — project root (default)
/ak-security

# One-shot audit — API layer only
/ak-security src/api/**/*.ts

# Red-team discovery — full codebase, all 4 personas
/ak-security full --red-team

# Red-team discovery — bounded to 20 iterations total
/ak-security src/ --red-team --iterations 20

# Red-team discovery + auto-fix confirmed Critical/High
/ak-security full --red-team --fix

# One-shot audit + auto-fix, max 15 iterations
/ak-security src/ --fix --iterations 15
```

---

See `references/stride-owasp-checklist.md` for the per-category checklist.
See `references/secret-patterns.md` for high and medium confidence secret detection regexes.
See `references/vulnerability-patterns.md` for grep-based vulnerability code patterns.
See `references/red-team-personas.md` for the full persona catalog and TSV schema.

---

## Lineage

Faithful absorption of upstream `/autoresearch:security` ([uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch), MIT) merged with AgentKit fast secret/dependency/vulnerability scanning.

See `/ak-autoresearch` for the full family map.

## Optional finding-triage experiment

After candidate discovery, explicitly opted-in experiments may follow
[semantic triage](references/semantic-triage.md). Ordinary review remains unchanged.
