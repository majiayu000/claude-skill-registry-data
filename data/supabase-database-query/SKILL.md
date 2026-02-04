---
name: Supabase Database Query
description: Execute SQL queries, migrations, and RLS policies on Supabase database using MCP tools
tags: [database, supabase, sql, mcp]
---

# Supabase Database Query Skill

这个 Skill 帮助 Claude 使用 Supabase MCP 工具执行数据库操作。

## 何时使用

当需要执行以下操作时自动激活：

- 执行 SQL 查询（SELECT、INSERT、UPDATE、DELETE）
- 创建或修改数据库表结构
- 添加或修改 Row Level Security (RLS) 策略
- 执行数据库迁移
- 查看数据库表结构和数据

## 可用的 MCP 工具

### 主要工具：

1. **mcp__supabase__execute_sql** - 执行原始 SQL
   - 参数：`project_id`, `query`
   - 用于：查询数据、修改结构、RLS 策略

2. **mcp__supabase__apply_migration** - 应用迁移
   - 参数：`project_id`, `name`, `query`
   - 用于：DDL 操作、结构变更

3. **mcp__supabase__list_tables** - 查看表列表
   - 参数：`project_id`, `schemas` (可选)
   - 用于：了解数据库结构

### 项目信息：
- **project_id**: `giluhqotfjpmofowvogn`
- **数据库**: PostgreSQL via Supabase

## 使用示例

### 1. 添加 RLS 策略
```sql
-- 使用 execute_sql 工具
ALTER TABLE analysis_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "认证用户可以查看报告" ON analysis_reports
  FOR SELECT
  USING (auth.role() = 'authenticated');
```

### 2. 查询数据
```sql
SELECT * FROM grade_data WHERE student_id = '12345' LIMIT 10;
```

### 3. 创建表（使用 apply_migration）
```sql
CREATE TABLE new_table (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

## 最佳实践

1. **优先使用 MCP 工具**：避免使用 bash psql 命令，直接用 MCP 工具
2. **RLS 策略**：所有新表都应该启用 RLS 并添加适当的策略
3. **文档迁移**：创建迁移文件在 `supabase/migrations/` 目录作为文档
4. **错误处理**：执行失败时检查返回的错误信息
5. **事务安全**：涉及多个表的操作使用事务（BEGIN/COMMIT）

## 常见操作

### 启用表的 RLS
```sql
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY "policy_name" ON table_name
  FOR SELECT
  USING (auth.role() = 'authenticated');
```

### 查看表结构
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'your_table';
```

### 查看现有策略
```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename = 'your_table';
```

## 注意事项

- 生产数据库操作需谨慎
- 始终在迁移文件中记录结构变更
- RLS 策略必须考虑用户权限
- 敏感操作前先备份或在测试环境验证
