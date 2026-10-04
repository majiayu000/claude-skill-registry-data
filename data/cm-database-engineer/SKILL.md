---
name: cm-database-engineer
description: 数据库工程师 Skill，执行数据模型设计、migration、查询优化，自动适配 ORM 和数据库类型
---

# cm-database-engineer — 数据库工程师

执行数据库相关开发任务。自动识别 ORM/查询工具和数据库类型。

## 触发条件

由 `/cm-ai` 自动调用，当 task 涉及数据库开发时触发。

## 工作流程

### 1. 识别技术栈

自动检测，不做硬编码假设：

- **ORM/查询工具**：Prisma / TypeORM / Drizzle / Knex / Sequelize / SQLAlchemy / GORM / diesel / raw SQL
- **数据库类型**：PostgreSQL / MySQL / SQLite / MongoDB / Redis / DynamoDB
- **Migration 工具**：ORM 内置 / Flyway / Alembic / golang-migrate / 自定义
- 扫描现有 migration 文件了解数据库演进历史和命名规范

### 2. 读取上下文

- `.claude/rules/database.md`、`.claude/rules/security.md`（如存在）
- design.md 中的数据模型和接口契约
- 现有 schema/model 文件

### 3. 开发

**Migration：**

- 遵循项目已有的 migration 命名规范（时间戳/序号）
- 确保可回滚（up + down），破坏性变更需暂停确认
- 新表包含审计字段（created_at、updated_at）
- 索引、外键、约束在 migration 中一并创建

**数据模型/Schema：**

- 跟随项目 ORM 的模型定义规范
- 字段类型精确（enum 不用 string 代替，decimal 不用 float）
- 关联关系清晰定义

**查询层：**

- 复杂查询封装为独立函数/repository
- 避免 N+1（eager loading / join / dataloader）
- 大数据量加分页和游标

**Seed 数据：**

- 如需开发用测试数据，创建 seed 脚本

### 4. 安全检查

- 连接字符串从环境变量读取
- 参数化查询，防止注入
- 敏感字段（密码、token）加密/哈希存储
- migration 不包含生产数据

### 5. 验证

```bash
# 根据项目实际工具执行
npx prisma migrate dev --name xxx    # Prisma
npx knex migrate:latest              # Knex
alembic upgrade head                 # Alembic
```

- migration 正常执行
- 回滚测试
- 模型类型与 API 契约一致

## 常见坑

| 问题 | 处理 |
| ---- | ---- |
| Migration 顺序冲突（多人开发） | 检查最新 migration 时间戳，避免冲突 |
| 大表加列/加索引锁表 | PostgreSQL 用 `CONCURRENTLY`，MySQL 考虑 `pt-online-schema-change` |
| ORM 生成的 SQL 性能差 | 用 `EXPLAIN ANALYZE` 检查，必要时写 raw query |
| 外键级联删除意外删数据 | 默认用 `RESTRICT`，只在明确需要时用 `CASCADE` |

## 输出

- 创建的 migration 文件和 schema 变更
- 验证结果
- 需要其他工种配合的事项
