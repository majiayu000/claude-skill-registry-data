---
name: deno-graphql-backend
description: Deno GraphQL 后端接口的完整开发指南. 当需要创建、修改后端 API 接口时使用此技能
compatibility: Requires Deno runtime
metadata:
  version: "1.0"
---

# Deno GraphQL 后端开发

## 三层架构

```
src/{mod}/{table}/
├── {table}.graphql.ts   # Schema 定义
├── {table}.model.ts     # Model 定义(可选)
├── {table}.resolver.ts  # 参数处理、事务/认证设置
└── {table}.service.ts   # 业务逻辑、调用 DAO
```

## 快速模板

### 1. GraphQL Schema

```typescript
import { defineGraphql } from "/lib/context.ts";
import * as resolver from "./{table}.resolver.ts";

defineGraphql(resolver, /* GraphQL */ `
  
  type {Table}Model {
    id: {Table}Id!
    lbl: String!
  }
  
  input {Table}Input {
    lbl: String!
  }
  
  input {Table}Search {
    lbl: String
  }
  
  type Query {
    "查询"
    get{Table}(id: {Table}Id!): {Table}Model
    "列表"
    findAll{Table}(search: {Table}Search): [{Table}Model!]!
  }
  
  type Mutation {
    "创建"
    create{Table}(input: {Table}Input!): {Table}Id!
    "更新"
    update{Table}(id: {Table}Id!, input: {Table}Input!): Boolean!
    "删除"
    delete{Table}(ids: [{Table}Id!]!): Int!
  }
`);
```

### 2. Resolver

```typescript
import {
  useContext,
} from "/lib/context.ts";

import type {
  {Table}Id,
  {Table}Input,
  {Table}Search,
} from "/gen/types.ts";

// 查询 - 不需要事务
export async function get{Table}(
  id: {Table}Id,
) {
  
  const {
    get{Table},
  } = await import("./{table}.service.ts");
  
  return await get{Table}(id);
}

// 修改 - 需要事务
export async function create{Table}(input: {Table}Input) {
  
  const {
    create{Table},
  } = await import("./{table}.service.ts");
  
  const context = useContext();
  context.is_tran = true;  // 开启事务
  
  return await create{Table}(input);
}
```

### 3. Service

```typescript
import {
  isEmpty,
} from "/lib/util/string_util.ts";

import {
  findById{Table},
  create{Table},
} from "/gen/{mod}/{table}/{table}.dao.ts";

import type {
  {Table}Id,
  {Table}Input
} from "/gen/types.ts";

export async function create{Table}(
  input: {Table}Input,
) {
  if (isEmpty(input.lbl)) {
    throw "名称不能为空";  // 业务错误用中文
  }
  return await create{Table}(input);
}
```

### 4. 注册模块

在 `src/{mod}/graphql.ts` 添加：
```typescript
import "./{table}/{table}.graphql.ts";
```

## 核心规则

| 规则 | 说明                                                      |
| ---- | --------------------------------------------------------- |
| 事务 | 增删改 `context.is_tran = true`，查询不设置               |
| 认证 | 默认需登录，公开接口设 `context.notVerifyToken = true`    |
| 错误 | `throw "中文提示"` 业务错误，`throw new Error()` 系统错误 |
| DAO  | 从 `gen/{mod}/{table}/{table}.dao.ts` 导入             |

## 详细参考

- [DAO 函数](references/dao.md) - 查询/创建/更新/删除函数
- [认证权限](references/auth.md) - 用户获取、权限检查、数据隔离
- [架构约定](references/architecture.md) - 目录结构、命名规范
