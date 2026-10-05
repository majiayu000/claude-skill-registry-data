---
name: data-model-discovery
description: Comprehensive process for discovering and validating data model requirements before design
languages: [all]
subagents: [architect/data-model]
tools_needed: []
---

## Data Model Discovery Process

Before designing any data model, gather complete requirements through systematic questioning. This prevents redesigns and ensures the model serves actual use cases.

---

## Discovery Questions Framework

### 1. Core Entities & Relationships

**Primary Questions:**
- What are the core entities (nouns) in this domain?
- What relationships exist between these entities?
- Are these relationships one-to-one, one-to-many, or many-to-many?
- Are there any hierarchical relationships (parent-child, categories)?
- Are there any self-referencing relationships (comments replying to comments)?

**Follow-Up Questions:**
- Can an entity exist independently, or does it require a parent?
- Are there any conditional relationships (relationship exists only if...)?
- Do entities have lifecycle dependencies (delete parent → delete children)?

**Example Discovery:**
```
Q: What are the core entities?
A: User, Order, Product, Payment

Q: Relationships between them?
A: 
- User places Orders (1:many)
- Order contains Products (many:many via OrderItem)
- Order has Payment (1:1)

Q: Can an Order exist without a User?
A: No, every Order must belong to a User

Q: If a User is deleted, what happens to their Orders?
A: Orders should be preserved (soft-delete User or keep Orders)
```

**Output:** Entity list + relationship map

---

### 2. Read Patterns (Query Requirements)

**Primary Questions:**
- What are the most common read operations?
- What filters/searches will users perform most often?
- What sorting is required?
- How many records are returned in typical queries?
- Are there any complex aggregations or reports needed?

**Follow-Up Questions:**
- Are there any full-text search requirements?
- Do queries span multiple entities (joins)?
- Are there time-range queries (created in last 30 days)?
- Do queries need pagination?
- Are there any real-time or near-real-time query requirements?

**Example Discovery:**
```
Q: Most common read operations?
A:
1. Get user by email (login) - very frequent
2. List user's orders (paginated) - frequent
3. Get order details with items and payment - frequent
4. Search products by name/category - very frequent
5. Dashboard analytics (total sales, order count) - moderate

Q: Filters needed?
A:
- Orders by status (pending, completed, cancelled)
- Orders by date range
- Products by category
- Products in stock vs out of stock

Q: Sorting requirements?
A:
- Orders by created_at DESC
- Products by price ASC/DESC
- Products by popularity (order count)
```

**Output:** Query patterns list with frequency estimates

---

### 3. Write Patterns (Mutation Requirements)

**Primary Questions:**
- What are the most common write operations?
- What is the expected write volume (inserts/updates per second)?
- Are there batch operations (bulk imports)?
- Are there cascading updates (change A triggers change B)?
- Are writes distributed across entities or concentrated on specific tables?

**Follow-Up Questions:**
- Do writes happen in transactions (multiple tables updated atomically)?
- Are there race conditions to consider (concurrent updates)?
- Do updates need optimistic locking (version checking)?
- Are there any scheduled/background writes (cleanup jobs)?

**Example Discovery:**
```
Q: Most common write operations?
A:
1. Create user (registration) - moderate
2. Create order with items - frequent
3. Update order status - very frequent
4. Create payment record - frequent
5. Update product stock - very frequent

Q: Write volume estimates?
A:
- User creation: ~100/day
- Order creation: ~1000/day
- Order status updates: ~5000/day
- Stock updates: ~2000/day

Q: Transactional requirements?
A:
- Order creation must be atomic (order + order_items + stock decrement)
- Payment processing must be atomic (payment record + order status update)

Q: Concurrency concerns?
A:
- Stock updates can race (need pessimistic locking or atomic decrement)
- Order status updates should not race (use optimistic locking)
```

**Output:** Write patterns list with volume estimates and transaction boundaries

---

### 4. Data Lifecycle & History

**Primary Questions:**
- Are there soft-delete requirements (mark as deleted vs actually delete)?
- Is audit trail needed (who changed what and when)?
- Is versioning required (keep history of changes)?
- How long should data be retained?
- Are there any compliance requirements (GDPR, HIPAA)?

**Follow-Up Questions:**
- Can deleted records be restored?
- Do users need to see change history?
- Are there immutable records (can't be edited after creation)?
- Do records expire after a certain time?

**Example Discovery:**
```
Q: Soft-delete requirements?
A:
- Users: Yes, soft-delete (legal retention requirement)
- Orders: No deletion allowed (audit requirement)
- Products: Soft-delete (may be re-enabled)

Q: Audit trail needed?
A:
- Order status changes: Yes, track who changed and when
- Payment records: Yes, immutable audit trail
- User profile changes: No

Q: Versioning requirements?
A:
- Product price: Yes, keep history of price changes
- Terms of service: Yes, track which version user agreed to

Q: Retention policy?
A:
- Deleted users: 7 years (legal requirement)
- Order data: Indefinite
- Session data: 30 days
```

**Output:** Lifecycle policies per entity

---

### 5. Scale & Performance Constraints

**Primary Questions:**
- How many total records are expected (initial and growth)?
- What is the expected request volume (reads/writes per second)?
- Are there any geographic distribution requirements (multi-region)?
- What are the performance SLAs (query latency, write latency)?
- Are there any peak load scenarios (Black Friday, end of month)?

**Follow-Up Questions:**
- Will data be partitioned/sharded?
- Are there hot records (frequently accessed)?
- Are there cold records (rarely accessed, candidates for archival)?
- Do queries need caching?
- Are there any real-time requirements (< 100ms latency)?

**Example Discovery:**
```
Q: Expected record counts?
A:
- Users: 100K initially, 1M in 2 years
- Orders: 500K initially, 10M in 2 years
- Products: 10K initially, 50K in 2 years
- Order items: 2M initially, 50M in 2 years

Q: Request volume?
A:
- Reads: 1000 req/sec average, 5000 req/sec peak
- Writes: 50 req/sec average, 500 req/sec peak

Q: Performance SLAs?
A:
- Read queries: < 100ms p95
- Write queries: < 200ms p95
- Search: < 500ms p95

Q: Geographic distribution?
A: Single region initially, multi-region in year 2

Q: Peak scenarios?
A: Sales events (3x normal traffic), month-end reporting (heavy analytics)
```

**Output:** Scale estimates and performance targets

---

## Entity Discovery Techniques

### Technique 1: Noun Extraction from Requirements

**Process:**
1. Read requirements document
2. Highlight all nouns
3. Categorize nouns:
   - **Entities:** Core concepts that need persistence (User, Order, Product)
   - **Attributes:** Properties of entities (email, status, price)
   - **Values:** Specific instances (not modeled separately)

**Example:**
> "Users can place orders containing multiple products. Each order has a shipping address and a billing address. Orders can be paid via credit card or PayPal."

**Nouns:**
- User → Entity
- Order → Entity
- Product → Entity
- Shipping address → Attribute (or separate entity if reusable)
- Billing address → Attribute (or separate entity if reusable)
- Credit card → Attribute or Entity (depends on storage needs)
- PayPal → Value (payment method type)

---

### Technique 2: Use Case Walkthrough

**Process:**
1. Walk through each user journey
2. Identify data created, read, updated, deleted at each step
3. Map data to entities

**Example: Checkout Flow**
```
Step 1: User adds items to cart
Data: CART_ITEM (user_id, product_id, quantity)

Step 2: User proceeds to checkout
Data: ORDER (user_id, status='pending')

Step 3: User enters shipping address
Data: ADDRESS (user_id, street, city, state, postal_code)
       ORDER (shipping_address_id)

Step 4: User selects payment method
Data: PAYMENT (order_id, method, status='pending')

Step 5: User confirms order
Data: ORDER_ITEM (order_id, product_id, quantity, price)
       ORDER (status='confirmed')
       PRODUCT (stock_quantity -= ordered_quantity)
```

**Result:** Entities identified + CRUD operations mapped

---

### Technique 3: Event Storming

**Process:**
1. List all domain events ("User Registered", "Order Placed", "Payment Completed")
2. For each event, identify:
   - What entity triggered it?
   - What entities were created/modified?
   - What data is needed for this event?

**Example:**
```
Event: OrderPlaced
Trigger: User clicks "Place Order"
Creates: ORDER, ORDER_ITEM records
Modifies: PRODUCT.stock_quantity
Reads: CART_ITEM, PRODUCT, ADDRESS
Data needed: user_id, product_ids, quantities, shipping_address, billing_address
```

---

## Relationship Discovery Techniques

### Technique 1: Cardinality Questions

For every pair of entities, ask:

**Question Template:**
- How many X can one Y have?
- How many Y can one X have?

**Example:**
```
Q: How many Orders can one User have?
A: Many (1:many)

Q: How many Users can one Order have?
A: One (order belongs to one user)

Result: USER ||--o{ ORDER
```

**Many-to-Many Detection:**
```
Q: How many Categories can one Product have?
A: Many (product can be in Electronics AND Sale)

Q: How many Products can one Category have?
A: Many (category contains many products)

Result: PRODUCT }o--o{ CATEGORY (requires junction table)
```

---

### Technique 2: Dependency Analysis

**Questions:**
- Can entity X exist without entity Y?
- If Y is deleted, what happens to X?

**Example:**
```
Q: Can ORDER exist without USER?
A: No → ORDER depends on USER

Q: If USER is deleted, what happens to ORDER?
A: Orders should persist (soft-delete USER instead)
```

---

## Validation Strategies

### Validation 1: Query Walkthrough

**Process:**
1. Take each identified query pattern
2. Walk through the data model to execute the query
3. Verify all needed data is accessible

**Example:**
```
Query: Get all orders for a user with status 'pending', sorted by date

Walkthrough:
1. Start at USER table
2. Join to ORDER table (via user_id FK)
3. Filter WHERE status = 'pending'
4. Sort by created_at DESC

Validation: ✓ All needed fields exist, FK exists, index on status recommended
```

---

### Validation 2: Normalization Check

**Process:**
1. Review entities for normalization violations
2. Apply normalization rules (typically target 3NF)
3. Denormalize strategically based on query patterns

**Common Violations:**

**1NF Violation (repeating groups):**
❌ Wrong:
```
ORDER {
    uuid id PK
    string product_ids  -- "uuid1,uuid2,uuid3"
}
```

✓ Correct:
```
ORDER_ITEM {
    uuid order_id FK
    uuid product_id FK
}
```

**2NF Violation (partial dependencies):**
❌ Wrong:
```
ORDER_ITEM {
    uuid order_id PK
    uuid product_id PK
    string product_name  -- depends only on product_id
}
```

✓ Correct: Move product_name to PRODUCT table

**3NF Violation (transitive dependencies):**
❌ Wrong:
```
ORDER {
    uuid id PK
    uuid user_id FK
    string user_email  -- depends on user_id, not order_id
}
```

✓ Correct: Remove user_email (derive from USER table)

**Strategic Denormalization:**
When read performance is critical, denormalize:
```
ORDER {
    uuid id PK
    uuid user_id FK
    string user_email  -- denormalized for query performance
}
```

**Document the decision:** "Denormalized user_email to avoid JOIN on every order list query (saves 40ms per request)"

---

### Validation 3: Write Path Testing

**Process:**
1. For each write operation, trace the transaction
2. Identify all tables that need updates
3. Verify foreign key constraints won't block the operation
4. Check for race conditions

**Example:**
```
Operation: Create order

Transaction steps:
1. INSERT INTO orders (user_id, ...) VALUES (...)
2. INSERT INTO order_items (order_id, product_id, quantity, ...) VALUES (...) -- multiple rows
3. UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ? -- for each item

Validation checks:
- FK user_id exists in users table? ✓
- FK product_id exists in products table? ✓
- Stock decrement atomic? ✓ (use UPDATE with WHERE stock_quantity >= ?)
- Rollback if any step fails? ✓ (transaction ensures atomicity)
```

---

### Validation 4: Scalability Analysis

**Process:**
1. Estimate table sizes at 1 year, 3 years, 5 years
2. Identify tables that will grow large
3. Plan indexing, partitioning, archival strategies

**Example:**
```
Table: ORDERS
Current: 10K rows
1 year: 500K rows (50K/month)
3 years: 2M rows
5 years: 4M rows

Analysis:
- Large table, needs indexing on user_id, created_at, status
- Queries often filter by date range → partition by created_at (monthly)
- Old orders (> 2 years) rarely accessed → archive to cold storage
```

---

## Common Discovery Mistakes

### Mistake 1: Jumping to Schema Too Early

❌ **Wrong Process:**
1. User asks for data model
2. Immediately write CREATE TABLE statements

✓ **Correct Process:**
1. Ask discovery questions
2. Document entities and relationships
3. Create ERD
4. Validate against use cases
5. THEN write schema

---

### Mistake 2: Ignoring Query Patterns

**Problem:** Model is correct but performs poorly

**Example:**
```
Entities: USER, ORDER, ORDER_ITEM, PRODUCT

Missing insight: Dashboard shows "total revenue per product"

Impact: Requires complex JOIN across 3 tables + SUM aggregation
→ Slow query (200ms+)

Fix: Add product_revenue summary table (updated on order creation)
```

**Lesson:** Always ask about read patterns before finalizing model

---

### Mistake 3: Under-Specifying Relationships

❌ **Vague:**
"Users and Orders are related"

✓ **Specific:**
"One User can have zero or many Orders. Each Order belongs to exactly one User. If a User is soft-deleted, their Orders remain accessible for audit purposes."

---

### Mistake 4: Forgetting About Data Lifecycle

**Problem:** No plan for deleted data, versioning, or audit trail

**Impact:**
- Can't restore accidentally deleted records
- Can't answer "who changed this and when?"
- Compliance violations (GDPR right to be forgotten)

**Fix:** Always ask about soft-delete, audit, versioning requirements

---

### Mistake 5: Ignoring Scale

**Problem:** Model works fine with 1K records, breaks at 1M records

**Example:**
```
Query: List all users with their order count
SELECT u.*, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id

Works at 10K users, but at 1M users:
- Full table scan (no index on order count)
- Expensive GROUP BY
- 10+ second query time

Fix: Denormalize order_count on users table, update on order creation/deletion
```

**Lesson:** Always ask about expected scale and growth

---

## Discovery Documentation Template

After completing discovery, document findings:

```markdown
## Data Model Discovery Summary

### Entities Identified
1. **USER** - Application user accounts
2. **ORDER** - Customer purchase orders
3. **ORDER_ITEM** - Line items within orders
4. **PRODUCT** - Items available for purchase
5. **PAYMENT** - Payment transactions

### Relationships
- USER ||--o{ ORDER (1:many) - User places orders
- ORDER ||--o{ ORDER_ITEM (1:many) - Order contains items
- PRODUCT ||--o{ ORDER_ITEM (1:many) - Product ordered multiple times
- ORDER ||--|| PAYMENT (1:1) - Order has one payment

### Query Patterns (Frequency: H=High, M=Medium, L=Low)
| Query | Frequency | Notes |
|-------|-----------|-------|
| Get user by email | H | Login, needs index on email |
| List user's orders | H | Dashboard, paginated |
| Get order with items | H | Order detail page, needs JOIN |
| Search products | H | Product listing, full-text search |
| Total revenue by product | M | Analytics, consider summary table |

### Write Patterns (Volume: requests/day)
| Operation | Volume | Notes |
|-----------|--------|-------|
| Create user | 100 | Registration flow |
| Create order | 1000 | Checkout flow, transactional |
| Update order status | 5000 | Workflow transitions |
| Update product stock | 2000 | Inventory management, race condition risk |

### Data Lifecycle
- **Users:** Soft-delete (7-year retention), audit trail not required
- **Orders:** No deletion (immutable audit record), status change history required
- **Products:** Soft-delete (can be re-enabled), price history required

### Scale Estimates
- **Users:** 100K initially → 1M in 2 years
- **Orders:** 500K initially → 10M in 2 years
- **Products:** 10K initially → 50K in 2 years
- **Read volume:** 1000 req/sec avg, 5000 req/sec peak
- **Write volume:** 50 req/sec avg, 500 req/sec peak

### Performance Requirements
- Read latency: < 100ms p95
- Write latency: < 200ms p95
- Search latency: < 500ms p95

### Open Questions
1. Should addresses be separate entity or embedded in orders? (Reusability vs simplicity)
2. Product variants (size, color) - separate entity or JSON column?
3. Multi-currency support needed? (Impacts price storage)
```

---

## Integration with Design Process

**Discovery (this skill) → ERD Creation → Schema Definition**

1. **Discovery Phase:** Ask all questions, document findings
2. **ERD Phase:** Visualize entities and relationships (use mermaid-erd-creation skill)
3. **Schema Phase:** Write SQL DDL or ORM models
4. **Validation Phase:** Review against discovery findings

---

## Summary

**Key Principles:**
1. Ask questions BEFORE designing
2. Understand both read and write patterns
3. Plan for scale from day one
4. Document lifecycle and retention policies
5. Validate model against real use cases
6. Don't jump to schema too early

**Required Outputs:**
- Entity list with descriptions
- Relationship map with cardinality
- Query patterns with frequency
- Write patterns with volume
- Lifecycle policies
- Scale estimates
