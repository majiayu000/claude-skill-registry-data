---
name: matrx-extend-tool-display
description: "Tool-call row display registry for the matrx-extend side panel. Use when making a tool 'show up nicely', editing `src/features/chat/tool-display/`, changing a row's icon, label, args, or result view, adding a CustomComponent, or a registered tool renders the default row. NOT for matrx-frontend (use matrx-frontend's create-tool-renderer)."
---

# matrx-extend Tool Display Registry

Per-tool customization for how a tool call shows up in the chat surface of the **matrx-extend Chrome extension** (the agent harness side panel). Anything not registered keeps rendering exactly as it does today — the registry only intercepts on opt-in.

**Scope guardrail**: this only applies to `src/features/chat/tool-display/` in the matrx-extend repo. The Matrx admin app, dashboard, workflow-studio, etc. are separate surfaces with their own rendering pipelines. Do NOT confuse with server-side tool catalog generation (`pnpm catalog:tools`) — that's about advertising tools to the LLM, not displaying their results to humans.

## When to use this skill

Trigger when the user asks to:
- Add a new tool to the display registry / "make X tool show up nicely"
- Customize what shows in the inline header (icon, prefix, "Getting X" labels, info hint)
- Render a tool's result with custom components instead of raw JSON
- Plug in a fully custom React component for one tool
- Debug a registered tool that's silently falling back to the default

## Branch files — read only when your run reaches them

- **Setting `CustomComponent` (charts, comparison views, interactive forms, answer-back tools) → read [custom-component.md](custom-component.md).**
- **Rendering every item of an array result (e.g. a list of `{title, url}` objects) — `keysInfo` only addresses single values → read [cookbook.md](cookbook.md) (CustomComponent or reshape on the server).**
- **Want a ready-made config pattern (tense prefixes, counts, hide-while-running, shimmering labels, per-category or favicon icons) → read [cookbook.md](cookbook.md).**
- **Want a complete registered entry to copy (`ctx_get`, `take_screenshot`) → read [worked-examples.md](worked-examples.md).**

## Mental model in 30 seconds

```
chat → ToolTimelineRow (client tools) ─┐
chat → ServerToolRow (server tools)  ─┴→ toolDisplayRegistry[toolName] ?
                                           ├─ no  → default rendering (unchanged)
                                           ├─ yes + cfg.CustomComponent → that
                                           └─ yes + config → ConfigurableToolRow
                                                       (wrapped in ToolDisplayBoundary)
```

Three failure modes are all silent — they log `console.warn` and degrade gracefully:
1. **Bad path/key** in config → that field is skipped, others render.
2. **Throwing transform / field component** → that field is skipped, others render.
3. **Throwing custom component** → entire row falls back to default.

The user never sees an error UI. Verify your config by checking the rendered row, not by waiting for an exception.

## Quick start — minimal entry

For a tool whose result has a `label` and `content` field that should render nicely:

```ts
// src/features/chat/tool-display/registry.tsx

export const toolDisplayRegistry: Record<string, ToolDisplayEntry> = {
  my_tool_name: {
    inline: {
      prefix: { started: 'Doing', completed: 'Did' },
      info: { path: 'args.target', transform: 'snakeToTitle' },
    },
    results: {
      displayType: 'custom',
      keysInfo: [
        { key: 'label',   component: 'BoldLabel' },
        { key: 'content', component: 'Markdown', transform: 'textClean' },
      ],
    },
  },
};
```

That's it. The tool name is the raw `toolName` string the SW dispatcher uses (e.g. `ctx_get`, `read_page`, `seo_get_keyword_data`) — not the title-cased label. Find it by triggering the tool once and reading the inline row.

## File map

| File | Purpose | When to edit |
|---|---|---|
| `src/features/chat/tool-display/registry.tsx` | The actual entries map | **Adding a new tool** — almost always the only file you touch |
| `src/features/chat/tool-display/types.ts` | TS shapes for the config | Only when adding a new top-level config field (rare) |
| `src/features/chat/tool-display/registry-transforms.ts` | Named transforms (`titleCase`, `textClean`, …) | Adding a reusable string transformer |
| `src/features/chat/tool-display/registry-components.tsx` | Field components (`BoldLabel`, `Markdown`, …) | Adding a new way to render a single value |
| `src/features/chat/tool-display/helpers.ts` | Resolution + error boundary | Almost never |
| `src/features/chat/tool-display/ConfigurableToolRow.tsx` | The renderer | Almost never — config-driven |
| `src/features/chat/ToolTimelineRow.tsx` | Client-tool dispatch (do NOT touch the default branch) | Only if changing the dispatcher itself |
| `src/features/chat/ServerToolRow.tsx` | Server-tool dispatch (same) | Same |

**One golden rule**: edits go to `registry.tsx` (and maybe `-transforms.ts` / `-components.tsx`). Never modify the default render paths in `ToolTimelineRow` / `ServerToolRow` — they are the safety net for every unregistered tool plus the fallback for any registered tool whose config blows up.

## The full config shape

Every visual segment is `PhaseAware<T>`: pass a single value to apply to all phases, or `{ started, completed, error }` to vary per phase.

```ts
interface ToolDisplayEntry {
  inline?: {
    hidden?: PhaseAware<boolean>;
    icon?: PhaseAware<IconName | InfoSpec>;  // lucide name OR InfoSpec resolving to a
                                              // lucide name OR a URL (rendered as <img>)
    prefix?: PhaseAware<string>;             // "Getting" / "Got" / "Failed to get"
    name?: PhaseAware<string | InfoSpec>;    // default: titleCase(toolName); '' to suppress;
                                              // pass an InfoSpec to pull from args/output
    suffix?: PhaseAware<string>;
    info?: PhaseAware<string | InfoSpec>;    // string shorthand = { path: string }
    color?: PhaseAware<ColorToken>;
    isMultiline?: boolean;                   // wrap vs truncate the info segment
    spinIcon?: PhaseAware<boolean>;          // default: true on 'started' only
    shimmerOnRunning?: boolean;              // shimmer the label while phase=started; default true
  };
  args?: {
    hidden?: PhaseAware<boolean>;
    displayType?: 'json' | 'key-value' | 'values-only';  // default 'json'
  };
  results?: {
    hidden?: PhaseAware<boolean>;
    displayType?: 'json' | 'key-value' | 'values-only' | 'custom';
    keysInfo?: KeyDisplay[];                 // required when displayType === 'custom'
    alwaysShow?: boolean;                    // render result content visibly under the row,
                                              // no click required (use for screenshots, charts)
  };
  CustomComponent?: ComponentType<{ entry: ToolTimelineEntry; kind: 'server' | 'client' }>;
}

interface InfoSpec {
  path: string;                              // see "Path expressions" below
  transform?: TransformName | TransformName[];
  fallback?: string;                         // shown when path is nullish/empty
}

interface KeyDisplay {
  key: string;                               // dot path within the result object
  component: FieldComponentName;
  className?: string;                        // appended to component default classes
  transform?: TransformName | TransformName[] | null;
  fallback?: string;
}
```

## Path expressions

Used in `inline.info.path` and (with shallow-only resolution) in `keysInfo[].key`. Recognized roots for the inline path:

- `args.<key>...` — the model-supplied input
- `output.<key>...` (or `result.<key>...`, alias) — the tool's return payload
- `message` — error message string (only set in `error` phase)
- `toolName`, `callId` — for completeness; rarely useful

Numeric segments index into arrays: `output.items.0.title`. Misses are silent — render skips that segment.

## Transforms (current set)

In `registry-transforms.ts`. Add new ones there — same `(unknown) => unknown` contract, never throw.

| Name | Effect |
|---|---|
| `titleCase` / `snakeToTitle` / `kebabToTitle` | `clean_content_markdown` → `Clean Content Markdown` (aliases — same impl) |
| `textClean` | Strips markdown escapes (`\_`, `\*`, `` \` ``), trims whitespace |
| `truncate80` / `truncate200` | Truncate long strings with an ellipsis |
| `lowercase` / `uppercase` | Case conversion |
| `formatImageDimensions` | `{ width, height, ... }` → `"WxH"` (e.g. `2576×1911`). Use with `info.path: 'output'` for image tools. |
| `formatBytes` | Number → `"123 KB"` / `"4.5 MB"` |
| `browserCategoryIcon` | Browser-tools category name → distinct lucide icon (`core` → `Wrench`, `forms` → `FormInput`, `cookies` → `Cookie`, …). Use as the transform on `inline.icon` with `path: 'args.category'`. |

Chain by passing an array: `transform: ['textClean', 'truncate80']`.

## Field components (current set)

In `registry-components.tsx`. Each receives `{ value, className? }`.

| Name | Renders as |
|---|---|
| `BoldLabel` | `<div>` with bold 12px text |
| `TextDisplay` | Plain 12px `<div>` |
| `Markdown` | `<MarkdownView density="compact">` (full markdown w/ remark-gfm) |
| `Code` | Pre-formatted scrollable code block |
| `Json` | Pretty-printed JSON in a code block |
| `Image` | `<img>` — value must be a URL or data-URI string |
| `Base64Image` | `<img>` from base64 — accepts a string OR an object like `{ image_base64, media_type, width?, height?, byte_length? }` (the screenshot result shape). Renders the image plus a small caption with dimensions and size. |
| `Badge` | Small pill — good for counts, statuses |
| `Chips` | An array of strings rendered as a wrapped row of monospace pills. Good for tool lists, tag arrays, etc. Non-array values are coerced to a single chip. |
| `TabCard` | Favicon + title + clickable URL card — built for `get_active_tab`-style payloads. Reads `fav_icon_url` (or `favIconUrl`/`favicon`), `title`, and `url` keys; falls back to a Globe icon if the favicon fails to load. Use with `key: ''` to pass the whole result. |

When adding a new component: keep it small, accept `unknown` for `value`, never throw.

### Whole-result key convention

`keysInfo[].key` normally points at one field of the result. To pass the **entire result object** to the field component, set `key: ''` (or `key: '*'`). This is how `Base64Image` gets at both `image_base64` and `media_type` in one render — no need to combine fields with a transform.

```ts
keysInfo: [{ key: '', component: 'Base64Image' }]
```

## Visual design philosophy

The chat surface treats tool calls like the Reasoning block — **slim, inline, low-noise**. No borders, no card backgrounds, just `py-0.5` rows with hover affordance. The visual heaviness of a tool row should match its semantic weight: a typical tool call is one log line, not a dashboard widget.

What this means concretely:

- **Inline rows are tiny.** Don't bulk them up with extra info segments unless they earn their space.
- **Most "rich" content goes in the expanded body.** Click to inspect args + result JSON.
- **A tool whose result IS the point** (screenshots, charts, favicons) should hoist that content with `results.alwaysShow: true` OR by putting the visual signal in the inline icon (favicons via `InfoSpec`).
- **Long-running tools** (`find`, AI tools, network-heavy actions) get a shimmering label automatically while phase=started — keep `shimmerOnRunning` enabled (it's the default).

## `results.alwaysShow` — render the result without a click

Set when the result payload IS the user-facing point of the tool. The `keysInfo` content renders directly under the row, visible by default. The click-to-expand still works for inspecting args + raw JSON.

```ts
// take_screenshot — image is the star, never hide it
results: {
  displayType: 'custom',
  keysInfo: [{ key: '', component: 'Base64Image' }],
  alwaysShow: true,
}
```

When to use it:
- **Yes**: screenshots, generated images, charts, single-pane media.
- **Maybe**: a TabCard or Chips list — but consider hoisting the signal into the inline row instead (favicon as icon, count in info).
- **No**: long text, JSON dumps, list of items — these are better behind a click so the chat doesn't sprawl.

## Result display modes

`results.displayType` controls how the (typically object) result is shown:

- **`'json'`** (default) — pretty-printed JSON in a `<pre>`. Same as today's default.
- **`'key-value'`** — two-column grid: bold key, value. One row per top-level key. Non-object payloads fall back to JSON.
- **`'values-only'`** — bulleted list of just the values. Loses keys. Useful when keys are noise.
- **`'custom'`** — iterate `keysInfo`; each entry `getByPath` → `applyTransforms` → render with `component`. Missing keys with no `fallback` are silently skipped + warned.

`args.displayType` supports the same modes minus `'custom'`.

## Icons + colors

**Icons**: any export name from `lucide-react`. Examples: `HandGrab`, `Database`, `Search`, `Globe`, `Cookie`, `Camera`, `MousePointerClick`, `Keyboard`, `FileText`, `BookOpenText`, `Wrench`, `Bug`, `Sparkles`, `Plug`, `AppWindow`. Unknown names log a warning and fall back to the phase default (`Loader2` / `CheckCircle2` / `AlertTriangle`).

**Dynamic icons (favicons, per-arg icons)**: pass an `InfoSpec` instead of a literal name. The resolved string is auto-detected as a lucide name OR a URL:

```ts
// Favicon as the inline icon (URL → <img>)
icon: { completed: { path: 'output.fav_icon_url', fallback: 'Globe' } }

// Per-arg icon via a transform that maps a value to a lucide name
icon: { completed: { path: 'args.category', transform: 'browserCategoryIcon' } }
```

When the URL fails to load (favicon 404, CSP block, etc.) the renderer falls back to a Globe icon. When an `InfoSpec` resolves to nothing, falls back to the phase-default lucide icon (use `fallback: 'SomeLucideName'` to override).

**Colors**: pick a `ColorToken` — `blue`, `sky`, `emerald`, `amber`, `red`, `violet`, `slate`, `primary`, `muted`. Resolves to a `text-{color}-600 dark:text-{color}-400` class. **Error phase always wins (forced red)** regardless of the override — keeps error visuals consistent across the app.

## `name` accepting an `InfoSpec`

Two patterns where this matters:

**Mid-sentence values** (the dynamic word lives between static prefix/suffix):

```ts
// load_chrome_tools — header: "Loading my core browser tools"
inline: {
  prefix: { started: 'Loading my', completed: 'Loaded my', error: 'Failed to load my' },
  name: { path: 'args.category' },  // resolves "core" / "page" / "interact" / …
  suffix: 'browser tools',
}
```

**Title-as-name** (a full descriptive title takes over the label after success):

```ts
// get_active_tab — header: "Reading active tab" → "<Page Title>" → "Couldn't read…"
inline: {
  prefix: { started: 'Reading active tab', error: "Couldn't read active tab" },
  name: {
    started: '',                                                // suppress
    completed: { path: 'output.title', transform: 'truncate80' },
    error: '',                                                  // suppress
  },
}
```

**Why both `''` and `undefined` matter:**
- `name: undefined` → falls back to `titleCase(entry.toolName)` (e.g. `Get Active Tab`)
- `name: ''` → suppresses the segment entirely (no fallback)
- `name: { path: '...' }` resolving to nothing → empty (no fallback to titleCase)

When you only want a name in some phases, set the others to `''` explicitly — otherwise the auto title-case sneaks back in.

## The CustomComponent escape hatch

When the config isn't expressive enough, a full React component owns the whole row. **Setting `CustomComponent` → read [custom-component.md](custom-component.md)** — its contract, the fallback on throw, and when interactive tools need it.

## Adding a new tool — checklist

```
- [ ] 1. Find the raw toolName. Trigger the tool once; the default row shows
       the snake_case name. (For server tools, ServerToolRow titleCases it,
       so use the catalog: types/tool-catalog.json or src/lib/tools/handlers/*.)

- [ ] 2. Decide the inline shape:
       - prefix (phase-aware verb: "Getting" / "Got" / "Failed to get")
       - icon (a lucide name that suggests the action)
       - color (one of the eight ColorTokens; error is always red)
       - info (the most identifying arg or result field, transformed for humans)

- [ ] 3. Decide the result shape:
       - Simple? Use 'key-value'.
       - Has a label + body? Use 'custom' with BoldLabel + Markdown/TextDisplay.
       - Already pretty as JSON? Leave default ('json').

- [ ] 4. Add the entry to toolDisplayRegistry in registry.tsx.

- [ ] 5. pnpm tsc --noEmit — confirm types check.

- [ ] 6. Reload the extension, trigger the tool, walk all three phases:
       - while running: prefix + icon + spinning + info text correct
       - after success: prefix swap + icon swap + color correct
       - on error: prefix swap + red icon, no crash, message visible
       (Force an error by passing invalid args or breaking the network.)
```

## Common patterns (cookbook)

Copy-ready `inline` snippets for recurring shapes. **Need one → read [cookbook.md](cookbook.md).**

## Verification

After every registry change:

1. **Typecheck**: `pnpm tsc --noEmit` (must exit 0).
2. **Build**: `pnpm wxt build` (extension must build cleanly).
3. **Visual sweep**: open the side panel, trigger the tool, walk all three phases (`started` → `completed` → `error`). Compare against an unregistered tool to confirm the default still works for everything else.
4. **Console check**: open DevTools console while triggering. Any `[tool-display] ...` warning means a path/transform/icon is wrong — silent in the UI but logged.
5. **Catalog regen** (only if you changed tool handlers, not just display): `pnpm catalog:tools:md` and commit. Display registry edits do NOT need catalog regen.

## Anti-patterns

- ❌ Modifying `DefaultToolTimelineRow` / `DefaultServerToolRow`. The defaults are the safety net — touch them and every fallback inherits your bug.
- ❌ Adding error UI in the configurable renderer. Failures should be silent + logged. The user should never see "config error" — they should see the default rendering.
- ❌ Putting tool-specific logic inside `helpers.ts` or `ConfigurableToolRow.tsx`. That's what the registry config + `CustomComponent` are for.
- ❌ Using the `result.` alias in `keysInfo[].key`. `keysInfo` paths are scoped to the result object already — just use `label` (or `nested.field`), not `result.label`.
- ❌ Registering a tool name that doesn't exist. The dispatcher silently falls through to the default; you'll think your config doesn't work when really the tool never ran.
- ❌ Importing from outside `src/features/chat/tool-display/` into the registry maps. Registry files should be a flat description of behavior — pull in shared UI through `registry-components.tsx` instead.

## Reference: the `ctx_get` worked example

Full registered entries with plain-English readings: `ctx_get` (the canonical starting template) and `take_screenshot` (whole-result key + `Base64Image`). **Starting a new entry from a real one → read [worked-examples.md](worked-examples.md).**

## Universal copy button

Every row (default and configurable, server and client) has a clipboard icon on the right that appears on hover. Clicking copies the full payload as pretty-printed JSON:

```json
{
  "tool": "ctx_get",
  "phase": "completed",
  "args": { "key": "clean_content_markdown" },
  "result": { "label": "...", "content": "..." },
  "duration_ms": 263,
  "callId": "..."
}
```

Lives in [CopyToolButton.tsx](../../../src/features/chat/tool-display/CopyToolButton.tsx). Each renderer constructs a `ToolCopyData` object and passes it as `data`. The button stops click propagation so it never toggles the row open. Don't add per-tool overrides for it — the universal payload is the right shape for users (paste into bug reports, share with another agent, etc.).
