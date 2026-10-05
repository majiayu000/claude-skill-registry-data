---
name: tauri
description: Desktop application framework using web frontends with Rust backend — IPC commands, Tauri v2, plugins, window management, system tray, and cross-platform bundling.
trigger: tauri, tauri v2, tauri invoke, tauri commands, tauri plugins, tauri shell, tauri fs, tauri dialog, tauri bundling, rust backend
---

# Tauri

## IPC Commands
Rust functions exposed to the frontend via `#[tauri::command]`. Invoked from JavaScript with `invoke('command_name', { args })`. Supports async, return values, and error handling.

## Rust Backend
Core logic runs in Rust for performance and security. Frontend loads as a webview (no embedded Chromium). Binary size is under 10 MB.

## Tauri v2
Major update with plugin architecture, multi-webview support, mobile targets (iOS/Android), and enhanced permission system.

## Plugins
Official plugins extend capabilities:
- `shell` — run external commands
- `fs` — filesystem access
- `dialog` — native file pickers and messages
- `notification` — OS notifications
- `clipboard-manager` — clipboard read/write

## Window Management
Create, resize, position, and style windows from Rust or JS. Supports transparent backgrounds, decorations, and always-on-top.

## System Tray
Native tray icon with context menu. Update icon, tooltip, and menu items at runtime from Rust.

## Bundling
Build platform-specific installers: `.msi` / `.nsis` (Windows), `.dmg` (macOS), `.AppImage` / `.deb` (Linux). Code signing and auto-update supported.
