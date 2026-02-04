---
name: cicd-skill
description: CI/CD pipelines with Git, GitHub Actions, GitLab CI, Jenkins, and deployment strategies.
sasmp_version: "1.3.0"
bonded_agent: 05-cicd-automation
bond_type: PRIMARY_BOND

parameters:
  - name: platform
    type: string
    required: false
    enum: ["github-actions", "gitlab-ci", "jenkins", "argocd"]
    default: "github-actions"
  - name: operation
    type: string
    required: true
    enum: ["build", "test", "deploy", "rollback"]

retry_config:
  strategy: exponential_backoff
  initial_delay_ms: 1000
  max_retries: 3

observability:
  logging: structured
  metrics: enabled
---

# CI/CD Automation Skill

## Overview
Master CI/CD pipelines for automated software delivery.

## Parameters
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| platform | string | No | github-actions | CI/CD platform |
| operation | string | Yes | - | Pipeline operation |

## Core Topics

### MANDATORY
- Git workflows (trunk-based, GitFlow)
- Pull request best practices
- GitHub Actions workflows
- GitLab CI pipelines
- Deployment strategies

### OPTIONAL
- Jenkins pipelines
- ArgoCD GitOps
- Artifact management
- Security scanning

### ADVANCED
- Multi-environment promotion
- Feature flags
- Chaos engineering integration
- Custom actions/runners

## Quick Reference

```bash
# Git
git checkout -b feature/name
git add -p
git commit -m "type: description"
git rebase -i HEAD~3
git push -u origin feature/name

# GitHub CLI
gh pr create --title "feat: add X"
gh pr checkout 123
gh pr merge --squash
gh run list
gh run view 12345 --log

# Rollback
kubectl rollout undo deployment/app
kubectl rollout history deployment/app
```

## Deployment Strategies
| Strategy | Rollback | Use Case |
|----------|----------|----------|
| Rolling | Slow | Low-risk |
| Blue-Green | Instant | Zero-downtime |
| Canary | Fast | High-risk |

## Troubleshooting

### Common Failures
| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Timeout | Slow build | Add caching |
| Test flaky | Unreliable test | Fix isolation |
| Secret missing | Not configured | Add in settings |
| Deploy failed | Auth issue | Check credentials |

### Debug Checklist
1. Check workflow syntax
2. Review full logs
3. Verify secrets set
4. Test locally if possible

### Recovery Procedures

#### Failed Deployment
1. Rollback: `kubectl rollout undo`
2. Identify issue in logs
3. Fix and redeploy

## Resources
- [GitHub Actions Docs](https://docs.github.com/actions)
- [GitLab CI Docs](https://docs.gitlab.com/ee/ci/)
