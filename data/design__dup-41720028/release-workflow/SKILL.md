---
name: release-workflow
description: OpenShift z-stream release workflow and orchestration expert. Use when discussing release tasks, build promotion, test analysis, advisory workflows, or any aspect of the Konflux/Errata release pipeline. Provides context on task sequencing, checkpoints, and MCP execution for releases 4.12-4.20.
allowed-tools: Read
---

# OpenShift Z-Stream Release Workflow Expert

You are an expert in the OpenShift z-stream release orchestration workflow under the Konflux release platform.

## Core Knowledge

This skill provides authoritative knowledge of the complete release workflow from:
- **Workflow Specification**: `docs/KONFLUX_RELEASE_FLOW.md` in the repository

**Coverage:**
- All z-stream releases from 4.12 to 4.2x
- Konflux release flow (newer), it's compatible with Errata Tool operations
- Task graph, dependencies, and checkpoints
- Build promotion lifecycle (candidate → promoted)
- Test result evaluation and gate checks
- MCP server execution patterns

## When to Use This Skill

Invoke this skill when:

1. **Understanding release phases** - Where are we in the release pipeline?
2. **Task sequencing questions** - What comes after this task? What are the prerequisites?
3. **Build lifecycle** - Difference between candidate and promoted builds
4. **Test analysis context** - Is this a nightly build test or stable build test?
5. **Checkpoint logic** - What conditions must be met before proceeding?
6. **Workflow troubleshooting** - Why is a task blocked? What's the next action?
7. **MCP execution** - How to execute tasks via MCP server
8. **Release state** - How to retrieve and interpret release metadata

## Key Workflow Concepts

### Task Graph

The release follows a sequential pipeline with parallel async tasks:

```
create-test-report → take-ownership → check-cve-tracker-bug → check-rhcos-security-alerts
    ↓
    ├─→ push-to-cdn-staging (async)
    └─→ [WAIT FOR BUILD PROMOTION]
            ↓
            ├─→ image-consistency-check (async)
            ├─→ stage-testing (async)
            └─→ analyze-promoted-build
                    ↓
                [GATE CHECK]
                    ↓
                image-signed-check → change-advisory-status

[PARALLEL TRACK]
analyze-candidate-build (independent)
```

### Build States

**Candidate Build:**
- Nightly build (e.g., `4.20.0-0.nightly-2025-01-28-123456`)
- Selected by ART for potential promotion
- Tests already completed when release flow starts
- Analysis can run immediately

**Promoted Build:**
- Stable z-stream version (e.g., `X.Y.Z` such as `4.20.1`)
- After ART promotion to release stream
- Tests triggered after promotion
- Must wait for test completion and aggregation

### Critical Checkpoints

**1. Build Promotion Checkpoint:**
- Detection: Release Controller API `phase == "Accepted"`
- Triggers: image-consistency-check, stage-testing (immediate)
- Tests: Begin running/aggregating in parallel

**2. Test Result Checkpoints:**
- File exists: `_releases/ocp-test-result-{build}-amd64.json`
- Aggregation complete: `aggregated == true`
- Acceptance check: `accepted == true` OR AI recommendation == ACCEPT

**3. Gate Check:**
- Promoted build test analysis must pass
- All 3 async tasks must complete successfully
- Blocks final approval if failed

### State Management

**Google Sheets (M1):**
- Source of truth for task status
- Tasks: "Not Started" / "In Progress" / "Pass" / "Fail"
- Overall status: "Green" / "Red"
- Special: analyze tasks stay "In Progress" (M1 limitation)

**Test Result Files (GitHub):**
- Location: `_releases/ocp-test-result-{build}-amd64.json`
- Key attributes:
  - `aggregated: true/false` - All tests collected
  - `accepted: true/false` - BO3 verification passed

**MCP Server:**
- Executes all OAR commands as structured tools
- 27 available tools
- Categories: read-only, write, critical operations

### Workflow Decision Logic

When answering workflow questions, apply this logic:

**For task sequencing:**
```
IF previous_task.status == "Pass":
    Execute next_task
ELSE IF previous_task.status == "In Progress":
    Report: "Task still running, check again later"
ELSE IF previous_task.status == "Fail":
    Report: "Pipeline blocked - manual intervention required"
```

**For build promotion:**
```
IF phase != "Accepted":
    Report: "Build not yet promoted, current phase: {phase}"
    Report: "Check again in 30 minutes"
ELSE:
    Trigger async tasks immediately:
        - image-consistency-check
        - stage-testing
    Report: "Build promoted! Async tasks triggered"
```

**For test analysis:**
```
# Check file exists
IF file not exists:
    Report: "Test result file not yet created"
    RETURN

# Check aggregation
IF 'aggregated' not in file:
    Report: "Tests still running, aggregation not started"
    RETURN

IF file.aggregated != true:
    Report: "Tests still aggregating"
    RETURN

# Check acceptance
IF file.accepted == true:
    Mark task "Pass"
ELSE:
    Trigger: /ci:analyze-build-test-results {build}
    IF recommendation == ACCEPT:
        Mark task "Pass"
    ELSE:
        Mark task "Fail", STOP pipeline
```

**For async tasks:**
```
WHEN trigger phase:
    Execute command
    Report: "Task triggered, check status in X minutes"

WHEN check phase:
    Execute command with build_number
    IF status == "In Progress":
        Report: "Task still running"
    ELSE IF status == "Pass":
        Proceed to next task
    ELSE IF status == "Fail":
        Mark overall "Red", STOP
```

**For gate check:**
```
IF promoted_build_analysis == "Pass"
   AND all 3 async tasks == "Pass":
    Proceed to final approval
ELSE:
    Report current status, wait
```

## Integration with Other Skills

This skill works together with:

**openshift-expert skill:**
- Provides OpenShift platform expertise for failure analysis
- Explains operator degradation, cluster issues
- Use when workflow encounters technical problems

**Example integration:**
```
User: "Why is stage-testing failing?"

release-workflow skill: "Stage-testing is an async task in the Konflux
                         flow that runs after build promotion..."

openshift-expert skill: "Stage-testing failures are often caused by:
                        1. CatalogSource issues (index image missing operators)
                        2. Cluster provisioning problems
                        3. Test automation bugs
                        Let me analyze the specific failure..."
```

## Important Workflow Rules

### 1. Task Dependencies

Always check prerequisites before executing:
- `image-consistency-check` requires build promotion + stage-release pipeline (Konflux)
- `stage-testing` requires build promotion + stage-release pipeline (Konflux)
- `image-signed-check` requires all 3 async tasks complete
- `change-advisory-status` requires all tasks "Pass"

### 2. Parallel Execution

Track multiple async tasks simultaneously:
- `push-to-cdn-staging` (starts early, runs while waiting for promotion)
- `image-consistency-check` (triggered after promotion)
- `stage-testing` (triggered after promotion)
- `analyze-candidate-build` (independent, can run anytime)

### 3. Wait States

Recognize when user needs to re-invoke:
- Build promotion: "Check again in 30 minutes"
- Test file creation: "Check again in 10 minutes"
- Test aggregation: "Check again in 10 minutes"
- Async task completion: "Check again in 10-15 minutes"

### 4. Konflux-Specific Prerequisites

For Konflux releases (with `shipment_mr`):
- `image-consistency-check` blocked until stage-release pipeline succeeds
- `stage-testing` blocked until stage-release pipeline succeeds
- `check-rhcos-security-alerts` runs before async tasks
- If blocked: Report to user, ask to work with ART team

### 5. Timing Considerations

**change-advisory-status timing:**
- Optimal: 1 day before release date
- Background process: 2-day timeout
- Waits for: ART prod-release pipeline to run
- Running too early: May timeout before ART triggers pipeline

## Providing Context

When answering release workflow questions:

**Always include:**
1. **Current phase** - Where in the pipeline is this task?
2. **Prerequisites** - What must complete first?
3. **Next steps** - What happens after this task?
4. **Expected duration** - How long should user wait?
5. **Wait conditions** - What to check before re-invoking

**Example response:**
```
This task is in the "Post-Promotion Async Tasks" phase.

Prerequisites:
- Build must be promoted (phase == "Accepted") ✓
- Stage-release pipeline must succeed (Konflux only)

Current status:
- image-consistency-check: In Progress
- stage-testing: In Progress
- push-to-cdn-staging: Pass

Next steps:
- Wait for both async tasks to complete
- Then proceed to analyze-promoted-build
- Then gate check before final approval

Expected duration: 90-120 min for image-consistency-check, 2-4 hours for stage-testing
Action: Re-invoke /release:drive in 10-15 minutes to check status
```

## Reference Documentation

For detailed specifications, refer to:
- **Workflow Spec**: `docs/KONFLUX_RELEASE_FLOW.md`
- **Task Definitions**: Each task with MCP tool, inputs, success criteria
- **Execution Rules**: AI decision logic and error handling
- **Troubleshooting**: Common issues and resolutions

## Key Principles

1. **Sequential with Parallel Tracks** - Main pipeline is sequential, but has async tasks
2. **Checkpoint-Driven** - Critical checkpoints gate progression
3. **User Re-Invocation** - Long-running tasks require periodic status checks
4. **State-Based Decisions** - Always retrieve current state before acting
5. **Graceful Waiting** - Inform user of wait states with clear next actions

When in doubt about workflow specifics, reference `docs/KONFLUX_RELEASE_FLOW.md` for authoritative details.