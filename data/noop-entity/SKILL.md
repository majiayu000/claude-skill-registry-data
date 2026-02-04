---
name: noop-entity
description: Generate new domain entities with full CRUD infrastructure in noop-based projects. Use when adding new resources, tables, or API endpoints to an existing project.
---

# Noop Entity Generator

This skill generates complete CRUD infrastructure for new domain entities.

## When Claude Should Use This

Automatically use this skill when the user wants to:
- Add a new resource/entity to their API
- Create a new database table with CRUD operations
- Add new API endpoints following noop patterns
- Mentions "add entity", "new model", "new resource"

## Framework Context

### Generator Instructions (TEMPLATES)
@docs/universal-framework/GENERATOR_INSTRUCTIONS.md

### Coding Conventions (NAMING)
@docs/universal-framework/CONVENTIONS.md

### Architecture Specification (PATTERNS)
@docs/universal-framework/ARCHITECTURE_SPEC.md

---

## Files Generated

For entity `Product`:

| File | Purpose |
|------|---------|
| `src/types/product.types.ts` | Type definitions |
| `src/db/pg/ProductOps.ts` | Database operations |
| `src/handlers/productHandler.ts` | HTTP handlers |
| Migration SQL | Table creation |

## Files Updated

| File | Changes |
|------|---------|
| `src/db/pg/PgClientStore.ts` | Register ProductOps |
| `src/routes.ts` | Add CRUD routes |
| `src/types/index.ts` | Export types |

## Naming Conventions

| Input | Output | Example |
|-------|--------|---------|
| Entity | PascalCase | `Product` |
| Type file | `{entity}.types.ts` | `product.types.ts` |
| Ops file | `{Entity}Ops.ts` | `ProductOps.ts` |
| Handler | `{entity}Handler.ts` | `productHandler.ts` |
| Table | snake_case plural | `products` |
| Routes | lowercase plural | `/api/v1/products` |
| Store prop | camelCase plural | `dbStore.products` |

## Templates

### Types
```typescript
export interface ProductInfo {
  id: string
  name: string
  description?: string
  organizationId: string
  createdAt: Date
  updatedAt: Date
}

export type CreateProductInput = Omit<ProductInfo, 'id' | 'organizationId' | 'createdAt' | 'updatedAt'>
```

### Ops Class (CRITICAL: organizationId required on ALL methods)
```typescript
export class ProductOps {
  async create(data: CreateProductInput, organizationId: string): Promise<ProductInfo> {
    if (!organizationId) throw new Error('organization_id is required')
    // parameterized INSERT
  }

  async getById(id: string, organizationId: string): Promise<ProductInfo | undefined> {
    if (!organizationId) throw new Error('organization_id is required')
    // SELECT with org filter
  }

  private mapRowToProduct(row: DbProductRow): ProductInfo { }
}
```

### Handler
```typescript
export const create = asyncHandler(async (req, res) => {
  const { name, description } = req.body
  if (!name) throw createError.requiredField('name')

  const dbStore = getDbStore()
  const item = await dbStore.products.create(
    { name, description },
    req.user.organizationId
  )

  return sendSuccess(res, item, 'Product created', 201)
})
```

### Migration SQL
```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  organization_id UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_products_organization ON products(organization_id);
```

### Routes
```typescript
app.get(`${API_PREFIX}/products`, productHandlers.list)
app.post(`${API_PREFIX}/products`, productHandlers.create)
app.get(`${API_PREFIX}/products/:id`, productHandlers.get)
app.put(`${API_PREFIX}/products/:id`, productHandlers.update)
app.delete(`${API_PREFIX}/products/:id`, productHandlers.remove)
```

## Verification

- `npm run typecheck` passes
- `npm run lint` passes
- Types exported from index
- Ops registered in PgClientStore
- Routes registered
