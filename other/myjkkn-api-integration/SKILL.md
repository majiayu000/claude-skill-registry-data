---
name: myjkkn-api-integration
description: Complete guide for integrating with MyJKKN external API. This skill should be used when creating API routes to fetch data from the MyJKKN platform (jkkn.ai), building API explorer/test pages, or implementing external API integrations following the 5-layer architecture pattern (Types → Services → API Routes → Pages). Automatically triggers when user mentions 'MyJKKN', 'external API', 'API integration', 'fetch from jkkn.ai', or 'API explorer page'.
---

# MyJKKN API Integration Skill

This skill provides comprehensive guidance for integrating with the MyJKKN external API system. Use this as a reference pattern for any external API integration in the JKKN COE application.

## When to Use This Skill

- Creating new API routes that fetch data from external APIs
- Building API explorer or test pages for debugging/testing
- Implementing the 5-layer architecture for external integrations
- Setting up environment configuration for API keys
- Creating service layers for external data fetching

## Architecture Overview

The MyJKKN API integration follows the project's 5-layer architecture:

```
1. Types      → types/myjkkn.ts           (Type definitions)
2. Services   → services/myjkkn-service.ts (Business logic, API calls)
3. Lib        → lib/myjkkn-api.ts          (Re-exports for convenience)
4. API Routes → app/api/myjkkn/*/route.ts  (Next.js API handlers)
5. Pages      → app/(coe)/test-myjkkn-api/ (UI components)
```

## Environment Configuration

### Required Environment Variables

Add to `.env.local`:

```env
# MyJKKN API Configuration
MYJKKN_API_URL=https://www.jkkn.ai/api
MYJKKN_API_KEY=jk_xxxxxxxx_xxxxxxxx
```

### API Key Format
- Format: `jk_<hash>_<suffix>` (e.g., `jk_8d1f70a4d6317109fced563a5626eaa8_miwpchif`)
- Authentication: Bearer token in Authorization header
- Header format: `Authorization: Bearer ${MYJKKN_API_KEY}`

## Implementation Steps

### Step 1: Define Types

Create type definitions in `types/myjkkn.ts`:

```typescript
// Paginated response wrapper
export interface MyJKKNPaginatedResponse<T> {
  data: T[]
  metadata: {
    page: number
    totalPages: number
    total: number
    limit?: number
    returned?: number
  }
}

// Entity interface example
export interface MyJKKNEntity {
  id: string
  name: string
  is_active: boolean
  created_at: string
  updated_at: string
  // Add entity-specific fields
}

// Fetch options interface
export interface MyJKKNEntityFetchOptions {
  page?: number
  limit?: number
  search?: string
  is_active?: boolean
  // Add entity-specific filters
}
```

For complete type definitions, see: [references/types.md](references/types.md)

### Step 2: Create Service Layer

Create service functions in `services/myjkkn-service.ts`:

```typescript
import type { MyJKKNPaginatedResponse, MyJKKNEntity } from '@/types/myjkkn'

// Configuration
function getBaseUrl(): string {
  return process.env.MYJKKN_API_URL || 'https://www.jkkn.ai/api'
}

function getApiKey(): string {
  return process.env.MYJKKN_API_KEY || ''
}

// Error class
export class MyJKKNApiError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.name = 'MyJKKNApiError'
    this.status = status
  }
}

// Core fetch function
async function fetchFromMyJKKN<T>(endpoint: string): Promise<T> {
  const apiKey = getApiKey()
  if (!apiKey) {
    throw new MyJKKNApiError('MYJKKN_API_KEY not configured', 500)
  }

  const response = await fetch(`${getBaseUrl()}${endpoint}`, {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new MyJKKNApiError(error.message || 'API Error', response.status)
  }

  return response.json()
}
```

For complete service implementation, see: [references/service-layer.md](references/service-layer.md)

### Step 3: Create Re-export File

Create `lib/myjkkn-api.ts` for convenient imports:

```typescript
// Re-export types
export type {
  MyJKKNPaginatedResponse,
  MyJKKNEntity,
  MyJKKNEntityFetchOptions,
} from '@/types/myjkkn'

// Re-export service functions
export {
  MyJKKNApiError,
  fetchMyJKKNEntities,
  fetchAllMyJKKNEntities,
} from '@/services/myjkkn-service'
```

### Step 4: Create API Routes

Create Next.js API routes in `app/api/myjkkn/[entity]/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { fetchMyJKKNEntities, MyJKKNApiError } from '@/lib/myjkkn-api'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const page = searchParams.get('page')
    const limit = searchParams.get('limit')
    const search = searchParams.get('search')

    const response = await fetchMyJKKNEntities({
      page: page ? parseInt(page, 10) : 1,
      limit: limit ? parseInt(limit, 10) : 10,
      search: search || undefined,
    })

    return NextResponse.json(response)
  } catch (error) {
    if (error instanceof MyJKKNApiError) {
      return NextResponse.json(
        { error: error.message, status: error.status },
        { status: error.status }
      )
    }
    return NextResponse.json(
      { error: 'Failed to fetch data' },
      { status: 500 }
    )
  }
}
```

For complete API route patterns, see: [references/api-routes.md](references/api-routes.md)

### Step 5: Create Test/Explorer Page

Create a test page in `app/(coe)/test-myjkkn-api/page.tsx`:

Key components:
- Endpoint selector cards
- Dynamic filter inputs
- Data table with pagination
- Collapsible raw JSON response
- API documentation tabs

For complete page implementation, see: [references/explorer-page.md](references/explorer-page.md)

## Available Endpoints

| Entity | Endpoint | API Path |
|--------|----------|----------|
| Institutions | `/api/myjkkn/institutions` | `/api-management/organizations/institutions` |
| Departments | `/api/myjkkn/departments` | `/api-management/organizations/departments` |
| Programs | `/api/myjkkn/programs` | `/api-management/organizations/programs` |
| Degrees | `/api/myjkkn/degrees` | `/api-management/organizations/degrees` |
| Courses | `/api/myjkkn/courses` | `/api-management/organizations/courses` |
| Semesters | `/api/myjkkn/semesters` | `/api-management/organizations/semesters` |
| Students | `/api/myjkkn/students` | `/api-management/students` |
| Staff | `/api/myjkkn/staff` | `/api-management/staff` |

## Common Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | number | Page number (default: 1) |
| `limit` | number | Items per page (default: 10, max: 100) |
| `search` | string | Search by name/code |
| `is_active` | boolean | Filter by active status |
| `institution_id` | UUID | Filter by institution |
| `department_id` | UUID | Filter by department |
| `program_id` | UUID | Filter by program |
| `all` | boolean | Fetch all pages (true/false) |

## Response Format

All endpoints return paginated responses:

```json
{
  "data": [...],
  "metadata": {
    "page": 1,
    "totalPages": 10,
    "total": 100,
    "limit": 10,
    "returned": 10
  }
}
```

## File Structure

```
jkkn_new/
├── .env.local                          # Environment variables
├── types/
│   └── myjkkn.ts                       # Type definitions
├── services/
│   └── myjkkn-service.ts               # Service layer
├── lib/
│   └── myjkkn-api.ts                   # Re-exports
├── app/
│   ├── api/
│   │   └── myjkkn/
│   │       ├── institutions/
│   │       │   └── route.ts            # GET institutions
│   │       ├── departments/
│   │       │   └── route.ts            # GET departments
│   │       ├── programs/
│   │       │   └── route.ts            # GET programs
│   │       ├── degrees/
│   │       │   └── route.ts            # GET degrees
│   │       ├── courses/
│   │       │   └── route.ts            # GET courses
│   │       ├── semesters/
│   │       │   └── route.ts            # GET semesters
│   │       ├── students/
│   │       │   ├── route.ts            # GET students list
│   │       │   └── [id]/
│   │       │       └── route.ts        # GET student by ID
│   │       └── staff/
│   │           ├── route.ts            # GET staff list
│   │           └── [id]/
│   │               └── route.ts        # GET staff by ID
│   └── (coe)/
│       └── test-myjkkn-api/
│           └── page.tsx                # API Explorer page
└── components/
    └── layout/
        └── app-sidebar.tsx             # Navigation (includes API Explorer link)
```

## Best Practices

1. **Environment Variables**: Never hardcode API keys; always use environment variables
2. **Error Handling**: Use custom error classes for consistent error responses
3. **Pagination**: Always support pagination for list endpoints
4. **Type Safety**: Define TypeScript interfaces for all API responses
5. **Service Layer**: Keep API logic in services, not in route handlers
6. **Re-exports**: Use lib files for convenient imports across the codebase
7. **Logging**: Add console logs for debugging (remove in production)

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check MYJKKN_API_KEY is set correctly
2. **500 Internal Error**: Verify MYJKKN_API_URL is correct
3. **Empty Response**: Check query parameters and filters
4. **CORS Errors**: API routes proxy requests server-side, avoiding CORS

### Debug Checklist

- [ ] Environment variables are set in `.env.local`
- [ ] Server restarted after env changes
- [ ] API key format is correct (`jk_xxx_xxx`)
- [ ] Endpoint path matches MyJKKN API documentation
