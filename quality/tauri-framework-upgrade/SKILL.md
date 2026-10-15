---
name: tauri-framework-upgrade
description: Guidance for upgrading to stable Tauri v2 from v1 or v2 beta with migration checks.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Upgrading from Tauri v1 to v2 / 从 v1 升级到 v2
- Migrating from v2 beta to v2 stable / v2 beta 迁移到稳定版
- Breaking changes in config or permissions / 配置或权限变更

**Trigger phrases include:**
- "migrate", "upgrade", "breaking changes", "v1 to v2"
- "升级", "迁移", "配置变更", "权限变更"

## How to use this skill

1. Identify current version and target / 确认当前版本与目标版本
2. Review breaking changes across config, plugins, permissions / 盘点变更点
3. Update tauri.conf.json and plugin layouts / 更新配置与插件位置
4. Migrate capabilities/default.json and scopes / 迁移能力与 Scope
5. Validate IPC, CSP, and runtime behavior / 验证 IPC、CSP 与运行行为

## Outputs

- Migration checklist / 迁移清单
- Updated config mapping / 更新后的配置映射
- Post-upgrade validation plan / 升级后验证计划

## Scope

- Boundary: Version migration and validation only / 仅限迁移与验证
- Key points: Config structure and capability system changes / 配置与权限体系
- Out of scope: feature redesign / 不包含功能重构

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/start/migrate/
- https://v2.tauri.app/start/migrate/from-tauri-1/
- https://v2.tauri.app/start/migrate/from-tauri-2-beta/

## Keywords

tauri upgrade, migrate, v2, breaking changes, config migration, 升级, 迁移, 配置变更

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
