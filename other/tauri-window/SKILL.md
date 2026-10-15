---
name: tauri-window
description: Guidance for Tauri v2 window creation, configuration, lifecycle management, and custom titlebar UI.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Creating or configuring Tauri windows / 创建或配置 Tauri 窗口
- Window lifecycle, behaviors, or multi-window patterns / 窗口生命周期、行为或多窗口模式
- Custom titlebar or frameless window UI / 自定义标题栏或无边框窗口

**Trigger phrases include:**
- "window", "titlebar", "frameless", "multi-window", "window lifecycle"
- "窗口", "标题栏", "无边框", "多窗口", "生命周期"

## How to use this skill

1. Identify the window requirements and platform targets
2. Map requirements to windows config and runtime APIs
3. Provide custom titlebar structure and event handling guidance
4. Validate lifecycle events and window state transitions

## Outputs

- Window configuration and lifecycle plan / 窗口配置与生命周期方案
- Custom titlebar guidance / 自定义标题栏指导

## Scope

- Boundary: Window creation, configuration, and lifecycle only
- v2 focus: Windows config and runtime window APIs

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/learn/window-customization/
- https://v2.tauri.app/zh-cn/learn/window-customization/
- https://v2.tauri.app/reference/config/#windows-config

## Keywords

tauri v2, window, titlebar, lifecycle, windows config, frameless

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
