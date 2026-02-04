---
name: new-db-schema
description: |
  Create new database tables with Drizzle ORM schemas and Valibot validation.
  使用 Drizzle ORM 创建新的数据库表模式和 Valibot 验证。

  Use when:
  - Adding new database tables
  - Creating entity schemas
  - User mentions "new table", "database schema", "add entity", "新增表", "数据库模式"
---

# New Database Schema Skill / 新增数据库模式技能

> **设计思路 / Design Notes**:
> 1. 数据库模式是基础设施，需要特别注意类型安全
> 2. 包含 Valibot 验证模式生成，与 API 层集成
> 3. 提供常用字段模式（UUID、时间戳、外键等）
> 4. 强调 snake_case 命名规范

## Overview / 概述

Create Drizzle ORM schemas with type-safe Valibot validation schemas.
创建带有类型安全 Valibot 验证模式的 Drizzle ORM 模式。

## Step-by-Step Instructions / 分步指令

### Step 1: Create Schema File / 创建模式文件

**File**: `packages/db/src/schemas/<entity>.ts`

```typescript
// [IN]: drizzle-orm/pg-core, drizzle-valibot, valibot, ./auth / 依赖 Drizzle、验证器及认证模式
// [OUT]: <entity> table, Create<Entity>Schema / 导出 <entity> 表及创建验证模式
// [POS]: Database layer - <Entity> schema / 数据库层 - <实体>模式
// Protocol: When updating me, sync this header + parent folder's .folder.md
// 协议：更新本文件时，同步更新此头注释及所属文件夹的 .folder.md

import { pgTable } from 'drizzle-orm/pg-core';
import { createInsertSchema } from 'drizzle-valibot';
import * as v from 'valibot';
import { user } from './auth';

// ============ Table Definition / 表定义 ============

export const <entity> = pgTable('<entity>', (t) => ({
  // Primary key - UUID
  id: t.uuid().primaryKey().defaultRandom(),

  // Required fields / 必需字段
  title: t.varchar({ length: 256 }).notNull(),
  content: t.text().notNull(),

  // Optional fields / 可选字段
  description: t.text(),

  // Timestamps / 时间戳
  createdAt: t
    .timestamp({ mode: 'string', withTimezone: true })
    .notNull()
    .defaultNow(),
  updatedAt: t
    .timestamp({ mode: 'string', withTimezone: true })
    .notNull()
    .defaultNow(),

  // Foreign key to user / 用户外键
  createdBy: t
    .text()
    .references(() => user.id)
    .notNull(),
}));

// ============ Validation Schemas / 验证模式 ============

// For creating new records (excludes auto-generated fields)
// 用于创建新记录（排除自动生成的字段）
export const Create<Entity>Schema = v.omit(
  createInsertSchema(<entity>, {
    // Custom validation rules / 自定义验证规则
    title: v.pipe(v.string(), v.minLength(3), v.maxLength(256)),
    content: v.pipe(v.string(), v.minLength(5), v.maxLength(5000)),
  }),
  ['id', 'createdAt', 'updatedAt', 'createdBy'],
);

// For updating records / 用于更新记录
export const Update<Entity>Schema = v.partial(Create<Entity>Schema);

// TypeScript types / TypeScript 类型
export type <Entity> = typeof <entity>.$inferSelect;
export type New<Entity> = typeof <entity>.$inferInsert;
```

### Step 2: Export from Schema Index / 从模式索引导出

**File**: `packages/db/src/schema.ts`

```typescript
// Add export / 添加导出
export * from './schemas/<entity>';
```

### Step 3: Update Folder Documentation / 更新文件夹文档

**File**: `packages/db/src/schemas/.folder.md`

Add the new file to the file list / 将新文件添加到文件列表：

```markdown
## Files
- `auth.ts`: Local - Authentication tables / 认证表
- `posts.ts`: Local - Post table / 文章表
- `<entity>.ts`: Local - <Entity> table / <实体>表  👈 New
```

### Step 4: Push to Database / 推送到数据库

```bash
pnpm db:push
```

## Common Field Patterns / 常用字段模式

### UUID Primary Key / UUID 主键
```typescript
id: t.uuid().primaryKey().defaultRandom(),
```

### Timestamps / 时间戳
```typescript
createdAt: t.timestamp({ mode: 'string', withTimezone: true }).notNull().defaultNow(),
updatedAt: t.timestamp({ mode: 'string', withTimezone: true }).notNull().defaultNow(),
```

### Foreign Key / 外键
```typescript
userId: t.text().references(() => user.id).notNull(),
// With cascade delete / 带级联删除
userId: t.text().references(() => user.id, { onDelete: 'cascade' }).notNull(),
```

### Enum / 枚举
```typescript
status: t.text({ enum: ['draft', 'published', 'archived'] }).notNull().default('draft'),
```

### JSON / JSON 字段
```typescript
metadata: t.jsonb().$type<{ key: string; value: unknown }[]>(),
```

## Validation Patterns / 验证模式

### String with length / 带长度的字符串
```typescript
v.pipe(v.string(), v.minLength(1), v.maxLength(100))
```

### Email / 邮箱
```typescript
v.pipe(v.string(), v.email())
```

### URL
```typescript
v.pipe(v.string(), v.url())
```

### Optional with default / 可选带默认值
```typescript
v.optional(v.string(), 'default value')
```

## Reference / 参考

- Existing example: `packages/db/src/schemas/posts.ts`
- Drizzle docs: https://orm.drizzle.team/docs/sql-schema-declaration
- Valibot docs: https://valibot.dev/guides/schemas/
