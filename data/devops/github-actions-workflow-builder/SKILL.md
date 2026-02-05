---
name: github-actions-workflow-builder
description: Creates GitHub Actions workflows for CI/CD (test, build, deploy, release). Use when user asks to "setup github actions", "create workflow", "ci/cd pipeline", "automate testing", or "deployment workflow".
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# GitHub Actions Workflow Builder

Creates GitHub Actions workflows for automated testing, building, deploying, and releasing applications.

## When to Use

- "Setup GitHub Actions"
- "Create CI/CD pipeline"
- "Automate tests on push"
- "Deploy on merge to main"
- "Release workflow"
- "Build and test automation"

## Instructions

### 1. Detect Project Type

Identify language/framework:

```bash
# Node.js
[ -f "package.json" ] && echo "Node.js"

# Python
[ -f "requirements.txt" ] && echo "Python"

# Ruby
[ -f "Gemfile" ] && echo "Ruby"

# Go
[ -f "go.mod" ] && echo "Go"

# Docker
[ -f "Dockerfile" ] && echo "Docker"
```

### 2. Create .github/workflows Directory

```bash
mkdir -p .github/workflows
```

### 3. Generate Workflows

## Common Workflows

**1. Test on Pull Request**

`.github/workflows/test.yml`:
```yaml
name: Test

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

**2. Build and Deploy**

`.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_ENV: production

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

**3. Release Automation**

`.github/workflows/release.yml`:
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**4. Docker Build and Push**

`.github/workflows/docker.yml`:
```yaml
name: Docker

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max
```

## Framework-Specific Workflows

**Next.js:**
```yaml
name: Next.js CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Type check
        run: npm run type-check

      - name: Lint
        run: npm run lint

      - name: Build
        run: npm run build

      - name: Run tests
        run: npm test

      - name: E2E tests
        run: npx playwright test
```

**Python/Django:**
```yaml
name: Django CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run migrations
        run: python manage.py migrate
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Run tests
        run: pytest
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
```

**Go:**
```yaml
name: Go CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'
          cache: true

      - name: Download dependencies
        run: go mod download

      - name: Run tests
        run: go test -v -race -coverprofile=coverage.out ./...

      - name: Run linter
        uses: golangci/golangci-lint-action@v3
        with:
          version: latest

      - name: Build
        run: go build -v ./...
```

## Advanced Workflows

**Matrix Testing (Multiple Versions):**
```yaml
name: Matrix Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 21]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm test
```

**Conditional Jobs:**
```yaml
name: Conditional Deploy

on:
  push:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm test

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run deploy:staging

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run deploy:production
```

**Cron Schedule:**
```yaml
name: Nightly Build

on:
  schedule:
    # Run at 2 AM UTC every day
    - cron: '0 2 * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run build
      - run: npm run test:integration
```

**Reusable Workflows:**
```yaml
# .github/workflows/test-reusable.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test

# Use in another workflow
# .github/workflows/main.yml
name: Main CI

on: [push]

jobs:
  call-test-workflow:
    uses: ./.github/workflows/test-reusable.yml
    with:
      node-version: '20'
```

### 4. Secrets Management

**Required secrets for common workflows:**

```yaml
# npm publish
NPM_TOKEN

# Vercel deploy
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID

# AWS deploy
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# Docker Hub
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN

# Codecov
CODECOV_TOKEN

# Slack notifications
SLACK_WEBHOOK_URL
```

**Set secrets:**
1. Go to repository Settings
2. Secrets and variables → Actions
3. New repository secret
4. Add name and value

### 5. Best Practices

**Optimize for speed:**
```yaml
jobs:
  test:
    steps:
      # Cache dependencies
      - uses: actions/setup-node@v3
        with:
          cache: 'npm'

      # Use npm ci instead of npm install
      - run: npm ci

      # Cache build outputs
      - uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

**Fail fast:**
```yaml
strategy:
  fail-fast: true
  matrix:
    node-version: [18, 20]
```

**Conditional steps:**
```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: npm run deploy
```

**Environment protection:**
```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://example.com
    steps:
      - run: npm run deploy
```

### 6. Notifications

**Slack notification:**
```yaml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment completed'
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
  if: always()
```

**Discord notification:**
```yaml
- name: Discord notification
  uses: Ilshidur/action-discord@master
  env:
    DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
  with:
    args: 'Build completed: ${{ job.status }}'
```

### 7. Security Scanning

**CodeQL:**
```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write

    steps:
      - uses: actions/checkout@v3

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

**Dependency Review:**
```yaml
name: Dependency Review

on: [pull_request]

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/dependency-review-action@v3
```

### 8. Common Patterns

**Monorepo (multiple packages):**
```yaml
strategy:
  matrix:
    package: [api, web, mobile]

steps:
  - run: npm test --workspace=packages/${{ matrix.package }}
```

**Preview deployments:**
```yaml
- name: Deploy Preview
  if: github.event_name == 'pull_request'
  run: |
    npx vercel --token=${{ secrets.VERCEL_TOKEN }}
    echo "Preview URL: $(npx vercel ls --token=${{ secrets.VERCEL_TOKEN }} | head -1)"
```

### 9. Troubleshooting

**Debug workflow:**
```yaml
- name: Debug
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "Actor: ${{ github.actor }}"
    env
```

**SSH debugging:**
```yaml
- name: Setup tmate session
  uses: mxschmitt/action-tmate@v3
  if: ${{ failure() }}
```

### 10. Documentation

**Add workflow status badge:**
```markdown
![CI](https://github.com/username/repo/workflows/CI/badge.svg)
```

**Document in README:**
```markdown
## CI/CD

This project uses GitHub Actions for:
- Running tests on every PR
- Building and deploying on merge to main
- Publishing releases on tags

See `.github/workflows/` for workflow definitions.
```

## Workflow Templates

**Complete starter workflow:**
```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  release:
    types: [created]

env:
  NODE_VERSION: '20'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build

  deploy:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - name: Deploy
        run: npm run deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}

  release:
    needs: test
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Best Practices Checklist

- [ ] Cache dependencies for faster builds
- [ ] Use specific action versions (@v3, not @latest)
- [ ] Set appropriate permissions
- [ ] Use secrets for sensitive data
- [ ] Fail fast when appropriate
- [ ] Add status badges to README
- [ ] Use matrix for multi-version testing
- [ ] Enable branch protection rules
- [ ] Review security with CodeQL
- [ ] Document workflows
