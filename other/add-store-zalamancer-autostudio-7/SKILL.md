---
name: add-store
description: Add a new Zustand store to ProAnimate with Immer middleware and Zundo undo/redo support. Includes TypeScript types and barrel export.
argument-hint: <store-name>
---

# Add Zustand Store to ProAnimate

Create a new Zustand store following the project's conventions: Immer middleware for immutable updates and optional Zundo temporal middleware for undo/redo.

## Steps

1. **Create the store file** at `src/stores/use<Name>Store.ts`

   Basic store with Immer:
   ```ts
   import { create } from 'zustand'
   import { immer } from 'zustand/middleware/immer'

   interface MyItem {
     id: string
     name: string
     // ... item properties
     position: { x: number; y: number }
     visible: boolean
     startFrame: number
     endFrame: number
   }

   interface MyFeatureState {
     items: MyItem[]
     selectedId: string | null

     // Actions
     addItem: (item: Omit<MyItem, 'id'>) => void
     removeItem: (id: string) => void
     updateItem: (id: string, updates: Partial<MyItem>) => void
     setSelectedId: (id: string | null) => void
     clearAll: () => void
   }

   export const useMyFeatureStore = create<MyFeatureState>()(
     immer((set) => ({
       items: [],
       selectedId: null,

       addItem: (item) =>
         set((state) => {
           const id = `my-feature-${Date.now()}`
           state.items.push({ ...item, id })
           state.selectedId = id
         }),

       removeItem: (id) =>
         set((state) => {
           state.items = state.items.filter((i) => i.id !== id)
           if (state.selectedId === id) {
             state.selectedId = null
           }
         }),

       updateItem: (id, updates) =>
         set((state) => {
           const item = state.items.find((i) => i.id === id)
           if (item) Object.assign(item, updates)
         }),

       setSelectedId: (id) =>
         set((state) => {
           state.selectedId = id
         }),

       clearAll: () =>
         set((state) => {
           state.items = []
           state.selectedId = null
         }),
     }))
   )
   ```

2. **Add Zundo undo/redo** (for stores that track user-editable state):

   ```ts
   import { create } from 'zustand'
   import { immer } from 'zustand/middleware/immer'
   import { temporal } from 'zundo'

   export const useMyFeatureStore = create<MyFeatureState>()(
     temporal(
       immer((set) => ({
         // ... same as above
       })),
       { limit: 50 }
     )
   )

   // Export undo hook
   export const useMyFeatureUndo = () => useMyFeatureStore.temporal.getState()
   ```

3. **Add barrel export** in `src/stores/index.ts`:

   ```ts
   export { useMyFeatureStore } from './useMyFeatureStore'
   ```

   **Exception**: If the store imports heavy services (like the orchestrator store), do NOT add it to the barrel export. Instead, import it directly where needed to avoid eager loading. Add a comment explaining why:
   ```ts
   // NOTE: useMyFeatureStore is intentionally NOT re-exported from the barrel.
   // It imports heavyService.ts which pulls in many dependencies.
   // Components import it directly: import { useMyFeatureStore } from '@/stores/useMyFeatureStore'
   ```

4. **Access other stores** from within actions:

   ```ts
   import { useTimelineStore } from './useTimelineStore'
   import { usePlaybackStore } from './usePlaybackStore'

   // Inside an action:
   addItem: () =>
     set((state) => {
       const { totalFrames } = useTimelineStore.getState()
       const { fps } = usePlaybackStore.getState()
       // Use these values...
     }),
   ```

## Key Files

| Purpose | Path |
|---------|------|
| Store directory | `src/stores/` |
| Barrel export | `src/stores/index.ts` |
| Timeline store (for frame data) | `src/stores/useTimelineStore.ts` |
| Playback store (for fps/frame) | `src/stores/usePlaybackStore.ts` |
| Canvas store (for dimensions) | `src/stores/useCanvasStore.ts` |

## Store Conventions

- **ID generation**: Use `feature-${Date.now()}` for unique IDs
- **Immer mutations**: Always mutate `state` directly inside `set()` -- Immer handles immutability
- **Cross-store reads**: Use `otherStore.getState()` to read from other stores (never subscribe inside actions)
- **No async in set()**: For async operations, do the async work first, then call `set()` with the results
- **Frame ranges**: Items displayed on canvas typically have `startFrame` and `endFrame` properties. Initialize `endFrame` from `useTimelineStore.getState().totalFrames`

## Common Issues

- **Stale state in callbacks**: Use `useStore.getState()` inside event handlers or async callbacks, not the hook return value.
- **Immer not working**: Ensure you wrap with `immer()` middleware. Without it, you must return new objects from `set()`.
- **Circular imports**: If store A imports store B and vice versa, use `getState()` inside actions (lazy access) instead of top-level imports of the store instance.
- **Barrel export causes slowdown**: If the store imports heavy modules, skip the barrel export and import directly to avoid eager loading at app startup.

## Example

Reference stores:
- Simple: `src/stores/useArtCurveStore.ts` -- Immer, CRUD for compositions, references `useTimelineStore`
- With timeline: `src/stores/useShapeStore.ts` -- Shapes with position, frame ranges
- Complex: `src/stores/useMultiCharacterStore.ts` -- Multi-character dialogue with cross-store dependencies
