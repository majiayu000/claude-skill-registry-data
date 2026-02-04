---
name: planetscale
description: Implements PlanetScale serverless MySQL with branching workflows, non-blocking schema changes, and Prisma integration. Use when building apps with PlanetScale, implementing database branching, or needing serverless MySQL.
---

# PlanetScale

PlanetScale is a serverless MySQL-compatible database built on Vitess, offering database branching, non-blocking schema changes, and horizontal scaling.

## Quick Start

### Create Database

```bash
# Install CLI
brew install planetscale/tap/pscale

# Authenticate
pscale auth login

# Create database
pscale database create my-app --region us-east

# Create branch
pscale branch create my-app feature-users

# Connect to branch
pscale connect my-app feature-users --port 3309
```

### Connection String

```
mysql://username:password@aws.connect.psdb.cloud/database?ssl={"rejectUnauthorized":true}
```

## Prisma Integration

### Setup

```bash
npm install prisma @prisma/client
npm install @prisma/adapter-planetscale  # For serverless
```

### Schema Configuration

```prisma
// prisma/schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]  // For serverless driver
}

datasource db {
  provider     = "mysql"
  url          = env("DATABASE_URL")
  relationMode = "prisma"  // Required if FK constraints disabled
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?  @db.Text
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())

  @@index([authorId])  // Required when using relationMode = "prisma"
}
```

### Push Schema

```bash
# Push schema to branch (not migrate)
npx prisma db push

# Generate client
npx prisma generate
```

### Standard Client Usage

```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// CRUD operations work normally
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe'
  }
})

const users = await prisma.user.findMany({
  include: { posts: true }
})
```

### Serverless Driver (Edge/Serverless)

```typescript
import { PrismaClient } from '@prisma/client'
import { PrismaPlanetScale } from '@prisma/adapter-planetscale'
import { Client } from '@planetscale/database'

// Create PlanetScale client
const client = new Client({
  url: process.env.DATABASE_URL
})

// Create Prisma adapter
const adapter = new PrismaPlanetScale(client)

// Create Prisma client with adapter
const prisma = new PrismaClient({ adapter })

export default prisma
```

## Database Branching

### Branch Workflow

```bash
# Create feature branch from main
pscale branch create my-app add-comments

# Connect and develop
pscale connect my-app add-comments --port 3309

# Make schema changes on branch
npx prisma db push

# Create deploy request (like a PR)
pscale deploy-request create my-app add-comments

# Review diff
pscale deploy-request diff my-app 1

# Deploy to main
pscale deploy-request deploy my-app 1
```

### Branch Types

- **Production branches**: Protected, require deploy requests
- **Development branches**: Can be modified directly
- **Safe migrations enabled**: Get schema reverts and deploy queues

## Non-Blocking Schema Changes

PlanetScale performs schema changes without locking tables:

```sql
-- These are safe to run in production
ALTER TABLE users ADD COLUMN avatar_url VARCHAR(255);
ALTER TABLE posts ADD INDEX idx_created_at (created_at);
```

### Schema Change Best Practices

1. **Add columns as nullable** or with defaults
2. **Add indexes** - always non-blocking
3. **Avoid removing columns** in the same deploy as code changes
4. **Use deploy requests** for production changes

## Direct MySQL Connection

```typescript
import { connect } from '@planetscale/database'

const conn = connect({
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD
})

// Execute query
const results = await conn.execute('SELECT * FROM users WHERE id = ?', [userId])

// Transaction-like batch (not true ACID)
const results = await conn.transaction(async (tx) => {
  await tx.execute('INSERT INTO users (email) VALUES (?)', ['user@example.com'])
  await tx.execute('INSERT INTO profiles (user_id) VALUES (?)', [1])
  return tx.execute('SELECT * FROM users WHERE id = ?', [1])
})
```

## Foreign Key Constraints

### Option 1: Enable FK Constraints (Recommended)

Enable in PlanetScale Dashboard > Settings > Beta features:

```prisma
// Then use normal Prisma schema
datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
  // No relationMode needed
}

model Post {
  id       String @id
  authorId String
  author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
}
```

### Option 2: Prisma Relation Mode

When FK constraints are disabled:

```prisma
datasource db {
  provider     = "mysql"
  url          = env("DATABASE_URL")
  relationMode = "prisma"  // Emulates FKs in Prisma
}

model Post {
  id       String @id
  authorId String
  author   User   @relation(fields: [authorId], references: [id])

  @@index([authorId])  // Must add indexes manually
}
```

## Environment Configuration

```env
# .env
DATABASE_URL="mysql://username:password@aws.connect.psdb.cloud/mydb?sslaccept=strict"

# For serverless driver
DATABASE_HOST="aws.connect.psdb.cloud"
DATABASE_USERNAME="your-username"
DATABASE_PASSWORD="your-password"
```

## Next.js Integration

### API Route

```typescript
// app/api/users/route.ts
import prisma from '@/lib/prisma'
import { NextResponse } from 'next/server'

export async function GET() {
  const users = await prisma.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await prisma.user.create({
    data: {
      email: body.email,
      name: body.name
    }
  })
  return NextResponse.json(user)
}
```

### Server Component

```typescript
// app/users/page.tsx
import prisma from '@/lib/prisma'

export default async function UsersPage() {
  const users = await prisma.user.findMany({
    orderBy: { createdAt: 'desc' }
  })

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

## Connection Pooling

PlanetScale handles connection pooling automatically. For high-traffic apps:

```typescript
// Singleton pattern for Prisma
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query'] : []
})

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}

export default prisma
```

## CLI Commands Reference

```bash
# Database operations
pscale database create <db> --region <region>
pscale database delete <db>
pscale database list

# Branch operations
pscale branch create <db> <branch>
pscale branch delete <db> <branch>
pscale branch list <db>
pscale branch schema <db> <branch>

# Connect for local dev
pscale connect <db> <branch> --port 3309

# Deploy requests
pscale deploy-request create <db> <branch>
pscale deploy-request list <db>
pscale deploy-request diff <db> <number>
pscale deploy-request deploy <db> <number>
pscale deploy-request close <db> <number>

# Password management
pscale password create <db> <branch> <name>
pscale password list <db> <branch>
```

## Monitoring

### Query Insights

View in Dashboard > Insights:
- Slow queries
- Query patterns
- Index recommendations
- Row reads/writes

### Connection Metrics

```typescript
// Log connection stats
const prisma = new PrismaClient({
  log: [
    { level: 'query', emit: 'event' },
    { level: 'error', emit: 'stdout' }
  ]
})

prisma.$on('query', (e) => {
  console.log(`Query: ${e.query}`)
  console.log(`Duration: ${e.duration}ms`)
})
```

## Best Practices

1. **Use branches for all schema changes** - Never modify production directly
2. **Add indexes on foreign key columns** - Required with `relationMode = "prisma"`
3. **Use `db push` not `migrate`** - PlanetScale manages its own migrations
4. **Enable safe migrations** - Get schema reverts and deploy queues
5. **Use serverless driver for edge** - Better cold start times
6. **Enable FK constraints if possible** - Simpler schema management

## References

- [Branching Workflow](references/branching.md)
- [Migration from Other Databases](references/migration.md)
