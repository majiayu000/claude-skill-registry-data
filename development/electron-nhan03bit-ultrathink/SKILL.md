---
name: electron
description: Cross-platform desktop applications with web technologies (Chromium + Node.js)
layer: domain
category: desktop
triggers:
  - "electron app"
  - "desktop app"
  - "BrowserWindow"
  - "ipcMain"
  - "ipcRenderer"
  - "electron-builder"
  - "contextBridge"
  - "preload script"
linksTo:
  - react
  - typescript-frontend
  - nodejs
  - pwa
linkedFrom:
  - code-writer
riskLevel: medium
---

# Electron

Framework for building cross-platform desktop applications using Chromium and Node.js. Ships a single codebase as native apps for macOS, Windows, and Linux.

## When to Use

- Desktop apps needing OS-level access (file system, tray, notifications)
- Wrapping an existing web app as a native desktop experience
- Offline-first apps with local data storage
- Cross-platform tools where native UI per-platform is not justified

## Key Patterns

**Main vs Renderer Process** — Main process (Node.js) manages windows, system APIs, and app lifecycle. Renderer processes (Chromium) handle UI. Never run privileged code in the renderer.

**IPC Communication** — Use `contextBridge.exposeInMainWorld()` in preload scripts to expose APIs safely. Communicate via `ipcMain.handle()` / `ipcRenderer.invoke()` (async) or `ipcMain.on()` / `ipcRenderer.send()` (fire-and-forget).

**Security Model** — Always enable `contextIsolation: true` and `sandbox: true`. Never set `nodeIntegration: true` in production. Validate all IPC inputs in main process. Use `safeStorage` for sensitive data.

**BrowserWindow Configuration** — Set `webPreferences.preload` to a dedicated preload script. Use `minWidth`/`minHeight` for sizing constraints. Enable `titleBarStyle: 'hiddenInset'` on macOS for frameless look.

**Auto-Update** — Use `electron-updater` with `autoUpdater.checkForUpdatesAndNotify()`. Publish to GitHub Releases or a private feed. Sign builds for macOS (notarization) and Windows (code signing).

**Tray & Menu System** — Create `Tray` in main process. Build menus with `Menu.buildFromTemplate()`. Use `nativeImage` for icons.

**Native File System** — Use `dialog.showOpenDialog()` / `dialog.showSaveDialog()` from main process, exposed via IPC. Never give renderer direct `fs` access.

**Packaging (electron-builder)** — Configure in `package.json` or `electron-builder.yml`. Target `dmg`+`zip` (macOS), `nsis` (Windows), `AppImage`+`deb` (Linux). Use `files` array to control included resources.

**Protocol Handlers** — Register custom protocols with `protocol.handle('app', handler)` for loading local resources securely instead of `file://` URLs.

**Context Isolation** — Always pair `contextIsolation: true` with a preload script. The preload runs in an isolated context with access to Node.js APIs but exposes only explicit bindings to the renderer.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| `nodeIntegration: true` | RCE via XSS | Use preload + contextBridge |
| Bundling unused locales | +40MB app size | Exclude via electron-builder config |
| Synchronous IPC (`sendSync`) | Blocks renderer, freezes UI | Use async `invoke`/`handle` |
| No code signing | OS warnings, update fails | Sign + notarize all builds |
| Single BrowserWindow for all | Memory bloat, no isolation | Separate windows for heavy features |
| Secrets in renderer | Exposed via DevTools | Use `safeStorage` in main process |
