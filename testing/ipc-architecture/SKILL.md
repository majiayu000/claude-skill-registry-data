---
name: ipc-architecture
description: "How to add or change an IPC channel in Struq Voice end to end. Use whenever a task involves IPC, a preload bridge, a channel, a payload type, window.struqVoice, invoke/send/on across main and renderer, or the PRELOAD_CHANNELS mechanism. Explains the single-source rule, the sandboxed-preload argv trick, the three file touch points (shared/ipc.ts, src/main/ipc.ts, preload + api), and the testing pattern. NOT for general gating (use verification-gates) or the capture state machine (use capture-session)."
argument-hint: "[add-channel | payload | preload | main-window-api]"
---

# IPC architecture in Struq Voice

Every channel is declared in `src/shared/ipc.ts` and nowhere else. There is
no second source. This is enforced by convention and is the first thing to
check when IPC "does not work": the name on the sender must equal the name on
the handler.

## Why the preloads work the way they do

Every window runs sandboxed (`sandbox: true`), so preloads cannot `import`
shared modules: each preload bundle must be one self-contained file. To give
the preload the channel names, main serializes `PRELOAD_CHANNELS` (exported
from `src/shared/ipc.ts`) into the window's `additionalArguments` as
`--struq-channels=...`, and each preload reads them from `process.argv`
before exposing its API via `contextBridge`.

## Adding a channel, end to end

1. **`src/shared/ipc.ts`**: declare the channel constant
   (`export const fooChannel = "foo:bar" as const;`), the request and result
   payload interfaces, and, if the preload needs it, add the channel under
   the matching group in `PRELOAD_CHANNELS` (top-level keys: `appGetVersion`,
   `window`, `captureStateChanged`, `captureLevelsChanged`, `recorder`,
   `history`, `clipboard`, `settings`, `devices`, `openRouterKey`, `models`,
   `metrics`).
2. **`src/shared/api.ts`**: add the method to the relevant `*WindowApi`
   interface (`MainWindowApi`, `OverlayWindowApi`, `RecorderWindowApi`).
3. **`src/preload/<window>.ts`**: implement it with `ipcRenderer.invoke` /
   `ipcRenderer.send` / `ipcRenderer.on`, using the argv-read channel names.
   For main-to-renderer pushes, return an unsubscribe function.
4. **`src/main/ipc.ts`**: register `ipcMain.handle` / `ipcMain.on` for the
   channel. This file is thin typed dispatch only; no business logic. If the
   handler needs a new dependency (a store, service or window), extend the
   `registerIpcHandlers(...)` signature and update the call site in
   `src/main/index.ts`.
5. **Renderer**: call `window.struqVoice` (typed as the window's API). Never
   construct channel names in the renderer.

## Testing pattern

- Pure logic behind IPC is unit tested directly (settings migration,
  engine router, text cleanup, paste decisions) with injected deps.
- The main-process test hook (`src/main/test-hook.ts`) exposes drives and
  accessors for e2e. Add accessors there when a new surface needs e2e
  coverage, following the existing `getState` / `history.getRecent` pattern.
- Payloads cross IPC as plain JSON; use `readonly` on interfaces and
  `exactOptionalPropertyTypes` (never send `undefined` fields).

## Gotchas

- `ipcMain.handle` returns a Promise; `ipcMain.on` is fire-and-forget.
- Transferable `ArrayBuffer` (PCM) travels via `ipcRenderer.send` with the
  transfer list, never `invoke`.
- Do not pass API keys or secrets across IPC. The key stays in main; the
  renderer only ever asks for a masked status.
