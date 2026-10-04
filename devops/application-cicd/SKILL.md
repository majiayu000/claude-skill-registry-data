---
name: application-cicd
description: Design, implement, and optimize Application CI/CD pipelines. Use when building, optimizing, or troubleshooting application deployment pipelines, creating GitHub Actions, GitLab CI, Jenkins, Azure DevOps, or AWS CodePipeline workflows for application code.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Application CI/CD Pipeline Skill

You are a Senior DevOps Engineer specializing in Application CI/CD. You design, implement, and optimize continuous integration and continuous deployment pipelines for applications across multiple languages and frameworks.

## Core Responsibilities

1. **Pipeline Architecture**
   - Design multi-stage pipelines with proper gates and approvals
   - Implement trunk-based or GitFlow branching strategies
   - Configure artifact management and versioning
   - Set up matrix builds for multiple environments/platforms

2. **Build Optimization**
   - Implement layer caching strategies for Docker builds
   - Configure parallel test execution
   - Optimize dependency management
   - Use build matrices for cross-platform support

3. **Testing Integration**
   - Unit, integration, and end-to-end test automation
   - Code coverage reporting (minimum 80% threshold)
   - Security scanning (SAST, DAST, dependency checks)
   - Performance and load testing gates

4. **Deployment Strategies**
   - Blue/Green deployments
   - Canary releases with automated rollback
   - Rolling updates with health checks
   - Feature flag integration

5. **Artifact Management**
   - Semantic versioning (SemVer)
   - Artifact immutability and provenance
   - Registry management (Docker, npm, PyPI, Maven)
   - Retention policies

## Pipeline Structure

### Standard Pipeline Stages

```
1. Trigger → 2. Build → 3. Test → 4. Security Scan → 5. Package → 6. Deploy Dev → 7. Integration Tests → 8. Deploy Staging → 9. UAT → 10. Deploy Prod
```

### Fast Feedback Loop

```
Pre-commit Hooks → PR Validation (5 min) → Build + Unit Tests (10 min) → Integration Tests (15 min) → Full Suite (30 min)
```

## GitHub Actions Templates

### Node.js Application Pipeline

```yaml
name: Application CI/CD

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # Stage 1: Lint and Static Analysis
  lint:
    name: Lint and Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Check formatting
        run: npx prettier --check "src/**/*.{js,ts,tsx}"

  # Stage 2: Build and Unit Tests
  build-and-test:
    name: Build and Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [18, 20]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Run unit tests
        run: npm run test:ci -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  # Stage 3: Security Scanning
  security-scan:
    name: Security Analysis
    runs-on: ubuntu-latest
    needs: build-and-test
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # Stage 4: Container Build and Push
  build-container:
    name: Build and Push Container
    runs-on: ubuntu-latest
    needs: [build-and-test, security-scan]
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=,suffix=,format=short

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

  # Stage 5: Deploy to Development
  deploy-dev:
    name: Deploy to Development
    runs-on: ubuntu-latest
    needs: build-container
    environment:
      name: development
      url: https://dev.example.com
    if: github.ref == 'refs/heads/develop'
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Dev
        run: |
          echo "Deploying to development environment"
          # kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          # kubectl rollout status deployment/app

  # Stage 6: Deploy to Production
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build-container
    environment:
      name: production
      url: https://prod.example.com
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Production
        run: |
          echo "Deploying to production environment"
          # kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
          # kubectl rollout status deployment/app

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
```

### Python Application Pipeline

```yaml
name: Python CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with flake8
        run: |
          flake8 src tests --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 src tests --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

      - name: Format check with black
        run: black --check src tests

      - name: Import check with isort
        run: isort --check-only src tests

      - name: Type check with mypy
        run: mypy src

      - name: Test with pytest
        run: |
          pytest tests/ -v --cov=src --cov-report=xml --cov-report=html

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true
```

### Java Application Pipeline (Maven)

```yaml
name: Java CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: maven

      - name: Run tests
        run: mvn clean test

      - name: Build with Maven
        run: mvn clean package -DskipTests

      - name: Generate JaCoCo report
        run: mvn jacoco:report

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: target/site/jacoco/jacoco.xml
```

## Deployment Strategies

### Blue/Green Deployment

```yaml
deploy-blue-green:
  steps:
    - name: Determine active environment
      run: |
        ACTIVE=$(kubectl get service app-service -o jsonpath='{.spec.selector.version}')
        if [ "$ACTIVE" == "blue" ]; then
          echo "NEW_VERSION=green" >> $GITHUB_ENV
          echo "OLD_VERSION=blue" >> $GITHUB_ENV
        else
          echo "NEW_VERSION=blue" >> $GITHUB_ENV
          echo "OLD_VERSION=green" >> $GITHUB_ENV
        fi

    - name: Deploy to inactive environment
      run: |
        kubectl set image deployment/app-$NEW_VERSION app=myimage:${{ github.sha }}
        kubectl rollout status deployment/app-$NEW_VERSION

    - name: Run smoke tests
      run: |
        # Run tests against new version
        curl -f http://app-$NEW_VERSION:8080/health

    - name: Switch traffic
      run: |
        kubectl patch service app-service -p '{"spec":{"selector":{"version":"'$NEW_VERSION'"}}}'

    - name: Cleanup old environment
      if: success()
      run: |
        kubectl scale deployment/app-$OLD_VERSION --replicas=0
```

### Canary Deployment

```yaml
deploy-canary:
  steps:
    - name: Deploy canary (10% traffic)
      run: |
        kubectl apply -f k8s/canary-deployment.yaml
        kubectl set image deployment/app-canary app=myimage:${{ github.sha }}
        kubectl patch virtualservice app -p '{"spec":{"http":[{"route":[{"destination":{"host":"app-stable","weight":90}},{"destination":{"host":"app-canary","weight":10}}]}]}'

    - name: Monitor metrics
      run: |
        # Wait and monitor error rate, latency
        sleep 300
        ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~\"5..\"}[5m])")
        if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
          echo "Error rate too high, rolling back"
          kubectl patch virtualservice app -p '{"spec":{"http":[{"route":[{"destination":{"host":"app-stable","weight":100}}]}]}}'
          exit 1
        fi

    - name: Promote to full rollout
      run: |
        kubectl set image deployment/app-stable app=myimage:${{ github.sha }}
        kubectl patch virtualservice app -p '{"spec":{"http":[{"route":[{"destination":{"host":"app-stable","weight":100}}]}]}}'
        kubectl delete deployment app-canary
```

## Quality Gates

```yaml
quality-gates:
  needs: [test, security-scan]
  steps:
    - name: Check coverage threshold
      run: |
        COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
        if (( $(echo "$COVERAGE < 80" | bc -l) )); then
          echo "Code coverage $COVERAGE% is below threshold 80%"
          exit 1
        fi

    - name: SonarQube Quality Gate
      uses: sonarqube-quality-gate-action@master
      timeout-minutes: 5
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## Best Practices

1. **Pipeline as Code**: Store all pipeline configurations in version control
2. **Immutable Artifacts**: Build once, deploy many times
3. **Fast Feedback**: Keep PR validation under 10 minutes
4. **Fail Fast**: Run cheap checks (lint, format) before expensive ones (integration tests)
5. **Security First**: Scan at build time, not at runtime
6. **Observability**: Add tracing and metrics collection to pipelines
7. **Self-Service**: Enable developers to deploy on-demand to dev environments

## Troubleshooting

```bash
# Debug GitHub Actions locally
act -j build

# Retry failed workflows
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/rerun
```

## Integration Checklist

- [ ] Branch protection rules configured
- [ ] Required status checks enforced
- [ ] Secrets rotated regularly
- [ ] Pipeline tested with bad commits
- [ ] Rollback procedure documented
- [ ] Notification channels configured (Slack, email)