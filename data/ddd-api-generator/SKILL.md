---
name: ddd-api-generator
description: Generate REST API endpoints with class-validator DTOs, routing-controllers decorators, and complete Swagger docs. Use when creating API endpoints for existing use cases, adding routes, or building custom API actions (e.g., "Create user API", "Generate product endpoints").
allowed-tools: Read, Write, Edit, Glob, Grep
---

# DDD API Generator

Generate presentation layer components using routing-controllers with NestJS-style decorators, class-validator for validation, and automatic Swagger documentation.

## What This Skill Does

Creates production-ready REST API endpoints:

- **Request DTOs**: Validation classes with class-validator decorators (`@IsString`, `@IsEmail`, etc.)
- **Response Serializers**: Separate classes with `@JSONSchema` decorators for Swagger docs
- **Controllers**: Decorator-based routing with `@JsonController`, `@Get`, `@Post`, etc.
- **OpenAPI Docs**: Complete Swagger documentation using `@OpenAPI` and `@ResponseSchema`
- **API Standards**: Versioning, naming, status codes, pagination

## When to Use This Skill

Use when you need to:
- Create REST API endpoints for existing use cases
- Add new routes to existing context
- Implement paginated list endpoints
- Build custom API actions

Examples:
- "Create API endpoints for user management"
- "Generate product API with search and filtering"
- "Add order API with status tracking"

## API Design Standards

### Versioning
All controllers MUST be prefixed with `/v1/`:
```typescript
@JsonController('/v1/users')
export class UserController { }
```

### Resource Naming
- Plural nouns: `/v1/users` not `/v1/user`
- Lowercase with hyphens: `/v1/sms-messages`
- No verbs: `/v1/users` not `/v1/getUsers`

### Status Codes
- **200 OK**: GET, PATCH, PUT success
- **201 Created**: POST success (use `@HttpCode(201)`)
- **204 No Content**: DELETE success
- **400 Bad Request**: Validation error
- **401 Unauthorized**: Auth required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **409 Conflict**: Duplicate resource
- **422 Unprocessable Entity**: Business rule violation

### Response Format
ResponseInterceptor middleware wraps all responses:
```typescript
{
  "success": true,
  "data": {...},
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Request DTO Pattern

Create request DTOs in `dto/requests/` with class-validator decorators:

```typescript
// dto/requests/create-entity.dto.ts
import { IsString, IsEmail, IsOptional, IsNumber, IsEnum, Length, Min, Max } from 'class-validator';
import { JSONSchema } from 'class-validator-jsonschema';

export class CreateEntityDto {
  @IsString()
  @Length(1, 100)
  @JSONSchema({
    description: 'Entity name (1-100 characters)',
    minLength: 1,
    maxLength: 100,
    example: 'My Entity',
  })
  name!: string;

  @IsEmail()
  @JSONSchema({
    description: 'Valid email address',
    format: 'email',
    example: 'user@example.com',
  })
  email!: string;

  @IsOptional()
  @IsNumber()
  @Min(0)
  @Max(150)
  @JSONSchema({
    description: 'Age in years (optional)',
    minimum: 0,
    maximum: 150,
    example: 30,
  })
  age?: number;

  @IsEnum(['admin', 'user', 'guest'])
  @JSONSchema({
    description: 'User role',
    enum: ['admin', 'user', 'guest'],
    example: 'user',
  })
  role!: 'admin' | 'user' | 'guest';
}
```

## Response Serializer Pattern

Create response serializers in `dto/responses/` with **BOTH** class-validator decorators AND `@JSONSchema` decorators:

**⚠️ CRITICAL**: Response serializers MUST include class-validator decorators (`@IsString()`, `@IsBoolean()`, etc.) for Swagger schema generation. Without these decorators, `validationMetadatasToSchemas()` cannot generate proper OpenAPI schemas, resulting in generic `["string"]` appearing in Swagger instead of the actual response structure.

```typescript
// dto/responses/entity-response.serializer.ts
import { JSONSchema } from 'class-validator-jsonschema';
import { IsString, IsBoolean, IsDate, IsArray, IsOptional } from 'class-validator';

export class EntityResponseSerializer {
  @IsString()
  @JSONSchema({
    description: 'Entity unique identifier',
    format: 'uuid',
    example: '550e8400-e29b-41d4-a716-446655440000',
  })
  id!: string;

  @IsString()
  @JSONSchema({
    description: 'Entity name',
    example: 'My Entity',
  })
  name!: string;

  @IsString()
  @JSONSchema({
    description: 'Email address',
    format: 'email',
    example: 'user@example.com',
  })
  email!: string;

  @IsBoolean()
  @JSONSchema({
    description: 'Whether entity is active',
    example: true,
  })
  isActive!: boolean;

  @IsArray()
  @JSONSchema({
    description: 'List of tags',
    type: 'array',
    items: { type: 'string' },
    example: ['tag1', 'tag2'],
  })
  tags!: string[];

  @IsString()
  @IsOptional()
  @JSONSchema({
    description: 'Optional description',
    nullable: true,
    example: 'Some description',
  })
  description?: string | null;

  @IsDate()
  @JSONSchema({
    description: 'Creation timestamp',
    format: 'date-time',
    example: '2024-01-15T10:30:00.000Z',
  })
  createdAt!: Date;

  @IsDate()
  @JSONSchema({
    description: 'Last update timestamp',
    format: 'date-time',
    example: '2024-01-15T10:30:00.000Z',
  })
  updatedAt!: Date;
}
```

**Required class-validator decorators for response serializers:**
- `@IsString()` - for string fields
- `@IsBoolean()` - for boolean fields
- `@IsNumber()` - for number fields
- `@IsDate()` - for Date fields
- `@IsArray()` - for array fields
- `@IsOptional()` - for optional/nullable fields

## Controller Pattern

```typescript
// entity.controller.ts
import { JsonController, Get, Post, Patch, Delete, Body, Param, Query, HttpCode } from 'routing-controllers';
import { ResponseSchema, OpenAPI } from 'routing-controllers-openapi';
import { injectable, inject } from 'tsyringe';

import { CurrentUser, RequirePermissions } from '@/global/decorators';
import { Permission } from '@/global/types';
import type { AuthenticatedUser } from '@/global/types/auth.types';

import {
  CreateEntityUseCase,
  FindEntityUseCase,
  UpdateEntityUseCase,
  DeleteEntityUseCase,
  ListEntitiesUseCase,
} from '../application';

import { CreateEntityDto } from './dto/requests/create-entity.dto';
import { UpdateEntityDto } from './dto/requests/update-entity.dto';
import { QueryEntityDto } from './dto/requests/query-entity.dto';
import { EntityResponseSerializer } from './dto/responses/entity-response.serializer';
import { EntityListResponseSerializer } from './dto/responses/entity-list-response.serializer';

@injectable()
@JsonController('/v1/entities')
export class EntityController {
  constructor(
    @inject(CreateEntityUseCase)
    private readonly createUseCase: CreateEntityUseCase,
    @inject(FindEntityUseCase)
    private readonly findUseCase: FindEntityUseCase,
    @inject(UpdateEntityUseCase)
    private readonly updateUseCase: UpdateEntityUseCase,
    @inject(DeleteEntityUseCase)
    private readonly deleteUseCase: DeleteEntityUseCase,
    @inject(ListEntitiesUseCase)
    private readonly listUseCase: ListEntitiesUseCase
  ) {}

  @Post('/')
  @HttpCode(201)
  @ResponseSchema(EntityResponseSerializer, { statusCode: 201 })
  @OpenAPI({
    summary: 'Create entity',
    description: 'Creates a new entity with the provided data',
    tags: ['Entities'],
    security: [{ bearerAuth: [] }],
    responses: {
      '201': { description: 'Entity created successfully' },
      '400': { description: 'Invalid input data' },
      '401': { description: 'Unauthorized' },
      '403': { description: 'Forbidden - insufficient permissions' },
      '409': { description: 'Entity already exists' },
    },
  })
  @RequirePermissions(Permission.ENTITIES_WRITE)
  async create(
    @CurrentUser() user: AuthenticatedUser,
    @Body() body: CreateEntityDto
  ): Promise<EntityResponseSerializer> {
    const result = await this.createUseCase.execute({
      ...body,
      tenantId: user.tenantId,
    });

    return {
      id: result.id,
      name: result.name,
      email: result.email,
      createdAt: result.createdAt,
      updatedAt: result.updatedAt,
    };
  }

  @Get('/:id')
  @ResponseSchema(EntityResponseSerializer)
  @OpenAPI({
    summary: 'Get entity by ID',
    description: 'Retrieves a single entity by its unique identifier',
    tags: ['Entities'],
    security: [{ bearerAuth: [] }],
    responses: {
      '200': { description: 'Entity found' },
      '401': { description: 'Unauthorized' },
      '403': { description: 'Forbidden - insufficient permissions' },
      '404': { description: 'Entity not found' },
    },
  })
  @RequirePermissions(Permission.ENTITIES_READ)
  async findById(
    @Param('id') id: string,
    @CurrentUser() user: AuthenticatedUser
  ): Promise<EntityResponseSerializer> {
    const entity = await this.findUseCase.execute(id);

    return {
      id: entity.id,
      name: entity.name,
      email: entity.email,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
    };
  }

  @Get('/')
  @ResponseSchema(EntityListResponseSerializer)
  @OpenAPI({
    summary: 'List entities',
    description: 'Retrieves a paginated list of entities',
    tags: ['Entities'],
    security: [{ bearerAuth: [] }],
    responses: {
      '200': { description: 'Entities retrieved successfully' },
      '401': { description: 'Unauthorized' },
      '403': { description: 'Forbidden - insufficient permissions' },
    },
  })
  @RequirePermissions(Permission.ENTITIES_READ)
  async list(
    @Query() query: QueryEntityDto,
    @CurrentUser() user: AuthenticatedUser
  ): Promise<EntityListResponseSerializer> {
    const result = await this.listUseCase.execute({
      ...query,
      tenantId: user.tenantId,
    });

    return {
      items: result.items.map((entity) => ({
        id: entity.id,
        name: entity.name,
        email: entity.email,
        createdAt: entity.createdAt,
        updatedAt: entity.updatedAt,
      })),
      total: result.total,
      limit: result.limit,
      offset: result.offset,
    };
  }

  @Patch('/:id')
  @ResponseSchema(EntityResponseSerializer)
  @OpenAPI({
    summary: 'Update entity',
    description: 'Updates an existing entity with partial data',
    tags: ['Entities'],
    security: [{ bearerAuth: [] }],
    responses: {
      '200': { description: 'Entity updated successfully' },
      '400': { description: 'Invalid input data' },
      '401': { description: 'Unauthorized' },
      '403': { description: 'Forbidden - insufficient permissions' },
      '404': { description: 'Entity not found' },
    },
  })
  @RequirePermissions(Permission.ENTITIES_WRITE)
  async update(
    @Param('id') id: string,
    @Body() body: UpdateEntityDto,
    @CurrentUser() user: AuthenticatedUser
  ): Promise<EntityResponseSerializer> {
    const result = await this.updateUseCase.execute({
      id,
      ...body,
    });

    return {
      id: result.id,
      name: result.name,
      email: result.email,
      createdAt: result.createdAt,
      updatedAt: result.updatedAt,
    };
  }

  @Delete('/:id')
  @HttpCode(200)
  @ResponseSchema(EntityResponseSerializer)
  @OpenAPI({
    summary: 'Delete entity',
    description: 'Permanently deletes an entity',
    tags: ['Entities'],
    security: [{ bearerAuth: [] }],
    responses: {
      '200': { description: 'Entity deleted successfully' },
      '401': { description: 'Unauthorized' },
      '403': { description: 'Forbidden - insufficient permissions' },
      '404': { description: 'Entity not found' },
    },
  })
  @RequirePermissions(Permission.ENTITIES_DELETE)
  async delete(
    @Param('id') id: string,
    @CurrentUser() user: AuthenticatedUser
  ): Promise<{ success: boolean }> {
    await this.deleteUseCase.execute(id);
    return { success: true };
  }
}
```

## Error Handling

Domain errors are automatically mapped to HTTP status codes by `GlobalErrorHandler`. No explicit try-catch needed in controllers - just let errors bubble up.

The middleware handles:
- `NotFoundError` → 404
- `ConflictError` → 409
- `ValidationError` → 400
- `UnauthorizedError` → 401
- `ForbiddenError` → 403
- `DomainError` → 422

## Pagination Pattern

```typescript
// dto/requests/query-entity.dto.ts
import { IsOptional, IsNumber, IsString, IsEnum, Min } from 'class-validator';
import { JSONSchema } from 'class-validator-jsonschema';
import { Type } from 'class-transformer';

export class QueryEntityDto {
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(1)
  @JSONSchema({
    description: 'Number of items per page',
    minimum: 1,
    example: 20,
  })
  limit?: number = 20;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(0)
  @JSONSchema({
    description: 'Number of items to skip',
    minimum: 0,
    example: 0,
  })
  offset?: number = 0;

  @IsOptional()
  @IsEnum(['name', 'createdAt'])
  @JSONSchema({
    description: 'Field to sort by',
    enum: ['name', 'createdAt'],
    example: 'createdAt',
  })
  sortBy?: 'name' | 'createdAt' = 'createdAt';

  @IsOptional()
  @IsEnum(['asc', 'desc'])
  @JSONSchema({
    description: 'Sort order',
    enum: ['asc', 'desc'],
    example: 'desc',
  })
  order?: 'asc' | 'desc' = 'desc';

  @IsOptional()
  @IsString()
  @JSONSchema({
    description: 'Search term',
    example: 'john',
  })
  search?: string;
}

// dto/responses/entity-list-response.serializer.ts
import { JSONSchema } from 'class-validator-jsonschema';
import { EntityResponseSerializer } from './entity-response.serializer';

export class EntityListResponseSerializer {
  @JSONSchema({
    description: 'List of entities',
    type: 'array',
    items: { $ref: '#/components/schemas/EntityResponseSerializer' },
  })
  items!: EntityResponseSerializer[];

  @JSONSchema({
    description: 'Total number of entities',
    example: 100,
  })
  total!: number;

  @JSONSchema({
    description: 'Number of items per page',
    example: 20,
  })
  limit!: number;

  @JSONSchema({
    description: 'Number of items skipped',
    example: 0,
  })
  offset!: number;
}
```

## Critical Rules

**MUST DO:**
- Version all routes with `/v1/`
- Use plural resource names
- Create separate request DTOs with class-validator decorators
- Create separate response serializers with `@JSONSchema` decorators
- Use `@JsonController` for routing
- Use route decorators: `@Get`, `@Post`, `@Patch`, `@Delete`
- Use `@CurrentUser()` to inject authenticated user
- Use `@RequirePermissions()` for authorization
- Add `@OpenAPI()` and `@ResponseSchema()` to all endpoints
- Use `@HttpCode(201)` for POST endpoints
- Implement pagination for list endpoints
- Document all response status codes

**MUST NOT:**
- Skip versioning
- Use singular resource names
- Include verbs in resource names
- Put business logic in controller
- Return domain entities directly
- Skip `@OpenAPI()` or `@ResponseSchema()` decorators
- Forget `@JSONSchema()` on DTO/Serializer fields
- Skip error handling or validation

## Generated Files

```
/src/contexts/{Context}/presentation/
├── dto/
│   ├── requests/
│   │   ├── create-{entity}.dto.ts
│   │   ├── update-{entity}.dto.ts
│   │   └── query-{entity}.dto.ts
│   └── responses/
│       ├── {entity}-response.serializer.ts
│       └── {entity}-list-response.serializer.ts
└── {context}.controller.ts
```

## Integration

Add controller to `/src/main.ts`:
```typescript
import { EntityController } from './contexts/entity/presentation/entity.controller';

const routingControllersOptions = {
  controllers: [UserController, TenantController, EntityController],
  // ...
};
```

## Validation Checklist

After generation, verify:
- [ ] Routes versioned with `/v1/`
- [ ] Plural resource names
- [ ] Lowercase-with-hyphens naming
- [ ] Request DTOs with class-validator decorators
- [ ] Response serializers with `@JSONSchema` decorators
- [ ] Controller has `@injectable()` and `@JsonController()`
- [ ] Use cases injected (not repositories)
- [ ] Route decorators used: `@Get`, `@Post`, `@Patch`, `@Delete`
- [ ] `@OpenAPI()` metadata complete
- [ ] `@ResponseSchema()` applied
- [ ] All response codes documented
- [ ] Tags assigned
- [ ] Pagination implemented for lists
- [ ] `@RequirePermissions()` added where needed

## Related Skills

- **ddd-usecase-generator**: Generate use cases called by controllers
- **api-validator**: Validate API standards compliance
- **ddd-validator**: Validate overall DDD compliance
