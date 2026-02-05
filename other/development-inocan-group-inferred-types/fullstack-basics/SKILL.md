---
name: fullstack-basics
description: Full-stack development fundamentals - architecture, patterns, integration
sasmp_version: "1.3.0"
bonded_agent: 01-fullstack-fundamentals
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: architecture_design

# Parameter Schema
parameters:
  type: object
  required: [action]
  properties:
    action:
      type: string
      enum: [design_architecture, define_api, setup_project, integrate_systems]
      description: The specific fullstack action to perform
    project_type:
      type: string
      enum: [monolith, microservices, serverless, hybrid]
      default: monolith
    tech_stack:
      type: object
      properties:
        frontend: { type: string }
        backend: { type: string }
        database: { type: string }
    scale:
      type: string
      enum: [startup, growth, enterprise]
      default: startup

# Return Schema
returns:
  type: object
  properties:
    success: { type: boolean }
    result: { type: object }
    confidence: { type: number, minimum: 0, maximum: 1 }
    next_steps: { type: array, items: { type: string } }

# Retry Configuration
retry:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000
  jitter: true

# Observability
logging:
  level: INFO
  events: [skill_invoked, action_completed, error_occurred]
  metrics: [execution_time_ms, success_rate]
---

# Fullstack Basics Skill

Atomic skill for full-stack development fundamentals including architecture design, API patterns, and system integration.

## Responsibility

**Single Purpose**: Design and structure fullstack application architectures

## Actions

### `design_architecture`
Design the overall application architecture based on requirements.

```typescript
// Input
{ action: "design_architecture", project_type: "microservices", scale: "growth" }

// Output
{
  success: true,
  result: {
    pattern: "microservices",
    services: ["api-gateway", "user-service", "product-service"],
    communication: "async-messaging",
    database_strategy: "database-per-service"
  },
  confidence: 0.85,
  next_steps: ["Define service boundaries", "Design API contracts"]
}
```

### `define_api`
Define API contracts between frontend and backend.

### `setup_project`
Set up project structure and development workflow.

### `integrate_systems`
Design integration patterns between system components.

## Validation Rules

```typescript
function validateParams(params: SkillParams): ValidationResult {
  if (!params.action) {
    return { valid: false, error: "action is required" };
  }
  if (!["design_architecture", "define_api", "setup_project", "integrate_systems"].includes(params.action)) {
    return { valid: false, error: "Invalid action" };
  }
  return { valid: true };
}
```

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| INVALID_ACTION | Unknown action specified | Check action enum |
| MISSING_CONTEXT | Insufficient project context | Request more details |
| INCOMPATIBLE_STACK | Tech stack conflict | Suggest alternatives |

## Logging Hooks

```json
{
  "on_invoke": "log.info('fullstack-basics invoked', { action, project_type })",
  "on_success": "log.info('Action completed', { result, duration_ms })",
  "on_error": "log.error('Skill failed', { error, params })"
}
```

## Unit Test Template

```typescript
import { describe, it, expect } from 'vitest';
import { fullstackBasics } from './fullstack-basics';

describe('fullstack-basics skill', () => {
  describe('design_architecture', () => {
    it('should return microservices pattern for growth scale', async () => {
      const result = await fullstackBasics({
        action: 'design_architecture',
        project_type: 'microservices',
        scale: 'growth'
      });

      expect(result.success).toBe(true);
      expect(result.result.pattern).toBe('microservices');
      expect(result.confidence).toBeGreaterThan(0.7);
    });

    it('should return monolith for startup scale', async () => {
      const result = await fullstackBasics({
        action: 'design_architecture',
        scale: 'startup'
      });

      expect(result.result.pattern).toBe('monolith');
    });
  });

  describe('validation', () => {
    it('should reject invalid action', async () => {
      await expect(fullstackBasics({ action: 'invalid' }))
        .rejects.toThrow('Invalid action');
    });
  });
});
```

## Integration

- **Bonded Agent**: 01-fullstack-fundamentals
- **Upstream Skills**: None (entry point)
- **Downstream Skills**: frontend-development, backend-development

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01 | Initial release |
| 2.0.0 | 2025-01 | Production-grade upgrade |
