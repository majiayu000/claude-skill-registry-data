---
name: add-panel
description: Add a new editor panel to ProAnimate's left sidebar. Covers panel component creation, tab registration in tabGroups.ts, and EditorLayout integration.
argument-hint: <panel-name>
---

# Add Panel to ProAnimate

Add a new panel to the left sidebar editor. Panels are organized into tab groups (Characters, Library, Image, Video, Audio, Edit, Script, Design, Publish, Layers).

## Steps

1. **Add the tab ID to the type union** in `src/types/editor.ts`

   Add your new tab to `LeftPanelBottomTab`:
   ```ts
   export type LeftPanelBottomTab =
     | 'character'
     | ...
     | 'my-feature'  // Add here
   ```

2. **Register the tab in a group** in `src/constants/tabGroups.ts`

   Add a sub-tab entry to the appropriate group in the `TAB_GROUPS` array:
   ```ts
   {
     id: 'design',  // or 'create', 'media', 'image', 'video', 'audio', 'edit', 'script', 'publish'
     label: 'Design',
     subTabs: [
       // ... existing tabs
       { id: 'my-feature', label: 'My Feature', icon: 'Sparkles', description: 'What this panel does' },
     ],
   },
   ```

   Available icon names come from `lucide-react` (e.g., `Sparkles`, `Pen`, `Music`, `Film`, `Image`, `Type`, `Palette`, `Camera`, `Mic`, `ScrollText`, `TrendingUp`, `Calendar`, `Search`, `Copy`, `Layers`, `Database`, `Component`, `Wand2`, `ScanFace`, `Clapperboard`, `PenTool`, `Flame`, `AudioLines`, `FileText`, `Subtitles`, `MessageCircle`, `ArrowRightLeft`, `FileVideo`, `Users`, `Library`).

3. **Create the panel component** in `src/components/panels/<MyFeature>Panel.tsx`

   ```tsx
   import { use<MyFeature>Store } from '@/stores/use<MyFeature>Store'

   export function MyFeaturePanel() {
     const { items, addItem } = use<MyFeature>Store()

     return (
       <div className="flex flex-col gap-3 p-3">
         <div className="flex items-center justify-between">
           <h3 className="text-sm font-medium text-zinc-200">My Feature</h3>
           <button
             onClick={() => addItem()}
             className="rounded bg-indigo-600 px-3 py-1 text-xs text-white hover:bg-indigo-500"
           >
             Add
           </button>
         </div>
         {/* Panel content */}
       </div>
     )
   }
   ```

4. **Connect panel to the left panel layout**

   The left panel renders panels based on `leftPanelActiveTab` from `useEditorStore`. Add a lazy-loaded case for your tab ID in the panel router/switch in the LeftPanel component. The pattern is:
   ```tsx
   case 'my-feature':
     return <MyFeaturePanel />
   ```

5. **Optionally update `GROUP_DEFAULT_TAB`** in `src/constants/tabGroups.ts`

   If your tab should be the default when clicking its group icon:
   ```ts
   export const GROUP_DEFAULT_TAB: Record<TabGroupId, LeftPanelTab> = {
     design: 'my-feature',  // Change the default
     // ...
   }
   ```

## Key Files

| Purpose | Path |
|---------|------|
| Tab type union | `src/types/editor.ts` (`LeftPanelBottomTab`) |
| Tab group registration | `src/constants/tabGroups.ts` (`TAB_GROUPS` array) |
| Group defaults | `src/constants/tabGroups.ts` (`GROUP_DEFAULT_TAB`) |
| Absorbed/redirect map | `src/constants/tabGroups.ts` (`ABSORBED_TAB_REDIRECT`) |
| Editor store | `src/stores/useEditorStore.ts` |
| Panel components | `src/components/panels/` |
| Left panel layout | `src/components/layout/LeftPanel/` |

## Tab Group IDs

| Group ID | Label | Purpose |
|----------|-------|---------|
| `create` | Characters | Character creation and management |
| `media` | Library | Media assets and stock library |
| `image` | Image | Image generation and manipulation |
| `video` | Video | Video generation, cinema, B-roll |
| `audio` | Audio | Voice, music, sound effects |
| `edit` | Edit | Mixed media, anim style, transitions |
| `script` | Script | Scripts, dialogue, transcripts, captions |
| `design` | Design | Text, transitions, animations, camera, whiteboard, brand |
| `publish` | Publish | Publishing, scheduling, trends, virality |
| `layers` | Layers | Layer tree (no sub-tabs) |

## Common Issues

- **Tab not appearing**: Must be added to both `LeftPanelBottomTab` type in `src/types/editor.ts` AND as a sub-tab in `TAB_GROUPS` in `src/constants/tabGroups.ts`. Missing either one will cause TypeScript errors or invisible tabs.
- **Groups with more than 3 tabs**: Groups with more sub-tabs than `CARD_GRID_THRESHOLD` (3) automatically use card grid navigation instead of a tab bar.
- **Redirected tabs**: If a tab was absorbed into another, add it to `ABSORBED_TAB_REDIRECT` so old references redirect properly.
- **Hidden tabs**: Some tabs (like `rig-editor`, `rig-editor-3d`) are not in `TAB_GROUPS.subTabs` but mapped in `TAB_TO_GROUP` below the array for canvas mode switching.

## Example

To add a "Particles" panel under the Design group:

1. Add `'particles'` to `LeftPanelBottomTab` in `src/types/editor.ts`
2. Add to the `design` group in `src/constants/tabGroups.ts`:
   ```ts
   { id: 'particles', label: 'Particles', icon: 'Sparkles', description: 'Particle effect generator' }
   ```
3. Create `src/components/panels/ParticlesPanel.tsx`
4. Add the case in the left panel switch to render `<ParticlesPanel />`
