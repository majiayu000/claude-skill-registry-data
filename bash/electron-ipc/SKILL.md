---
name: electron-ipc
description: "World Pulse: When adding communication between the Electron main process (`src/main/main.ts`) and the renderer (`src/renderer/`), or modifying the preload script."
---

# Electron IPC

**When to use:** When adding communication between the Electron main process (`src/main/main.ts`) and the renderer (`src/renderer/`), or modifying the preload script.

---

## Architecture (from `src/main/main.ts`)

World Pulse uses Electron with an **embedded backend** launched via Node `fork()`:

```
main process (Electron)
  └── BrowserWindow (renderer)
        └── preload.ts (context bridge)
  └── child_process.fork() → server/index.ts (Express + Socket.io)
```

The renderer communicates with the backend through **Socket.io over HTTP** — not through IPC. IPC is reserved for system-level operations (window management, native dialogs, file access).

---

## Security Baseline (enforced in `main.ts`)

```ts
new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, '../preload/index.js'),
    contextIsolation: true,   // REQUIRED — never set to false
    nodeIntegration: false,   // REQUIRED — never set to true
  },
});
```

These two settings are **non-negotiable**. Any PR that weakens them must be rejected.

---

## Preload Pattern (`src/main/preload.ts`)

The preload script is the only place Node.js APIs are exposed to the renderer. Use `contextBridge`:

```ts
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electron', {
  // Whitelist only specific, typed methods
  getVersion: () => ipcRenderer.invoke('get-version'),
  openExternal: (url: string) => ipcRenderer.invoke('open-external', url),
});
```

Rules:
- Expose **only** the methods the renderer actually needs.
- Validate and sanitize all arguments before passing to `ipcRenderer`.
- Never expose the raw `ipcRenderer` object.
- Never use `ipcRenderer.sendSync` — it blocks the main process.

---

## Main Process IPC Handlers

```ts
import { ipcMain, shell } from 'electron';

ipcMain.handle('get-version', () => app.getVersion());

ipcMain.handle('open-external', (_event, url: string) => {
  // Validate URL before opening — never trust renderer input
  if (url.startsWith('https://')) {
    return shell.openExternal(url);
  }
});
```

Always use `ipcMain.handle` (async) over `ipcMain.on` for two-way communication.

---

## External Link Handling

External links in the renderer open in the system browser, not Electron:

```ts
mainWindow.webContents.setWindowOpenHandler(({ url }) => {
  shell.openExternal(url);
  return { action: 'deny' };
});
```

This is already wired in `main.ts`. Do not add `<a target="_blank">` without this handler.

---

## Backend Lifecycle

The server is started via `fork()` before the window is created:

```ts
function startBackendServer(): void {
  serverProcess = fork(serverEntry, [], {
    env: { ...process.env, PORT: String(SERVER_PORT) },
    execArgv: is.dev ? ['--import', 'tsx'] : [],
    stdio: 'pipe',
  });
}

app.whenReady().then(() => {
  startBackendServer();
  createWindow();
});
```

On quit, `serverProcess.kill()` must be called to avoid orphaned processes. The `app.on('before-quit')` hook handles this.

---

## Anti-Patterns

- **Never** set `nodeIntegration: true` or `contextIsolation: false`.
- **Never** use `remote` module — it was deprecated and removed.
- **Never** load remote URLs in BrowserWindow without `will-navigate` validation.
- **Never** pass unsanitized renderer input directly to `shell.openExternal`.
- **Never** use `require()` in the renderer — use the context bridge.
- Do not add `webSecurity: false` even in development.
