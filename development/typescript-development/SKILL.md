---
name: typescript-development
description: Helps build and extend TypeScript Express APIs using Clean Architecture, inversify dependency injection, Prisma ORM, and Railway deployment patterns established in the upkeep-io project.
---

# TypeScript Development

## Research Protocol

**MANDATORY:** Follow the research protocol in `@shared/research-protocol.md` before implementing backend features.

### When to Research

You MUST use `mcp__Ref__ref_search_documentation` before:
- Using Prisma features you haven't verified this session
- Implementing inversify patterns
- Using Express middleware patterns
- Making Zod validation decisions
- Advising on JWT or authentication patterns

**Never assume training data reflects current library versions. When in doubt, verify.**

## Project Context

This is a **monorepo** property management system with shared libraries:

```
upkeep-io/
├── apps/
│   ├── backend/              # Node/Express API (CommonJS)
│   └── frontend/             # Vue 3 SPA (ES Modules)
└── libs/                     # Shared libraries
    ├── domain/               # Entities, errors (Property, MaintenanceWork, User)
    ├── validators/           # Zod schemas (shared validation)
    └── auth/                 # JWT utilities
```

**Key Principle:** Backend and frontend share validation schemas and domain entities from `libs/` for maximum code reuse.

## Capabilities

- Build new features following Clean Architecture with inversify DI
- Implement JWT + bcrypt authentication
- Create comprehensive unit tests with mocked repositories
- Set up production logging for Railway deployment
- Configure Prisma repositories with type transformations
- Implement shared validation using Zod schemas

## Creating a New Feature

Follow this 8-step workflow that matches the actual project structure:

### 1. Define Domain Entity (if needed)

```typescript
// libs/domain/src/entities/Resource.ts
export interface CreateResourceData {
  userId: string;
  name: string;
  description?: string;
}

export interface Resource extends CreateResourceData {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}
```

### 2. Create Validation Schema

```typescript
// libs/validators/src/resource.ts
import { z } from 'zod';

export const createResourceSchema = z.object({
  userId: z.string().uuid(),
  name: z.string().min(1).max(255),
  description: z.string().max(1000).optional()
});

export type CreateResourceInput = z.infer<typeof createResourceSchema>;
```

### 3. Create Repository Interface

```typescript
// apps/backend/src/domain/repositories/IResourceRepository.ts
import { Resource, CreateResourceData } from '@domain/entities';

export interface IResourceRepository {
  create(data: CreateResourceData): Promise<Resource>;
  findById(id: string): Promise<Resource | null>;
  findByUserId(userId: string): Promise<Resource[]>;
  update(id: string, data: Partial<Resource>): Promise<Resource>;
  delete(id: string): Promise<void>;
}
```

### 4. Implement Use Case

```typescript
// apps/backend/src/application/resource/CreateResourceUseCase.ts
import { injectable, inject } from 'inversify';
import { IResourceRepository } from '../../domain/repositories';
import { ILogger } from '../../domain/services';
import { ValidationError } from '@domain/errors';
import { createResourceSchema } from '@validators/resource';
import { Resource } from '@domain/entities';

interface CreateResourceInput {
  userId: string;
  name: string;
  description?: string;
}

@injectable()
export class CreateResourceUseCase {
  constructor(
    @inject('IResourceRepository') private repository: IResourceRepository,
    @inject('ILogger') private logger: ILogger
  ) {}

  async execute(input: CreateResourceInput): Promise<Resource> {
    // Validate with shared schema
    const validation = createResourceSchema.safeParse(input);
    if (!validation.success) {
      throw new ValidationError(validation.error.errors[0].message);
    }

    // Execute business logic
    const resource = await this.repository.create(validation.data);

    this.logger.info('Resource created', { resourceId: resource.id, userId: input.userId });

    return resource;
  }
}
```

### 5. Create Prisma Repository

```typescript
// apps/backend/src/infrastructure/repositories/PrismaResourceRepository.ts
import { injectable } from 'inversify';
import { PrismaClient } from '@prisma/client';
import { IResourceRepository } from '../../domain/repositories';
import { Resource, CreateResourceData } from '@domain/entities';

@injectable()
export class PrismaResourceRepository implements IResourceRepository {
  private prisma: PrismaClient;

  constructor() {
    this.prisma = new PrismaClient();
  }

  async create(data: CreateResourceData): Promise<Resource> {
    const result = await this.prisma.resource.create({ data });

    // Transform Prisma nulls to undefined for domain entity
    return {
      ...result,
      description: result.description ?? undefined
    };
  }

  async findById(id: string): Promise<Resource | null> {
    const result = await this.prisma.resource.findUnique({ where: { id } });
    if (!result) return null;

    return {
      ...result,
      description: result.description ?? undefined
    };
  }

  async findByUserId(userId: string): Promise<Resource[]> {
    const results = await this.prisma.resource.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' }
    });

    return results.map(r => ({
      ...r,
      description: r.description ?? undefined
    }));
  }

  async update(id: string, data: Partial<Resource>): Promise<Resource> {
    const result = await this.prisma.resource.update({ where: { id }, data });

    return {
      ...result,
      description: result.description ?? undefined
    };
  }

  async delete(id: string): Promise<void> {
    await this.prisma.resource.delete({ where: { id } });
  }
}
```

### 6. Register in Container

```typescript
// apps/backend/src/container.ts
import { IResourceRepository } from './domain/repositories';
import { PrismaResourceRepository } from './infrastructure/repositories';
import { CreateResourceUseCase } from './application/resource';
import { ResourceController } from './presentation/controllers';

export function createContainer(): Container {
  const container = new Container();

  // ... existing bindings ...

  // Repository
  container
    .bind<IResourceRepository>('IResourceRepository')
    .to(PrismaResourceRepository)
    .inTransientScope();

  // Use Case
  container.bind(CreateResourceUseCase).toSelf().inTransientScope();

  // Controller
  container.bind(ResourceController).toSelf().inTransientScope();

  return container;
}
```

### 7. Create Controller

```typescript
// apps/backend/src/presentation/controllers/ResourceController.ts
import { injectable, inject } from 'inversify';
import { Response, NextFunction } from 'express';
import { CreateResourceUseCase } from '../../application/resource';
import { AuthRequest } from '../middleware';

@injectable()
export class ResourceController {
  constructor(
    @inject(CreateResourceUseCase) private createUseCase: CreateResourceUseCase
  ) {}

  async create(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      if (!req.user) {
        res.status(401).json({ error: 'Unauthorized' });
        return;
      }

      const resource = await this.createUseCase.execute({
        ...req.body,
        userId: req.user.userId
      });

      res.status(201).json(resource);
    } catch (error) {
      next(error);
    }
  }
}
```

### 8. Write Unit Tests

```typescript
// apps/backend/src/application/resource/CreateResourceUseCase.unit.test.ts
import { CreateResourceUseCase } from './CreateResourceUseCase';
import { IResourceRepository } from '../../domain/repositories';
import { ILogger } from '../../domain/services';
import { ValidationError } from '@domain/errors';
import { Resource } from '@domain/entities';

describe('CreateResourceUseCase', () => {
  let useCase: CreateResourceUseCase;
  let mockRepository: jest.Mocked<IResourceRepository>;
  let mockLogger: jest.Mocked<ILogger>;

  beforeEach(() => {
    mockRepository = {
      create: jest.fn(),
      findById: jest.fn(),
      findByUserId: jest.fn(),
      update: jest.fn(),
      delete: jest.fn()
    };

    mockLogger = {
      info: jest.fn(),
      warn: jest.fn(),
      error: jest.fn(),
      debug: jest.fn()
    };

    useCase = new CreateResourceUseCase(mockRepository, mockLogger);
  });

  it('should create resource with valid input', async () => {
    const input = {
      userId: 'user-123',
      name: 'Test Resource',
      description: 'Test description'
    };

    const expected: Resource = {
      id: 'resource-456',
      ...input,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    mockRepository.create.mockResolvedValue(expected);

    const result = await useCase.execute(input);

    expect(result).toEqual(expected);
    expect(mockRepository.create).toHaveBeenCalledWith(input);
    expect(mockLogger.info).toHaveBeenCalledWith('Resource created', {
      resourceId: expected.id,
      userId: input.userId
    });
  });

  it('should throw ValidationError when name is empty', async () => {
    const input = {
      userId: 'user-123',
      name: '' // Invalid
    };

    await expect(useCase.execute(input)).rejects.toThrow(ValidationError);
  });
});
```

## Authentication Pattern (JWT + bcrypt)

This project uses **JWT tokens with bcrypt password hashing**, not OAuth.

### Signup Flow

```typescript
// apps/backend/src/application/auth/CreateUserUseCase.ts
@injectable()
export class CreateUserUseCase {
  constructor(
    @inject('IUserRepository') private userRepository: IUserRepository,
    @inject('IPasswordHasher') private passwordHasher: IPasswordHasher,
    @inject('ITokenGenerator') private tokenGenerator: ITokenGenerator
  ) {}

  async execute(input: CreateUserInput): Promise<CreateUserOutput> {
    // 1. Validate with shared schema
    const validation = signupSchema.safeParse(input);
    if (!validation.success) {
      throw new ValidationError(validation.error.errors[0].message);
    }

    // 2. Check for existing user
    const existingUser = await this.userRepository.findByEmail(input.email);
    if (existingUser) {
      throw new ValidationError('User already exists');
    }

    // 3. Hash password
    const passwordHash = await this.passwordHasher.hash(input.password);

    // 4. Create user
    const user = await this.userRepository.create({
      email: input.email,
      passwordHash,
      name: input.name
    });

    // 5. Generate JWT
    const token = this.tokenGenerator.generate({
      userId: user.id,
      email: user.email
    });

    return { user, token };
  }
}
```

### JWT Middleware

```typescript
// apps/backend/src/presentation/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface AuthRequest extends Request {
  user?: {
    userId: string;
    email: string;
  };
}

export function authenticate(req: AuthRequest, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as {
      userId: string;
      email: string;
    };

    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

## Production Logging for Railway (Next Feature)

You're about to deploy to Railway and need diagnostic logging. Here's how to implement it:

### Option 1: Pino (Recommended for Railway)

**Pros:**
- Fastest JSON logger (optimized for stdout)
- Railway-friendly (structured JSON output)
- Low overhead, great for high-throughput APIs
- Built-in request correlation IDs

**Installation:**
```bash
npm install pino pino-pretty
```

**Setup:**
```typescript
// apps/backend/src/infrastructure/services/PinoLogger.ts
import pino from 'pino';
import { ILogger } from '../../domain/services';

export function createPinoLogger(): ILogger {
  const logger = pino({
    level: process.env.LOG_LEVEL || 'info',
    transport: process.env.NODE_ENV === 'development' ? {
      target: 'pino-pretty',
      options: {
        colorize: true,
        translateTime: 'HH:MM:ss Z',
        ignore: 'pid,hostname'
      }
    } : undefined,
    // Railway captures these fields for log aggregation
    base: {
      service: 'upkeep-api',
      environment: process.env.NODE_ENV || 'development'
    }
  });

  return {
    info: (message: string, context?: object) => logger.info(context, message),
    warn: (message: string, context?: object) => logger.warn(context, message),
    error: (message: string, context?: object) => logger.error(context, message),
    debug: (message: string, context?: object) => logger.debug(context, message)
  };
}
```

### Option 2: Winston

**Pros:**
- More features (multiple transports, custom formats)
- Better for complex logging requirements
- Larger ecosystem

**Cons:**
- Heavier than Pino
- More configuration needed

### Option 3: Enhanced Console Logger

Keep it simple if you don't need advanced features:

```typescript
// apps/backend/src/infrastructure/services/StructuredConsoleLogger.ts
import { ILogger } from '../../domain/services';

export class StructuredConsoleLogger implements ILogger {
  info(message: string, context?: object): void {
    console.log(JSON.stringify({
      level: 'info',
      message,
      timestamp: new Date().toISOString(),
      ...context
    }));
  }

  error(message: string, context?: object): void {
    console.error(JSON.stringify({
      level: 'error',
      message,
      timestamp: new Date().toISOString(),
      ...context
    }));
  }

  warn(message: string, context?: object): void {
    console.warn(JSON.stringify({
      level: 'warn',
      message,
      timestamp: new Date().toISOString(),
      ...context
    }));
  }

  debug(message: string, context?: object): void {
    if (process.env.LOG_LEVEL === 'debug') {
      console.debug(JSON.stringify({
        level: 'debug',
        message,
        timestamp: new Date().toISOString(),
        ...context
      }));
    }
  }
}
```

### Request Correlation IDs

Track requests across use cases and repositories:

```typescript
// apps/backend/src/presentation/middleware/requestId.ts
import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

export function requestIdMiddleware(req: Request, res: Response, next: NextFunction) {
  const requestId = uuidv4();
  req.headers['x-request-id'] = requestId;
  res.setHeader('x-request-id', requestId);
  next();
}

// Use in use cases:
this.logger.info('Creating resource', {
  requestId: req.headers['x-request-id'],
  userId: input.userId
});
```

### Performance Logging

Track slow operations:

```typescript
async execute(input: CreateResourceInput): Promise<Resource> {
  const start = Date.now();

  try {
    // ... business logic ...

    const duration = Date.now() - start;
    this.logger.info('Resource created', {
      resourceId: resource.id,
      duration
    });

    if (duration > 1000) {
      this.logger.warn('Slow operation detected', {
        operation: 'CreateResource',
        duration
      });
    }

    return resource;
  } catch (error) {
    this.logger.error('Failed to create resource', {
      error: error.message,
      stack: error.stack,
      userId: input.userId
    });
    throw error;
  }
}
```

## Railway Deployment

### Required Configuration

**railway.json:**
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm ci && npm run build && npx prisma generate"
  },
  "deploy": {
    "startCommand": "npm run start",
    "healthcheckPath": "/api/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

### Environment Variables

Set in Railway dashboard:

```env
# Database (Railway provides this)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Server
PORT=${{PORT}}
NODE_ENV=production
LOG_LEVEL=info

# Authentication
JWT_SECRET=<generate-secure-random-string>
JWT_EXPIRY=7d

# Frontend (for CORS)
FRONTEND_URL=https://your-frontend.railway.app
```

### Database Migrations

**Development (Prisma):**
```bash
npm run migrate:dev          # Create and apply migration
npm run generate             # Regenerate Prisma client
```

**Production (Flyway):**
1. Prisma generates SQL in `prisma/migrations/`
2. Copy to `migrations/V{number}__{name}.sql`
3. GitHub Actions runs Flyway before deployment
4. Atomic, transactional migrations with rollback

### Health Check Endpoint

```typescript
// apps/backend/src/presentation/routes/health.ts
router.get('/api/health', async (req, res) => {
  try {
    // Check database connection
    await prisma.$queryRaw`SELECT 1`;

    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime()
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message
    });
  }
});
```

## Key Patterns

### inversify Dependency Injection

```typescript
// ALWAYS required in tsconfig.json:
{
  "experimentalDecorators": true,
  "emitDecoratorMetadata": true
}

// MUST be first import in server.ts:
import 'reflect-metadata';
```

### Shared Validation (DRY)

```typescript
// libs/validators/src/property.ts - SINGLE SOURCE OF TRUTH
export const createPropertySchema = z.object({
  street: z.string().min(1),
  city: z.string().min(1),
  state: z.string().length(2),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/)
});

// Backend use case imports it
import { createPropertySchema } from '@validators/property';

// Frontend form imports THE SAME schema
import { toTypedSchema } from '@vee-validate/zod';
import { createPropertySchema } from '@validators/property';

const schema = toTypedSchema(createPropertySchema);
```

### Type Transformations (Prisma → Domain)

```typescript
// Prisma returns Decimal and nulls, domain expects number and undefined
return {
  ...property,
  address2: property.address2 ?? undefined,
  purchasePrice: property.purchasePrice ? property.purchasePrice.toNumber() : undefined
};
```

## References

See [reference.md](reference.md) for:
- Clean Architecture layer details
- Testing strategy and mock factories
- Railway deployment configuration
- API design patterns
- Security middleware setup

See [examples.md](examples.md) for:
- Complete feature implementation (MaintenanceWork)
- Full use case examples with tests
- Repository patterns with Prisma
- Controller and routing setup
