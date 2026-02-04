---
name: do-platform-neon
description: Neon serverless PostgreSQL 전문가 - auto-scaling, database branching, PITR, connection pooling 지원. serverless 앱에서 PostgreSQL 필요시 사용
version: 1.0.0
category: platform
tags: [neon, postgresql, serverless, branching, auto-scaling]
context7-libraries: [/neondatabase/neon]
related-skills: [do-platform-supabase, do-lang-typescript]
allowed-tools: Read, Write, Bash, Grep, Glob
---

# do-platform-neon: Neon Serverless PostgreSQL 전문가

## 핵심 역량

Neon Serverless PostgreSQL 전문 지식: auto-scaling, scale-to-zero 컴퓨트, database branching, Point-in-Time Recovery, 최신 ORM 통합을 위한 전문화된 지식 제공

### 주요 기능

- Serverless Compute: auto-scaling PostgreSQL + scale-to-zero로 비용 최적화
- Database Branching: dev, staging, preview 환경용 instant copy-on-write 브랜치
- Point-in-Time Recovery: 30일 PITR로 모든 타임스탬프에 즉시 복원
- Connection Pooling: serverless 및 edge 호환 내장 connection pooler
- PostgreSQL 16: 전체 PostgreSQL 16 호환성 및 extension 지원

### 빠른 의사결정 가이드

- serverless PostgreSQL + auto-scaling 필요? Neon 선택
- CI/CD용 database branching 필요? Neon branching 활용
- edge 호환 데이터베이스 필요? Neon + connection pooling
- instant preview 환경 필요? PR당 Neon branch 생성

### Context7 라이브러리 매핑

Neon: /neondatabase/neon

---

## 구현 가이드

### 설정 및 구성

패키지 설치:
```bash
npm install @neondatabase/serverless
npm install drizzle-orm  # Optional: Drizzle ORM
npm install @prisma/client prisma  # Optional: Prisma ORM
```

환경 변수 설정:
```env
# Direct connection (migrations용)
DATABASE_URL=postgresql://user:pass@ep-xxx.region.neon.tech/dbname?sslmode=require

# Pooled connection (serverless/edge용)
DATABASE_URL_POOLED=postgresql://user:pass@ep-xxx-pooler.region.neon.tech/dbname?sslmode=require

# Neon API (branching용)
NEON_API_KEY=neon_api_key_xxx
NEON_PROJECT_ID=project-xxx
```

### Serverless 드라이버 사용법

기본 쿼리 실행:
```typescript
import { neon } from '@neondatabase/serverless'

const sql = neon(process.env.DATABASE_URL!)

// 간단한 쿼리
const users = await sql`SELECT * FROM users WHERE active = true`

// 파라미터화된 쿼리 (SQL injection 방지)
const userId = 'user-123'
const user = await sql`SELECT * FROM users WHERE id = ${userId}`

// 트랜잭션 지원
const result = await sql.transaction([
  sql`UPDATE accounts SET balance = balance - 100 WHERE id = ${fromId}`,
  sql`UPDATE accounts SET balance = balance + 100 WHERE id = ${toId}`
])
```

세션 지속성을 위한 WebSocket 연결:
```typescript
import { Pool, neonConfig } from '@neondatabase/serverless'
import ws from 'ws'

// Node.js 환경에서 필수
neonConfig.webSocketConstructor = ws

const pool = new Pool({ connectionString: process.env.DATABASE_URL })

// 세션 기반 작업에 pool 사용
const client = await pool.connect()
try {
  await client.query('BEGIN')
  await client.query('INSERT INTO logs (message) VALUES ($1)', ['Action'])
  await client.query('COMMIT')
} finally {
  client.release()
}
```

### Database Branching

Branch 관리 API:
```typescript
class NeonBranchManager {
  private apiKey: string
  private projectId: string
  private baseUrl = 'https://console.neon.tech/api/v2'

  constructor(apiKey: string, projectId: string) {
    this.apiKey = apiKey
    this.projectId = projectId
  }

  private async request(path: string, options: RequestInit = {}) {
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    })
    if (!response.ok) throw new Error(`Neon API error: ${response.statusText}`)
    return response.json()
  }

  async createBranch(name: string, parentId: string = 'main') {
    return this.request(`/projects/${this.projectId}/branches`, {
      method: 'POST',
      body: JSON.stringify({
        branch: { name, parent_id: parentId }
      })
    })
  }

  async deleteBranch(branchId: string) {
    return this.request(`/projects/${this.projectId}/branches/${branchId}`, {
      method: 'DELETE'
    })
  }

  async listBranches() {
    return this.request(`/projects/${this.projectId}/branches`)
  }

  async getBranchConnectionString(branchId: string) {
    const endpoints = await this.request(
      `/projects/${this.projectId}/branches/${branchId}/endpoints`
    )
    return endpoints.endpoints[0]?.connection_uri
  }
}
```

Pull Request용 Preview Branch:
```typescript
async function createPreviewEnvironment(prNumber: number) {
  const branchManager = new NeonBranchManager(
    process.env.NEON_API_KEY!,
    process.env.NEON_PROJECT_ID!
  )

  // main에서 branch 생성
  const branch = await branchManager.createBranch(`pr-${prNumber}`, 'main')

  // connection string 획득
  const connectionString = await branchManager.getBranchConnectionString(branch.branch.id)

  return {
    branchId: branch.branch.id,
    branchName: branch.branch.name,
    connectionString
  }
}

async function cleanupPreviewEnvironment(branchId: string) {
  const branchManager = new NeonBranchManager(
    process.env.NEON_API_KEY!,
    process.env.NEON_PROJECT_ID!
  )
  await branchManager.deleteBranch(branchId)
}
```

### Point-in-Time Recovery

특정 시점으로 복원:
```typescript
async function restoreToPoint(timestamp: Date) {
  const response = await fetch(
    `https://console.neon.tech/api/v2/projects/${process.env.NEON_PROJECT_ID}/branches`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.NEON_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        branch: {
          name: `restore-${timestamp.toISOString().replace(/[:.]/g, '-')}`,
          parent_id: 'main',
          parent_timestamp: timestamp.toISOString()
        }
      })
    }
  )

  return response.json()
}

// 사용 예시: 1시간 전으로 복원
const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000)
const restoredBranch = await restoreToPoint(oneHourAgo)
```

### Drizzle ORM 통합

스키마 정의:
```typescript
// schema.ts
import { pgTable, uuid, text, timestamp, boolean, jsonb } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow(),
  metadata: jsonb('metadata')
})

export const projects = pgTable('projects', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  ownerId: uuid('owner_id').references(() => users.id),
  isPublic: boolean('is_public').default(false),
  createdAt: timestamp('created_at').defaultNow()
})
```

Drizzle 클라이언트 설정:
```typescript
// db.ts
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'
import * as schema from './schema'

const sql = neon(process.env.DATABASE_URL!)
export const db = drizzle(sql, { schema })

// 쿼리 예시
const allUsers = await db.select().from(schema.users)

const userProjects = await db
  .select()
  .from(schema.projects)
  .where(eq(schema.projects.ownerId, userId))
  .orderBy(desc(schema.projects.createdAt))
```

### Prisma ORM 통합

Prisma 스키마:
```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String    @id @default(uuid())
  email     String    @unique
  name      String?
  projects  Project[]
  createdAt DateTime  @default(now())
}

model Project {
  id        String   @id @default(uuid())
  name      String
  owner     User     @relation(fields: [ownerId], references: [id])
  ownerId   String
  isPublic  Boolean  @default(false)
  createdAt DateTime @default(now())
}
```

Prisma + Neon Serverless 드라이버:
```typescript
// db.ts
import { Pool, neonConfig } from '@neondatabase/serverless'
import { PrismaNeon } from '@prisma/adapter-neon'
import { PrismaClient } from '@prisma/client'

neonConfig.webSocketConstructor = require('ws')

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const adapter = new PrismaNeon(pool)
export const prisma = new PrismaClient({ adapter })

// 쿼리 예시
const users = await prisma.user.findMany({
  include: { projects: true }
})
```

---

## 고급 패턴

### Edge용 Connection Pooling

Edge Function 설정:
```typescript
import { neon } from '@neondatabase/serverless'

// edge 환경에서는 pooled connection 사용
const sql = neon(process.env.DATABASE_URL_POOLED!)

export const config = {
  runtime: 'edge'
}

export default async function handler(request: Request) {
  const users = await sql`SELECT id, name FROM users LIMIT 10`
  return Response.json(users)
}
```

### CI/CD Branch 자동화

GitHub Actions 통합:
```yaml
name: Preview Environment

on:
  pull_request:
    types: [opened, synchronize, closed]

jobs:
  create-preview:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest
    steps:
      - name: Create Neon Branch
        id: create-branch
        run: |
          BRANCH=$(curl -s -X POST \
            -H "Authorization: Bearer ${{ secrets.NEON_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"branch":{"name":"pr-${{ github.event.number }}"}}' \
            "https://console.neon.tech/api/v2/projects/${{ secrets.NEON_PROJECT_ID }}/branches")
          echo "branch_id=$(echo $BRANCH | jq -r '.branch.id')" >> $GITHUB_OUTPUT

  cleanup-preview:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - name: Delete Neon Branch
        run: |
          curl -X DELETE \
            -H "Authorization: Bearer ${{ secrets.NEON_API_KEY }}" \
            "https://console.neon.tech/api/v2/projects/${{ secrets.NEON_PROJECT_ID }}/branches/pr-${{ github.event.number }}"
```

### Auto-Scaling 설정

API를 통한 컴퓨트 설정:
```typescript
async function configureAutoScaling(endpointId: string) {
  const response = await fetch(
    `https://console.neon.tech/api/v2/projects/${process.env.NEON_PROJECT_ID}/endpoints/${endpointId}`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${process.env.NEON_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        endpoint: {
          autoscaling_limit_min_cu: 0.25,  // Scale to zero
          autoscaling_limit_max_cu: 4,     // 최대 4 compute units
          suspend_timeout_seconds: 300     // 5분 유휴 후 중단
        }
      })
    }
  )
  return response.json()
}
```

### 마이그레이션 워크플로우

개발에서 프로덕션으로:
```typescript
// direct connection에서 마이그레이션 실행 (pooled 아님)
import { migrate } from 'drizzle-orm/neon-http/migrator'
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'

async function runMigrations() {
  // 마이그레이션에는 direct connection 사용
  const sql = neon(process.env.DATABASE_URL!)
  const db = drizzle(sql)

  await migrate(db, { migrationsFolder: './drizzle' })
  console.log('Migrations completed')
}
```

---

## 프로바이더 선택 가이드

### Neon 사용 권장 상황

- Serverless 애플리케이션: auto-scaling과 scale-to-zero로 비용 절감
- Preview 환경: instant branching으로 PR당 데이터베이스 제공
- Edge 배포: connection pooling이 edge runtime과 호환
- 개발 워크플로우: 프로덕션에서 branch하여 실제 개발 데이터 사용
- 비용 최적화: 활성 컴퓨트 시간에만 비용 발생

### 대안 고려 상황

- Vector Search 필요: pgvector가 있는 Supabase 고려
- Real-time Subscription 필요: Supabase 또는 Convex 고려
- NoSQL 유연성 필요: Firestore 또는 Convex 고려
- 내장 Auth 필요: Supabase 고려

### 가격 참고 (2024)

- Free Tier: 3GB 스토리지, 월 100 compute hours
- Pro Tier: 사용량 기반 가격, 추가 스토리지 및 컴퓨트
- Scale-to-Zero: 유휴 기간 중 비용 미발생

---

## 관련 스킬

- do-platform-supabase: RLS 또는 pgvector 필요시 대안
- do-lang-typescript: Drizzle 및 Prisma용 TypeScript 패턴
- do-domain-backend: 데이터베이스 통합 백엔드 아키텍처

---

Status: Production Ready
Generated with: Do Skill Factory v2.0
Last Updated: 2025-12-07
Technology: Neon Serverless PostgreSQL
