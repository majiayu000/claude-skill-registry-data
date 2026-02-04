---
name: create-module
description: 创建新的业务模块。当需要添加新模块如 ec、crm 时使用
---

# 创建模块

## 文件结构

```
src/tables/{mod}/
├── {mod}.sql    # 表结构
└── {mod}.ts     # 表配置
```

## 步骤

1. 创建 `src/tables/{mod}/{mod}.sql`
2. 创建 `src/tables/{mod}/{mod}.ts`
3. 在 `src/tables/tables.ts` 注册：

```typescript
import { defineConfig } from "../config";
import base from "./base/base";
import {mod} from "./{mod}/{mod}.ts";

export default defineConfig({
  ...base,
  ...{mod},
});
```

## 示例

模块名: `ec`（电商）

```typescript
// src/tables/ec/ec.ts
import { defineConfig } from "../../config";

export default defineConfig({
  ec_order: { /* 订单表配置 */ },
  ec_order_detail: { /* 订单明细配置 */ },
});
```
