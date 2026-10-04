---
name: rich-document-actions
description: "RichDocument action toolkit for markdown and interactive content outside live chat. Use when adding an action or content source, wiring a remote action surface, putting actions on a MarkdownStream/BasicMarkdownContent preview, or touching features/rich-document/**, <RichDocument>, <RichDocumentActionSurface>, registerAction, ContentSourceAdapter, or enableContextMenu. NOT for the live chat message bar (use overlay-system)."
---

# RichDocument Actions

Canonical how-to for the **RichDocument** system — the wrapper that pairs the markdown content engine with a configurable, pluggable **action toolkit**. Deep reference: [`features/rich-document/FEATURE.md`](../../../features/rich-document/FEATURE.md). Master design/plan: `~/.claude/plans/if-you-review-the-snappy-stallman.md`.

---

## The most important context

**`MarkdownStream` / `BasicMarkdownContent` are NOT a thin react-markdown wrapper.** They are a multi-thousand-line content engine that renders interactive flashcards (with AI integrations), live diagrams, wired task lists, code surfaces, tool-call visualizations, realtime feeds, classification analyzers, plan viewers, and more. The "markdown" name is historical. **Never reimplement it, never "replace it with a plugin," never fork it.** RichDocument _wraps_ it — it does not replace it.

**RichDocument's job is the action layer**, not rendering. It forwards content to the engine and adds a surface of actions (copy / save-to-notes / save-to-task / print / html-preview / edit / …) that used to exist only on the chat `AssistantActionBar`. The whole point: every surface that shows content can now offer the same depth of interaction with one component.

---

## Mental model — three layers + two extras

```
<RichDocument>                       ← Layer 1: wrapper. Forwards to the engine,
  ├─ MarkdownStream (the engine)        renders the chosen action variant.
  └─ action variant (bar / menu / …)
        │ looks up handlers by id
        ▼
  actions/registry.ts                ← Layer 2: the action registry. Module-scope
  actions/handlers/*.ts                 Map<id, RichDocumentAction>, populated by
                                        self-registering handler modules.
        │ source-specific edit/delete
        ▼
  actions/sources/*.ts               ← per-source adapters (ContentSourceAdapter)

<RichDocumentActionSurface           ← Layer 3 (REMOTE): renders a RichDocument's
   surfaceId="…" />                     actions somewhere else in the tree (a header,
                                        a sidebar) — connected by surfaceId.

enableContextMenu                    ← Extra: lazy, streaming-safe right-click menu.
runtime/providerBridge.ts            ← Extra: module-scope bridge that lets the remote
                                        surface invoke handlers WITHOUT functions in Redux.
```

**Load-bearing invariant:** the `richDocumentActionSurfaces` Redux slice stores **only pure metadata** (action ids, labels, icon names, disabled flags) — never handlers, content, callbacks, or React elements. Handlers live in the module-scope registry and are looked up by id at click time; live content is read through the `providerBridge`'s `getCtx()` getter. This is the same pattern the overlay system uses (`callbackManager`). **Do not put functions in the slice.**

---

## TASK: Use RichDocument on a page (the common case)

Swap a bare `<MarkdownStream content={x}/>` for:

```tsx
import { RichDocument } from "@/features/rich-document/RichDocument";
import type { ContentSource } from "@/features/rich-document/types";

<RichDocument
  content={text}
  source={{ type: "note", noteId }} // drives action visibility + save-to-task linking
  actionsVariant="bar" // bar | mini-bar | menu | icon-only | remote | none
/>;
```

`RichDocument` is `"use client"` (the engine is `dynamic({ ssr:false })`). **Server components cannot render it directly** — render it from a client child.

### Pick a `source`

The discriminated union in `features/rich-document/types.ts`. The type drives which actions show and how `save-to-task` links a parent:

| Source                                                                  | Use for                                                                                                                                |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `{ type: "chat-message", messageId, conversationId, streamRequestId? }` | a cx_message                                                                                                                           |
| `{ type: "note", noteId }`                                              | a note                                                                                                                                 |
| `{ type: "prompt-result", executionId, promptId? }`                     | a prompt run result                                                                                                                    |
| `{ type: "artifact", artifactId }`                                      | an artifact                                                                                                                            |
| `{ type: "scraper-result", runId }`                                     | a scraper/research run                                                                                                                 |
| `{ type: "working-document", conversationId, kind, documentId? }`       | the per-conversation working doc / scratchpad (`kind: "working" \| "scratch"`); edits persist via `persistWorkingDocumentContentThunk` |
| `{ type: "raw" }`                                                       | generic content with no entity link (most read-only previews)                                                                          |

`raw` is fine for read-only displays — you still get copy/save/print/html-preview/etc.; only the parent link on `save-to-task` is absent.

### Pick a variant + position + behavior (three orthogonal axes)

```tsx
actionsVariant: "bar" | "mini-bar" | "menu" | "icon-only" | "remote" | "none"; // WHAT
actionsPosition: "below" |
  "above" |
  "top-right" |
  "top-left" |
  "middle-right" |
  "middle-left"; // WHERE (default "below")
actionsBehavior: "always" | "hover-only"; // VISIBILITY (default "always")
```

Conventions used across the codebase:

- **Main content output** (note preview, research report) → `variant="bar"` (or `"mini-bar"`), `position="below"`, `behavior="always"`.
- **Compact card / preview / overlay** → `variant="icon-only"`, `position="top-right"`, `behavior="hover-only"` (an unobtrusive ⋯ that fades in on hover).
- **Tight footprint** (toast) → `variant="mini-bar"`.

There is **no `"hover-menu"` variant** — it was removed. Express it as `{ icon-only, top-right, hover-only }`.

### Tune which actions appear

All built-ins are included by default; trim/extend via the `actions` prop:

```tsx
actions={{
  exclude: ["announcements", "preferences"],   // hide specific ids
  extra: [ /* custom RichDocumentAction[] — see below */ ],
  callbacks: { onFullPrint, onRequestDelete },  // host-supplied hooks some actions call
}}
```

Source-incompatible actions hide themselves automatically (e.g. `fork-at-message` only shows for `chat-message`). The overflow menu is a **multi-layer** menu (top-level promoted items + Save / Copy as / Export / Edit / Creator / Admin / App submenus, mobile = drawer + accordion) driven by `variants/shared/menuStructure.ts`.

### Add a right-click context menu (optional)

```tsx
enableContextMenu                                    // boolean, or:
enableContextMenu={{ extra: [...], exclude: [...] }} // context-menu-only actions
```

Lazy (the menu chunk loads only on first right-click) and **streaming-safe** (yields to the native browser menu while `isStreamActive`). This is the extension point for future per-surface right-click functionality.

---

## TASK: Render actions in a _different_ location (remote surface)

Put the bar in a page header / toolbar while the content lives elsewhere:

```tsx
// In the header chrome:
<RichDocumentActionSurface surfaceId={`note-detail-${noteId}`} variant="bar" fallback={null} />

// In the body:
<RichDocument
  content={text}
  source={{ type: "note", noteId }}
  actionsVariant="remote"
  actionsSurfaceId={`note-detail-${noteId}`}
/>
```

- Use a **per-entity surfaceId** (`note-detail-${id}`) so fast A→B navigation never collides.
- The surface renders nothing (`fallback`) when no provider is registered (e.g. the body is in a non-preview mode) — so an empty header row is fine.
- The registry is a **stack**: if two RichDocuments target one surfaceId, the most-recently-mounted wins, and out-of-order unmount during navigation stays correct. Don't add your own last-wins logic.
- Real example to copy: `packages/chat/src/agents/components/working-document/WorkingDocumentPanel.tsx` (headless provider + header surface). The live `/notes` header intentionally has no remote consumer, so `NotesView` omits `actionsSurfaceId` and keeps preview/split actions inline.

**Surface draws its OWN content (an editor)?** Don't mount a hidden `RichDocument` just to register the toolbar — it would double-render the heavy engine. Use the **headless `RichDocumentActionProvider`** (renders `null`):

```tsx
// Mounted once, always (gate on whatever "active" means for your surface):
<RichDocumentActionProvider content={liveText} source={mySource} surfaceId={mySurfaceId} />
// The toolbar, anywhere:
<RichDocumentActionSurface surfaceId={mySurfaceId} variant="bar" fallback={null} />
```

This is how the toolbar appears in **every** editor mode (plain / split / wysiwyg / preview), not just the one mode that mounts a `RichDocument`. Real example: `packages/chat/src/agents/components/working-document/WorkingDocumentPanel.tsx` (provider + header bar) + `WorkingDocumentControls.tsx` (compact `menu` surface). It shares `useActionSurfaceProvider` with `RichDocument`, so behavior never drifts.

`MatrxSplit` has opt-in passthrough props (`actionsSource` / `actionsVariant` / `actionsPosition` / `actionsBehavior` / `actionsSurfaceId` / `actionsExclude`) — when `actionsSource` is set it swaps its preview pane to RichDocument (lazily), including the streaming-safe right-click menu. Pattern in `components/matrx/MatrxSplit.tsx`.

---

## TASK: Add a new action

1. Pick the right handler module under `features/rich-document/actions/handlers/` (`copy.ts`, `save.ts`, `export.ts`, `print.ts`, `edit.ts`, `feedback.ts`, `creator.ts`, `fullscreen-editor.ts`, `stubs.ts`, `app.ts`, `server-api.ts`) or add a new one and import it in `actions/handlers/index.ts`.
2. Call `registerAction` at module load:

```ts
import { registerAction } from "../registry";

registerAction({
  id: "my-action", // unique; built-ins are in RichDocumentActionId
  label: "Do the thing", // string OR (ctx) => string for dynamic labels
  icon: SomeLucideIcon,
  iconColor: "text-blue-500 dark:text-blue-400", // optional, preserves visual variety
  category: "save", // feedback|copy|export|save|edit|share|creator|app|admin
  supportedSources: "*", // or ["chat-message", "note", ...]
  renderSlot: "overflow", // "primary" (inline) | "overflow" (⋯) | "both"
  order: 5,
  visible: (ctx) => true, // optional
  disabled: (ctx) => false, // optional; return { reason } for a tooltip
  run: async (ctx) => {
    // ctx: content, source, metadata, dispatch, isAuthenticated, isAdmin,
    //      isCreator, surfaceKey, instanceKey(prefix), sourceAdapter, callbacks, extensions
    await doSomething(ctx.content);
    toast.success("Done"); // handlers OWN their toasts/dialogs
  },
});
```

3. **Place it in the menu hierarchy:** add its id to a section in `features/rich-document/variants/shared/menuStructure.ts` (top-level array for promoted items, or a submenu's `actionIds`). If you skip this, it falls into a trailing "extras" group.
4. **Source-specific behavior goes through the adapter**, never hard-coded: call `ctx.sourceAdapter.edit({ newContent, source, dispatch })` rather than dispatching a chat thunk directly. That's how one generic `edit` action works for chat (editMessage), notes (NotesAPI.update), etc.
5. **Auth-gated actions:** call `requireAuth(ctx, key, featureName, description)` from `actions/utils.ts` at the top of `run`; it opens the authGate overlay and returns false when signed out.
6. Overlay `instanceId`s: use `ctx.instanceKey("prefix")` so two documents on one page don't collide.

For a per-surface, app-specific action, prefer `actions={{ extra: [...] }}` at the call site over a global registry entry.

### `extra` actions that open an overlay

```ts
run: ({ dispatch, source, instanceKey }) =>
  dispatch(openOverlay({
    overlayId: "noteWindow",                 // MUST already exist in features/overlays/
    instanceId: instanceKey("note-window"),
    data: { noteId: (source as Extract<ContentSource,{type:"note"}>).noteId },
  })),
```

The shape is `{ overlayId, data, instanceId }` — **not** `{ component, props }`. To add a _new_ overlay, follow `features/overlays/FEATURE.md` (the 3-file process). Invoke the `overlay-system` skill.

---

## TASK: Add a new content source type

1. Add the variant to `ContentSource` (and, if it carries chat-style baggage, `SourceExtensions`) in `features/rich-document/types.ts`.
2. Create `actions/sources/<type>.ts` implementing `ContentSourceAdapter` — at minimum `instanceKeyPrefix(source)`; add `edit` / `delete` / `reRun` if the source supports them (they gate the `edit` / `delete` actions' visibility).
3. Register it in `actions/sources/index.ts` (`SOURCE_ADAPTERS` map).
4. If `save-to-task` should link a parent, add the source to `sourceToEntityType()` in `actions/handlers/save.ts`.
5. Add the new `type` to the `RichDocumentActionId` source-compatibility expectations in any actions that should support it (`supportedSources`).

---

## Invariants & gotchas

- **No functions / content / React elements in the `richDocumentActionSurfaces` slice.** Metadata only. (Bridge + module registry hold the live stuff.)
- **`"use client"` is mandatory** on anything rendering RichDocument; the engine is SSR-disabled.
- **No `useMemo` / `useCallback` / `React.memo`** — the React Compiler is on. Refs are read only inside event handlers / effects, never during render (`react-hooks/refs`). Avoid impure calls (`Date.now()`) the `react-hooks/purity` rule flags.
- **`renderer` has no `"auto"`.** The basic vs configurable engines preprocess differently; silent swaps diverge output. Default is the standard engine path; pick explicitly only when needed.
- **Do NOT wrap engine-internal block renderers** (`ArtifactBlock`, `MarkdownPreviewBlock`, `StructuredPlanViewer`, anything in `components/mardown-display/`) in RichDocument — they run _inside_ the engine, so wrapping recurses infinitely. The parent message/surface provides actions at the outer level.
- **`MarkdownRenderer`** (`components/ai/MarkdownRenderer` and `components/mardown-display/MarkdownRenderer`) is a SEPARATE lightweight react-markdown primitive, not the heavy engine — out of scope; don't migrate those to RichDocument reflexively.
- **The live chat bar is off-limits here.** `AssistantActionBar` + `messageActionRegistry.ts` (1.6k lines) still power chat and carry intricate chat-only behavior (fork-vs-delete dialog, local thumbs state, density hover, group aggregation, the per-conversation menu gate). RichDocument's handlers were _ported_ from it and are equivalent for `chat-message`, but swapping the live bar is a supervised consolidation (plan Phase 4), not a casual change. Until then the duplication is intentional.

---

## When NOT to use RichDocument

- Engine-internal blocks → recursion (see above).
- A surface that already owns a bespoke action bar you must keep (e.g. `research/DocumentViewer`'s `ContentActionBar`) → swapping changes behavior; leave it or migrate deliberately.
- Pure non-interactive micro-text where a menu would be noise.
- Live streaming chat messages → that's the chat pipeline's territory.

---

## Verification

- `pnpm type-check` and `pnpm eslint features/rich-document/ <your-files>` — must be clean (the feature itself carries zero errors; pre-existing react-compiler warnings in unrelated files are not yours to fix here).
- Browser: render the surface, open the ⋯ menu — confirm the multi-layer hierarchy, that source-incompatible actions are hidden, and that a submenu expands. For a **remote** surface: confirm the body is chrome-free and the header bar opens a menu that operates on the body's live content. For **context menu**: DevTools Network shows no context-menu chunk until first right-click; during an active stream the native browser menu shows instead.
- Auto-login for testing (nonce handshake, two steps): `openssl rand -hex 16 > .dev-login-nonce`, then `/api/dev-login?nonce=<that value>&next=/<route>`.

---

## File map

```
features/rich-document/
├── RichDocument.tsx                 ← the wrapper (engine + variant switch, positioning, context-menu mount; delegates registration to useActionSurfaceProvider)
├── RichDocumentActionSurface.tsx    ← remote renderer (reads slice top-of-stack → bridge → variant)
├── RichDocumentActionProvider.tsx   ← headless: registers the toolkit for a surfaceId WITHOUT the engine (renders null)
├── types.ts                         ← ContentSource, RichDocumentAction(Context), variant/position/behavior, adapter, specs
├── actions/
│   ├── registry.ts                  ← registerAction / getAction / resolveActions
│   ├── utils.ts                     ← requireAuth, getErrorMessage, extractFirstCodeBlock, buildTaskTitle, resolveActionLabel
│   ├── handlers/*.ts                ← self-registering action modules (index.ts imports them all)
│   └── sources/*.ts                 ← per-source ContentSourceAdapter + SOURCE_ADAPTERS map
├── variants/
│   ├── ActionBar / MiniActionBar / MenuVariant   ← inline variants
│   ├── OverflowMenu.tsx             ← ⋯ dropdown (desktop) → MobileActionDrawer (mobile)
│   ├── MobileActionDrawer.tsx       ← bottom sheet + accordion
│   ├── ContextMenu.tsx              ← lazy right-click menu (controlled dropdown at cursor)
│   └── shared/{menuStructure,DropdownMenuTree,PrimaryButtons,runAction,categories}.ts
├── runtime/
│   ├── useActionSurfaceProvider.ts   ← shared registration brain (RichDocument + RichDocumentActionProvider; buildContext/specs/provider+bridge effects)
│   ├── providerBridge.ts            ← module-scope getCtx/actions registry (no functions in Redux)
│   └── ContextMenuMount.tsx         ← lightweight, streaming-safe, lazy-loads ContextMenu
└── redux/actionSurfacesSlice.ts     ← surfaceId → provider stack (metadata only)
```

Real migrated consumers to copy from: `features/notes/components/NoteEditorCore.tsx` + `NotesView.tsx` (inline preview/split actions), `features/tool-call-visualization/renderers/web-research/WebResearchOverlay.tsx` (icon-only hover), and `packages/chat/src/agents/components/working-document/WorkingDocumentPanel.tsx` (headless provider + remote header toolbar in every editor mode).
