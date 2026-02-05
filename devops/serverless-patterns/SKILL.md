---
name: serverless-patterns
description: Serverless deployment patterns for Node.js. Use when deploying to serverless platforms.
---

# Serverless Patterns Skill

This skill covers serverless deployment patterns for Node.js applications.

## When to Use

Use this skill when:
- Deploying to Vercel, AWS Lambda, Cloudflare Workers
- Building serverless APIs
- Optimizing cold start performance
- Designing for serverless constraints

## Core Principle

**STATELESS AND FAST** - No persistent state. Minimize cold starts. Design for request-response lifecycle.

## Vercel Serverless Functions

### Project Structure

```
my-api/
├── api/
│   ├── health.ts          # /api/health
│   ├── users/
│   │   ├── index.ts       # /api/users (GET, POST)
│   │   └── [id].ts        # /api/users/:id
│   └── auth/
│       ├── login.ts       # /api/auth/login
│       └── register.ts    # /api/auth/register
├── lib/
│   ├── db.ts
│   └── auth.ts
├── vercel.json
└── package.json
```

### Basic Handler

```typescript
// api/health.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default function handler(
  req: VercelRequest,
  res: VercelResponse
): VercelResponse {
  return res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
  });
}
```

### CRUD Handler

```typescript
// api/users/index.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';
import { prisma } from '../../lib/db';
import { authenticate } from '../../lib/auth';
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
): Promise<VercelResponse> {
  try {
    if (req.method === 'GET') {
      const users = await prisma.user.findMany({
        select: { id: true, email: true, name: true },
      });
      return res.status(200).json(users);
    }

    if (req.method === 'POST') {
      const body = CreateUserSchema.parse(req.body);
      const user = await prisma.user.create({ data: body });
      return res.status(201).json(user);
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors });
    }
    console.error(error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
```

### Dynamic Route Handler

```typescript
// api/users/[id].ts
import type { VercelRequest, VercelResponse } from '@vercel/node';
import { prisma } from '../../lib/db';

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
): Promise<VercelResponse> {
  const { id } = req.query;

  if (typeof id !== 'string') {
    return res.status(400).json({ error: 'Invalid ID' });
  }

  try {
    if (req.method === 'GET') {
      const user = await prisma.user.findUnique({ where: { id } });
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      return res.status(200).json(user);
    }

    if (req.method === 'PUT') {
      const user = await prisma.user.update({
        where: { id },
        data: req.body,
      });
      return res.status(200).json(user);
    }

    if (req.method === 'DELETE') {
      await prisma.user.delete({ where: { id } });
      return res.status(204).end();
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
```

### vercel.json

```json
{
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/$1" }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "GET, POST, PUT, DELETE, OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type, Authorization" }
      ]
    }
  ]
}
```

## AWS Lambda

### Handler Pattern

```typescript
// src/handlers/users.ts
import { APIGatewayProxyHandler, APIGatewayProxyResult } from 'aws-lambda';
import { prisma } from '../lib/db';
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});

export const createUser: APIGatewayProxyHandler = async (event) => {
  try {
    const body = JSON.parse(event.body ?? '{}');
    const data = CreateUserSchema.parse(body);

    const user = await prisma.user.create({ data });

    return {
      statusCode: 201,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user),
    };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: error.errors }),
      };
    }
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
};

export const getUser: APIGatewayProxyHandler = async (event) => {
  const id = event.pathParameters?.id;

  if (!id) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing ID' }),
    };
  }

  const user = await prisma.user.findUnique({ where: { id } });

  if (!user) {
    return {
      statusCode: 404,
      body: JSON.stringify({ error: 'User not found' }),
    };
  }

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  };
};
```

### Serverless Framework Config

```yaml
# serverless.yml
service: my-api
frameworkVersion: '3'

provider:
  name: aws
  runtime: nodejs20.x
  stage: ${opt:stage, 'dev'}
  region: us-east-1
  environment:
    DATABASE_URL: ${env:DATABASE_URL}
    NODE_OPTIONS: --enable-source-maps

functions:
  createUser:
    handler: dist/handlers/users.createUser
    events:
      - http:
          path: users
          method: post
          cors: true

  getUser:
    handler: dist/handlers/users.getUser
    events:
      - http:
          path: users/{id}
          method: get
          cors: true

plugins:
  - serverless-esbuild

custom:
  esbuild:
    bundle: true
    minify: true
    sourcemap: true
    target: 'node20'
```

## Cloudflare Workers

### Worker Handler

```typescript
// src/worker.ts
import { Router } from 'itty-router';

interface Env {
  DATABASE_URL: string;
}

const router = Router();

router.get('/api/health', () => {
  return Response.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
  });
});

router.get('/api/users', async (request, env: Env) => {
  // Use D1 or external database
  const users = await fetchUsers(env.DATABASE_URL);
  return Response.json(users);
});

router.post('/api/users', async (request, env: Env) => {
  const body = await request.json();
  const user = await createUser(env.DATABASE_URL, body);
  return Response.json(user, { status: 201 });
});

router.all('*', () => {
  return Response.json({ error: 'Not found' }, { status: 404 });
});

export default {
  fetch: (request: Request, env: Env) => router.handle(request, env),
};
```

### wrangler.toml

```toml
name = "my-api"
main = "src/worker.ts"
compatibility_date = "2024-01-01"

[vars]
NODE_ENV = "production"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xxx"
```

## Cold Start Optimization

### Lazy Loading

```typescript
// lib/db.ts - Lazy initialization
import { PrismaClient } from '@prisma/client';

let prisma: PrismaClient | null = null;

export function getPrisma(): PrismaClient {
  if (!prisma) {
    prisma = new PrismaClient();
  }
  return prisma;
}
```

### Connection Pooling

```typescript
// Use connection pooler for serverless
// Prisma Data Proxy or PgBouncer

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL, // Use pooler URL
    },
  },
});
```

### Bundle Optimization

```typescript
// tsup.config.ts - Optimize bundle
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/handlers/**/*.ts'],
  format: ['esm'],
  target: 'node20',
  clean: true,
  minify: true,
  treeshake: true,
  external: ['@prisma/client'],
});
```

## Middleware Pattern

```typescript
// lib/middleware.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

type Handler = (req: VercelRequest, res: VercelResponse) => Promise<VercelResponse>;
type Middleware = (handler: Handler) => Handler;

export const withCors: Middleware = (handler) => async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  return handler(req, res);
};

export const withAuth: Middleware = (handler) => async (req, res) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    // Verify token
    const user = await verifyToken(token);
    (req as any).user = user;
    return handler(req, res);
  } catch {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Compose middleware
export const compose = (...middlewares: Middleware[]) => (handler: Handler): Handler => {
  return middlewares.reduceRight((h, m) => m(h), handler);
};

// Usage
export default compose(withCors, withAuth)(async (req, res) => {
  const user = (req as any).user;
  return res.json({ message: `Hello, ${user.name}` });
});
```

## Error Handling

```typescript
// lib/errors.ts
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function withErrorHandling(handler: Handler): Handler {
  return async (req, res) => {
    try {
      return await handler(req, res);
    } catch (error) {
      if (error instanceof ApiError) {
        return res.status(error.statusCode).json({
          error: error.message,
          code: error.code,
        });
      }

      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      }

      console.error('Unhandled error:', error);
      return res.status(500).json({ error: 'Internal server error' });
    }
  };
}
```

## Best Practices

1. **Minimize dependencies** - Smaller bundles = faster cold starts
2. **Connection pooling** - Use external pooler for databases
3. **Lazy initialization** - Initialize on first request
4. **Stateless design** - No persistent state between requests
5. **Error handling** - Catch and log all errors
6. **Response caching** - Use CDN edge caching when possible

## Notes

- Cold starts vary by platform (50ms-500ms)
- Database connections are the main cold start cost
- Use edge functions for low-latency responses
- Monitor invocation counts and duration
