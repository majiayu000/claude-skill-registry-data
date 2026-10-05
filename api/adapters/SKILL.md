---
name: adapters
description: "Skill for the Adapters area of paddock. 108 symbols across 22 files."
---

# Adapters

108 symbols | 22 files | Cohesion: 85%

## When to Use

- Working with code in `src/`
- Understanding how getAdapter, POST, tx work
- Modifying adapters-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/lib/adapters/index.ts` | getAdapter, openclaw, generic, crewai, langgraph (+3) |
| `src/lib/adapters/adapter.ts` | register, heartbeat, reportTask, getAssignments, disconnect (+2) |
| `src/lib/observability/adapters/openclaw-gateway.ts` | tx, defaultHealthDir, registerOpenclawGatewaySource, readCostBasis, readCurrentRate (+2) |
| `src/lib/observability/adapters/copilot-events-jsonl.ts` | tierToEligibility, tierToConfidence, tx, defaultEventsPath, registerCopilotEventsSource (+2) |
| `src/lib/adapters/openclaw.ts` | register, heartbeat, reportTask, disconnect, OpenClawAdapter (+1) |
| `src/lib/adapters/langgraph.ts` | register, heartbeat, reportTask, disconnect, LangGraphAdapter (+1) |
| `src/lib/adapters/generic.ts` | register, heartbeat, reportTask, disconnect, GenericAdapter (+1) |
| `src/lib/adapters/crewai.ts` | register, heartbeat, reportTask, disconnect, CrewAIAdapter (+1) |
| `src/lib/adapters/claude-sdk.ts` | register, heartbeat, reportTask, disconnect, ClaudeSdkAdapter (+1) |
| `src/lib/adapters/autogen.ts` | register, heartbeat, reportTask, disconnect, AutoGenAdapter (+1) |

## Entry Points

Start here when exploring this area:

- **`getAdapter`** (Function) — `src/lib/adapters/index.ts:17`
- **`POST`** (Function) — `src/app/api/adapters/route.ts:28`
- **`tx`** (Function) — `src/lib/observability/adapters/openclaw-gateway.ts:213`
- **`tx`** (Function) — `src/lib/observability/adapters/ollama-log.ts:186`
- **`adaptManualPost`** (Function) — `src/lib/observability/adapters/manual-post.ts:80`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `OpenClawAdapter` | Class | `src/lib/adapters/openclaw.ts` | 4 |
| `LangGraphAdapter` | Class | `src/lib/adapters/langgraph.ts` | 4 |
| `GenericAdapter` | Class | `src/lib/adapters/generic.ts` | 4 |
| `CrewAIAdapter` | Class | `src/lib/adapters/crewai.ts` | 4 |
| `ClaudeSdkAdapter` | Class | `src/lib/adapters/claude-sdk.ts` | 4 |
| `AutoGenAdapter` | Class | `src/lib/adapters/autogen.ts` | 4 |
| `getAdapter` | Function | `src/lib/adapters/index.ts` | 17 |
| `POST` | Function | `src/app/api/adapters/route.ts` | 28 |
| `tx` | Function | `src/lib/observability/adapters/openclaw-gateway.ts` | 213 |
| `tx` | Function | `src/lib/observability/adapters/ollama-log.ts` | 186 |
| `adaptManualPost` | Function | `src/lib/observability/adapters/manual-post.ts` | 80 |
| `tx` | Function | `src/lib/observability/adapters/lm-studio-log.ts` | 215 |
| `tx` | Function | `src/lib/observability/adapters/copilot-events-jsonl.ts` | 252 |
| `tx` | Function | `src/lib/observability/adapters/codex-rollout.ts` | 216 |
| `tx` | Function | `src/lib/observability/adapters/claude-code-transcript.ts` | 189 |
| `partitionMonthFromMs` | Function | `src/lib/observability/adapters/_adapter-helpers.ts` | 61 |
| `insertRawUsageEvent` | Function | `src/lib/observability/adapters/_adapter-helpers.ts` | 87 |
| `queryPendingAssignments` | Function | `src/lib/adapters/adapter.ts` | 2 |
| `registerManualPostSource` | Function | `src/lib/observability/adapters/manual-post.ts` | 66 |
| `registerClaudeTranscriptSource` | Function | `src/lib/observability/adapters/claude-code-transcript.ts` | 108 |

## Connected Areas

| Area | Connections |
|------|-------------|
| [id] | 4 calls |
| Observability | 2 calls |
| Tasks | 1 calls |

## How to Explore

1. `gitnexus_context({name: "getAdapter"})` — see callers and callees
2. `gitnexus_query({query: "adapters"})` — find related execution flows
3. Read key files listed above for implementation details
