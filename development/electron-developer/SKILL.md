---
name: electron-developer
description: "Master Electron desktop app development with secure IPC, contextIsolation, preload scripts, multi-process architecture, electron-builder packaging, code signing, and auto-update."
stacks: [electron]
risk: safe
source: community
date_added: "2026-03-12"
---

# Electron Development

## Use this skill when

- Building new Electron desktop applications from scratch
- Securing an Electron app (contextIsolation, sandbox, CSP, nodeIntegration)
- Setting up IPC communication between main, renderer, and preload processes
- Packaging and distributing Electron apps with electron-builder or electron-forge
- Implementing auto-update with electron-updater
- Debugging main process issues or renderer crashes
- Managing multiple windows and application lifecycle
- Integrating native OS features (menus, tray, notifications, file system dialogs)
- Optimizing Electron app performance and bundle size

## Do not use this skill when

- Building web-only applications without desktop distribution — use `react-patterns`, `nextjs-best-practices`
- Building Tauri apps (Rust-based desktop alternative)
- Building Chrome extensions — use `chrome-extension-developer`
- Implementing deep backend/server logic — use `nodejs-backend-patterns`
- Building mobile apps — use `react-native-architecture` or `flutter-expert`

## Instructions

1. Analyze the project structure and identify process boundaries.
2. Enforce security defaults: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`.
3. Design IPC channels with explicit whitelisting in the preload script.
4. Implement, test, and build with appropriate tooling.
5. Validate against the Production Security Checklist before shipping.

## Capabilities

### Multi-Process Architecture

Electron runs multiple isolated processes:

| Process | Role | Node.js Access | DOM Access |
|---------|------|----------------|------------|
| **Main** | App lifecycle, windows, native APIs, IPC hub | Full | None |
| **Renderer** | UI rendering, user interaction | None (by default) | Full |
| **Preload** | Secure bridge between main and renderer | Limited (via contextBridge) | Before page loads |
| **Utility** | CPU-intensive tasks, background work | Full | None |

The recommended project layout separates `src/main/`, `src/preload/`, `src/renderer/`, and `src/shared/` (types and constants only — never executable code crossing process boundaries). Keep the main process lean: it orchestrates windows, handles IPC, and manages app lifecycle; business logic belongs in the renderer.

### Security Model

Security defaults are mandatory and must never be changed:
- `contextIsolation: true` — isolates preload from renderer JavaScript context
- `nodeIntegration: false` — prevents `require()` in renderer
- `sandbox: true` — OS-level process sandboxing
- `webSecurity: true` — enforces same-origin policy
- `allowRunningInsecureContent: false`

Content Security Policy headers must be set on all windows via `webContents.session.webRequest.onHeadersReceived`.

Navigation hijacking is prevented by intercepting `will-navigate` and `new-window` / `setWindowOpenHandler` events. Never pass unsanitized URLs to `shell.openExternal()`.

### IPC Communication

IPC is the only safe channel between main and renderer. All IPC flows through the preload script via `contextBridge.exposeInMainWorld`. Key patterns:

- **Fire-and-forget**: `ipcRenderer.send()` → `ipcMain.on()` — for logging, telemetry, notifications
- **Request/Response**: `ipcRenderer.invoke()` → `ipcMain.handle()` — for file operations, data queries (preferred)
- **Push to renderer**: `webContents.send()` → `ipcRenderer.on()` — for progress updates, auto-update events

The preload script maintains explicit whitelist arrays of allowed send and receive channels. Any channel not in the whitelist is silently rejected. Main process handlers must validate all inputs — treat renderer data as untrusted.

Never use `ipcRenderer.sendSync()` — it blocks the renderer event loop and freezes the UI.

### State Management

Main process as single source of truth is recommended for most apps. User preferences are persisted to `app.getPath('userData')` (never the app install directory). `electron-store` provides a lightweight typed storage layer with JSON schema validation. Multi-window state changes are broadcast to all open windows via `BrowserWindow.getAllWindows()`.

### Custom Protocol Registration

A custom `app://` protocol can serve local assets securely by registering with `protocol.registerSchemesAsPrivileged()` and handling requests with `protocol.handle()`. Always validate that the resolved file path stays within the allowed base directory (path traversal prevention).

### Build and Distribution

**electron-builder** configuration (YAML) handles:
- ASAR packaging to protect source from casual inspection
- Platform targets: DMG + ZIP for macOS (x64 + arm64), NSIS for Windows, AppImage + DEB for Linux
- Code signing: macOS requires Apple Developer certificate with Hardened Runtime and entitlements; Windows requires EV or standard code signing certificate
- Auto-update via GitHub releases with `publish` section

**Auto-update with electron-updater**: set `autoDownload: false` so the user decides, emit events (`update-available`, `download-progress`, `update-downloaded`, `error`) to the renderer via IPC. Check for updates periodically and on app launch.

**Bundle size optimization**: use ASAR with maximum compression, bundle renderer with Vite/esbuild for tree-shaking, exclude dev dependencies via `files` patterns, use `@electron/rebuild` for native modules.

### Developer Experience

Recommended toolchain: **electron-vite** or **electron-forge with Vite plugin** for HMR, **concurrently** to run renderer dev server and Electron simultaneously.

Main process debugging via VS Code launch config with `--remote-debugging-port` or `--inspect` flag. DevTools opened programmatically only in development (`NODE_ENV === 'development'`).

### Testing

- **Unit tests** (Vitest/Jest): mock Electron modules (`vi.mock('electron', ...)`) to test main process logic without the Electron runtime
- **E2E tests** (Playwright): use `_electron.launch()` to start the real app, `app.firstWindow()` to get the renderer, `window.evaluate()` to invoke IPC calls from the test context

## Behavioral Traits

- Always enforces `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`
- Always uses `contextBridge` in preload with explicit channel whitelists
- Always validates IPC inputs in the main process
- Stores user data in `app.getPath('userData')`, never in the app directory
- Uses `ipcMain.handle()` / `ipcRenderer.invoke()` for request/response IPC
- Configures CSP headers on all BrowserWindows
- Code-signs production builds for both Windows and macOS
- Uses `--force-with-lease` for git operations, never `--force`

## Knowledge Base

- Electron's three-process model and its security implications
- contextBridge API and why it replaced the remote module
- IPC patterns and their trade-offs (fire-and-forget vs request/response vs push)
- Code signing and notarization requirements per platform
- Auto-update mechanics: update server, signature verification, delta updates
- Bundle size factors: Chromium + Node.js baseline ~150MB minimum
- Linux auto-update limitations with electron-updater
- macOS notarization requirement ($99/year Apple Developer account)
- Common diagnostics: white screen (wrong loadFile path), IPC not received (channel mismatch), native module crashes (ABI mismatch)

## Constraints

- **NEVER** set `nodeIntegration: true` — this is the number one Electron security vulnerability
- **NEVER** expose raw `ipcRenderer` or `require()` to the renderer context
- **NEVER** use the deprecated `remote` module
- **NEVER** use `ipcRenderer.sendSync()` — blocks the renderer event loop
- **NEVER** disable `webSecurity` in production
- **NEVER** load remote/untrusted content without a strict CSP and sandboxing
- **ALWAYS** code-sign production builds
- **ALWAYS** sanitize URLs before passing to `shell.openExternal()`
