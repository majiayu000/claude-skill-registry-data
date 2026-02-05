---
name: backend-engineer
description: Expert in Lighthouse Journey Timeline backend architecture, service patterns, testing, and API development using Express.js, TypeScript, and Drizzle ORM. Use when implementing backend services, APIs, controllers, database queries, authentication, permissions, error handling, testing server code, or writing migrations.
---

# Lighthouse Backend Engineer

Expert knowledge of backend patterns and architecture for the Lighthouse Journey Timeline.

## 🏗️ Core Architecture

### Technology Stack

- **Runtime**: Node.js with TypeScript
- **Framework**: Express.js
- **Database**: PostgreSQL with Drizzle ORM
- **DI Container**: Awilix (Proxy injection mode)
- **Testing**: Vitest with vitest-mock-extended
- **Validation**: Zod schemas (CRITICAL: Use across ALL layers)
- **Documentation**: express-jsdoc-swagger → OpenAPI

### Service Layer Architecture

```
HTTP Request → Routes → Middleware → Controller → Service → Repository → Database
                                          ↓           ↓           ↓
                                     Validation  Business    Drizzle
                                     & Mapping     Logic        ORM
```

## 📍 CRITICAL: Where to Look Before Making Changes

### Pattern References (ALWAYS CHECK THESE FIRST)

| Pattern               | Primary Reference                     | Example Implementation                               |
| --------------------- | ------------------------------------- | ---------------------------------------------------- |
| **New Service**       | `src/services/hierarchy-service.ts`   | Complex service with multiple dependencies           |
| **New Controller**    | `src/controllers/user.controller.ts`  | Request validation, error handling, response mapping |
| **New Repository**    | `src/repositories/user-repository.ts` | Drizzle patterns, complex queries                    |
| **New Route**         | `src/routes/hierarchy.routes.ts`      | DI scope resolution, middleware chain                |
| **Response Mapper**   | `src/mappers/user.mapper.ts`          | DTO transformation patterns                          |
| **Unit Tests**        | `src/services/__tests__/*.test.ts`    | Mock setup, test structure                           |
| **Error Codes**       | `src/core/error-codes.ts`             | 70+ standardized error codes                         |
| **API Documentation** | `openapi-schema.yaml`                 | Current API specs - MUST UPDATE                      |

## ⚡ CRITICAL: Zod Validation Across All Layers

### Why Zod Everywhere?

Strong typing with Zod schemas ensures type safety between server and client, catching errors at compile/validation time rather than runtime. **EVERY data boundary must have Zod validation.**

## 🎯 CRITICAL: Use Enums and Constants, Not Magic Strings

**Never use magic strings.** Always use enums or constants for:

- **Error codes**: `src/core/error-codes.ts` - STRING enums (not numbers)
- **Node types**: `z.enum(['job', 'education', 'project', 'event'])`
- **Permission levels**: Define as const objects or Zod enums
- **Status values**: Use Zod enums for type safety
- **Configuration**: Store in constants files, not inline strings

**Example - Error Codes**:

```typescript
// ✅ GOOD: Using enum
export enum ErrorCode {
  USER_NOT_FOUND = 'USER_NOT_FOUND',
  INVALID_PERMISSION = 'INVALID_PERMISSION',
}
throw new AppError(ErrorCode.USER_NOT_FOUND);

// ❌ BAD: Magic strings
throw new AppError('USER_NOT_FOUND');
```

**Example - Zod Enums**:

```typescript
// ✅ GOOD: Zod enum for validation + TypeScript type
const NodeTypeSchema = z.enum(['job', 'education', 'project']);
type NodeType = z.infer<typeof NodeTypeSchema>;

// ❌ BAD: Plain strings
type NodeType = string;
```

### Layer-by-Layer Validation

#### 1. Controller Layer (Request Validation)

```typescript
// Define request/response schemas in controller or separate file
const CreateNodeRequestSchema = z.object({
  type: z.enum(['job', 'education', 'project', 'event']),
  parentId: z.string().uuid().optional(),
  meta: z.object({
    title: z.string().min(1).max(200),
    company: z.string().optional(),
    startDate: z.string().datetime(),
    endDate: z.string().datetime().optional(),
    description: z.string().optional()
  })
});

// In controller method
async createNode(req: Request, res: Response) {
  // Validate request body
  const validatedData = CreateNodeRequestSchema.parse(req.body);
  // validatedData is now strongly typed

  // Pass to service (type-safe)
  const result = await this.nodeService.create(validatedData);
}
```

#### 2. Service Layer (Business Logic Validation)

```typescript
// Service method input schemas
const ServiceCreateNodeSchema = z.object({
  userId: z.number().positive(),
  type: z.enum(['job', 'education', 'project']),
  parentId: z.string().uuid().optional(),
  meta: z.record(z.any())
});

// Service method
async create(input: z.infer<typeof ServiceCreateNodeSchema>) {
  // Additional business validation
  const validated = ServiceCreateNodeSchema.parse(input);

  // Business rules validation
  if (validated.parentId) {
    await this.validateParentAccess(validated.parentId, validated.userId);
  }

  return await this.repository.create(validated);
}
```

#### 3. Repository Layer (Database Schema Validation)

```typescript
// Database insert/update schemas
const DbNodeInsertSchema = z.object({
  id: z.string().uuid().default(() => crypto.randomUUID()),
  type: z.string(),
  userId: z.number(),
  parentId: z.string().uuid().nullable(),
  meta: z.any(), // JSON column
  createdAt: z.date().default(() => new Date()),
  updatedAt: z.date().default(() => new Date())
});

// Repository method
async create(data: unknown) {
  // Validate before database operation
  const dbData = DbNodeInsertSchema.parse(data);
  return await this.db.insert(nodes).values(dbData);
}
```

#### 4. Response Validation (DTO Layer)

```typescript
// Response DTOs with Zod
const NodeResponseSchema = z.object({
  id: z.string().uuid(),
  type: z.string(),
  meta: z.object({
    title: z.string(),
    // ... other fields
  }),
  createdAt: z.string().datetime(),
  permissions: z.object({
    canView: z.boolean(),
    canEdit: z.boolean(),
    canDelete: z.boolean()
  })
});

// In mapper
static toDto(node: unknown): NodeResponseDto {
  // Validate and transform
  return NodeResponseSchema.parse({
    id: node.id,
    type: node.type,
    // ... mapping
  });
}
```

### Shared Schema Patterns

#### Location Strategy

```
packages/
├── schema/
│   └── src/
│       ├── api/                        # ⭐ API Contracts (PRIMARY - ALWAYS USE)
│       │   ├── auth.schemas.ts         # Auth request/response schemas
│       │   ├── user.schemas.ts         # User request/response schemas
│       │   ├── timeline.schemas.ts     # Timeline request/response schemas
│       │   ├── files.schemas.ts        # File upload schemas
│       │   ├── common.schemas.ts       # Shared API schemas (pagination, etc.)
│       │   ├── validation-helpers.ts   # Reusable validators
│       │   └── index.ts                # Re-exports all API schemas
│       ├── schema.ts                   # Drizzle database schema
│       └── types.ts                    # Database type exports
└── server/
    └── src/
        ├── controllers/                # Import from @journey/schema/src/api
        ├── services/                   # Import from @journey/schema/src/api
        └── mappers/                    # Transform DB types → API response types
```

**CRITICAL**:

- All API request/response contracts MUST be defined in `@journey/schema/src/api/`
- Never create validation schemas in `server/src/` - always use `@journey/schema/src/api/`
- Controllers import and use these schemas directly
- This ensures type safety between frontend and backend

#### Reusable Schema Components

```typescript
// packages/schema/src/api/common.schemas.ts (or validation-helpers.ts)
export const uuidSchema = z.string().uuid();
export const dateTimeSchema = z.string().datetime();
export const paginationSchema = z.object({
  page: z.number().positive().default(1),
  limit: z.number().positive().max(100).default(20),
});

// Compose in controller-specific schemas
// packages/schema/src/api/timeline.schemas.ts
import { uuidSchema, paginationSchema } from './common.schemas';

export const getNodesRequestSchema = z.object({
  userId: uuidSchema,
  ...paginationSchema.shape,
});

export type GetNodesRequest = z.infer<typeof getNodesRequestSchema>;
```

### Zod with Drizzle ORM

```typescript
// Generate Zod schemas from Drizzle tables
import { createInsertSchema, createSelectSchema } from 'drizzle-zod';
import { users } from '@journey/schema';

// Auto-generate schemas from Drizzle table definitions
export const insertUserSchema = createInsertSchema(users);
export const selectUserSchema = createSelectSchema(users);

// Extend with custom validations
export const createUserSchema = insertUserSchema
  .extend({
    email: z.string().email(),
    password: z.string().min(8).max(100),
  })
  .omit({ id: true, createdAt: true });
```

### Error Handling for Zod Validation

```typescript
// In controller error handling
import { ZodError } from 'zod';
import { fromZodError } from 'zod-validation-error';

try {
  const validated = schema.parse(req.body);
} catch (error) {
  if (error instanceof ZodError) {
    // Convert to friendly error message
    const validationError = fromZodError(error);
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: validationError.toString(),
        details: error.issues,
      },
    });
  }
  throw error;
}
```

### Type Inference Pattern

```typescript
// Define schema once
const NodeCreateSchema = z.object({
  type: z.enum(['job', 'education']),
  meta: z.object({
    title: z.string(),
    company: z.string().optional(),
  }),
});

// Infer TypeScript type from schema
type NodeCreateInput = z.infer<typeof NodeCreateSchema>;

// Use throughout application
class NodeService {
  async create(input: NodeCreateInput) {
    // input is strongly typed
  }
}
```

### Testing Zod Schemas

```typescript
describe('NodeCreateSchema', () => {
  it('should validate correct input', () => {
    const input = {
      type: 'job',
      meta: { title: 'Software Engineer' },
    };

    expect(() => NodeCreateSchema.parse(input)).not.toThrow();
  });

  it('should reject invalid type', () => {
    const input = {
      type: 'invalid',
      meta: { title: 'Test' },
    };

    expect(() => NodeCreateSchema.parse(input)).toThrow(ZodError);
  });
});
```

### Best Practices

1. **Parse, Don't Validate**: Use `parse()` for runtime validation, `safeParse()` when you need to handle errors
2. **Single Source of Truth**: Define schemas once in `@journey/schema` package
3. **Compose Schemas**: Build complex schemas from simple, reusable parts
4. **Type Inference**: Use `z.infer<>` instead of manually defining types
5. **Validate Early**: Validate at system boundaries (API endpoints, external services)
6. **Document Schemas**: Add descriptions for better OpenAPI generation
   ```typescript
   z.string().describe('User email address');
   ```

## 🔐 Authentication Patterns

### JWT Implementation

- **Access Token**: 15min expiry, contains userId and basic claims
- **Refresh Token**: 7 days, stored in DB, rotated on use
- **Token Service**: `src/services/jwt.service.ts`
- **Refresh Service**: `src/services/refresh-token.service.ts`

### Auth Middleware Stack

```typescript
// From src/middleware/auth.middleware.ts
requireAuth; // Validates JWT, loads user, fails if invalid
optionalAuth; // Validates JWT if present, continues regardless
requireGuest; // Ensures user is NOT authenticated
requireRole(role); // Role-based access control
requirePermission(); // Permission-based access
```

### Token Refresh Flow

1. Client sends refresh token to `/api/auth/refresh`
2. Validate refresh token exists in DB and not expired
3. Rotate: Mark old token as used, create new token pair
4. Return new access + refresh tokens
5. Clean up expired tokens periodically

## 🧪 Unit Testing Patterns

### Test Structure (TDD Approach)

```typescript
// Standard test file structure
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mock, mockDeep } from 'vitest-mock-extended';

describe('ServiceName', () => {
  let service: ServiceName;
  let mockRepo: MockType<Repository>;

  beforeEach(() => {
    vi.clearAllMocks();
    mockRepo = mock<Repository>();
    service = new ServiceName(mockRepo);
  });

  describe('methodName', () => {
    it('should handle success case', async () => {
      // Arrange
      const input = {
        /* test data */
      };
      const expected = {
        /* expected result */
      };
      mockRepo.findById.mockResolvedValue(expected);

      // Act
      const result = await service.method(input);

      // Assert
      expect(result).toEqual(expected);
      expect(mockRepo.findById).toHaveBeenCalledWith(input.id);
    });

    it('should handle error case', async () => {
      // Test error scenarios
    });
  });
});
```

### Common Mock Patterns

```typescript
// Mock with specific return
mockService.method.mockResolvedValue(result);

// Mock with implementation
mockService.method.mockImplementation(async (id) => {
  return id === 'valid' ? data : null;
});

// Mock chainable queries (Drizzle)
const mockQuery = {
  select: vi.fn().mockReturnThis(),
  from: vi.fn().mockReturnThis(),
  where: vi.fn().mockReturnThis(),
  limit: vi.fn().mockResolvedValue([result]),
};

// Reset mocks
mockReset(mockService); // Clear all mock data
mockClear(mockService); // Clear call history only
```

## 🗄️ Database & Schema

### Schema Management

- **Schema Location**: `packages/schema/src/schema.ts`
- **Migrations**: `packages/schema/migrations/`
- **Commands**:
  ```bash
  cd packages/schema
  pnpm db:generate --name migration_name  # Generate migration
  pnpm db:migrate                         # Run migrations
  pnpm db:studio                          # Open Drizzle Studio
  ```

### Drizzle ORM Patterns

```typescript
// Repository pattern example
class UserRepository {
  constructor(private db: NodePgDatabase) {}

  async findById(id: number) {
    return this.db.query.users.findFirst({
      where: eq(users.id, id),
    });
  }

  async search(term: string) {
    return this.db
      .select()
      .from(users)
      .where(
        or(
          ilike(users.firstName, `%${term}%`),
          ilike(users.lastName, `%${term}%`)
        )
      )
      .limit(20);
  }
}
```

## 🔒 Permission Cascade Pattern

### Hierarchy

```
Node Level (most specific)
    ↓
Organization Level (if node belongs to org member)
    ↓
User Level (node owner)
    ↓
Public Level (if explicitly set)
```

### Permission Check Flow

1. **Check Node Policies** (`node_policies` table)
   - Direct user permissions
   - Organization permissions (if user is org member)
   - Public permissions

2. **Check Ownership**
   - Node owner has full access
   - Parent node owners have view access

3. **Apply Most Permissive**
   - If multiple policies exist, most permissive wins
   - DENY effects override ALLOW

### Implementation Reference

- **Service**: `src/services/node-permission.service.ts`
- **Repository**: `src/repositories/node-permission.repository.ts`
- **SQL CTE**: `src/repositories/sql/permission-cte.ts`

## ❌ Error Handling

### Error Code Reference

```typescript
// Location: src/core/error-codes.ts
// NOTE: Error codes are STRING enums, not numbers
export enum ErrorCode {
  // Auth errors
  AUTHENTICATION_REQUIRED = 'AUTHENTICATION_REQUIRED',
  INVALID_TOKEN = 'INVALID_TOKEN',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',

  // Validation errors
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  INVALID_REQUEST = 'INVALID_REQUEST',

  // Resource errors
  NOT_FOUND = 'NOT_FOUND',
  ALREADY_EXISTS = 'ALREADY_EXISTS',

  // Business errors
  BUSINESS_RULE_VIOLATION = 'BUSINESS_RULE_VIOLATION',
  CIRCULAR_REFERENCE = 'CIRCULAR_REFERENCE',
  MAX_DEPTH_EXCEEDED = 'MAX_DEPTH_EXCEEDED',

  // Server errors
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  DATABASE_ERROR = 'DATABASE_ERROR',
  EXTERNAL_SERVICE_ERROR = 'EXTERNAL_SERVICE_ERROR',
}

// Check error-codes.ts for complete list (70+ codes)
```

### Error Usage Pattern

```typescript
// In service layer
throw new ValidationError(ErrorCode.VALIDATION_ERROR, 'Detailed error message');

// In controller - automatically handled by error middleware
// Returns standardized ApiErrorResponse
```

## 📝 API Documentation

### JSDoc Requirements

```typescript
/**
 * @route POST /api/v2/timeline/nodes
 * @summary Create timeline node
 * @description Creates a new node in user's timeline hierarchy
 * @body {CreateNodeDto} Node creation data
 * @response {201} {ApiSuccessResponse<Node>} Node created
 * @response {400} {ApiErrorResponse} Validation error
 * @response {403} {ApiErrorResponse} Permission denied
 * @security BearerAuth
 */
async createNode(req: Request, res: Response) {
  // Implementation
}
```

### OpenAPI Verification

- **Schema File**: `packages/server/openapi-schema.yaml`
- **Generation**: Automatic from JSDoc comments
- **Verification**: After API changes, verify schema is updated:
  ```bash
  pnpm generate:swagger
  # Check git diff on openapi-schema.yaml
  ```

## 📜 One-Time Scripts Pattern

### Script Structure

```typescript
#!/usr/bin/env tsx

/**
 * Script Name and Purpose
 *
 * Run with: NODE_ENV=development tsx scripts/script-name.ts
 */

import { Container } from '../src/core/container-setup';
import { CONTAINER_TOKENS } from '../src/core/container-tokens';

async function main() {
  console.log('🚀 Starting script...');

  // Initialize container (reuse app services)
  await Container.configure(console);
  const container = Container.getRootContainer();

  // Resolve services
  const userService = container.resolve(CONTAINER_TOKENS.USER_SERVICE);
  const hierarchyService = container.resolve(
    CONTAINER_TOKENS.HIERARCHY_SERVICE
  );

  try {
    // Use services exactly like controllers do
    const users = await userService.getAllUsers();

    // Process data...

    console.log('✅ Script completed successfully');
  } catch (error) {
    console.error('❌ Script failed:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}
```

### Script Locations

- **Database Scripts**: `packages/server/scripts/`
- **Migration Scripts**: `packages/schema/migrations/`
- **Package Commands**: See `package.json` scripts section

## 🔄 Response Mapping Patterns

### Mapper Location Strategy

```typescript
// Check for existing mapper
src / mappers / [entity].mapper.ts;

// If none exists, check similar entities
src / mappers / user.mapper.ts; // User-related mappings
src / mappers / experience.mapper.ts; // Experience-related

// Mapper pattern
class EntityMapper {
  static toDto(entity: Entity): EntityDto {
    return {
      id: entity.id,
      // Transform fields
      // Omit internal fields
      // Format dates
    };
  }

  static toDtoArray(entities: Entity[]): EntityDto[] {
    return entities.map((e) => this.toDto(e));
  }
}
```

### Response Wrapper

```typescript
// All responses use standardized format
interface ApiSuccessResponse<T> {
  success: true;
  data: T;
}

// In controller
return res.status(200).json({
  success: true,
  data: UserMapper.toDto(user),
});
```

## 🎯 Development Workflow

### Before Making Changes

1. **Check Pattern References** (table above)
2. **Read Existing Implementation** of similar feature
3. **Check Error Codes** for appropriate errors
4. **Write Tests First** (TDD approach)
5. **Update OpenAPI** documentation via JSDoc

### Common Commands

```bash
# From packages/server
pnpm test:unit              # Run unit tests only (fast)
pnpm test                   # All tests including integration
pnpm dev                    # Start dev server

# Run specific test file (fastest for TDD)
pnpm vitest run --no-coverage src/services/__tests__/user.service.test.ts

# From project root (Nx commands)
pnpm test:changed           # Test only changed packages
pnpm test:changed:all       # Include e2e for changed packages
```

## 📚 Learning & Skill Updates

### How to Update This Skill

1. **Identify New Pattern**: During implementation, notice repeated pattern
2. **Verify Pattern**: Ensure it's used in multiple places
3. **Document Location**: Add to "Pattern References" table
4. **Add Example**: Include minimal code example if complex
5. **Update Skill**: Edit this file at `.claude/skills/backend-engineer/SKILL.md`

### What to Document

- ✅ New service patterns that differ from existing
- ✅ Complex query patterns (CTEs, joins)
- ✅ New middleware patterns
- ✅ Integration patterns with external services
- ✅ Performance optimization patterns
- ❌ One-off implementations
- ❌ Temporary workarounds
- ❌ Feature-specific business logic

### Memory Integration

- **Project Patterns**: Document in Serena memory via `mcp__serena__write_memory`
- **Reusable Patterns**: Save to Memory MCP via `mcp__memory__create_entities`
- **Skill Updates**: Direct edits to this file

## 🚀 Quick Reference

### DI Container Tokens

```typescript
// Infrastructure
CONTAINER_TOKENS.DATABASE;
CONTAINER_TOKENS.LOGGER;

// Services (check container-tokens.ts for complete list)
CONTAINER_TOKENS.USER_SERVICE;
CONTAINER_TOKENS.HIERARCHY_SERVICE;
CONTAINER_TOKENS.NODE_PERMISSION_SERVICE;
// ... 15+ more services

// Controllers
CONTAINER_TOKENS.USER_CONTROLLER;
CONTAINER_TOKENS.HIERARCHY_CONTROLLER;
// ... 9+ controllers
```

### Test Coverage Requirements

- **Target**: 80% coverage minimum
- **Critical Paths**: 100% coverage for auth, permissions
- **Check Coverage**: `pnpm test:coverage`
- **View Report**: `pnpm coverage:html`

### Performance Considerations

- **Query Optimization**: Use Drizzle's query builder over raw SQL
- **Pagination**: Always paginate lists (default 20, max 100)
- **N+1 Prevention**: Use joins or batch queries
- **Caching**: Consider Redis for frequently accessed data

---

**Remember**: Always check existing patterns before implementing new ones. This maintains consistency and reduces technical debt.
