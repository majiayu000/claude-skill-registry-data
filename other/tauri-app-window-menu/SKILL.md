---
name: tauri-app-window-menu
description: Guidance for Tauri v2 window menu definition, event handling, and shortcuts.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Native window menus with shortcuts / 原生窗口菜单与快捷键
- Menu events and command handlers / 菜单事件与命令处理
- Platform-specific menu layouts / 平台菜单布局差异

**Trigger phrases include:**
- "window menu", "shortcuts", "menu events", "command handlers"
- "窗口菜单", "快捷键", "菜单事件", "命令处理"

## How to use this skill

1. Define menu structure and keyboard shortcuts
2. Separate command identifiers from event handlers
3. Handle platform-specific menu conventions
4. Test menu event routing and focus behavior

## Outputs

- Menu layout and shortcut plan / 菜单布局与快捷键方案
- Event routing checklist / 事件路由清单

## Scope

- Boundary: Window menu definitions and event handling
- Key points: Command/handler separation and testability

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/learn/window-menu/
- https://v2.tauri.app/zh-cn/learn/window-menu/

## Keywords

tauri menu, window menu, shortcuts, commands

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
