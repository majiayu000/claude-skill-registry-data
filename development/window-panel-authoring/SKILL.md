---
name: window-panel-authoring
description: "Recipe for creating or changing a floating window panel. Use when adding a window, editing a window component, adding persistence, onCollectData, or ephemeral mode, wiring the Tools grid, or a window fails to restore after reload. NOT for WindowPanel drag/resize/tray internals (use window-panels)."
---

# Window Panel Authoring

## Quick Orientation

Every floating window is a `WindowPanel` shell rendered by ONE hand-maintained controller, `features/overlays/OverlayController.tsx`. **No registry renders windows** — `windowRegistry.ts` is deleted; any doc that says "add a registry entry to render a window" is stale. Persistence is a **local-first, tab-scoped workspace** (localStorage mirror + IndexedDB, `features/window-panels/persistence/`, coordinated by `WindowPersistenceManager`); nothing window-related is stored server-side (the `window_sessions` table was dropped 2026-08-12). Slots / drag / tray internals → `window-panels` skill. Openers / controller / catalogue rules → `overlay-system` skill.

If this window is an agent-aware surface, invoke `surface-authoring` and its overlay-surface reference for the manifest, scoped registration receipt, and nested runtime provider. A window resident never inherits ambient surface values; an outside helper may receive an approved task-appropriate snapshot under its documented integration contract.

**Key files:**

| File | When you touch it |
|------|-------------------|
| `features/overlays/catalogue.ts` | Every new overlay: its key IS the id (`OverlayId = keyof typeof OVERLAY_CATALOGUE`) + `{ label, instanceMode, isWindow }` |
| `features/window-panels/registry/windowRegistryMetadata.ts` | Every new window; any `defaultData` / `preservation` change |
| `features/window-panels/windows/[<feature>/]MyFeatureWindow.tsx` | New window component |
| `features/overlays/OverlayController.tsx` | Mount: `lazyOverlay` import + selectors + gated block |
| `features/overlays/openers/<overlayId>.tsx` | Typed `useOpenX` hook + `XController` |
| `features/window-panels/tools-grid/toolsGridTiles.ts` | Optional Tools-grid tile |
| `features/window-panels/url-sync/initUrlHydration.ts` | Optional `?panels=` deep-link |

---

## Step-by-Step: Creating a New Window

A window is registered **at every boundary, by hand** (no codegen): catalogue entry (the id) → metadata → component → controller → opener, then the optional tile and hydrator.

### 1. Add the catalogue entry — it defines the id

In `features/overlays/catalogue.ts`: `myFeatureWindow: { label: "My Feature", instanceMode: "singleton", isWindow: true },`. The key IS the overlay id — the `OverlayId` union is `keyof typeof OVERLAY_CATALOGUE`, so every opener and `openOverlay` call narrows at compile time. There is no second id list.

### 2. Declare static metadata in `windowRegistryMetadata.ts`

```ts
// features/window-panels/registry/windowRegistryMetadata.ts
{
  slug: "my-feature-window",       // kebab-case; URL / diagnostic identity
  overlayId: "myFeatureWindow",    // camelCase; the exact catalogue key (step 1)
  kind: "window",
  label: "My Feature",
  defaultData: {
    selectedId: null,
    search: "",
  },
  mobilePresentation: "drawer",    // required for kind "window": fullscreen | drawer | card | hidden
  // ephemeral: true,                            // never enters the local workspace
  // preservation: { dataKeys: ["selectedId"] }, // opt in to refresh restore (default-deny)
  // instanceMode: "multi",
  // urlSync: { key: "my_feature" },             // needs a hydrator (step 7)
},
```

Rules:
- `slug` and `overlayId` are each unique across the registry.
- `overlayId` is the key every opener and `openOverlay({ overlayId })` uses.
- `defaultData` documents every key `onCollectData()` will ever return.
- **Component-free** — never import component code here; this file is safe in boot code only because it has none.

### 3. Create `windows/[<feature>/]MyFeatureWindow.tsx`

```tsx
"use client";
import { useState } from "react";
import { WindowPanel } from "@/features/window-panels/WindowPanel";
import { MyFeatureBody } from "@/features/my-feature/components/MyFeatureBody";

interface MyFeatureWindowProps {
  isOpen: boolean;
  onClose: () => void;
  initialSelectedId?: string | null;   // from overlay data, wired by the controller block
}

export default function MyFeatureWindow({ isOpen, onClose, initialSelectedId }: MyFeatureWindowProps) {
  if (!isOpen) return null;
  return <MyFeatureWindowInner onClose={onClose} initialSelectedId={initialSelectedId} />;
}

function MyFeatureWindowInner({ onClose, initialSelectedId }: Omit<MyFeatureWindowProps, "isOpen">) {
  const [selectedId, setSelectedId] = useState<string | null>(initialSelectedId ?? null);

  const collectData = (): Record<string, unknown> => ({ selectedId, search: "" });

  return (
    <WindowPanel
      title="My Feature"
      id="my-feature-window"          // stable id — key in windowManagerSlice
      minWidth={380}
      minHeight={280}
      width={560}
      height={440}
      position="center"
      onClose={onClose}
      overlayId="myFeatureWindow"     // identical to the catalogue key + metadata
      onCollectData={collectData}
      bodyClassName="flex min-h-0 flex-1 flex-col overflow-hidden p-0"
    >
      <MyFeatureBody selectedId={selectedId} onSelect={setSelectedId} />
    </WindowPanel>
  );
}
```

Critical rules:
- Outer guard `if (!isOpen) return null` — inner component does the real work.
- `id` must be stable (not a random UUID; omitted → `useId()`) — it is the Redux key for geometry.
- `overlayId` must exactly match the catalogue key and the metadata `overlayId`. It is also the close binding: `overlayId` or `onClose` is required (type-enforced).
- `instanceMode: "multi"` → also pass `overlayInstanceId`, or close and restore cannot find the exact instance.
- `onCollectData` must return **all** keys that appear in `defaultData`, read from live state. No manual `useCallback` — the React Compiler memoizes it.
- Body is content only; header / footer / sidebar are `WindowPanel` slots → `window-panels` skill.

### 4. Mount in `features/overlays/OverlayController.tsx`

Three hand edits. Props are wired **by name** — a `{...spread}` is an ESLint error.

```ts
// 1 — lazy import near the other window imports
const MyFeatureWindow = lazyOverlay(
  () => import("@/features/window-panels/windows/my-feature/MyFeatureWindow"),
  { ssr: false },
);
```

```ts
// 2 — one entry in `isOpenById`, one in `dataById`
myFeatureWindow: useAppSelector((s) => selectIsOverlayOpen(s, "myFeatureWindow")),
// …
myFeatureWindow: useAppSelector((s) => selectOverlayData(s, "myFeatureWindow")),
```

```tsx
{/* 3 — gated render block; NEVER render ungated */}
{/* myFeatureWindow */}
{(() => {
  const isOpen = isOpenById.myFeatureWindow;
  const data = dataById.myFeatureWindow as Record<string, unknown> | null | undefined;
  if (!isOpen) return null;
  return (
    <MyFeatureWindow
      isOpen
      onClose={() => dispatch(closeOverlay({ overlayId: "myFeatureWindow" }))}
      initialSelectedId={typeof data?.selectedId === "string" ? data.selectedId : null}
    />
  );
})()}
```

### 5. Add the opener

- `features/overlays/openers/myFeatureWindow.tsx` — copy an existing opener (`feedbackDialog.tsx`): `useOpenMyFeatureWindow()` + `<MyFeatureWindowController />`. New code opens the window through the opener, never a raw `dispatch(openOverlay(...))`.

### 6. (Optional) Tools grid — `tools-grid/toolsGridTiles.ts`

Tiles are declarative; `ToolsGrid.tsx` reads them and opens the overlay. Never add a tile inside `components/SidebarWindowToggle.tsx`.

```ts
{
  id: "tile.my-feature",
  label: "My Feature",
  icon: MyFeatureIcon,             // Lucide icon component
  category: "general",
  overlayId: "myFeatureWindow",
  // seedData: (ctx) => ({ selectedId: null }),
},
```

### 7. (Optional) URL hydrator — `url-sync/initUrlHydration.ts`

Only needed if you want `?panels=my_feature` to reopen the window. The hydrator and the metadata `urlSync.key` (step 2) come as a pair: a hydrator without the key opens from the URL but never writes back.

```ts
registerPanelHydrator("my_feature", (dispatch, id) => {
  dispatch(openOverlay({ overlayId: "myFeatureWindow" }));   // multi-instance: add instanceId: id
});
```

---

## Modifying an Existing Window

When you add/remove keys from a window's content state:

1. Update `defaultData` in `windowRegistryMetadata.ts` — add new keys with null/empty defaults; remove stale ones. A preserved window: update `preservation.dataKeys` too, or the new key is silently dropped from storage.
2. Update `onCollectData` in the window component to return all current keys.
3. Update the inner component to read new keys from `initialXxx` props.
4. Props changed → update the gated block in `OverlayController.tsx` AND the opener's `Open…Options` interface.

---

## Persistence Contract

**Default-deny.** A window survives a refresh only when its metadata declares `preservation.dataKeys` and is not `ephemeral` (multi-instance: plus `overlayInstanceId`). Every other window simply closes on reload. The opted-in list and full lifecycle: `features/window-panels/FEATURE.md` § Persistence.

For a preserved window, `WindowPanel` captures chrome automatically when `overlayId` is set. The child only supplies content via `onCollectData`.

**What `panelState` captures (automatic):**
- `rect`: `{ x, y, width, height }`
- `windowState`: `"windowed" | "maximized" | "minimized"`
- `sidebarOpen`: boolean
- `zIndex`: number

**What `data` captures (child's responsibility):**
- Whatever `onCollectData()` returns, merged over the launch data and **filtered to `preservation.dataKeys`** — JSON-serializable, ≤ `maxDataBytes` (32 KiB default). Functions, callbacks, and blobs never reach storage.

**Save triggers:**
- Any `windowManagerSlice` change (move, resize, minimize, sidebar toggle) → workspace save, debounced 250 ms.
- `onCollectData` or launch data changes → semantic data re-staged automatically; minimize collects and saves too.
- Explicit: user clicks "Save window state" in the green traffic-light dropdown.
- `pagehide` → synchronous localStorage flush.

**On close:** `closeOverlay` (and toggle-close / close-all) tombstones the session and the close middleware flushes localStorage synchronously, so the window doesn't reopen next load — even when closed mid-hydration.

**On page load:** `WindowPersistenceManager` reads the tab's identity-scoped workspace (localStorage mirror, then IndexedDB), clamps rects to the viewport, stages each session, and dispatches `openOverlay`; `registerWindow` consumes the staged state when the window mounts.

---

## Ephemeral Windows

Use `ephemeral: true` in the metadata for windows that must NOT persist:
- Debug/dev tool windows
- One-shot dialogs (file upload, confirmation flows)
- Windows whose state cannot be serialized (file blobs, live streams, callback-group windows)

Ephemeral windows never enter the workspace and never restore on reload. The "Save window state" item still renders for every `overlayId` window — without `preservation` it does nothing.

---

## Sidebar Layout Rules

```tsx
// Correct sidebar root
<div className="flex flex-col min-h-0 h-full">
  <div className="px-2 py-1 border-b text-xs font-medium shrink-0">Header</div>
  <div className="flex-1 min-h-0 p-1.5 space-y-1">
    {items.map(item => <Item key={item.id} />)}
  </div>
</div>
```

- DO use `h-full min-h-0 flex flex-col` on root.
- DO NOT set `overflow-y-auto` on root — `WindowPanel` handles it.
- DO NOT use `shrink-0` on the root element.

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| `overlayId` in component ≠ catalogue key / metadata `overlayId` | Type error, or the window reads another overlay's mobile / restore metadata | Make them identical |
| `onCollectData` returns stale values | Saved data has old values | Read live state in the collector, never a cached copy |
| Missing gated block in `OverlayController.tsx` | Window never renders | Add `lazyOverlay` import + selectors + gated block |
| Missing metadata entry in `windowRegistryMetadata.ts` | No mobile presentation, URL sync, or restore | Add the entry (`kind`, `mobilePresentation`) |
| No `preservation` on the metadata entry | Window doesn't reopen after refresh; "Save window state" does nothing | Declare `preservation.dataKeys` |
| Multi-instance window without `overlayInstanceId` | Close logs `Cannot close multi-instance…`; no restore | Pass `overlayInstanceId` |
| Random `id` passed to `WindowPanel` | Geometry lost on re-render | Use stable string like `"my-feature-window"` |
| `ephemeral: true` but window needs restore | Window doesn't reopen | Remove `ephemeral`, declare `preservation` |

---

## Additional Resources

- Deep reference (registry fields, persistence lifecycle, URL sync, Tools grid): `features/window-panels/FEATURE.md`
- Static metadata: `features/window-panels/registry/windowRegistryMetadata.ts` (types: `windowRegistryTypes.ts`)
- Local workspace store: `features/window-panels/persistence/localWindowSessionStore.ts` (+ `windowSessionSerialization.ts`, `windowPersistenceCloseMiddleware.ts`)
- Persistence coordinator: `features/window-panels/WindowPersistenceManager.tsx` → `WindowPersistenceCore.tsx`
- Openers, controller, catalogue: `overlay-system` skill · slots, drag, tray: `window-panels` skill
