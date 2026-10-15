---
name: tauri-security
description: Guidance for Tauri v2 capabilities, scope configuration, and ACL-based permission control.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Capability/Scope design or ACL permission control / 能力、Scope、ACL 权限控制
- Building capabilities/default.json / 生成或校验 capabilities/default.json
- Tightening plugin access in production / 生产环境权限收敛

**Trigger phrases include:**
- "capabilities", "scope", "acl", "permissions file"
- "权限配置", "能力文件", "Scope 配置", "ACL"

## How to use this skill

1. Translate features into plugin capabilities / 业务功能映射为插件能力
2. Define scoped access rules per capability / 为能力定义 Scope 规则
3. Generate and validate capabilities/default.json / 生成并校验能力文件
4. Verify runtime behavior matches minimum-privilege policy / 验证最小权限运行效果

## Outputs

- Capability-to-scope mapping / 能力到 Scope 的映射
- Validated capabilities/default.json / 可直接使用的能力文件
- Permission audit checklist / 权限审计清单

## Scope

- Boundary: Capabilities, scope, and ACL configuration only / 仅限权限配置
- v2 focus: Capabilities & scope are mandatory controls / v2 强制配置
- Out of scope: app feature design or backend auth / 不含功能设计与后端鉴权

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/security/capabilities/
- https://v2.tauri.app/security/scope/
- https://v2.tauri.app/security/acl/

## Keywords

tauri security, capabilities, scope, acl, permissions, 权限配置, 能力文件, 最小权限

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
