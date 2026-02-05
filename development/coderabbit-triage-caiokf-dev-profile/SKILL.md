---
name: coderabbit-triage
description: Analyze code review findings and create execution plan. Decides parallel vs sequential fixing based on issue severity and independence. Returns structured task list with clear fixer instructions.
---

# Triaging Issues

## Overview

This skill transforms CodeRabbit's raw findings into an executable task plan. It analyzes issues by severity, checks for dependencies, and decides the optimal execution strategy (parallel fixers vs sequential).

**Input**: JSON from `coderabbit-request`

**Output**: Structured task dispatch plan with fixer instructions

**When to use**: After CodeRabbit review completes, before dispatching fixer subagents.

## Decision Logic

### Step 1: Count and Categorize

Analyze the issue distribution:

```text
Critical (security, data corruption, crashes):
  - Race conditions, missing auth/validation, unsafe state mutations
  - Must fix immediately, cannot ship with these

Important (bugs, performance issues, missing error handling):
  - Logic errors, performance regressions, unhandled edge cases
  - Should fix before merge, affects product quality

Minor (style, simplification, documentation):
  - Code clarity, pattern consistency, comments
  - Can defer but should fix for consistency
```

### Step 2: Identify Independent Domains

For critical issues, check if they're in the same domain:

**Independent** (can fix in parallel):

- Race condition in webhook async handler (domain: concurrency)
- Missing signature verification (domain: security)
- Missing error logging (domain: observability)

**Dependent** (must fix sequentially):

- Missing signature verification depends on understanding webhook flow
- Missing error handling in same flow that signature relies on
- Both in same file and related code paths

**Same domain** (likely sequential):

- Race condition in webhook handler AND race condition in retry logic
- Both race conditions, likely need same fix pattern

### Step 3: Check File/Region Overlap

Before deciding strategy, check if issues share files or have overlapping line ranges:

```text
File overlap check:
  - Group all issues by file path
  - If multiple issues target the same file → they are DEPENDENT
  - Same-file issues cannot run in parallel (risk of merge conflicts)

Region overlap check (for same-file issues):
  - If line ranges overlap or are within 20 lines → tightly coupled
  - If line ranges are far apart but same file → still dependent (file lock)

Example:
  Task 1: src/webhooks.ts:42 (signature verification)
  Task 2: src/webhooks.ts:89 (idempotency handling)
  Task 3: src/webhooks.ts:156 (error logging)
  → All target same file → DEPENDENT → use SINGLE_COMPREHENSIVE or BATCH_SEQUENTIAL
```

### Step 4: Decide Execution Strategy

```text
IF 0 critical issues:
  Strategy: "COMPLETE"
  Status: "No critical issues found"
  Offer: "Fix important + minor issues?"

IF 1-3 critical AND all in DIFFERENT files AND non-overlapping:
  Strategy: "PARALLEL_CRITICAL"
  Pattern: Dispatch each critical as separate subagent
  Then: Sequential important/minor fixers
  Prerequisite: No two critical issues share the same file

IF critical issues share same file OR have overlapping regions:
  Strategy: "SINGLE_COMPREHENSIVE"
  Pattern: One fixer with full file context handles all issues in that file
  Reason: Prevents merge conflicts, simpler coordination for same-file edits

IF 3+ critical OR critical issues have logical dependencies:
  Strategy: "SEQUENTIAL"
  Pattern: Fix each critical, verify, then move to next
  Reason: Complex dependencies require verification between fixes

IF only important/minor (no critical):
  Strategy: "BATCH_SEQUENTIAL"
  Pattern: Group by file, fix each file completely before moving to next
  Reason: Reduces context switching, prevents same-file conflicts
```

### Step 5: Create Task Dispatch Plan

For each issue, create a fixer task:

```json
{
  "total_issues": 3,
  "by_severity": {
    "critical": 1,
    "important": 2,
    "minor": 0
  },
  "strategy": "SINGLE_COMPREHENSIVE",
  "analysis": {
    "all_issues_same_file": true,
    "file": "src/webhooks.ts",
    "reason": "All 3 issues target same file - must fix sequentially to prevent conflicts",
    "critical_are_independent": false,
    "important_are_related": true,
    "minor_count": 0
  },
  "tasks": [
    {
      "task_id": 1,
      "severity": "critical",
      "priority": 1,
      "domain": "payment-webhook-security",
      "file": "src/webhooks.ts",
      "line": 42,
      "issue": "Missing HMAC signature verification for webhook authenticity",
      "coderabbit_suggestion": "Add HMAC-SHA256 signature verification using crypto module. Compare against timestamp to prevent replay attacks.",
      "fixer_instructions": [
        "1. Import crypto.timingSafeEqual at top of file",
        "2. At webhook handler entry (line 42), before processing body:",
        "   - Extract 'X-Webhook-Signature' header",
        "   - Extract request body as raw string",
        "   - Compute HMAC-SHA256 signature using process.env.WEBHOOK_SECRET",
        "   - Use timingSafeEqual to compare (prevents timing attacks)",
        "   - Return 401 Unauthorized if verification fails",
        "3. Extract 'X-Webhook-Timestamp' header",
        "4. Verify timestamp is within 5 minutes of current time",
        "5. Return 401 if timestamp too old (replay attack protection)",
        "6. Add structured logging: {timestamp, signature_valid, webhook_id, processed: true}",
        "7. Run: npm test -- src/webhooks.test.ts",
        "8. Verify all webhook security tests pass"
      ],
      "constraints": [
        "DO NOT modify webhook body parsing logic",
        "DO NOT change authentication for other endpoints",
        "DO NOT remove existing error handling",
        "ONLY modify webhook entry point validation"
      ],
      "estimated_time": "10 minutes",
      "can_run_parallel_with": [],
      "must_complete_before": [2, 3],
      "same_file_as": [2, 3]
    },
    {
      "task_id": 2,
      "severity": "important",
      "priority": 2,
      "domain": "webhook-concurrency",
      "file": "src/webhooks.ts",
      "line": 89,
      "issue": "Race condition: multiple concurrent webhook calls can update state simultaneously",
      "coderabbit_suggestion": "Implement idempotency key handling. Store processed keys in cache with TTL to deduplicate retries.",
      "fixer_instructions": [
        "1. Create idempotency key map at module level:",
        "   const idempotencyCache = new Map()",
        "2. At webhook handler (line 89), extract 'X-Idempotency-Key' header",
        "3. Check if key exists in cache:",
        "   - IF exists: return cached result (prevents duplicate processing)",
        "   - IF not exists: continue processing",
        "4. Process webhook (database writes, event emits, etc)",
        "5. Store result in cache with 24-hour TTL:",
        "   idempotencyCache.set(key, {result, timestamp: Date.now()})",
        "6. Clean up old entries (cron every hour):",
        "   - Remove keys older than 24 hours",
        "7. Add test: duplicate webhook with same key returns same result",
        "8. Add test: webhook with different key processes independently",
        "9. Run: npm test -- src/webhooks.test.ts",
        "10. Verify idempotency and concurrency tests pass"
      ],
      "constraints": [
        "DO NOT modify signature verification logic (task 1)",
        "DO NOT remove existing error handling",
        "DO NOT change database schema",
        "ONLY add idempotency deduplication"
      ],
      "estimated_time": "12 minutes",
      "can_run_parallel_with": [],
      "depends_on": [1],
      "must_complete_before": [3],
      "same_file_as": [1, 3]
    },
    {
      "task_id": 3,
      "severity": "important",
      "priority": 3,
      "domain": "webhook-observability",
      "file": "src/webhooks.ts",
      "line": 156,
      "issue": "Missing error logging for webhook failures. Makes debugging production issues difficult.",
      "coderabbit_suggestion": "Add structured logging with timestamp, error type, and webhook ID. Include full error stack.",
      "fixer_instructions": [
        "1. Import logger at top (ensure it's structured JSON logger)",
        "2. At webhook handler (line 156), add pre-processing log:",
        "   logger.info({event: 'webhook_received', webhook_id, timestamp, domain})",
        "3. Wrap webhook processing in try-catch:",
        "   - On success: logger.info({event: 'webhook_processed', webhook_id, duration_ms})",
        "   - On error: logger.error({event: 'webhook_failed', webhook_id, error_type, error_message, stack})",
        "4. For specific error types, add context:",
        "   - If signature fails: log 'signature_verification_failed'",
        "   - If database fails: log 'database_operation_failed', include operation type",
        "   - If event emit fails: log 'event_emission_failed'",
        "5. Add log levels:",
        "   - Validation failures: warn",
        "   - Processing failures: error",
        "   - Success: info",
        "6. Verify all logs have: webhook_id, timestamp, event_type, error details",
        "7. Run: npm test -- src/webhooks.test.ts",
        "8. Verify logging tests pass"
      ],
      "constraints": [
        "DO NOT change webhook processing logic",
        "DO NOT log sensitive data (secrets, full bodies)",
        "DO NOT break existing tests",
        "ONLY add observability logging"
      ],
      "estimated_time": "8 minutes",
      "can_run_parallel_with": [],
      "depends_on": [1, 2],
      "same_file_as": [1, 2]
    }
  ],
  "execution_plan": {
    "phase_1_sequential": [
      "Step 1: Fix task 1 (signature verification) - critical, must complete first",
      "Step 2: Fix task 2 (idempotency handling) - depends on task 1 completing",
      "Step 3: Fix task 3 (error logging) - depends on tasks 1 and 2 completing"
    ],
    "reason": "All tasks target src/webhooks.ts - sequential execution prevents merge conflicts",
    "verification": {
      "after_each_fix": "Run npm test -- src/webhooks.test.ts",
      "after_all_fixes": [
        "Run full test suite: npm test",
        "Re-run coderabbit: coderabbit --prompt-only --type uncommitted",
        "Verify zero issues remain"
      ]
    }
  },
  "summary": "3 issues identified in src/webhooks.ts. Strategy: SINGLE_COMPREHENSIVE (all same file). Sequential execution required to prevent conflicts. Estimated total time: 30 minutes."
}
```

## Verification Checklist

Before returning plan, verify:

- [ ] Every issue has a task_id
- [ ] Severity is accurately assessed
- [ ] Dependencies identified correctly
- [ ] Strategy choice justified by analysis
- [ ] Fixer instructions are clear and specific
- [ ] Constraints explicitly listed
- [ ] Estimated times are realistic
- [ ] Parallel groups don't have conflicts
- [ ] All CodeRabbit suggestions referenced

## Key Principles

**Analysis over assumption**: Check real dependencies, don't assume everything is parallel.

**Clarity for fixers**: Fixer subagents need exact step-by-step instructions, not vague guidance.

**Constraint enforcement**: Tell fixers explicitly what NOT to change, prevents scope creep.

**Transparency**: Explain WHY you chose a strategy, not just what it is.

## Common Patterns

**All independent critical issues (different files)**:

```json
{
  "strategy": "PARALLEL_CRITICAL",
  "analysis": {
    "files_are_independent": true,
    "no_file_overlap": true
  },
  "tasks": [
    {"task_id": 1, "file": "src/auth.ts", "can_run_parallel_with": [2, 3]},
    {"task_id": 2, "file": "src/payments.ts", "can_run_parallel_with": [1, 3]},
    {"task_id": 3, "file": "src/notifications.ts", "can_run_parallel_with": [1, 2]}
  ]
}
```

**Mix of critical and important**:

```json
{
  "strategy": "SEQUENTIAL_WITH_PARALLEL_IMPORTANT",
  "phase_1": ["critical issues"],
  "phase_2": ["important issues in parallel"]
}
```

**Complex interdependencies**:

```json
{
  "strategy": "SEQUENTIAL",
  "must_complete_before": {
    "task_2": ["task_1"],
    "task_3": ["task_1", "task_2"]
  }
}
```

## Integration Points

```text
coderabbit-request
        ↓ (outputs JSON)
coderabbit-triage
        ↓ (outputs task plan)
coderabbit-fix (dispatched per task)
```

Return structured task plan. Main agent will dispatch fixer subagents based on strategy and parallelization groups.
