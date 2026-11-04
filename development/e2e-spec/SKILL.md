---
name: e2e-spec
description: Write, run and debug the WebdriverIO + tauri-driver end-to-end specs of EasyTask (e2e/), and measure UI lag in the real app. Use when a user flow is added or changed, when an e2e test fails, or to measure UI lag in the real app
---

# WebdriverIO E2E spec (EasyTask)

`e2e/wdio.conf.ts` builds the debug app (`tauri build --debug --no-bundle`), creates a temporary `EASYTASK_DATA_DIR` (real data is never touched), starts `tauri-driver` (port 4444) per session and drives the real app: WebView2 + msedgedriver on Windows, WebKitGTK + WebKitWebDriver under xvfb on Linux. Mocha bdd, timeout 120 s, `waitforTimeout` 10 s, `maxInstances: 1`. Specs are `e2e/specs/**/*.e2e.ts`. Failure screenshots and logs go to `e2e/output/`.

## Running it

```
npm run e2e                    # build + all specs
E2E_SKIP_BUILD=1 npm run e2e   # reuse the existing debug binary
npm run e2e:typecheck          # tsc -p e2e/tsconfig.json (also run by CI, "frontend" job)
npm run ui-tour                # screenshot tour (e2e/ui-tour), not part of the regular run
```

- Other env vars read by `wdio.conf.ts`: `E2E_APP=<exe>` (custom binary), `E2E_NATIVE_DRIVER=<path>`, `E2E_EDGE_ARGS` (extra WebView2 args), `E2E_DRIVER_LOG=1` (verbose msedgedriver log).
- Windows: run from a NON-elevated terminal. In an Administrator shell WebView2 does not open its debug port ("DevToolsActivePort file doesn't exist"). `e2e/run-as-basic-user.cmd` runs the suite with a limited token. For the same reason the Windows e2e CI job runs only on `workflow_dispatch`; Linux runs on every push. The user parked that issue: do not reopen it unless asked.
- Linux CI e2e can flake: rerun the failed jobs before investigating.
- CI e2e job is `continue-on-error`; it uploads `e2e/output` as `e2e-output-<os>`.
- Known: locally "empties the trash" fails on the Windows dev build (passes on Linux CI); there is no e2e for export/import yet (native dialogs, see the manual checklist in `e2e/README.md`).
- Keep the current @wdio major (9): the 10 upgrade was left out on purpose (needs expect-webdriverio 8 and rewriting e2e code: `executeAsync` is gone).

## Helpers (`e2e/helpers.ts`)

- `currentLang()` / `trIn(lang, key, vars)` / `tr(key, vars)`: read `<html lang>` and look labels up in `src/i18n/locales` (never hard-code UI strings).
- `byLabel(label)` / `allByLabel(label)`: element(s) by `aria-label`.
- `byText(text, scope?)`: button/radio/menuitem/tab whose visible text is exactly `text`.
- `addTaskButton(scope)`: the "+" add-task button of a section card.
- `groupCard(label)` / `newSectionInGroup(group, title)` / `directTasks(group)` / `groupAddTaskButton(group)` / `addTaskToGroup(group, text)`: a group card (`[data-group-card]`), a new section from the group menu (there is no section button), and the direct tasks area with its "Nuovo task" button.
- `menuButtonPredicate()` / `menuButton(scope)`: the "..." menu button ("Apri menu" or "Menu: <name>").
- `topDialog()`: last open `dialog`/`alertdialog`.
- `waitForApp()`: waits until `#root` has rendered.
- `typeInto(input, value)`: click (retried, reports what covers the field) + setValue, with a native-setter fallback for WebKitWebDriver dropping Shift.
- `createWorkspace(name)` / `openWorkspace(name)`: home page flow (create retries the click until the dialog opens).
- `createFromSidebar(buttonKey, submitKey, name)`: folder/note dialogs with a `name` field.
- `treeRow(name)` / `sectionCard(title)`: sidebar `treeitem` / `[data-section-card]` by name.
- `openContextMenu(target)`: right click, returns the `[role=menu]`.
- `openSubmenu(menu, triggerText, item)`: Radix submenu, with ArrowRight fallback (hover is unreliable on WebKitGTK).
- `domClick(element)`: click through the DOM when a tooltip covers the target on WebKitGTK.
- `cssColor`, `compose`, `contrastRatio`, `backgroundOf`, `inTheme(theme, fn)`: computed colors and WCAG contrast in light/dark.
- `dataDir()` / `dbUrl()` / `sql(kind, query, values)`: app data folder and direct SQLite access through the page's sql plugin (assert what was saved).

## Writing a spec

1. New file `e2e/specs/<topic>.e2e.ts`; imports from `@wdio/globals` (`$`, `$$`, `browser`, `expect`) and `../helpers`.
2. Specs run in separate sessions, one at a time, on the SAME data folder: use unique names (`"Feat Workspace"`, `"Audio Note"`...) and do not depend on file order. Inside a spec, `it`s run in order and build on each other (create workspace, open it, act, assert).
3. Start with `waitForApp()`, then `createWorkspace` / `openWorkspace`.
4. Select by role/`aria-label`/visible text via `tr(key)`; use xpath only for structure (`treeRow`, `sectionCard`). Prefer `waitForDisplayed` / `waitUntil({ timeoutMsg })` over `pause`; always give a `timeoutMsg`.
5. Check persistence with `sql(...)` (see `savedOrder` in `features.e2e.ts`) and wait for the write before undo/reload.
6. Toasts: `[data-sonner-toast]`; the automations spec waits for old toasts to disappear first (`noToasts`) so they cannot cover targets or be confused with new ones.
7. Run `npm run e2e:typecheck`, then the suite (non-elevated terminal on Windows).

## Pitfalls

- Opening submenus, hovering and tooltips behave differently on WebKitGTK: use `openSubmenu` / `domClick`.
- Right after start the home page can still redraw and swallow a click: the helpers retry, do the same in new helpers.
- The driver does not share the webview profile across sessions: localStorage (theme) is lost on restart.
- Unit tests are separate (vitest + jsdom, `npm run test`). jsdom matches `:focus-visible` on every focus, so focus-visible behaviour needs the real app (e2e) or a stub.

## Measuring UI lag in the real app

1. Scratch spec (do not commit) with a wdio config extending `e2e/wdio.conf.ts` (see `e2e/ui-tour/wdio.ui-tour.conf.ts`: `{ ...base, specs: [...] }`).
2. `EASYTASK_DATA_DIR` pointing to a COPY of the user's db (never the original in `Documents\EasyTask\easytask.db`). Note `onPrepare` overrides it with a fresh temp dir: set it so the copy is used (or adapt the scratch config); verify before trusting numbers.
3. `E2E_APP=<exe>` and `E2E_SKIP_BUILD=1`.
4. Drag with `browser.action("pointer")` in ~40 steps; in the page record `requestAnimationFrame` deltas and a `PerformanceObserver("longtask")`. Compare frame mean/p95 and long task count before/after the change.
5. Pitfall: `src-tauri/target/debug/EasyTask.exe` may be the `tauri dev` build (Vite dev server, React dev mode, much slower). For production-like numbers: `CARGO_TARGET_DIR=<short path> npm run tauri -- build --debug --no-bundle` (long paths fail with LNK1104), then point `E2E_APP` at that exe.
