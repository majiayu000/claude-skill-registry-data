---
name: dl-electron-react
description: Build, scaffold, and structure cross-platform desktop applications using Electron with React and TypeScript. Use for Electron architecture, secure IPC, preload/contextBridge APIs, React renderers, packaging, or Electron security reviews. Preserve an existing build tool and conventions; electron-vite and electron-builder are suitable defaults for a new app, not requirements.
---

# Electron + React (TypeScript)

This skill builds desktop apps with React and TypeScript while keeping the renderer isolated from operating-system access. Choose the project's existing build and packaging tooling. For a new project, electron-vite and electron-builder are practical defaults, but Electron Forge or a custom Vite setup can be equally appropriate when requested or already established.

Electron has three "worlds" and the whole architecture hinges on respecting their boundaries:

- **Main process** — Node.js. Owns windows, the OS, the filesystem, native dialogs. One per app.
- **Renderer process** — Chromium. Runs your React app. Should have **zero** direct Node/OS access.
- **Preload script** — the only bridge. Runs before the renderer loads, with access to a limited Node surface, and exposes a *narrow, explicit* API to the renderer via `contextBridge`.

Getting this boundary right is the single most important thing. A renderer with `nodeIntegration: true` is a remote-code-execution hole; a renderer that talks to the OS only through a hand-written, validated preload API is safe. The rest of this skill keeps you on the safe side by default.

## Choosing the path

For a new project, the official electron-vite React template is a convenient default. It gives a familiar React layout with an `electron/` folder on top, HMR for the renderer, hot-reload for main/preload, and TypeScript wired up. Do not replace an existing build system merely to adopt it.

| Situation | What to do |
|---|---|
| New app from scratch | Scaffold with the template (see "Scaffolding" below) |
| Existing Vite/React app, wants desktop | Inspect its build scripts and add Electron using a compatible integration; keep the renderer and tooling conventions intact |
| Existing Electron app, wants help | Read their `electron.vite.config.ts` / `vite.config.ts` and `package.json` first, then match their conventions — don't rewrite their setup |
| Just an IPC / security question | Jump to `references/ipc-and-security.md`, no scaffolding needed |

When in doubt about a setup detail (versions, plugin APIs, builder targets), prefer reading the relevant reference file below over guessing — Electron's APIs shift between major versions.

## Scaffolding a new project

Use the official template. It's the least-surprising starting point and stays current:

```bash
npm create @quick-start/electron@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

This produces the canonical layout. Internalize it — every file below has a specific job:

```
my-app/
├── electron.vite.config.ts     # one config, three builds: main / preload / renderer
├── electron-builder.yml        # packaging & distribution targets
├── package.json                # "main" points to out/main/index.js
├── tsconfig.json               # references the two tsconfigs below
├── tsconfig.node.json          # main + preload (Node env)
├── tsconfig.web.json           # renderer (DOM env)
├── src/
│   ├── main/
│   │   └── index.ts            # app lifecycle, BrowserWindow, ipcMain handlers
│   ├── preload/
│   │   ├── index.ts            # contextBridge.exposeInMainWorld(...)
│   │   └── index.d.ts          # types for window.api — shared with renderer
│   └── renderer/
│       ├── index.html
│       └── src/
│           ├── main.tsx        # React entry / createRoot
│           ├── App.tsx
│           └── ...             # your components, hooks, etc.
└── resources/                  # icons, native assets bundled into the app
```

electron-vite is useful when starting fresh because it builds the main, preload, and renderer targets from one config and handles their dev/production loading split. It is not a prerequisite for secure Electron IPC or for maintaining an existing application.

If the user wants **electron-builder vs electron-forge**: this skill standardizes on electron-builder (what the template ships with). It's mature, config-driven via one YAML file, and covers Windows/macOS/Linux targets plus auto-update. Only switch to Forge if the user explicitly asks.

## The non-negotiable security baseline

Every `BrowserWindow` you create MUST use these `webPreferences`. This is the difference between a safe app and an exploitable one — never relax them to "make something work"; if something needs Node, it belongs in the main process behind an IPC handler.

```ts
const win = new BrowserWindow({
  // ...
  webPreferences: {
    preload: join(__dirname, '../preload/index.js'),
    sandbox: true,            // renderer runs sandboxed
    contextIsolation: true,   // renderer & preload have separate JS contexts
    nodeIntegration: false,   // NO Node globals in the renderer
  },
})
```

`contextIsolation: true` + `nodeIntegration: false` + `sandbox: true` is the trio. With these on, the *only* way the renderer can reach the OS is through what the preload explicitly exposes. That's the whole point.

Full reasoning, the validation pattern for IPC inputs, and how to handle the rare cases that need to relax `sandbox` (native modules in preload) are in **`references/ipc-and-security.md`** — read it before writing or reviewing any IPC code.

## Wiring IPC — the typed three-file pattern

Cross-process communication should be **one typed contract touched in exactly three places**. When you add a feature that crosses the boundary, edit all three together so types stay honest:

1. **`src/main/index.ts`** — register a handler with `ipcMain.handle('channel', ...)` (use `handle`/`invoke` for request→response; `on`/`send` only for fire-and-forget or main→renderer pushes).
2. **`src/preload/index.ts`** — expose a function that calls `ipcRenderer.invoke('channel', ...)` through `contextBridge`. Never expose `ipcRenderer` itself.
3. **`src/preload/index.d.ts`** — declare the shape on `window.api` so the renderer gets autocomplete and type-checking.

A complete, copy-adaptable example of all three files (plus the renderer call site) lives in **`references/ipc-and-security.md`**. The guiding rule: expose *specific, named operations* (`api.readConfig()`, `api.saveFile(data)`), never generic escape hatches (`api.invoke(anyChannel, anyArgs)`) — a generic bridge re-opens the hole `contextIsolation` closed.

Each main-process handler must also verify that the sender is an expected, currently loaded application frame before acting. Input validation alone does not prevent a navigated, compromised, or unexpected renderer from invoking a privileged channel. Establish a deliberate navigation and external-link policy for every window; the reference includes both checks.

## Common build & packaging tasks

For anything beyond `npm run dev`, read **`references/build-and-packaging.md`**. It covers:

- `electron.vite.config.ts` structure (the three-build config and common plugins)
- Dev vs. production window loading (`loadURL(devServerUrl)` vs `loadFile(builtHtml)`)
- `electron-builder.yml` targets for Windows (nsis), macOS (dmg), Linux (AppImage/deb)
- App icons, `resources/` handling, and `asar` packaging
- Auto-update basics and code-signing pointers
- Environment variables and the `import.meta.env` / `process.env` split across processes

## Conventions to keep the codebase clean

- **Keep the renderer "dumb" about Electron.** React components call `window.api.something()`; they should not know whether that's a file read or a network call. This keeps components testable and portable.
- **State management: use Zustand in the renderer.** It's tiny, hook-based, and provider-free. In the renderer it works exactly as in any web app — what's Electron-specific is bridging the store to the main process (hydrating from disk/OS, persisting back, and reacting to main→renderer pushes). Keep that bridge inside store actions, not components. The pattern is in `references/ipc-and-security.md` §8. Durable data stays authoritative in main (e.g. `electron-store`); the Zustand store mirrors it.
- **One IPC channel = one purpose.** Name channels by intent (`dialog:openFile`, `store:get`), not by mechanism.
- **Validate every IPC input in the main process.** The renderer is the untrusted side of the boundary — treat its arguments like form input from the internet.
- **Put shared types in a place both sides import.** `src/preload/index.d.ts` for the bridge API; a `src/shared/` folder for domain types used in both processes.
- **Don't block the main process.** Heavy CPU work goes in a `utilityProcess`, worker thread, or child process — a blocked main process freezes every window.
- **Match the existing project's style** when editing an established app; the conventions above are defaults for greenfield work, not edicts to impose on someone's running codebase.

## Quick reference: which file do I read?

- IPC, preload, contextBridge, security flags, "is this safe?", renderer state with Zustand → `references/ipc-and-security.md`
- Vite config, electron-builder, packaging, icons, auto-update, env vars → `references/build-and-packaging.md`
- A starting `electron.vite.config.ts` or `electron-builder.yml` to copy → `assets/`
