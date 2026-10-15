---
name: tauri-app-dialog
description: Guidance for Tauri v2 dialog plugin with native dialogs and unified API design.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Native alert, confirm, or file dialogs / 原生提示、确认或文件对话框
- Unified dialog APIs across platforms / 跨平台统一对话框 API
- Async dialog flows with cancellation / 异步对话框与取消流程

**Trigger phrases include:**
- "dialog", "alert", "confirm", "file picker", "native dialog"
- "对话框", "提示框", "确认框", "文件选择"

## How to use this skill

1. Define dialog types and UI flows
2. Configure dialog plugin capabilities and scope
3. Implement async dialog calls and cancellation handling
4. Provide a unified dialog service layer for reuse

## Outputs

- Dialog service design / 对话框服务设计
- Async and cancellation flow checklist / 异步与取消流程清单

## Scope

- Boundary: Dialog plugin usage only
- Key points: Async behavior and platform consistency

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/dialog/
- https://v2.tauri.app/zh-cn/plugin/dialog/

## Keywords

tauri dialog, alert, confirm, file picker, native dialogs

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
