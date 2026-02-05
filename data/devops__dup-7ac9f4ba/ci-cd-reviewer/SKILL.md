---
name: ci-cd-reviewer
description: |
  WHEN: CI/CD pipeline review, GitHub Actions, GitLab CI, Jenkins, build optimization
  WHAT: Pipeline structure + Job optimization + Security scanning + Caching strategy + Deployment patterns
  WHEN NOT: Kubernetes → k8s-reviewer, Terraform → terraform-reviewer
---

# CI/CD Reviewer Skill

## Purpose
Reviews CI/CD pipelines for structure, security, optimization, and best practices.

## When to Use
- GitHub Actions workflow review
- GitLab CI pipeline review
- Jenkins pipeline review
- Build optimization
- Deployment strategy review

## Project Detection
- `.github/workflows/*.yml`
- `.gitlab-ci.yml`
- `Jenkinsfile`
- `azure-pipelines.yml`
- `.circleci/config.yml`

## Workflow

### Step 1: Analyze Project
```
**Platform**: GitHub Actions
**Triggers**: push, pull_request
**Jobs**: build, test, deploy
**Environments**: staging, production
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full CI/CD review (recommended)
- Pipeline structure
- Security and secrets
- Caching and optimization
- Deployment strategy
multiSelect: true
```

## Detection Rules

### GitHub Actions

#### Workflow Structure
| Check | Recommendation | Severity |
|-------|----------------|----------|
| All jobs sequential | Parallelize independent jobs | MEDIUM |
| No job dependencies | Add needs for proper order | HIGH |
| Duplicate steps | Extract to composite action | MEDIUM |
| No concurrency control | Add concurrency group | MEDIUM |

```yaml
# BAD: Sequential, no optimization
name: CI
on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm run build
      - run: npm test
      - run: npm run lint
      - run: docker build .
      - run: docker push

# GOOD: Parallel jobs with dependencies
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test

  build:
    needs: [lint, test]  # Run after lint and test pass
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
      - run: ./deploy.sh
```

#### Security
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Secrets in plain text | Use secrets context | CRITICAL |
| No permissions defined | Add explicit permissions | HIGH |
| Third-party actions unpinned | Pin to SHA | HIGH |
| No environment protection | Use environments | MEDIUM |

```yaml
# BAD: Security issues
name: Deploy
on: push

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: |
          curl -X POST https://api.example.com \
            -H "Authorization: Bearer ${{ secrets.API_KEY }}"
      - uses: some-org/some-action@main  # Unpinned!

# GOOD: Secure workflow
name: Deploy

on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write  # For OIDC

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502 # v4.0.2
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy
        run: ./deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

#### Caching
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No dependency caching | Add cache action | HIGH |
| No Docker layer cache | Use buildx cache | MEDIUM |
| Cache key not specific | Include lockfile hash | MEDIUM |

```yaml
# GOOD: Comprehensive caching
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Node.js caching
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # Or manual cache
      - uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      # Docker layer caching
      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: myapp:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"

.node_template: &node_template
  image: node:${NODE_VERSION}-alpine
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - node_modules/
  before_script:
    - npm ci --cache .npm --prefer-offline

lint:
  <<: *node_template
  stage: lint
  script:
    - npm run lint

test:
  <<: *node_template
  stage: test
  script:
    - npm test
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  <<: *node_template
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

deploy_staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - ./deploy.sh staging
  only:
    - main

deploy_production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  script:
    - ./deploy.sh production
  when: manual
  only:
    - main
```

### Deployment Strategies
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Direct to production | Add staging environment | HIGH |
| No rollback plan | Add rollback mechanism | HIGH |
| No health checks | Add post-deploy verification | MEDIUM |

```yaml
# Blue-Green / Canary with GitHub Actions
deploy:
  runs-on: ubuntu-latest
  environment: production
  steps:
    - name: Deploy canary (10%)
      run: |
        kubectl set image deployment/app app=myapp:${{ github.sha }}
        kubectl rollout status deployment/app --timeout=5m

    - name: Verify canary
      run: |
        sleep 60
        ./verify-deployment.sh

    - name: Promote to 100%
      if: success()
      run: kubectl scale deployment/app --replicas=10

    - name: Rollback on failure
      if: failure()
      run: kubectl rollout undo deployment/app
```

## Response Template
```
## CI/CD Review Results

**Project**: [name]
**Platform**: GitHub Actions
**Jobs**: 4 | **Workflows**: 2

### Pipeline Structure
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | ci.yml | All jobs run sequentially |

### Security
| Status | File | Issue |
|--------|------|-------|
| HIGH | deploy.yml | Actions not pinned to SHA |

### Caching
| Status | File | Issue |
|--------|------|-------|
| HIGH | ci.yml | No dependency caching |

### Deployment
| Status | File | Issue |
|--------|------|-------|
| HIGH | deploy.yml | No staging environment |

### Recommended Actions
1. [ ] Parallelize lint and test jobs
2. [ ] Pin all actions to commit SHA
3. [ ] Add npm caching
4. [ ] Add staging deployment step
```

## Best Practices
1. **Structure**: Parallel jobs, proper dependencies
2. **Security**: Pin actions, use OIDC, minimal permissions
3. **Caching**: Cache dependencies and Docker layers
4. **Deployment**: Staging → Production with approvals
5. **Monitoring**: Add status checks and notifications

## Integration
- `docker-reviewer`: Container build steps
- `k8s-reviewer`: Kubernetes deployments
- `security-scanner`: SAST/DAST in pipeline
