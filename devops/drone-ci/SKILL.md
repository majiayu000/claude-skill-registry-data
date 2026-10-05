---
name: drone-ci
description: Use when drone CI — container-native CI/CD, YAML pipelines, plugins,
  secrets, multi-machine builds. Use when working with drone ci.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- ci-cd
- devops
- drone
- infrastructure
- machine-learning
- pipeline
version: 1.0.0
category: devops
---



## Overview

Drone is a container-native CI/CD platform where each pipeline step runs in a Docker container. Simple YAML configuration, plugin ecosystem, and built-in secrets management.

## Capabilities

- Container-native steps (each step is a Docker container)
- YAML pipeline configuration (.drone.yml)
- Plugin ecosystem (Docker, Slack, S3, etc.)
- Encrypted secrets at repo/org level
- Multi-machine runners (Docker, SSH, Kubernetes)
- Matrix builds for testing across environments

## When to Use
**Trigger phrases:**
- "drone ci"
- "Drone CI — container-native CI/CD, YAML pipelines, plugins, secrets, multi-machi"


- Want simple, container-based CI/CD
- Need lightweight CI that runs anywhere Docker runs
- Prefer YAML-driven pipelines over Groovy/scripted CI
- Self-hosted CI with minimal infrastructure

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The drone-ci workflow follows a standard pipeline pattern.

Core flow:
```
# drone-ci primary flow
input = prepare(raw_data)
result = process(input, config={builds, container, drone, machine, multi})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Basic Pipeline
```yaml
# .drone.yml
kind: pipeline
type: docker
name: default

steps:
  - name: test
    image: node:20
    commands:
      - npm ci
      - npm test

  - name: build
    image: plugins/docker
    settings:
      repo: myapp
      tags:
        - ${DRONE_COMMIT_SHA:0:8}
        - latest
      username:
        from_secret: docker_username
      password:
        from_secret: docker_password

  - name: deploy
    image: appleboy/drone-ssh
    settings:
      host: prod.example.com
      username: deploy
      key:
        from_secret: ssh_key
      script:
        - docker pull myapp:latest
        - docker-compose up -d
```

### Matrix Build
```yaml
kind: pipeline
type: docker
name: test

platform:
  os: linux
  arch: amd64

steps:
  - name: test
    image: node:${NODE_VERSION}
    commands:
      - npm ci
      - npm test

matrix:
  NODE_VERSION:
    - 18
    - 20
    - 22
```

### Multi-Pipeline (Dependency)
```yaml
---
kind: pipeline
type: docker
name: build
steps:
  - name: build
    image: plugins/docker
    settings:
      repo: myapp
      tags: latest

---
kind: pipeline
type: docker
name: deploy
depends_on: [build]
steps:
  - name: deploy
    image: appleboy/drone-ssh
    settings:
      host: prod.example.com
      script:
        - docker-compose up -d
```

## Common Patterns

- **Secrets**: `drone secret add --name docker_username --value admin myorg/myrepo`
- **Caching**: Use `drone-s3-cache` plugin for dependency caching
- **Concurrency**: `concurrency: { limit: 1 }` to prevent parallel deploys
- **Conditions**: `when: { branch: [main], event: [push] }` for conditional steps
- **Plugins**: Most integrations are Docker images (plugins/docker, plugins/slack, plugins/s3, and community plugins)

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |