---
name: tauri-config
description: Guidance for Tauri v2 tauri.conf.json structure, lifecycle management, and CSP configuration.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Configuring tauri.conf.json / 配置 tauri.conf.json
- Config changes from Tauri v1 to v2 / v1 到 v2 的配置变更
- CSP or platform-specific config sections / CSP 或平台配置段

**Trigger phrases include:**
- "tauri.conf.json", "config", "CSP", "android", "ios"
- "配置", "CSP", "Android", "iOS"

## How to use this skill

1. Identify app requirements and platform targets
2. Map requirements to tauri.conf.json sections
3. Apply v2 config layout and plugin locations
4. Validate CSP and platform config for desktop and mobile

## Outputs

- Config structure mapping / 配置结构映射
- CSP and platform config checklist / CSP 与平台配置清单

## Scope

- Boundary: tauri.conf.json lifecycle management
- v2 focus: Config structure changes and platform sections

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/reference/config/
- https://v2.tauri.app/security/csp/

## Keywords

tauri v2, tauri.conf.json, config, csp, plugins, android, ios

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
