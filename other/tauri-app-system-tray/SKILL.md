---
name: tauri-app-system-tray
description: Guidance for Tauri v2 system tray interactions and platform behavior differences.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- System tray or status bar behavior / 系统托盘或状态栏行为
- Tray menu and window visibility / 托盘菜单与窗口可见性
- Platform-specific tray conventions / 跨平台托盘约定

**Trigger phrases include:**
- "system tray", "status bar", "tray menu", "visibility"
- "系统托盘", "状态栏", "托盘菜单", "可见性"

## How to use this skill

1. Define tray icon behavior and menu actions
2. Map actions to window show, hide, and focus
3. Handle macOS, Windows, and Linux behavior differences
4. Ensure security gating for sensitive actions

## Outputs

- Tray interaction and visibility plan / 托盘交互与可见性方案
- Platform differences checklist / 跨平台差异清单

## Scope

- Boundary: System tray interaction patterns only
- Key points: Platform differences and secure actions

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/learn/system-tray/
- https://v2.tauri.app/zh-cn/learn/system-tray/

## Keywords

tauri system tray, status bar, menu, cross-platform

## 常见陷阱 (Gotchas)

1. **版本兼容性**：注意框架版本与依赖库的兼容性，不同版本 API 可能有差异
2. **配置文件格式**：配置文件格式错误是最常见的问题，建议使用编辑器的语法检查
3. **环境变量**：确保所有必要的环境变量已正确设置，敏感信息不要硬编码
4. **依赖冲突**：多版本共存时注意依赖冲突，使用 lock 文件锁定版本
5. **性能陷阱**：大数据量场景下注意性能优化，避免 N+1 查询等常见问题

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
