---
name: dispatching-parallel-agents
description: Identify independent failures and spawn concurrent agents. Turns sequential N×time into 1×time.
type: orchestrate
tier: core
trigger: "run in parallel, multiple independent tasks, concurrent agents, parallel execution"
---

## Purpose

When you have multiple independent failures or tasks that don't depend on each other, dispatch them in parallel. This skill defines how to identify, split, and recombine parallel work.

## Step 1: Independence Check

Tasks are independent if:
- They don't read each other's outputs
- They don't write to the same files
- They don't share database transactions

```
task-A modifies src/auth.ts
task-B modifies src/payments.ts
task-C modifies src/notifications.ts
→ All independent → dispatch in parallel
```

```
task-A creates User model
task-B creates Auth that imports User
→ task-B blocked_by task-A → serial only
```

## Step 2: Parallel Dispatch via Task Tool

Use the `Task` tool to spawn multiple agents simultaneously:

```
Spawn Task 1: {role: "developer", task: "implement auth module", files: ["src/auth.ts"]}
Spawn Task 2: {role: "developer", task: "implement payments module", files: ["src/payments.ts"]}
Spawn Task 3: {role: "tester",    task: "fix auth-abort.test.ts failures", files: ["tests/auth-abort.test.ts"]}
```

These run concurrently. Time to resolution: 1× instead of 3×.

## Step 3: File Lock Protocol

To prevent race conditions, each parallel agent registers its file ownership:

Lock file: `.jonggrang/locks/{agentId}.lock`

```json
{
  "agent_id": "developer-auth-001",
  "role": "developer",
  "files": ["src/auth.ts", "src/auth.test.ts"],
  "acquired_at": "2024-01-01T00:00:00Z"
}
```

**Before writing any file:**
1. Check if a lock exists for that file by another agent
2. If locked → add to your blocked list, skip for now
3. If unlocked → write your lock file, proceed

**After completing task:**
1. Remove your lock file

## Step 4: Recombination

After all parallel agents complete:
1. Collect all outputs (JSON results from each agent)
2. Check for conflicts:
   - Same function modified by two agents → manual resolution needed
   - Imports added to same file → merge required
3. Run tests across the full set to verify no integration issues

## Use This Skill For

**Parallel test fixing:**
```
Test failures: auth-abort.test.ts (3), batch.test.ts (2), race.test.ts (1)
→ Spawn 3 tester agents in parallel, one per file
```

**Independent feature implementation:**
```
Feature: user dashboard
Tasks: [create user profile component, create activity feed component, create settings panel]
→ All independent → dispatch in parallel
```

**Multi-domain reviews:**
```
Review needed: backend changes (3 files) + frontend changes (4 files)
→ Spawn backend-reviewer + frontend-reviewer in parallel
```
