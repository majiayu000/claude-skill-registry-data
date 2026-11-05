---
name: electron-dev
description: Development workflow, build commands, and IPC patterns for the Electron+React+Vite image gallery application.
---

# Electron Development Workflow

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev mode (Vite HMR + Electron) |
| `npm run build` | Production build + electron-builder |
| `npm run lint` | ESLint checks |
| `./run.bat` | Shortcut launcher for dev mode |

## Architecture

```
Main Process (Node.js)          Renderer Process (Chromium)
┌─────────────────────┐         ┌──────────────────────────┐
│ electron/main.ts    │◄─IPC──►│ src/main.tsx             │
│ electron/db.ts      │         │ src/App.tsx              │
│ electron/preload.ts │         │ src/components/...       │
│ electron/nefExtractor.ts│     │ src/hooks/...            │
└─────────────────────┘         └──────────────────────────┘
```

- **Main Process** (`electron/`): DB operations, file system, OS integration
- **Renderer Process** (`src/`): React UI, hooks, state
- **Bridge**: `contextBridge` in `preload.ts` exposes `window.electron` API

## Adding a New IPC Handler (Step-by-Step)

This is the most common task. Follow these 4 files in order:

### Step 1: Database function in `electron/db.ts`

```typescript
export async function getMyData(options: MyOptions = {}): Promise<MyResult[]> {
    return query<MyResult>('SELECT ... FROM ... WHERE ...', []);
}
```

### Step 2: IPC handler in `electron/main.ts`

Add inside `app.whenReady().then(() => { ... })`:

```typescript
ipcMain.handle('db:my-channel', async (_, options) => {
    try {
        return await db.getMyData(options);
    } catch (e: any) {
        console.error('DB Error:', e);
        return [];
    }
});
```

### Step 3: Expose in `electron/preload.ts`

```typescript
getMyData: (options?: any) => ipcRenderer.invoke('db:my-channel', options),
```

### Step 4: Declare types in `src/electron.d.ts`

Add to the `Window.electron` interface:

```typescript
getMyData: (options?: { limit?: number; offset?: number }) => Promise<any[]>;
```

### Step 5: Use in React

```typescript
const data = await window.electron.getMyData({ limit: 50 });
```

## Key Patterns

### Media Protocol
Images are served via a custom `media://` protocol registered in `main.ts`. To display an image:
```typescript
const src = `media://${image.thumbnail_path || image.file_path}`;
```

### WSL Path Conversion
The DB stores WSL-style paths (`/mnt/d/...`). The `convertPathToLocal()` function in `main.ts` converts them to Windows paths (`D:/...`). Any new path handling must account for this.

### Config Loading
`config.json` at project root provides DB credentials and dev server URL. Both `main.ts` and `db.ts` load it independently via `loadConfig()`.

## Tech Stack

| Package | Version | Purpose |
|---------|---------|---------|
| `electron` | 40.x | Desktop runtime |
| `react` | 19.x | UI framework |
| `vite` | 7.x | Build tool + HMR |
| `typescript` | 5.9 | Type safety |
| `pg` | 8.x | PostgreSQL DB client |
| `zustand` | 5.x | State management |
| `react-virtuoso` | 4.x | Virtualized grid |
| `exiftool-vendored` | 35.x | EXIF/RAW metadata |
| `libraw-wasm` | 1.x | Client-side RAW decode |
| `lucide-react` | 0.5x | Icons |

## Troubleshooting

1. **App won't start**: Check PostgreSQL is running (Docker container on `localhost:5432`)
2. **Blank gallery**: Check Electron main process console for DB errors
3. **Images not loading**: Verify `media://` protocol and WSL path conversion
4. **Type errors**: Run `npm run lint` — check `electron.d.ts` matches `preload.ts`
