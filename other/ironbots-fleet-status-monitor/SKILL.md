---
name: ironbots-fleet-status-monitor
description: Use when monitoring the Ironbots fleet execution state, checking scheduled task telemetry across background workers, detecting bot failures, or generating aggregated health status reports.
compatibility: |
  - Runtime: Node.js 18+, TypeScript 5.0+
  - Dependencies: _status-feed/ telemetry, Windows Task Scheduler / process logs
  - Permissions: read:repo, read:logs
---

# ironbots-fleet-status-monitor

Aggregates execution status and live telemetry across all 9 Ironbots fleet tasks, detects runtime errors and PGID threshold violations, and renders unified fleet health summaries.

## When to Use

- Daily scheduled fleet health reporting and telemetry aggregation
- On-demand fleet state checks across autonomous bot processes
- Triage and investigation of failing or degraded Ironbots scheduled tasks

## Core Fleet Tasks

The monitor tracks the following 9 canonical fleet tasks:
1. `Notebook-Ingester`
2. `KB-Sentinel`
3. `TRM-Bot`
4. `Watchlist-Miner`
5. `Daemon-Healer`
6. `CI-Watchdog`
7. `TRM-Drive-Sync`
8. `Storage-Pruner`
9. `Ironbots-Reporter`

## Trigger & Usage

```bash
# Query live fleet health status
invoke ironbots-fleet-status-monitor { "action": "status" }

# Run full telemetry aggregation and alert detection
invoke ironbots-fleet-status-monitor { "action": "aggregate", "verbose": true }
```

## Input Schema

```typescript
interface SkillInput {
  action: "status" | "aggregate" | "diagnose";
  statusFeedDir?: string;       // Default: _status-feed/
  taskFilter?: string[];        // Optional subset of bot tasks to query
  verbose?: boolean;            // Enable detailed output
}
```

## Output Schema

```typescript
interface TaskTelemetry {
  taskId: string;
  status: "HEALTHY" | "DEGRADED" | "FAILED" | "UNKNOWN";
  lastRun?: string;
  exitCode?: number;
  message?: string;
  details?: Record<string, unknown>;
}

interface SkillOutput {
  status: "success" | "warning" | "error";
  fleetScore: number;           // 0 to 100
  totalTasks: number;
  healthyCount: number;
  failedCount: number;
  tasks: TaskTelemetry[];
  alerts: string[];
  timestamp: string;
}
```

## Error Handling

| Code | Message | Handler | Escalation |
|------|---------|---------|------------|
| `STATUS_FEED_MISSING` | Telemetry directory not accessible | Fallback to direct process query | Inspect `_status-feed/` mount |
| `TASK_NOT_FOUND` | Specified task ID not recognized | Skip or warn | Verify task name in `REQUIRED_FLEET_TASKS` |
| `TELEMETRY_CORRUPT` | Telemetry report JSON unparseable | Mark task as UNKNOWN | Inspect log format |

---

## Quick Reference

| Action | Purpose | Typical Latency |
|--------|---------|-----------------|
| `status` | Lightweight query of cached task reports | < 50ms |
| `aggregate` | Deep scan of all 9 bot telemetry reports + scoring | < 200ms |
| `diagnose` | Detailed error trace of failing fleet bots | < 500ms |
