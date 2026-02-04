---
name: api-architecture
description: API 아키텍처 설계 원칙과 패턴을 적용합니다. RESTful API 설계, 버저닝, 응답 표준화, 미들웨어 패턴 구현 시 사용하세요. Next.js App Router 기반 서버리스 아키텍처에 최적화되어 있습니다.
allowed-tools: Read, Glob, Grep
---

# API Architecture Skill

## Instructions

1. Follow REST conventions (resource-centric URLs)
2. Use proper HTTP methods (GET/POST/PATCH/DELETE)
3. Apply security pipeline: Rate Limit → Auth → Validate → Authorize → Execute
4. Return consistent response structures
5. Use cursor-based pagination

## REST URL Patterns

```
GET    /api/projects          → List
POST   /api/projects          → Create
GET    /api/projects/[id]     → Read
PATCH  /api/projects/[id]     → Update
DELETE /api/projects/[id]     → Delete
POST   /api/projects/[id]/like → Action
```

## Response Structure

```typescript
// Success
{ data: [...], nextCursor: "id", hasMore: true }

// Error
{ error: "한국어 메시지", details: { field: "에러" } }
```

## Request Pipeline

```typescript
// 1. Rate Limit → 2. Auth → 3. Validate → 4. Authorize → 5. Execute
```

For complete architecture diagrams, anti-patterns, and caching strategies, see [reference.md](reference.md).
