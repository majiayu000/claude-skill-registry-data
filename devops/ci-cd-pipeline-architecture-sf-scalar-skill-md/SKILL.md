---
name: ci-cd-pipeline-architecture
description: When configuring automated build, test, and deployment workflows for a repository.
version: 2.0.0
category: dev-tools
tags: [dev-tools, ci-cd, automation, devops]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 2200
dangerous: false
requires_review: true
security_level: review-required
dependencies: [git-workflow-branching]
triggers: [ci-cd, pipeline, automation, deployment]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: true }
  shell: { execute: true }
input_requirements: [git repository, build environment config]
output_contract: [declarative pipeline yaml, immutable artifacts, environment promotion]
failure_conditions: [rebuilding per environment, secrets hardcoded, flaky tests ignored]
last_updated: 2026-05-15
---

# CI/CD Pipeline Architecture

## Purpose
Pipelines are the line between "works on my machine" and "production is down." This skill ensures code is built exactly once, tested comprehensively, and deployed reliably through immutable artifacts without human intervention.

## When to use
- Setting up a new GitHub Actions, GitLab CI, or Jenkins workflow
- Automating manual deployment processes
- Enforcing code quality checks on Pull Requests
- Establishing environment promotion strategy (dev → staging → production)

## When NOT to use
- Local development builds (use Makefile or npm scripts)
- Manual hotfixes (always use pipeline)

## Inputs required
- Git repository with configured CI/CD platform (GitHub Actions, GitLab CI, Jenkins)
- Build/test environment specifications
- Environment configurations (dev, staging, prod)
- Secret management platform access

## Workflow
1. **Trigger Definition**: Define strict triggers. Run tests/linters on `pull_request`. Run builds/deployments on `push` to `main` or upon `release` tags.
2. **Fail Fast**: Order jobs sequentially by speed. Run Linters, Type Checkers first. If they fail, halt before running expensive test suites.
3. **Automate Testing**: Run unit and integration tests inside isolated, ephemeral containers (e.g., Docker).
4. **Build Immutable Artifacts**: Compile code or build Docker image exactly ONCE. Tag the artifact with the Git commit SHA.
5. **Promote the Artifact**: Deploy the EXACT SAME artifact from Staging to Production. Do not rebuild for production.
6. **Monitor Deployment**: Log deployment status, verify health checks, alert on failures.
7. **Rollback Strategy**: Define clear rollback criteria and process (revert to previous artifact tag).

## Rules
- MUST inject secrets/API keys via platform's secret manager (NEVER hardcode)
- MUST fail immediately if any step returns non-zero exit code
- MUST tag artifacts with commit SHA (no "latest" tag in production)
- MUST build artifact exactly once, then promote across environments
- MUST NOT rebuild code for different environments
- MUST NOT ignore flaky tests (use `continue-on-error: true`)
- MUST NOT allow manual deployments outside pipeline
- MUST cache dependencies between runs (optimization)

## Anti-patterns
- **Rebuilding for Environments**: Running `npm run build` in staging, then again in production
- **Flaky Test Tolerance**: Adding `continue-on-error: true` instead of fixing flaky test
- **Deploying from Local**: Developer running `deploy.sh` from laptop
- **Hardcoded Secrets**: Passwords/API keys in pipeline YAML
- **Concurrent Deployments**: No lock preventing simultaneous prod deployments
- **No Artifact Tracking**: Unable to trace which code is deployed where
- **Test Skipping**: Disabling tests on main branch to speed up pipeline

## Failure conditions
- Secrets leaked in logs
- Artifact rebuilt per environment
- No way to rollback (missing artifact tags)
- Concurrent deployments possible (race condition)
- Test suite disabled for speed
- Deployment fails without clear error message

## Validation checklist
- [ ] Linters/formatters run first (fail fast)
- [ ] All tests run in isolated environments
- [ ] Artifact built and tagged with commit SHA
- [ ] Same artifact deployed to staging and production
- [ ] Secrets injected via platform, not hardcoded
- [ ] No hardcoded environment-specific values (use env vars)
- [ ] Deployment logs include timing and status
- [ ] Rollback process documented and tested
- [ ] No manual steps required (fully automated)
- [ ] Pipeline failure notifications configured
- [ ] Artifacts retained for minimum period (compliance)
- [ ] Concurrent deploys prevented (lock mechanism)

## Output format
- **Pipeline format**: YAML (GitHub Actions, GitLab CI, or equivalent)
- **Artifact structure**: Docker image tagged with commit SHA, or compiled binaries with version metadata
- **Logs**: Structured JSON with deployment status, timing, git SHA
- **Environment config**: Separate YAML files per environment (dev.yml, staging.yml, prod.yml)
- **Deployment record**: Tracked in artifact registry (ECR, DockerHub, Artifactory, etc.)

## Security considerations
- Secrets MUST be injected via platform secret manager (not environment variables in YAML)
- CI/CD logs MUST NOT output secrets (masking configured)
- Artifact signatures MUST be verified on deployment
- Deployment permissions MUST be role-based (not all contributors can deploy to prod)
- Audit logs MUST track who deployed what when
- Rollback MUST be possible without rebuilding

## Agent execution notes
- Agent MAY: Define pipeline stages, add tests, configure artifact tagging, implement promotion strategy
- Agent MUST NEVER: Hardcode secrets, skip tests, allow rebuilding per environment, enable manual deployments
- Agent MUST ASK: Before adding new environment, before skipping test stage, before modifying deployment strategy
- Agent MUST VALIDATE: Artifacts immutable, secrets not leaked, pipeline is fully declarative

## Example

**❌ Anti-pattern (Rebuilding, secrets hardcoded, no promotion):**
```yaml
# BAD: Separate build jobs per environment
build-staging:
  script:
    - npm run build
    - docker build -t myapp:staging .
    - docker push myapp:staging
  only: [main]

build-production:
  script:
    - npm run build  # REBUILDING!
    - docker build -t myapp:latest .  # No SHA tag!
    - docker push myapp:latest
  only: [tags]

# BAD: Secrets hardcoded
deploy-production:
  script:
    - kubectl set image deployment/api api=$DOCKER_IMAGE
  env:
    AWS_KEY: "AKIA1234567890"  # LEAKED!
    DB_PASSWORD: "super-secret-123"  # LEAKED!
```

**✅ Correct pattern (Single artifact, promotion, secrets managed):**
```yaml
# CORRECT: Single build, tagged with SHA
build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY/myapp:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY/myapp:$CI_COMMIT_SHA
  only: [main, tags]

# CORRECT: Promote existing artifact (no rebuild)
deploy-staging:
  stage: deploy
  script:
    - kubectl set image deployment/api api=$CI_REGISTRY/myapp:$CI_COMMIT_SHA
  environment: staging
  only: [main]

deploy-production:
  stage: deploy
  script:
    - kubectl set image deployment/api api=$CI_REGISTRY/myapp:$CI_COMMIT_SHA
  environment: production
  only: [tags]
  when: manual  # Explicit approval required

# CORRECT: Secrets injected via platform
deploy-production:
  script:
    - echo $AWS_ACCESS_KEY_ID | aws sts get-caller-identity  # Platform injects
    - helm upgrade myapp ./chart -f values-prod.yaml
  secrets:
    AWS_ACCESS_KEY_ID:
      vault: aws/prod/access_key
  environment: production
```
