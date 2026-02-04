---
name: db-common
description: 提供通用的数据库查询工作流程、SQL 模板和结果分析方法。使用 exec_sql 工具执行查询。
---

# 通用数据库查询工具

## 【通用规范】

参考：[通用规范](./COMMON.md)

## 【查询工作流程】

### 1. 确定查询目标
- 明确要查询的数据和目的
- 选择合适的数据库和表
- 确定查询范围（单条记录、列表、统计等）

### 2. 选择查询方法
- **SQL 查询**：适用于快速查询、批量查询、统计分析
  - 使用场景：只提供实例 id、批量查询、统计分析
- **MCP 工具**：适用于需要详细执行日志的场景
  - 使用场景：需要完整执行日志、链路追踪等

### 3. 执行查询
- 使用 `exec_sql` 工具执行
- **执行前**：必须打印完整的目标 SQL 语句（用【】包起来）
- **示例**：【SELECT * FROM v3_workflow.workflow_instance WHERE id = 123 AND deleted_at = 0;】

### 4. 结果分析
- **结构化展示**：明确说明查询到的记录数量
- **提取关键字段**：展示重要字段的值
- **格式化输出**：多条记录使用表格展示，避免直接输出原始 JSON

## 执行方式

所有查询使用 `exec_sql` 工具执行，参数替换为实际值。

**重要**：在执行 SQL 前，必须先打印出完整的目标 SQL 语句，然后再使用 `exec_sql` 工具执行。

**重要**：执行 SQL 后，必须对查询结果进行结构化展示：
- 明确说明查询到的记录数量
- 提取并展示关键字段的值
- 多条记录时使用表格或列表形式展示，避免直接输出原始 JSON 数据

## 通用查询方法

### 表结构查询

```sql
-- 查询表结构（推荐）
DESC database_name.table_name;

-- 查询完整表定义（包含索引、约束等）
SHOW CREATE TABLE database_name.table_name;

-- 查询表状态
SHOW TABLE STATUS LIKE 'table_name';
```

### 数据库信息查询

```sql
-- 查询所有数据库
SHOW DATABASES;

-- 查询当前数据库
SELECT DATABASE();

-- 查询指定数据库的所有表
SHOW TABLES FROM database_name;

-- 查询表的创建语句
SHOW CREATE TABLE table_name;
```

### 基础查询技巧

```sql
-- 查询前 N 条记录
SELECT * FROM table_name LIMIT N;

-- 查询去重
SELECT DISTINCT column_name FROM table_name;

-- 查询排序
SELECT * FROM table_name ORDER BY column_name DESC;

-- 查询统计
SELECT COUNT(*) FROM table_name WHERE condition;

-- 条件查询
SELECT * FROM table_name WHERE condition AND deleted_at = 0;
```

## 专用数据库查询

### 常用数据库（有专用 Skill）

- **v3_user**：查询组织/租户信息，使用 [db-user](../db-user/SKILL.md)
- **v3_openapi**：查询连接器/API配置，使用 [db-openapi](../db-openapi/SKILL.md)
- **v3_metadata**：查询事件/按钮/元数据配置，使用 [db-metadata](../db-metadata/SKILL.md)
- **v3_e-report**：查询数据分析告警配置，使用 [db-e-report](../db-e-report/SKILL.md)
- **v3_workflow**：查询工作流相关数据，使用本 skill 的通用方法

## 注意事项

1. 参数替换：所有模板中的`{参数名}`都需要替换为实际值
2. 删除标记：查询时需注意 `deleted_at = 0` 条件（如果表有软删除字段）
3. 执行方式：必须通过 MCP 工具 `exec_sql` 执行
4. 数据唯一性：不同 `org_id` 下可能存在相同的 `id`，这是不同的数据记录
