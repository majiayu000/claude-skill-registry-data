---
name: connect-to-backend-api
description: Connect frontend to backend API routes. Create service files, handle API calls, error handling, and response transformation.
---

# Connect to Backend API

> **Instructions for integrating frontend with backend API endpoints**

Use this skill when:
- Creating a new service file to call backend APIs
- Connecting a component to an existing API
- Handling API responses and errors
- Transforming data between frontend and backend

---

## Service File Pattern

### File Location
```
src/
└── services/
    ├── [resource]Service.ts     # API call functions
    └── types/
        └── [resource].ts        # TypeScript interfaces
```

### Naming Convention
- Service files: `[resource]Service.ts` (camelCase)
- Type files: `[resource].ts` (camelCase)
- Export named functions (not default exports)

---

## Basic Service File Structure

**File:** `src/services/[resource]Service.ts`

```typescript
import apiClient from './apiClient'
import type {
  [Resource],
  Create[Resource]Payload,
  Update[Resource]Payload,
  [Resource]Response,
  [Resources]Response,
  Delete[Resource]Response,
} from './types/[resource]'

/**
 * Get all resources
 * @param parentId - User ID (property manager)
 * @returns Promise with resources array
 */
export async function get[Resources](
  parentId: string
): Promise<[Resources]Response> {
  return apiClient<[Resources]Response>(`/[resources]?parentId=${parentId}`)
}

/**
 * Get single resource by ID
 * @param id - Resource ID
 * @returns Promise with resource details
 */
export async function get[Resource]ById(
  id: string
): Promise<[Resource]Response> {
  return apiClient<[Resource]Response>(`/[resources]/${id}`)
}

/**
 * Create a new resource
 * @param data - Resource creation payload
 * @returns Promise with created resource
 */
export async function create[Resource](
  data: Create[Resource]Payload
): Promise<[Resource]Response> {
  return apiClient<[Resource]Response, Create[Resource]Payload>('/[resources]', {
    method: 'POST',
    body: data,
  })
}

/**
 * Update an existing resource
 * @param id - Resource ID
 * @param data - Resource update payload
 * @returns Promise with updated resource
 */
export async function update[Resource](
  id: string,
  data: Update[Resource]Payload
): Promise<[Resource]Response> {
  return apiClient<[Resource]Response, Update[Resource]Payload>(
    `/[resources]/${id}`,
    {
      method: 'PUT',
      body: data,
    }
  )
}

/**
 * Delete a resource (soft delete)
 * @param id - Resource ID
 * @returns Promise with success message
 */
export async function delete[Resource](
  id: string
): Promise<Delete[Resource]Response> {
  return apiClient<Delete[Resource]Response>(`/[resources]/${id}`, {
    method: 'DELETE',
  })
}

/**
 * Toggle resource active status
 * @param id - Resource ID
 * @param isActive - New active status
 * @returns Promise with updated resource
 */
export async function toggle[Resource]Status(
  id: string,
  isActive: boolean
): Promise<[Resource]Response> {
  return apiClient<[Resource]Response, { isActive: boolean }>(
    `/[resources]/${id}/status`,
    {
      method: 'PATCH',
      body: { isActive },
    }
  )
}
```

---

## Type Definitions

**File:** `src/services/types/[resource].ts`

```typescript
// Main entity interface
export interface [Resource] {
  id: string
  name: string
  isActive: boolean
  createdAt: string
  updatedAt: string | null
  // ... other fields
}

// Create payload (fields required for creation)
export interface Create[Resource]Payload {
  name: string
  // ... other required fields
}

// Update payload (all fields optional)
export interface Update[Resource]Payload {
  name?: string
  // ... other optional fields
}

// API response wrappers
export interface [Resource]Response {
  status: 'success' | 'failed'
  message?: string
  data: [Resource]
}

export interface [Resources]Response {
  status: 'success' | 'failed'
  message?: string
  data: [Resource][]
}

export interface Delete[Resource]Response {
  status: 'success' | 'failed'
  message: string
}
```

---

## Using the API Client

### The `apiClient` Function

**Location:** `src/services/apiClient.ts` (already exists)

**Signature:**
```typescript
apiClient<ResponseType, BodyType>(
  endpoint: string,
  options?: {
    method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
    body?: BodyType
    headers?: HeadersInit
  }
): Promise<ResponseType>
```

### GET Request (No Body)
```typescript
// Simple GET
const response = await apiClient<ResourceResponse>('/resources/123')

// GET with query params
const response = await apiClient<ResourcesResponse>(
  `/resources?parentId=${userId}&status=active`
)
```

### POST Request (With Body)
```typescript
const response = await apiClient<ResourceResponse, CreateResourcePayload>(
  '/resources',
  {
    method: 'POST',
    body: {
      name: 'New Resource',
      field: 'value'
    }
  }
)
```

### PUT Request (Update)
```typescript
const response = await apiClient<ResourceResponse, UpdateResourcePayload>(
  `/resources/${id}`,
  {
    method: 'PUT',
    body: {
      name: 'Updated Name'
    }
  }
)
```

### DELETE Request
```typescript
const response = await apiClient<DeleteResourceResponse>(
  `/resources/${id}`,
  {
    method: 'DELETE'
  }
)
```

### PATCH Request (Partial Update)
```typescript
const response = await apiClient<ResourceResponse, { isActive: boolean }>(
  `/resources/${id}/status`,
  {
    method: 'PATCH',
    body: { isActive: true }
  }
)
```

---

## Error Handling Pattern

### In Component
```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()

  try {
    const res = await createResource(payload)

    if (res.status === 'success') {
      // Success path
      onAdd(res.data)
      showNotification('Resource created successfully', 'success')
      onClose()
    } else {
      // Backend returned error
      showNotification(res.message || 'Failed to create resource', 'error')
    }
  } catch (err) {
    // Network error or exception
    console.error('Error creating resource:', err)
    const message = err instanceof Error ? err.message : 'Error creating resource'
    showNotification(message, 'error')
  }
}
```

### Error Response Structure

**Backend always returns:**
```json
{
  "status": "failed",
  "message": "Human-readable error message"
}
```

**Frontend should:**
1. Check `res.status === 'success'` or `'failed'`
2. Display `res.message` in notification
3. Catch network errors in `catch` block
4. Always show user-friendly error messages

---

## Authentication Handling

### Current Implementation

**No manual auth headers needed** - The current `apiClient` does NOT send Authorization headers.

**Future Auth Implementation (if needed):**
```typescript
// In apiClient.ts (modify if auth is added later)
const supabase = createClient()
const { data: { session } } = await supabase.auth.getSession()

const config: RequestInit = {
  method,
  headers: {
    'Content-Type': 'application/json',
    ...(session?.access_token && {
      'Authorization': `Bearer ${session.access_token}`
    }),
    ...headers,
  },
}
```

**For now:** Just use `apiClient` as-is. Auth is handled on backend via session cookies.

---

## Data Transformation

### Backend (snake_case) ↔ Frontend (camelCase)

**Good news:** The backend already transforms data to camelCase before sending responses!

**Backend returns:**
```json
{
  "clientId": "uuid",
  "propertyType": "STR",
  "isActive": true,
  "createdAt": "2025-11-04T..."
}
```

**No transformation needed in frontend** - Just use the data as-is.

---

## Query Parameters

### Single Parameter
```typescript
const response = await apiClient<ResourcesResponse>(
  `/resources?parentId=${userId}`
)
```

### Multiple Parameters
```typescript
const params = new URLSearchParams({
  parentId: userId,
  status: 'active',
  limit: '10'
})

const response = await apiClient<ResourcesResponse>(
  `/resources?${params.toString()}`
)
```

### Optional Parameters
```typescript
export async function getResources(
  parentId: string,
  filters?: { status?: string; limit?: number }
): Promise<ResourcesResponse> {
  let url = `/resources?parentId=${parentId}`

  if (filters?.status) {
    url += `&status=${filters.status}`
  }

  if (filters?.limit) {
    url += `&limit=${filters.limit}`
  }

  return apiClient<ResourcesResponse>(url)
}
```

---

## Helper Functions in Services

### Client-Side Calculations
```typescript
/**
 * Calculate resource statistics
 * Client-side calculation for dashboard
 */
export function calculateResourceStats(resources: Resource[]) {
  const total = resources.length
  const active = resources.filter(r => r.isActive).length
  const inactive = total - active

  return { total, active, inactive }
}
```

### Data Formatting
```typescript
/**
 * Format display text for table
 */
export function formatResourceDisplay(resource: Resource): string {
  return `${resource.name} (${resource.status})`
}
```

### Validation Helpers
```typescript
/**
 * Check if resource has specific property
 */
export function hasSpecialFeature(resource: Resource): boolean {
  return resource.featureFlag !== null
}
```

---

## Complete Example: Property Service

See the existing `src/services/propertyService.ts` for a real-world example:

**Key Features:**
- Full CRUD operations (GET, POST, PUT, DELETE, PATCH)
- Helper functions for data calculations
- JSDoc comments for all functions
- Proper TypeScript typing
- Clean error propagation (no try/catch in service layer)

**Pattern to follow:**
1. Import `apiClient` and types
2. Define all CRUD functions
3. Add helper functions for data manipulation
4. Export everything as named exports
5. Add JSDoc comments for documentation

---

## For More Details

- **Service layer patterns:** See `service-patterns.md`
- **Error handling examples:** See `error-handling.md`

---

**Last Updated:** November 4, 2025
