---
name: loadout-system-design
description: >
  Complete system design reference for the Loadout VSCode extension — a GUI panel for
  managing Claude Code agents, skills, and commands as swappable equipment loadouts.
  Use at the start of ANY implementation task to ensure design consistency. Covers:
  two-process architecture (Extension Host Node.js + Angular 21 Webview), postMessage
  protocol, data.js filesystem layer, signal-based state services, storage layout, and
  non-negotiable coding rules. Invoke when implementing stories, adding features,
  reviewing code, making ANY UI/styling change (design tokens, SCSS, components,
  animations), or when any system design question arises in Loadout.
---

# Loadout — System Design Reference

## Quick Navigation

| What you need | Load |
|---|---|
| Two-process overview, file map, state flow, build pipeline | [references/architecture.md](references/architecture.md) |
| Extension entry, src/ modules, data.js API, security model | [references/extension-host.md](references/extension-host.md) |
| Angular 21, state services, DataSyncService, shared primitives | [references/webview-angular.md](references/webview-angular.md) |
| Full message catalogue (WebviewMessage + ExtensionMessage types) | [references/messaging-protocol.md](references/messaging-protocol.md) |
| Domain types, storage paths, profiles, hash/sync mechanics | [references/domain-storage.md](references/domain-storage.md) |
| File size limits, CommonJS rules, Angular rules, git, formatting | [references/coding-rules.md](references/coding-rules.md) |
| Design tokens, color palettes, SCSS mixins, animations, a11y | [references/ui-design-system.md](references/ui-design-system.md) |

---

## Non-negotiable invariants

These apply everywhere, always — no exceptions.

1. **No VSCode API in webview** — never `import vscode` or use `fs`/`path`/`os` from any file under `webview/`.
2. **All filesystem mutations go through `data.js`** — no ad-hoc `fs.writeFileSync` in `src/` modules.
3. **Every Angular component**: `standalone: true` + `ChangeDetectionStrategy.OnPush` — no exceptions.
4. **State in `core/state/*.state.ts` signal services only** — components are dumb views; no component-local mutable state for domain data.
5. **Signals for state, RxJS only for the bridge stream** — no `BehaviorSubject` / `ReplaySubject` for state.
6. **File size cap ~400 lines** — split into a new `src/` module or Angular subcomponent when approaching this.
7. **Profiles store filenames only** — never copy file content into `profiles.json`.
8. **Icons: `lucide-angular` only** — no SVG file imports, no inline `<svg>`.
9. **CommonJS in extension host** — `require()` / `module.exports` in all `.js` root files; `update-claude.mjs` is the sole ESM exception.
10. **Build `webview-dist/` before committing UI changes** — run `cd webview && npm run build`.

---

## Feature implementation checklist

When adding a new feature end-to-end, follow this order:

1. **Domain** — add or extend types in `webview/src/app/core/messages.ts` (single source of truth for all shared types).
2. **Storage** — decide persistence: `profiles.json`, `ui-state.json`, or a new `data.js` function. Update `data.js` and `src/snapshot.js::buildInitialData` if `InitialData` changes.
3. **Extension messages** — add the `WebviewMessage` union variant and/or `ExtensionMessage` variant to `messages.ts`; handle the new case in `src/message-handler.js`.
4. **data.js** — implement the filesystem operation (pure I/O, no VSCode API, no side effects beyond fs).
5. **State service** — update the relevant `core/state/*.state.ts` to expose new signals or a setter; update `DataSyncService.applyData()` if `InitialData` fields changed.
6. **Component** — create a standalone `OnPush` component or extend an existing feature. Inject the state service; never own domain state locally. Send actions via `bridge.send()` in methods, not templates.
7. **Validators** — if new user-supplied input crosses the bridge, add a guard in `src/validators.js` and call it in `message-handler.js` before acting.
8. **Build** — run `cd webview && npm run build`, verify `webview-dist/` is updated.
9. **Git** — stage specific files by name; conventional commit in imperative mood.
