---
name: secrets
description: "Audit codebases for leaked secrets and hardcoded credentials, generate .env templates, configure secrets management with AWS Secrets Manager, Vault, Doppler, or GCP Secret Manager, set up credential rotation, and integrate secrets into CI/CD pipelines via OIDC federation"
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- A secrets provider: `vault`, `aws-sm` (Secrets Manager), `aws-ssm` (Parameter Store), `gcp-sm`, `doppler`, `infisical`
- `--audit` — only audit current secret handling, do not generate config
- `--rotate` — set up secret rotation for database and API credentials
- `--ci` — configure CI/CD pipeline to pull secrets from provider
- `--env-template` — generate `.env.example` from detected env vars
- If no arguments, perform audit and recommend a provider based on existing infrastructure

============================================================
PHASE 1 — SECRET AUDIT
============================================================

Perform a comprehensive scan for secret exposure:

**1. Hardcoded secrets in source code** (exclude node_modules, vendor, .git):
- API keys: `(api[_-]?key|apikey)\s*[:=]\s*['"][A-Za-z0-9]{16,}['"]`
- AWS keys: `AKIA[0-9A-Z]{16}`
- Private keys: `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`
- Tokens: `(token|secret|password)\s*[:=]\s*['"][^'"]{8,}['"]`
- Connection strings: `(postgres|mysql|mongodb|redis)://[^@]+@`
- JWT secrets: `(jwt[_-]?secret|signing[_-]?key)\s*[:=]\s*['"]`
- Generic high-entropy strings in assignment context (16+ chars, mixed case + digits)

**2. Environment files**:
- Check for `.env`, `.env.local`, `.env.production`, `.env.development`
- Check if `.env` is in `.gitignore`
- Check if any `.env` files are tracked by git: `git ls-files .env*`
- Read `.env` files and categorize values as: secret vs configuration

**3. Git history** (last 50 commits):
- Scan diffs for accidentally committed secrets
- Check if any `.env` files were ever committed then removed
- Flag any file in history matching secret patterns

**4. Configuration files**:
- `docker-compose.yml` — passwords in environment blocks
- `application.yml` / `application.properties` — embedded credentials
- Terraform files — hardcoded provider credentials or database passwords
- Kubernetes secrets — base64-encoded values in committed YAML

**5. CI/CD configuration**:
- `.github/workflows/*.yml` — check for inline secrets (should use `${{ secrets.NAME }}`)
- `.gitlab-ci.yml` — check for variables with exposed values

**Severity classification**:
- **CRITICAL**: Secrets in source code or git history
- **HIGH**: .env files tracked by git, secrets in docker-compose
- **MEDIUM**: .env not in .gitignore, missing .env.example
- **LOW**: No secrets manager configured, no rotation policy

============================================================
PHASE 2 — ENVIRONMENT TEMPLATE
============================================================

Generate `.env.example` from all detected environment variable references.

Scan for env var patterns:
- Node.js: `process.env.VARNAME`
- Python: `os.environ["VARNAME"]`, `os.getenv("VARNAME")`
- Go: `os.Getenv("VARNAME")`
- Generic: `${VARNAME}` in config files

Create `.env.example` with:
- Grouped sections (Application, Database, Cache, Authentication, External APIs, Cloud)
- `# SECRET:` prefix for values that must come from secrets manager
- `# CONFIG:` prefix for non-sensitive configuration
- Placeholder values that clearly indicate they need replacement (e.g., `REPLACE_ME_WITH_SECURE_RANDOM_VALUE`)

============================================================
PHASE 3 — SECRETS PROVIDER SETUP
============================================================

Based on detected infrastructure or $ARGUMENTS, set up the appropriate provider:

**AWS Secrets Manager**:
- Generate Terraform for `aws_secretsmanager_secret` resources
- Generate application helper to read secrets at startup (using `@aws-sdk/client-secrets-manager` or equivalent)
- Configure IAM policy for ECS task role / Lambda execution role
- Set up secret versioning and stage labels

**AWS Systems Manager Parameter Store**:
- Generate Terraform for `aws_ssm_parameter` resources (SecureString type)
- Hierarchical naming: `/{project}/{env}/{secret_name}`
- Cheaper alternative for smaller number of secrets

**GCP Secret Manager**:
- Generate Terraform for `google_secret_manager_secret` resources
- Configure IAM bindings for service account access

**HashiCorp Vault**:
- Generate Vault policy file and AppRole auth method config
- Docker Compose service for local Vault dev server
- Application helper for Vault API integration

**Doppler**:
- Generate `doppler.yaml` project config
- Set up environment configs (dev, staging, prod)

**For all providers**, generate a unified secrets loading wrapper:
- In production: load from secrets manager
- In development: load from `.env` file via dotenv

============================================================
PHASE 4 — SECRET ROTATION (if --rotate)
============================================================

**Database credentials**:
- AWS: Lambda rotation function with `aws_secretsmanager_secret_rotation`
- Dual-user rotation strategy (alternating credentials for zero-downtime)
- Rotation schedule: every 30 days

**API keys**:
- Script that: creates new key, updates secrets manager, waits for propagation, revokes old key
- Document manual rotation steps for third-party APIs

**TLS certificates**:
- Reference cert-manager or ACM for auto-renewal
- Alert 30 days before expiration

============================================================
PHASE 5 — CI/CD INTEGRATION (if --ci)
============================================================

**GitHub Actions**:
- OIDC federation for GitHub -> AWS (no long-lived credentials needed)
- `aws-actions/configure-aws-credentials@v4` with `role-to-assume`
- `aws-actions/aws-secretsmanager-get-secrets@v2` for loading secrets
- Environment protection rules for production secrets

**Doppler**:
- `dopplerhq/secrets-fetch-action@v1` with `DOPPLER_TOKEN` secret

**General**:
- Enable GitHub secret scanning and push protection
- Document all required repository secrets and where to obtain them

============================================================
PHASE 6 — REMEDIATION
============================================================

For each CRITICAL and HIGH finding from the audit:

1. **Hardcoded secrets**: Replace with environment variable references
2. **Committed .env files**: Add to `.gitignore`, remove from git tracking (warn about history)
3. **Docker compose passwords**: Replace with variable references `${DB_PASSWORD}`
4. **Missing .gitignore entries**: Add `.env*`, `*.pem`, `*.key`, `*.jks` patterns

If secrets were found in git history:
- Recommend `git-filter-repo` to remove from history (document command but do NOT execute)
- Recommend rotating ALL exposed credentials immediately


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

```
## Secrets Audit & Configuration

### Audit Results
| Severity | Finding | Location | Status |
|----------|---------|----------|--------|
| CRITICAL | {finding} | {file:line} | {fixed/needs-action} |
| HIGH | {finding} | {file} | {fixed/needs-action} |
| MEDIUM | {finding} | {file} | {fixed/needs-action} |

### Files Created/Modified
- .env.example — Environment variable template ({N} variables)
- .gitignore — Added secret file patterns
- {provider config files}
- {application secret loader}

### Secrets Inventory
| Secret | Provider | Rotation | CI/CD |
|--------|----------|----------|-------|
| DATABASE_URL | {provider} | 30 days | configured |
| JWT_SECRET | {provider} | 90 days | configured |

### Immediate Actions Required
{ordered list of manual actions needed, starting with credential rotation}
```

============================================================
NEXT STEPS
============================================================

1. Rotate any credentials that were exposed in source or git history
2. Set up the secrets provider account/project if not already done
3. Migrate existing .env values to the secrets provider
4. Update deployment scripts to pull secrets from provider at runtime
5. Enable GitHub secret scanning and push protection on the repository
6. Schedule quarterly secret rotation reviews


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /secrets — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT print, log, or display actual secret values in any output
- Do NOT commit real secrets to any file, even temporarily
- Do NOT delete `.env` files without warning — they may be the only copy of secrets
- Do NOT run `git filter-repo` or `git filter-branch` without explicit user confirmation
- Do NOT disable git history scanning — secrets in history are a real risk
- Do NOT use symmetric encryption for secrets at rest — use provider-managed encryption
- Do NOT create IAM users with long-lived credentials — prefer roles and OIDC federation
- Do NOT store secrets in Terraform state without encrypting the state backend
- Do NOT skip the audit phase — always scan before configuring
