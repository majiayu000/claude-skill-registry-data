---
name: tauri-app-store
description: Guidance for Tauri v2 store plugin with key-value persistence and lazy loading.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Lightweight persistent storage / 轻量持久化存储
- Store vs LazyStore decision / Store 与 LazyStore 选择
- Saving app settings to disk / 应用配置落盘保存

**Trigger phrases include:**
- "store", "lazystore", "persistence", "key-value"
- "持久化", "本地存储", "配置保存", "键值"

## How to use this skill

1. Decide between Store and LazyStore based on load timing
2. Define the storage file location and schema
3. Restrict access via capabilities and scope
4. Validate persistence lifecycle and error handling

## Outputs

- Store selection guidance / Store 选择指导
- Persistence plan for app settings / 应用配置持久化方案

## Scope

- Boundary: Store plugin usage only
- Key points: Store vs LazyStore differences

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/store/
- https://v2.tauri.app/zh-cn/plugin/store/

## Keywords

tauri store, key-value, persistence, local storage

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
