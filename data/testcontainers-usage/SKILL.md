---
name: testcontainers-usage
description: Docker-based testing with testcontainers. Use when running tests with real databases.
---

# Testcontainers Usage Skill

This skill covers testcontainers for isolated integration testing with Docker.

## When to Use

Use this skill when:
- Need isolated database per test run
- Testing against real database
- Running CI/CD pipeline tests
- Testing database-specific features

## Core Principle

**REAL DEPENDENCIES** - Test against real databases in containers. No mocking database behavior.

## Installation

```bash
npm install -D @testcontainers/postgresql testcontainers
```

## Basic Setup

```typescript
// tests/setup/containers.ts
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { PrismaClient } from '@prisma/client';
import { execSync } from 'child_process';

let container: StartedPostgreSqlContainer;
let prisma: PrismaClient;

export async function startDatabase(): Promise<{
  container: StartedPostgreSqlContainer;
  prisma: PrismaClient;
  connectionString: string;
}> {
  container = await new PostgreSqlContainer('postgres:16-alpine')
    .withDatabase('testdb')
    .withUsername('test')
    .withPassword('test')
    .start();

  const connectionString = container.getConnectionUri();

  // Set environment variable for Prisma
  process.env.DATABASE_URL = connectionString;

  // Run migrations
  execSync('npx prisma migrate deploy', {
    env: { ...process.env, DATABASE_URL: connectionString },
    stdio: 'inherit',
  });

  // Create Prisma client
  prisma = new PrismaClient({
    datasources: {
      db: { url: connectionString },
    },
  });

  await prisma.$connect();

  return { container, prisma, connectionString };
}

export async function stopDatabase(): Promise<void> {
  if (prisma) {
    await prisma.$disconnect();
  }
  if (container) {
    await container.stop();
  }
}

export function getPrisma(): PrismaClient {
  return prisma;
}
```

## Vitest Configuration

```typescript
// vitest.container.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['**/*.container.test.ts'],
    testTimeout: 120000,
    hookTimeout: 60000,
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: true, // Run serially for container tests
      },
    },
    globalSetup: './tests/setup/container-setup.ts',
  },
});
```

## Global Setup

```typescript
// tests/setup/container-setup.ts
import { startDatabase, stopDatabase } from './containers';

export async function setup(): Promise<void> {
  console.log('Starting test database container...');
  await startDatabase();
  console.log('Test database ready');
}

export async function teardown(): Promise<void> {
  console.log('Stopping test database container...');
  await stopDatabase();
  console.log('Container stopped');
}
```

## Per-Test Container

```typescript
// tests/setup/per-test-container.ts
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { PrismaClient } from '@prisma/client';
import { execSync } from 'child_process';

export async function withDatabase<T>(
  testFn: (prisma: PrismaClient) => Promise<T>
): Promise<T> {
  const container = await new PostgreSqlContainer('postgres:16-alpine')
    .withDatabase('testdb')
    .withUsername('test')
    .withPassword('test')
    .start();

  const connectionString = container.getConnectionUri();

  // Run migrations
  execSync('npx prisma migrate deploy', {
    env: { ...process.env, DATABASE_URL: connectionString },
    stdio: 'pipe',
  });

  const prisma = new PrismaClient({
    datasources: { db: { url: connectionString } },
  });

  try {
    await prisma.$connect();
    return await testFn(prisma);
  } finally {
    await prisma.$disconnect();
    await container.stop();
  }
}
```

## Integration Test Example

```typescript
// src/services/__tests__/user.container.test.ts
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import { PrismaClient } from '@prisma/client';
import { startDatabase, stopDatabase, getPrisma } from '../../../tests/setup/containers';
import { UserService } from '../user';

describe('UserService with testcontainers', () => {
  let prisma: PrismaClient;
  let userService: UserService;

  beforeAll(async () => {
    const db = await startDatabase();
    prisma = db.prisma;
    userService = new UserService(prisma);
  }, 120000); // 2 minute timeout for container startup

  afterAll(async () => {
    await stopDatabase();
  });

  beforeEach(async () => {
    // Clean up between tests
    await prisma.user.deleteMany();
  });

  it('creates a user', async () => {
    const user = await userService.create({
      email: 'test@example.com',
      name: 'Test User',
      password: 'password123',
    });

    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });

  it('finds user by email', async () => {
    await userService.create({
      email: 'find@example.com',
      name: 'Find Me',
      password: 'password123',
    });

    const found = await userService.findByEmail('find@example.com');

    expect(found).not.toBeNull();
    expect(found?.name).toBe('Find Me');
  });

  it('returns null for non-existent user', async () => {
    const found = await userService.findByEmail('nonexistent@example.com');
    expect(found).toBeNull();
  });

  it('updates user', async () => {
    const user = await userService.create({
      email: 'update@example.com',
      name: 'Original Name',
      password: 'password123',
    });

    const updated = await userService.update(user.id, { name: 'New Name' });

    expect(updated.name).toBe('New Name');
  });

  it('deletes user', async () => {
    const user = await userService.create({
      email: 'delete@example.com',
      name: 'Delete Me',
      password: 'password123',
    });

    await userService.delete(user.id);

    const found = await userService.findById(user.id);
    expect(found).toBeNull();
  });
});
```

## Multiple Containers

```typescript
// tests/setup/multi-containers.ts
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { GenericContainer, StartedTestContainer } from 'testcontainers';

interface TestContainers {
  postgres: StartedPostgreSqlContainer;
  redis: StartedTestContainer;
}

export async function startContainers(): Promise<TestContainers> {
  // Start containers in parallel
  const [postgres, redis] = await Promise.all([
    new PostgreSqlContainer('postgres:16-alpine')
      .withDatabase('testdb')
      .start(),
    new GenericContainer('redis:7-alpine')
      .withExposedPorts(6379)
      .start(),
  ]);

  // Set environment variables
  process.env.DATABASE_URL = postgres.getConnectionUri();
  process.env.REDIS_URL = `redis://${redis.getHost()}:${redis.getMappedPort(6379)}`;

  return { postgres, redis };
}

export async function stopContainers(containers: TestContainers): Promise<void> {
  await Promise.all([
    containers.postgres.stop(),
    containers.redis.stop(),
  ]);
}
```

## Reusable Container

```typescript
// tests/setup/reusable-container.ts
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';

let reusableContainer: StartedPostgreSqlContainer | null = null;

export async function getReusableContainer(): Promise<StartedPostgreSqlContainer> {
  if (!reusableContainer) {
    reusableContainer = await new PostgreSqlContainer('postgres:16-alpine')
      .withReuse()
      .start();
  }
  return reusableContainer;
}

// Note: Reusable containers persist between test runs
// Use for faster local development
// Don't use in CI - start fresh containers there
```

## Test with App

```typescript
// src/routes/__tests__/users.container.test.ts
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import supertest from 'supertest';
import { FastifyInstance } from 'fastify';
import { PrismaClient } from '@prisma/client';
import { buildApp } from '../../app';
import { startDatabase, stopDatabase } from '../../../tests/setup/containers';

describe('Users API with real database', () => {
  let app: FastifyInstance;
  let prisma: PrismaClient;

  beforeAll(async () => {
    const db = await startDatabase();
    prisma = db.prisma;
    app = await buildApp();
    await app.ready();
  }, 120000);

  afterAll(async () => {
    await app.close();
    await stopDatabase();
  });

  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  it('creates and retrieves user', async () => {
    // Create
    const createResponse = await supertest(app.server)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
        password: 'Password123!',
      })
      .expect(201);

    const userId = createResponse.body.id;

    // Retrieve
    const getResponse = await supertest(app.server)
      .get(`/api/users/${userId}`)
      .expect(200);

    expect(getResponse.body.email).toBe('test@example.com');
  });
});
```

## CI Configuration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  container-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - run: npm ci

      - name: Run container tests
        run: npm run test:containers
```

## Best Practices

1. **Single fork mode** - Run container tests serially
2. **Adequate timeouts** - Container startup takes time
3. **Clean between tests** - Delete data, not container
4. **Reuse for dev** - Speed up local development
5. **Fresh for CI** - Always start new in CI
6. **Parallel containers** - Start multiple services together

## Notes

- Requires Docker to be running
- First run downloads images (slow)
- Reusable containers speed up local dev
- Container logs available for debugging
