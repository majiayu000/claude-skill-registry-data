---
name: tauri-concept
description: Guidance for Tauri v2 architecture concepts, process model, and IPC isolation patterns.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- How Tauri works internally / Tauri 内部工作机制
- Isolation or brownfield patterns / 隔离模式或棕地集成
- Architecture context before implementation / 实现前的架构认知

**Trigger phrases include:**
- "architecture", "process model", "isolation", "brownfield"
- "架构", "进程模型", "隔离", "棕地"

## How to use this skill

1. Explain the core process and WebView process separation
2. Describe process model and IPC isolation options
3. Map concept choices to practical architecture decisions
4. Provide conceptual risks and tradeoffs

## Outputs

- Conceptual model summary / 概念模型总结
- Architecture decision guidance / 架构决策指导

## Scope

- Boundary: Architecture concepts only
- v2 focus: Process model and IPC isolation patterns

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/concept/
- https://v2.tauri.app/concept/architecture/
- https://v2.tauri.app/concept/process-model/
- https://v2.tauri.app/concept/size/
- https://v2.tauri.app/concept/inter-process-communication/
- https://v2.tauri.app/concept/inter-process-communication/brownfield/
- https://v2.tauri.app/concept/inter-process-communication/isolation/
- https://v2.tauri.app/zh-cn/concept/
- https://v2.tauri.app/zh-cn/concept/architecture/
- https://v2.tauri.app/zh-cn/concept/process-model/
- https://v2.tauri.app/zh-cn/concept/size/
- https://v2.tauri.app/zh-cn/concept/inter-process-communication/
- https://v2.tauri.app/zh-cn/concept/inter-process-communication/brownfield/
- https://v2.tauri.app/zh-cn/concept/inter-process-communication/isolation/

## Keywords

tauri v2, architecture, process model, ipc isolation, brownfield

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
