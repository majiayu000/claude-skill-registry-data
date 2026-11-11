---
name: opencode-gui-plugins
description: Build or debug OpenCode Desktop GUI plugins and prove their UI matches the host (native parity). Use for any desktop UI change (sidebar rows, context menus, popovers, header buttons, chat timeline, composer, panels), a plugin element that must look and behave like the app's own, plugin loading/build failures, GUI plugin registration, or porting another app's feature into OpenCode as a plugin.
---

A GUI plugin is a normal OpenCode plugin package whose `./gui-experimental` export is a CommonJS bundle the desktop app loads into every window. It is built on the same SDK and host as the app's own features: 15 built-in GUI plugins (terminal, files, review, browser, SSH ...) load through the registries ours use. It registers into public registries (`Command`, `Slot`, `ComposerPill`, `Panel`, `SettingsPage`, `TitlebarItem`, `Style`, `MenuItem`, `LinkHandler`, `Server`), reads the app's reactive state through `ctx`, and — only when no registry fits — injects DOM. Nothing in the app bundle is patched; the installed `.app` stays untouched.

Plugins are registered by absolute path in `~/.config/opencode/opencode.json`:

```json
"plugins": ["/Users/isaac/git/dev-files/apps/opencode-plugins/sidebar-repos"]
```

## Branches

- Choosing which extension point a job needs, or what has none → [reference/host-architecture.md](reference/host-architecture.md) §9
- Lifecycle, reload, error isolation, ids, built-in versus user power, registry behaviour, the core team's idioms → [reference/host-architecture.md](reference/host-architecture.md)
- The host API's shape (registry fields, `ctx` members) → [reference/host-api.md](reference/host-api.md)
- A row, button, menu, popover or avatar that must look like the app's own → [reference/native-ui.md](reference/native-ui.md)
- Proving a UI change matches its native sibling, writing or reading a parity spec or report → [reference/native-parity.md](reference/native-parity.md)
- Touching the app's real DOM or CSS (sidebar tabs, timeline, status marks) → [reference/dom-map.md](reference/dom-map.md)
- An icon the catalog lacks, or which catalog icon to use → [reference/icons.md](reference/icons.md)
- Any transition, fade, accordion or expand (match the host's motion; recommend it over novelty) → [reference/animation.md](reference/animation.md)
- Running a plugin in the real UI (harness, screenshots, DOM checks, hot reload, seeded long sessions) → [reference/browser-testing.md](reference/browser-testing.md)
- Worst-case data, narrow or zoomed layouts, empty/one/huge states → [reference/stress.md](reference/stress.md)
- Plugin cost: profiling, overhead budgets, hill-climbing a slow plugin → [reference/performance.md](reference/performance.md)
- Writing or updating a plugin's README, its demo media, or crediting what inspired it → [reference/readme.md](reference/readme.md)
- A first build in a new checkout, an install/build failure, or a plugin that does not appear → [reference/build.md](reference/build.md)

## Workflow

1. Confirm the installed app version and the feature's observable behaviour. Read https://opencode.ai/v2/docs/build/plugins/gui and the installed SDK declarations for the relevant surface.
2. **Align** before building. The request is aligned when it pins all four: where the UI lives (a native surface to extend, or a new one), which native sibling it must be indistinguishable from, scope and defaults, and entry points. When any is open, or a plugin can reach the goal by more than one route, load the `grilling` skill and settle each with the user through the question tool, one decision at a time with a recommended answer, until every one is written in the plugin's `DESIGN.md` under `## Decisions`. A worker without the question tool returns the open questions to its orchestrator before building the less obvious route.
3. **Lean into OpenCode, never fight it.** **Extend** before inventing: look for an existing host concept or mechanic that covers the job (tools, artifacts, panels, commands, registries) and build on it, adding only the missing view or behaviour; a parallel concept doubles what users and models learn. Hunt for these opportunities proactively on every task, updates and fixes included, not only new builds: when touching a plugin, check whether a host concept now covers its workaround (host-architecture.md §9; the host moves each release). Raise each one as soon as it appears, with the evidence, and settle it in step 2 before building a new concept or extending a workaround. Then choose a public registry or host API with the decision guide ([host-architecture.md](reference/host-architecture.md) §9). If it lists the job under "no extension point", isolate the DOM workaround, verify selectors against the installed app before editing, and record the reason in `DESIGN.md`.
4. Scaffold from `~/git/dev-files/apps/opencode-plugins/sidebar-repos`: read its manifest, Vite and workspace config rather than guessing the build contract, and preserve package identity when moving a plugin. Build each UI element from [native-ui](reference/native-ui.md) or from the host source of the sibling named in step 2.
5. Separate pure logic from setup, test it, and run every declared package check. Register the built package through the global config.
6. Load the plugin in the harness (`scripts/desktop-harness.sh`: an isolated second app driven over CDP; `opencode serve` never loads GUI plugins) and exercise it there: open the element, hot reload, switch sessions, run the cleanup. The hand-off shows a screenshot of the real window for each, listed apart from the package checks.
7. **Parity** closes the task: run `scripts/parity.mjs` against the native sibling and iterate until the report is all PASS (next section). The hand-off carries the report and its side-by-side screenshot.
8. **Stress**: run the worst realistic data through the element ([reference/stress.md](reference/stress.md)); fix what breaks.
9. **Free** also closes it: profile the plugin against the bare app and hill climb until every scenario is inside the bars in [reference/performance.md](reference/performance.md). The hand-off carries the table.

## Parity

A UI change is done when `scripts/parity.mjs` reports PASS for style, motion and behaviour against the named native sibling, and `report.md` plus `side-by-side.png` are in the hand-off. An N/A carries a written reason in the spec (`allow` for a difference by design, `na` for a sibling the harness cannot show). A FAIL means the change is not done, whatever it looks like.

Name the sibling before building (the element table in [reference/native-parity.md](reference/native-parity.md)) and build from [native-ui](reference/native-ui.md), whose components already pass. The spec format, the run command and how to read the three layers are in [reference/native-parity.md](reference/native-parity.md).

## Scaffold

A plugin is its own package, outside the app. Copy these four files.

`package.json` — the export path and the app's own SDK version are both load-bearing:

```json
{
  "name": "sidebar-repos",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "exports": { "./gui-experimental": "./dist/gui-experimental.cjs" },
  "scripts": { "build": "vite build", "typecheck": "tsc --noEmit", "test": "tsx --test src/*.test.ts" },
  "dependencies": { "@opencode/plugin": "2.2.5", "solid-js": "1.9.10" },
  "devDependencies": { "@types/node": "^22.20.5", "happy-dom": "^21.0.4", "tsx": "^4.23.15", "typescript": "^5.9.3", "vite": "^7.3.7", "vite-plugin-solid": "^2.11.15" }
}
```

Pin `@opencode/plugin` to the installed app's version (`defaults read /Applications/OpenCode.app/Contents/Info.plist CFBundleShortVersionString`). A mismatch type-checks against an API the running app does not have.

`vite.config.ts` and `tsconfig.json`:

```ts
import { defineConfig } from "vite"
import { gui } from "@opencode/plugin/gui/vite"
export default defineConfig({ plugins: [gui({ entry: "src/gui.ts" })] })
```

```json
{
  "compilerOptions": {
    "target": "ES2022", "module": "ESNext", "moduleResolution": "Bundler", "strict": true,
    "noEmit": true, "skipLibCheck": true, "lib": ["ES2022", "DOM", "DOM.Iterable"], "types": ["node"]
  },
  "include": ["src", "vite.config.ts"]
}
```

`src/gui.ts` — the default export is the plugin:

```ts
import { Plugin, Style, Command } from "@opencode/plugin/gui"

export default Plugin.define({
  setup(ctx) {
    ctx.add(Style, `[data-sidebar-repo] { color: var(--v2-text-text-muted); }`)
    ctx.add(Command, {
      id: "hello",
      title: "Say hello",
      run: () => { ctx.toast.show({ title: "Hello" }) },
    })
  },
})
```

- `setup(ctx)` runs once per window, synchronously, inside a Solid root owner. Do not return a promise; return a cleanup (or use `onCleanup`). Async work goes in `createKeyed` / `createLatest` with `ctx.signal`.
- `main(ctx)` runs once in the desktop app's main process, may be async, and is where Node-only work and `ctx.provide(Ipc)` belong. Windows reach it through `ctx.main(Ipc)`.
- The host assigns the id (`ctx.id`): the server part's `id`, else the package name, else the directory name. It prefixes every command, panel key and stored key. Built-in ids, ids nested under or over them, and the `opencode` namespace are reserved; the plugin then does not load.
- Rebuild after source changes. Local GUI bundles are watched and reload in every window (`setup` runs again in the same window); an options change reloads too. Use Extensions → Plugins → **Reload** if the running version stays stale.
- Build the bundle and its `exports` entry before the first load: a service that resolved the directory without a GUI keeps ignoring it until the service restarts ([build.md](reference/build.md)). Test on a private service (the harness, step 6), never the shared one; restart the shared service only to ship, with `~/git/dev-files/scripts/opencode-safe-restart.sh`, not `opencode service restart`: it waits for running sessions and wakes the ones a restart leaves stranded.

## Rules that keep a plugin working

- **Cap every test and script run.** Start each with `NODE_OPTIONS=--max-old-space-size=1500` under a wall-clock limit (`perl -e 'alarm 120; exec @ARGV' ...`), never leave one running, and before reporting check `ps` for leftover `node`, `tsx` and harness processes of yours and kill them. One hung test once grew to 440 GB of compressed memory and the system ran out of memory.

- **Native UI comes from the host, in this order.** (1) A registry item the host renders (`Command`, `ComposerPill`, `Panel`, `SettingsPage`, `MenuItem`, `TitlebarItem`); (2) a `ctx.ui` component (`Icon`, `Button`, `IconButton`, `Tooltip`, `Menu`, `Loader`, `Dialog`, `Switch`, `TextInput`, `Keybind`, `Markdown`, `Code`), mounted with Solid `render` inside the setup owner; (3) a [native-ui](reference/native-ui.md) component, the host's own markup and classes copied from the installed source so its CSS applies; (4) when none exists, copy the host component's real markup from the extracted source into native-ui with a parity spec; (5) hand-written HTML/CSS only for what none of these express, with `--v2-*` tokens and a one-line reason in the code. Icons come from the app catalog (`IconName`), or are drawn in its style ([reference/icons.md](reference/icons.md)).
- **Your own actions are silent when they succeed.** Snoozing, archiving, stopping, cancelling, copying and saving show their result in the UI (the row moves, the chip count drops) and never toast. Toast only failures, and things you did not do yourself (a wake, a crash, a finished background run), and route those through the notifications hub when it is installed.
- **Reach for a registry before the DOM.** A registry item re-renders from app state and survives app updates; an injected node survives neither. The registry table in `reference/host-api.md` lists every one with its slots.
- **Write plugin code the way the core team writes theirs.** `createKeyed`/`createLatest` for effects (no `createEffect`), state inside `setup` (no module-level `Map`/`let`/signal), declared `Store.global`/`Store.session` for persisted state, `Live` handling for every `ctx.use`, labels in function-item form, contracts instead of sibling imports. The rules and their sources are in [host-architecture.md](reference/host-architecture.md) §7 and §10.
- **Read state through `ctx`, never by scraping.** `ctx.tabs.list()`, `ctx.sessions.list()`, `ctx.sessions.current()`, and each session's `server.data.*` stores are reactive inside `createEffect`. Scraping the DOM for state produces stale UI the moment the app re-renders.
- **Scope styles.** `ctx.add(Style, css)` registers global CSS while the contribution is active; the host withdraws it on cleanup. Key rules on an attribute you inject (`[data-sidebar-repo]`) and use the app's `--v2-*` tokens so light and dark both work. Use app-wide selectors only when changing that app-wide behavior is the feature.
- **Injection is idempotent and reversible.** Query for your own hook before creating a node, key it on `data-tab-key` / a row key, write only when the value changes, and remove every node and attribute in the cleanup. The setup can run more than once in a window's life.
- **Never rewrite app-owned text.** Inject a sibling node instead: the app rebuilds titles from its own store, and a rewritten `textContent` is lost or duplicated depending on render order (and renaming a session must keep working).
- **A `MutationObserver` filters.** Observe the smallest attribute set that matters (`attributeFilter: ["data-tab-key", "data-orientation", "data-status"]`) and coalesce work into one `requestAnimationFrame`; an unfiltered observer over `documentElement` re-enters on its own writes.
- **Animation earns a purpose first.** Gate by frequency, then follow [reference/animation.md](reference/animation.md): ease-out curve, 150-250ms, `transform`/`opacity`, interruptible transitions, reduced-motion branch, accordions via `grid-template-rows`. Override the app's own motion with `!important` only where it is a `mask-image` fade.
- **Assume the app is hostile to long-lived references.** Elements unmount on session switch; re-resolve your container from the DOM rather than caching an element across renders. A popover or menu of your own portals into `<body>`: a plugin mount point can sit under `contain: strict`, which clips a fixed box out of hit-testing.
- **Write model-facing text as if the user reads it.** A tool that feeds the user's timeline (monitor lines, scheduled prompts) shows what the agent writes in a one-line row, so its description tells the agent to print short plain sentences (no raw ids, ISO timestamps or JSON) with one good and one bad example; the row may reword for reading (`native-ui/src/humanize-line.ts`) but the raw text stays in the tooltip and the card. Tool text is the mechanism, not a system-prompt hook; the Code Mode catalog shows parameter docs in full but cuts a description at 117 characters, so the rule goes in the first sentence and the examples in the parameter doc.

## Proportion

Effort is a dial, never a switch. Pick the tier from the change's size and risk (hot path, DOM injection, data flow, shared library), state it in the hand-off with what was skipped and why, and put it in every worker brief. Within a tier, run only the checks and axes that bear on the change.

| Tier | Change | Runs |
|---|---|---|
| T0 | copy, colour, spacing | typecheck, related tests |
| T1 | small logic | + one harness screenshot |
| T2 | new or changed UI | + parity, stress on the relevant axes |
| T3 | hot path or shared lib (timeline, rows, composer, native-ui) | + realistic-data profile on the relevant scenarios |

Spend where the risk is. A cheap check on a risky change is the waste; a full suite on a copy tweak is too.
