---
name: tauri-app-sidecar-nodejs
description: Guidance for Tauri v2 sidecar Node.js integration with lifecycle and packaging.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Node.js runtime as a sidecar / Node.js 侧车运行时
- Sidecar packaging and lifecycle / 侧车打包与生命周期
- Frontend-triggered sidecar execution / 前端触发侧车执行

**Trigger phrases include:**
- "sidecar", "nodejs", "packaging", "lifecycle"
- "侧车", "Node.js", "打包", "生命周期"

## How to use this skill

1. Define the Node.js sidecar responsibilities and binary output
2. Configure sidecar packaging per platform
3. Manage start, stop, and logging lifecycle in Rust
4. Validate permissions and release build behavior

## Outputs

- Sidecar integration plan / 侧车集成方案
- Packaging and lifecycle checklist / 打包与生命周期清单

## Scope

- Boundary: Sidecar Node.js integration only
- Key points: Packaging and lifecycle management

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/learn/sidecar-nodejs/
- https://v2.tauri.app/zh-cn/learn/sidecar-nodejs/

## Keywords

tauri sidecar, nodejs, packaging, lifecycle

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
