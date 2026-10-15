---
name: e2e-code-writer
description: Use when implementing any feature end-to-end in Cortex Notes — wires IPC handlers, preload bridge, renderer UI/state, and CSS together. Invoke before writing code for new features, settings options, panels, or views.
---

You are implementing a feature in **Cortex Notes** — an Electron 29 desktop app (no frameworks, vanilla JS).

## Stack at a Glance

| Layer | Runtime file | What you touch |
|-------|-------------|----------------|
| Main process | `main/main.js` | `ipcMain.handle(channel, handler)` |
| Bridge | `main/preload.js` | `contextBridge.exposeInMainWorld('noteflow', {...})` |
| HTML shell | `renderer/index.html` | DOM elements, modal markup |
| UI logic | `renderer/app.js` | state fields, event listeners, render functions |
| Styles | `renderer/styles.css` | CSS custom properties only (`--accent`, `--bg`, etc.) |
| TS types | `main/types.ts` / `renderer/src/types.ts` | Update when schemas change |

## IPC Contract (never break this)

```js
// main/main.js
ipcMain.handle('domain:action', async (e, payload) => {
  try { return ok(result) } catch(err) { return err(err.message) }
})

// main/preload.js — must be exposed here too
domainAction: (payload) => ipcRenderer.invoke('domain:action', payload)

// renderer/app.js — call via
const res = await window.noteflow.domainAction(payload)
if (!res.success) { /* handle error */ }
```

## Key Conventions

- **Atomic writes:** write `.tmp` → `fs.renameSync` to final path (never write directly)
- **State:** single `state` object in `renderer/app.js` — init all new fields in it
- **UUIDs:** `crypto.randomUUID()` in renderer
- **Timestamps:** `new Date().toISOString()`
- **PINs:** bcryptjs `saltRounds:10` — NEVER plaintext
- **Encryption:** AES-256-GCM via Web Crypto API (PBKDF2 key derivation)
- **No frameworks** — direct DOM manipulation only
- **No comments** on code not already commented
- **No over-engineering** — implement exactly what is asked

## Data Location

`%APPDATA%\noteflow-pro\noteflow-data\` → `notes.json`, `folders.json`, `goals.json`, `tasks.json`, `settings.json`

## Implementation Checklist

Before writing any code, confirm which layers are affected:
- [ ] `main/main.js` — new `ipcMain.handle` needed?
- [ ] `main/preload.js` — new bridge method needed?
- [ ] `renderer/index.html` — new DOM elements?
- [ ] `renderer/app.js` — new state fields + event listeners + render logic?
- [ ] `renderer/styles.css` — new CSS using custom properties?
- [ ] `main/types.ts` — schema changed?
- [ ] `main/store.js` — new settings to persist?

## Output Format

Present changes **file-by-file** in this order:
1. `main/main.js`
2. `main/preload.js`
3. `renderer/index.html`
4. `renderer/app.js`
5. `renderer/styles.css`
6. TypeScript sources (if schema changed)

Each section clearly labeled. Never truncate with `// ... rest unchanged` — show exact placement (e.g., "Add after the `notes:delete` handler:" or "Replace the `saveNote` function:").

After all code: one sentence on how to manually test, and note any edge cases handled.

## Hard Rules

- `contextIsolation:true` / `nodeIntegration:false` — never bypass
- IPC response always `{ success: bool, data?, error? }` via `ok()` / `err()` helpers
- Never `git add -A`
- Backward-compatible schema changes only (existing data must not break)
- `position:fixed` overlays/dropdowns **must be at `<body>` level** — `.ed-tb` has `backdrop-filter` which breaks fixed positioning for any descendant
- Use event delegation (`.closest('[data-x]')`) for dynamically-rendered lists, never `querySelectorAll` at init time

## Planned Feature: License System

Full plan in `docs/LICENSE_PLAN.md`. When implementing license features:
- New main-process files: `main/license-validator.js`, `main/machine-id.js`
- New IPC channels: `license:status`, `license:activate`, `license:deactivate`, `license:openPortal`
- New data file: `%APPDATA%\noteflow-pro\license.json` (AES-256-GCM encrypted, separate from settings.json)
- New state field: `state.license` — loaded at startup via `window.noteflow.license.status()`
- Dependency to add: `@noble/ed25519` (pure-JS, audited, works in Node + browser)
