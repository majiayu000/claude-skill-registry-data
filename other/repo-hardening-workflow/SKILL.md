---
name: repo-hardening-workflow
description: "Audit repository configuration, authentication, secrets, dependencies, containers and CI; document evidence, remediation and readiness limits."
---
# repo-hardening-workflow

Repeatable 8-phase security hardening workflow. Run against any repo to produce a structured findings report with severity ratings and a maturity gate verdict.

---

## Invocation

Trigger phrases: "harden this repo", "security audit", "production readiness review", "repo audit [path]"

If no path is specified, default to current working directory.

---

## Pre-Flight

1. Identify repo root — check for `pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`
2. Note language(s), framework(s), and deployment target (Docker, K3s, bare metal, etc.)
3. Check for existing `.gitleaks.toml`, `.pre-commit-config.yaml`, `trivy.yaml` — note gaps

---

## Phase 1: Config Scan

**What to check:**
- Hardcoded `localhost` instead of `127.0.0.1` (IPv6 resolution bug surface)
- Default fallback secrets: `secret = "changeme"`, `password = "password"`, `key = "dev"`, empty string defaults
- Debug flags that default to `True` or `1`
- `CORS_ORIGINS = ["*"]` or equivalent open CORS
- Unguarded admin endpoints (no auth decorator)

**Tools:**
```bash
grep -r "changeme\|password123\|secret123\|localhost" --include="*.py" --include="*.js" --include="*.ts" --include="*.yaml" .
grep -r "DEBUG.*=.*True\|debug.*=.*true" --include="*.py" --include="*.env*" .
grep -rn "CORS.*\*\|allow_origins.*\*" .
```

**Pass criteria:** No hardcoded fallback secrets. Debug off by default. CORS locked to explicit origins. All bind addresses use `127.0.0.1` or `0.0.0.0` with intent documented.

---

## Phase 2: Auth Review

**What to check:**
- Fail-open vs fail-closed: missing auth check defaults to allow?
- JWT: algorithm pinned (reject `alg: none`)? Secret loaded from env, not hardcoded?
- Auth bypass paths: unauthenticated health/metrics endpoints accessible externally?
- API key rotation: is there a mechanism, or is it baked into config?
- RBAC: is authorization checked after authentication?

**Tools:**
```bash
grep -rn "jwt\|JWT\|bearer\|Bearer\|api_key\|API_KEY" --include="*.py" --include="*.ts" .
grep -rn "verify.*=.*False\|verify_ssl.*False\|check_expiration.*False" .
grep -rn "@app.route\|router\.\|app\.get\|app\.post" . | grep -v "auth\|require\|protect\|secure"
```

**Pass criteria:** All non-public operations enforce the declared authentication and authorization policy. JWT algorithm explicitly pinned. Auth secrets loaded from an approved secret mechanism. No verify=False in production paths.

---

## Phase 3: Secret Scan

**What to check:**
- Tracked `.env` files — run `git log --oneline --all -- "*.env"` to check history
- Inline credentials in source (`sk-`, `ghp_`, `AKIA`, private key blocks)
- Secrets in Docker/K8s manifests
- `.gitignore` completeness: `.env`, `*.pem`, `*.key`, `credentials.json` all excluded?

**Tools:**
```bash
# Check git history for .env files
git log --oneline --all -- "*.env" ".env*"

# Gitleaks (if installed)
gitleaks detect --source . --no-git

# Trufflehog (if installed)
trufflehog filesystem . --only-verified

# Manual grep
grep -rn "AKIA[A-Z0-9]\|sk-[a-zA-Z0-9]\|ghp_[a-zA-Z0-9]\|-----BEGIN.*PRIVATE" .
```

Record scanner availability separately from its exit status. Nonzero results can be findings or tool failures; inspect them rather than reporting a missing tool. Filesystem scans do not cover history; scan history explicitly before claiming it clean.

**Pass criteria:** No detected secrets within the inspected scope. `.gitignore` covers all secret file patterns. Gitleaks/Trufflehog return clean. `.env.example` present with placeholder values only.

---

## Phase 4: Dependency Audit

**What to check:**
- Python: known CVEs in `requirements.txt` or `pyproject.toml`
- Node: known CVEs in `package.json`
- Unpinned dependencies (floating `>=` or `*` versions in production)
- Abandoned packages (last release > 2 years, no maintainer activity)

**Tools:**
```bash
# Python
pip-audit --requirement requirements.txt
safety check

# Node
npm audit --audit-level=high

# Trivy (covers all)
trivy fs . --scanners vuln --severity HIGH,CRITICAL
```

**Pass criteria:** No Critical or High CVEs unmitigated. All production dependencies pinned to exact versions. Audit tool integrated into CI.

---

## Phase 5: Compose / Docker Review

**What to check:**
- Services bound to `0.0.0.0` without firewall context documented
- Credentials in `environment:` blocks (use secrets references instead)
- Images unpinned (`latest` tag in production)
- Containers running as root (no `user:` directive)
- Volumes with overly broad host mounts (`/:/host` pattern)
- `privileged: true` without documented justification

**Tools:**
```bash
find . -name "docker-compose*.yml" -o -name "docker-compose*.yaml" | xargs grep -l "."
grep -n "image:.*:latest\|image:.*[^:]$" docker-compose*.yml 2>/dev/null
grep -n "privileged.*true\|user: root" docker-compose*.yml 2>/dev/null
grep -n "POSTGRES_PASSWORD\|DB_PASSWORD\|SECRET_KEY" docker-compose*.yml 2>/dev/null
```

**Pass criteria:** Images pinned to digest or semver. No credentials in compose environment blocks. Non-root user specified. No `privileged: true` without documented need.

---

## Phase 6: CI Review

**What to check:**
- Secret scanning in pipeline (gitleaks, trufflehog, or GitHub secret scanning)
- SAST tool present (bandit for Python, eslint-security for JS, semgrep)
- Dependency audit in pipeline (pip-audit, npm audit, trivy)
- Pinned GitHub Actions versions (use commit SHA, not `@v3`)
- Workflow permissions: `permissions: read-all` as default?

**Tools:**
```bash
ls .github/workflows/ 2>/dev/null || echo "no GitHub Actions"
grep -rn "gitleaks\|trufflehog\|secret-scan" .github/ 2>/dev/null
grep -rn "bandit\|semgrep\|eslint" .github/ 2>/dev/null
grep -rn "uses:.*@[a-f0-9]\{40\}" .github/ 2>/dev/null  # pinned SHAs
```

**Pass criteria:** Secret scan runs on every PR. SAST runs on every PR. Dependency audit in pipeline. Actions pinned to SHA (not floating tags).

---

## Phase 7: Data Governance

**What to check:**
- Encryption at rest: database encryption, file storage encryption configured?
- Encryption in transit: TLS enforced, no plain HTTP in production paths?
- PII handling: is PII logged? Masked in logs?
- Data retention: is there a retention/purge policy?
- Audit trails: sensitive operations logged with actor + timestamp?

**Tools:**
```bash
grep -rn "logging\.\(info\|debug\|warning\).*password\|logging.*email\|logging.*ssn" .
grep -rn "print.*password\|console\.log.*token" .
grep -rn "ssl.*False\|tls.*False\|verify.*False" .
```

**Pass criteria:** No PII in log statements. TLS enforced in production config. Retention policy documented. Sensitive operations produce audit log entries.

---

## Phase 8: Maturity Gate Assessment

Assign one of three tiers based on findings:

### DEV (not safe for any real data)
Any one of:
- Critical or High severity findings unmitigated
- Secrets tracked in git history
- Auth fail-open (unauthenticated access to non-public endpoints)
- `DEBUG=True` in production config

### INTERNAL-CONTROLS-CHECKED (not a safety certification)
All of:
- No Critical CVEs; High CVEs mitigated or accepted with documented rationale
- No secrets in git history
- Auth fail-closed
- Dependency audit passing
- `.env` properly gitignored
- Compose/Docker review passing

### PRODUCTION-CONTROLS-CHECKED (further system assessment required)
All internal-hardened criteria, plus:
- Secret scanning in CI
- SAST in CI
- Dependencies pinned to exact versions
- PII not logged
- Encryption at rest configured
- TLS enforced
- Audit trails on sensitive operations
- Data retention policy documented

---

## Output Format

Produce a structured report:

```
## Security Hardening Report — [repo-name] — [date]

**Maturity Gate: [DEV / INTERNAL-CONTROLS-CHECKED / PRODUCTION-CONTROLS-CHECKED]**

### Critical Findings
- [Phase] [file:line] — [description] — Fix: [specific action]

### High Findings
- ...

### Medium Findings
- ...

### Low / Informational
- ...

### Passing Checks
- Phase 1: Config scan — PASS
- ...

### Recommended Next Steps (priority order)
1. ...
```

---

## Integration

- Feed Critical/High findings to `triage-issue` skill to create GitHub issues
- Run after `insecure-defaults` skill for deeper per-pattern analysis
- Run `supply-chain-risk-auditor` skill in parallel with Phase 4 for SBOM-level review
- Use `infosec-architect` persona for architectural findings that need design guidance

---

## Anti-Patterns

- Do NOT produce generic advice ("use HTTPS") — always reference actual files and line numbers found
- Do NOT mark phase as PASS if tools were unavailable — mark as SKIPPED with reason
- Do NOT skip Phase 8 gate — the maturity verdict is the primary deliverable
- Do NOT accept "will fix later" — findings stay open until verified remediated
