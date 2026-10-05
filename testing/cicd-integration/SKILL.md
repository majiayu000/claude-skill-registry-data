---
name: cicd-integration
description: Configure test automation in CI/CD pipelines with quality gates, parallel execution, and reporting. Use when setting up GitHub Actions, GitLab CI, Jenkins.
---

# CI/CD Integration for Testing

Configure comprehensive test automation in CI/CD pipelines with quality gates, parallel execution, caching, and reporting. This skill implements **Phase 6** of the 8-phase testing methodology.

## When to Use This Skill

Use this skill when you need to:

- Set up automated testing in CI/CD
- Configure GitHub Actions for testing
- Set up GitLab CI test pipelines
- Implement quality gates
- Enable parallel test execution
- Configure test result reporting
- Set up test caching for speed

**Trigger phrases**: "CI/CD tests", "GitHub Actions tests", "automated testing pipeline", "quality gates", "test automation", "GitLab CI tests", "Jenkins testing", "parallel tests"

## What This Skill Does

### CI/CD Components

1. **Test Automation**
   - Automated test execution on push/PR
   - Multiple test types (unit, integration, e2e)
   - Environment-specific testing

2. **Quality Gates**
   - Coverage thresholds
   - Test pass requirements
   - Linting and formatting checks

3. **Optimization**
   - Parallel test execution
   - Dependency caching
   - Test result caching

4. **Reporting**
   - Test result summaries
   - Coverage reports
   - Failure notifications

### Platform-Specific Examples

#### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '20'

jobs:
  # ==================== PYTHON TESTS ====================
  python-tests:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run linting
        run: |
          ruff check .
          black --check .
          mypy src/

      - name: Run unit tests
        run: |
          pytest tests/unit -v \
            --cov=src \
            --cov-report=xml \
            --cov-report=html \
            --junitxml=test-results/unit.xml

      - name: Run integration tests
        run: |
          pytest tests/integration -v \
            --junitxml=test-results/integration.xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: true

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.python-version }}
          path: test-results/

  # ==================== JAVASCRIPT TESTS ====================
  javascript-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: ['18', '20']

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run type checking
        run: npm run type-check

      - name: Run unit tests
        run: npm test -- --coverage --ci

      - name: Upload coverage
        uses: codecov/codecov-action@v4

  # ==================== QUALITY GATE ====================
  quality-gate:
    needs: [python-tests, javascript-tests]
    runs-on: ubuntu-latest
    steps:
      - name: Download all test results
        uses: actions/download-artifact@v4

      - name: Check test results
        run: |
          echo "All tests passed - quality gate check complete"

  # ==================== E2E TESTS ====================
  e2e-tests:
    needs: quality-gate
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup environment
        run: |
          cp .env.test .env
          docker-compose up -d

      - name: Wait for services
        run: |
          sleep 10
          curl --retry 10 --retry-delay 3 http://localhost:3000/health

      - name: Run E2E tests
        run: |
          npm run test:e2e

      - name: Stop services
        if: always()
        run: docker-compose down
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - quality
  - e2e

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  NPM_CONFIG_CACHE: "$CI_PROJECT_DIR/.cache/npm"

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/
    - node_modules/
    - .venv/

# ==================== LINT ====================
lint:python:
  stage: lint
  image: python:3.11
  before_script:
    - pip install ruff black mypy
  script:
    - ruff check .
    - black --check .
    - mypy src/

lint:javascript:
  stage: lint
  image: node:20
  before_script:
    - npm ci
  script:
    - npm run lint
    - npm run type-check

# ==================== TESTS ====================
test:python:
  stage: test
  image: python:3.11
  parallel:
    matrix:
      - PYTHON_VERSION: ['3.10', '3.11', '3.12']
  before_script:
    - pip install -e ".[dev]"
  script:
    - pytest tests/unit -v --cov=src --cov-report=xml --junitxml=report.xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    when: always
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

test:javascript:
  stage: test
  image: node:20
  before_script:
    - npm ci
  script:
    - npm test -- --ci --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

# ==================== QUALITY GATE ====================
quality:check:
  stage: quality
  needs:
    - test:python
    - test:javascript
  script:
    - echo "Quality gate passed"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

# ==================== E2E ====================
e2e:tests:
  stage: e2e
  needs:
    - quality:check
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2376
  before_script:
    - docker-compose up -d
    - sleep 15
  script:
    - docker-compose run app npm run test:e2e
  after_script:
    - docker-compose down
```

#### Jenkins (Jenkinsfile)

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
        NODE_VERSION = '20'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            parallel {
                stage('Python Lint') {
                    agent {
                        docker { image 'python:3.11' }
                    }
                    steps {
                        sh 'pip install ruff black mypy'
                        sh 'ruff check .'
                        sh 'black --check .'
                    }
                }
                stage('JavaScript Lint') {
                    agent {
                        docker { image 'node:20' }
                    }
                    steps {
                        sh 'npm ci'
                        sh 'npm run lint'
                    }
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Python Tests') {
                    agent {
                        docker { image 'python:3.11' }
                    }
                    steps {
                        sh 'pip install -e ".[dev]"'
                        sh 'pytest tests/ -v --cov=src --junitxml=results.xml'
                    }
                    post {
                        always {
                            junit 'results.xml'
                            publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                        }
                    }
                }
                stage('JavaScript Tests') {
                    agent {
                        docker { image 'node:20' }
                    }
                    steps {
                        sh 'npm ci'
                        sh 'npm test -- --ci --coverage'
                    }
                    post {
                        always {
                            junit 'junit.xml'
                        }
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def coverage = readFile('coverage.xml')
                    if (!coverage.contains('line-rate="0.8')) {
                        error "Coverage below 80% threshold"
                    }
                }
            }
        }

        stage('E2E Tests') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker-compose up -d'
                sh 'sleep 15'
                sh 'npm run test:e2e'
            }
            post {
                always {
                    sh 'docker-compose down'
                }
            }
        }
    }

    post {
        failure {
            emailext subject: "Build Failed: ${env.JOB_NAME}",
                     body: "Check console output at ${env.BUILD_URL}",
                     recipientProviders: [developers()]
        }
    }
}
```

## Prerequisites

- Tests written and passing locally
- CI/CD platform access
- Repository configuration permissions
- Understanding of deployment workflow

## Instructions

### Step 1: Choose CI/CD Platform

1. **Evaluate Options**
   - GitHub Actions (GitHub repos)
   - GitLab CI (GitLab repos)
   - Jenkins (self-hosted)
   - Azure DevOps (Microsoft ecosystem)

2. **Configure Access**
   - Repository permissions
   - Secrets management
   - Environment variables

### Step 2: Configure Test Pipeline

1. **Define Stages**
   - Lint/format checks
   - Unit tests
   - Integration tests
   - E2E tests (optional)

2. **Set Up Caching**
   - Dependencies
   - Build artifacts
   - Test results

3. **Configure Parallelization**
   - Matrix builds
   - Parallel jobs
   - Sharded tests

### Step 3: Implement Quality Gates

1. **Coverage Thresholds**
   - Minimum line coverage
   - Branch coverage
   - Per-file thresholds

2. **Test Requirements**
   - All tests must pass
   - No regressions allowed
   - Performance thresholds

## Quality Checklist

- [ ] Pipeline triggers on push and PR
- [ ] Tests run in parallel where possible
- [ ] Dependencies cached effectively
- [ ] Coverage reports uploaded
- [ ] Quality gates configured
- [ ] Failure notifications set up
- [ ] E2E tests run on main branch

## Related Skills

- `test-structure` - Test infrastructure (Phase 1)
- `code-coverage` - Coverage analysis (Phase 7)
- `performance-testing` - Load testing (Phase 5)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/maintenance_cicd/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
