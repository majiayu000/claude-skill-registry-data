---
name: secret-scanning-rotation-planner
displayName: Secret Scanning & Rotation Planner
tagline: Scan repos for exposed secrets and generate a prioritized rotation plan with remediation steps.
description: |
  Scans GitHub repositories for exposed secrets including API keys, tokens, passwords,
  and certificates. Classifies each finding by severity and exposure window, then
  generates a prioritized rotation plan with step-by-step remediation instructions
  and prevention recommendations.
department:
  - Security & Compliance
  - Engineering
use_cases:
  - Code Review
  - Incident Response
tools_required:
  - GitHub MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-02-24
version: 1.0.0
exampleInput: |
  Organization: 45 repositories across a microservices architecture
  Context: Preparing for quarterly security audit, need to scan entire org
  Repos: Mix of Node.js, Python, Go services with shared infra
  Concern: Past incidents of accidental key commits, want full inventory
exampleOutput: |
  Secret Scanning Report — 45 Repositories

  EXECUTIVE SUMMARY
  Total Findings:     23 secrets across 12 repos
  Critical:          4 (AWS keys, Slack tokens)
  High:              7 (API keys, JWT signing keys)
  Medium:            8 (Database URLs, internal tokens)
  Low:               4 (Development keys in .env.example samples)
  Longest Exposure:  AWS key in payment-service — 18 months (git history)

  FINDINGS BY SECRET TYPE
  | Type           | Count | Severity | Sample Repos                          |
  |----------------|-------|----------|--------------------------------------|
  | AWS Keys       | 5     | Critical | payment-service, deploy-scripts      |
  | Slack Tokens   | 3     | Critical | slack-bot, notifications             |
  | Stripe Keys    | 2     | High     | payment-service                      |
  | JWT Secrets    | 4     | High     | auth-service, api-gateway            |
  | DB Credentials | 6     | Medium   | user-service, analytics              |
  | Internal APIs  | 3     | Medium   | order-service, inventory             |

  ROTATION PLAN (Prioritized)
  1. [P0] AWS keys — Revoke in IAM, rotate within 24h, redeploy 3 services
  2. [P0] Slack tokens — Regenerate in Slack admin, update 2 bots
  3. [P1] Stripe keys — Rotate in Dashboard, update env vars
  4. [P1] JWT secrets — Generate new, coordinate auth-service rollout

  Generated: Rotation playbook (15 steps), git filter-repo commands, prevention checklist
---

# Secret Scanning & Rotation Planner

Scan repos for exposed secrets and generate a prioritized rotation plan with remediation steps.

**Integrations:** GitHub

## When to Use

- The user needs to scan repositories for exposed secrets before or after an incident
- A security audit requires a full inventory of secrets across an organization
- The user mentions "secret scanning", "credential exposure", "rotation plan", or "leaked keys"
- Teams want to proactively identify and remediate accidentally committed secrets

## Steps

### Step 1: Configure Scan Scope

Define what to scan:

| Scope Option | Description |
|--------------|-------------|
| **Organization** | All repos the user has access to, or a filtered subset (e.g., by language, team) |
| **Repository list** | Specific repos provided by the user (URLs or names) |
| **Branch** | Default branch only, all branches, or specific branches |
| **History depth** | Head only, last N commits, or full history (affects exposure window analysis) |
| **Path exclusions** | Skip `node_modules/`, `vendor/`, `.lock` files, etc. to reduce false positives |

Ask the user for: org name or repo list, branch strategy, and whether to include full git history.

### Step 2: Scan for Secret Patterns

Search for common secret patterns:

| Pattern Type | Examples | Detection Approach |
|--------------|----------|-------------------|
| AWS | `AKIA...`, `aws_secret_access_key` | Regex for key format, env var names |
| Slack | `xoxb-`, `xoxp-`, `xapp-` | Token prefix patterns |
| Stripe | `sk_live_`, `pk_live_` | Live/test key prefixes |
| GitHub | `ghp_`, `gho_`, `github_pat_` | Personal access token formats |
| Generic | `password=`, `secret=`, `api_key=` | Config patterns with high-entropy values |
| JWT/Keys | Base64-encoded JWTs, PEM priv keys | Format validation |
| Database | Connection strings with creds | JDBC, MongoDB, Postgres URL patterns |
| Certificates | PEM blocks, PKCS12 | File extensions and content structure |

Use GitHub MCP to search repo contents (code search, file reads) for these patterns. Cross-reference with GitHub's native secret scanning if available.

### Step 3: Classify and Prioritize Findings

For each finding, classify:

| Field | Options | Notes |
|-------|---------|-------|
| **Severity** | Critical, High, Medium, Low | Based on secret type and exposed capabilities |
| **Secret Type** | AWS, Slack, DB, API key, etc. | From pattern detection |
| **Exposure Window** | First commit date → now (or last seen) | Use git blame / history to determine |
| **Location** | Repo, file path, branch, commit SHA | For precise remediation |
| **In History** | Yes/No | Whether secret exists in git history (vs. removed in later commits) |
| **False Positive** | Yes/No | Exclude samples, placeholders, test fixtures |

**Severity Guidelines:**
- **Critical:** Cloud provider keys, payment keys, tokens with broad access
- **High:** API keys with write access, signing secrets
- **Medium:** Internal API keys, DB credentials in non-production configs
- **Low:** Dev keys, samples, revoked/test credentials

### Step 4: Generate Rotation Plan

Create a prioritized rotation plan:

| Priority | Action | Timeline | Dependencies |
|----------|--------|----------|--------------|
| P0 | Rotate immediately | 24–48 hours | Revoke old keys first, then rotate |
| P1 | Rotate this week | 3–7 days | Coordinate with deployments |
| P2 | Rotate this sprint | 2 weeks | Schedule during maintenance window |
| P3 | Rotate when convenient | Next quarter | Low exposure, can batch |

For each finding, include:
1. **Rotation steps** — Exact steps for the specific service (e.g., AWS IAM → create new key → revoke old → update env vars)
2. **Affected services** — Which repos/apps use this secret
3. **Redeploy requirements** — Whether services need restarts or env updates
4. **Verification** — How to confirm rotation succeeded
5. **History cleanup** — `git filter-repo` or BFG commands to remove from git history (if applicable)

### Step 5: Recommend Prevention Measures

Provide prevention recommendations:

| Measure | Description |
|---------|-------------|
| **Pre-commit hooks** | gitleaks, truffleHog, or detect-secrets in pre-commit |
| **CI scanning** | Add secret scanning to GitHub Actions or equivalent |
| **GitHub advanced security** | Enable secret scanning and push protection for the org |
| **Secret management** | Migrate to Vault, AWS Secrets Manager, or similar |
| **Documentation** | Document where secrets live, who can rotate them, playbooks |
| **Developer training** | Guidelines on never committing secrets, using .env.example |

Include sample configs for gitleaks, truffleHog, or GitHub Actions where relevant.

## Output

Deliver:
- A findings report with severity, location, and exposure window for each secret
- A prioritized rotation plan with step-by-step remediation instructions per finding
- Git history cleanup commands (filter-repo, BFG) for each affected repo
- A prevention checklist with tool configs and recommendations
- A summary table mapping findings to rotation P0/P1/P2/P3
