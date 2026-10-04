---
name: dnd-map-builder
description: Use when working on the DnD Map Builder — a Next.js 14+ interactive map tool for DMs. Local install at C:\Users\joshu\OneDrive\AITools\dnd-map-builder, dev server at http://localhost:3000/. Triggers on map builder, terrain, canvas, grid, map editor, dnd-map-builder.
argument-hint: [feature|bug|question]
allowed-tools: Read Grep Glob Bash Edit Write
---

# DnD Map Builder

**Local install:** `C:\Users\joshu\OneDrive\AITools\dnd-map-builder`  
**Dev server:** http://localhost:3000/  
**Stack:** Next.js 14+ (App Router) · TypeScript · Tailwind CSS · Zustand · HTML5 Canvas · LocalStorage

## Working Directory

Always run commands from the install root:
```bash
cd "C:/Users/joshu/OneDrive/AITools/dnd-map-builder"
```

## Dev Commands

```bash
npm run dev          # start dev server → http://localhost:3000/
npm run build        # production build
npm start            # production server
npm run lint         # ESLint
npm run type-check   # TypeScript (tsc --noEmit)
npm run format       # Prettier write
npm run format:check # Prettier check
```

## Key Files

| Path | Purpose |
|------|---------|
| `src/stores/mapStore.ts` | Zustand store — grid, terrain, objects, tool, pan/zoom |
| `src/components/core/` | Canvas, Toolbar |
| `src/components/ui/` | Button, Tooltip, reusable UI |
| `src/lib/demoMaps.ts` | Pre-built demo map data |
| `src/lib/hooks/` | Custom hooks (useMapStore, etc.) |
| `src/lib/utils.ts` | Utility functions |
| `src/app/` | Next.js App Router pages and layouts |

## State (mapStore.ts)

Zustand store holds:
- Grid dimensions and cell size
- Terrain data per cell (`grass` | `water` | `sand` | `stone`)
- Object positions and types (Trees · Rocks · Buildings)
- Active tool and selected terrain/object
- Canvas pan/zoom state

## Common Tasks

**Add a terrain type:**
1. Extend the terrain enum/union in `src/stores/mapStore.ts`
2. Add rendering in the Canvas component (`src/components/core/`)
3. Add button in Toolbar

**Add an object type:**
1. Extend the object type enum in `mapStore.ts`
2. Add render logic in Canvas
3. Add to Toolbar selector

**Add a demo map:**
1. Add entry to `src/lib/demoMaps.ts` — terrain encoded as char map (`G`=grass, `W`=water, `S`=sand, `R`=stone)
2. Add name to "Load Demo" dropdown in Toolbar

**Performance on large grids:**
- Use offscreen canvas for terrain layer; overlay canvas for objects/cursor
- Debounce pan/zoom redraws
- Only repaint changed regions

## Before Completing Any Change

```bash
cd "C:/Users/joshu/OneDrive/AITools/dnd-map-builder" && npm run type-check && npm run lint
```
