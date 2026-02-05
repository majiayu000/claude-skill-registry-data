---
name: devops-fullstack
description: DevOps for fullstack - Docker, CI/CD, deployment, monitoring
sasmp_version: "1.3.0"
bonded_agent: 05-devops-integration
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: devops_operations

# Parameter Schema
parameters:
  type: object
  required: [action]
  properties:
    action:
      type: string
      enum: [containerize, setup_cicd, deploy, configure_monitoring]
      description: The specific DevOps action to perform
    container_runtime:
      type: string
      enum: [docker, podman]
      default: docker
    ci_platform:
      type: string
      enum: [github-actions, gitlab-ci, circleci]
      default: github-actions
    cloud_provider:
      type: string
      enum: [aws, gcp, azure, vercel, railway]

# Return Schema
returns:
  type: object
  properties:
    success: { type: boolean }
    dockerfile: { type: string }
    pipeline: { type: object }
    deployment_config: { type: object }
    monitoring_config: { type: object }

# Retry Configuration
retry:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 2000
  max_delay_ms: 20000
  jitter: true

# Observability
logging:
  level: INFO
  events: [container_built, pipeline_created, deployment_completed]
  metrics: [build_time, deployment_duration, resource_usage]
---

# DevOps Fullstack Skill

Atomic skill for DevOps operations including containerization, CI/CD, and deployment.

## Responsibility

**Single Purpose**: Containerize, automate, and deploy fullstack applications

## Actions

### `containerize`
Create optimized Docker configuration for the application.

```typescript
// Input
{
  action: "containerize",
  container_runtime: "docker"
}

// Output
{
  success: true,
  dockerfile: "FROM node:20-alpine AS builder\n...",
  files: [
    { path: "Dockerfile", content: "..." },
    { path: "docker-compose.yml", content: "..." },
    { path: ".dockerignore", content: "..." }
  ]
}
```

### `setup_cicd`
Configure CI/CD pipeline.

### `deploy`
Deploy application to cloud platform.

### `configure_monitoring`
Set up monitoring and alerting.

## Validation Rules

```typescript
function validateParams(params: SkillParams): ValidationResult {
  if (!params.action) {
    return { valid: false, error: "action is required" };
  }

  if (params.action === 'deploy' && !params.cloud_provider) {
    return { valid: false, error: "cloud_provider required for deployment" };
  }

  return { valid: true };
}
```

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| BUILD_FAILED | Docker build failed | Check Dockerfile syntax |
| PIPELINE_INVALID | CI/CD config invalid | Validate YAML syntax |
| DEPLOYMENT_FAILED | Deployment unsuccessful | Check credentials and resources |
| HEALTH_CHECK_FAILED | Service not healthy | Review logs and config |

## Logging Hooks

```json
{
  "on_invoke": "log.info('devops-fullstack invoked', { action, ci_platform })",
  "on_success": "log.info('DevOps operation completed', { files, duration_ms })",
  "on_error": "log.error('DevOps skill failed', { error })"
}
```

## Unit Test Template

```typescript
import { describe, it, expect } from 'vitest';
import { devopsFullstack } from './devops-fullstack';

describe('devops-fullstack skill', () => {
  describe('containerize', () => {
    it('should create multi-stage Dockerfile', async () => {
      const result = await devopsFullstack({
        action: 'containerize',
        container_runtime: 'docker'
      });

      expect(result.success).toBe(true);
      expect(result.dockerfile).toContain('AS builder');
      expect(result.dockerfile).toContain('AS runner');
    });

    it('should use non-root user', async () => {
      const result = await devopsFullstack({
        action: 'containerize'
      });

      expect(result.dockerfile).toContain('USER');
    });
  });

  describe('setup_cicd', () => {
    it('should create GitHub Actions workflow', async () => {
      const result = await devopsFullstack({
        action: 'setup_cicd',
        ci_platform: 'github-actions'
      });

      expect(result.success).toBe(true);
      expect(result.pipeline.jobs).toBeDefined();
    });
  });
});
```

## Integration

- **Bonded Agent**: 05-devops-integration
- **Upstream Skills**: All development skills
- **Downstream Skills**: fullstack-security

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01 | Initial release |
| 2.0.0 | 2025-01 | Production-grade upgrade with GitOps patterns |
