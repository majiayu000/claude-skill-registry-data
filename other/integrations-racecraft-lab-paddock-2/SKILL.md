---
name: integrations
description: "Skill for the Integrations area of paddock. 25 symbols across 2 files."
---

# Integrations

25 symbols | 2 files | Cohesion: 82%

## When to Use

- Working with code in `src/`
- Understanding how getPluginIntegrations, getPluginCategories, GET work
- Modifying integrations-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/app/api/integrations/route.ts` | parseEnv, serializeEnv, getEnvPath, readEnvFile, writeEnvFile (+18) |
| `src/lib/plugins.ts` | getPluginIntegrations, getPluginCategories |

## Entry Points

Start here when exploring this area:

- **`getPluginIntegrations`** (Function) — `src/lib/plugins.ts:66`
- **`getPluginCategories`** (Function) — `src/lib/plugins.ts:78`
- **`GET`** (Function) — `src/app/api/integrations/route.ts:308`
- **`POST`** (Function) — `src/app/api/integrations/route.ts:582`
- **`integrations`** (Function) — `src/app/api/integrations/route.ts:354`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `getPluginIntegrations` | Function | `src/lib/plugins.ts` | 66 |
| `getPluginCategories` | Function | `src/lib/plugins.ts` | 78 |
| `GET` | Function | `src/app/api/integrations/route.ts` | 308 |
| `POST` | Function | `src/app/api/integrations/route.ts` | 582 |
| `integrations` | Function | `src/app/api/integrations/route.ts` | 354 |
| `parseEnv` | Function | `src/app/api/integrations/route.ts` | 119 |
| `serializeEnv` | Function | `src/app/api/integrations/route.ts` | 141 |
| `getEnvPath` | Function | `src/app/api/integrations/route.ts` | 148 |
| `readEnvFile` | Function | `src/app/api/integrations/route.ts` | 153 |
| `writeEnvFile` | Function | `src/app/api/integrations/route.ts` | 165 |
| `checkCommandAvailable` | Function | `src/app/api/integrations/route.ts` | 220 |
| `checkXintState` | Function | `src/app/api/integrations/route.ts` | 229 |
| `resolveOllamaBaseUrl` | Function | `src/app/api/integrations/route.ts` | 238 |
| `checkOllamaReachable` | Function | `src/app/api/integrations/route.ts` | 245 |
| `getIntegrationProbeSnapshot` | Function | `src/app/api/integrations/route.ts` | 255 |
| `checkOpAvailable` | Function | `src/app/api/integrations/route.ts` | 273 |
| `getOpEnv` | Function | `src/app/api/integrations/route.ts` | 287 |
| `handleTest` | Function | `src/app/api/integrations/route.ts` | 637 |
| `handlePull` | Function | `src/app/api/integrations/route.ts` | 834 |
| `handlePullAll` | Function | `src/app/api/integrations/route.ts` | 919 |

## Connected Areas

| Area | Connections |
|------|-------------|
| [id] | 6 calls |
| Status | 2 calls |

## How to Explore

1. `gitnexus_context({name: "getPluginIntegrations"})` — see callers and callees
2. `gitnexus_query({query: "integrations"})` — find related execution flows
3. Read key files listed above for implementation details
