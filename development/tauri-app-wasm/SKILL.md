---
name: tauri-app-wasm
description: Guidance for running Rust-compiled WASM in the Tauri v2 frontend.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- High-performance frontend computation / 高性能前端计算
- WASM vs IPC trade-offs / WASM 与 IPC 取舍
- Rust logic running in the WebView / Rust 逻辑运行于 WebView

**Trigger phrases include:**
- "WASM", "WebAssembly", "IPC", "performance"
- "WASM", "WebAssembly", "性能", "IPC"

## How to use this skill

1. Identify workloads suitable for WASM execution
2. Build Rust code to WASM and integrate with the frontend
3. Keep system API access in Rust core via IPC when needed
4. Validate performance gains and bundle size impact

## Outputs

- WASM integration plan / WASM 集成方案
- Performance and bundle checklist / 性能与包体清单

## Scope

- Boundary: Frontend WASM usage only
- Key points: WASM vs IPC responsibilities

## References

- https://v2.tauri.app/llms.txt
- https://crates.io/crates/tauri-wasm
- https://v2.tauri.app/develop/calling-rust/#wasm
- https://github.com/p1mo/tauri-wasm
- https://zhuanlan.zhihu.com/p/533025312
- https://blog.csdn.net/qq_63401240/article/details/147340217

## Keywords

tauri wasm, rust wasm, frontend compute, performance

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
