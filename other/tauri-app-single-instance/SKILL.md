---
name: tauri-app-single-instance
description: Guidance for Tauri v2 single-instance behavior and second-launch argument handling.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Preventing multiple app instances / 防止多开实例
- Handling second-launch arguments / 处理二次启动参数
- Deep-linking or CLI with single-instance / 深链或 CLI 与单实例联动

**Trigger phrases include:**
- "single instance", "second launch", "arguments", "deep linking"
- "单实例", "二次启动", "参数", "深链"

## How to use this skill

1. Enable single-instance and define init behavior
2. Capture and route second-launch arguments to the app
3. Focus or restore the main window on re-entry
4. Validate behavior with deep-linking or CLI scenarios

## Outputs

- Single-instance behavior plan / 单实例行为方案
- Second-launch routing checklist / 二次启动路由清单

## Scope

- Boundary: Single-instance configuration and runtime behavior
- Key points: Safe argument passing and window focus behavior

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/single-instance/
- https://v2.tauri.app/zh-cn/plugin/single-instance/

## Keywords

tauri single instance, second launch, args, focus window

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
