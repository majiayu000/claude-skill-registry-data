---
name: initialize-game-repo
description: Initialize a modern React, Vite, Babylon.js, and Electron game repository with web and desktop scripts.
---

# Initialize Game Repo

Use this skill when a user wants to bootstrap a 3D web game or prototype repository that runs in the browser and can also launch as an Electron desktop app.

## Goals

Create a small, working starter project with:

- React latest with Vite.
- Babylon.js packages for 3D scene work.
- A simple full-window Babylon scene to edit from.
- Source files under `app/`, not `src/`.
- Electron files under `electron/`.
- Kebab-case naming for `.ts` and `.tsx` files.
- Web scripts named `*:web`.
- Desktop scripts named `*:desktop`.

## Recommended Setup

If the target folder is empty, scaffold Vite React in place:

```powershell
npm create vite@latest . -- --template react
```

If the scaffold does not apply the React template cleanly, convert the generated project manually:

- Use `index.html` with `<div id="root"></div>`.
- Point the module script to `/app/main.tsx`.
- Add `vite.config.ts` with the React plugin.
- Set `jsx: "react-jsx"` in `tsconfig.json`.
- Include `app` in `tsconfig.json`.

Install runtime dependencies:

```powershell
npm install react@latest react-dom@latest babylonjs@latest react-babylonjs@latest @babylonjs/core@latest @babylonjs/loaders@latest
```

Install dev dependencies:

```powershell
npm install -D @vitejs/plugin-react@latest @types/react@latest @types/react-dom@latest electron@latest concurrently@latest wait-on@latest
```

## File Layout

Use this shape:

```text
app/
  app.tsx
  babylon-scene.tsx
  main.tsx
  styles.css
electron/
  main.cjs
  preload.cjs
index.html
package.json
tsconfig.json
vite.config.ts
```

Keep all project-owned `.ts` and `.tsx` file names in kebab-case. `main.tsx` is already compliant.

## Vite Configuration

Use `base: './'` so production assets load correctly from Electron's `file://` path:

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: './',
  plugins: [react()],
})
```

## Package Scripts

Use explicit web and desktop script names:

```json
{
  "main": "electron/main.cjs",
  "scripts": {
    "dev:web": "vite",
    "build:web": "tsc && vite build",
    "start:web": "vite preview",
    "dev:desktop": "concurrently -k \"vite --host 127.0.0.1\" \"wait-on tcp:127.0.0.1:5173 && electron .\"",
    "build:desktop": "npm run build:web",
    "start:desktop": "electron ."
  }
}
```

## Electron Main Process

Create `electron/main.cjs` using CommonJS so it works cleanly in a package with `"type": "module"`:

```js
const { app, BrowserWindow, shell } = require('electron')
const path = require('node:path')

const isDev = process.env.npm_lifecycle_event === 'dev:desktop'

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 960,
    minHeight: 640,
    backgroundColor: '#070b12',
    title: 'Game',
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      preload: path.join(__dirname, 'preload.cjs'),
    },
  })

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  if (isDev) {
    mainWindow.loadURL('http://127.0.0.1:5173')
    mainWindow.webContents.openDevTools({ mode: 'detach' })
  } else {
    mainWindow.loadFile(path.join(__dirname, '..', 'dist', 'index.html'))
  }
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
```

Create `electron/preload.cjs` with only minimal, safe context exposure:

```js
const { contextBridge } = require('electron')

contextBridge.exposeInMainWorld('desktop', {
  platform: process.platform,
})
```

## Babylon Scene

Create a simple scene in `app/babylon-scene.tsx` with:

- A canvas ref.
- `Engine` and `Scene` lifecycle inside `useEffect`.
- `ArcRotateCamera` attached to the canvas.
- A `HemisphericLight`.
- A ground mesh and one or two starter meshes.
- A render loop.
- Cleanup for resize listener, scene, and engine.

Keep the canvas full-window and set `touch-action: none` in CSS.

## Verification

Run at least:

```powershell
npm run build:web
```

If Electron is installed and available, also verify:

```powershell
npm run build:desktop
```

Use `npm run dev:web` for browser development and `npm run dev:desktop` for Electron development.

## Git Publish Notes

Before committing or pushing:

- Inspect `git status -sb`.
- Stage only intended project files.
- Do not commit `node_modules/` or `dist/`.
- Verify there is a configured remote before pushing.
- If GitHub auth is invalid, commit locally and tell the user that push is blocked until auth is repaired.
