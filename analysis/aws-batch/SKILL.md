---
name: aws-batch
description: |
  Use when working with Aws Batch — aWS Batch compute environment management,
  job queue analysis, scheduling policy review, and array job monitoring. Covers
  compute resource utilization, job status tracking, failure investigation,
  Fargate vs EC2 comparison, and queue priority analysis.
connection_type: aws
preload: false
---

# AWS Batch Skill

Analyze AWS Batch compute environments and jobs with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-batch/` → Batch-specific analysis (compute environments, job queues, jobs)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for ce in $compute_envs; do
  describe_compute_env "$ce" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List compute environments
list_compute_environments() {
  aws batch describe-compute-environments \
    --output text \
    --query 'computeEnvironments[].[computeEnvironmentName,state,status,type,computeResources.type,computeResources.minvCpus,computeResources.maxvCpus,computeResources.desiredvCpus]'
}

# List job queues
list_job_queues() {
  aws batch describe-job-queues \
    --output text \
    --query 'jobQueues[].[jobQueueName,state,status,priority,computeEnvironmentOrder[].computeEnvironment]'
}

# List jobs by status
list_jobs() {
  local queue=$1 status=$2
  aws batch list-jobs --job-queue "$queue" --job-status "$status" \
    --output text \
    --query 'jobSummaryList[].[jobId,jobName,status,createdAt,startedAt,stoppedAt,statusReason]' | head -20
}

# Describe jobs (batch)
describe_jobs() {
  local job_ids="$@"
  aws batch describe-jobs --jobs $job_ids \
    --output text \
    --query 'jobs[].[jobId,jobName,status,statusReason,container.exitCode,container.reason,startedAt,stoppedAt]'
}

# List job definitions
list_job_definitions() {
  aws batch describe-job-definitions --status ACTIVE \
    --output text \
    --query 'jobDefinitions[].[jobDefinitionName,revision,type,status,containerProperties.vcpus,containerProperties.memory]' | head -20
}

# List scheduling policies
list_scheduling_policies() {
  aws batch list-scheduling-policies \
    --output text \
    --query 'schedulingPolicies[].[arn,name]' 2>/dev/null
}
```

## Common Operations

### 1. Compute Environment Overview

```bash
#!/bin/bash
export AWS_PAGER=""
aws batch describe-compute-environments \
  --output text \
  --query 'computeEnvironments[].[computeEnvironmentName,state,status,type,computeResources.type,computeResources.minvCpus,computeResources.maxvCpus,computeResources.desiredvCpus]'
```

### 2. Job Queue Status with Active Jobs

```bash
#!/bin/bash
export AWS_PAGER=""
QUEUES=$(aws batch describe-job-queues --output text --query 'jobQueues[].jobQueueName')
for queue in $QUEUES; do
  {
    info=$(aws batch describe-job-queues --job-queues "$queue" \
      --output text --query 'jobQueues[].[jobQueueName,state,priority]')
    running=$(aws batch list-jobs --job-queue "$queue" --job-status RUNNING \
      --output text --query 'length(jobSummaryList)')
    pending=$(aws batch list-jobs --job-queue "$queue" --job-status PENDING \
      --output text --query 'length(jobSummaryList)')
    submitted=$(aws batch list-jobs --job-queue "$queue" --job-status SUBMITTED \
      --output text --query 'length(jobSummaryList)')
    printf "%s\tRunning:%s\tPending:%s\tSubmitted:%s\n" "$info" "$running" "$pending" "$submitted"
  } &
done
wait
```

### 3. Failed Job Investigation

```bash
#!/bin/bash
export AWS_PAGER=""
QUEUES=$(aws batch describe-job-queues --output text --query 'jobQueues[].jobQueueName')
for queue in $QUEUES; do
  FAILED=$(aws batch list-jobs --job-queue "$queue" --job-status FAILED \
    --output text --query 'jobSummaryList[:5].jobId')
  [ -z "$FAILED" ] && continue
  aws batch describe-jobs --jobs $FAILED \
    --output text \
    --query 'jobs[].[jobName,status,statusReason,container.exitCode,container.reason,stoppedAt]' &
done
wait
```

### 4. Array Job Progress

```bash
#!/bin/bash
export AWS_PAGER=""
QUEUE=$1
ARRAY_JOBS=$(aws batch list-jobs --job-queue "$QUEUE" --job-status RUNNING \
  --output text --query 'jobSummaryList[?arrayProperties].jobId')
for job_id in $ARRAY_JOBS; do
  aws batch describe-jobs --jobs "$job_id" \
    --output text \
    --query 'jobs[].[jobName,arrayProperties.size,arrayProperties.statusSummary]' &
done
wait
```

### 5. Job Definition Audit

```bash
#!/bin/bash
export AWS_PAGER=""
aws batch describe-job-definitions --status ACTIVE \
  --output text \
  --query 'jobDefinitions[].[jobDefinitionName,revision,type,platformCapabilities[0],containerProperties.image,containerProperties.vcpus,containerProperties.memory,retryStrategy.attempts]' | head -30
```

## Anti-Hallucination Rules

1. **Compute environment types** - MANAGED or UNMANAGED. Managed CEs auto-scale. Unmanaged CEs require manual instance management.
2. **Compute resource types** - EC2, SPOT, FARGATE, or FARGATE_SPOT. Each has different pricing and availability characteristics.
3. **Job status flow** - SUBMITTED -> PENDING -> RUNNABLE -> STARTING -> RUNNING -> SUCCEEDED/FAILED. Jobs do not skip states.
4. **vCPU units** - `minvCpus`, `maxvCpus`, `desiredvCpus` are in vCPU units, not instance counts. The scheduler maps vCPUs to instance types.
5. **Array job indexing** - Array job indices are 0-based. An array of size 100 has indices 0-99. Each index runs as a separate container.

## Output Format

Present results as a structured report:
```
Aws Batch Report
════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **PENDING vs RUNNABLE**: PENDING means the job is waiting for dependencies. RUNNABLE means it is ready but waiting for compute capacity. Extended RUNNABLE time indicates insufficient capacity.
- **Fargate limitations**: Fargate Batch jobs have vCPU/memory limits (max 16 vCPU, 120 GB). EC2 CEs support larger instances.
- **Spot interruptions**: SPOT compute environments may lose instances. Check `statusReason` for "Host EC2 (instance i-xxx) terminated" messages.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Job definition revisions**: Each update creates a new revision. Jobs reference a specific revision. Use `:N` suffix for specific revision or omit for latest active.
