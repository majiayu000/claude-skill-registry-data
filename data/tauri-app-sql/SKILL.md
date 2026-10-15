---
name: tauri-app-sql
description: Guidance for Tauri v2 SQL plugin setup, migrations, and safe query access.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Using SQLite, MySQL, or PostgreSQL in Tauri / 在 Tauri 中使用 SQLite、MySQL 或 PostgreSQL
- SQL migrations or connection configuration / SQL 迁移或连接配置
- Secure frontend query access / 前端安全查询访问

**Trigger phrases include:**
- "sql", "sqlite", "postgres", "mysql", "migration"
- "数据库", "迁移", "连接配置", "SQL"

## How to use this skill

1. Select the database engine and connection string
2. Configure migrations in tauri.conf.json
3. Enable SQL plugin capabilities with scoped access
4. Validate queries and error handling in the app flow

## Outputs

- Database integration plan / 数据库集成方案
- Minimal-permission capability checklist / 最小权限能力清单

## Scope

- Boundary: SQL plugin configuration and usage only
- Key points: Migrations setup and capability scoping

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/sql/
- https://v2.tauri.app/zh-cn/plugin/sql/

## Keywords

tauri sql, sqlite, postgres, mysql, migrations, database

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
