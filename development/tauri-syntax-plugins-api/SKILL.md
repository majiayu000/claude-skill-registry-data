---
name: tauri-syntax-plugins-api
description: >
  Use when using any official Tauri 2 plugin, accessing the file system, making HTTP requests, showing dialogs, or resolving app directories.
  Prevents missing plugin initialization in Builder, missing npm packages, and absent permission entries.
  Covers fs, dialog, http, notification, shell, clipboard, os, process, updater, store, opener, path API, and isTauri().
  Keywords: tauri plugin, fs, dialog, http, notification, shell, clipboard, store, updater, BaseDirectory, convertFileSrc.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-plugins-api

## Quick Reference

### Plugin Setup Matrix

| Plugin | Cargo Crate | npm Package | Default Permission |
|--------|-------------|-------------|-------------------|
| File System | `tauri-plugin-fs = "2"` | `@tauri-apps/plugin-fs` | `fs:default` |
| Dialog | `tauri-plugin-dialog = "2"` | `@tauri-apps/plugin-dialog` | `dialog:default` |
| HTTP | `tauri-plugin-http = "2"` | `@tauri-apps/plugin-http` | `http:default` |
| Notification | `tauri-plugin-notification = "2"` | `@tauri-apps/plugin-notification` | `notification:default` |
| Shell | `tauri-plugin-shell = "2"` | `@tauri-apps/plugin-shell` | `shell:default` |
| Clipboard | `tauri-plugin-clipboard-manager = "2"` | `@tauri-apps/plugin-clipboard-manager` | (none, explicit only) |
| OS | `tauri-plugin-os = "2"` | `@tauri-apps/plugin-os` | `os:default` |
| Process | `tauri-plugin-process = "2"` | `@tauri-apps/plugin-process` | `process:default` |
| Updater | `tauri-plugin-updater = "2"` | `@tauri-apps/plugin-updater` | `updater:default` |
| Store | `tauri-plugin-store = "2"` | `@tauri-apps/plugin-store` | `store:default` |
| Opener | `tauri-plugin-opener = "2"` | `@tauri-apps/plugin-opener` | `opener:default` |

### Plugin Installation Steps

For EVERY plugin, ALWAYS perform these three steps:

1. **Cargo.toml**: Add the crate to `[dependencies]` in `src-tauri/Cargo.toml`
2. **npm**: Install the JS package with `npm install @tauri-apps/plugin-<name>`
3. **Capability**: Add permissions to `src-tauri/capabilities/default.json`

Additionally, register the plugin in Rust:

```rust
// src-tauri/src/lib.rs
tauri::Builder::default()
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_dialog::init())
    // ... other plugins
```

### Path API Directory Functions

| Function | Description | Example (Windows) |
|----------|-------------|-------------------|
| `appDataDir()` | App-specific data | `C:\Users\X\AppData\Roaming\com.app` |
| `appConfigDir()` | App-specific config | `C:\Users\X\AppData\Roaming\com.app` |
| `appLocalDataDir()` | App-specific local data | `C:\Users\X\AppData\Local\com.app` |
| `appCacheDir()` | App-specific cache | `C:\Users\X\AppData\Local\com.app` |
| `appLogDir()` | App-specific logs | `C:\Users\X\AppData\Roaming\com.app\logs` |
| `homeDir()` | User home | `C:\Users\X` |
| `desktopDir()` | User desktop | `C:\Users\X\Desktop` |
| `documentDir()` | User documents | `C:\Users\X\Documents` |
| `downloadDir()` | User downloads | `C:\Users\X\Downloads` |
| `tempDir()` | System temp | `C:\Users\X\AppData\Local\Temp` |
| `resourceDir()` | Bundled resources | App install directory |

### BaseDirectory Enum Key Members

| Member | Value | Description |
|--------|-------|-------------|
| `AppData` | 14 | App-specific data directory |
| `AppConfig` | 13 | App-specific config directory |
| `AppLocalData` | 15 | App-specific local data |
| `AppCache` | 16 | App-specific cache |
| `AppLog` | 17 | App-specific log directory |
| `Home` | 21 | User home directory |
| `Desktop` | 18 | Desktop directory |
| `Document` | 6 | Documents directory |
| `Download` | 7 | Downloads directory |
| `Resource` | 11 | App bundled resources |
| `Temp` | 12 | System temp directory |

### Critical Warnings

**NEVER** use a plugin without adding its permissions to the capability file -- all plugin API calls will fail with "command not allowed" at runtime.

**NEVER** use relative paths without a `BaseDirectory` in the fs plugin -- paths without a base directory fail security checks.

**NEVER** assume path functions are synchronous -- ALL path functions in Tauri return `Promise<string>`, unlike Node.js.

**NEVER** forget to install BOTH the Cargo crate AND the npm package -- plugins require both Rust and JS components.

**ALWAYS** use `isTauri()` to guard Tauri-specific API calls when the frontend may also run in a browser.

**ALWAYS** use `convertFileSrc()` to display local files in HTML -- direct file paths do not work in the webview.

**ALWAYS** register plugins in `tauri::Builder` with `.plugin()` -- installing the crate alone is not sufficient.

---

## Essential Patterns

### Pattern 1: File System Plugin

```typescript
import { readTextFile, writeTextFile, readDir, mkdir, exists } from '@tauri-apps/plugin-fs';
import { BaseDirectory } from '@tauri-apps/api/path';

// Read text file
const content = await readTextFile('config.toml', {
  baseDir: BaseDirectory.AppConfig,
});

// Write text file
await writeTextFile('config.json', JSON.stringify({ theme: 'dark' }), {
  baseDir: BaseDirectory.AppConfig,
});

// Check existence
if (await exists('token.json', { baseDir: BaseDirectory.AppLocalData })) {
  // file exists
}

// Create directory
await mkdir('cache/images', { baseDir: BaseDirectory.AppCache });

// Read directory
const entries = await readDir('data', { baseDir: BaseDirectory.AppData });
```

### Pattern 2: Dialog Plugin

```typescript
import { open, save, ask, confirm, message } from '@tauri-apps/plugin-dialog';

// File picker
const filePath = await open({
  multiple: false,
  directory: false,
  filters: [{ name: 'Images', extensions: ['png', 'jpg', 'gif'] }],
});

// Directory picker
const dirPath = await open({ directory: true });

// Save dialog
const savePath = await save({
  filters: [{ name: 'Documents', extensions: ['pdf', 'docx'] }],
});

// Message dialogs
await message('Operation completed!', { title: 'Success', kind: 'info' });
const yes = await ask('Delete this file?', { title: 'Confirm', kind: 'warning' });
const ok = await confirm('Proceed?', { title: 'Action' });
```

### Pattern 3: HTTP Plugin

```typescript
import { fetch } from '@tauri-apps/plugin-http';

const response = await fetch('https://api.example.com/data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' }),
});

console.log(response.status);
const data = await response.json();
```

HTTP permission requires URL scoping:

```json
{
  "identifier": "http:default",
  "allow": [{ "url": "https://api.example.com/*" }],
  "deny": [{ "url": "https://api.example.com/admin/*" }]
}
```

### Pattern 4: Notification Plugin

```typescript
import { isPermissionGranted, requestPermission, sendNotification } from '@tauri-apps/plugin-notification';

let granted = await isPermissionGranted();
if (!granted) {
  const permission = await requestPermission();
  granted = permission === 'granted';
}

if (granted) {
  sendNotification({
    title: 'Download Complete',
    body: 'Your file has been downloaded successfully.',
  });
}
```

### Pattern 5: Shell Plugin

```typescript
import { Command } from '@tauri-apps/plugin-shell';

const result = await Command.create('exec-sh', ['-c', 'echo "Hello"']).execute();
console.log(result.stdout);
console.log(result.status.code);
```

Shell permission requires command whitelisting:

```json
{
  "identifier": "shell:allow-execute",
  "allow": [{
    "name": "exec-sh",
    "cmd": "sh",
    "args": ["-c", { "validator": "\\S+" }],
    "sidecar": false
  }]
}
```

### Pattern 6: Clipboard Plugin

```typescript
import { writeText, readText } from '@tauri-apps/plugin-clipboard-manager';

await writeText('Hello, clipboard!');
const content = await readText();
```

### Pattern 7: OS Information Plugin

```typescript
import { platform, arch, type, version, hostname, locale, eol } from '@tauri-apps/plugin-os';

const os = await platform();   // "windows", "linux", "macos", "android", "ios"
const cpu = await arch();      // "x86_64", "aarch64", etc.
const ver = await version();   // e.g., "10.0.22621"
const host = await hostname();
const loc = await locale();    // e.g., "en-US"
const lineEnd = eol();         // "\r\n" on Windows, "\n" on Unix
```

### Pattern 8: Process Plugin

```typescript
import { exit, relaunch } from '@tauri-apps/plugin-process';

await exit(0);      // exit with code
await relaunch();   // restart app
```

### Pattern 9: Store Plugin

```typescript
import { load } from '@tauri-apps/plugin-store';

const store = await load('settings.json', { autoSave: true });

await store.set('theme', 'dark');
await store.set('user', { name: 'Alice', prefs: { lang: 'en' } });

const theme = await store.get<string>('theme');
const hasKey = await store.has('theme');
const allKeys = await store.keys();

await store.delete('theme');
await store.clear();
await store.save();    // manual save (if autoSave is false)
await store.reload();  // reload from disk
```

### Pattern 10: Path API

```typescript
import { appDataDir, join, resolve, dirname, basename, extname } from '@tauri-apps/api/path';

const dataPath = await appDataDir();
const full = await join(await appDataDir(), 'databases', 'app.db');
const dir = await dirname('/path/to/file.txt');   // "/path/to"
const base = await basename('/path/to/file.txt'); // "file.txt"
const ext = await extname('document.pdf');         // "pdf"
```

### Pattern 11: convertFileSrc

```typescript
import { convertFileSrc } from '@tauri-apps/api/core';
import { appDataDir, join } from '@tauri-apps/api/path';

const imgSrc = convertFileSrc(
  await join(await appDataDir(), 'photos', 'avatar.jpg')
);
document.getElementById('avatar').src = imgSrc;
// Returns: "https://asset.localhost/path/to/avatar.jpg"
```

### Pattern 12: isTauri Guard

```typescript
import { isTauri } from '@tauri-apps/api/core';
import { invoke } from '@tauri-apps/api/core';

if (isTauri()) {
  const data = await invoke('get_data');
} else {
  const data = await fetch('/api/data').then(r => r.json());
}
```

### Pattern 13: Updater Plugin

```typescript
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

const update = await check();
if (update) {
  console.log(`Update available: ${update.version}`);
  await update.downloadAndInstall((event) => {
    switch (event.event) {
      case 'Started':
        console.log(`Downloading ${event.data.contentLength} bytes`);
        break;
      case 'Progress':
        console.log(`Chunk: ${event.data.chunkLength} bytes`);
        break;
      case 'Finished':
        console.log('Download complete');
        break;
    }
  });
  await relaunch();
}
```

---

## Typical Capability File

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default capabilities for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:app:default",
    "fs:default",
    "dialog:default",
    "http:default",
    "notification:default",
    "shell:default",
    "clipboard-manager:allow-read-text",
    "clipboard-manager:allow-write-text",
    "os:default",
    "process:default",
    "updater:default",
    "store:default",
    "opener:default"
  ]
}
```

---

## Permission Suffix Convention

For each plugin, auto-generated permissions follow this pattern:
- `<plugin>:default` -- Safe default permissions
- `<plugin>:allow-<command>` -- Allow a specific command
- `<plugin>:deny-<command>` -- Deny a specific command

Deny rules ALWAYS take precedence over allow rules.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for all plugins and path functions
- [references/examples.md](references/examples.md) -- Working code examples for each plugin
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with plugins, with WHY explanations

### Official Sources

- https://v2.tauri.app/plugin/
- https://v2.tauri.app/reference/javascript/api/namespacepath/
- https://v2.tauri.app/reference/javascript/api/namespacecore/
