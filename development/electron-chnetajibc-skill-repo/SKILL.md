---
name: electron
description: "Electron with security first: main/renderer/preload/IPC, context isolation, sandbox, CSP, navigation control, signing/auto-update. Use for Electron apps; untrusted content never gains privileges."
---

# electron

Two processes, one hard boundary. The renderer is hostile territory; preload is the only bridge, and it is narrow.

## Activate when

- Building or changing Electron apps: IPC surface, preload scripts, navigation, permissions, packaging, updates.

## Do NOT activate for

- Pure web UI (see frontend/*); Node services (see frameworks/express).

## Procedure

1. Version: detect Electron release from package.json lockfile; research in https://www.electronjs.org/docs/latest/ for that release (defaults for isolation/sandbox changed across majors). Check https://github.com/electron/electron releases for breaking changes.
2. Architecture: main (Node privileges) vs renderer (untrusted) vs preload (minimal typed bridge). `contextIsolation: true`, `sandbox: true`, `nodeIntegration: false`; never relax for convenience.
3. IPC: allowlisted channels with schema-validated payloads both directions; `ipcRenderer` never exposed raw — expose named functions via `contextBridge`; `ipcMain.handle` validates sender frame.
4. Navigation: `will-navigate`/`new-window`/`setWindowOpenHandler` deny-by-default; `webContents` permission handlers deny by default (media, notifications, fullscreen); CSP set; remote content over HTTPS only, and remote content never receives privileged APIs.
5. Native: modules rebuilt for the pinned Electron/Node ABI; auto-update feed over HTTPS with signature verification; code signing (macOS/Windows) before distribution.
6. Secrets/storage: OS keychain via safeStorage for secrets; no tokens in localStorage; clear-session-data on logout.
7. Verify: security checklist review per release, navigation/permission abuse tests, packaged-app smoke test with update check, signed installer confirmed.

## Failure modes

- `nodeIntegration: true` for debugging left on; preload exposing entire modules; `shell.openExternal` on unvalidated URLs; loading remote content with privileges; unsigned auto-updates.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (electron).
