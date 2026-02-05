---
name: vercel-github-actions
description: Vercel deployment and GitHub Actions CI/CD patterns. Use when deploying to Vercel, managing environments, creating staging URLs, or setting up GitHub Actions workflows.
---

# Vercel + GitHub Actions Skill

Patterns for deploying to Vercel with GitHub Actions CI/CD pipelines.

## Three-Environment Model

| Environment | Branch | Purpose |
|-------------|--------|---------|
| **Preview** | `feature/*` | Auto-generated per PR, ephemeral |
| **Staging** | `staging` | Persistent URL for UAT testing |
| **Production** | `main` | Live user-facing deployment |

## Vercel CLI Commands

### Authentication & Setup

```bash
# Login to Vercel
vercel login

# Link project to Vercel (creates .vercel/project.json)
vercel link

# Pull environment variables to local .env.local
vercel env pull
vercel env pull --environment=production
vercel env pull --environment=preview
```

### Deployments

```bash
# Deploy to preview (default)
vercel

# Deploy to production
vercel --prod

# Deploy prebuilt artifacts (faster, for CI)
vercel deploy --prebuilt
vercel deploy --prebuilt --prod

# Build locally for prebuilt deploy
vercel build
vercel build --prod
```

### Staging Alias Management

Vercel aliases create persistent URLs pointing to specific deployments.

```bash
# Create staging alias (one-time setup)
vercel alias <deployment-url> <project>-staging.vercel.app

# Example:
vercel alias my-app-abc123-team.vercel.app my-app-staging.vercel.app

# Update alias after new staging deploy
vercel alias <new-deployment-url> <project>-staging.vercel.app

# List current aliases
vercel alias ls

# Remove an alias
vercel alias rm <alias-url>
```

**Important**: Aliases point to specific deployments, not branches. After each staging branch deploy, update the alias manually or via CI.

### Rollback & Promotion

```bash
# Rollback production to previous deployment
vercel rollback

# Rollback to specific deployment
vercel rollback <deployment-id>

# Promote a preview deployment to production
vercel promote <deployment-url>

# List deployments
vercel ls
vercel ls --prod
```

### Domains

```bash
# Add custom domain
vercel domains add <domain>

# List domains
vercel domains ls

# Inspect domain configuration
vercel domains inspect <domain>
```

## GitHub Actions Workflow Patterns

### Required Secrets

Configure these in GitHub Repository Settings → Secrets and variables → Actions:

| Secret | Source | Purpose |
|--------|--------|---------|
| `VERCEL_TOKEN` | Vercel Dashboard → Settings → Tokens | CLI authentication |
| `VERCEL_ORG_ID` | `.vercel/project.json` after `vercel link` | Team identifier |
| `VERCEL_PROJECT_ID` | `.vercel/project.json` after `vercel link` | Project identifier |

### Preview Deployment Workflow

```yaml
# .github/workflows/preview.yml
name: Preview Deployment

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

on:
  push:
    branches-ignore:
      - main
      - staging
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=preview --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project
        run: vercel build --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Preview
        id: deploy
        run: |
          url=$(vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }})
          echo "url=$url" >> $GITHUB_OUTPUT

      - name: Comment PR with Preview URL
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Preview deployed: ${{ steps.deploy.outputs.url }}`
            })
```

### Production Deployment Workflow

```yaml
# .github/workflows/production.yml
name: Production Deployment

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test

  deploy-production:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Production
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### Staging with Alias Update

```yaml
# .github/workflows/staging.yml
name: Staging Deployment

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
  STAGING_ALIAS: my-project-staging.vercel.app  # Customize this

on:
  push:
    branches:
      - staging

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=preview --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project
        run: vercel build --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Staging
        id: deploy
        run: |
          url=$(vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }})
          echo "url=$url" >> $GITHUB_OUTPUT

      - name: Update Staging Alias
        run: vercel alias ${{ steps.deploy.outputs.url }} ${{ env.STAGING_ALIAS }} --token=${{ secrets.VERCEL_TOKEN }}

      - name: Output Staging URL
        run: echo "Staging deployed to https://${{ env.STAGING_ALIAS }}"
```

### E2E Tests Against Preview

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps chromium

      - name: Build Application
        env:
          # Add your build-time env vars here (non-secrets only)
          NODE_ENV: test
        run: npm run build

      - name: Run E2E Tests
        env:
          # Point to localhost for self-hosted tests
          PLAYWRIGHT_BASE_URL: http://localhost:4321
        run: npx playwright test

      - name: Upload Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7

      - name: Upload Test Videos on Failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results/
          retention-days: 7
```

## vercel.json Configuration

```json
{
  "framework": "astro",
  "buildCommand": "npm run build",
  "github": {
    "enabled": false,
    "silent": true
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains" }
      ]
    }
  ]
}
```

**Note**: Set `github.enabled: false` when using custom GitHub Actions workflows to prevent duplicate deployments.

## Common Patterns

### Check Deployment Status

```bash
# Get latest deployment info
vercel inspect <deployment-url>

# Check if deployment is ready
curl -s -o /dev/null -w "%{http_code}" https://<deployment-url>/api/health
```

### Environment Variable Management

```bash
# Add environment variable
vercel env add <NAME> <VALUE> --environment=production

# List environment variables
vercel env ls

# Remove environment variable
vercel env rm <NAME> --environment=production
```

### Conditional Workflow Steps

```yaml
# Skip job if secrets not configured
- name: Check secrets
  id: check
  run: |
    if [ -z "${{ secrets.SOME_SECRET }}" ]; then
      echo "skip=true" >> $GITHUB_OUTPUT
    else
      echo "skip=false" >> $GITHUB_OUTPUT
    fi

- name: Conditional step
  if: steps.check.outputs.skip != 'true'
  run: echo "Running because secrets are configured"
```

### PR Comment with Deployment URL

```yaml
- name: Comment PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      const status = '${{ job.status }}' === 'success' ? '✅' : '❌';
      const url = '${{ steps.deploy.outputs.url }}';

      await github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## ${status} Deployment\n\nPreview: ${url}`
      });
```

## Troubleshooting

### "You don't have access to the domain"

The domain isn't configured in Vercel. Use a `.vercel.app` subdomain instead:
```bash
vercel alias <url> <project>-staging.vercel.app
```

### Build works locally but fails in CI

1. Check Node.js version matches (`node -v`)
2. Verify all env vars are set in GitHub Secrets
3. Run `vercel env pull` and compare with CI environment

### Deployment succeeds but site shows errors

1. Check if env vars are set for the correct environment (preview vs production)
2. Verify build command produces expected output
3. Check Vercel function logs: `vercel logs <deployment-url>`

## Security Reminders

- **Never** commit `.vercel/project.json` with sensitive data
- **Never** echo secrets in workflow logs
- Use GitHub's automatic secret masking
- Rotate `VERCEL_TOKEN` periodically
- Use environment-specific secrets (TEST_, STAGING_, PROD_ prefixes)

---

*Patterns extracted from production deployments. Last updated: December 2025*
