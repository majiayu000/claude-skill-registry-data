---
name: shape-authoring
description: "The complete rules for writing or editing a shape's component (kind component). Use when creating, editing, patching or fixing a kind component, calling any kindcomp_* tool, or when a shape renders empty, broken, cropped, cramped or ugly."
attach_with_tools: [kindcomp_get_context, kindcomp_create_component, kindcomp_update_code, kindcomp_patch_code, kindcomp_get_code, kindcomp_update_settings, kindcomp_resolve_incident, kind_create]
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/shape-authoring/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# shape-authoring — the one rulebook for shape components

A shape component is React (TSX) stored in the platform and compiled in the reader's browser. It
renders one item an agent produced. **This file is the whole contract.** An import, prop, action
or pattern that is not written here does not exist — do not guess one.

Each block below is the single home of its rule. To change a rule, change its block.

<workflow>
1. `kindcomp_get_context` with the kind (or component_id) — FIRST, every time. It returns the
   kind's schema, the example payload your component receives, the other components, and open
   render incidents.
2. Write the COMPLETE component against the example payload, following every block below.
3. Save: `kindcomp_create_component` (new), `kindcomp_update_code` (whole source),
   `kindcomp_patch_code` (small exact edits).
4. A save can be REFUSED with a sentence (unknown import, banned global, no `data` read). Fix
   exactly what it names and save again — never work around it.
5. Fixing a crash: read the incident from step 1, fix, save, then `kindcomp_resolve_incident`.
</workflow>

<props_contract>
export default function MyShape({ data, kind, config, runAction, itemState }) { … }

- `data` — the item. EVERY field is read from it: `data.title`, `data.items?.map(…)`. Flat props
  (`props.title`) are never provided; a component reading them renders empty with no error.
  Read-only — never mutate it, never write results into it.
- `props_transform` (optional) reshapes the value before mounting; its output STILL arrives as
  `data`.
- `kind`, `config` — the kind slug and this component's config.
- `runAction(key, input)` — the ONLY way anything leaves the component (see <actions>).
- `itemState` — what actions saved onto this item; `{}` when nothing yet. Survives reload.
- `onResolve`, `uiOptions` — only inside a picker the page opened; ignore otherwise.
- One default export. Hooks only at the top level of components.
</props_contract>

<available_imports>
Only these module paths may be imported, with exactly these names. Anything else is refused at save.

Kit (use FIRST — see <kit>):
"@/components/kind-kit/KindHeaderBar"
"@/components/kind-kit/KindPanel"
"@/components/kind-kit/KindPanelGrid"
"@/components/kind-kit/SortableList"
"@/components/kind-kit/TagList"
"@/components/kind-kit/StreamingSkeleton"
"@/components/kind-kit/KindActionButton"
"@/components/kind-kit/KindImage"

Copy:
"@/components/agent-copy/CopyButtons"
"@/components/agent-copy/CopyForAiButton"

Text:
"@/components/Markdown"
"@/components/MarkdownStream"
"@/components/markdown"
"@/components/mardown"

UI controls (prefer the design system; the ui/* paths are the same parts):
"@ai-matrx/design-system/controls"
"@ai-matrx/design-system"
"@/components/ui/accordion"
"@/components/ui/alert"
"@/components/ui/avatar"
"@/components/ui/badge"
"@/components/ui/button"
"@/components/ui/card"
"@/components/ui/checkbox"
"@/components/ui/collapsible"
"@/components/ui/dialog"
"@/components/ui/dropdown-menu"
"@/components/ui/input"
"@/components/ui/label"
"@/components/ui/popover"
"@/components/ui/progress"
"@/components/ui/radio-group"
"@/components/ui/scroll-area"
"@/components/ui/select"
"@/components/ui/separator"
"@/components/ui/sheet"
"@/components/ui/skeleton"
"@/components/ui/slider"
"@/components/ui/switch"
"@/components/ui/table"
"@/components/ui/tabs"
"@/components/ui/textarea"
"@/components/ui/tooltip"
"@/lib/utils"

Icons:
"lucide-react"
"@ai-matrx/icons"
"@/components/official/icons/IconResolver"

Libraries:
"react"
"recharts"
"motion/react"
"date-fns"
"lodash"
"react-katex"
"react-pdf"          (PDFs from data: URIs or bytes only — never a URL)
"xlsx"
"three"
"@react-three/fiber"

Applets (page only — they do not run inside the sealed frame; do not use in shapes):
"@/applets"
"@ai-matrx/applets/react"

Libraries load only when imported. `props_transform` cannot import them.
</available_imports>

<kit>
The kit makes every shape correct and consistent by construction. Hand-rolling a header, panel,
grid, sortable list, chip list, skeleton, action button or image is a defect.

- `KindHeaderBar` — the one compact header: `title` (required), `icon?`, `subtitle?`,
  `stats?: [{label, value, icon?}]`, `streaming?`, `copy?` (CopyButtons props, `label` required),
  `actions?`, `size?: 'sm'|'md'`, `className?`. It has NO padding of its own: the host frame pads
  it. Put it inside your own bordered card and you pad it to match your rows
  (`className="px-3 py-2"` beside `px-3` rows), or the icon touches the card edge.
- `KindPanelGrid` — auto-fit grid of equal-height panels: `minColumnWidth?` (default 280, never
  smaller for text), `maxColumns?`, `gap?: 'sm'|'md'|'lg'`.
- `KindPanel` — `title` (required), `icon?`, `count?`, `badge?`, `streaming?`, `actions?` (≤2),
  `menuItems?: [{label, onSelect, icon?, disabled?, destructive?, separatorBefore?}]`,
  `subline?` (full width under the header), `footer?` (pinned to the bottom), `variant?:
  'card'|'bare'`, `dense?`.
- `SortableList` — drag to reorder with displacement and a drop placeholder: `items`,
  `onReorder(items)` (required), `getKey?`, `renderItem?(item, {index, isDragging})`,
  `onRemove?`, `emptyState?`.
- `TagList` / `KeywordChip` — chips that wrap, never truncate. TagList: `items` (strings or
  `{label, key?, meta?}`), `selected?`, `onToggle?`, `onRemove?`, `onEdit?`, `onAdd?` (renders the
  add input), `addPlaceholder?`. KeywordChip: `label`, `meta?`, `selected?`, `onSelect?`,
  `onRemove?`, `tone?: 'default'|'primary'|'muted'`.
- `StreamingSkeleton`, `useStreamingValue`, `streamList`, `streamText` — see <streaming>.
- `KindActionButton` — see <actions>. `KindImage` — see <media>.

Import each by its exact path with the named export: `import { KindPanel } from "@/components/kind-kit/KindPanel"`.
</kit>

<copy>
Every shape has a copy bar in its header (`KindHeaderBar copy={…}`); rows and panels that hold
something worth copying get their own small `CopyButtons`.

`CopyButtons`: `label` (REQUIRED), `human?: string | () => string` (plain text or markdown you
build), `agent?: () => ({ kind, location, description, data, summary? })` (Copy for AI),
`json?: () => value`, `size?: 'xs'|'icon'|'sm'`, `export?: { items: [{ id, label, filename,
content: () => string }] }` (downloads), `hide?: ('copy'|'ai'|'export')[]`.
There is no `content` or `data` prop. Pass builder functions so text is built at click time.
`CopyForAiButton`: `label` and `agent` required; `size?`, `compact?`.
</copy>

<actions>
`runAction(key, input)` never throws. It resolves `{ok: true, result}` or `{ok: false, error}`;
show `error` small beside the control that caused it.

| key | does | input |
|---|---|---|
| `run_shortcut` | runs AI on this item | `{ shortcutId, scope?, variables?, display?, expect?, saveAs?, label? }` |
| `save_item_state` | keeps a person's pick or edit | `{ patch: { key: value } }` (`null` deletes a key) |
| `open_file` | opens a saved file in the platform viewer | `{ file_id }` |
| `share_file` | opens the share window for a saved file | `{ file_id }` |
| `apply_surface_write` | writes a value into the page around the shape | `{ target, value }` |
| `list_surface_write_targets` | which page fields accept writes | `{}` |

`run_shortcut`:
- `shortcutId` — a named constant at the top of the file. Never a raw agent id.
- `scope: { selection, content, … }` — TEXT the agent can read (a short markdown rendering of
  the piece), never the raw object.
- No `saveAs` → the shortcut opens in its own window (a conversation the person continues).
- `saveAs: "idea_3_brief"` → runs in the background and the platform saves the product onto
  this item as `itemState.idea_3_brief`. Key per piece: `<piece>_<n>_<what>`.
- `expect: "json"` (default) | `"text"` | `"image"` (an image shortcut; saves an image ref).
- Chains: await step 1 with `saveAs`, pass its product into step 2's `scope`, `saveAs` again.

Render saved results in place, next to the piece they belong to; keep the button available to
run again (re-running replaces the value). Where the item has no saved record (a preview),
`saveAs` and `save_item_state` refuse with a sentence; opening in a window still works.

`KindActionButton` is the button for any action — busy state, double-click guard, error line,
confirm:
```tsx
<KindActionButton runAction={runAction} action="run_shortcut"
  input={() => ({ shortcutId: BRIEF_SHORTCUT, scope: { selection: ideaText(idea) }, saveAs: `idea_${idea.number}_brief` })}
  label="Visual brief" confirm="Writes a detailed brief. Uses credits." />
```
For a chain pass `run={() => chain()}` instead of `action` + `input`. Every button that spends
credits or creates something passes `confirm`. Props: `label`, `icon?`, `busyLabel?`, `confirm?`,
`onDone?`, `onError?`, `variant?`, `compact?`, `disabled?`.

Platform image shortcuts: `c70e1694-9b84-4843-9999-cb5471478bb4` (idea → image prompt, text),
`a415f9f8-aa62-45f9-a532-5987da03ee59` (prompt → image, `expect: "image"`).
</actions>

<media>
- A saved image (an `itemState` value with `file_id`) renders ONLY with
  `<KindImage image={ref} alt="…" runAction={runAction} pending={busy && !ref} maxHeight={480} />`.
  It shows the whole image at its real proportions (never cropped), with expand and share.
  Never a bare `<img>` for it, and never build a URL from a `file_id`.
- Images inside `data` as `data:` URIs and inline `<svg>` render normally.
- Images from other websites do not load. Do not reference them.
- Never save a `src`, URL or download link into item state — only the ref.
</media>

<links>
- Plain `<a href="…">` for web (`https:`), `mailto:`, `tel:` and in-app paths (`/crm/…`). The
  platform opens them in a new tab, inside the frame too. Links that arrive in `data` are fine;
  `javascript:`, `data:` and `blob:` links are refused.
</links>

<frame_rules>
A shape may run inside a sealed frame. Write every component so it works there:
- No `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`, `eval`,
  `new Function`, dynamic `import()`, cookies, `localStorage`, `sessionStorage` — refused at save.
  Keep transient state in React state; keep durable state with `save_item_state`.
- No `window.parent`, `window.top`, no navigating or reading the page around you.
- Size against your own box: container queries (`@container` with `@sm:`, `@md:`, `@lg:`), never
  screen classes (`sm:`, `md:`, `lg:`).
- Dialogs, popovers, menus and tooltips work but are clipped to the shape's box. Anything that
  needs the whole screen goes behind an action.
- No `alert`, `confirm`, `prompt`, `window.open`, `window.print` — use dialogs, the kit's
  `confirm`, and actions.
- The frame never scrolls; long content scrolls inside a panel (`max-h-* overflow-y-auto`).
</frame_rules>

<streaming>
The item arrives progressively while the agent streams. The component renders its full layout
immediately and fills in:
- Before data lands: `<StreamingSkeleton layout="list"|"cards"|"table"|"text" rows={3} />` that
  mimics the finished layout — never a spinner, never a blank box.
- `const { value, arrived } = useStreamingValue(data?.summary, "")` keeps the last defined value;
  call it unconditionally with a field read. `streamList(data?.items)` for arrays,
  `streamText(data?.body, "")` for strings.
- Render list items as each one parses, with stable keys. Every field access tolerates absence:
  never show `undefined`, `[object Object]` or a raw JSON dump.
</streaming>

<layout>
- Budget width from the CONTENT, never from how many things you want side by side. Text panels
  need ≥280px: use `KindPanelGrid` so four panels become 2×2 or one column when space is short.
- Text wraps; it is never truncated with an ellipsis.
- A header row holds the title, ONE count or badge and at most two controls; the rest go in the
  panel's overflow menu. Per-row actions appear on hover and focus.
- Side-by-side panels are equal height with footer actions pinned to the bottom.
- Dense, never cramped: minimal outer padding, tight inner spacing, full width.
- Prefer one excellent column over four unreadable ones.
</layout>

<design>
- **Unstyled element inside the sandbox frame? Check the daily stylesheet first.** On Vercel the
  frame's stylesheet (`public/kind-sandbox.css`) is rebuilt at most once a day: a Tailwind class used
  for the FIRST time in a repo file since the last rebuild is missing from it until the next one
  (the main app is unaffected). The release's build log has one `[kind-sandbox-css] REUSED …` or
  `BUILT …` line saying which happened. Fix now: put `[fresh-css]` in the next release message.
  Rule + reason: `features/content-ir/sandbox/build-kind-sandbox.ts` § THE DAILY STYLESHEET.
- Modern, professional, delicate. Semantic Tailwind tokens only: `bg-card`, `bg-muted`,
  `text-foreground`, `text-muted-foreground`, `border-border`, `text-primary` and their variants.
  No hex colors, no arbitrary values, no emojis in the interface.
- Correct in light and dark mode — tokens guarantee it; fixed colors break it.
- Interactive wherever the data invites it: reorder, inline edit, add and remove, one-click copy.
  Dragging always shows where the item will land (`SortableList` does this).
- In-app text is short labels, not sentences.
</design>

<before_saving>
- [ ] Every field read from `data`, null-guarded.
- [ ] Every import is in <available_imports>, by exact path and name.
- [ ] Kit used for header, panels, grid, lists, chips, skeleton, buttons, images.
- [ ] Header copy bar with a `label`.
- [ ] Renders a skeleton before data and fills in while streaming.
- [ ] Container queries, no screen-width classes; nothing truncated; nothing cropped.
- [ ] Results in `itemState`, never in `data`; shortcuts by named constant; credit-spending
      buttons confirm.
</before_saving>
