---
name: tauri-app-persisted-scope
description: Guidance for Tauri v2 persisted-scope plugin with expiration and revocation flows.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Persisting plugin scopes across sessions / 跨会话持久化插件 Scope
- Scope expiration or revocation / Scope 过期或撤销
- Re-authorization workflow / 重新授权流程

**Trigger phrases include:**
- "persisted scope", "expiration", "revocation", "re-authorization"
- "持久化权限", "过期", "撤销", "重新授权"

## How to use this skill

1. Define which scopes can be persisted and for how long
2. Configure persisted-scope plugin capabilities
3. Implement expiration, revocation, and re-approval flows
4. Validate scope restoration and downgrade handling

## Outputs

- Scope persistence policy / Scope 持久化策略
- Expiration and revocation checklist / 过期与撤销清单

## Scope

- Boundary: Persisted-scope plugin usage only
- Key points: Avoid permanent over-privilege

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/persisted-scope/
- https://v2.tauri.app/zh-cn/plugin/persisted-scope/

## Keywords

tauri persisted scope, permissions, expiration, security

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
