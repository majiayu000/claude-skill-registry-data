---
name: db-openapi
description: 查询集成连接器和API配置（v3_openapi数据库）。使用 exec_sql 工具执行查询。
---

# v3_openapi 数据库查询

## 【通用规范】

参考：[通用规范](./COMMON.md)

## 执行方式

所有查询使用 `exec_sql` 工具执行，参数替换为实际值。

**重要**：在执行 SQL 前，必须先打印出完整的目标 SQL 语句，然后再使用 `exec_sql` 工具执行。

**重要**：执行 SQL 后，必须对查询结果进行结构化展示：
- 明确说明查询到的记录数量
- 提取并展示关键字段的值（如连接器ID、接口ID等）
- 多条记录时使用表格或列表形式展示，避免直接输出原始 JSON 数据

## 查询模板

### integrated_connector

**参数**：
- `{org_id}` - 租户ID

```sql
-- 按租户查询集成连接器
SELECT * FROM v3_openapi.integrated_connector WHERE org_id = {org_id} and deleted_at = 0;
```

### integrated_connector_api

**参数**：
- `{org_id}` - 租户ID
- `{interface_id}` - API接口ID
- `{connector_id}` - 连接器ID

```sql
-- 按租户查询API接口列表
SELECT * FROM v3_openapi.integrated_connector_api WHERE org_id = {org_id} and deleted_at = 0;

-- 按接口ID查询API详情
SELECT * FROM v3_openapi.integrated_connector_api WHERE org_id = {org_id} AND id = {interface_id} and deleted_at = 0;

-- 按连接器ID查询API接口
SELECT * FROM v3_openapi.integrated_connector_api WHERE integrated_connector_id = {connector_id} and deleted_at = 0;
```

### integrated_connector_api_field

**参数**：
- `{org_id}` - 租户ID
- `{interface_id}` - API接口ID
- `{connector_id}` - 连接器ID

```sql
-- 按接口ID查询字段配置
SELECT * FROM v3_openapi.integrated_connector_api_field WHERE org_id = {org_id} AND interface_id = {interface_id} and deleted_at = 0 order by req_or_res, id;

-- 按连接器ID查询所有API的字段
SELECT * FROM v3_openapi.integrated_connector_api_field 
WHERE org_id = {org_id} AND interface_id IN (
    SELECT id FROM v3_openapi.integrated_connector_api 
    WHERE org_id = {org_id} AND integrated_connector_id = {connector_id} and deleted_at = 0
) and deleted_at = 0
order by interface_id, req_or_res, id;
```

## 注意事项

1. 参数替换：所有模板中的`{参数名}`都需要替换为实际值
2. 删除标记：所有查询都包含`deleted_at = 0`条件
3. 执行方式：必须通过 MCP 工具 `exec_sql` 执行
4. 表结构查询：使用 `DESC table_name` 或 `SHOW COLUMNS FROM table_name` 查询
