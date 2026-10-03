---
name: cortivex-mesh
version: 1.0.0
description: Mesh coordination protocol for multi-agent file ownership and conflict resolution
category: coordination
tags: [mesh, coordination, agents, conflict-resolution, file-ownership]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [file-locking, conflict-detection, agent-coordination, ownership-tracking]
injection: always
---

# Cortivex Mesh Coordination Protocol

**CRITICAL: This skill is injected into EVERY spawned agent's system prompt. All instructions below are mandatory for any agent operating within a Cortivex pipeline.**

You are operating as one agent within a multi-agent Cortivex pipeline. Multiple agents may be working on the same repository simultaneously. To prevent conflicts, data corruption, and wasted work, you MUST follow the mesh coordination protocol described below.

## Prime Directive

**NEVER modify a file without first checking and claiming ownership through the mesh.**

Violating this rule can cause:
- Silent overwrites of another agent's work
- Merge conflicts that require manual resolution
- Pipeline failures that waste time and cost
- Corrupted file states that break the repository

## Protocol: Before Modifying Any File

Before you write to, edit, rename, move, or delete ANY file, you must execute this sequence:

### Step 1: Check File Ownership

Call `cortivex_mesh` with the `check` action to see if another agent has claimed the file:

```
cortivex_mesh({
  action: "check",
  files: ["src/auth/login.ts", "src/auth/session.ts"],
  agent_id: "<your-agent-id>"
})
```

**Response possibilities:**

```json
{
  "status": "available",
  "files": {
    "src/auth/login.ts": { "owner": null, "available": true },
    "src/auth/session.ts": { "owner": null, "available": true }
  }
}
```

or

```json
{
  "status": "conflict",
  "files": {
    "src/auth/login.ts": {
      "owner": "agent-code-reviewer-7f3a",
      "available": false,
      "claimed_at": "2025-01-15T10:23:45Z",
      "operation": "reviewing"
    },
    "src/auth/session.ts": { "owner": null, "available": true }
  }
}
```

### Step 2: Handle the Response

**If ALL files are available:** proceed to Step 3 (claim them).

**If ANY file is claimed by another agent:** follow the Conflict Resolution procedure below. DO NOT proceed to claim the available files yet -- handle the conflict first.

### Step 3: Claim Ownership

Claim the files you need to modify:

```
cortivex_mesh({
  action: "claim",
  files: ["src/auth/login.ts", "src/auth/session.ts"],
  agent_id: "<your-agent-id>",
  operation: "auto-fixing",
  ttl_seconds: 300
})
```

Parameters:
- `files` -- Array of file paths relative to repository root
- `agent_id` -- Your unique agent identifier (provided in your spawn config)
- `operation` -- Brief description of what you plan to do (for other agents to see)
- `ttl_seconds` -- How long you expect to hold the claim. The mesh will auto-release after this time. Set conservatively; you can extend if needed.

**Response:**

```json
{
  "status": "claimed",
  "files": {
    "src/auth/login.ts": { "owner": "<your-agent-id>", "expires_at": "2025-01-15T10:28:45Z" },
    "src/auth/session.ts": { "owner": "<your-agent-id>", "expires_at": "2025-01-15T10:28:45Z" }
  },
  "claim_id": "claim-8x9y2z"
}
```

**Important:** Save the `claim_id`. You need it to release the claim.

### Step 4: Do Your Work

Now you may safely modify the claimed files. Work efficiently -- other agents may be waiting.

### Step 5: Release Ownership

After you finish modifying the files, release them immediately:

```
cortivex_mesh({
  action: "release",
  claim_id: "claim-8x9y2z",
  agent_id: "<your-agent-id>",
  files: ["src/auth/login.ts", "src/auth/session.ts"]
})
```

**Response:**

```json
{
  "status": "released",
  "files": ["src/auth/login.ts", "src/auth/session.ts"],
  "held_duration_seconds": 47
}
```

**CRITICAL: Always release files when done, even if your operation failed.** Use a try/finally pattern:

```
1. Check ownership
2. Claim files
3. Try: do your work
4. Finally: release files (always, regardless of success or failure)
```

## Conflict Resolution

When a file you need is owned by another agent, follow this procedure:

### Option A: Work on Something Else

If you have other files to process that are not blocked:

1. Skip the conflicted file
2. Process other available files
3. Come back to check the conflicted file later
4. Record the skip in your output:

```json
{
  "skipped_files": [
    {
      "file": "src/auth/login.ts",
      "reason": "owned by agent-code-reviewer-7f3a",
      "will_retry": true
    }
  ]
}
```

### Option B: Wait and Retry

If the conflicted file is essential and you cannot proceed without it:

1. Wait for a short interval (5-10 seconds)
2. Re-check ownership
3. If still claimed, wait again (up to 3 retries)
4. If still claimed after retries, report the conflict

```
cortivex_mesh({
  action: "wait",
  files: ["src/auth/login.ts"],
  agent_id: "<your-agent-id>",
  timeout_seconds: 30,
  poll_interval_seconds: 5
})
```

**Response (success):**

```json
{
  "status": "available",
  "waited_seconds": 12,
  "files": {
    "src/auth/login.ts": { "owner": null, "available": true }
  }
}
```

**Response (timeout):**

```json
{
  "status": "timeout",
  "waited_seconds": 30,
  "files": {
    "src/auth/login.ts": {
      "owner": "agent-code-reviewer-7f3a",
      "available": false,
      "claimed_at": "2025-01-15T10:23:45Z"
    }
  }
}
```

### Option C: Report the Conflict

If you cannot proceed and waiting has not resolved the issue:

```
cortivex_mesh({
  action: "report_conflict",
  files: ["src/auth/login.ts"],
  agent_id: "<your-agent-id>",
  blocking_agent: "agent-code-reviewer-7f3a",
  urgency: "high",
  message: "AutoFixer cannot proceed: src/auth/login.ts needed for critical bug fix but held by CodeReviewer for 5+ minutes"
})
```

The orchestrator will receive this conflict report and may:
- Ask the blocking agent to release the file
- Forcibly release the stale claim
- Reorder pipeline execution
- Cancel one of the conflicting agents

## Extending Claims

If your operation is taking longer than expected, extend your claim before it expires:

```
cortivex_mesh({
  action: "extend",
  claim_id: "claim-8x9y2z",
  agent_id: "<your-agent-id>",
  additional_seconds: 120
})
```

**Response:**

```json
{
  "status": "extended",
  "new_expires_at": "2025-01-15T10:30:45Z"
}
```

If the claim has already expired and been taken by another agent:

```json
{
  "status": "claim_lost",
  "new_owner": "agent-auto-fixer-2b4d",
  "message": "Claim expired and was acquired by another agent"
}
```

In this case, you must re-check ownership and re-claim if available.

## Bulk Operations

When you need to modify many files (e.g., a migration or refactor), claim them in batches:

```
cortivex_mesh({
  action: "claim_batch",
  files: ["src/utils/a.ts", "src/utils/b.ts", "src/utils/c.ts", /* ... up to 50 files */],
  agent_id: "<your-agent-id>",
  operation: "typescript-migration",
  ttl_seconds: 600
})
```

**Response (partial success):**

```json
{
  "status": "partial",
  "claimed": ["src/utils/a.ts", "src/utils/c.ts"],
  "conflicts": {
    "src/utils/b.ts": {
      "owner": "agent-lint-fixer-9e1f",
      "operation": "fixing lint errors"
    }
  },
  "claim_id": "claim-batch-4k5m"
}
```

Process the claimed files first, then retry the conflicted ones.

## Directory-Level Claims

For operations that affect an entire directory (like scaffolding or large-scale refactors), claim at the directory level:

```
cortivex_mesh({
  action: "claim_directory",
  directory: "src/auth/",
  agent_id: "<your-agent-id>",
  operation: "auth-module-refactor",
  ttl_seconds: 900,
  recursive: true
})
```

This claims all files within the directory. Other agents will see the directory as owned and cannot claim individual files within it.

## Read-Only Access

If you only need to READ a file (not modify it), you do not need to claim ownership. Multiple agents can read the same file simultaneously. However, be aware that the file contents may change while you are reading if another agent has claimed it for modification.

For consistent reads, use the `snapshot` action:

```
cortivex_mesh({
  action: "snapshot",
  files: ["src/auth/login.ts"],
  agent_id: "<your-agent-id>"
})
```

This returns a versioned snapshot that will not change even if another agent modifies the file.

## Status Query

To see the current state of the mesh (all claims across all agents):

```
cortivex_mesh({
  action: "status",
  agent_id: "<your-agent-id>"
})
```

**Response:**

```json
{
  "active_claims": 7,
  "agents_active": 3,
  "claims": [
    {
      "claim_id": "claim-8x9y2z",
      "agent_id": "agent-code-reviewer-7f3a",
      "files": ["src/auth/login.ts"],
      "operation": "reviewing",
      "claimed_at": "2025-01-15T10:23:45Z",
      "expires_at": "2025-01-15T10:28:45Z"
    },
    {
      "claim_id": "claim-3j4k5l",
      "agent_id": "agent-test-runner-1c2d",
      "files": ["tests/auth.test.ts", "tests/session.test.ts"],
      "operation": "running tests",
      "claimed_at": "2025-01-15T10:24:10Z",
      "expires_at": "2025-01-15T10:29:10Z"
    }
  ]
}
```

## Error Handling

### Claim Denied

If a claim is denied (race condition -- another agent claimed between your check and claim):

```json
{
  "status": "denied",
  "files": {
    "src/auth/login.ts": {
      "owner": "agent-auto-fixer-2b4d",
      "claimed_at": "2025-01-15T10:23:46Z"
    }
  }
}
```

Action: Go to Conflict Resolution procedure.

### Mesh Unavailable

If the mesh service is unreachable:

```json
{
  "status": "error",
  "error": "mesh_unavailable",
  "message": "Could not connect to mesh coordinator"
}
```

Action: **STOP all file modifications.** Do not proceed without mesh coordination. Report the error to the orchestrator. You may continue read-only operations.

### Stale Claim

If you try to release a claim that has already expired:

```json
{
  "status": "warning",
  "message": "Claim already expired. Files were auto-released at 2025-01-15T10:28:45Z"
}
```

Action: This is informational. No action needed, but consider increasing your TTL for future claims.

## Summary of Mandatory Rules

1. **ALWAYS check ownership** before modifying any file
2. **ALWAYS claim files** before writing to them
3. **NEVER modify a file** owned by another agent
4. **ALWAYS release files** when done, even on failure
5. **REPORT conflicts** you cannot resolve yourself
6. **EXTEND claims** if your operation runs long -- do not let them expire silently
7. **STOP all writes** if the mesh is unavailable
8. **USE batching** for operations affecting many files
9. **READ without claiming** is allowed, but be aware of concurrent modifications
10. **INCLUDE skipped files** in your output so the orchestrator knows what was not processed

## Reasoning Protocol

Before any file operation, reason through this checklist:

1. **Do I actually need to modify this file?** If you only need to read the file, skip the claim protocol entirely. Read-only access is always free.
2. **Is there a less invasive approach?** Could you achieve the same result by modifying fewer files? Smaller claim sets reduce conflict probability.
3. **What is the minimum TTL I need?** Estimate your actual operation time and add a 50% buffer. Do not use the maximum TTL by default.
4. **Are any of my target files likely contested?** If you are modifying files in a shared module (auth, utils, config), expect conflicts and plan for them.
5. **What is my fallback if I cannot claim?** Decide before attempting the claim whether you will wait, skip, or report.

## Anti-Patterns

**DO NOT** make these mistakes:

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Modifying files without checking mesh | Silent overwrites, lost work, pipeline failure | Always check -> claim -> work -> release |
| Claiming files and forgetting to release | Blocks other agents indefinitely until TTL expires | Use try/finally pattern; release on success AND failure |
| Setting TTL to maximum "just in case" | Blocks other agents for longer than necessary | Estimate actual duration + 50% buffer |
| Claiming all files in a directory when you only need 2 | Unnecessary blocking of other agents | Claim only the specific files you will modify |
| Ignoring "mesh_unavailable" errors | Concurrent writes corrupt the repository | Stop all modifications immediately; continue read-only only |
| Retrying claims in a tight loop | Wastes cycles, may look like a DoS to the mesh | Use `cortivex_mesh({ action: "wait" })` with backoff |
| Not including skipped files in output | Orchestrator does not know what was missed | Always report skipped files with reasons |

**WRONG:**
```
# Claim everything, work on one file, release everything
cortivex_mesh({ action: "claim", files: [all 50 files in src/], ttl_seconds: 900 })
// only modify src/auth/login.ts
cortivex_mesh({ action: "release", ... })
```

**RIGHT:**
```
# Claim only what you need
cortivex_mesh({ action: "claim", files: ["src/auth/login.ts"], ttl_seconds: 120 })
// modify src/auth/login.ts
cortivex_mesh({ action: "release", ... })
```

## Grounding Rules

When you encounter uncertainty in the mesh protocol:

- **Claim denied but you urgently need the file:** Do NOT bypass the mesh. Use Option B (wait and retry) or Option C (report the conflict). The mesh exists to prevent data corruption.
- **Unsure if another agent is still active:** Check the claim's `claimed_at` timestamp. If it is older than the TTL, the claim will auto-expire. Wait for expiration rather than assuming the agent is dead.
- **File was modified externally (outside mesh):** Report this to the orchestrator. Do not assume external changes are safe. The mesh only tracks agent-initiated modifications.
- **Your operation failed mid-way:** Release all claimed files immediately, even if your work is incomplete. Holding claims after failure blocks other agents for no benefit.
- **Mesh returns unexpected errors:** Log the error, release any held claims, and report to the orchestrator. Do not retry mesh operations that return non-transient errors.

## Advanced Capabilities

This section covers advanced mesh features for distributed file locking, topology optimization, partition tolerance, TTL-based resource management, and health monitoring.

### Distributed File Locking Strategies

The mesh supports multiple locking strategies beyond simple exclusive claims. Use `cortivex_mesh_lock` for fine-grained control over concurrent access patterns, including shared read locks, exclusive write locks, and intent locks for staged operations.

```json
{
  "tool": "cortivex_mesh_lock",
  "request": {
    "action": "acquire",
    "lock_type": "intent_exclusive",
    "files": ["src/core/engine.ts", "src/core/pipeline.ts"],
    "agent_id": "agent-refactor-4a2c",
    "strategy": "optimistic",
    "retry_policy": {
      "max_retries": 3,
      "backoff_ms": 500,
      "backoff_multiplier": 2.0
    },
    "queue_position": true
  }
}
```

```json
{
  "tool": "cortivex_mesh_lock",
  "response": {
    "status": "acquired",
    "lock_id": "lock-xe93mz",
    "lock_type": "intent_exclusive",
    "files": ["src/core/engine.ts", "src/core/pipeline.ts"],
    "queue_ahead": 0,
    "escalation_available": true,
    "granted_at": "2025-06-10T14:05:22Z",
    "expires_at": "2025-06-10T14:10:22Z"
  }
}
```

When an intent lock must be promoted to a full exclusive lock, call `cortivex_mesh_lock` with `action: "escalate"` and the existing `lock_id`. The mesh will block until all concurrent shared readers have released.

### Mesh Topology Optimization

Mesh topology defines how agents discover and communicate with each other. The default `full_mesh` topology connects every agent to every other agent, but this does not scale. Use topology configuration to define hierarchical or ring-based layouts for large pipelines.

```yaml
# mesh-topology.yaml
mesh:
  topology: hierarchical
  replication_factor: 2
  sync_interval_ms: 1000

  zones:
    - name: core-zone
      role: coordinator
      max_agents: 3
      agents:
        - pattern: "agent-orchestrator-*"
        - pattern: "agent-planner-*"

    - name: worker-zone
      role: worker
      max_agents: 20
      parent: core-zone
      agents:
        - pattern: "agent-fixer-*"
        - pattern: "agent-reviewer-*"
        - pattern: "agent-test-*"

    - name: observer-zone
      role: readonly
      max_agents: 10
      parent: core-zone
      agents:
        - pattern: "agent-monitor-*"

  routing:
    claim_propagation: "upward"
    conflict_resolution: "coordinator"
    heartbeat_interval_ms: 5000
    stale_threshold_ms: 15000
```

Agents in worker zones route claim requests through their parent coordinator zone, reducing cross-zone chatter. Observer zones receive replicated state but cannot issue claims.

### Partition Tolerance & Recovery

When network issues split the mesh into isolated partitions, agents must follow a partition handling policy to avoid conflicting writes across segments. The policy schema defines behavior during and after partition events.

```json
{
  "$schema": "https://cortivex.dev/schemas/partition-policy/v1",
  "type": "object",
  "properties": {
    "detection": {
      "type": "object",
      "properties": {
        "heartbeat_timeout_ms": { "type": "integer", "default": 10000 },
        "min_quorum_percentage": { "type": "integer", "default": 51 },
        "consecutive_failures": { "type": "integer", "default": 3 }
      }
    },
    "during_partition": {
      "type": "object",
      "properties": {
        "write_policy": {
          "type": "string",
          "enum": ["freeze", "local_only", "optimistic_continue"],
          "default": "freeze"
        },
        "read_policy": {
          "type": "string",
          "enum": ["allow_stale", "reject", "cached_only"],
          "default": "cached_only"
        },
        "claim_behavior": {
          "type": "string",
          "enum": ["deny_new", "local_scope", "queue_for_reconciliation"],
          "default": "deny_new"
        }
      }
    },
    "recovery": {
      "type": "object",
      "properties": {
        "reconciliation_strategy": {
          "type": "string",
          "enum": ["last_writer_wins", "coordinator_decides", "merge_and_review"],
          "default": "coordinator_decides"
        },
        "conflict_log_retention_hours": { "type": "integer", "default": 48 },
        "auto_release_orphaned_claims": { "type": "boolean", "default": true }
      }
    }
  }
}
```

When a partition is detected, agents in the minority segment must freeze writes immediately. After reconnection, the coordinator runs reconciliation using the configured strategy before any agent resumes normal operations.

### TTL-Based Resource Management

Beyond per-claim TTL values, the mesh supports global TTL policies that govern resource lifecycle, automatic cleanup, and claim renewal thresholds. Use `cortivex_mesh_ttl_configure` to define these policies.

```json
{
  "tool": "cortivex_mesh_ttl_configure",
  "request": {
    "action": "set_policy",
    "policy": {
      "default_ttl_seconds": 300,
      "max_ttl_seconds": 1800,
      "min_ttl_seconds": 30,
      "auto_renew": {
        "enabled": true,
        "renew_at_percentage": 75,
        "max_renewals": 5
      },
      "expiration_behavior": {
        "notify_agent_before_seconds": 30,
        "grace_period_seconds": 10,
        "on_expire": "release_and_notify"
      },
      "resource_classes": {
        "config_files": { "default_ttl_seconds": 120, "max_renewals": 2 },
        "source_files": { "default_ttl_seconds": 300, "max_renewals": 5 },
        "test_files": { "default_ttl_seconds": 600, "max_renewals": 10 }
      }
    }
  }
}
```

```json
{
  "tool": "cortivex_mesh_ttl_configure",
  "response": {
    "status": "policy_applied",
    "effective_at": "2025-06-10T14:12:00Z",
    "active_claims_affected": 4,
    "claims_adjusted": [
      { "claim_id": "claim-8x9y2z", "new_ttl_seconds": 300, "class": "source_files" },
      { "claim_id": "claim-3j4k5l", "new_ttl_seconds": 600, "class": "test_files" }
    ]
  }
}
```

Resource classes allow different file categories to have tailored TTL behavior. Config files receive shorter TTLs to minimize blocking on shared configuration, while test files receive longer TTLs to accommodate extended test suite execution.

### Mesh Health Monitoring & Alerts

The mesh exposes a health monitoring endpoint that agents and external systems can query for real-time status. Configure health checks and alert thresholds using the following schema.

```json
{
  "$schema": "https://cortivex.dev/schemas/mesh-health/v1",
  "type": "object",
  "properties": {
    "health_check": {
      "type": "object",
      "properties": {
        "interval_seconds": { "type": "integer", "default": 30 },
        "timeout_seconds": { "type": "integer", "default": 5 },
        "checks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string", "enum": ["latency", "claim_throughput", "agent_count", "partition_status"] },
              "warning_threshold": { "type": "number" },
              "critical_threshold": { "type": "number" }
            }
          }
        }
      }
    },
    "alerts": {
      "type": "object",
      "properties": {
        "on_critical": {
          "type": "string",
          "enum": ["notify_orchestrator", "freeze_mesh", "log_only"],
          "default": "notify_orchestrator"
        },
        "on_warning": {
          "type": "string",
          "enum": ["notify_orchestrator", "log_only"],
          "default": "log_only"
        },
        "stale_claim_threshold_seconds": { "type": "integer", "default": 900 },
        "max_active_claims_per_agent": { "type": "integer", "default": 15 }
      }
    }
  }
}
```

Health checks run at the configured interval and evaluate each metric against its thresholds. When a critical threshold is breached (for example, mesh latency exceeds the limit or active agent count drops below quorum), the mesh triggers the configured alert action. Agents should query mesh health before starting large batch operations to avoid working against a degraded mesh.

```typescript
// Example: programmatic health check before a batch operation
async function safeBatchClaim(files: string[], agentId: string): Promise<boolean> {
  const health = await cortivexMesh({ action: "health", agent_id: agentId });

  if (health.status === "critical") {
    console.error(`Mesh is in critical state: ${health.reason}`);
    return false;
  }

  if (health.degraded_zones && health.degraded_zones.length > 0) {
    console.warn(`Degraded zones detected: ${health.degraded_zones.join(", ")}`);
  }

  const claim = await cortivexMesh({
    action: "claim_batch",
    files,
    agent_id: agentId,
    operation: "batch-update",
    ttl_seconds: 300,
  });

  return claim.status === "claimed" || claim.status === "partial";
}
```

## Security Hardening (OWASP AST10 Aligned)

This section defines security controls for the mesh coordination layer, mapped to the OWASP Agentic Security Threats (AST) taxonomy. These controls protect against skill file tampering, file integrity violations, and insufficient audit trails in multi-agent mesh operations.

### AST01: Skill File Tamper Detection

Because this skill uses `injection: always`, its contents are loaded into every spawned agent's system prompt. A tampered skill file could inject malicious instructions into all agents simultaneously. This makes hash verification on load a critical control against AST01 (Prompt Injection).

```yaml
# mesh-integrity.yaml — AST01 Tamper Detection
skill_integrity:
  ast01_tamper_detection:
    enabled: true
    target_skill: "cortivex-mesh"
    injection_mode: "always"  # this skill is auto-injected — highest risk

    hash_verification:
      algorithm: "sha256"
      expected_hash_source: ".cortivex/manifests/skill-hashes.json"
      verify_on: ["agent_spawn", "skill_reload", "pipeline_start"]
      fail_action: "abort_pipeline"  # do NOT inject a tampered skill

    signature_verification:
      enabled: true
      public_key_path: "/etc/cortivex/keys/skill-signing.pub"
      signature_path: ".agents/skills/cortivex-mesh/SKILL.md.sig"
      algorithm: "ed25519"

    runtime_monitoring:
      detect_in_memory_modification: true
      recheck_interval_seconds: 300
      on_drift_detected: "kill_affected_agents"
```

The skill hash manifest records the expected hash for each skill file:

```json
{
  "$schema": "https://cortivex.dev/schemas/skill-hash-manifest/v1.json",
  "type": "object",
  "properties": {
    "skills": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["skill_name", "file_path", "sha256", "signed_at"],
        "properties": {
          "skill_name": { "type": "string" },
          "file_path": { "type": "string" },
          "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
          "signed_at": { "type": "string", "format": "date-time" },
          "signed_by": { "type": "string" },
          "injection_mode": {
            "type": "string",
            "enum": ["always", "on_demand", "never"]
          }
        }
      }
    },
    "manifest_hash": {
      "type": "string",
      "description": "SHA-256 of the entire skills array for manifest self-verification"
    }
  }
}
```

Verify integrity before agent spawn using MCP:

```json
{
  "tool": "cortivex_mesh",
  "request": {
    "action": "verify_skill_integrity",
    "skill_name": "cortivex-mesh",
    "manifest_path": ".cortivex/manifests/skill-hashes.json",
    "ast_risk_id": "AST01",
    "abort_on_mismatch": true
  }
}
```

### AST06: File Integrity Validation Before Claim Release

When an agent releases a file claim, the mesh MUST validate that the file was modified in an expected manner. This prevents AST06 (Insecure Input/Output Handling) scenarios where a compromised agent writes malicious content and then releases the claim, allowing other agents to consume corrupted files.

```yaml
# claim-release-validation.yaml — AST06 File Integrity on Release
claim_release_security:
  ast06_file_validation:
    enabled: true
    validate_on_release: true

    checks:
      - name: size_delta_check
        description: "Reject releases where file size changed by more than 500%"
        max_growth_percent: 500
        max_shrink_percent: 95
        on_violation: "hold_claim_and_alert"

      - name: content_type_check
        description: "Ensure file still matches expected content type"
        enforce_original_mime: true
        on_violation: "reject_release"

      - name: binary_injection_check
        description: "Detect binary content injected into text files"
        scan_for_binary: true
        on_violation: "quarantine_and_alert"

      - name: secret_scan
        description: "Block release if secrets were written into the file"
        patterns:
          - "(?i)(api[_-]?key|secret|password|token)\\s*[:=]\\s*['\"][^'\"]{8,}"
          - "-----BEGIN (RSA |EC )?PRIVATE KEY-----"
          - "ghp_[a-zA-Z0-9]{36}"
          - "sk-[a-zA-Z0-9]{48}"
        on_violation: "reject_release_and_audit"
```

Enforce validation at release time:

```json
{
  "tool": "cortivex_mesh",
  "request": {
    "action": "release",
    "claim_id": "claim-8x9y2z",
    "agent_id": "agent-auto-fixer-2b4d",
    "files": ["src/auth/login.ts"],
    "ast06_validate": true,
    "integrity_checks": ["size_delta", "content_type", "binary_injection", "secret_scan"]
  }
}
```

### AST09: Mesh Operation Audit Trail

Every mesh operation (check, claim, release, conflict, extend, wait) MUST produce an immutable audit record. This addresses AST09 (Insufficient Logging and Monitoring) by creating a complete chain-of-custody for file ownership throughout a pipeline run.

```json
{
  "$schema": "https://cortivex.dev/schemas/mesh-audit-entry/v1.json",
  "type": "object",
  "required": ["audit_id", "timestamp", "ast_risk_id", "operation", "agent_id"],
  "properties": {
    "audit_id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "ast_risk_id": { "type": "string", "enum": ["AST09"] },
    "operation": {
      "type": "string",
      "enum": [
        "check", "claim", "release", "extend", "wait",
        "claim_denied", "claim_expired", "conflict_reported",
        "directory_claim", "batch_claim", "force_release",
        "integrity_violation", "tamper_detected"
      ]
    },
    "agent_id": { "type": "string" },
    "files": { "type": "array", "items": { "type": "string" } },
    "claim_id": { "type": "string" },
    "outcome": {
      "type": "string",
      "enum": ["success", "denied", "timeout", "error", "violation"]
    },
    "context": {
      "type": "object",
      "properties": {
        "run_id": { "type": "string" },
        "blocking_agent": { "type": "string" },
        "ttl_seconds": { "type": "integer" },
        "held_duration_seconds": { "type": "number" },
        "integrity_check_results": { "type": "object" }
      }
    },
    "chain_hash": {
      "type": "string",
      "description": "SHA-256 linking this entry to the previous, forming a tamper-evident chain"
    }
  }
}
```

Configure audit logging for the mesh:

```yaml
mesh:
  audit:
    ast09_compliance: true
    log_destination: ".cortivex/audit/mesh-operations.jsonl"
    hash_chain: true
    include_file_hashes: true  # record SHA-256 of files at claim and release
    retention_days: 90
    export_format: "jsonl"
    real_time_stream: true     # emit events as they occur for external SIEM
```

### Partition-Mode Security Defaults

The default partition write policy MUST be `freeze`, not `optimistic_continue`. Optimistic continue during a network partition allows conflicting writes across isolated segments, which can lead to data corruption that reconciliation cannot fully resolve. This is a security-critical default.

```yaml
# partition-security-defaults.yaml
partition_security:
  mandatory_defaults:
    write_policy: "freeze"            # REQUIRED: never optimistic_continue
    read_policy: "cached_only"        # stale reads are acceptable; blind writes are not
    claim_behavior: "deny_new"        # no new claims during partition

  prohibited_configurations:
    - write_policy: "optimistic_continue"
      reason: "Risk of conflicting writes across partitions leading to unrecoverable corruption"
      ast_risk_ids: ["AST06", "AST09"]

  enforcement:
    reject_optimistic_continue: true  # coordinator refuses to start with this config
    log_partition_events: true        # AST09: all partition events are audited
    require_quorum_for_writes: true   # writes require majority quorum confirmation
    min_quorum_percentage: 51
```

Validate partition configuration at pipeline start:

```json
{
  "tool": "cortivex_mesh",
  "request": {
    "action": "validate_partition_policy",
    "policy_path": "partition-security-defaults.yaml",
    "reject_optimistic_continue": true,
    "ast_risk_ids": ["AST06", "AST09"]
  }
}
```

### Stale Claim Timeout Enforcement

Stale claims that exceed their TTL without renewal MUST be forcibly released to prevent resource exhaustion. An agent that holds claims indefinitely (whether due to a bug, crash, or malicious behavior) blocks all other agents from accessing those files, effectively creating a denial-of-service condition.

```yaml
stale_claim_enforcement:
  enabled: true
  max_ttl_seconds: 1800              # absolute maximum claim duration
  max_renewals: 5                     # cap on how many times a claim can be extended
  grace_period_seconds: 10            # brief window after TTL before force-release
  force_release_on_agent_death: true  # immediately release if owning agent is dead

  escalation:
    warn_at_percent: 75               # alert when 75% of TTL consumed
    alert_at_percent: 90              # escalate when 90% consumed
    force_release_at_percent: 100     # hard release at 100%

  audit:
    log_all_expirations: true         # AST09: every expiration is logged
    log_force_releases: true
    include_held_duration: true
    include_agent_state_at_expiry: true
```

Monitor stale claims via MCP:

```json
{
  "tool": "cortivex_mesh",
  "request": {
    "action": "audit_stale_claims",
    "threshold_seconds": 900,
    "include_agent_health": true,
    "auto_release_dead_agents": true,
    "ast_risk_id": "AST09"
  }
}
```

Response:

```json
{
  "stale_claims": [
    {
      "claim_id": "claim-old-7k2m",
      "agent_id": "agent-fixer-9e1f",
      "agent_status": "dead",
      "files": ["src/utils/helpers.ts"],
      "claimed_at": "2026-03-24T13:45:00Z",
      "ttl_seconds": 300,
      "expired_at": "2026-03-24T13:50:00Z",
      "action_taken": "force_released",
      "audit_entry_id": "evt-3a2b1c0d"
    }
  ],
  "total_released": 1,
  "ast_risk_id": "AST09"
}
