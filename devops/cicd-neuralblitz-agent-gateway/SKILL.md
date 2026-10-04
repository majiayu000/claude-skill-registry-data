---
name: cicd
description: Continuous integration and delivery pipelines
license: MIT
compatibility: opencode
metadata:
  audience: developer, devops-engineer
  category: devops
---

## What I do

- Design and implement CI/CD pipelines
- Automate build, test, and deployment processes
- Integrate security scanning into pipelines
- Configure deployment strategies (blue-green, canary, rolling)
- Set up artifact management and version control
- Build monitoring and feedback loops for deployments

## When to use me

- When establishing DevOps practices
- When automating software delivery
- When implementing GitOps workflows
- When integrating automated testing
- When setting up release automation
- When building deployment infrastructure

## Key Concepts

### GitHub Actions Pipeline

```yaml
name: CI/CD Pipeline

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
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.sha }}
```

### GitLab CI Pipeline

```yaml
stages:
  - build
  - test
  - security
  - deploy

build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  script:
    - npm test
  coverage: /Coverage: \d+\.\d+%/

security:
  stage: security
  script:
    - npm audit
    - trivy image myapp:latest

deploy:
  stage: deploy
  script:
    - kubectl apply -f k8s/
  only:
    - main
```

### Pipeline Best Practices

- **Fast feedback**: Run fastest tests first
- **Parallel execution**: Distribute tests across runners
- **Caching**: Cache dependencies and build artifacts
- **Infrastructure as Code**: Version control pipeline configs
- **Secret management**: Use secure vaults for credentials
- **Idempotency**: Pipelines should be re-runnable
- **Monitoring**: Track pipeline health and duration

### Security Integration (DevSecOps)

```yaml
security-scan:
  stage: security
  script:
    - trivy fs --severity HIGH,CRITICAL .
    - snyk test
    - checkov -d .
    - semgrep --config=auto .
  allow_failure: false
```

### Deployment Strategies

- **Blue-Green**: Two identical environments, instant switch
- **Canary**: Gradually shift traffic, metric-based rollout
- **Rolling**: Update instances incrementally
- **Feature Flags**: Toggle features without deployment
- **GitOps**: Declarative infrastructure with Git
