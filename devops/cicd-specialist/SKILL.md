---
name: cicd-specialist
description: CI/CD pipeline design and configuration for GitHub Actions, GitLab CI,
  Jenkins, CircleCI, and Azure DevOps. Use when asked to write a pipeline, set up
  automated testing or deployment, configure build caching, add security scanning
  to CI, implement blue-green or canary deployments, set up artifact publishing, or
  fix a broken pipeline.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-platform
  tags:
  - cicd
  - github-actions
  - gitlab-ci
  - jenkins
  - deployment
  - automation
  - pipelines
---

# CI/CD Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `set up a pipeline`, `GitHub Actions`, `GitLab CI`.
- The requested work fits this skill's lane: Pipeline configuration, build automation, deployment strategies, security scanning in CI, artifact management.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Application build logic; infrastructure provisioning.

## First actions
1. `Glob('**/.github/workflows/*.yml', '**/.gitlab-ci.yml', '**/Jenkinsfile', '**/.circleci/config.yml', '**/azure-pipelines.yml')` — identify CI platform in use
2. Read the existing pipeline file to understand current stages, caching approach, and deployment targets
3. Identify: branch strategy (gitflow vs trunk), deployment environments (dev/staging/prod), secret management approach

## Decision rules
- If no CI platform files exist: ask which platform before writing anything
- For caching: always cache dependency directories keyed on lock file hash (package-lock.json, Pipfile.lock, go.sum)
- For secrets: never echo secrets; use platform-provided secret variables; never commit .env files
- For deployment: include smoke tests after deploy; include rollback step for production
- If Kubernetes is the deploy target: generate manifests in CI, apply in CD step; route k8s config to kubernetes-specialist

## Steps

### Step 1: Read existing pipeline
Understand current stages, what's already working, and what's broken or missing.

### Step 2: Write or modify pipeline
Structure: trigger → checkout → cache restore → build → test → security scan → artifact publish → deploy → smoke test → notify. Apply only stages relevant to the task.

### Step 3: Validate
For GitHub Actions: use `act` locally if available, or validate YAML syntax. For GitLab: validate with `gitlab-ci-lint` endpoint. Always check secret variable names are referenced correctly.

## Output contract
- Primary artifact: pipeline YAML file at the correct platform path
- Required: caching configured; secrets referenced as variables (not hardcoded); at least one test stage
- Security: dependency scanning and container scanning stages included for any Dockerfile-based projects

## Constraints
- NEVER hardcode credentials, tokens, or passwords in pipeline files
- NEVER push to production without a manual approval gate or smoke test
- Scope boundary: application build logic belongs to the app; infrastructure provisioning belongs to terraform/cloud specialists

## Examples

### Example 1: GitHub Actions pipeline
User says: "Set up a GitHub Actions pipeline for my Python Flask app that runs tests and deploys to AWS ECS"
Actions:
1. Glob for existing .github/workflows/
2. Write workflow with: trigger on push to main, pip cache keyed on requirements.txt hash, pytest stage, Docker build+push to ECR, ECS task definition update
Result: .github/workflows/deploy.yml with all stages

## Troubleshooting
**Pipeline triggers but skips expected jobs**
Cause: `if:` conditions or path filters excluding the run
Fix: Check `paths:` filters and branch conditions; use workflow dispatch to test manually

**Cache miss on every run**
Cause: Cache key includes volatile data
Fix: Key cache on lock files only: `hashFiles('**/package-lock.json')`

## Reference
- `references/legacy-agent.md`: full platform reference — GitHub Actions, GitLab CI, Jenkins, CircleCI patterns; caching strategies; security scanning; deployment automation
