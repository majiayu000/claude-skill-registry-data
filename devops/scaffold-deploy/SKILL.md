---
name: scaffold-deploy
description: Generate deployment configuration files (Dockerfile, vercel.json, wrangler.toml, etc.) based on target type.
type: scaffold
project_types: [web-app, api, library, cli, tui]
trigger: "setup deploy, create CI/CD, dockerize, deploy config"
inputs:
  - name: target
    description: Deployment target (docker, vercel, railway, fly, aws, gcp, custom)
    required: false
    default: "docker"
  - name: ci_provider
    description: CI/CD provider (github-actions, gitlab-ci, custom)
    required: false
    default: "github-actions"
---

## Context

Project {{project_name}} ({{project_type}}) uses {{stack}}.
Setup deployment to {{input.target}} with CI/CD via {{input.ci_provider}}.

## Instructions

1. **Create Dockerfile** (if target = docker, railway, fly, aws, gcp)
   - Multi-stage build (builder + runner)
   - Non-root user
   - Minimal image size (alpine if possible)
   - Proper .dockerignore
   - Health check endpoint

2. **Create docker-compose.yml** (for local development)
   - App service
   - Database service (if applicable)
   - Redis service (if applicable)
   - Volume mounts for development
   - Environment variables from .env

3. **Create CI/CD pipeline**

   **GitHub Actions:**
   ```
   .github/workflows/
   ├── ci.yml        # Run on PR: lint, typecheck, test
   ├── deploy.yml    # Run on push to main: build, deploy
   └── release.yml   # Run on tag (library only): publish
   ```

   **GitLab CI:**
   ```
   .gitlab-ci.yml    # stages: test, build, deploy
   ```

4. **Create environment configs**
   - `.env.example` (template, committed)
   - Document required env vars
   - Separation: development, staging, production

5. **Platform-specific config:**
   - Vercel: `vercel.json`
   - Railway: `railway.toml`
   - Fly.io: `fly.toml`
   - Library: npm publish config in package.json

## Script

```bash
#!/bin/bash
# Create deployment directories
mkdir -p .github/workflows 2>/dev/null

# Create .dockerignore if using Docker
if [ "{{input.target}}" != "vercel" ]; then
cat > .dockerignore << 'DOCKERIGNORE'
node_modules
.git
.env
.env.local
dist
coverage
.next
DOCKERIGNORE
echo "Created .dockerignore"
fi
```

## Validation

- [ ] Dockerfile builds successfully (`docker build .`)
- [ ] Container runs and responds to health check
- [ ] CI pipeline syntax valid
- [ ] CI pipeline runs successfully (lint, typecheck, test)
- [ ] .env.example contains all required variables
- [ ] No secrets hardcoded in any config file
- [ ] .dockerignore excludes sensitive files
