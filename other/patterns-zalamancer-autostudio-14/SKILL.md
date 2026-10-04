---
name: patterns
description: ProAnimate coding patterns, conventions, naming rules, import style, and component patterns. Auto-applied when writing code.
user-invocable: false
---

# ProAnimate Coding Patterns

## TypeScript

- Strict mode enabled
- Types defined in `src/types/<featureName>.ts`
- Path alias `@/` maps to `./src/` (e.g., `import { useCanvasStore } from '@/stores/useCanvasStore'`)
- Prefer `type` imports: `import type { ClipPlan } from '@/types/orchestrator'`
- Use `interface` for component props and state shapes, `type` for unions and utility types

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Services | camelCase file | `orchestrator.ts`, `meshyAPI.ts`, `lipSync.ts` |
| Stores | camelCase with `use` prefix | `useCanvasStore.ts`, `useOrchestratorStore.ts` |
| Components | PascalCase file | `VideoCanvas.tsx`, `ScriptsPanel.tsx` |
| Types | camelCase file | `orchestrator.ts`, `character3d.ts` |
| Hooks | camelCase with `use` prefix | `useKeyboardShortcuts.ts`, `useDialoguePlayback.ts` |
| Server routes | camelCase file | `hunyuanMotion.ts`, `meshy.ts` |
| API paths | kebab-case | `/api/ai-animation`, `/api/auto-rig` |
| Store exports | `useFeatureNameStore` | `useCanvasStore`, `useVoiceStore` |
| IDs | template literal with timestamp | `` `feature-${Date.now()}` `` |

## Zustand Store Pattern

Every store follows this exact structure:

```ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface FeatureState {
  // Data
  items: FeatureItem[]
  selectedId: string | null
  isLoading: boolean

  // Actions
  addItem: (item: FeatureItem) => void
  removeItem: (id: string) => void
  updateItem: (id: string, updates: Partial<FeatureItem>) => void
}

export const useFeatureStore = create<FeatureState>()(
  immer((set, get) => ({
    items: [],
    selectedId: null,
    isLoading: false,

    addItem: (item) => set((state) => {
      state.items.push(item)
    }),

    removeItem: (id) => set((state) => {
      state.items = state.items.filter((i) => i.id !== id)
    }),

    updateItem: (id, updates) => set((state) => {
      const item = state.items.find((i) => i.id === id)
      if (item) Object.assign(item, updates)
    }),
  }))
)
```

### Store with Undo/Redo (Zundo)

```ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'
import { temporal } from 'zundo'

interface TimelineState {
  tracks: Track[]
  // ... actions
}

export const useTimelineStore = create<TimelineState>()(
  temporal(
    immer((set, get) => ({
      tracks: [],
      // ... implementation
    })),
    { limit: 50 }  // undo history limit
  )
)

// Undo/redo hook export
export const useTimelineUndo = () => useTimelineStore.temporal.getState()
```

### Key Rules
- Always use `immer` middleware -- mutate `state` inside `set()`, never return new objects
- Cross-store reads: `useOtherStore.getState()` (not hooks, which cause subscription)
- Barrel export in `src/stores/index.ts` (except `useOrchestratorStore` -- too many deps)
- For undo/redo: wrap with `temporal` from `zundo` (see `useTimelineStore`)

## Component Patterns

### Panel Components (Left Sidebar) — Cinema Standard

All preset-browsing panels follow the Cinema panel standard. See `standardize-panel` skill for the complete template.

**Structure:** `flex flex-col h-full overflow-hidden` shell → animated tab bar → search + filter icon → scrollable body with thick rows → optional footer.

**Key elements:**
- Animated icon tab bar with flex-grow expansion (`flex: isActive ? 2 : 1`)
- Always-visible search input + `SlidersHorizontal` filter toggle
- `PanelCategoryTabs` behind filter icon (hidden by default)
- Blue dot indicator on filter icon when category != 'all'
- Thick rows: `w-full px-3 py-2.5 rounded-lg border` with name + description
- "None" row (Ban icon) as first item for disable/deselect
- Active state: `bg-[#4a7eff]/10 border-[#4a7eff]/30`
- No `PanelLayout` or `PanelSection` wrappers

```tsx
import { useState, useMemo } from 'react'
import { Search, SlidersHorizontal, Ban, FeatureIcon } from 'lucide-react'
import { PanelCategoryTabs } from '@/components/ui/panel-controls'
import { cn } from '@/lib/utils'
import { useFeatureStore } from '@/stores/useFeatureStore'

export function FeaturePanel() {
  const [search, setSearch] = useState('')
  const [filtersOpen, setFiltersOpen] = useState(false)
  // ... see standardize-panel skill for full template
  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* tab bar → search + filter → scrollable body → footer */}
    </div>
  )
}
```

- Tailwind CSS for all styling (dark theme base: `bg-zinc-900`, `text-zinc-100`)
- Icons from `lucide-react`
- Named export for panels (lazy-loaded by `LeftPanel.tsx`)
- **Do not use** `PanelLayout` or `PanelSection` for new panels — use the Cinema standard

### Canvas Layer Components

```tsx
import { usePlaybackStore } from '@/stores/usePlaybackStore'
import { useFeatureStore } from '@/stores/useFeatureStore'

export default function FeatureLayer() {
  const currentFrame = usePlaybackStore((s) => s.currentFrame)
  const items = useFeatureStore((s) => s.items)

  const visible = items.filter(
    (i) => i.visible && currentFrame >= i.startFrame && currentFrame <= i.endFrame
  )

  return (
    <>
      {visible.map((item) => (
        <div key={item.id} style={{ position: 'absolute', zIndex: item.zIndex }}>
          {/* Render item */}
        </div>
      ))}
    </>
  )
}
```

Canvas layers read from Zustand stores and subscribe to `currentFrame` for animation.

### Remotion Export Layers

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion'

interface Props {
  data: FeatureItem[]
}

export const RemotionFeatureLayer: React.FC<Props> = ({ data }) => {
  const frame = useCurrentFrame()

  const visible = data.filter(
    (i) => i.visible && frame >= i.startFrame && frame <= i.endFrame
  )

  return (
    <>
      {visible.map((item) => (
        <div key={item.id} style={{ position: 'absolute' }}>
          {/* Render for export */}
        </div>
      ))}
    </>
  )
}
```

Key rule: Remotion layers receive data as props from `VideoComposition.tsx`, never read stores directly.

## Tab Registration Pattern

### Step 1: Add sub-tab to `src/constants/tabGroups.ts`

```ts
// Inside the appropriate group's subTabs array:
{ id: 'my-feature', label: 'My Feature', icon: 'Wand2', description: 'Feature description' },
```

### Step 2: Add tab ID to `src/types/editor.ts` LeftPanelTab union

```ts
export type LeftPanelTab = 'character' | 'media' | /* ... */ | 'my-feature'
```

### Step 3: Add lazy import in `LeftPanel.tsx`

```ts
const MyFeaturePanel = lazy(() => import('@/components/panels/MyFeaturePanel').then(m => ({ default: m.MyFeaturePanel })))
```

### Step 4: Add rendering case in `PanelContent`

```ts
if (tab === 'my-feature') return <Suspense fallback={lazyFallback}><MyFeaturePanel /></Suspense>
```

### Step 5: Add icon to `ICON_MAP` in `LeftPanel.tsx` (if new icon)

```ts
const ICON_MAP: Record<string, LucideIcon> = {
  // ...existing
  Wand2,
}
```

## Service Patterns

### Client-Side Service (API Call)

```ts
import { withCreditGate } from './creditGate'

const API_BASE = '/api/feature-name'

export async function startGeneration(request: FeatureRequest): Promise<{ taskId: string }> {
  return withCreditGate('feature-operation', async () => {
    const res = await fetch(`${API_BASE}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    })

    if (!res.ok) {
      const error = await res.json().catch(() => ({ error: res.statusText }))
      throw new Error(error.error || 'Generation failed')
    }

    return res.json()
  })
}
```

### Server Route

```ts
import { Router, type Request, type Response } from 'express'

const router = Router()

router.post('/generate', async (req: Request, res: Response) => {
  try {
    const { prompt } = req.body
    if (!prompt) {
      res.status(400).json({ error: 'Missing required field: prompt' })
      return
    }
    // Process...
    res.json({ taskId, status: 'processing' })
  } catch (error) {
    console.error('[FeatureName] Error:', error)
    res.status(500).json({
      error: 'Operation failed',
      message: error instanceof Error ? error.message : 'Unknown error',
    })
  }
})

export default router
```

### Server Route Mounting (`server/index.ts`)

```ts
// In server/index.ts:
import myFeatureRoutes from './routes/myFeature'
app.use('/api/my-feature', requireAuth, aiRateLimiter, myFeatureRoutes)
```

Middleware order: `requireAuth` first (JWT validation), then `aiRateLimiter` (if AI endpoint).

## Import Style

```ts
// Type imports (use `import type` when only importing types)
import type { ClipPlan, OrchestratorSettings } from '@/types/orchestrator'

// Store imports
import { useCanvasStore } from '@/stores/useCanvasStore'

// Service imports
import { generateMotion } from '@/services/hunyuanMotion'

// React
import { useState, useCallback, useEffect } from 'react'

// Icons
import { Play, Pause, Settings } from 'lucide-react'

// Relative imports for same-directory
import { helperFunction } from './helper'
```

## Common Patterns

- **Credit gating**: All AI operations wrapped in `withCreditGate(operationType, fn)`
- **Async polling**: Long operations (Meshy, HunyuanMotion) use task-based polling with `pollUntilComplete` helpers
- **Abort signals**: Pipeline operations accept `AbortSignal` for cancellation
- **Progress callbacks**: `onProgress?: (step: string, progress: number) => void`
- **Error handling**: try/catch with `error instanceof Error ? error.message : 'Unknown error'`
- **Feature flags**: Conditional logic based on service availability (e.g., `hasElevenLabsService()`, `hasPixabayService()`)
- **Env vars**: Frontend uses `VITE_` prefix (`import.meta.env.VITE_GEMINI_API_KEY`), server uses `process.env`
- **Zustand selectors**: Always use selectors to avoid full-store subscription: `useStore((s) => s.field)`
- **Error boundary**: Canvas layers wrapped in `PanelErrorBoundary` for graceful failure
- **Lazy panel loading**: Use `React.lazy()` with `.then(m => ({ default: m.ComponentName }))` pattern for named exports
