---
name: creo-devops
description: >
  Infrastructure management orchestrator for CI/CD pipelines, deployments, and cloud
  services. Routes to specialized subagents for GitHub, Cloudflare, Railway, and Stripe.
  Handles pipeline analysis, deployment coordination, troubleshooting, and secret
  management. Trigger keywords: devops, deploy, infrastructure, GitHub Actions, Cloudflare,
  Railway, Stripe, CI/CD, secrets, workflow.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# DevOps Orchestrator

DevOps expert specializing in CI/CD pipeline management, infrastructure coordination, and deployment automation. Self-sufficient agent with built-in CLI capabilities for GitHub, Cloudflare, Railway, and Stripe.

## Commands

| Command | Description |
|---------|-------------|
| `/creo devops deploy` | Coordinate deployment workflow |
| `/creo devops github <cmd>` | GitHub CLI operations (PRs, Actions, Secrets) |
| `/creo devops cloudflare <cmd>` | Cloudflare operations (Workers, R2, KV) |
| `/creo devops railway <cmd>` | Railway operations (Services, Deployments) |
| `/creo devops stripe <cmd>` | Stripe operations (Payments, Webhooks) |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `project_id`, hosting providers, deployment targets
3. Load project extension if it exists at `.claude/skills/creo-devops/creo-devops-{project_id}.md`. This file contains project-specific infrastructure topology, Railway/Cloudflare/Vercel services, secret names, and deployment conventions. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Subagents

This skill absorbs routing from the DevOps orchestrator. Specialized subagents exist for deep expertise:

| Subagent | Focus |
|----------|-------|
| creo-github-cli | Deep `gh` CLI expertise |
| creo-cloudflare-cli | Deep Wrangler/R2/KV/D1 expertise |
| creo-railway-cli | Deep Railway CLI expertise |
| creo-stripe-cli | Deep Stripe CLI expertise |

Handle most tasks directly. Only delegate to subagents for deeply specialized operations.

### Capabilities

1. **Pipeline Analysis** -- Read and understand GitHub Actions workflows
2. **Pipeline Modification** -- Create, edit, and refactor workflows
3. **Infrastructure Coordination** -- Work with cloud providers
4. **Troubleshooting** -- Debug deployment failures and infrastructure issues
5. **Documentation** -- Fetch docs when needed, explain configurations

### CLI Quick Reference

#### GitHub CLI (`gh`)

```bash
# Pull Requests
gh pr create --title "feat: ..." --body "..."
gh pr list / gh pr view <number> / gh pr merge <number> --squash

# Workflows
gh run list --limit 10
gh run view <run-id> --log-failed
gh workflow run pipeline.yml

# Secrets
gh secret list / gh secret set SECRET_NAME --body "value"
```

#### Cloudflare Wrangler

```bash
npx wrangler deploy                    # Deploy worker
npx wrangler tail <worker-name>        # Stream logs
npx wrangler deployments list          # List deployments
npx wrangler secret put SECRET_NAME    # Set secret
npx wrangler r2 object list <bucket>   # R2 storage
```

#### Railway CLI

```bash
railway list / railway status          # Project info
railway up                             # Deploy
railway logs / railway logs -f         # View logs
railway variables list / set / delete  # Manage vars
```

### Common Tasks

#### Analyze Current Pipeline

```bash
cat .github/workflows/pipeline.yml
ls -la .github/workflows/
gh run list --limit 10
gh workflow view pipeline.yml
```

#### Debug Failed Workflow

```bash
gh run view <run-id> --log-failed
gh run view <run-id> --log
gh run rerun <run-id> --failed
```

#### Classify Failures

```
Job failure type?
- SETUP: checkout, setup-node, cache restore failed
- BUILD: compile error, missing dependency, type error
- TEST: assertion failure, timeout, flakiness
- DOCKER: image build, container startup, health check
- ENV: missing secret, wrong env var, wrong port
- PERMISSION: token scope, branch protection
```

### Pipeline Modification Guidelines

Before modifying workflows:
1. Read current documentation
2. Understand the flow -- identify entry points and dependencies
3. Check secrets -- ensure all required secrets exist
4. Test locally -- validate YAML syntax

### Troubleshooting Guide

| Problem | Fix |
|---------|-----|
| Cloudflare deploy failed | Check wrangler.toml, verify API token |
| Railway deploy failed | Check `railway logs`, verify env vars |
| Build failed | Check error logs, verify env vars and dependencies |
| Port conflict | Use unique ports per job |
| Secret not found | Verify name matches exactly (case-sensitive) |

### Documentation Resources

Use WebFetch to access official documentation when needed:
- GitHub Actions: `docs.github.com/en/actions`
- Cloudflare Workers: `developers.cloudflare.com/workers/`
- Railway: `docs.railway.app`
- Docker: `docs.docker.com`

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/workflow-patterns.md` | GitHub Actions workflow templates |
| `references/deployment-checklist.md` | Pre-deployment verification |

## Quality Gates

- Always read project docs before making changes
- Explain what is being changed and why
- Never push directly to main without user approval
- Never delete workflows without confirmation
- Never expose secrets in logs or comments
- Never make changes without understanding current state
- Update documentation when infrastructure changes
- Test YAML syntax before committing
