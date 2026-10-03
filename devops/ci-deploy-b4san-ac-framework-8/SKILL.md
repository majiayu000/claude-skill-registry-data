---
name: ci-deploy
description: Automate continuous integration, deployment, and post-deployment verification of developed solutions. Use when setting up CI/CD pipelines, deploying to staging/production environments, running automated tests in CI, or verifying deployments. Ensures reproducible builds and reliable deployments.
license: MIT
metadata:
  author: AC Framework
  version: "1.0"
---

# CI/CD & Deployment

Automated continuous integration, deployment pipelines, and post-deployment verification for reliable software delivery.

## When to Use This Skill

Use this skill when:
- Setting up CI/CD pipelines for a project
- Deploying to staging or production environments
- Configuring GitHub Actions, GitLab CI, or other CI systems
- Running automated tests in CI environments
- Verifying deployments are successful
- Rolling back failed deployments
- Setting up infrastructure as code

## Instructions

### Step 1: Analyze Deployment Requirements

1. **Identify target environments**:
   - Development
   - Staging/Preview
   - Production

2. **Determine deployment strategy**:
   - Direct deployment (simple)
   - Blue-green deployment (zero downtime)
   - Canary deployment (gradual rollout)
   - Feature flags (controlled release)

3. **List prerequisites**:
   - Environment variables
   - Secrets management
   - Database migrations
   - Infrastructure requirements

### Step 2: Set Up CI Pipeline

**GitHub Actions Example**:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run type check
        run: npm run typecheck
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

**GitLab CI Example**:

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm run lint
    - npm run test

build:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
```

### Step 3: Configure Deployment Pipeline

**Vercel Deployment**:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Vercel
        uses: vercel/action-deploy@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

**Docker Deployment**:
```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Image

on:
  push:
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Step 4: Set Up Secrets Management

**GitHub Secrets**:
```bash
# Add via GitHub UI or CLI
gh secret set DATABASE_URL --body "postgresql://..."
gh secret set API_KEY --body "sk-..."
gh secret set JWT_SECRET --body "..."
```

**Environment Variables**:
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    environment: production
    env:
      NODE_ENV: production
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      API_KEY: ${{ secrets.API_KEY }}
```

### Step 5: Configure Database Migrations

**Run Migrations in CI**:
```yaml
- name: Run Database Migrations
  run: npm run migrate
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

**Pre-deployment Check**:
```yaml
- name: Check Migration Status
  run: |
    npm run migrate:status
    if [ $? -ne 0 ]; then
      echo "Pending migrations detected"
      exit 1
    fi
```

### Step 6: Set Up Automated Testing in CI

**Test Matrix** (multiple environments):
```yaml
strategy:
  matrix:
    node-version: [18, 20, 21]
    os: [ubuntu-latest, windows-latest]

steps:
  - uses: actions/checkout@v4
  - name: Use Node.js ${{ matrix.node-version }}
    uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node-version }}
  - run: npm ci
  - run: npm test
```

**Coverage Reporting**:
```yaml
- name: Run tests with coverage
  run: npm run test:coverage

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage/lcov.info
```

### Step 7: Implement Security Scanning

**Dependency Vulnerability Check**:
```yaml
- name: Run npm audit
  run: npm audit --audit-level=moderate

- name: Check for known vulnerabilities
  run: npx audit-ci --moderate
```

**Static Application Security Testing (SAST)**:
```yaml
- name: Run CodeQL Analysis
  uses: github/codeql-action/init@v2
  with:
    languages: javascript

- name: Autobuild
  uses: github/codeql-action/autobuild@v2

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v2
```

### Step 8: Post-Deployment Verification

**Health Checks**:
```yaml
- name: Verify Deployment
  run: |
    sleep 30  # Wait for deployment
    curl -f https://your-app.com/health || exit 1
    curl -f https://your-app.com/api/status || exit 1
```

**Smoke Tests**:
```yaml
- name: Run Smoke Tests
  run: |
    npm run test:smoke
  env:
    BASE_URL: https://your-app.com
```

**Performance Checks**:
```yaml
- name: Lighthouse CI
  run: |
    npm install -g @lhci/cli@0.12.x
    lhci autorun
  env:
    LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

### Step 9: Set Up Notifications

**Slack Notifications**:
```yaml
- name: Notify Slack on Success
  if: success()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    channel: '#deployments'
    text: 'Deployment successful!'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

- name: Notify Slack on Failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    channel: '#alerts'
    text: 'Deployment failed!'
```

### Step 10: Configure Rollback Strategy

**Automatic Rollback on Failure**:
```yaml
- name: Deploy
  id: deploy
  run: |
    # Deploy command
    vercel --prod

- name: Verify Deployment
  id: verify
  run: |
    sleep 30
    curl -f https://your-app.com/health
  continue-on-error: true

- name: Rollback on Failure
  if: steps.verify.outcome == 'failure'
  run: |
    echo "Deployment verification failed, rolling back..."
    vercel rollback
```

**Manual Rollback**:
```bash
# Via CLI
vercel rollback

# Via Git
git revert HEAD
 git push
```

## Integration with OpenSpec

- Run CI pipeline after `openspec-apply-change` completes
- Use `openspec-verify-change` as part of CI verification
- Archive changes automatically after successful deployment
- Link deployment status to change documentation

## Guardrails

- **Test before deploying** - Never deploy without running tests
- **Use staging environment** - Always test in staging first
- **Keep secrets secure** - Never commit secrets to repository
- **Monitor deployments** - Watch for errors after deployment
- **Have rollback plan** - Know how to revert quickly
- **Document deployments** - Record what was deployed when

## Common Patterns

**Feature Branch Workflow**:
```yaml
on:
  push:
    branches-ignore:
      - main

jobs:
  preview:
    steps:
      - name: Deploy Preview
        run: vercel --target=preview
```

**Tag-based Production Deployment**:
```yaml
on:
  push:
    tags:
      - 'v*'

jobs:
  production:
    environment: production
    steps:
      - name: Deploy to Production
        run: vercel --prod
```

**Monorepo Deployment**:
```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      frontend: ${{ steps.changes.outputs.frontend }}
      backend: ${{ steps.changes.outputs.backend }}
    steps:
      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            frontend:
              - 'apps/frontend/**'
            backend:
              - 'apps/backend/**'
  
  deploy-frontend:
    needs: changes
    if: ${{ needs.changes.outputs.frontend == 'true' }}
    steps:
      - name: Deploy Frontend
        run: vercel --cwd apps/frontend
  
  deploy-backend:
    needs: changes
    if: ${{ needs.changes.outputs.backend == 'true' }}
    steps:
      - name: Deploy Backend
        run: vercel --cwd apps/backend
```

## Requirements

- Access to CI/CD platform (GitHub Actions, GitLab CI, etc.)
- Deployment target access (Vercel, AWS, GCP, etc.)
- Secrets management (GitHub Secrets, Vault, etc.)
- Infrastructure access (for database, cache, etc.)

## Output Format

After setting up CI/CD:

```
## CI/CD Pipeline Configuration

**Platform**: [GitHub Actions/GitLab CI/etc.]
**Environments**: [List of configured environments]

### Workflows Created

1. **CI** (.github/workflows/ci.yml)
   - Triggers: Push to main/develop, PRs
   - Jobs: Lint, Test, Build
   - Duration: ~3 minutes

2. **Deploy Staging** (.github/workflows/deploy-staging.yml)
   - Triggers: Push to develop
   - Jobs: Deploy to Vercel Preview
   - URL: https://staging-your-app.vercel.app

3. **Deploy Production** (.github/workflows/deploy-prod.yml)
   - Triggers: Tags (v*)
   - Jobs: Security scan, Deploy, Verify
   - URL: https://your-app.com
   - Rollback: Enabled

### Secrets Configured

- [x] DATABASE_URL
- [x] API_KEY
- [x] JWT_SECRET
- [x] VERCEL_TOKEN

### Deployment Strategy

- Staging: Auto-deploy on push to develop
- Production: Manual deploy via git tag
- Rollback: Automatic on health check failure

### Verification

- Health check: /health endpoint
- Smoke tests: 5 critical user flows
- Performance: Lighthouse CI
```

## See Also

- `testing-qa` - Test automation
- `secure-coding-cybersecurity` - Security scanning
- `openspec-verify-change` - Verification steps
- `documentation` - Document deployment process
