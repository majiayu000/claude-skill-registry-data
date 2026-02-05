---
name: tauri-v2-dev
description: Tauri v2 跨平台应用开发指南。用于开发桌面 (macOS/Windows/Linux) 和移动端 (iOS/Android) 应用。包含项目初始化、Rust 后端、React 前端集成、移动端配置等最佳实践。当需要创建 Tauri 项目、配置移动端支持、编写 Rust 命令、或解决 Tauri 相关问题时使用此 skill。
---

# Tauri v2 开发指南

Tauri v2.2 是 2025年1月最新稳定版，支持桌面 + 移动端跨平台开发。

## 快速开始

### 创建项目

```bash
# 使用 create-tauri-app 创建项目
npm create tauri-app@latest

# 选择:
# - Project name: your-app-name
# - Package manager: npm/pnpm/yarn
# - UI template: React + TypeScript
```

### 项目结构

```
your-app/
├── src/                    # React 前端代码
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/              # Rust 后端代码
│   ├── src/
│   │   ├── main.rs         # 入口点
│   │   └── lib.rs          # 命令定义
│   ├── Cargo.toml          # Rust 依赖
│   ├── tauri.conf.json     # Tauri 配置
│   └── capabilities/       # 权限配置
├── package.json
└── vite.config.ts
```

## 移动端配置

### 前置条件

**macOS (iOS 开发):**
```bash
# 安装 Xcode (从 App Store)
# 安装 iOS targets
rustup target add aarch64-apple-ios x86_64-apple-ios aarch64-apple-ios-sim

# 安装 Cocoapods
brew install cocoapods
```

**Android 开发:**
```bash
# 安装 Android Studio
# 设置环境变量
export JAVA_HOME=/Applications/Android\ Studio.app/Contents/jbr/Contents/Home
export ANDROID_HOME=$HOME/Library/Android/sdk
export NDK_HOME=$ANDROID_HOME/ndk/26.1.10909125

# 安装 Android targets
rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android
```

### 初始化移动端

```bash
# 初始化 iOS
npm run tauri ios init

# 初始化 Android
npm run tauri android init
```

### 运行移动端

```bash
# iOS 模拟器
npm run tauri ios dev

# Android 模拟器
npm run tauri android dev

# 真机调试
npm run tauri ios dev --open  # 在 Xcode 中打开
```

## Rust 命令开发

### 定义命令 (src-tauri/src/lib.rs)

```rust
use tauri::Manager;

// 简单命令
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// 异步命令
#[tauri::command]
async fn fetch_data(url: String) -> Result<String, String> {
    reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())
}

// 带状态的命令
#[tauri::command]
fn get_count(state: tauri::State<'_, AppState>) -> i32 {
    *state.count.lock().unwrap()
}

// 注册命令
pub fn run() {
    tauri::Builder::default()
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![
            greet,
            fetch_data,
            get_count
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 前端调用 (TypeScript)

```typescript
import { invoke } from '@tauri-apps/api/core';

// 调用 Rust 命令
const result = await invoke<string>('greet', { name: 'World' });

// 异步调用
const data = await invoke<string>('fetch_data', { url: 'https://api.example.com' });
```

## 事件系统

### Rust 端发送事件

```rust
use tauri::Emitter;

#[tauri::command]
fn start_process(app: tauri::AppHandle) {
    std::thread::spawn(move || {
        for i in 0..100 {
            app.emit("progress", i).unwrap();
            std::thread::sleep(std::time::Duration::from_millis(100));
        }
    });
}
```

### 前端监听事件

```typescript
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<number>('progress', (event) => {
    console.log('Progress:', event.payload);
});

// 清理
unlisten();
```

## 常用插件

```bash
# 文件系统
npm run tauri add fs

# 对话框
npm run tauri add dialog

# 剪贴板
npm run tauri add clipboard-manager

# 通知
npm run tauri add notification

# HTTP 客户端
npm run tauri add http

# 全局快捷键
npm run tauri add global-shortcut

# 系统托盘
npm run tauri add tray-icon
```

### 插件使用示例

```typescript
// 文件系统
import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs';

const content = await readTextFile('path/to/file.txt');
await writeTextFile('path/to/file.txt', 'Hello World');

// 对话框
import { open, save } from '@tauri-apps/plugin-dialog';

const file = await open({
    multiple: false,
    filters: [{ name: 'Text', extensions: ['txt'] }]
});

// 剪贴板
import { writeText, readText } from '@tauri-apps/plugin-clipboard-manager';

await writeText('Hello');
const text = await readText();
```

## 配置文件 (tauri.conf.json)

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "Echo",
  "version": "0.1.0",
  "identifier": "com.echo.app",
  "build": {
    "beforeDevCommand": "npm run dev",
    "devUrl": "http://localhost:5173",
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../dist"
  },
  "app": {
    "windows": [
      {
        "title": "Echo",
        "width": 1200,
        "height": 800,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "security": {
      "csp": null
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

## 常见问题

### 1. iOS 签名问题
在 Xcode 中配置 Signing & Capabilities，使用个人开发者账号。

### 2. Android NDK 版本
确保 NDK 版本与 Cargo.toml 中的配置匹配。

### 3. 热重载不工作
检查 `devUrl` 配置是否正确指向前端开发服务器。

### 4. 权限问题
在 `src-tauri/capabilities/` 中配置所需权限。

## 参考资源

- [Tauri 官方文档](https://tauri.app)
- [Tauri v2 迁移指南](https://v2.tauri.app/start/migrate/from-tauri-1/)
- [Tauri 插件列表](https://tauri.app/plugin/)
