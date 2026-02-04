---
name: database-best-practices
description: Prisma ORM best practices for Shopify apps including multi-tenant data isolation, query optimization, transaction patterns, and migration strategies. Auto-invoked when working with database operations.
allowed-tools: [Read, Edit, Write, Grep, Glob]
---

# Database Best Practices Skill

## Purpose
Provides best practices and patterns for database operations in Shopify apps using Prisma ORM, focusing on data isolation, query optimization, and safe migrations.

## When This Skill Activates
- Working with Prisma schema or queries
- Creating database migrations
- Optimizing database performance
- Implementing multi-tenant data isolation
- Handling transactions

## Critical: Multi-Tenant Data Isolation

**ALWAYS filter by shopId** - This prevents data leaks between shops.

```typescript
// ✅ CORRECT - Always include shopId
const products = await db.product.findMany({
  where: {
    shopId: shop.id,
    status: "active",
  },
});

// ❌ WRONG - Missing shopId (data leak!)
const products = await db.product.findMany({
  where: { status: "active" },
});
```

## Core Patterns

### 1. Safe Query Pattern

```typescript
// Always filter by shopId for shop-specific data
async function getShopProducts(shopId: string) {
  return db.product.findMany({
    where: { shopId },
    select: {
      id: true,
      title: true,
      vendor: true,
      // Only select needed fields
    },
    take: 50,
    orderBy: { createdAt: "desc" },
  });
}
```

### 2. Pagination Pattern

```typescript
async function getPaginatedProducts(shopId: string, page: number = 1) {
  const pageSize = 50;
  const skip = (page - 1) * pageSize;

  const [products, totalCount] = await Promise.all([
    db.product.findMany({
      where: { shopId },
      skip,
      take: pageSize,
      orderBy: { createdAt: "desc" },
    }),
    db.product.count({
      where: { shopId },
    }),
  ]);

  return {
    products,
    totalCount,
    totalPages: Math.ceil(totalCount / pageSize),
    currentPage: page,
  };
}
```

### 3. Transaction Pattern

```typescript
// Use transactions for operations that must succeed/fail together
await db.$transaction(async (tx) => {
  // Update product
  await tx.product.update({
    where: { id: productId },
    data: { status: "synced" },
  });

  // Create audit log
  await tx.auditLog.create({
    data: {
      shopId: shop.id,
      entityType: "product",
      entityId: productId,
      action: "update",
      changesSummary: "Product synced",
    },
  });
});
```

### 4. Upsert Pattern

```typescript
// Create or update based on existence
await db.product.upsert({
  where: {
    shopId_productId: {
      shopId: shop.id,
      productId: shopifyProductId,
    },
  },
  create: {
    shopId: shop.id,
    productId: shopifyProductId,
    title: "Product Title",
  },
  update: {
    title: "Updated Title",
    updatedAt: new Date(),
  },
});
```

### 5. Bulk Operations

```typescript
// Use createMany for bulk inserts
await db.product.createMany({
  data: products.map(p => ({
    shopId: shop.id,
    productId: p.id,
    title: p.title,
  })),
  skipDuplicates: true, // Skip if unique constraint violated
});

// Use updateMany for bulk updates
await db.product.updateMany({
  where: {
    shopId: shop.id,
    status: "pending",
  },
  data: {
    status: "processed",
    updatedAt: new Date(),
  },
});
```

### 6. JSON Field Handling

```typescript
// Store complex data as JSON
const metadata = { tags: ["summer", "sale"], featured: true };

await db.product.create({
  data: {
    shopId: shop.id,
    title: "Product",
    metadata: JSON.stringify(metadata),
  },
});

// Retrieve and parse JSON
const product = await db.product.findUnique({
  where: { id: productId },
});

const metadata = JSON.parse(product.metadata || "{}");
```

### 7. Error Handling

```typescript
// Handle unique constraint violations
try {
  await db.product.create({
    data: { shopId, productId, title },
  });
} catch (error) {
  if (error.code === "P2002") {
    // Unique constraint violation - update instead
    await db.product.update({
      where: { shopId_productId: { shopId, productId } },
      data: { title, updatedAt: new Date() },
    });
  } else {
    throw error;
  }
}
```

### 8. N+1 Query Prevention

```typescript
// ❌ BAD: N+1 query problem
const products = await db.product.findMany();
for (const product of products) {
  const shop = await db.shop.findUnique({
    where: { id: product.shopId },
  });
  console.log(shop.shopDomain);
}

// ✅ GOOD: Use include
const products = await db.product.findMany({
  include: {
    shop: {
      select: {
        shopDomain: true,
      },
    },
  },
});
```

## Schema Design Patterns

### Multi-Tenant Schema

```prisma
// Base Shop model - required
model Shop {
  id          String   @id @default(cuid())
  shopDomain  String   @unique
  accessToken String
  installedAt DateTime @default(now())

  // All shop-specific data references this
  products Product[]
  orders   Order[]
}

// Shop-specific model
model Product {
  id        String   @id @default(cuid())
  shopId    String
  shop      Shop     @relation(fields: [shopId], references: [id], onDelete: Cascade)
  productId String   // Shopify product ID
  title     String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@unique([shopId, productId])
  @@index([shopId])
}
```

### Common Indexes

```prisma
// Essential indexes for performance
@@index([shopId])                 // Filter by shop
@@index([shopId, status])         // Shop + status filter
@@index([createdAt])              // Time-based queries
@@index([updatedAt])              // Recently updated
@@unique([shopId, externalId])    // Prevent duplicates per shop
```

## Migration Best Practices

### 1. Safe Migrations

```bash
# Development - generates migration
npx prisma migrate dev --name add_vendor_field

# Production - applies migrations
npx prisma migrate deploy
```

### 2. Adding Fields Safely

```prisma
// Step 1: Add as optional
model Product {
  vendor String?  // Optional first
}

// Step 2: Backfill data
// Run a script to populate vendor for existing records

// Step 3: Make required (in next migration)
model Product {
  vendor String  // Required after backfill
}
```

### 3. Data Migration Script

```typescript
// scripts/backfill-vendor.ts
async function backfillVendor() {
  const products = await db.product.findMany({
    where: { vendor: null },
  });

  for (const product of products) {
    await db.product.update({
      where: { id: product.id },
      data: {
        vendor: extractVendorFromTitle(product.title),
      },
    });
  }

  console.log(`Updated ${products.length} products`);
}
```

## Performance Optimization

### 1. Select Only Needed Fields

```typescript
// ❌ Inefficient - fetches all fields
const products = await db.product.findMany();

// ✅ Efficient - only needed fields
const products = await db.product.findMany({
  select: {
    id: true,
    title: true,
    status: true,
  },
});
```

### 2. Use Appropriate Indexes

```prisma
// Index frequently queried fields
@@index([shopId, status])      // Composite index for common query
@@index([createdAt])           // Time-based sorting
@@index([vendor])              // Filtering by vendor
```

### 3. Batch Operations

```typescript
// Process in batches to avoid memory issues
const batchSize = 100;
let skip = 0;

while (true) {
  const batch = await db.product.findMany({
    where: { shopId: shop.id },
    skip,
    take: batchSize,
  });

  if (batch.length === 0) break;

  await processBatch(batch);
  skip += batchSize;
}
```

## Common Prisma Errors

### P2002 - Unique Constraint Violation

```typescript
// Handle gracefully with upsert
await db.product.upsert({
  where: { shopId_productId: { shopId, productId } },
  create: { shopId, productId, title },
  update: { title, updatedAt: new Date() },
});
```

### P2025 - Record Not Found

```typescript
// Check existence first or use try/catch
const product = await db.product.findUnique({
  where: { id: productId },
});

if (!product) {
  throw new Response("Product not found", { status: 404 });
}
```

## Best Practices Checklist

- [ ] Always filter shop-specific queries by shopId
- [ ] Use transactions for multi-step operations
- [ ] Select only needed fields in queries
- [ ] Add indexes for common query patterns
- [ ] Handle unique constraint violations gracefully
- [ ] Use upsert for create-or-update logic
- [ ] Validate JSON data before storing
- [ ] Test migrations in development first
- [ ] Use cascade delete appropriately
- [ ] Monitor query performance

---

**Remember**: Proper database practices prevent data leaks, improve performance, and ensure data integrity.
