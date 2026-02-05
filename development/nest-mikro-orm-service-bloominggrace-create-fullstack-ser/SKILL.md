---
name: nest-mikro-orm-service
description: Use when creating or modifying NestJS service files that interact with MikroORM.
---

# NestJS Service + MikroORM Guide

Use this skill when creating or modifying NestJS service files that interact with MikroORM.

In MikroORM v6+, `persistAndFlush` and `removeAndFlush` are deprecated.
Instead, use method chaining: `persist(entity).flush()` and `remove(entity).flush()`.
This skill defines the correct CRUD patterns using EntityManager.

## Basic Service Structure

```typescript
import {
  EntityManager,
  FilterQuery,
  NotFoundError,
  UniqueConstraintViolationException,
} from "@mikro-orm/core";
import {
  ConflictException,
  Injectable,
  NotFoundException,
} from "@nestjs/common";

import { CreateEntityDto } from "./dto/create-entity.dto";
import { UpdateEntityDto } from "./dto/update-entity.dto";
import { Entity } from "./entities/entity.entity";

@Injectable()
export class EntityService {
  constructor(private readonly entityManager: EntityManager) {}

  // CRUD methods...
}
```

## Custom Repository Pattern

Use Custom Repository when you need to encapsulate complex database queries or reusable logic.

### 1. Define Repository

```typescript
import { EntityRepository } from "@mikro-orm/core";
import { Entity } from "./entities/entity.entity";

export class CustomRepository extends EntityRepository<Entity> {
  async findWithCustomLogic() {
    return this.createQueryBuilder("u")
      .leftJoinAndSelect("u.posts", "p")
      .where({ "u.active": true })
      .getResultList();
  }
}
```

### 2. Register in Entity

```typescript
import { Entity } from "@mikro-orm/core";
import { CustomRepository } from "./custom.repository";

@Entity({ repository: () => CustomRepository })
export class EntityName {
  // ...
}
```

## CRUD Patterns

### Create

```typescript
async create(createDto: CreateEntityDto): Promise<Entity> {
  const entity = this.entityManager.create(Entity, {
    field: createDto.field,
  });

  try {
    await this.entityManager.persist(entity).flush();
  } catch (error) {
    if (error instanceof UniqueConstraintViolationException) {
      throw new ConflictException('중복된 데이터가 존재합니다.');
    }
    throw error;
  }

  return entity;
}
```

### Read

```typescript
async findOne(filterQuery: FilterQuery<Entity>): Promise<Entity> {
  try {
    return await this.entityManager.findOneOrFail(Entity, filterQuery);
  } catch (error) {
    if (error instanceof NotFoundError) {
      throw new NotFoundException('찾을 수 없는 데이터입니다.');
    }
    throw error;
  }
}
```

### Update

```typescript
async update(id: string, updateDto: UpdateEntityDto): Promise<Entity> {
  const entity = await this.findOne({ id });
  this.entityManager.assign(entity, omitBy(updateDto, isUndefined));

  try {
    await this.entityManager.flush();
  } catch (error) {
    if (error instanceof UniqueConstraintViolationException) {
      throw new ConflictException('중복된 데이터가 존재합니다.');
    }
    throw error;
  }

  return entity;
}
```

### Delete

```typescript
async delete(id: string): Promise<void> {
  const entity = await this.findOne({ id });
  await this.entityManager.remove(entity).flush();
}
```

## Core Rules

### 1. EntityManager & Repository Injection

- Inject `EntityManager` for basic CRUD operations
- Use **Custom Repository** for complex queries or reusable business logic
- `private readonly entityManager: EntityManager`

### 2. Method Usage

| Operation | Method                                            |
| --------- | ------------------------------------------------- |
| Create    | `em.create()` → `em.persist(e).flush()`           |
| Read      | `em.findOne()`, `em.findOneOrFail()`, `em.find()` |
| Update    | `em.assign()` → `em.flush()`                      |
| Delete    | `em.remove(e).flush()`                            |

### 3. Exception Handling

- `UniqueConstraintViolationException` → `ConflictException` (409)
- `NotFoundError` → `NotFoundException` (404)
- Exception messages should be written in Korean

### 4. FilterQuery Usage

- Use `FilterQuery<Entity>` type for query methods
- Supports flexible query conditions

### 5. Handling Undefined Fields

- Use `omitBy`, `isUndefined` from `es-toolkit`
- Exclude undefined fields from updates

## Transactions

### Programmatic Approach

```typescript
await this.entityManager.transactional(async (em) => {
  const entity = await em.findOne(Entity, { id });
  entity.field = "new value";
  // Auto flush
});
```

### Decorator Approach

```typescript
import { Transactional } from '@mikro-orm/core';

@Transactional()
async complexOperation(): Promise<void> {
  // Executed within transaction
}
```

## File Naming Conventions

- Service file: `{module}.service.ts`
- Repository file: `{module}.repository.ts` (if used)
- One service per entity
