---
name: backend-master
description: Master skill for TypeScript backend development. Decision framework for APIs (tRPC/REST), authentication (Auth.js/Passport), database (Prisma), validation (Zod), logging (Pino), testing (Vitest), and deployment (Docker). Routes to specialized skills for implementation. Use as entry point for any backend task.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Backend Master Skill

Unified decision framework for TypeScript backend development.

**Stack:** Node.js · TypeScript · tRPC/Express · Prisma · Zod · Vitest · Docker

---

## Quick Decision Matrix

```yaml
WHAT DO YOU NEED?
│
├─► API Layer
│   ├─ Full-stack TypeScript app → tRPC [skill: backend-trpc]
│   ├─ Need REST for external clients → tRPC + OpenAPI [skill: backend-trpc-openapi]
│   └─ Pure Express API → Express + Zod
│
├─► Authentication
│   ├─ Next.js App Router → Auth.js [skill: backend-auth-js]
│   └─ Express/pure API → Passport.js [skill: backend-passport-js]
│
├─► Database
│   └─ TypeScript + SQL → Prisma [skill: backend-prisma]
│
├─► Validation
│   └─ Any input validation → Zod [skill: backend-zod]
│
├─► Observability
│   └─ Structured logging → Pino [skill: backend-pino]
│
├─► Testing
│   └─ Unit/integration tests → Vitest [skill: backend-vitest]
│
└─► Deployment
    └─ Containerization → Docker [skill: docker-node]
```

---

## 1. Project Setup Checklist

### New tRPC + Prisma Project

```bash
# Initialize
mkdir my-api && cd my-api
npm init -y

# Core dependencies
npm install @trpc/server zod @prisma/client pino
npm install -D typescript @types/node prisma vitest

# Initialize TypeScript
npx tsc --init

# Initialize Prisma
npx prisma init
```

### Recommended tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "resolveJsonModule": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Recommended Structure

```
src/
├── server/
│   ├── trpc.ts              # tRPC instance, base procedures
│   ├── context.ts           # Request context
│   └── routers/
│       ├── _app.ts          # Root router (merges all)
│       ├── user.ts          # User procedures
│       └── post.ts          # Post procedures
├── lib/
│   ├── prisma.ts            # Prisma singleton
│   ├── logger.ts            # Pino configuration
│   └── env.ts               # Environment validation
├── schemas/
│   ├── user.schema.ts       # User Zod schemas
│   └── common.schema.ts     # Shared schemas
├── middleware/
│   ├── auth.ts              # Auth middleware
│   └── logging.ts           # Request logging
└── index.ts                 # Entry point

prisma/
├── schema.prisma            # Database schema
└── migrations/              # Migration history

test/
├── setup.ts                 # Test setup
└── context.ts               # Mock context factory
```

---

## 2. API Layer Decision

### tRPC vs REST Decision Tree

```yaml
Building an API?
│
├─► Who are the clients?
│   │
│   ├─► Only TypeScript (Next.js, React)
│   │   └─► Pure tRPC ✓
│   │       - End-to-end type safety
│   │       - No code generation
│   │       - Automatic request batching
│   │
│   ├─► TypeScript + external clients (mobile, third-party)
│   │   └─► tRPC + OpenAPI ✓
│   │       - Type-safe internal API
│   │       - REST endpoints for external
│   │       - Swagger documentation
│   │
│   └─► Only external/non-TypeScript clients
│       └─► Express + OpenAPI ✓
│           - Standard REST
│           - Maximum compatibility
```

### tRPC Quick Setup

→ See **[backend-trpc]** for full guide

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { z } from 'zod';

interface Context {
  user?: { id: string; role: string };
  db: PrismaClient;
  log: Logger;
}

const t = initTRPC.context<Context>().create();

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;

// Auth middleware
const isAuthed = middleware(async ({ ctx, next }) => {
  if (!ctx.user) throw new TRPCError({ code: 'UNAUTHORIZED' });
  return next({ ctx: { user: ctx.user } });
});

export const protectedProcedure = publicProcedure.use(isAuthed);
```

### When to Add OpenAPI

→ See **[backend-trpc-openapi]** for full guide

```typescript
// Add OpenAPI meta to expose as REST
.meta({
  openapi: {
    method: 'GET',
    path: '/users/{id}',
    tags: ['Users'],
  },
})
```

| Scenario | Recommendation |
|----------|----------------|
| Internal TypeScript clients | Pure tRPC |
| Third-party integrations | tRPC + OpenAPI |
| Public API documentation | tRPC + OpenAPI |
| Mobile apps (non-React Native) | tRPC + OpenAPI |
| Microservices (mixed languages) | OpenAPI/REST |

---

## 3. Authentication Decision

### Auth.js vs Passport.js

```yaml
Need authentication?
│
├─► Next.js App Router?
│   └─► Auth.js (NextAuth.js v5) ✓
│       - Native Next.js integration
│       - OAuth providers built-in
│       - Serverless/Edge ready
│
└─► Express.js / Pure API?
    └─► Passport.js ✓
        - JWT authentication
        - 500+ strategies
        - Maximum control
```

### Auth.js Quick Setup (Next.js)

→ See **[backend-auth-js]** for full guide

```typescript
// auth.ts
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import { PrismaAdapter } from '@auth/prisma-adapter';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'jwt' },
  providers: [GitHub],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.id = user.id;
      return token;
    },
    session({ session, token }) {
      session.user.id = token.id as string;
      return session;
    },
  },
});
```

### Passport.js Quick Setup (Express)

→ See **[backend-passport-js]** for full guide

```typescript
// src/strategies/jwt.strategy.ts
import passport from 'passport';
import { Strategy as JwtStrategy, ExtractJwt } from 'passport-jwt';

passport.use(new JwtStrategy({
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: process.env.JWT_SECRET!,
}, async (payload, done) => {
  const user = await prisma.user.findUnique({ where: { id: payload.sub } });
  return done(null, user || false);
}));
```

| Feature | Auth.js | Passport.js |
|---------|---------|-------------|
| Best for | Next.js | Express |
| OAuth setup | Minimal | Manual |
| JWT support | Built-in | passport-jwt |
| Session storage | JWT/DB | Manual |
| Serverless | Yes | Limited |
| Strategies | ~20 | 500+ |

---

## 4. Database Layer (Prisma)

→ See **[backend-prisma]** for full guide

### Singleton Pattern (Required)

```typescript
// src/lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient({
  log: process.env.NODE_ENV === 'development' 
    ? ['query', 'error', 'warn'] 
    : ['error'],
});

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

### Essential Schema Patterns

```prisma
// prisma/schema.prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Post {
  id        String   @id @default(cuid())
  title     String   @db.VarChar(255)
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  
  @@index([authorId])
  @@index([createdAt(sort: Desc)])
}

enum Role {
  USER
  ADMIN
}
```

### Migration Commands

```bash
npx prisma migrate dev --name init    # Development
npx prisma migrate deploy             # Production
npx prisma generate                   # Regenerate client
npx prisma studio                     # GUI viewer
```

---

## 5. Validation Layer (Zod)

→ See **[backend-zod]** for full guide

### Core Patterns

```typescript
// src/schemas/user.schema.ts
import { z } from 'zod';

// Base schema
export const UserSchema = z.object({
  id: z.string().cuid(),
  email: z.string().email(),
  name: z.string().min(2).max(100),
  role: z.enum(['USER', 'ADMIN']),
});

// Derive variations
export const CreateUserSchema = UserSchema.omit({ id: true });
export const UpdateUserSchema = CreateUserSchema.partial();

// Infer types
export type User = z.infer<typeof UserSchema>;
export type CreateUser = z.infer<typeof CreateUserSchema>;
```

### Common Schemas

```typescript
// src/schemas/common.schema.ts
export const PaginationSchema = z.object({
  limit: z.number().min(1).max(100).default(10),
  cursor: z.string().optional(),
});

export const IdSchema = z.object({
  id: z.string().cuid(),
});

// Environment validation
export const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  PORT: z.coerce.number().default(3000),
});

export const env = EnvSchema.parse(process.env);
```

### Zod + tRPC Integration

```typescript
// Zod validates input automatically
export const userRouter = router({
  create: protectedProcedure
    .input(CreateUserSchema)
    .mutation(({ input, ctx }) => {
      // input is typed as CreateUser
      return ctx.db.user.create({ data: input });
    }),
});
```

---

## 6. Logging (Pino)

→ See **[backend-pino]** for full guide

### Configuration

```typescript
// src/lib/logger.ts
import pino from 'pino';

const isDev = process.env.NODE_ENV === 'development';

export const logger = pino({
  level: process.env.LOG_LEVEL || (isDev ? 'debug' : 'info'),
  
  transport: isDev ? {
    target: 'pino-pretty',
    options: { colorize: true },
  } : undefined,
  
  redact: {
    paths: ['password', 'token', '*.password', 'req.headers.authorization'],
    censor: '[REDACTED]',
  },
  
  base: {
    service: process.env.SERVICE_NAME || 'api',
    env: process.env.NODE_ENV,
  },
});
```

### Request Logging Middleware

```typescript
// src/middleware/logging.ts
export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const requestId = req.headers['x-request-id'] || randomUUID();
  const start = Date.now();

  req.log = logger.child({ requestId, method: req.method, path: req.path });
  req.log.info('Request started');

  res.on('finish', () => {
    req.log.info({ statusCode: res.statusCode, duration: Date.now() - start }, 'Request completed');
  });

  next();
}
```

### Structured Logging Rules

```typescript
// ❌ String interpolation
logger.info(`User ${userId} logged in from ${ip}`);

// ✅ Structured objects
logger.info({ userId, ip, action: 'login' }, 'User logged in');
```

---

## 7. Testing (Vitest)

→ See **[backend-vitest]** for full guide

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    globals: true,
    environment: 'node',
    include: ['**/*.test.ts'],
    setupFiles: ['./test/setup.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
    },
  },
});
```

### Mock Context Factory

```typescript
// test/context.ts
import { mockDeep, DeepMockProxy } from 'vitest-mock-extended';
import { PrismaClient } from '@prisma/client';

export type MockContext = {
  prisma: DeepMockProxy<PrismaClient>;
  user: { id: string; role: string } | null;
};

export const createMockContext = (user = null): MockContext => ({
  prisma: mockDeep<PrismaClient>(),
  user,
});
```

### Testing tRPC Procedures

```typescript
// src/server/routers/user.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { createCallerFactory } from '../trpc';
import { userRouter } from './user';
import { createMockContext } from '@/test/context';

describe('User Router', () => {
  let mockCtx: MockContext;
  const createCaller = createCallerFactory(userRouter);

  beforeEach(() => {
    mockCtx = createMockContext();
  });

  it('should return user by id', async () => {
    const mockUser = { id: '1', email: 'test@example.com', name: 'Test' };
    mockCtx.prisma.user.findUnique.mockResolvedValue(mockUser);

    const caller = createCaller(mockCtx);
    const result = await caller.getById({ id: '1' });

    expect(result).toEqual(mockUser);
  });

  it('should reject unauthenticated create', async () => {
    const caller = createCaller(mockCtx); // user is null
    
    await expect(caller.create({ email: 'new@example.com', name: 'New' }))
      .rejects.toThrow('UNAUTHORIZED');
  });
});
```

### Test Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

---

## 8. Deployment (Docker)

→ See **[docker-node]** for full guide

### Multi-Stage Dockerfile

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY tsconfig.json ./
COPY prisma ./prisma/
COPY src ./src/
RUN npx prisma generate
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001 -G nodejs

COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/prisma ./prisma
COPY --from=builder --chown=nodejs:nodejs /app/node_modules/.prisma ./node_modules/.prisma

USER nodejs
EXPOSE 3000

CMD ["sh", "-c", "npx prisma migrate deploy && node dist/index.js"]
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      target: builder
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/myapp
    volumes:
      - ./src:/app/src:delegated
    depends_on:
      postgres:
        condition: service_healthy
    command: npm run dev

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  postgres_data:
```

### Commands

```bash
# Development
docker-compose up              # Start all
docker-compose up --build      # Rebuild
docker-compose down -v         # Stop + reset DB

# Production
docker build -t myapp:latest .
docker run -p 3000:3000 --env-file .env.production myapp:latest
```

---

## 9. Security Checklist

### Authentication

```yaml
✓ Hash passwords with argon2/bcrypt
✓ Use short-lived access tokens (15min)
✓ Store refresh tokens in httpOnly cookies
✓ Validate JWT on every request
✓ Use HTTPS in production
```

### Input Validation

```yaml
✓ Validate ALL inputs with Zod
✓ Use z.coerce for query parameters
✓ Sanitize user-generated content
✓ Limit request body size
```

### Database

```yaml
✓ Use Prisma (prevents SQL injection)
✓ Never expose raw database errors
✓ Use transactions for multi-step operations
✓ Add indexes for frequent queries
```

### Logging

```yaml
✓ Redact sensitive data (passwords, tokens)
✓ Include request IDs for tracing
✓ Don't log PII in production
✓ Use structured JSON logs
```

---

## 10. Error Handling

### tRPC Error Codes

| Code | HTTP | Use Case |
|------|------|----------|
| `BAD_REQUEST` | 400 | Invalid input |
| `UNAUTHORIZED` | 401 | No/invalid auth |
| `FORBIDDEN` | 403 | No permission |
| `NOT_FOUND` | 404 | Resource missing |
| `CONFLICT` | 409 | Already exists |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected error |

### Error Handling Pattern

```typescript
import { TRPCError } from '@trpc/server';

// In procedures
const user = await ctx.db.user.findUnique({ where: { id } });
if (!user) {
  throw new TRPCError({ code: 'NOT_FOUND', message: 'User not found' });
}

// Global error formatter
const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError: error.cause instanceof z.ZodError 
          ? error.cause.flatten() 
          : null,
      },
    };
  },
});
```

---

## 11. Common Patterns

### Cursor-Based Pagination

```typescript
list: publicProcedure
  .input(z.object({
    limit: z.number().min(1).max(100).default(10),
    cursor: z.string().optional(),
  }))
  .query(async ({ input, ctx }) => {
    const items = await ctx.db.post.findMany({
      take: input.limit + 1,
      cursor: input.cursor ? { id: input.cursor } : undefined,
      orderBy: { createdAt: 'desc' },
    });
    
    let nextCursor: string | undefined;
    if (items.length > input.limit) {
      nextCursor = items.pop()?.id;
    }
    
    return { items, nextCursor };
  }),
```

### Role-Based Authorization

```typescript
const hasRole = (role: string) => middleware(async ({ ctx, next }) => {
  if (ctx.user?.role !== role) {
    throw new TRPCError({ code: 'FORBIDDEN' });
  }
  return next();
});

export const adminProcedure = protectedProcedure.use(hasRole('ADMIN'));
```

### Transactions

```typescript
const result = await ctx.db.$transaction(async (tx) => {
  const sender = await tx.account.update({
    where: { id: senderId },
    data: { balance: { decrement: amount } },
  });
  
  if (sender.balance < 0) throw new Error('Insufficient funds');
  
  await tx.account.update({
    where: { id: receiverId },
    data: { balance: { increment: amount } },
  });
  
  return sender;
});
```

---

## 12. Skill Reference Map

| Task | Primary Skill | When to Use |
|------|---------------|-------------|
| Type-safe API | backend-trpc | Full-stack TypeScript |
| REST endpoints | backend-trpc-openapi | External clients need REST |
| Next.js auth | backend-auth-js | OAuth, sessions in Next.js |
| Express auth | backend-passport-js | JWT APIs, custom auth |
| Database ORM | backend-prisma | Any SQL database |
| Input validation | backend-zod | ALL input validation |
| Structured logging | backend-pino | Production observability |
| Unit testing | backend-vitest | tRPC, Zod, utilities |
| Containerization | docker-node | Deployment, CI/CD |

---

## 13. Quick Start Templates

### Complete tRPC Router

```typescript
// src/server/routers/user.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';
import { TRPCError } from '@trpc/server';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
});

export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input, ctx }) => {
      const user = await ctx.db.user.findUnique({ where: { id: input.id } });
      if (!user) throw new TRPCError({ code: 'NOT_FOUND' });
      return user;
    }),

  list: publicProcedure
    .input(z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.string().optional(),
    }))
    .query(async ({ input, ctx }) => {
      const items = await ctx.db.user.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: 'desc' },
      });
      
      let nextCursor: string | undefined;
      if (items.length > input.limit) nextCursor = items.pop()?.id;
      
      return { items, nextCursor };
    }),

  create: protectedProcedure
    .input(CreateUserSchema)
    .mutation(async ({ input, ctx }) => {
      return ctx.db.user.create({ data: input });
    }),

  update: protectedProcedure
    .input(z.object({
      id: z.string(),
      name: z.string().min(2).optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const { id, ...data } = input;
      return ctx.db.user.update({ where: { id }, data });
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ input, ctx }) => {
      await ctx.db.user.delete({ where: { id: input.id } });
      return { success: true };
    }),
});
```

### Express Server with tRPC

```typescript
// src/index.ts
import express from 'express';
import cors from 'cors';
import { createExpressMiddleware } from '@trpc/server/adapters/express';
import { appRouter } from './server/routers/_app';
import { createContext } from './server/context';
import { logger } from './lib/logger';
import { requestLogger } from './middleware/logging';

const app = express();

app.use(cors());
app.use(express.json());
app.use(requestLogger);

app.get('/health', async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    res.json({ status: 'healthy' });
  } catch {
    res.status(503).json({ status: 'unhealthy' });
  }
});

app.use('/trpc', createExpressMiddleware({
  router: appRouter,
  createContext,
}));

const port = process.env.PORT || 3000;
app.listen(port, () => {
  logger.info({ port }, 'Server started');
});
```

---

## External Resources

- **tRPC:** https://trpc.io/docs
- **Prisma:** https://prisma.io/docs
- **Zod:** https://zod.dev
- **Auth.js:** https://authjs.dev
- **Passport.js:** https://passportjs.org
- **Pino:** https://getpino.io
- **Vitest:** https://vitest.dev
- **Docker:** https://docs.docker.com

For latest API of any library → use context7 skill
