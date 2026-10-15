---
name: tauri-ipc
description: Guidance for Tauri v2 IPC with frontend invoke calls, Rust commands, and type-safe bindings.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Frontend-to-Rust IPC or invoke calls / 前端到 Rust 的 IPC 或 invoke 调用
- Tauri commands or type-safe bindings / Tauri 命令或类型安全绑定
- Bidirectional messaging or event-based IPC / 双向消息或事件驱动 IPC

**Trigger phrases include:**
- "IPC", "invoke", "command", "tauri-specta", "type safety"
- "IPC", "调用命令", "类型安全", "tauri-specta"

## How to use this skill

1. Define Rust commands and register them in the Tauri builder
2. Use invoke on the frontend with typed payloads
3. Apply type generation tools to avoid any-typed IPC
4. Establish error handling and response contracts

## Outputs

- Typed IPC request/response contract / 类型化 IPC 请求响应契约
- Error handling and validation guidance / 错误处理与校验指导

## Scope

- Boundary: invoke calls and command definitions only
- v2 focus: type-safe IPC with tauri-specta or official generators

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/concept/inter-process-communication/
- https://v2.tauri.app/develop/calling-rust/
- https://v2.tauri.app/develop/calling-frontend/

## Keywords

tauri ipc, invoke, tauri command, type safety, tauri-specta

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
