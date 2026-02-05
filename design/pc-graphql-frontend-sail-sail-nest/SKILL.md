---
name: pc-graphql-frontend
description: 前端自定义 GraphQL API 接口开发。当需要在 Vue 3 前端调用后端自定义接口（非标准 CRUD）时使用此技能。
compatibility: Vue 3 + TypeScript
metadata:
  version: "1.0"
---

# 前端自定义 API 接口开发

## 文件结构

```
src/views/{module}/{table}/
├── Api.ts      # 自动生成(尽量不修改)
└── Api2.ts     # 手写自定义接口
```

## Query 模板

```typescript
import type {
  Query,
} from "#/types.ts";

/** 接口描述 */
export async function 函数名(
  id: XxxId,
  opt?: GqlOpt,
) {
  
  const res: {
    函数名: Query["函数名"];
  } = await query({
    query: /* GraphQL */ `
      query($id: XxxId!) {
        函数名(id: $id) {
          field1
          field2
        }
      }
    `,
    variables: { id },
  }, opt);
  
  const data = res.函数名;
  
  return data;
}
```

## Mutation 模板

```typescript
import type {
  Mutation,
  XxxInput,
} from "#/types.ts";

/** 接口描述 */
export async function updateXxx(
  id: XxxId,
  input: XxxInput,
  opt?: GqlOpt,
) {
  
  const res: {
    updateXxx: Mutation["updateXxx"];
  } = await mutation({
    query: /* GraphQL */ `
      mutation($id: XxxId!, $input: XxxInput!) {
        updateXxx(id: $id, input: $input)
      }
    `,
    variables: {
      id,
      input,
    },
  }, opt);
  
  const data = res.updateXxx;
  
  return data;
}
```

## 核心规则

| 规则 | 说明 |
|------|------|
| 类型导入 | 从 `#/types.ts` 导入 `Query`、`Mutation`、`XxxInput` 等,如果是标准的{table}Model,{table}Input,{table}Search就不需要引入,因为已经在Model.ts全局定义了 |
| 返回类型 | 使用 `Query["xxx"]` 或 `Mutation["xxx"]` 声明 |
| 命名 | 函数驼峰式，参数蛇形式，与后端保持一致 |

## 开发流程

1. 后端接口开发完成并重启服务
2. 类型自动生成到 `#/types.ts`
3. 在 `Api2.ts` 创建接口函数
4. 使用 `Query` 或 `Mutation` 声明返回类型
