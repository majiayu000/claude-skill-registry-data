---
name: add-feature
description: Guide for implementing a new feature in ProAnimate. Covers types, store, service, panel, canvas layer, Remotion layer, server route, and tab registration.
argument-hint: <feature-name>
---

# Add Feature to ProAnimate

Implement a complete feature end-to-end in the ProAnimate animation studio. This skill walks through every layer from types to UI to export.

## Steps

1. **Define types** in `src/types/<featureName>.ts`
   - Export interfaces for the feature's data model
   - Follow the pattern in `src/types/artCurves.ts` (simple interfaces with id, position, scale, opacity, rotation, zIndex, visible, startFrame, endFrame)
   - Re-export from `src/types/index.ts` if the types are used broadly

2. **Create Zustand store** in `src/stores/use<FeatureName>Store.ts`
   - Use `create` from `zustand` with `immer` middleware
   - Define state interface with data arrays and CRUD actions
   - Use `Date.now()` for unique IDs (e.g., `feature-${Date.now()}`)
   - Read timeline state via `useTimelineStore.getState()` for frame ranges
   - Add barrel export in `src/stores/index.ts`:
     ```ts
     export { use<FeatureName>Store } from './use<FeatureName>Store'
     ```

3. **Create service** in `src/services/<featureName>.ts`
   - Business logic, generation, processing, or API calls
   - Keep pure functions separate from store mutations
   - For AI features, call server endpoints via fetch to `/api/<feature-name>`

4. **Create panel** in `src/components/panels/<FeatureName>Panel.tsx`
   - React component that connects to the store
   - Use Tailwind CSS for styling (dark theme: `bg-zinc-900`, `text-zinc-100`)
   - Import store with `use<FeatureName>Store`
   - Follow GlassPanel pattern if applicable

5. **Create canvas layer** in `src/components/canvas/<FeatureName>Layer.tsx`
   - Render feature data on the main VideoCanvas
   - Read from store, filter by `visible` and frame range (`startFrame`/`endFrame`)
   - Use `usePlaybackStore` for current frame
   - Position with `position: 'absolute'` and layer's position/zIndex

6. **Create Remotion export layer** in `src/remotion/Remotion<FeatureName>Layer.tsx`
   - Use `useFrame()` from `@/engine` (NOT from 'remotion' directly)
   - Accept data as props (not from stores -- stores are read in VideoComposition and passed down)
   - Filter items by `visible`, `startFrame`, `endFrame` vs current frame
   - Register in `src/remotion/VideoComposition.tsx`:
     ```tsx
     import { Remotion<FeatureName>Layer } from './Remotion<FeatureName>Layer'
     // Then render inside the composition JSX
     <Remotion<FeatureName>Layer data={props.<featureName>Data} />
     ```

7. **Add server route** (if needed) in `server/routes/<featureName>.ts`
   - Create Express Router
   - Import `requireAuth` from `../middleware/supabaseAuth.js`
   - Mount in `server/index.ts`:
     ```ts
     import <featureName>Routes from './routes/<featureName>'
     app.use('/api/<feature-name>', requireAuth, <featureName>Routes)
     ```
   - Add `aiRateLimiter` middleware for AI/expensive endpoints

8. **Register tab in left panel**
   - Add tab ID to `LeftPanelBottomTab` union in `src/types/editor.ts`
   - Add sub-tab entry in `src/constants/tabGroups.ts` under the appropriate group:
     ```ts
     { id: '<tab-id>', label: 'Label', icon: 'IconName', description: 'Description' }
     ```
   - The panel component is rendered via lazy loading in the left panel layout based on the active tab ID

## Key Files

| Purpose | Path |
|---------|------|
| Types | `src/types/<featureName>.ts` |
| Store | `src/stores/use<FeatureName>Store.ts` |
| Store barrel | `src/stores/index.ts` |
| Service | `src/services/<featureName>.ts` |
| Panel | `src/components/panels/<FeatureName>Panel.tsx` |
| Canvas layer | `src/components/canvas/<FeatureName>Layer.tsx` |
| Remotion layer | `src/remotion/Remotion<FeatureName>Layer.tsx` |
| VideoComposition | `src/remotion/VideoComposition.tsx` |
| Server route | `server/routes/<featureName>.ts` |
| Server mount | `server/index.ts` |
| Tab registration | `src/constants/tabGroups.ts` |
| Tab types | `src/types/editor.ts` |

## Common Issues

- **Store not updating UI**: Ensure you use `immer` middleware and mutate `state` inside `set()` callbacks, not return new objects.
- **Canvas layer not visible**: Check that `zIndex` is set on the layer and does not conflict with other layers.
- **Remotion export blank**: Verify the data is passed as props through `VideoComposition.tsx`, not read from stores directly in the Remotion layer.
- **Tab not appearing**: Must add the tab ID to both `LeftPanelBottomTab` in `src/types/editor.ts` AND as a sub-tab in `src/constants/tabGroups.ts`.
- **Server route 404**: Ensure the route is mounted in `server/index.ts` and the Vite proxy (`/api` -> `localhost:3001`) is active.

## Example

See `ArtCurves` as a complete reference implementation:
- Types: `src/types/artCurves.ts`
- Store: `src/stores/useArtCurveStore.ts`
- Service: `src/services/artCurveGenerator.ts`
- Panel: `src/components/panels/ArtCurvesPanel.tsx`
- Canvas: `src/components/canvas/ArtCurveLayer.tsx`
- Remotion: `src/remotion/RemotionArtCurveLayer.tsx`
