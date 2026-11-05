---
name: persisting-agent-outputs
description: Protocol for agents to write structured outputs that survive session resets and are findable by the orchestrator.
type: orchestrate
tier: core
trigger: "save output, persist results, write report, store findings, agent output location"
---

## Purpose

Agent outputs must be findable after session reset. The orchestrator reads these to resume work and make decisions. This skill defines the exact write protocol.

## Output Location Protocol

All agent outputs go to:
```
.jonggrang/.output/features/{feature_id}/{phase}-{role}-output.json
```

Examples:
```
.jonggrang/.output/features/auth-feature-abc123/
  07-lead-architecture-plan.json
  08-developer-task-001.json
  09-reviewer-design-check.json
  11-reviewer-code-quality.json
  12-test-lead-test-plan.json
  13-tester-results.json
```

## Output File Format

Every output file must include this header:

```json
{
  "jonggrang-output": true,
  "feature_id": "auth-feature-abc123",
  "phase": 8,
  "role": "developer",
  "task_id": "task-001",
  "agent_id": "developer-auth-001",
  "timestamp": "2024-01-01T00:00:00Z",
  "status": "completed",
  "output": {
    // role-specific payload here
  }
}
```

## Role-Specific Output Schemas

**Lead (architecture plan):**
```json
{
  "output": {
    "work_type": "MEDIUM",
    "tasks": [
      { "id": "task-001", "title": "...", "description": "...", "files": [...], "blocked_by": [] },
      { "id": "task-002", "title": "...", "description": "...", "files": [...], "blocked_by": ["task-001"] }
    ],
    "tech_decisions": [...],
    "risk_factors": [...]
  }
}
```

**Developer (implementation):**
```json
{
  "output": {
    "task_id": "task-001",
    "files_modified": ["src/auth.ts"],
    "files_created": ["src/auth.test.ts"],
    "summary": "Implemented JWT auth with refresh tokens",
    "notes": "Used bcrypt for password hashing"
  }
}
```

**Reviewer (review report):**
```json
{
  "output": {
    "approved": true,
    "score": 8,
    "violations": [],
    "warnings": ["Consider adding rate limiting"],
    "required_fixes": []
  }
}
```

**Tester (test results):**
```json
{
  "output": {
    "tests_passed": true,
    "total": 24,
    "passed": 24,
    "failed": 0,
    "coverage": 87.3,
    "failed_tests": []
  }
}
```

## Output File Manifest (phases 8, 12, 14)

After phases 8 (implementation), 12 (code-quality), and 14 (testing) complete, the orchestrator automatically records which files changed via `git diff`. No action required from the agent — file tracking is based on actual git state, not self-reporting.

To inspect what a phase recorded: `jonggrang manifest show [feature-id]`

## Discovery Protocol

When an agent needs to find a previous phase's output:
1. Look in `.jonggrang/.output/features/{feature_id}/`
2. Find files matching `{phase}-{role}-*.json`
3. Parse and use

The orchestrator knows the feature_id from MANIFEST.yaml:
```yaml
feature_id: auth-feature-abc123
```
