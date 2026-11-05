---
name: persisting-progress-across-sessions
description: Resume an interrupted orchestration run across Claude Code sessions using MANIFEST.yaml
trigger: "resume|continue|restart|session.*reset|context.*compact|pick up where"
category: core
---

# Persisting Progress Across Sessions

Use this skill when a session ends mid-orchestration (context compaction, manual restart, crash) and you need to resume without repeating completed work.

## The Resume Protocol

### Step 1 — Find the Incomplete MANIFEST

```bash
# List all in-progress features
ls .jonggrang/.output/features/
```

Look for a `MANIFEST.yaml` with `status: running` or `status: paused`. Read it:

```bash
cat .jonggrang/.output/features/{feature_id}/MANIFEST.yaml
```

Key fields to read:
- `current_phase` — next phase to execute
- `active_phases` — which phases this run is executing
- `phases` — per-phase status (completed / failed / pending)
- `agents` — which agents ran and their output paths
- `validation` — review_passed, tests_passed, coverage_met

### Step 2 — Reconstruct Context from Phase Outputs

Do NOT re-run completed phases. Read their outputs instead:

```bash
# Phase 7 output (architecture plan)
cat .jonggrang/.output/features/{feature_id}/07-lead-architecture-plan.json

# Phase 8 output (implementation)
cat .jonggrang/.output/features/{feature_id}/08-developer-{task_id}.json

# Any reviewer reports
cat .jonggrang/.output/features/{feature_id}/09-reviewer-report.json
```

### Step 3 — Identify Resumption Point

```
current_phase in MANIFEST  →  start from this phase
phases[N].status == 'failed'  →  retry this phase
phases[N].status == 'completed'  →  skip, output already exists
```

### Step 4 — Resume the Orchestration

Call `orchestrating-feature` with `resume: true` and the feature_id. Pass the reconstructed context as a summary — do NOT re-read all source code; trust the phase outputs.

```
Resuming feature: {feature_id}
Completed phases: 1, 2, 3, 4, 7, 8
Current phase: 9 (design-verification)
Architecture plan: [summary from 07-lead-architecture-plan.json]
Implementation: [summary from 08-developer.json]
```

## Cross-Session State Guarantee

The MANIFEST survives session resets. The ephemeral state does NOT:

| File | Survives reset? | Action on resume |
|------|----------------|------------------|
| `MANIFEST.yaml` | ✅ Yes | Read to get current phase |
| `feedback-loop-state.json` | ❌ No | Assume clean state, re-run review/test if dirty_bit lost |
| `compaction-state.json` | ❌ No | Will be refreshed on next Task spawn |
| `session-roles.json` | ❌ No | Will be re-populated on next session start |

## When Tests Were Running

If context compacted during phase 13 (testing), check `validation.tests_passed` in MANIFEST:

- `false` → re-spawn tester
- `true` → proceed to phase 14 (coverage)

## Stale Lock Cleanup

On resume, clean up any stale lock files left by crashed agents:

```javascript
const { cleanStaleLocks } = require('./lib/locks');
cleanStaleLocks(projectRoot);  // removes locks older than 30 minutes
```

## Example Resume Flow

```
Session ended at phase 9.
MANIFEST shows: phases[8].status = 'completed', phases[9].status = 'running'

Resume steps:
1. Read 07-lead-architecture-plan.json → architecture context
2. Read 08-developer-*.json → what was implemented
3. Re-spawn reviewer for phase 9 with the implementation context
4. Continue from phase 9 forward
```
