---
name: scale-ingestion-service
description: Adjust RL ingestion service worker count based on queue backlog to maintain optimal throughput.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: Kubernetes client, queue monitoring service
  - Permissions: read:queue, write:deployment
---

# scale-ingestion-service Specification

**ID**: `scale-ingestion-service`
**Version**: 1.0.0
**Status**: Active
**Owner**: CIC Pipeline Team

---

## Purpose

Monitor ingestion queue depth and automatically scale workers:
- Queue > 500: Scale to 8 workers + send alert
- Queue 100–500: Scale to 4 workers
- Queue < 100: Scale to 2 workers

---

## Trigger

```
scale-ingestion-service [target-queue-depth]
```

---

## Input Schema

```typescript
interface SkillInput {
  targetQueueDepth?: number;  // Optional override (100-500; default: 100)
}
```

---

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  currentQueueDepth: number;
  recommendedWorkers: number;
  previousWorkers: number;
  deploymentTime: string;
  timestamp: string;
}
```

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional errors:

| Code | Message | Handler |
|------|---------|---------|
| `QUEUE_UNAVAILABLE` | Cannot access queue service | Check service connectivity |
| `DEPLOYMENT_FAILED` | Worker scaling failed | Retry or manual rollout |

---

## Full Reference

For Setup, Requirements, Testing, Configuration, and Troubleshooting:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

