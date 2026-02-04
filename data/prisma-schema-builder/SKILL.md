---
name: prisma-schema-builder
description: Generate Prisma schema files with models, relations, enums, and database configuration for TypeScript ORM setup. Triggers on "create Prisma schema", "generate Prisma model", "prisma.schema for", "database schema Prisma".
---

# Prisma Schema Builder

Generate complete Prisma schema files with models, relationships, enums, and proper configuration.

## Output Requirements

**File Output:** `schema.prisma`
**Format:** Prisma Schema Language (PSL)
**Compatibility:** Prisma 5.x

## When Invoked

Immediately generate a complete Prisma schema with appropriate models, relations, and indexes for the domain.

## Schema Structure

```prisma
// Datasource configuration
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Generator configuration
generator client {
  provider = "prisma-client-js"
}

// Models
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
}
```

## Complete Templates

### User Authentication System
```prisma
// schema.prisma

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearch"]
}

// ==========================================
// Enums
// ==========================================

enum UserRole {
  USER
  ADMIN
  MODERATOR
}

enum UserStatus {
  ACTIVE
  INACTIVE
  SUSPENDED
  PENDING_VERIFICATION
}

// ==========================================
// User Management
// ==========================================

model User {
  id            String     @id @default(cuid())
  email         String     @unique
  emailVerified DateTime?  @map("email_verified")
  passwordHash  String?    @map("password_hash")

  // Profile
  firstName     String?    @map("first_name")
  lastName      String?    @map("last_name")
  displayName   String?    @map("display_name")
  avatarUrl     String?    @map("avatar_url")
  bio           String?

  // Account status
  role          UserRole   @default(USER)
  status        UserStatus @default(PENDING_VERIFICATION)

  // Timestamps
  createdAt     DateTime   @default(now()) @map("created_at")
  updatedAt     DateTime   @updatedAt @map("updated_at")
  lastLoginAt   DateTime?  @map("last_login_at")

  // Relations
  sessions      Session[]
  accounts      Account[]
  passwordReset PasswordReset[]

  @@map("users")
}

model Session {
  id           String   @id @default(cuid())
  userId       String   @map("user_id")
  token        String   @unique
  expiresAt    DateTime @map("expires_at")
  ipAddress    String?  @map("ip_address")
  userAgent    String?  @map("user_agent")
  createdAt    DateTime @default(now()) @map("created_at")

  // Relations
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([expiresAt])
  @@map("sessions")
}

model Account {
  id                String  @id @default(cuid())
  userId            String  @map("user_id")
  type              String
  provider          String
  providerAccountId String  @map("provider_account_id")
  refreshToken      String? @map("refresh_token") @db.Text
  accessToken       String? @map("access_token") @db.Text
  expiresAt         Int?    @map("expires_at")
  tokenType         String? @map("token_type")
  scope             String?
  idToken           String? @map("id_token") @db.Text

  // Relations
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
  @@index([userId])
  @@map("accounts")
}

model PasswordReset {
  id        String   @id @default(cuid())
  userId    String   @map("user_id")
  token     String   @unique
  expiresAt DateTime @map("expires_at")
  usedAt    DateTime? @map("used_at")
  createdAt DateTime @default(now()) @map("created_at")

  // Relations
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@map("password_resets")
}

model VerificationToken {
  identifier String
  token      String   @unique
  expiresAt  DateTime @map("expires_at")

  @@unique([identifier, token])
  @@map("verification_tokens")
}
```

### E-commerce Schema
```prisma
// schema.prisma - E-commerce

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

// ==========================================
// Enums
// ==========================================

enum OrderStatus {
  PENDING
  CONFIRMED
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
  REFUNDED
}

enum PaymentStatus {
  PENDING
  COMPLETED
  FAILED
  REFUNDED
}

// ==========================================
// Products
// ==========================================

model Category {
  id          String     @id @default(cuid())
  name        String
  slug        String     @unique
  description String?
  imageUrl    String?    @map("image_url")
  parentId    String?    @map("parent_id")
  sortOrder   Int        @default(0) @map("sort_order")
  isActive    Boolean    @default(true) @map("is_active")
  createdAt   DateTime   @default(now()) @map("created_at")
  updatedAt   DateTime   @updatedAt @map("updated_at")

  // Self-relation for hierarchy
  parent      Category?  @relation("CategoryHierarchy", fields: [parentId], references: [id])
  children    Category[] @relation("CategoryHierarchy")

  // Relations
  products    ProductCategory[]

  @@index([parentId])
  @@index([slug])
  @@map("categories")
}

model Product {
  id             String    @id @default(cuid())
  sku            String    @unique
  name           String
  slug           String    @unique
  description    String?   @db.Text
  price          Decimal   @db.Decimal(10, 2)
  compareAtPrice Decimal?  @map("compare_at_price") @db.Decimal(10, 2)
  cost           Decimal?  @db.Decimal(10, 2)
  quantity       Int       @default(0)
  lowStockAlert  Int       @default(10) @map("low_stock_alert")
  weight         Decimal?  @db.Decimal(8, 3)
  isActive       Boolean   @default(true) @map("is_active")
  isFeatured     Boolean   @default(false) @map("is_featured")
  metadata       Json?
  createdAt      DateTime  @default(now()) @map("created_at")
  updatedAt      DateTime  @updatedAt @map("updated_at")

  // Relations
  categories     ProductCategory[]
  images         ProductImage[]
  variants       ProductVariant[]
  orderItems     OrderItem[]
  cartItems      CartItem[]
  reviews        Review[]

  @@index([sku])
  @@index([slug])
  @@index([isActive, isFeatured])
  @@map("products")
}

model ProductImage {
  id        String   @id @default(cuid())
  productId String   @map("product_id")
  url       String
  altText   String?  @map("alt_text")
  sortOrder Int      @default(0) @map("sort_order")
  isPrimary Boolean  @default(false) @map("is_primary")
  createdAt DateTime @default(now()) @map("created_at")

  // Relations
  product   Product  @relation(fields: [productId], references: [id], onDelete: Cascade)

  @@index([productId])
  @@map("product_images")
}

model ProductVariant {
  id        String   @id @default(cuid())
  productId String   @map("product_id")
  name      String
  sku       String   @unique
  price     Decimal  @db.Decimal(10, 2)
  quantity  Int      @default(0)
  options   Json     // { "color": "red", "size": "M" }
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  // Relations
  product   Product  @relation(fields: [productId], references: [id], onDelete: Cascade)

  @@index([productId])
  @@map("product_variants")
}

model ProductCategory {
  productId  String   @map("product_id")
  categoryId String   @map("category_id")

  product    Product  @relation(fields: [productId], references: [id], onDelete: Cascade)
  category   Category @relation(fields: [categoryId], references: [id], onDelete: Cascade)

  @@id([productId, categoryId])
  @@map("product_categories")
}

// ==========================================
// Customers & Orders
// ==========================================

model Customer {
  id        String    @id @default(cuid())
  email     String    @unique
  firstName String    @map("first_name")
  lastName  String    @map("last_name")
  phone     String?
  createdAt DateTime  @default(now()) @map("created_at")
  updatedAt DateTime  @updatedAt @map("updated_at")

  // Relations
  addresses Address[]
  orders    Order[]
  cart      Cart?
  reviews   Review[]

  @@map("customers")
}

model Address {
  id         String   @id @default(cuid())
  customerId String   @map("customer_id")
  type       String   @default("shipping") // shipping, billing
  firstName  String   @map("first_name")
  lastName   String   @map("last_name")
  line1      String
  line2      String?
  city       String
  state      String?
  postalCode String   @map("postal_code")
  country    String   @db.Char(2) // ISO 3166-1 alpha-2
  phone      String?
  isDefault  Boolean  @default(false) @map("is_default")
  createdAt  DateTime @default(now()) @map("created_at")

  // Relations
  customer   Customer @relation(fields: [customerId], references: [id], onDelete: Cascade)

  @@index([customerId])
  @@map("addresses")
}

model Order {
  id              String        @id @default(cuid())
  orderNumber     String        @unique @map("order_number")
  customerId      String?       @map("customer_id")
  status          OrderStatus   @default(PENDING)
  paymentStatus   PaymentStatus @default(PENDING) @map("payment_status")
  subtotal        Decimal       @db.Decimal(10, 2)
  tax             Decimal       @default(0) @db.Decimal(10, 2)
  shipping        Decimal       @default(0) @db.Decimal(10, 2)
  discount        Decimal       @default(0) @db.Decimal(10, 2)
  total           Decimal       @db.Decimal(10, 2)
  currency        String        @default("USD") @db.Char(3)
  shippingAddress Json?         @map("shipping_address")
  billingAddress  Json?         @map("billing_address")
  notes           String?       @db.Text
  metadata        Json?
  createdAt       DateTime      @default(now()) @map("created_at")
  updatedAt       DateTime      @updatedAt @map("updated_at")

  // Relations
  customer        Customer?     @relation(fields: [customerId], references: [id], onDelete: SetNull)
  items           OrderItem[]

  @@index([customerId])
  @@index([orderNumber])
  @@index([status])
  @@index([createdAt])
  @@map("orders")
}

model OrderItem {
  id        String  @id @default(cuid())
  orderId   String  @map("order_id")
  productId String? @map("product_id")
  sku       String
  name      String
  quantity  Int
  unitPrice Decimal @map("unit_price") @db.Decimal(10, 2)
  total     Decimal @db.Decimal(10, 2)
  metadata  Json?

  // Relations
  order     Order   @relation(fields: [orderId], references: [id], onDelete: Cascade)
  product   Product? @relation(fields: [productId], references: [id], onDelete: SetNull)

  @@index([orderId])
  @@map("order_items")
}

// ==========================================
// Cart
// ==========================================

model Cart {
  id         String     @id @default(cuid())
  customerId String?    @unique @map("customer_id")
  sessionId  String?    @unique @map("session_id")
  expiresAt  DateTime?  @map("expires_at")
  createdAt  DateTime   @default(now()) @map("created_at")
  updatedAt  DateTime   @updatedAt @map("updated_at")

  // Relations
  customer   Customer?  @relation(fields: [customerId], references: [id], onDelete: Cascade)
  items      CartItem[]

  @@map("carts")
}

model CartItem {
  id        String  @id @default(cuid())
  cartId    String  @map("cart_id")
  productId String  @map("product_id")
  quantity  Int

  // Relations
  cart      Cart    @relation(fields: [cartId], references: [id], onDelete: Cascade)
  product   Product @relation(fields: [productId], references: [id], onDelete: Cascade)

  @@unique([cartId, productId])
  @@map("cart_items")
}

// ==========================================
// Reviews
// ==========================================

model Review {
  id         String   @id @default(cuid())
  productId  String   @map("product_id")
  customerId String   @map("customer_id")
  rating     Int      // 1-5
  title      String?
  content    String?  @db.Text
  isVerified Boolean  @default(false) @map("is_verified")
  createdAt  DateTime @default(now()) @map("created_at")
  updatedAt  DateTime @updatedAt @map("updated_at")

  // Relations
  product    Product  @relation(fields: [productId], references: [id], onDelete: Cascade)
  customer   Customer @relation(fields: [customerId], references: [id], onDelete: Cascade)

  @@unique([productId, customerId])
  @@index([productId])
  @@map("reviews")
}
```

## Field Type Reference

### Scalar Types
| Prisma Type | PostgreSQL | MySQL | Description |
|-------------|------------|-------|-------------|
| String | TEXT | VARCHAR(191) | Text |
| Int | INTEGER | INT | Integer |
| BigInt | BIGINT | BIGINT | Large integer |
| Float | DOUBLE PRECISION | DOUBLE | Floating point |
| Decimal | DECIMAL | DECIMAL | Precise decimal |
| Boolean | BOOLEAN | BOOLEAN | True/false |
| DateTime | TIMESTAMP(3) | DATETIME(3) | Date and time |
| Json | JSONB | JSON | JSON data |
| Bytes | BYTEA | LONGBLOB | Binary data |

### Database-Specific Types
```prisma
// PostgreSQL specific
field String @db.VarChar(255)
field String @db.Text
field Decimal @db.Decimal(10, 2)
field String @db.Char(2)

// MySQL specific
field String @db.VarChar(255)
field String @db.LongText
field Int @db.UnsignedInt
```

## Relation Patterns

### One-to-Many
```prisma
model User {
  posts Post[]
}

model Post {
  authorId String
  author   User   @relation(fields: [authorId], references: [id])
}
```

### Many-to-Many (Implicit)
```prisma
model Post {
  tags Tag[]
}

model Tag {
  posts Post[]
}
```

### Many-to-Many (Explicit)
```prisma
model Post {
  categories PostCategory[]
}

model Category {
  posts PostCategory[]
}

model PostCategory {
  postId     String
  categoryId String
  post       Post     @relation(fields: [postId], references: [id])
  category   Category @relation(fields: [categoryId], references: [id])

  @@id([postId, categoryId])
}
```

## Validation Checklist

Before outputting, verify:
- [ ] Datasource configured with env variable
- [ ] Generator block present
- [ ] All relations have inverse defined
- [ ] Foreign keys have `@index`
- [ ] Unique fields have `@unique`
- [ ] `@@map` used for table names (snake_case)
- [ ] `@map` used for column names (snake_case)
- [ ] Cascade deletes appropriate

## Example Invocations

**Prompt:** "Create Prisma schema for a blog with posts, tags, and comments"
**Output:** Complete `schema.prisma` with User, Post, Tag, Comment models.

**Prompt:** "Generate Prisma schema for SaaS multi-tenant app"
**Output:** Complete `schema.prisma` with Organization, User, Membership, Team models.

**Prompt:** "Prisma schema for task management application"
**Output:** Complete `schema.prisma` with Project, Task, User, Comment, Label models.
