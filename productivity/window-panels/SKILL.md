---
name: window-panels
description: "The WindowPanel component and Window Manager. Use when a window won't drag/resize/minimize, the tray is missing, window state doesn't persist, rendering `<WindowPanel>` on a page, or editing features/window-panels/** or windowManagerSlice.ts. NOT for opening/registering overlays (use overlay-system)."
---

# Window Panels — the WindowPanel component + Window Manager

This skill covers the **WindowPanel component primitive** and the runtime **Window Manager** (`windowManagerSlice` + `WindowTray`). For deep reference, see [`features/window-panels/FEATURE.md`](../../../features/window-panels/FEATURE.md).

**Opening / adding / registering / closing an overlay is NOT this skill.** That moved to a separate system (the two were merged in April 2026, causing a class of silent-render bugs, and split back apart in May 2026 — keep them separate) — read the [`overlay-system`](../overlay-system/SKILL.md) skill first for anything about `openOverlay`, openers, the `OverlayController`, or `lazyOverlay`. This skill is what the WindowPanel *is*, once something renders it.

If your task is "the window won't drag", "the tray isn't showing", "window state doesn't persist", "I want to render a `<WindowPanel>` directly on a page", "fix Window Manager focus / minimize-all", or "build a window component to spec" → this skill. If it's "open / dispatch / register an overlay" → overlay-system.

## Branches — read only when the task reaches them

- **Drag, resize, traffic lights, snap, full screen, pop-out** → read [drag-resize-popout.md](drag-resize-popout.md).
- **The tray dock or `windowManagerSlice`** (reveal, arrange, `windowsHidden`, pop-out state, silent-render guard) → read [tray-and-window-manager.md](tray-and-window-manager.md).
- **Saving / restoring window state, `onCollectData`, ephemeral / autosave, `?panels=` URL sync** → read [persistence.md](persistence.md).
- **How a window renders on mobile (`mobilePresentation`)** → read [mobile-presentation.md](mobile-presentation.md).

---

## Mental model

**`WindowPanel` is a leaf component.** It is a draggable / resizable / minimizable / maximizable / poppable frame. Render it like any other component:

- **Almost always** via a `lazyOverlay(...)` block in `features/overlays/OverlayController.tsx` (the overlay-system skill owns that path), or
- **Page-local** — a `<WindowPanel id="x" onClose={…}>` dropped on a page, behind your own `dynamic({ ssr: false })`.

**There is NO registry that renders windows.** Nothing iterates a list to mount your window. The legacy registry-driven path — `UnifiedOverlayController`, `OverlaySurface`, `windowRegistry.ts`, the "2-step registry recipe", `NEXT_PUBLIC_OVERLAYS_V2` — is **deleted**. If a doc or memory tells you to "add a registry entry to render a window," it is stale.

**On mount, a `<WindowPanel>` joins the runtime Window Manager** (`windowManagerSlice`). That is the only registration — by mounting, not by static declaration. Once joined, it participates in minimize-all, focus / z-index, the tray, arrange-all, persistence, and pop-out — **whether the overlay controller rendered it or a page did.** This is why the two systems are independent: the overlay controller is one renderer of windows, not the owner of "what is a window."

**`registry/windowRegistryMetadata.ts` is metadata, not a renderer.** It's a side-effect-free lookup (`getStaticEntryByOverlayId`) for an overlay's `mobilePresentation`, `urlSync.key`, `ephemeral`, `autosave`, `deprecated` flags. `WindowPanel` reads it to resolve mobile presentation + URL sync; it never drives rendering.

---

## The SLOTS contract — the heart of building a window

**The body is content ONLY. Every piece of chrome — header, footer, sidebar, secondary panel — is a `WindowPanel` prop slot, never body JSX.** Never hand-roll a header bar, a footer row, or a side rail inside `children`. Pass the slot. Reference consumers: [`windows/notes/NotesWindow.tsx`](../../../features/window-panels/windows/notes/NotesWindow.tsx), [`windows/FeedbackWindow.tsx`](../../../features/window-panels/windows/FeedbackWindow.tsx).

**Canonical body class:** `bodyClassName="flex min-h-0 flex-1 flex-col overflow-hidden p-0"`.

| Slot | Props (defaults) | Contract |
|---|---|---|
| **Body** | `children`, `bodyClassName` | Content only. Use the canonical class above. |
| **Header** | `title` (string) / `titleNode` (rich JSX, wins over `title`); `actionsLeft`; `actionsRight` | Title is **absolute-centered** across the full header width. Keep action clusters **compact** — wide ones reach the centered title and overlap it (known rough edge). `actions` is **deprecated** → maps to `actionsRight`. Traffic lights + sidebar toggle render on the left automatically; don't add your own. |
| **Footer** | `footer` (single flex row) **OR** `footerLeft` / `footerCenter` / `footerRight` (zoned); `footerVariant` (`"bar"` default / `"rich"`) | Renders only when content is passed. `footer` wins over the zoned trio. Default `footerVariant="bar"` hardcodes compact metadata-bar styling (`text-xs`, tiny buttons/icons) that **crushes a rich composer** — pass **`footerVariant="rich"`** for a multi-row input / composer (`SmartAgentInput`): it drops the compact descendant selectors + `bg-muted/40`, leaving `shrink-0 border-t`. Reference: `windows/multi-file-smart-code-editor`. |
| **Sidebar (left)** | `sidebar`; `sidebarDefaultSize` (200); `sidebarMinSize` (100); `defaultSidebarOpen` (true); `sidebarClassName` | Resizable + collapsible; a toggle appears by the traffic lights. **`sidebarExpandsWindow` is a footgun** — it mutates the window rect on every toggle (a second sizing path that fights drag/snap). Leave it `false`. |
| **Secondary panel (right)** | `secondaryPanel`; `secondaryPanelOpen` (true when `secondaryPanel` set); `secondaryPanelDefaultSize` (360); `secondaryPanelMinSize` (240); `secondaryPanelClassName` | Canonical home for a **history / inspector / details pane** that belongs to the window, not the body. Resizable, mirrors the sidebar. **Desktop only** — no built-in mobile route; the consumer handles mobile (a Drawer). Reference: `features/notes` `NoteHistoryPane`. |

**The close-binding contract (type-enforced).** Every `WindowPanel` MUST declare how it closes — exactly one of:
- **`overlayId`** (overlay-managed) — closing is handled by the persistence layer dispatching `closeOverlay({ overlayId })`; the `OverlayController` then unmounts it. `onClose` becomes an **optional** extra-cleanup hook.
- **`onClose`** (inline-managed) — required when the panel lives directly on a page with no overlay slice; nothing else closes it.

Passing **neither is a compile error.** Do not relax `overlayId?` / `onClose?` back to both-optional — the discriminated union is what made the dead-X-button bug class structurally impossible.

---

## The composition-root pattern — how to build a window right

A window component is a **thin composition root**: it hoists shared state once, then maps independent units onto the slots. The body holds only content.

1. **Hoist shared state into one `use<Feature>` hook at the window root.** State a footer and the body both need lives at the root, not inside the body — slots are siblings of the body, so a hook buried in the body can't feed them. (`FeedbackWindow` → `useFeedbackForm`; `NotesWindow` owns the instance lifecycle at the root.)
2. **Each unit takes an `id` and reads Redux** — zero prop drilling. The sidebar, header controls, footer, and history pane each subscribe to the slice for the instance id; you pass an id, not data.
3. **Map units onto slots; body is content-only.**

```tsx
"use client";
import { WindowPanel, type WindowPanelProps } from "@/features/window-panels/WindowPanel";

export function MyFeatureWindow({ id = "my-feature-window", onClose, ...rest }: Props) {
  const state = useMyFeature();           // 1 — all shared state hoisted here

  return (
    <WindowPanel
      id={id}
      overlayId="myFeatureWindow"         // overlay-managed close (or use onClose for inline)
      title="My Feature"
      width={640} height={480}
      minWidth={380} minHeight={280}
      bodyClassName="flex min-h-0 flex-1 flex-col overflow-hidden p-0"
      actionsRight={<MyFeatureControls id={id} />}   // unit reads Redux by id
      sidebar={<MyFeatureSidebar id={id} />}
      footer={<MyFeatureFooter state={state} />}     // sibling of body — needs hoisted state
      secondaryPanel={state.inspectorOpen ? <MyFeatureInspector id={id} /> : undefined}
      onClose={onClose}
      {...rest}
    >
      <MyFeatureBody id={id} />            {/* content ONLY */}
    </WindowPanel>
  );
}
```

Route-shared units (a component used both inside a window and on a plain page) drop INTO a slot as content — they take **no `WindowPanel` import**, so a route rendering them never drags the window stack into its bundle.

---

## 🚨 Bundle invariant — non-negotiable

**`WindowPanel`, the `OverlayController`, and every `windows/**/*Window.tsx` MUST stay behind the lazy boundary** — loaded ONLY via `lazyOverlay(() => import(...))` or `dynamic(..., { ssr: false })`. **NEVER static-import any of them from a route, layout, provider, or boot module.** One static import collapses 100+ lazy overlay chunks into that route's bundle.

- **Runtime guard:** `assertLazyLoaded("features/window-panels/WindowPanel.tsx")` runs at `WindowPanel.tsx` module top ([`utils/lazy-bundle-guard.ts`](../../../features/window-panels/utils/lazy-bundle-guard.ts)). If the file is parsed during boot it screams a red `[WINDOW-PANELS BUNDLE LEAK]` banner naming the eager-import chain (leaking file = top frame). Deduped per session via `window.__WP_LEAK_REPORTED__`.
- **Never nest `ssr:false` boundaries down one render path** — one boundary covers everything beneath it; a second is a waterfall for zero gain.
- **Need a utility from a window component?** Lift it into a shared module (e.g. `features/window-panels/utils/`). Never import the window to reach the util.
- `scripts/check-bundle-size.ts` gates per-route growth at +2 KB; the runtime guard catches leaks it misses.

**Read the [`code-splitting`](../code-splitting/SKILL.md) skill** before adding any `import` of a window-panel file.

---

## Drag / resize / minimize / maximize / pop-out

Every `<WindowPanel>` gets drag, resize, min/max, snap, and pop-out for free. **Working on that behavior → read [drag-resize-popout.md](drag-resize-popout.md).**

---

## The tray (WindowTray)

Mount exactly one `<WindowTray />` and one `<WindowTraySync />`, high in the tree. **Tray work → read [tray-and-window-manager.md](tray-and-window-manager.md).**

---

## Window Manager slice (`lib/redux/slices/windowManagerSlice.ts`)

Runtime registry of mounted windows — a window joins on mount and leaves on unmount. **Slice work (reveal, arrange, `windowsHidden`, pop-out state, silent-render guard) → read [tray-and-window-manager.md](tray-and-window-manager.md).**

---

## Persistence (local-first workspace cache + URL)

Local-first and tab-scoped; nothing window-related is stored server-side. **Save/restore, `onCollectData`, ephemeral/autosave, or `?panels=` URL sync → read [persistence.md](persistence.md).**

---

## Mobile presentation

On mobile, `WindowPanel` routes by the overlay's `mobilePresentation`. **Choosing or debugging mobile rendering → read [mobile-presentation.md](mobile-presentation.md).**

---

## Common pitfalls

1. **Hand-rolling chrome in the body.** A header bar / footer row / side rail inside `children` is the #1 mistake. Use the slot. Body is content only.
2. **`sidebarExpandsWindow`.** Mutates the rect on every toggle — a second sizing path that fights drag/snap. Leave it `false`.
3. **State buried in the body that a footer/sidebar slot needs.** Slots are siblings of the body. Hoist shared state into a `use<Feature>` hook at the window root.
4. **Static-importing a `*Window.tsx` or `WindowPanel` from a route/provider.** Bundle leak — the runtime guard screams. Always lazy.
5. **Forgetting the close binding.** Pass `overlayId` (overlay-managed) or `onClose` (inline). Neither = compile error; that's intentional.
6. **Multiple `<WindowTray>` / `<WindowTraySync>` mounts.** Exactly one of each, high in the tree, outside any `transform`/`overflow` ancestor.
7. **Reaching for a "registry entry to render a window."** Gone. Windows render via `lazyOverlay` in `OverlayController` (overlay-system skill) or a page-local `dynamic`.

---

## Key files

| Path | Role |
|---|---|
| `features/window-panels/WindowPanel.tsx` | The primitive: slots, drag/resize/min/max, persistence binding, URL sync, mobile routing, popout. |
| `features/window-panels/hooks/useWindowPanel.ts` | Pointer-driven move/resize + Redux window registration. |
| `features/window-panels/WindowTray.tsx` / `WindowTraySync.tsx` | Minimized-window dock + debounced viewport sync. Mount one of each. |
| `features/window-panels/WindowPersistenceManager.tsx` | local workspace hydration context; rect clamping; idle GC. |
| `features/window-panels/registry/windowRegistryMetadata.ts` | Side-effect-free metadata lookup (`getStaticEntryByOverlayId`) — NOT a renderer. |
| `features/window-panels/utils/lazy-bundle-guard.ts` | `assertLazyLoaded` bundle-leak guard. |
| `features/window-panels/popout/**` | Pop-out lifecycle (`usePopoutWindow`, `usePopoutControl`, portal, feature detection). |
| `features/window-panels/windows/notes/NotesWindow.tsx` | Composition-root reference (sidebar + actions + footer + secondary panel). |
| `features/window-panels/windows/FeedbackWindow.tsx` | Composition-root reference (hoisted `useFeedbackForm` → footer slots). |
| `lib/redux/slices/windowManagerSlice.ts` | Runtime Window Manager: geometry, z-index, tray, popout, `revealWindow`, `arrangeActiveWindows`. |
| `features/overlays/OverlayController.tsx` | Where windows are rendered as overlays (via `lazyOverlay`) — **overlay-system skill**. |
| `features/window-panels/FEATURE.md` | Deep reference. |

---

## Checklist (before submitting)

- [ ] Body is content only — header/footer/sidebar/secondary are slots, not body JSX.
- [ ] `bodyClassName="flex min-h-0 flex-1 flex-col overflow-hidden p-0"`.
- [ ] Shared state hoisted into a `use<Feature>` hook at the window root; units read Redux by id.
- [ ] Close binding declared (`overlayId` OR `onClose`).
- [ ] `sidebarExpandsWindow` left `false`.
- [ ] No static import of `WindowPanel` / `*Window.tsx` outside a lazy boundary; no `[WINDOW-PANELS BUNDLE LEAK]` banner at boot.
- [ ] If `onCollectData` is set, its return keys are stable and `useCallback`-wrapped.
- [ ] If the overlay has `urlSync.key`, a matching hydrator exists in `initUrlHydration.ts`.
- [ ] `pnpm type-check` clean for `features/window-panels/**`.
