---
name: github
description: "Skill for the Github area of paddock. 23 symbols across 5 files."
---

# Github

23 symbols | 5 files | Cohesion: 66%

## When to Use

- Working with code in `src/`
- Understanding how getEffectiveEnvValue, getGitHubToken, fetchIssues work
- Modifying github-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/app/api/github/route.ts` | GET, handleSync, handleGitHubStats, mapPriority, POST (+5) |
| `src/lib/github.ts` | getGitHubToken, fetchIssues, createIssueComment, updateIssueState, createLabel (+1) |
| `src/lib/runtime-env.ts` | parseEnvLine, readOpenClawEnvFile, getEffectiveEnvValue |
| `src/lib/github-sync-engine.ts` | classifyLabelProvisioningError, sanitizeLabelProvisioningError, initializeLabels |
| `src/lib/github-label-map.ts` | areaLabelsForWorkspace |

## Entry Points

Start here when exploring this area:

- **`getEffectiveEnvValue`** (Function) — `src/lib/runtime-env.ts:33`
- **`getGitHubToken`** (Function) — `src/lib/github.ts:74`
- **`fetchIssues`** (Function) — `src/lib/github.ts:124`
- **`GET`** (Function) — `src/app/api/github/route.ts:21`
- **`createIssueComment`** (Function) — `src/lib/github.ts:172`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `getEffectiveEnvValue` | Function | `src/lib/runtime-env.ts` | 33 |
| `getGitHubToken` | Function | `src/lib/github.ts` | 74 |
| `fetchIssues` | Function | `src/lib/github.ts` | 124 |
| `GET` | Function | `src/app/api/github/route.ts` | 21 |
| `createIssueComment` | Function | `src/lib/github.ts` | 172 |
| `updateIssueState` | Function | `src/lib/github.ts` | 190 |
| `POST` | Function | `src/app/api/github/route.ts` | 62 |
| `createLabel` | Function | `src/lib/github.ts` | 256 |
| `ensureLabels` | Function | `src/lib/github.ts` | 274 |
| `classifyLabelProvisioningError` | Function | `src/lib/github-sync-engine.ts` | 56 |
| `sanitizeLabelProvisioningError` | Function | `src/lib/github-sync-engine.ts` | 86 |
| `initializeLabels` | Function | `src/lib/github-sync-engine.ts` | 122 |
| `areaLabelsForWorkspace` | Function | `src/lib/github-label-map.ts` | 136 |
| `parseEnvLine` | Function | `src/lib/runtime-env.ts` | 5 |
| `readOpenClawEnvFile` | Function | `src/lib/runtime-env.ts` | 18 |
| `handleSync` | Function | `src/app/api/github/route.ts` | 100 |
| `handleGitHubStats` | Function | `src/app/api/github/route.ts` | 321 |
| `mapPriority` | Function | `src/app/api/github/route.ts` | 468 |
| `handleComment` | Function | `src/app/api/github/route.ts` | 229 |
| `handleClose` | Function | `src/app/api/github/route.ts` | 258 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `POST → NormalizeSecurityEventType` | cross_community | 6 |
| `POST → EnsureDirExists` | cross_community | 6 |
| `POST → HashPassword` | cross_community | 6 |
| `POST → ParseEnvLine` | cross_community | 6 |
| `POST → GitHubUrlValidationError` | cross_community | 6 |
| `POST → GetGeneratedFilePath` | cross_community | 6 |
| `POST → Generate` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| [id] | 9 calls |
| Cluster_251 | 5 calls |
| Tasks | 1 calls |
| Cluster_125 | 1 calls |
| Cluster_256 | 1 calls |

## How to Explore

1. `gitnexus_context({name: "getEffectiveEnvValue"})` — see callers and callees
2. `gitnexus_query({query: "github"})` — find related execution flows
3. Read key files listed above for implementation details
