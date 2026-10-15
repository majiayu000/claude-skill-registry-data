---
name: tauri-app-logging
description: Guidance for Tauri v2 logging plugin with levels, filtering, and safe diagnostics.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Unified logging for dev and release builds / 开发与发布统一日志
- Log filtering or persistence / 日志过滤或持久化
- Safe diagnostics without leaking secrets / 安全诊断不泄露敏感信息

**Trigger phrases include:**
- "logging", "log levels", "filtering", "persistence", "diagnostics"
- "日志", "级别", "过滤", "持久化", "诊断"

## How to use this skill

1. Define log levels and redaction rules
2. Configure logging plugin outputs and filters
3. Implement diagnostic toggles for release builds
4. Validate log storage location and rotation policy

## Outputs

- Logging strategy and configuration / 日志策略与配置
- Redaction and rotation checklist / 脱敏与滚动清单

## Scope

- Boundary: Logging plugin usage only
- Key points: Redaction and environment-specific verbosity

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/logging/
- https://v2.tauri.app/zh-cn/plugin/logging/

## Keywords

tauri logging, log levels, diagnostics, redaction

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
