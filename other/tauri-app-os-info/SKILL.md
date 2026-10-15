---
name: tauri-app-os-info
description: Guidance for Tauri v2 os-info plugin with safe system diagnostics and reporting.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- System version or architecture info / 系统版本或架构信息
- Safe diagnostics data collection / 安全诊断数据采集
- Platform compatibility checks / 平台兼容性检查

**Trigger phrases include:**
- "os info", "system info", "diagnostics", "compatibility"
- "系统信息", "诊断", "兼容性"

## How to use this skill

1. Define the minimum OS info required for diagnostics
2. Configure os-info plugin capabilities and scope
3. Implement data redaction and reporting policy
4. Validate behavior across platforms and locales

## Outputs

- Diagnostics data plan / 诊断数据方案
- Redaction and reporting checklist / 脱敏与上报清单

## Scope

- Boundary: OS info plugin usage only
- Key points: Data minimization and redaction

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/os-info/
- https://v2.tauri.app/zh-cn/plugin/os-info/

## Keywords

tauri os info, diagnostics, system info, privacy

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
