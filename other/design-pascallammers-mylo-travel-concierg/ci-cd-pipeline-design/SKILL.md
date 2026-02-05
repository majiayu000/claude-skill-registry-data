---
name: ci-cd-pipeline-design
description: Guide developers through CI/CD pipeline design including architecture patterns, stage design, and security considerations
license: Complete terms in LICENSE.txt
---

# CI/CD Pipeline Design
**Version:** 0.17.0

## When to Use
- Setting up CI/CD for new project
- Optimizing pipeline performance
- Adding security scanning
- Designing multi-environment deployment

## CI/CD Fundamentals
**CI (Integration):** Auto build/test on every change. Goal: Fast feedback (<10 min)
**CD (Delivery):** Auto prepare releases. Goal: Always deployable main
**CD (Deployment):** Auto deploy to production. Requires: High coverage, feature flags, monitoring

## Pipeline Architectures

### Linear
```
Build → Test → Security → Deploy
```
Best for: Simple projects

### Parallel
```
Build → [Unit|Lint|SAST] → Deploy
```
Best for: Faster feedback

### Multi-Environment
```
Build → Test → Staging → Approval → Production
```
Best for: Production deployments

## Stage Design

### Build
- Cache dependencies, multi-stage builds, version artifacts

### Test (Pyramid)
```
Few E2E (slow) → Some Integration → Many Unit (fast)
```

### Security
| Type | Tools |
|------|-------|
| SAST | SonarQube, Semgrep, CodeQL |
| Dependencies | Snyk, Dependabot |
| Secrets | GitLeaks, TruffleHog |
| Containers | Trivy, Clair |

### Deploy
- Staging: automatic
- Production: manual approval, canary rollout

## Deployment Strategies

### Blue-Green
Deploy to inactive (Green), switch traffic, keep Blue for rollback

### Canary
Route 10% to new version, monitor, gradually increase

### Rolling
Update instances one at a time with health checks

## GitHub Actions Example
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build

  test:
    needs: build
    steps:
      - run: npm test

  deploy-staging:
    needs: test
    environment: staging

  deploy-production:
    needs: deploy-staging
    environment: production
```

## Security Practices
**Never:** Hardcode secrets, commit secrets, log secrets
**Do:** Use env vars, secret management, rotate regularly

## GitHub API Best Practices
- Use fine-scoped PATs or GitHub Apps
- Implement exponential backoff with jitter
- Monitor rate limit headers
- Prevent workflow cascades with `concurrency`
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Best Practices
1. **Fast feedback:** CI under 10 min, parallelize
2. **Reliable:** Reproducible builds, pin versions
3. **Visible:** Clear naming, meaningful errors
4. **Secure:** Scan early, block on failures
5. **Parity:** Same config patterns across environments

---

**End of CI/CD Pipeline Design Skill**
