---
name: superpowers-cso
description: >
  Use when asked to "run a security audit", "security review", "check for vulnerabilities",
  "OWASP review", "threat model", "secrets audit", or when starting a new project with
  sensitive data. Chief Security Officer — 15-phase security audit covering attack surface,
  secrets archaeology, dependency supply chain, CI/CD, LLM security, skill supply chain,
  OWASP Top 10, and STRIDE threat modeling.
---

> **DEPRECATED** — use `/cso` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Chief Security Officer (CSO) Audit

**Purpose:** Comprehensive security posture assessment. Read-only — no code changes are made.

## Modes

| Mode | Confidence gate | When |
|------|---------------|------|
| `/cso` | 8/10 | Daily scan — zero-noise, critical items only |
| `/cso --comprehensive` | 2/10 | Monthly deep-dive |

## Flags

| Flag | Focus |
|------|-------|
| `--diff` | Only audit branch changes |
| `--infra` | Infrastructure focus |
| `--code` | Code focus |
| `--skills` | Skill supply chain only |
| `--supply-chain` | Dependencies only |
| `--owasp` | OWASP Top 10 only |
| `--scope <area>` | e.g. `--scope auth`, `--scope payments` |

---

## Architecture Mental Model (Phase 0)

Before scanning, build a mental model:

1. **Detect the stack:**
```bash
ls *.json requirements.txt Cargo.toml go.mod 2>/dev/null | head -5
cat package.json 2>/dev/null | grep '"dependencies"' -A 30 || true
```

2. **Identify trust boundaries:**
   - User input → web layer
   - Web layer → business logic
   - Business logic → database
   - Internal services → external APIs

3. **Map data flows:**
   - What sensitive data exists? (PII, credentials, tokens, payment data)
   - Where does it travel?
   - Where is it stored?
   - Who can access it?

---

## Audit Phases

### Phase 1: Attack Surface Census

```bash
# Endpoints
grep -rE "app\.(get|post|put|delete|patch)|router\.(get|post)|@.*\(|route\(" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . 2>/dev/null | grep -v node_modules | head -30

# Listen addresses
grep -rE "listen|bind|serve|http.Listen|app.run|uvicorn|flask|express" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . 2>/dev/null | grep -v node_modules | head -20

# Environment exposure
grep -rE "process\.env|os\.environ|\benv\." --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . 2>/dev/null | grep -v node_modules | head -20
```

Document: public endpoints, internal endpoints, admin routes, API versioning.

### Phase 2: Secrets Archaeology

```bash
# Leaked secrets in git history (last 5 commits)
git log --oneline -5 --name-only
git log -p --all -S "api_key\|secret\|password\|token" -- "*.ts" "*.js" "*.py" "*.go" 2>/dev/null | head -50

# Tracked .env files
find . -name ".env*" -not -path "./node_modules/*" -not -path "./.git/*" 2>/dev/null
grep -rE "api_key|secret|password|token|private_key" --include=".env*" . 2>/dev/null | head -10

# CI inline secrets
grep -rE "secrets\.|env\.|vars\." --include="*.yml" --include="*.yaml" .github/ 2>/dev/null | grep -v "secrets: $" | head -20
```

Flag: any hardcoded secrets, committed credentials, leaked tokens in git history.

### Phase 3: Dependency Supply Chain

```bash
# Check for known vulnerabilities
npm audit 2>/dev/null | head -30 || true
pip-audit 2>/dev/null | head -30 || true
cargo audit 2>/dev/null | head -30 || true

# Outdated packages
npm outdated 2>/dev/null | head -20 || true

# Lockfile integrity
ls package-lock.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null

# Install scripts
grep -rE "preinstall\|postinstall\|prepare" package.json 2>/dev/null
```

Flag: known CVEs, outdated critical packages, custom install scripts.

### Phase 4: CI/CD Pipeline Security

```bash
# GitHub Actions
ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null
grep -rE "pull_request_target|checkout.*with.*token|secrets\.|github\.token" --include="*.yml" --include="*.yaml" .github/ 2>/dev/null | head -20

# Unpinned actions
grep -E "uses: [a-zA-Z]+/[a-zA-Z]+@[a-z0-9]" --include="*.yml" .github/workflows/*.yml 2>/dev/null | grep -v "@" | head -10
```

Flag: `pull_request_target` with write permissions, unpinned third-party actions, secrets in logs.

### Phase 5: Infrastructure Shadow Surface

```bash
# Docker
find . -name "Dockerfile" -o -name "docker-compose*.yml" -o -name ".dockerignore" 2>/dev/null
cat Dockerfile 2>/dev/null | grep -v "^#" | head -20

# IaC
find . -name "*.tf" -o -name "*.tfvars" -o -name "Pulumi.yaml" -o -name "serverless.yml" 2>/dev/null | head -10

# Prod credentials in configs
grep -rE "prod|production|staging" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.env*" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -20
```

Flag: secrets in Dockerfiles, hardcoded prod credentials, overly permissive IAM.

### Phase 6: Webhook & Integration Audit

```bash
# Webhook handlers
grep -rE "webhook|signature|verify|hmac" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | grep -v node_modules | head -20

# OAuth scopes
grep -rE "scope|permissions|authorization" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | grep -v node_modules | head -20

# External API calls
grep -rE "fetch\(|axios\.|requests\.|http\.client\|urllib" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | grep -v node_modules | head -20
```

Flag: missing webhook signature verification, overly broad OAuth scopes, unsanitized external responses.

### Phase 7: LLM & AI Security

```bash
# Prompt injection vectors
grep -rE "user_input\|user_message\|user_prompt\|directive" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | grep -v node_modules | head -20

# Unsanitized LLM output
grep -rE "\.text\|\.content\|\.message\|renderMarkdown\|innerHTML" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | grep -v node_modules | grep -v test | head -20

# Tool call validation
grep -rE "execute\|run\(|eval\(|exec\(|system\(" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | grep -v node_modules | head -20
```

Flag: prompt injection from user input, unsanitized LLM output rendered as HTML, tool calls with unsanitized arguments.

### Phase 8: Skill Supply Chain Audit

```bash
# Scan installed skills for malicious patterns
SKILL_DIR="$HOME/.claude/skills"
find "$SKILL_DIR" -name "SKILL.md" -o -name "CLAUDE.md" 2>/dev/null | head -20

# Check for credential access patterns
grep -rE "process\.env|os\.environ|getenv|apikey|api_key|secret|token|password" "$SKILL_DIR" 2>/dev/null | grep -v node_modules | head -20

# Check for suspicious external calls
grep -rE "fetch\(|axios|requests|urlopen" "$SKILL_DIR" 2>/dev/null | grep -v node_modules | grep -v test | head -20

# Check for data exfiltration patterns
grep -rE "console\.log|writeFile|appendFile|fs\.write|post.*http" "$SKILL_DIR" 2>/dev/null | grep -v node_modules | head -20
```

Flag: skills accessing credentials, skills making unexpected network calls, skills exfiltrating data.

### Phase 9: OWASP Top 10 Assessment

| # | Category | Check |
|---|----------|-------|
| A01 | Broken Access Control | IDOR, privilege escalation, missing auth on endpoints |
| A02 | Cryptographic Failures | Hardcoded crypto, weak algorithms, missing encryption |
| A03 | Injection | SQL, NoSQL, OS, LDAP, XSS, command injection |
| A04 | Insecure Design | Missing rate limiting, missing MFA, missing account lockout |
| A05 | Security Misconfiguration | Default credentials, verbose errors, unnecessary features |
| A06 | Vulnerable Components | Outdated deps, unmaintained libraries |
| A07 | Auth Failures | Weak passwords, session fixation, missing logout |
| A08 | Data Integrity Failures | Unvalidated redirects, SSRF, insecure deserialization |
| A09 | Logging Failures | Missing audit logs, unlogged security events |
| A10 | SSRF | Unvalidated URL fetches, file:// access |

### Phase 10: STRIDE Threat Modeling

For each component in the architecture:

| Threat | Mitigation |
|--------|------------|
| **S**poofing | Authentication, certificate pinning |
| **T**ampering | Integrity checks, HMAC, signed payloads |
| **R**epudiation | Audit logs, non-repudiable signatures |
| **I**nformation Disclosure | Encryption, access controls, TLS |
| **D**enial of Service | Rate limiting, CDN, autoscaling |
| **E**levation of Privilege | Least privilege, role-based access |

### Phase 11: Data Classification

| Class | Examples | Controls required |
|-------|---------|-------------------|
| **Restricted** | Passwords, private keys, SSNs, payment data | Encryption at rest + in transit, MFA, audit logging |
| **Confidential** | User data, PII, API keys | Encryption at rest, access controls |
| **Internal** | Business logic, non-public docs | Access controls, clean desk |
| **Public** | Marketing content, open API docs | None |

### Phase 12: False Positive Filtering

Apply these filters before reporting. A finding is a false positive if:
- The flagged code is never reachable in production
- The flagged pattern is in test/development code only
- The finding requires a prerequisite vulnerability that doesn't exist
- The finding is mitigated by an upstream control (e.g., WAF)

### Phase 13: Active Verification

For each remaining finding, verify actively:
- Can this be exploited in the current codebase?
- Is there a proof-of-concept scenario?
- Is there a compensating control that wasn't checked?

Use parallel subagents to verify findings independently.

### Phase 14: Findings Report

```
SECURITY POSTURE REPORT
════════════════════════════════════════
Scope:     [project] — [mode]
Date:      YYYY-MM-DD
Confidence: X/10
════════════════════════════════════════

## CRITICAL (fix immediately)

| # | Finding | Component | CVSS | Remediation |
|---|---------|-----------|------|-------------|
| 1 | ... | ... | ... | ... |

## HIGH

| # | Finding | Component | CVSS | Remediation |
|---|---------|-----------|------|-------------|
| 1 | ... | ... | ... | ... |

## MEDIUM

...

## Findings Summary
Critical: N  High: N  Medium: N  Low: N
Total: N

## OWASP Coverage
A01: [status]  A02: [status]  ...  A10: [status]

## STRIDE Coverage
S: [status]  T: [status]  R: [status]  I: [status]  D: [status]  E: [status]
```

### Phase 15: Save Report

```bash
mkdir -p .claude/security-reports
REPORT_FILE=".claude/security-reports/cso-$(date +%Y-%m-%d).json"
cat > "$REPORT_FILE" << 'EOF'
{
  "date": "YYYY-MM-DD",
  "scope": "...",
  "mode": "daily|comprehensive",
  "confidence": N,
  "findings": [...],
  "owasp_coverage": {...},
  "stride_coverage": {...},
  "data_classification": {...}
}
EOF
echo "Report saved to: $REPORT_FILE"
```

---

## Completion Status

- **DONE** — Full audit complete, report generated and saved
- **DONE_WITH_CONCERNS** — Audit complete with limitations (partial coverage, tools unavailable)
- **BLOCKED** — Cannot complete due to missing access or tools

---

## Key Rules

- **Read-only** — never modify code or configuration
- **Confidence gates** — daily mode is zero-noise (8/10), comprehensive is thorough (2/10)
- **Evidence for every finding** — a finding without a concrete exploit scenario is incomplete
- **False positive filter** — apply before reporting
- **Prioritize by impact** — CVSS scoring, business risk, exploitability
