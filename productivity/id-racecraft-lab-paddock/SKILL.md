---
name: id
description: "Skill for the [id] area of paddock. 497 symbols across 165 files."
---

# [id]

497 symbols | 165 files | Cohesion: 88%

## When to Use

- Working with code in `src/`
- Understanding how listWorkspacesForTenant, resolveWorkspaceScopeFromRequest, workspaceScopePredicate work
- Modifying [id]-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/lib/task-artifacts.ts` | getInlineContent, SupersedeTargetAlreadySuperseded, CannotSupersedeQuarantined, InternalStorageError, fetchArtifactRow (+18) |
| `src/lib/db.ts` | getDatabase, logActivity, createNotification, createTaskReadyForOwnerNotification, parseMentions (+8) |
| `src/app/api/tokens/route.ts` | extractAgentName, loadTokenDataFromDb, normalizeTokenRecord, dedupeTokenRecords, loadTokenDataFromFile (+5) |
| `src/app/api/chat/messages/route.ts` | parseGatewayJson, toGatewayAttachments, safeParseMetadata, createChatReply, extractReplyText (+5) |
| `src/lib/agent-evals.ts` | evalTaskCompletion, evalCorrectnessScore, runOutputEvals, convergenceScore, evalReasoningCoherence (+4) |
| `src/app/api/workflows/route.ts` | parseJsonField, serializeJsonField, serializeRoutingRules, templateResponse, requireProductLineScope (+4) |
| `src/app/api/tasks/[id]/route.ts` | formatTicketRef, mapTaskRow, hasAegisApproval, taskProducesPr, isReadyForOwnerMergeGatedTask (+4) |
| `src/lib/runs.ts` | updateRun, attachEval, getRun, listRuns, getRunProvenance (+3) |
| `src/app/api/projects/[id]/route.ts` | classifyError, normalizePrefix, toProjectId, GET, PATCH (+3) |
| `src/app/api/governance/policies/route.ts` | policyEtag, jsonError, decodeCursor, clampLimit, kindToPolicyType (+3) |

## Entry Points

Start here when exploring this area:

- **`listWorkspacesForTenant`** (Function) — `src/lib/workspaces.ts:110`
- **`resolveWorkspaceScopeFromRequest`** (Function) — `src/lib/workspaces.ts:256`
- **`workspaceScopePredicate`** (Function) — `src/lib/workspaces.ts:266`
- **`agentWorkspaceScopePredicate`** (Function) — `src/lib/workspaces.ts:282`
- **`workspaceScopeError`** (Function) — `src/lib/workspaces.ts:298`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `SupersedeTargetAlreadySuperseded` | Class | `src/lib/task-artifacts.ts` | 409 |
| `CannotSupersedeQuarantined` | Class | `src/lib/task-artifacts.ts` | 421 |
| `InternalStorageError` | Class | `src/lib/task-artifacts.ts` | 437 |
| `ArtifactNotFound` | Class | `src/lib/task-artifacts.ts` | 1184 |
| `AlreadyQuarantined` | Class | `src/lib/task-artifacts.ts` | 1193 |
| `NotQuarantined` | Class | `src/lib/task-artifacts.ts` | 1202 |
| `SweepInProgress` | Class | `src/lib/task-artifacts.ts` | 1211 |
| `listWorkspacesForTenant` | Function | `src/lib/workspaces.ts` | 110 |
| `resolveWorkspaceScopeFromRequest` | Function | `src/lib/workspaces.ts` | 256 |
| `workspaceScopePredicate` | Function | `src/lib/workspaces.ts` | 266 |
| `agentWorkspaceScopePredicate` | Function | `src/lib/workspaces.ts` | 282 |
| `workspaceScopeError` | Function | `src/lib/workspaces.ts` | 298 |
| `deliverWebhookPublic` | Function | `src/lib/webhooks.ts` | 164 |
| `validateBody` | Function | `src/lib/validation.ts` | 9 |
| `getModelPricing` | Function | `src/lib/token-pricing.ts` | 46 |
| `calculateTokenCost` | Function | `src/lib/token-pricing.ts` | 62 |
| `hasAssignee` | Function | `src/lib/task-status.ts` | 108 |
| `normalizeTaskCreateStatus` | Function | `src/lib/task-status.ts` | 116 |
| `normalizeTaskUpdateStatus` | Function | `src/lib/task-status.ts` | 129 |
| `parseMetadata` | Function | `src/lib/task-routing.ts` | 15 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `PATCH → EnsureDirExists` | cross_community | 7 |
| `PATCH → CalculateAgentTrustScore` | cross_community | 7 |
| `PATCH → Generate` | cross_community | 7 |
| `POST → EnsureDirExists` | cross_community | 7 |
| `POST → CalculateAgentTrustScore` | cross_community | 7 |
| `POST → Generate` | cross_community | 7 |
| `GET → EnsureDirExists` | cross_community | 7 |
| `GET → CalculateAgentTrustScore` | cross_community | 7 |
| `GET → Generate` | cross_community | 7 |
| `POST → EnsureDirExists` | cross_community | 7 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tasks | 9 calls |
| Users | 8 calls |
| Sessions | 6 calls |
| Aggregate | 4 calls |
| Cluster_240 | 4 calls |
| Cluster_237 | 4 calls |
| Integrations | 4 calls |
| Cluster_251 | 4 calls |

## How to Explore

1. `gitnexus_context({name: "listWorkspacesForTenant"})` — see callers and callees
2. `gitnexus_query({query: "[id]"})` — find related execution flows
3. Read key files listed above for implementation details
