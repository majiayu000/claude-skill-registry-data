---
name: deno-graphql-backend
description: 创建 Deno GraphQL 后端接口的完整开发指南。包含三层架构（GraphQL/Resolver/Service）、DAO 函数使用、事务处理、认证权限、错误处理。当需要创建、修改后端 API 接口时使用此技能。
compatibility: Requires Deno runtime
metadata:
  version: "1.0"
---

# Deno GraphQL 后端开发

## 三层架构

```
src/{module}/{feature}/
├── {feature}.graphql.ts   # Schema 定义
├── {feature}.resolver.ts  # 参数处理、事务/认证设置
└── {feature}.service.ts   # 业务逻辑、调用 DAO
```

## 快速模板

### 1. GraphQL Schema

```typescript
import { defineGraphql } from "/lib/context.ts";
import * as resolver from "./{feature}.resolver.ts";

defineGraphql(resolver, /* GraphQL */ `
  type {Feature}Model { id: {Feature}Id!, lbl: String! }
  input {Feature}Input { lbl: String! }
  input {Feature}Search { lbl: String }
  
  type Query {
    "查询" get{Feature}(id: {Feature}Id!): {Feature}Model
    "列表" findAll{Feature}(search: {Feature}Search): [{Feature}Model!]!
  }
  
  type Mutation {
    "创建" create{Feature}(input: {Feature}Input!): {Feature}Id!
    "更新" update{Feature}(id: {Feature}Id!, input: {Feature}Input!): Boolean!
    "删除" delete{Feature}(ids: [{Feature}Id!]!): Int!
  }
`);
```

### 2. Resolver

```typescript
import { useContext } from "/lib/context.ts";
import type { {Feature}Id, {Feature}Input, {Feature}Search } from "/gen/types.ts";

// 查询 - 不需要事务
export async function get{Feature}(id: {Feature}Id) {
  const { get{Feature} } = await import("./{feature}.service.ts");
  return await get{Feature}(id);
}

// 修改 - 需要事务
export async function create{Feature}(input: {Feature}Input) {
  const { create{Feature} } = await import("./{feature}.service.ts");
  const context = useContext();
  context.is_tran = true;  // 增删改必须设置
  return await create{Feature}(input);
}
```

### 3. Service

```typescript
import { isEmpty } from "/lib/util/string_util.ts";
import { findById{Feature}, create{Feature} as createDao } from "/gen/{module}/{feature}/{feature}.dao.ts";
import type { {Feature}Id, {Feature}Input } from "/gen/types.ts";

export async function create{Feature}(input: {Feature}Input) {
  if (isEmpty(input.lbl)) throw "名称不能为空";  // 业务错误用中文
  return await createDao(input);
}
```

### 4. 注册模块

在 `src/{module}/graphql.ts` 添加：
```typescript
import "./{feature}/{feature}.graphql.ts";
```

## 核心规则

| 规则 | 说明 |
|------|------|
| 事务 | 增删改 `context.is_tran = true`，查询不设置 |
| 认证 | 默认需登录，公开接口设 `context.notVerifyToken = true` |
| 错误 | `throw "中文提示"` 业务错误，`throw new Error()` 系统错误 |
| DAO | 从 `gen/{module}/{table}/{table}.dao.ts` 导入 |

## 详细参考

- [DAO 函数](references/dao.md) - 查询/创建/更新/删除函数
- [认证权限](references/auth.md) - 用户获取、权限检查、数据隔离
- [架构约定](references/architecture.md) - 目录结构、命名规范
