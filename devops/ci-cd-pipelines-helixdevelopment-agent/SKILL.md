---
name: ci-cd-pipelines
description: Design and implement CI/CD pipelines for automated testing, building, and deployment. Support multiple platforms and deployment strategies.
triggers:
- /ci cd
- /pipeline
---

# CI/CD Pipeline Design

This skill guides you through designing and implementing continuous integration and continuous deployment pipelines for automated software delivery.

## When to use this skill

Use this skill when you need to:
- Set up automated build pipelines
- Implement continuous deployment
- Design multi-stage release workflows
- Configure pipeline security and compliance
- Optimize pipeline performance

## Prerequisites

- CI/CD platform (GitHub Actions, GitLab CI, Azure DevOps, Jenkins)
- Source code repository access
- Deployment target access (servers, Kubernetes, cloud)
- Container registry (for containerized apps)

## Guidelines

### Pipeline Architecture

**Pipeline Stages**
```
Code Commit → Build → Test → Security Scan → Deploy to Dev → Deploy to Prod
     ↓           ↓      ↓         ↓              ↓              ↓
   Trigger   Compile  Unit    SAST/DAST    Integration    Smoke Tests
             & Package Tests    Tests        Tests
```

**Pipeline Types**
- **Continuous Integration**: Build and test on every commit
- **Continuous Delivery**: Deploy to staging automatically, prod manually
- **Continuous Deployment**: Deploy to production automatically
- **GitOps**: Declarative infrastructure and application deployment

### GitHub Actions Example

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-test:
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
      
      - name: Run tests
        run: npm test -- --coverage
      
      - name: Build application
        run: npm run build

  security-scan:
    runs-on: ubuntu-latest
    needs: build-and-test
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          format: 'sarif'
          output: 'trivy-results.sarif'

  build-and-push:
    runs-on: ubuntu-latest
    needs: [build-and-test, security-scan]
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-and-push
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

### Deployment Strategies

**Blue-Green Deployment**
- Maintain two identical environments
- Route traffic to active (blue) environment
- Deploy to inactive (green) environment
- Switch traffic after validation
- Instant rollback capability

**Canary Deployment**
- Deploy to small subset of servers/users
- Monitor metrics and errors
- Gradually increase traffic
- Roll back if issues detected
- Minimizes blast radius

**Rolling Deployment**
- Update instances one by one
- Maintain application availability
- Slower but resource efficient
- Automatic rollback on failure

### Security Best Practices

**Secrets Management**
- Store secrets in CI/CD platform vault
- Use short-lived credentials
- Rotate secrets regularly
- Never commit secrets to code

**Pipeline Security**
- Pin action versions to commit SHA
- Require signed commits
- Implement branch protection
- Run security scans (SAST, DAST, SCA)
- Use least privilege service accounts

**Artifact Security**
- Sign container images
- Scan for vulnerabilities
- Use private registries
- Implement image promotion

### Pipeline Optimization

**Caching**
- Cache dependencies (npm, pip, Maven)
- Cache Docker layers
- Use cache keys based on lock files
- Invalidate cache when needed

**Parallelization**
- Run independent jobs in parallel
- Use job matrices for multiple versions
- Parallelize test execution
- Distribute builds across runners

**Conditional Execution**
- Skip unnecessary steps
- Run jobs only on specific branches
- Use paths filters for monorepos
- Fail fast on critical checks

## Examples

See the `examples/` directory for:
- `github-actions/` - GitHub Actions workflows
- `gitlab-ci/` - GitLab CI configurations
- `deployment-strategies/` - Blue-green and canary examples
- `security-scanning/` - Security scan configurations

## References

- [GitHub Actions documentation](https://docs.github.com/actions)
- [GitLab CI/CD documentation](https://docs.gitlab.com/ee/ci/)
- [Azure DevOps Pipelines](https://docs.microsoft.com/azure/devops/pipelines/)
- [Trunk-based development](https://trunkbaseddevelopment.com/)
- [Continuous Delivery book](https://continuousdelivery.com/)
