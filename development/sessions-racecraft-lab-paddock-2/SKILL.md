---
name: sessions
description: "Skill for the Sessions area of paddock. 50 symbols across 13 files."
---

# Sessions

50 symbols | 13 files | Cohesion: 67%

## When to Use

- Working with code in `src/`
- Understanding how processWebhookRetries, requeueStaleTasks, autoRouteInboxTasks work
- Modifying sessions-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/app/api/sessions/route.ts` | POST, DELETE, GET, mapGatewaySessions, getLocalClaudeSessions (+7) |
| `src/lib/openclaw-gateway.ts` | parseGatewayJsonOutput, formatGatewayError, formatGatewayFrameError, buildGatewayWebSocketUrl, unwrapGatewayResponsePayload (+6) |
| `src/lib/scheduler.ts` | getSettingNumber, runBackup, runCleanup, runHeartbeatCheck, initScheduler (+3) |
| `src/lib/task-dispatch.ts` | syncAndEscalateIfFailed, requeueStaleTasks, scoreAgentForTask, autoRouteInboxTasks |
| `src/lib/claude-sessions.ts` | clampTimestamp, parseSessionFile, scanClaudeSessions, syncClaudeSessions |
| `src/lib/schedule-parser.ts` | isCronDue, matchesCronField |
| `src/lib/recurring-tasks.ts` | formatDateSuffix, spawnRecurringTasks |
| `src/lib/codex-sessions.ts` | listRecentCodexSessionFiles, scanCodexSessions |
| `src/lib/webhooks.ts` | processWebhookRetries |
| `src/lib/skill-sync.ts` | syncSkillsFromDisk |

## Entry Points

Start here when exploring this area:

- **`processWebhookRetries`** (Function) — `src/lib/webhooks.ts:301`
- **`requeueStaleTasks`** (Function) — `src/lib/task-dispatch.ts:1644`
- **`autoRouteInboxTasks`** (Function) — `src/lib/task-dispatch.ts:2035`
- **`syncSkillsFromDisk`** (Function) — `src/lib/skill-sync.ts:133`
- **`initScheduler`** (Function) — `src/lib/scheduler.ts:278`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `processWebhookRetries` | Function | `src/lib/webhooks.ts` | 301 |
| `requeueStaleTasks` | Function | `src/lib/task-dispatch.ts` | 1644 |
| `autoRouteInboxTasks` | Function | `src/lib/task-dispatch.ts` | 2035 |
| `syncSkillsFromDisk` | Function | `src/lib/skill-sync.ts` | 133 |
| `initScheduler` | Function | `src/lib/scheduler.ts` | 278 |
| `triggerTask` | Function | `src/lib/scheduler.ts` | 512 |
| `isCronDue` | Function | `src/lib/schedule-parser.ts` | 165 |
| `spawnRecurringTasks` | Function | `src/lib/recurring-tasks.ts` | 29 |
| `scanClaudeSessions` | Function | `src/lib/claude-sessions.ts` | 219 |
| `syncClaudeSessions` | Function | `src/lib/claude-sessions.ts` | 273 |
| `syncAgentsFromConfig` | Function | `src/lib/agent-sync.ts` | 288 |
| `POST` | Function | `src/app/api/claude/sessions/route.ts` | 90 |
| `parseGatewayJsonOutput` | Function | `src/lib/openclaw-gateway.ts` | 39 |
| `unwrapGatewayResponsePayload` | Function | `src/lib/openclaw-gateway.ts` | 97 |
| `callOpenClawGatewayViaWebSocket` | Function | `src/lib/openclaw-gateway.ts` | 137 |
| `finishReject` | Function | `src/lib/openclaw-gateway.ts` | 154 |
| `finishResolve` | Function | `src/lib/openclaw-gateway.ts` | 165 |
| `timer` | Function | `src/lib/openclaw-gateway.ts` | 176 |
| `callOpenClawGateway` | Function | `src/lib/openclaw-gateway.ts` | 304 |
| `POST` | Function | `src/app/api/sessions/route.ts` | 47 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `GET → NormalizeSecurityEventType` | cross_community | 6 |
| `GET → EnsureDirExists` | cross_community | 6 |
| `GET → HashPassword` | cross_community | 6 |
| `GET → GetGeneratedFilePath` | cross_community | 6 |
| `GET → ClampTimestamp` | cross_community | 5 |
| `GET → Generate` | cross_community | 5 |
| `GET → ExtractClientIpFromTrusted` | cross_community | 4 |
| `GET → ParseMcSessionCookieHeader` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| [id] | 25 calls |
| Cluster_218 | 4 calls |
| Aggregate | 3 calls |
| Cluster_126 | 2 calls |
| Cluster_127 | 2 calls |
| Cluster_219 | 2 calls |
| Cluster_102 | 1 calls |
| Cluster_142 | 1 calls |

## How to Explore

1. `gitnexus_context({name: "processWebhookRetries"})` — see callers and callees
2. `gitnexus_query({query: "sessions"})` — find related execution flows
3. Read key files listed above for implementation details
