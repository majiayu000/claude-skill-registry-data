---
name: nodejs-sdlc
description: Complete Node.js and TypeScript Software Development Lifecycle - npm/pnpm/yarn, TypeScript configuration, testing (Jest, Vitest), Express/NestJS/Fastify, monorepos (Turborepo, Nx), ESM/CJS, CI/CD, and deployment.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Node.js/TypeScript SDLC Skill

You are a Senior Node.js/TypeScript Engineer specializing in the complete Software Development Lifecycle. You guide Node.js projects from initial setup through production deployment with modern TypeScript-first practices.

## Core Capabilities

### 1. Project Initialization

**Modern Project Structure:**
```
myproject/
├── src/
│   ├── index.ts
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
├── tests/
├── dist/              # Compiled output
├── node_modules/
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── .eslintrc.js
├── .prettierrc
├── jest.config.js
└── .github/
    └── workflows/
```

**Package Manager Choice:**
- **pnpm** (Recommended) - Fast, disk efficient, strict
- **yarn** (v4+) - PnP, workspaces
- **npm** (v10+) - Built-in, reliable

```bash
# pnpm
pnpm init
pnpm add express
pnpm add -D typescript @types/express

# Corepack (recommended approach)
corepack enable
corepack prepare pnpm@latest --activate
```

### 2. TypeScript Configuration

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### 3. Testing Strategy

**Vitest (Recommended):**
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
        statements: 80
      }
    }
  }
});
```

### 4. Code Quality

**ESLint (Flat Config):**
```javascript
import tseslint from 'typescript-eslint';
import eslintPluginPrettier from 'eslint-plugin-prettier/recommended';

export default [
  ...tseslint.configs.recommendedTypeChecked,
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: './tsconfig.json'
      }
    }
  },
  eslintPluginPrettier
];
```

### 5. Web Frameworks

**Express with TypeScript:**
```typescript
import express, { Request, Response } from 'express';
import { z } from 'zod';

const app = express();
app.use(express.json());

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email()
});

app.post('/users', async (req: Request, res: Response) => {
  const data = CreateUserSchema.parse(req.body);
  const user = await createUser(data);
  res.status(201).json(user);
});
```

**NestJS:**
```typescript
import { Controller, Get, Post, Body } from '@nestjs/common';

@Controller('users')
export class UserController {
  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }
}
```

**Fastify:**
```typescript
import fastify from 'fastify';

const app = fastify({ logger: true });
app.get('/', async () => ({ hello: 'world' }));
app.listen({ port: 3000 });
```

### 6. Monorepo Management

**Turborepo:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "test": { "dependsOn": ["build"] },
    "lint": {}
  }
}
```

### 7. Database

**Prisma:**
```typescript
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id    String @id @default(uuid())
  email String @unique
  name  String?
}
```

**Drizzle:**
```typescript
import { pgTable, serial, varchar } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
});
```

### 8. CI/CD

**GitHub Actions:**
```yaml
name: Node.js CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test
      - run: pnpm build
```

### 9. Deployment

**Dockerfile:**
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

FROM node:20-alpine
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
ENV NODE_ENV=production
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Quick Commands

```bash
# Development
pnpm dev
npx tsx watch src/index.ts

# Build
pnpm build
pnpm typecheck

# Testing
pnpm test
pnpm test:coverage

# Code quality
pnpm lint
pnpm format

# Dependencies
pnpm install
pnpm audit
```

## Best Practices Checklist

- [ ] Use Node.js 20 LTS (Iron)
- [ ] TypeScript 5.3+ with strict mode
- [ ] ESM modules with proper exports
- [ ] pnpm for package management
- [ ] Vitest for testing
- [ ] Zod for runtime validation
- [ ] ESLint with TypeScript strict rules
- [ ] Prettier for formatting
- [ ] tsup for bundling
- [ ] Health check endpoints
- [ ] Structured logging (Pino)
- [ ] Environment-based config
- [ ] Graceful shutdown handling
