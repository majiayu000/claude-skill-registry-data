---
name: panels
description: "Skill for the Panels area of paddock. 727 symbols across 76 files."
---

# Panels

727 symbols | 76 files | Cohesion: 75%

## When to Use

- Working with code in `src/`
- Understanding how appendScopeToPath, fetchProjects, exportClientCsv work
- Modifying panels-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/components/panels/office-panel.tsx` | formatLastSeen, easeInOut, getStatusEmote, inferLocalRole, getPropSprite (+41) |
| `src/components/panels/agent-detail-tabs.tsx` | handleSendMessage, handleSave, fetchTasks, fetchActivities, loadWorkspaceDocs (+37) |
| `src/components/panels/task-board-panel.tsx` | handleClick, handleSpawn, fetchReviews, fetchComments, handleAddComment (+32) |
| `src/components/panels/channels-panel.tsx` | ChannelsPanel, fetchChannels, handleProbe, handleAction, onProbe (+27) |
| `src/components/panels/cron-management-panel.tsx` | getAgentColorClass, isSameDay, formatDateLabel, CronManagementPanel, formatRelativeTime (+27) |
| `src/components/panels/memory-browser-panel.tsx` | mergeDirectoryChildren, fetchTree, loadFileTree, loadFileContent, toggleFolder (+26) |
| `src/components/panels/cost-tracker-panel.tsx` | buildGovernancePath, formatNumber, formatCost, getModelDisplayName, CostTrackerPanel (+18) |
| `src/components/panels/gateway-config-panel.tsx` | defaultValueFor, deepSet, matchesSearch, GatewayConfigPanel, fetchSchema (+18) |
| `src/components/panels/token-dashboard-panel.tsx` | exportClientCsv, TokenDashboardPanel, loadUsageStats, loadTrendData, loadSessionCosts (+16) |
| `src/components/panels/agent-squad-panel-phase3.tsx` | syncFromConfig, fetchAgents, updateAgentStatus, wakeAgent, toggleAgentHidden (+15) |

## Entry Points

Start here when exploring this area:

- **`appendScopeToPath`** (Function) — `src/types/product-line.ts:120`
- **`fetchProjects`** (Function) — `src/store/index.ts:1006`
- **`exportClientCsv`** (Function) — `src/components/panels/token-dashboard-panel.tsx:204`
- **`handleSpawn`** (Function) — `src/components/panels/task-board-panel.tsx:681`
- **`fetchTree`** (Function) — `src/components/panels/memory-browser-panel.tsx:145`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `appendScopeToPath` | Function | `src/types/product-line.ts` | 120 |
| `fetchProjects` | Function | `src/store/index.ts` | 1006 |
| `exportClientCsv` | Function | `src/components/panels/token-dashboard-panel.tsx` | 204 |
| `handleSpawn` | Function | `src/components/panels/task-board-panel.tsx` | 681 |
| `fetchTree` | Function | `src/components/panels/memory-browser-panel.tsx` | 145 |
| `loadFileTree` | Function | `src/components/panels/memory-browser-panel.tsx` | 153 |
| `loadFileContent` | Function | `src/components/panels/memory-browser-panel.tsx` | 192 |
| `toggleFolder` | Function | `src/components/panels/memory-browser-panel.tsx` | 246 |
| `saveFile` | Function | `src/components/panels/memory-browser-panel.tsx` | 261 |
| `createNewFile` | Function | `src/components/panels/memory-browser-panel.tsx` | 285 |
| `deleteFile` | Function | `src/components/panels/memory-browser-panel.tsx` | 302 |
| `runPipelineAction` | Function | `src/components/panels/memory-browser-panel.tsx` | 362 |
| `buildGovernancePath` | Function | `src/components/panels/cost-tracker-panel.tsx` | 182 |
| `updateAgentStatus` | Function | `src/components/panels/agent-squad-panel.tsx` | 89 |
| `syncFromConfig` | Function | `src/components/panels/agent-squad-panel-phase3.tsx` | 103 |
| `fetchAgents` | Function | `src/components/panels/agent-squad-panel-phase3.tsx` | 134 |
| `updateAgentStatus` | Function | `src/components/panels/agent-squad-panel-phase3.tsx` | 166 |
| `wakeAgent` | Function | `src/components/panels/agent-squad-panel-phase3.tsx` | 200 |
| `toggleAgentHidden` | Function | `src/components/panels/agent-squad-panel-phase3.tsx` | 228 |
| `deleteAgent` | Function | `src/components/panels/agent-squad-panel-phase3.tsx` | 241 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Home → Error` | cross_community | 4 |
| `ContentRouter → PanelHref` | cross_community | 4 |
| `ContentRouter → SafePrefetch` | cross_community | 4 |
| `ContentRouter → StartNavigationTiming` | cross_community | 4 |
| `ContentRouter → Cn` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ui | 5 calls |
| Dashboard | 3 calls |
| Settings | 2 calls |
| Cluster_272 | 1 calls |
| Modals | 1 calls |
| Cluster_274 | 1 calls |
| Onboarding | 1 calls |
| Setup | 1 calls |

## How to Explore

1. `gitnexus_context({name: "appendScopeToPath"})` — see callers and callees
2. `gitnexus_query({query: "panels"})` — find related execution flows
3. Read key files listed above for implementation details
