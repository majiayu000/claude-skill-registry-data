---
name: tauri-app-plugin-permissions
description: Guidance for Tauri v2 plugin permission authoring, capability generation, and platform differences.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Writing or auditing plugin permissions / 编写或审计插件权限
- Plugin capability templates / 插件权限模板
- Cross-platform permission differences / 跨平台权限差异

**Trigger phrases include:**
- "plugin permissions", "capability template", "permissions schema"
- "插件权限", "权限模板", "平台差异"

## How to use this skill

1. Enumerate feature → plugin permission needs / 功能与插件权限需求映射
2. Separate plugin-defined permissions from app-enabled capabilities / 区分插件权限与应用能力
3. Generate capabilities/default.json with minimal scope / 生成最小权限配置
4. Validate Windows/platform differences and adjust / 校验平台差异并调整

## Outputs

- Permission template per plugin / 插件权限模板
- Capability file with minimal scope / 最小权限能力文件
- Cross-platform audit checklist / 跨平台审计清单

## Scope

- Boundary: Plugin permissions and capability configuration only / 仅限权限配置
- Key points: Windows and platform capability differences / 平台差异
- Out of scope: plugin implementation details / 不涉及插件实现

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/learn/using-plugin-permissions/
- https://v2.tauri.app/zh-cn/learn/security/using-plugin-permissions/
- https://v2.tauri.app/learn/security/capabilities-for-windows-and-platforms/
- https://v2.tauri.app/zh-cn/learn/security/capabilities-for-windows-and-platforms/
- https://v2.tauri.app/learn/security/writing-plugin-permissions/
- https://v2.tauri.app/zh-cn/learn/security/writing-plugin-permissions/

## Keywords

tauri permissions, plugin permissions, capabilities, scope, security, 插件权限, 权限模板, 平台差异

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
