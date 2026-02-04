---
name: minimal-modeling
description: Use when designing database schemas from business requirements, translating vague requirements into concrete SQL definitions, or validating database designs with non-technical stakeholders. Provides a systematic methodology that decouples logical business modeling from physical implementation to reduce cognitive load and ensure business-driven design.
---

# Minimal Modeling Database Design

## Overview

Minimal Modeling is a database design methodology that bridges the gap between vague business requirements and concrete SQL schemas through systematic decoupling of logical and physical concerns.

**Core Principle:** Separate the "what exists" (business logic) from "how to store it" (technical implementation) to reduce cognitive load and enable validation by non-technical stakeholders before writing any SQL.

## When to Use

Use this skill when:

- Translating business requirements ("I need a website for...") into database schemas
- Starting a new project with unclear data requirements
- Validating database design with non-technical stakeholders
- Experiencing analysis paralysis from too many implementation details early
- Need to explain database structure to business users

Do NOT use when:

- Database schema already exists and you're just querying it
- Working with predefined ORM models that can't be changed
- Technical constraints (like existing tables) must drive the design

## The Two-Phase Process

### Phase A: Logical Model (Business Domain)

Focus entirely on business concepts without technical implementation.

### Phase B: Physical Schema (Implementation)

Translate business concepts into tables, columns, and data types.

## Phase A: Logical Model

### Step 1: Gather Requirements

Start with informal text or transcript describing the system.

### Step 2: Find Anchors (The "Nouns")

**Definition:** Entities that exist independently with unique IDs. They represent things you count, not data itself.

**Validation:** Use two sentences to test if a noun is an Anchor:

```
Counting Sentence: "We have 1,000 [Nouns] in our database."
Adding Sentence: "The system inserts another [Noun] into the database."
```

If both sentences sound natural, it's an Anchor.

**Examples:**

- ✅ User, Post, Order, Product (you count these)
- ❌ Email, Title, Price (these are data about things)

### Step 3: Find Attributes (The "Data")

**Definition:** Information that describes an Anchor.

**Validation:** Define each attribute with a Human-Readable Question:

```
"What is the [attribute name]?"
"Is this [condition]?"
```

**Examples:**

- User → "What is the email address?" (String)
- Product → "What is the price?" (Decimal)
- Room → "Is this wheelchair accessible?" (Boolean)

**Common Attribute Types:**

- Strings: Names, descriptions, addresses
- Numbers: Counts, IDs, quantities
- Money: Prices, balances (always use DECIMAL, never Float)
- Booleans: Flags, yes/no questions
- Dates/Times: Created dates, scheduled events
- Binary: Files, images (or S3 URLs)

### Step 4: Find Links (The "Relationships")

**Definition:** Connections between two Anchors (or an Anchor to itself).

**Validation:** Use the Two-Sentence Rule to determine cardinality:

```
Sentence 1: "An [Anchor A] [verb] [one/several] [Anchor B]."
Sentence 2: "An [Anchor B] [verb] [one/several] [Anchor A]."
```

**Cardinality Patterns:**

| Sentence Pattern                         | Cardinality        | Implementation              |
| ---------------------------------------- | ------------------ | --------------------------- |
| "A has several B" + "B belongs to one A" | 1:N (One-to-Many)  | Foreign key in B table      |
| "A has one B" + "B belongs to one A"     | 1:1 (One-to-One)   | Foreign key in either table |
| "A has several B" + "B has several A"    | N:M (Many-to-Many) | Junction table              |

**Examples:**

```
User ↔ Order
"A User can place several Orders."
"An Order is placed by one User."
Result: 1:N → Add user_id to orders table

User ↔ Post (likes)
"A User can like several Posts."
"A Post can be liked by several Users."
Result: N:M → Create users_liked_posts junction table
```

### Step 5: Verify Completeness

Go back to original requirements. Highlight every word covered by your model.

**Missing highlights indicate:**

- Missed Anchors
- Missed Attributes
- Missed Links

Continue iterating until all business concepts are captured.

## Phase B: Physical Schema

### Step 6: Choose Table Names

**Convention:** Pluralize the Anchor name

- User → `users`
- Post → `posts`
- Order → `orders`

### Step 7: Choose Column Types

**Critical Type Decisions:**

| Logical Type       | SQL Type                    | Notes                                           |
| ------------------ | --------------------------- | ----------------------------------------------- |
| ID                 | `INTEGER` or `BIGINT`       | Use BIGINT for massive scale (billions of rows) |
| String             | `VARCHAR(N)`                | Default to empty string, not NULL               |
| Money              | `DECIMAL(M,D)`              | NEVER use Float for money                       |
| Boolean            | `BOOLEAN` or `TINYINT`      | Depends on database                             |
| Timestamp (past)   | `TIMESTAMP` in UTC          | Store server events in UTC                      |
| Timestamp (future) | Store local time + timezone | For user-scheduled events                       |
| Binary             | `BLOB` or S3 URL            | Consider external storage for large files       |

**NULL vs Default Values:**

- Prefer meaningful defaults over NULL when possible
- Strings: Default to `''` (empty string)
- Numbers: Consider if `0` makes sense or if NULL is semantic

### Step 8: Implement Links

**One-to-Many (1:N):**
Add foreign key column to the "Many" side table.

```sql
-- User has many Orders
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,  -- Foreign key to users
  total_amount DECIMAL(10,2),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Many-to-Many (N:M):**
Create a junction table with foreign keys to both sides.

```sql
-- Users can like many Posts, Posts can be liked by many Users
CREATE TABLE users_liked_posts (
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, post_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (post_id) REFERENCES posts(id)
);
```

**One-to-One (1:1):**
Add foreign key to either table (choose based on query patterns).

```sql
-- User has one Profile
CREATE TABLE profiles (
  id INTEGER PRIMARY KEY,
  user_id INTEGER UNIQUE NOT NULL,  -- UNIQUE enforces 1:1
  bio TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Quick Reference: Validation Checklist

**Anchors:**

- [ ] Pass counting sentence test
- [ ] Pass adding sentence test
- [ ] Have unique IDs
- [ ] Exist independently

**Attributes:**

- [ ] Have human-readable question
- [ ] Belong to a specific Anchor
- [ ] Are single-valued (not lists)
- [ ] Appropriate SQL type chosen

**Links:**

- [ ] Two-sentence validation complete
- [ ] Cardinality determined (1:1, 1:N, N:M)
- [ ] Implementation strategy chosen
- [ ] Foreign keys properly constrained

**Physical Schema:**

- [ ] Table names pluralized
- [ ] Primary keys defined
- [ ] Foreign keys with constraints
- [ ] Column types match logical types
- [ ] Defaults specified where appropriate
- [ ] Indexes planned for common queries

## Common Mistakes

**Mistake 1: Mixing Logical and Physical Too Early**

```
❌ BAD: "Should User have a VARCHAR(255) email?"
✅ GOOD: "Does User have an email address? [Yes] → Later: VARCHAR(255)"
```

**Mistake 2: Attributes as Anchors**

```
❌ BAD: EmailAddress as an Anchor
✅ GOOD: Email as an Attribute of User
Ask: "We have 1,000 emails in our database?" (sounds weird → not an Anchor)
```

**Mistake 3: Using Float for Money**

```
❌ BAD: price FLOAT
✅ GOOD: price DECIMAL(10,2)
Reason: Float has rounding errors; DECIMAL is exact
```

**Mistake 4: Wrong Cardinality Side**

```
❌ BAD: Adding order_id to users table (1:N wrong side)
✅ GOOD: Adding user_id to orders table (1:N correct side)
Rule: Foreign key goes on the "Many" side
```

**Mistake 5: Missing Junction Tables**

```
❌ BAD: Adding post_ids array column to users (N:M)
✅ GOOD: Create users_liked_posts junction table
Reason: Relational databases don't handle arrays well
```

**Mistake 6: Storing Timezone as String**

```
❌ BAD: "America/New_York" string for all times
✅ GOOD:
  - Past events: UTC timestamp
  - Future events: Local time + timezone
Reason: Different semantic needs
```

## Secondary Data

**Definition:** Data that is duplicated, cached, or aggregated for performance. Not the source of truth.

**Examples:**

- `total_posts` count on User (redundant with COUNT of posts)
- `last_login_at` on User (duplicated from sessions table)

**When to Use:**

- Performance optimization after proving it's needed
- Denormalization for read-heavy workloads

**Always:**

- Document as secondary data
- Have mechanism to rebuild from source of truth
- Consider if query optimization or indexing is better solution

## Working with Query Builders and ORMs

When using query builders like Kysely or ORMs, the process remains the same:

1. **Logical Model first** (Anchors, Attributes, Links)
2. **Define schema types** instead of raw SQL
3. **Generate migrations** from type definitions

```typescript
// After logical modeling, translate to Kysely schema:

// Define database schema interface
interface Database {
  users: UserTable; // Anchor: User
  orders: OrderTable; // Anchor: Order
}

// Anchor: User
interface UserTable {
  id: Generated<number>;
  email: string; // Attribute
  created_at: Generated<Timestamp>;
}

// Anchor: Order
interface OrderTable {
  id: Generated<number>;
  user_id: number; // Link (1:N) - Foreign key to users
  total: string; // Decimal stored as string for precision
  created_at: Generated<Timestamp>;
}

// Create Kysely instance
const db = new Kysely<Database>({
  dialect: new PostgresDialect({ pool }),
});

// Queries respect the logical model:
const userOrders = await db
  .selectFrom('orders')
  .where('user_id', '=', userId) // Following 1:N relationship
  .selectAll()
  .execute();
```

## Time and Timezone Best Practices

**Past Events (already happened):**

```sql
-- Server events, log entries, message timestamps
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Store in UTC
```

**Future Events (scheduled by user):**

```sql
-- Concert times, meeting schedules, alarm times
event_time TIMESTAMP,
event_timezone VARCHAR(50)  -- e.g., "America/New_York"
```

**Reason:** Past events have definite UTC times. Future events need local context because timezone rules may change (DST, political changes).

## Iterative Refinement

Database design is iterative. After creating initial schema:

1. **Test with sample data** - Does it feel natural?
2. **Write common queries** - Are they simple or complex?
3. **Show to stakeholders** - Do they understand the model?
4. **Adjust and repeat** - Refine based on feedback

**Signs you need to revisit:**

- Queries require 5+ JOINs regularly
- Stakeholders confused by table names
- Constant use of NULL checks in queries
- Performance issues with simple queries
- Adding "workaround" columns frequently

## Real-World Impact

**Benefits:**

- Non-technical stakeholders can validate the logical model
- Catch misunderstandings before writing SQL
- Faster iterations (change model, not migrations)
- Clear documentation of business logic
- Reduced cognitive load during design

**When you skip this:**

- Premature optimization (wrong indexes too early)
- Schema doesn't match business needs
- Expensive refactoring later
- Technical debt from implementation-driven design
