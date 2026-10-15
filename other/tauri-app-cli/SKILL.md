---
name: tauri-app-cli
description: Guidance for Tauri v2 CLI plugin with argument schema and app command routing.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- CLI arguments for a Tauri app / Tauri 应用的命令行参数
- Schema-based argument parsing / 基于 schema 的参数解析
- Triggering app behaviors from CLI / CLI 触发应用行为

**Trigger phrases include:**
- "cli", "arguments", "schema", "command routing"
- "命令行", "参数", "schema", "命令路由"

## How to use this skill

1. Define the CLI argument schema and command map
2. Configure CLI plugin capabilities and parsing
3. Route startup and second-launch arguments to the app
4. Validate CLI behaviors with single-instance mode

## Outputs

- CLI schema and routing plan / CLI schema 与路由方案
- Second-launch integration checklist / 二次启动集成清单

## Scope

- Boundary: CLI plugin usage only
- Key points: Schema definition and argument routing

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/cli/
- https://v2.tauri.app/zh-cn/plugin/cli/

## Keywords

tauri cli, arguments, schema, command routing

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
