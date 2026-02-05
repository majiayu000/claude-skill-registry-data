---
name: fastify-patterns
description: Fastify framework patterns including routing, plugins, and decorators. Use when building Fastify APIs.
---

# Fastify Patterns Skill

This skill covers Fastify 5.x patterns for building high-performance Node.js APIs.

## When to Use

Use this skill when:
- Building REST APIs with Fastify
- Creating reusable plugins
- Implementing schema-based validation
- Designing middleware patterns

## Core Principle

**SCHEMA-FIRST DEVELOPMENT** - Define schemas before implementation. Fastify uses schemas for validation and serialization.

## Project Setup

### Installation

```bash
npm install fastify @fastify/cors @fastify/jwt @fastify/swagger
npm install -D @types/node
```

### Basic Application

```typescript
// src/app.ts
import Fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';

export async function buildApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: process.env.LOG_LEVEL ?? 'info',
      transport: process.env.NODE_ENV === 'development'
        ? { target: 'pino-pretty' }
        : undefined,
    },
  });

  // Register plugins
  await app.register(cors, {
    origin: process.env.CORS_ORIGIN ?? true,
  });

  // Register routes
  await app.register(import('./routes'));

  return app;
}
```

```typescript
// src/index.ts
import { buildApp } from './app';

const start = async (): Promise<void> => {
  const app = await buildApp();

  try {
    const port = parseInt(process.env.PORT ?? '3000', 10);
    await app.listen({ port, host: '0.0.0.0' });
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
```

## Route Patterns

### Basic Routes

```typescript
// src/routes/index.ts
import { FastifyPluginAsync } from 'fastify';

const routes: FastifyPluginAsync = async (fastify) => {
  await fastify.register(import('./health'));
  await fastify.register(import('./users'), { prefix: '/api/users' });
  await fastify.register(import('./posts'), { prefix: '/api/posts' });
};

export default routes;
```

### Schema-Based Route

```typescript
// src/routes/users.ts
import { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

const UserResponseSchema = z.object({
  id: z.string(),
  email: z.string(),
  name: z.string(),
  createdAt: z.string(),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;
type UserResponse = z.infer<typeof UserResponseSchema>;

const usersRoutes: FastifyPluginAsync = async (fastify) => {
  // GET /api/users
  fastify.get<{ Reply: UserResponse[] }>('/', {
    schema: {
      response: {
        200: zodToJsonSchema(z.array(UserResponseSchema)),
      },
    },
  }, async () => {
    return fastify.db.user.findMany();
  });

  // POST /api/users
  fastify.post<{ Body: CreateUserInput; Reply: UserResponse }>('/', {
    schema: {
      body: zodToJsonSchema(CreateUserSchema),
      response: {
        201: zodToJsonSchema(UserResponseSchema),
      },
    },
  }, async (request, reply) => {
    const user = await fastify.db.user.create({
      data: request.body,
    });
    return reply.status(201).send(user);
  });

  // GET /api/users/:id
  fastify.get<{ Params: { id: string }; Reply: UserResponse }>('/:id', {
    schema: {
      params: zodToJsonSchema(z.object({ id: z.string() })),
    },
  }, async (request, reply) => {
    const user = await fastify.db.user.findUnique({
      where: { id: request.params.id },
    });

    if (!user) {
      return reply.status(404).send({ error: 'User not found' });
    }

    return user;
  });
};

export default usersRoutes;
```

## Plugin Patterns

### Database Plugin

```typescript
// src/plugins/database.ts
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';
import { PrismaClient } from '@prisma/client';

declare module 'fastify' {
  interface FastifyInstance {
    db: PrismaClient;
  }
}

const databasePlugin: FastifyPluginAsync = async (fastify) => {
  const prisma = new PrismaClient({
    log: ['query', 'info', 'warn', 'error'],
  });

  await prisma.$connect();

  fastify.decorate('db', prisma);

  fastify.addHook('onClose', async () => {
    await prisma.$disconnect();
  });
};

export default fp(databasePlugin, {
  name: 'database',
});
```

### Authentication Plugin

```typescript
// src/plugins/auth.ts
import { FastifyPluginAsync, FastifyRequest } from 'fastify';
import fp from 'fastify-plugin';
import jwt from '@fastify/jwt';

declare module 'fastify' {
  interface FastifyInstance {
    authenticate: (request: FastifyRequest) => Promise<void>;
  }
}

declare module '@fastify/jwt' {
  interface FastifyJWT {
    payload: { userId: string; role: string };
    user: { userId: string; role: string };
  }
}

const authPlugin: FastifyPluginAsync = async (fastify) => {
  await fastify.register(jwt, {
    secret: process.env.JWT_SECRET ?? 'your-secret-key',
  });

  fastify.decorate('authenticate', async (request: FastifyRequest) => {
    await request.jwtVerify();
  });
};

export default fp(authPlugin, {
  name: 'auth',
});
```

## Hook Patterns

### Request Lifecycle Hooks

```typescript
// src/hooks/logging.ts
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';

const loggingHooks: FastifyPluginAsync = async (fastify) => {
  fastify.addHook('onRequest', async (request) => {
    request.log.info({
      method: request.method,
      url: request.url
    }, 'incoming request');
  });

  fastify.addHook('onResponse', async (request, reply) => {
    request.log.info({
      method: request.method,
      url: request.url,
      statusCode: reply.statusCode,
      responseTime: reply.elapsedTime,
    }, 'request completed');
  });

  fastify.addHook('onError', async (request, reply, error) => {
    request.log.error({
      method: request.method,
      url: request.url,
      error: error.message,
    }, 'request error');
  });
};

export default fp(loggingHooks);
```

## Error Handling

### Global Error Handler

```typescript
// src/plugins/error-handler.ts
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';
import { ZodError } from 'zod';

interface ErrorResponse {
  error: string;
  code: string;
  statusCode: number;
  details?: unknown;
}

const errorHandler: FastifyPluginAsync = async (fastify) => {
  fastify.setErrorHandler((error, request, reply) => {
    request.log.error(error);

    // Zod validation errors
    if (error instanceof ZodError) {
      const response: ErrorResponse = {
        error: 'Validation failed',
        code: 'VALIDATION_ERROR',
        statusCode: 400,
        details: error.errors,
      };
      return reply.status(400).send(response);
    }

    // Fastify validation errors
    if (error.validation) {
      const response: ErrorResponse = {
        error: 'Validation failed',
        code: 'VALIDATION_ERROR',
        statusCode: 400,
        details: error.validation,
      };
      return reply.status(400).send(response);
    }

    // Default error response
    const statusCode = error.statusCode ?? 500;
    const response: ErrorResponse = {
      error: statusCode >= 500 ? 'Internal Server Error' : error.message,
      code: error.code ?? 'INTERNAL_ERROR',
      statusCode,
    };

    return reply.status(statusCode).send(response);
  });
};

export default fp(errorHandler);
```

## Testing Patterns

### Route Testing

```typescript
// src/routes/__tests__/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { FastifyInstance } from 'fastify';
import { buildApp } from '../../app';

describe('Users routes', () => {
  let app: FastifyInstance;

  beforeAll(async () => {
    app = await buildApp();
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  it('creates a user with valid data', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/users',
      payload: {
        email: 'test@example.com',
        name: 'Test User',
      },
    });

    expect(response.statusCode).toBe(201);
    expect(response.json()).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    });
  });

  it('rejects invalid email', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/users',
      payload: {
        email: 'invalid-email',
        name: 'Test User',
      },
    });

    expect(response.statusCode).toBe(400);
  });
});
```

## OpenAPI Documentation

```typescript
// src/plugins/swagger.ts
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';

const swaggerPlugin: FastifyPluginAsync = async (fastify) => {
  await fastify.register(swagger, {
    openapi: {
      info: {
        title: 'API Documentation',
        version: '1.0.0',
      },
      servers: [
        { url: 'http://localhost:3000', description: 'Development' },
      ],
    },
  });

  await fastify.register(swaggerUi, {
    routePrefix: '/docs',
  });
};

export default fp(swaggerPlugin);
```

## Best Practices

1. **Use plugins** - Encapsulate functionality in plugins
2. **Schema-first** - Define schemas for all routes
3. **Type decorations** - Extend FastifyInstance types properly
4. **Fastify-plugin** - Use `fp()` for plugins that need encapsulation
5. **Lifecycle hooks** - Use hooks for cross-cutting concerns
6. **Error handling** - Centralize error handling

## Notes

- Fastify auto-validates with JSON Schema
- Use `zodToJsonSchema` for Zod integration
- Plugins are encapsulated by default (use `fp()` to share)
- Always type route handlers with generics
