---
name: verify-alignment
description: >
  Run full source-of-truth verification: tests, lint, contract drift check, and codegraph scan.
  Automatically invoked after significant code or documentation changes to confirm alignment.
  Also triggered by session-end drift check hook when contract-paired files were modified.
---

# Verify Alignment

Full verification suite for source-of-truth alignment. Run this after any significant changes to confirm nothing drifted.

## Phase 1: Automated Checks

Run these in parallel:

```bash
npm test --prefix server        # State machine + other tests
npm run lint --prefix client    # ESLint
```

Both must pass before continuing. If either fails, fix the issue first.

## Phase 2: Codegraph Scan

Use the codegraph MCP tools (load via ToolSearch first):

1. `mcp__codegraph__codegraph_scan` — rebuild the dependency graph
2. `mcp__codegraph__codegraph_get_stats` — check file counts and connectivity

Compare stats against CLAUDE.md `CODEGRAPH_ANALYSIS.stats_as_of` section. If numbers changed significantly, update CLAUDE.md.

## Phase 3: Contract Drift Check

For each contract pair, do a targeted comparison. Read both sides and check for mismatches.

### 3a. State Machine
- Read `server/src/taskStateMachine.js` — extract TRANSITION_MAP and TRANSITION_REQUIREMENTS
- Read `docs/contracts/task-state-machine.md` — extract documented states/transitions/guards
- Read CLAUDE.md STATE_MACHINE section
- Verify all three agree on: states, transitions, guards, invariants

### 3b. Database Schema
- Read `server/src/db/schema.js` — extract CREATE TABLE statements
- Read `docs/contracts/database-schema.md`
- Read CLAUDE.md DB_SCHEMA section
- Verify: table names, column names, types, CHECK constraints, defaults, indexes

### 3c. API Endpoints
- Read `server/src/routes/tasks.js`, `projects.js`, `documents.js`, `activity.js`
- Read `docs/contracts/api-endpoints.md`
- Read CLAUDE.md API_ENDPOINTS section
- Verify: method, path, required fields, response codes, error shapes

### 3d. WebSocket Events
- Read `server/src/ws.js` and `server/src/events.js`
- Read `docs/contracts/websocket-events.md`
- Read CLAUDE.md WEBSOCKET_EVENTS section
- Verify: event names, triggers, payload fields, broadcast pattern

### 3e. Milestone System
- Read `server/src/milestoneSync.js` and `server/src/templates/milestoneTasks.js`
- Read CLAUDE.md MILESTONE_SYSTEM section
- Verify: auto-transition rules, milestone count, phase linkage

### 3f. Phase System
- Read `client/src/components/layout/PhaseBar.jsx`
- Read CLAUDE.md PHASE_SYSTEM section
- Verify: phase numbers/names, canAdvance() logic, doc requirements

### 3g. File Map
- Read CLAUDE.md FILE_MAP section
- Spot-check that listed files actually exist (use Glob)
- Check for files that exist but aren't listed (especially in routes/, hooks/, components/)

## Phase 4: Cross-Reference Checks

Verify internal CLAUDE.md consistency:
- `SAFE_MODIFICATIONS` references correct file paths
- `DEBUG_CHECKLIST` references correct file paths and field names
- `ANTI_PATTERNS` examples use valid field names and status values
- `CODEGRAPH_ANALYSIS` stats are current

## Output

```
ALIGNMENT VERIFICATION REPORT
  Date: [current date]

  Automated Checks:
    Tests: PASS/FAIL [details if fail]
    Lint: PASS/FAIL [details if fail]

  Codegraph:
    Files: [N] (was [N] in CLAUDE.md)
    Stats current: YES/NO

  Contract Drift:
    State Machine: ALIGNED/DRIFT [details]
    Database Schema: ALIGNED/DRIFT [details]
    API Endpoints: ALIGNED/DRIFT [details]
    WebSocket Events: ALIGNED/DRIFT [details]
    Milestone System: ALIGNED/DRIFT [details]
    Phase System: ALIGNED/DRIFT [details]
    File Map: ALIGNED/DRIFT [details]

  Cross-References: CONSISTENT/ISSUES [details]

  Overall: ALIGNED / [N] issues found
```

If drift is found, list each finding but do NOT fix anything automatically. The user decides what to change.
