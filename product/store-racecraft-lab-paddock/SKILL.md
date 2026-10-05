---
name: store
description: "Skill for the Store area of paddock. 29 symbols across 4 files."
---

# Store

29 symbols | 4 files | Cohesion: 71%

## When to Use

- Working with code in `src/`
- Understanding how dismissUpdate, dismissOpenclawUpdate, dismissDoctor work
- Modifying store-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/store/index.ts` | setStorageItem, dismissUpdate, dismissOpenclawUpdate, dismissDoctor, toggleSidebar (+17) |
| `src/types/product-line.ts` | parsePersistedProductLineScope, selectableProductLines, serializeProductLineScope |
| `src/store/product-line-broadcast.test.ts` | installLocalStorage, installBroadcastChannel, loadStore |
| `src/components/layout/workspace-switcher.tsx` | productLines |

## Entry Points

Start here when exploring this area:

- **`dismissUpdate`** (Function) — `src/store/index.ts:776`
- **`dismissOpenclawUpdate`** (Function) — `src/store/index.ts:785`
- **`dismissDoctor`** (Function) — `src/store/index.ts:795`
- **`toggleSidebar`** (Function) — `src/store/index.ts:1214`
- **`setSidebarExpanded`** (Function) — `src/store/index.ts:1220`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `dismissUpdate` | Function | `src/store/index.ts` | 776 |
| `dismissOpenclawUpdate` | Function | `src/store/index.ts` | 785 |
| `dismissDoctor` | Function | `src/store/index.ts` | 795 |
| `toggleSidebar` | Function | `src/store/index.ts` | 1214 |
| `setSidebarExpanded` | Function | `src/store/index.ts` | 1220 |
| `toggleGroup` | Function | `src/store/index.ts` | 1224 |
| `toggleLiveFeed` | Function | `src/store/index.ts` | 1232 |
| `setHeaderDensity` | Function | `src/store/index.ts` | 1238 |
| `parsePersistedProductLineScope` | Function | `src/types/product-line.ts` | 82 |
| `selectableProductLines` | Function | `src/types/product-line.ts` | 116 |
| `fetchWorkspaces` | Function | `src/store/index.ts` | 1067 |
| `productLines` | Function | `src/components/layout/workspace-switcher.tsx` | 47 |
| `serializeProductLineScope` | Function | `src/types/product-line.ts` | 106 |
| `setActiveProductLine` | Function | `src/store/index.ts` | 1025 |
| `setActiveTenant` | Function | `src/store/index.ts` | 958 |
| `setActiveProject` | Function | `src/store/index.ts` | 995 |
| `setDashboardLayout` | Function | `src/store/index.ts` | 1180 |
| `setStorageItem` | Function | `src/store/index.ts` | 52 |
| `getStorageItem` | Function | `src/store/index.ts` | 47 |
| `deriveTenantId` | Function | `src/store/index.ts` | 671 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Feature-flags | 2 calls |
| Panels | 2 calls |
| Tasks | 1 calls |

## How to Explore

1. `gitnexus_context({name: "dismissUpdate"})` — see callers and callees
2. `gitnexus_query({query: "store"})` — find related execution flows
3. Read key files listed above for implementation details
