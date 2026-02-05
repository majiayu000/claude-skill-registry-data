---
name: deployment-scripts
description: Platform-specific deployment scripts and configurations. Use when deploying applications, configuring cloud platforms, validating deployment environments, setting up CI/CD pipelines, or when user mentions Vercel, Netlify, AWS, Docker, deployment config, build scripts, or environment validation.
allowed-tools: Bash, Read, Write, Edit
---

# deployment-scripts

This skill provides reusable deployment utilities, platform configurations, and automation scripts for deploying applications to various cloud platforms.

## Available Scripts

### Authentication & Validation
- **scripts/check-auth.sh** - Verify authentication for deployment platforms (Vercel, Netlify, AWS, etc.)
- **scripts/validate-env.sh** - Validate environment variables and secrets before deployment
- **scripts/validate-build.sh** - Run pre-deployment build validation checks

### Deployment Helpers
- **scripts/deploy-helper.sh** - Universal deployment wrapper with platform detection
- **scripts/rollback-deployment.sh** - Rollback to previous deployment version
- **scripts/health-check.sh** - Post-deployment health and smoke testing

### Platform-Specific
- **scripts/vercel-deploy.sh** - Vercel deployment with environment handling
- **scripts/netlify-deploy.sh** - Netlify deployment with configuration

## Available Templates

### Platform Configurations
- **templates/vercel.json** - Vercel platform configuration template
- **templates/netlify.toml** - Netlify platform configuration template
- **templates/fly.toml** - Fly.io platform configuration template
- **templates/render.yaml** - Render platform configuration template

### Docker Templates
- **templates/Dockerfile.node** - Node.js optimized Dockerfile
- **templates/Dockerfile.python** - Python optimized Dockerfile
- **templates/.dockerignore** - Standard Docker ignore patterns

### CI/CD Templates
- **templates/github-actions-deploy.yml** - GitHub Actions deployment workflow
- **templates/gitlab-ci-deploy.yml** - GitLab CI deployment configuration
- **templates/.env.example** - Environment variables template

## Available Examples

- **examples/basic-deployment.md** - Simple deployment workflow
- **examples/multi-environment.md** - Multi-environment deployment strategy
- **examples/docker-deployment.md** - Containerized deployment patterns
- **examples/cicd-integration.md** - CI/CD pipeline integration examples
- **examples/troubleshooting.md** - Common deployment issues and solutions

## Usage Instructions

### 1. Validate Environment Before Deployment

```bash
# Check authentication status for target platform
bash scripts/check-auth.sh vercel

# Validate all required environment variables
bash scripts/validate-env.sh .env.production
```

### 2. Use Platform Templates

```bash
# Read template and customize for your project
Read: templates/vercel.json
# Modify configuration as needed
Write: vercel.json
```

### 3. Deploy with Helper Scripts

```bash
# Deploy using platform-specific script
bash scripts/vercel-deploy.sh production

# Or use universal deployment helper
bash scripts/deploy-helper.sh --platform vercel --env production
```

### 4. Post-Deployment Validation

```bash
# Run health checks after deployment
bash scripts/health-check.sh https://your-app.vercel.app
```

## Integration with Commands

Commands should use these scripts via Bash tool:

```markdown
# In a deployment command
Bash: bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/deployment/skills/deployment-scripts/scripts/check-auth.sh vercel
Bash: bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/deployment/skills/deployment-scripts/scripts/validate-env.sh .env.production
Bash: bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/deployment/skills/deployment-scripts/scripts/vercel-deploy.sh production
```

## Requirements

- **Platform CLIs**: Install required CLI tools (vercel, netlify, aws, gcloud, etc.)
- **Environment Files**: Maintain `.env.production`, `.env.staging` for each environment
- **Git**: Scripts assume git repository for deployment tracking
- **Permissions**: Ensure scripts are executable (`chmod +x scripts/*.sh`)
