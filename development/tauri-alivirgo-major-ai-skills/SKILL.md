---
name: tauri
description: "Build secure cross-platform desktop applications with Tauri v2; configure Rust backend IPC commands, window management, and granular permission capabilities."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-09-13"
tags: ["tauri", "desktop", "rust", "cross-platform", "ipc", "webview", "frontend", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Tauri Lightweight Cross-Platform Desktop AI Skill Guide

## Overview & Engine Architecture

Tauri is an open-source framework for building tiny, ultra-fast, and secure cross-platform desktop applications. Unlike Electron, which bundles an entire Chromium browser and Node.js runtime with every app, Tauri utilizes the operating system's native webview component (WebView2 on Windows, WebKitGTK on Linux, and WebKit on macOS) coupled with a memory-safe **Rust backend**. This architecture yields production binaries under 10 MB and baseline RAM consumption under 50 MB.

Claude operates as a Principal Desktop Application Engineer, specializing in **Tauri v2 core architecture**, **Rust-to-Frontend IPC (Inter-Process Communication)**, **granular capability and permission configurations**, **system tray and window management**, and **secure multi-platform code signing and packaging**.

### Tauri v2 Runtime & IPC Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Tauri v2 Desktop Architecture               │
│                                                             │
│  Web Frontend Layer (React / Vue / Svelte / Vanilla JS)     │
│  ├── User Interface & DOM State                             │
│  └── Tauri JS SDK (@tauri-apps/api/core)                    │
│                                                             │
│  Secure IPC Bridge (JSON Message Passing)                   │
│  └── Capability & Permission Firewall (Explicit Whitelists) │
│                                                             │
│  Tauri Rust Core Runtime (src-tauri)                        │
│  ├── #[tauri::command] Handlers (Async, Typed Serialization)│
│  ├── Native OS System APIs (File I/O, Tray, Notifications)  │
│  └── Native OS Webview Wrapper (WebView2 / WebKit)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Explicit Permission Capabilities in v2**: Tauri v2 enforces strict capability files (`src-tauri/capabilities/*.json`). Every native plugin or command accessed by the frontend must be declared explicitly in capability rules; undeclared calls fail silently or return permission errors.
2. **Type-Safe Rust IPC Commands**: Annotate backend functions with `#[tauri::command]`. Return `Result<T, String>` or structured serializable errors (`#[derive(serde::Serialize)]`) so the frontend can catch errors via standard JavaScript `try/catch` promise rejection.
3. **Async Offloading for Heavy Tasks**: Never block the main Rust thread inside a command handler. Mark commands with `async` or use `tauri::async_runtime::spawn` for intensive CPU calculations or disk reads to keep the UI responsive at 60+ FPS.
4. **Strict Content Security Policy (CSP)**: Maintain a strict CSP in `tauri.conf.json` preventing arbitrary remote script execution or insecure inline code evaluation.

---

## Production Rust & TypeScript Automation: IPC Command & Frontend Binding

### 1. Rust Backend Command Implementation (`src-tauri/src/lib.rs`)

```rust
use serde::{Deserialize, Serialize};
use tauri::AppHandle;

#[derive(Debug, Serialize, Deserialize)]
pub struct SystemStats {
    pub total_memory_mb: u64,
    pub used_memory_mb: u64,
    pub cpu_cores: usize,
}

#[derive(Debug, Serialize)]
pub struct CommandError {
    pub message: String,
    pub code: u32,
}

#[tauri::command]
pub async fn fetch_system_metrics(
    _app: AppHandle,
    sample_rate_ms: u64,
) -> Result<SystemStats, CommandError> {
    if sample_rate_ms < 100 {
        return Err(CommandError {
            message: "Sample rate cannot be lower than 100ms".into(),
            code: 400,
        });
    }

    // Example reading system hardware statistics
    let stats = SystemStats {
        total_memory_mb: 16384,
        used_memory_mb: 8192,
        cpu_cores: num_cpus::get(),
    };

    Ok(stats)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![fetch_system_metrics])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 2. Frontend TypeScript Invocation (`src/metrics.ts`)

```typescript
import { invoke } from "@tauri-apps/api/core";

export interface SystemStats {
  total_memory_mb: number;
  used_memory_mb: number;
  cpu_cores: number;
}

export interface CommandError {
  message: string;
  code: number;
}

export async function loadSystemMetrics(): Promise<SystemStats | null> {
  try {
    const stats = await invoke<SystemStats>("fetch_system_metrics", {
      sampleRateMs: 500, // Note: camelCase in TS maps to snake_case in Rust
    });
    console.log(`Loaded metrics across ${stats.cpu_cores} CPU cores.`);
    return stats;
  } catch (error) {
    const err = error as CommandError;
    console.error(`Failed to load metrics [${err.code}]: ${err.message}`);
    return null;
  }
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`command not found: fetch_system_metrics`** | Function was not added to `tauri::generate_handler![...]` in `lib.rs`. | Register command name inside the builder's `invoke_handler` macro. |
| **`command not allowed by permission rules`** | In Tauri v2, the command or plugin is missing from `src-tauri/capabilities/default.json`. | Add command name or plugin permission (e.g., `core:default`, `shell:allow-open`) to permissions array. |
| **Linux build fails: `missing webkit2gtk-4.1`** | Host development system is missing required Linux WebKit development packages. | Install packages: `sudo apt-get install -y libwebkit2gtk-4.1-dev build-essential curl wget file libssl-dev libayatana-appindicator3-dev librsvg2-dev`. |
| **White screen on startup in production build** | Asset path in `tauri.conf.json` (`frontendDist`) points to wrong build output directory (e.g., `dist` vs `build`). | Verify build command generates HTML into exact path configured in `build.frontendDist`. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Start development desktop app with hot module reloading
npm run tauri dev

# 2. Inspect system environment, dependencies, and webview versions
npx tauri info

# 3. Build optimized, production signed installer package (.msi/.dmg/.deb/.AppImage)
npm run tauri build

# 4. Add a native Tauri plugin (e.g., file system or notifications)
npx tauri add fs
```

---

## Agent Operational Directive

> **MANDATORY**: When declaring commands in Rust, always remember that Tauri automatically converts JavaScript camelCase argument keys (`sampleRateMs`) to Rust snake_case parameters (`sample_rate_ms`).
