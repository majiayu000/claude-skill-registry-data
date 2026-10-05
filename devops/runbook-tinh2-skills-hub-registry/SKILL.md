---
name: runbook
description: "Generate an operations runbook from your deployment config, Docker/K8s manifests, CI/CD pipelines, and monitoring setup. Triggers: you need a runbook, ops playbook, deployment guide, incident response plan, or production operations documentation."
version: "2.0.1"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze the project's
infrastructure and operations artifacts to produce a comprehensive runbook.

INPUT:
$ARGUMENTS

Accepted arguments:
- No arguments: generate a complete operations runbook.
- `deployment`: focus on deployment procedures only.
- `incident`: focus on incident response procedures only.
- `database`: focus on database maintenance procedures only.
- `troubleshooting`: focus on troubleshooting guides only.

============================================================
PHASE 1: INFRASTRUCTURE DISCOVERY
============================================================

Step 1.1 -- Deployment Configuration

Scan for deployment artifacts:

| Type | Files to Check |
|------|---------------|
| Docker | Dockerfile, docker-compose.yml, docker-compose.*.yml |
| Kubernetes | k8s/, kubernetes/, manifests/, *.yaml with `apiVersion:` |
| Helm | Chart.yaml, values.yaml, templates/ |
| Terraform | *.tf, terraform/, infrastructure/ |
| Serverless | serverless.yml, SAM template.yaml |
| PaaS | Procfile, fly.toml, vercel.json, netlify.toml, app.yaml |
| PM2 | ecosystem.config.js |

Step 1.2 -- CI/CD Pipeline

Scan for: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`,
`.circleci/config.yml`, `bitbucket-pipelines.yml`, `cloudbuild.yaml`,
`azure-pipelines.yml`.

Read each pipeline file and extract build steps, deployment targets,
environment variables, secrets referenced, and branch triggers.

Step 1.3 -- Database Configuration

Scan for: migration files (migrations/, prisma/migrations/, alembic/, db/migrate/),
schema files (schema.prisma, models.py, *.entity.ts), seed files, database config
(database.yml, knexfile.js), and backup scripts.

Step 1.4 -- Monitoring and Observability

Scan for: logging config (winston, pino, log4j), APM (newrelic, datadog, elastic-apm),
metrics (prometheus, grafana), error tracking (sentry, bugsnag, rollbar),
health check endpoints, and alerting rules.

Step 1.5 -- Environment Configuration

Scan for: .env.example, environment-specific configs, feature flags, and
secrets management (vault, AWS SSM, sealed secrets).

============================================================
PHASE 2: RUNBOOK GENERATION
============================================================

Generate `docs/runbook.md` with these sections. Only include sections relevant
to detected infrastructure. Every procedure must have copy-pasteable commands.

The runbook MUST cover these areas (skip if not applicable to project):

1. **Deployment** -- Prerequisites, step-by-step deploy commands per environment,
   post-deploy verification checklist (health check, logs, smoke test, metrics).

2. **Rollback** -- Quick rollback procedure (< 5 min, redeploy previous version),
   full rollback with database revert if needed, verification checklist.

3. **Scaling** -- Scale up/down commands, auto-scaling config and thresholds.

4. **Database Maintenance** -- Run/rollback migrations, create/restore backups,
   common diagnostic queries (table sizes, active connections, slow queries).

5. **Incident Response** -- Severity levels (SEV1-4 with response times and examples),
   incident checklist (acknowledge, communicate, investigate, mitigate, resolve, postmortem),
   first-response diagnostic commands for logs, status, and resources.

6. **Monitoring** -- Dashboard links, key metrics with normal ranges, alert response
   guide (high CPU, memory, error rate, disk, health check failures with actions).

7. **Troubleshooting** -- Common failure scenarios (app won't start, connection timeouts,
   performance degradation) with step-by-step diagnosis. Error-to-solution lookup table.

Format: use markdown headers, numbered steps with fenced bash blocks for commands,
checklists for verification, and tables for reference data.

If a runbook already exists, read it first and preserve manually-written sections.

============================================================
PHASE 3: VALIDATE AND WRITE
============================================================

For each command in the runbook:
- Verify the referenced tool/CLI exists in the project's dependencies or Dockerfile
- Verify paths and file references are correct
- Verify environment variable names match what the project uses

Write the runbook to `docs/runbook.md`.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Runbook Generated

### Infrastructure Detected
- **Deployment:** [Docker / K8s / Serverless / etc.]
- **CI/CD:** [GitHub Actions / GitLab CI / etc.]
- **Database:** [PostgreSQL / MongoDB / etc.]
- **Monitoring:** [Datadog / Prometheus / etc.]
- **Environments:** [dev, staging, production]

### Sections Generated
- [ ] Deployment procedures
- [ ] Rollback procedures
- [ ] Scaling instructions
- [ ] Database maintenance
- [ ] Incident response
- [ ] Monitoring and alerts
- [ ] Troubleshooting guide

### File Written
- `docs/runbook.md`


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /runbook — {{YYYY-MM-DD}}
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

- Do NOT fabricate infrastructure details. Only document what is evident from config files.
- Do NOT include actual secrets, passwords, or API keys in the runbook.
- Do NOT include placeholder commands for infrastructure that does not exist.
- Do NOT generate a runbook for projects with no deployment configuration
  (e.g., a library or CLI tool). Report that no runbook is needed and suggest `/readme`.
- Do NOT include generic advice not specific to this project's stack.

NEXT STEPS:

After generating the runbook:
- "Run `/document` to check overall documentation health."
- "Run `/diagram` to generate infrastructure diagrams."
- "Run `/devops` to review and improve the deployment pipeline."
