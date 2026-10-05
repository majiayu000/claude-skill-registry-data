---
name: devops
description: "Audit deployment readiness across CI/CD, containers, monitoring, IaC, secrets, CDN, and DNS — score each area 0-100, identify critical gaps, and optionally auto-fix by chaining deploy sub-skills"
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
- A specific sub-area to focus on: `ci`, `docker`, `k8s`, `monitoring`, `terraform`, `secrets`, `cdn`, `dns`
- `--report-only` — produce the readiness report without generating or modifying files
- `--fix` — attempt to fix all identified gaps by chaining sub-skills
- A target environment: `aws`, `gcp`, `azure`, `fly`, `vercel`
- If no arguments, default to `--report-only`

============================================================
PHASE 1 — INFRASTRUCTURE DISCOVERY
============================================================

Scan the entire project root for existing infrastructure artifacts:

1. **CI/CD**: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`
2. **Containers**: `Dockerfile`, `docker-compose.yml`, `docker-compose.*.yml`, `.dockerignore`
3. **Kubernetes**: `k8s/`, `kubernetes/`, `helm/`, `charts/`, any `*.yaml` with `apiVersion: apps/`
4. **IaC**: `terraform/`, `*.tf`, `pulumi/`, `Pulumi.yaml`, `cdk/`, `cloudformation/`
5. **Monitoring**: `prometheus.yml`, `grafana/`, `datadog.yaml`, `.newrelic.yml`, `alertmanager.yml`
6. **Secrets**: `.env`, `.env.*`, `vault/`, `secrets/`, hardcoded API keys or tokens in source
7. **CDN**: `cdn/`, Cloudflare config (`wrangler.toml`), CloudFront references in Terraform
8. **DNS**: DNS records in Terraform, Cloudflare zone configs, Route53 references

Also detect the application stack:
- **Language**: Check `package.json`, `go.mod`, `Cargo.toml`, `requirements.txt`, `pyproject.toml`, `Gemfile`, `pubspec.yaml`, `pom.xml`, `build.gradle`
- **Framework**: Next.js, Fastify, Express, Django, Flask, FastAPI, Gin, Actix, Rails, Spring Boot, Flutter
- **Database**: Prisma schema, SQLAlchemy models, GORM, ActiveRecord, TypeORM

Store all findings in memory for scoring.

============================================================
PHASE 2 — READINESS SCORING
============================================================

Score each area on a 0-100 scale using the rubric below. Be precise — partial credit is valid (e.g., 35 or 65).

| Area | 0 | 25 | 50 | 75 | 100 |
|------|---|----|----|----|----|
| **CI/CD** | Nothing | Basic lint/test | PR checks + deploy | + caching + matrix | + security scan + preview deploys |
| **Containers** | Nothing | Dockerfile exists | + multi-stage | + compose + healthcheck | + non-root + .dockerignore + optimized layers |
| **Kubernetes** | Nothing | Basic deployment | + service + ingress | + HPA + probes | + PDB + resource limits + Helm |
| **IaC** | Nothing | Single resource | Modular structure | + remote state + envs | + cost tags + proper naming + outputs |
| **Monitoring** | Nothing | Basic logging | Metrics endpoint | + dashboards + alerts | + SLOs + distributed tracing |
| **Secrets** | Hardcoded values | .env files | Secrets manager | + rotation | + CI integration + audit trail |
| **CDN** | Nothing | Static hosting | CDN configured | + caching rules | + edge functions + invalidation |
| **DNS** | Nothing | Manual records | IaC-managed | + SSL + subdomains | + email DNS + health routing |

Calculate an overall **Deployment Readiness Score** as the weighted average:
- CI/CD: 25%
- Containers: 20%
- Monitoring: 15%
- IaC: 15%
- Secrets: 10%
- Kubernetes: 5% (0-weight if app is serverless/edge)
- CDN: 5%
- DNS: 5%

============================================================
PHASE 3 — GAP ANALYSIS
============================================================

For each area scoring below 50, generate a specific remediation plan:

1. What is missing (concrete, not vague)
2. Which sub-skill can fix it (reference: `deploy/github-actions`, `deploy/docker`, `deploy/k8s`, `deploy/monitoring`, `deploy/terraform`, `deploy/secrets`, `deploy/cdn`, `deploy/dns`)
3. Estimated effort: quick (<5 min), moderate (5-15 min), significant (15+ min)
4. Priority based on:
   - **Critical**: No CI/CD, secrets in source code, no containerization for production app
   - **High**: No monitoring, no IaC for cloud resources, no health checks
   - **Medium**: Missing caching, no preview deploys, basic Kubernetes without HPA
   - **Low**: No CDN, no email DNS, no edge functions

============================================================
PHASE 4 — REMEDIATION (if --fix)
============================================================

If `--fix` was passed, execute remediations in priority order:

1. **Critical items first** — fix secrets exposure, add basic CI/CD
2. **High items next** — add Dockerfile, monitoring, IaC
3. **Medium items** — optimize CI caching, add HPA, preview deploys
4. **Low items** — CDN, DNS, edge functions

For each remediation:
- Read the sub-skill's approach and apply it inline (do not shell out)
- After each fix, re-score that area and record the before/after delta
- Stop if cumulative changes exceed 20 new files (to avoid overwhelming a single PR)

============================================================
PHASE 5 — OUTPUT
============================================================

Generate a deployment readiness report. Print to stdout AND write to `DEPLOY_READINESS.md` in the project root.

```
## Deployment Readiness Report

**Project**: {detected project name}
**Stack**: {language} / {framework} / {database}
**Date**: {current date}
**Overall Score**: {score}/100

### Area Scores

| Area | Score | Status | Key Finding |
|------|-------|--------|-------------|
| CI/CD | XX | PASS/WARN/FAIL | {one-line summary} |
| Containers | XX | PASS/WARN/FAIL | {one-line summary} |
| Kubernetes | XX | PASS/WARN/FAIL | {one-line summary} |
| IaC | XX | PASS/WARN/FAIL | {one-line summary} |
| Monitoring | XX | PASS/WARN/FAIL | {one-line summary} |
| Secrets | XX | PASS/WARN/FAIL | {one-line summary} |
| CDN | XX | PASS/WARN/FAIL | {one-line summary} |
| DNS | XX | PASS/WARN/FAIL | {one-line summary} |

### Critical Gaps
{list of critical and high priority gaps with sub-skill references}

### Recommended Actions
{ordered list of remediations — each with sub-skill name, estimated effort, and expected score improvement}

### Changes Made (if --fix)
{list of files created/modified with before/after scores}
```

Use PASS for scores >= 75, WARN for 50-74, FAIL for < 50.


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
NEXT STEPS
============================================================

After generating the report, suggest:
1. Which sub-skill to run first if gaps exist (with the exact command)
2. Whether the project is ready for production deployment
3. Any architectural concerns (e.g., no database backups, no rate limiting, no disaster recovery)


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /devops — {{YYYY-MM-DD}}
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

- Do NOT delete existing infrastructure files — only add or modify
- Do NOT commit changes — leave them staged for review
- Do NOT expose secrets in the report output
- Do NOT assume a cloud provider — detect or use $ARGUMENTS
- Do NOT generate Kubernetes manifests for projects that are clearly serverless/edge
- Do NOT modify application source code — only infrastructure files
- Do NOT install CLI tools or dependencies — work with what is available
