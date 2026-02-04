---
name: database-schema-validator
description: Validates database schemas, Kysely types, and migrations. Use when checking schema correctness or migration safety.
---

# Database Schema Validator Skill

This skill provides database schema validation for Kysely-based projects.
It ensures type safety, migration correctness, and schema best practices.

## Capabilities

### Schema Type Validation

- Verify Kysely schema type definitions
- Check column type consistency
- Validate foreign key relationships
- Ensure proper nullable/required field definitions
- Detect missing or incorrect type mappings

### Migration Analysis

- Validate migration file structure
- Check migration naming conventions
- Verify migration ordering
- Detect unsafe migrations (data loss risks)
- Ensure rollback compatibility

### Best Practices Enforcement

- Check for proper indexing
- Verify primary key definitions
- Validate unique constraints
- Ensure proper use of timestamps
- Check for naming convention compliance

### Consistency Checks

- Compare schema types with actual migrations
- Verify consistency between schema.ts and migration files
- Check for orphaned foreign keys
- Detect schema drift

## Usage Examples

### Validate Schema Type Definitions

```typescript
// Good: Properly typed schema
export interface Database {
  users: {
    id: Generated<string>;
    email: string;
    name: string | null;
    created_at: Generated<string>;
    updated_at: string;
  };
  posts: {
    id: Generated<string>;
    user_id: string;  // Foreign key
    title: string;
    content: string;
    published: Generated<boolean>;
    created_at: Generated<string>;
  };
}

// Bad: Inconsistent or missing types
export interface Database {
  users: {
    id: string;  // ❌ Should use Generated<string>
    email: any;  // ❌ Should have specific type
    // ❌ Missing created_at
  };
}
```

### Migration File Structure

```typescript
// Good: Proper migration structure
import { Kysely, sql } from 'kysely';

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('users')
    .addColumn('id', 'text', (col) => col.primaryKey())
    .addColumn('email', 'text', (col) => col.notNull().unique())
    .addColumn('name', 'text')
    .addColumn('created_at', 'text', (col) =>
      col.notNull().defaultTo(sql`CURRENT_TIMESTAMP`)
    )
    .execute();

  // Create index for frequently queried columns
  await db.schema
    .createIndex('users_email_idx')
    .on('users')
    .column('email')
    .execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('users').execute();
}

// Bad: Missing down migration
export async function up(db: Kysely<any>): Promise<void> {
  // ... migration code
}

// ❌ No down function - can't rollback!
```

### Foreign Key Validation

```typescript
// Good: Proper foreign key with constraints
await db.schema
  .createTable('posts')
  .addColumn('id', 'text', (col) => col.primaryKey())
  .addColumn('user_id', 'text', (col) =>
    col.notNull().references('users.id').onDelete('cascade')
  )
  .execute();

// Bad: No foreign key constraint
await db.schema
  .createTable('posts')
  .addColumn('user_id', 'text')  // ❌ No foreign key reference
  .execute();
```

## Validation Checks

### Schema Type Checks

#### 1. Primary Keys

```typescript
// ✅ Correct
id: Generated<string>;

// ❌ Incorrect (missing Generated)
id: string;
```

#### 2. Timestamps

```typescript
// ✅ Correct (auto-generated)
created_at: Generated<string>;

// ✅ Correct (manually set)
updated_at: string;

// ❌ Incorrect (should be Generated or string)
created_at: Date;
```

#### 3. Nullable Fields

```typescript
// ✅ Correct
name: string | null;

// ❌ Incorrect (TypeScript null vs SQL NULL)
name?: string;  // Optional property, not nullable column
```

#### 4. Foreign Keys

```typescript
// ✅ Correct (matches referenced table's PK type)
users: {
  id: Generated<string>;
};
posts: {
  user_id: string;  // Matches users.id type
};

// ❌ Incorrect (type mismatch)
users: {
  id: Generated<number>;
};
posts: {
  user_id: string;  // ❌ Should be number
};
```

### Migration Safety Checks

**Safe Migrations:**

- Adding new tables
- Adding new columns (with defaults or nullable)
- Adding indexes
- Creating new foreign keys (if data integrity allows)

**Unsafe Migrations (require caution):**

- Dropping tables (data loss)
- Dropping columns (data loss)
- Changing column types (potential data loss)
- Adding NOT NULL constraints (fails if existing NULLs)
- Modifying foreign keys (may fail on existing data)

### Migration Naming Convention

```text
Format: <sequence>_<description>.ts

Good examples:
- 001_initial_schema.ts
- 002_add_user_roles.ts
- 003_add_post_categories.ts

Bad examples:
- migration.ts           // ❌ No sequence number
- 1_users.ts            // ❌ Inconsistent padding
- add-posts.ts          // ❌ No sequence number
- 002_AddPosts.ts       // ❌ PascalCase instead of snake_case
```

## Validation Workflow

### 1. Schema Type Validation

```bash
# Check TypeScript compilation
npx tsc --noEmit

# Verify schema types match database
# (Manual review or custom validation script)
```

### 2. Migration File Validation

Check each migration for:

- Proper naming convention
- Presence of both `up` and `down` functions
- Correct Kysely API usage
- Proper error handling
- Transaction safety

### 3. Schema Consistency Check

```typescript
// Example validation script
import { Database } from './schema';
import { Kysely } from 'kysely';

async function validateSchema(db: Kysely<Database>) {
  // 1. Check if all tables exist
  const tables = await db.introspection.getTables();

  // 2. Verify foreign key references
  for (const table of tables) {
    const foreignKeys = await db.introspection.getTableMetadata(table.name);
    // Validate each FK points to existing table/column
  }

  // 3. Check for orphaned rows
  // Custom queries to detect FK violations
}
```

## Common Issues and Solutions

### Issue: Schema Type Mismatch

**Problem:**

```typescript
// schema.ts
posts: {
  user_id: string;
};

// Migration has:
.addColumn('user_id', 'integer')  // ❌ Type mismatch
```

**Solution:**

```typescript
// Fix migration to match schema
.addColumn('user_id', 'text')  // ✅ Now matches
```

### Issue: Missing Down Migration

**Problem:**

```typescript
export async function up(db: Kysely<any>): Promise<void> {
  await db.schema.createTable('users').execute();
}
// ❌ No down function
```

**Solution:**

```typescript
export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('users').execute();
}
```

### Issue: Unsafe Column Deletion

**Problem:**

```typescript
// Migration that drops column
await db.schema
  .alterTable('users')
  .dropColumn('old_field')
  .execute();
// ❌ Data loss!
```

**Solution:**

```typescript
// 1. First, migrate data to new column
await db
  .updateTable('users')
  .set({ new_field: sql`old_field` })
  .execute();

// 2. Then drop old column in a later migration
// Give users time to rollback if needed
```

### Issue: Missing Foreign Key Constraint

**Problem:**

```typescript
// Schema defines relationship
posts: {
  user_id: string;  // Implies FK to users.id
};

// But migration doesn't enforce it
.addColumn('user_id', 'text')  // ❌ No constraint
```

**Solution:**

```typescript
.addColumn('user_id', 'text', (col) =>
  col.notNull().references('users.id').onDelete('cascade')
)
```

## Best Practices

### Schema Design

#### 1. Use Consistent Naming

- Tables: plural, snake_case (e.g., `user_profiles`)
- Columns: singular, snake_case (e.g., `created_at`)
- Foreign keys: `{table}_id` (e.g., `user_id`)

#### 2. Always Include Timestamps

```typescript
created_at: Generated<string>;
updated_at: string;
```

#### 3. Use Appropriate Types

- IDs: `text` (for UUIDs) or `integer` (for auto-increment)
- Booleans: `boolean` with defaults
- Timestamps: `text` (ISO 8601) or `integer` (Unix timestamp)
- Money: `integer` (cents) to avoid floating point issues

#### 4. Index Frequently Queried Columns

```typescript
// Create index for email lookups
await db.schema
  .createIndex('users_email_idx')
  .on('users')
  .column('email')
  .execute();
```

### Migration Best Practices

#### 1. Make Migrations Atomic

Use transactions when possible:

```typescript
await db.transaction().execute(async (trx) => {
  await trx.schema.createTable('users').execute();
  await trx.schema.createTable('posts').execute();
});
```

#### 2. Test Migrations Both Ways

- Test `up` migration applies successfully
- Test `down` migration rolls back completely
- Verify data integrity after each

#### 3. Version Control

- Always commit schema.ts and migrations together
- Never modify existing migrations that have been applied
- Create new migrations for schema changes

#### 4. Document Complex Migrations

```typescript
/**
 * Migration: Add user_roles table
 *
 * This migration creates a many-to-many relationship between
 * users and roles through the user_roles join table.
 *
 * Rollback: Drops user_roles table and all role assignments.
 */
export async function up(db: Kysely<any>): Promise<void> {
  // ...
}
```

## Output Format

When reporting validation results, use this format:

```markdown
# Database Schema Validation Report

## Summary
- Total Tables: X
- Total Migrations: Y
- Issues Found: Z

## Critical Issues
[Issues that must be fixed immediately]

### Schema Type Mismatch
**Table:** `posts`
**Column:** `user_id`
**Issue:** Schema type `string` doesn't match migration type `integer`
**Fix:**
\`\`\`typescript
// Update migration or schema to match
.addColumn('user_id', 'text')  // Match schema type
\`\`\`

## Warnings
[Issues that should be addressed]

## Recommendations
[Suggestions for improvement]

## Schema Consistency
✅ All foreign keys have proper constraints
✅ All tables have timestamps
✅ All migrations have down functions
⚠️ Missing indexes on frequently queried columns
```

## Validation Checklist

- [ ] All tables defined in schema.ts have corresponding migrations
- [ ] All foreign keys in schema match migration definitions
- [ ] All migrations have both `up` and `down` functions
- [ ] Migration files follow naming convention
- [ ] No `any` types in schema definitions
- [ ] All required fields use `notNull()` in migrations
- [ ] Timestamps use `Generated<string>` for auto-generated fields
- [ ] Foreign keys have proper `onDelete` behavior
- [ ] Frequently queried columns are indexed
- [ ] No unsafe migrations without data migration plan
