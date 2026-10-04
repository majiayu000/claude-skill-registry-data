---
name: ci-cd
description: CI/CD pipeline best practices and implementation
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: devops
---
## What I do
- Design CI/CD pipelines
- Implement automated testing
- Configure build automation
- Manage deployments
- Implement rollback strategies
- Configure notifications
- Manage secrets in pipelines
- Monitor pipeline health

## When to use me
When creating or optimizing CI/CD workflows.

## GitHub Actions Pipeline
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install black isort mypy
      
      - name: Check formatting
        run: |
          black --check .
          isort --check-only .
      
      - name: Type checking
        run: mypy src/

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
        os: [ubuntu-latest, macos-latest]
        exclude:
          - python-version: '3.12'
            os: 'macos-latest'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata for Docker
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Production
        run: |
          echo "Deploying to production..."
          kubectl apply -f k8s/
        env:
          KUBECONFIG: ${{ secrets.KUBE_CONFIG }}
```

## GitLab CI Pipeline
```yaml
stages:
  - lint
  - test
  - build
  - security
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

lint:
  stage: lint
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - black --check .
    - isort --check-only .
    - mypy src/
  only:
    - merge_requests
    - main

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pytest --cov=src
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      junit: report.xml
  parallel:
    matrix:
      - PYTHON_VERSION: ['3.10', '3.11', '3.12']

security:
  stage: security
  image: 
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy fs --exit-code 1 --severity HIGH,CRITICAL .
  allow_failure: true

build:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy:
  stage: deploy
  script:
    - echo "Deploying application..."
  environment:
    name: production
    url: https://example.com
  only:
    - main
```

## Best Practices
```
Pipeline Best Practices:

1. Fast feedback
   Run fast tests first
   Parallelize where possible

2. Isolate environments
   Use containers
   Don't share state

3. Fail fast
   Check linting before testing
   Validate before building

4. Use artifacts
   Pass build outputs between jobs
   Store test results

5. Secure secrets
   Use encrypted secrets
   Don't log sensitive data

6. Single source of truth
   Pipeline as code
   Version controlled

7. Atomic commits
   Small, focused commits
   Clear commit messages

8. Manual approvals
   Require approval for production
   Add gates for critical steps

9. Monitor pipelines
   Track success/failure rates
   Alert on regressions

10. Keep pipelines simple
    Don't overcomplicate
    Extract complex logic to scripts
```
