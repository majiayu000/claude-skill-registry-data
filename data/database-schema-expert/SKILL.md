---
name: database-schema-expert
description: Expert knowledge on Supabase Postgres schema, Drizzle ORM patterns, normalized user tables, relations, query patterns, and migrations. Use this skill when user asks about "database", "schema", "drizzle", "query", "table", "postgres", "supabase", "migration", or database design questions.
allowed-tools: Read, Grep, Glob
---

# Database Schema Expert

You are an expert in the database architecture for this influencer discovery platform. This skill provides comprehensive knowledge about the Postgres schema, Drizzle ORM patterns, normalized user tables, and query optimization.

## When To Use This Skill

This skill activates when users:
- Ask about database tables or schema design
- Need to write Drizzle ORM queries
- Work with user data across normalized tables
- Debug data consistency issues
- Plan database migrations
- Optimize query performance
- Understand table relationships
- Need to query campaigns, jobs, or creators

## Core Knowledge

### Schema Architecture

**Database:** Supabase Postgres
**ORM:** Drizzle ORM
**Schema File:** `/lib/db/schema.ts`

**Key Design Principles:**
1. **Normalized User Tables**: Replaced monolithic `user_profiles` with 5 focused tables
2. **JSONB for Flexibility**: `features`, `searchParams`, `metadata` use JSONB
3. **UUID Primary Keys**: All tables use UUID for distributed system compatibility
4. **Timestamp Tracking**: `createdAt` and `updatedAt` on all tables
5. **Soft Relations**: Foreign keys with cascade deletes where appropriate

### Table Structure

**Core Tables:**

1. **campaigns** - User search campaigns
```typescript
{
  id: uuid (PK)
  userId: text (FK to Clerk ID)
  name: text
  description: text
  searchType: varchar(20) // 'instagram-reels', 'tiktok-keyword', etc.
  status: varchar(20) // 'draft', 'active', 'completed', 'archived'
  createdAt: timestamp
  updatedAt: timestamp
}
```

2. **scraping_jobs** - Background search jobs
```typescript
{
  id: uuid (PK)
  userId: text
  runId: text
  status: varchar(20) // 'pending', 'processing', 'completed', 'error', 'timeout'
  keywords: jsonb
  platform: varchar(50) // 'Instagram', 'TikTok', 'YouTube'
  region: varchar(10) // 'US', 'UK', etc.
  campaignId: uuid (FK to campaigns)
  targetUsername: text
  searchParams: jsonb
  qstashMessageId: text
  processedRuns: integer
  processedResults: integer
  targetResults: integer
  cursor: integer
  progress: numeric
  createdAt: timestamp
  startedAt: timestamp
  completedAt: timestamp
  timeoutAt: timestamp
  updatedAt: timestamp
  error: text
}
```

3. **scraping_results** - Creator results from jobs
```typescript
{
  id: uuid (PK)
  jobId: uuid (FK to scraping_jobs)
  creators: jsonb // Array of creator objects
  createdAt: timestamp
}
```

4. **subscription_plans** - Available plans
```typescript
{
  id: uuid (PK)
  planKey: varchar // 'glow_up', 'viral_surge', 'fame_flex', 'free'
  planName: text
  campaignsLimit: integer // -1 for unlimited
  creatorsLimit: integer // -1 for unlimited
  features: jsonb
  priceMonthly: numeric
  priceYearly: numeric
  stripePriceIdMonthly: text
  stripePriceIdYearly: text
  isActive: boolean
  displayOrder: integer
  createdAt: timestamp
  updatedAt: timestamp
}
```

**Normalized User Tables (5 tables replace user_profiles):**

1. **users** - Core identity
```typescript
{
  id: uuid (PK, internal)
  userId: text (unique, Clerk ID)
  email: text
  fullName: text
  businessName: text
  brandDescription: text
  industry: text
  onboardingStep: varchar(50) // 'pending', 'step-1', 'step-2', 'completed'
  isAdmin: boolean
  createdAt: timestamp
  updatedAt: timestamp
}
```

2. **user_subscriptions** - Trial and subscription state
```typescript
{
  id: uuid (PK)
  userId: uuid (FK to users.id)
  currentPlan: varchar(50)
  intendedPlan: varchar(50)
  subscriptionStatus: varchar(20)
  trialStatus: varchar(20) // 'pending', 'active', 'expired', 'converted'
  trialStartDate: timestamp
  trialEndDate: timestamp
  trialConversionDate: timestamp
  subscriptionCancelDate: timestamp
  subscriptionRenewalDate: timestamp
  billingSyncStatus: varchar(20)
  createdAt: timestamp
  updatedAt: timestamp
}
```

3. **user_billing** - Stripe payment data
```typescript
{
  id: uuid (PK)
  userId: uuid (FK to users.id)
  stripeCustomerId: text (unique)
  stripeSubscriptionId: text
  paymentMethodId: text
  cardLast4: varchar(4)
  cardBrand: varchar(20)
  cardExpMonth: integer
  cardExpYear: integer
  billingAddressCity: text
  billingAddressCountry: varchar(2)
  billingAddressPostalCode: varchar(20)
  createdAt: timestamp
  updatedAt: timestamp
}
```

4. **user_usage** - Plan limits and usage tracking
```typescript
{
  id: uuid (PK)
  userId: uuid (FK to users.id)
  planCampaignsLimit: integer
  planCreatorsLimit: integer
  planFeatures: jsonb
  usageCampaignsCurrent: integer
  usageCreatorsCurrentMonth: integer
  enrichmentsCurrentMonth: integer
  usageResetDate: timestamp
  createdAt: timestamp
  updatedAt: timestamp
}
```

5. **user_system_data** - System metadata
```typescript
{
  id: uuid (PK)
  userId: uuid (FK to users.id)
  signupTimestamp: timestamp
  emailScheduleStatus: jsonb
  lastWebhookEvent: varchar(100)
  lastWebhookTimestamp: timestamp
  createdAt: timestamp
  updatedAt: timestamp
}
```

**System Tables:**

- **events** - Event sourcing for audit trail
- **background_jobs** - Scheduled background tasks
- **system_configurations** - Hot-reloadable config
- **logging_configurations** - Runtime logging control

### Drizzle ORM Patterns

**Database Client:** `/lib/db/index.ts`
```typescript
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client, { schema });
```

**Common Query Patterns:**

**1. Select Single Record:**
```typescript
import { db } from '@/lib/db';
import { users } from '@/lib/db/schema';
import { eq } from 'drizzle-orm';

const user = await db.query.users.findFirst({
  where: eq(users.userId, clerkUserId)
});
```

**2. Select with Relations:**
```typescript
const user = await db.query.users.findFirst({
  where: eq(users.userId, clerkUserId),
  with: {
    subscriptions: true,
    billing: true,
    usage: true,
    systemData: true
  }
});
```

**3. Insert Record:**
```typescript
const [campaign] = await db.insert(campaigns)
  .values({
    userId: clerkUserId,
    name: 'My Campaign',
    searchType: 'instagram-reels',
    status: 'draft'
  })
  .returning();
```

**4. Update Record:**
```typescript
await db.update(scrapingJobs)
  .set({
    status: 'completed',
    completedAt: new Date(),
    processedResults: 1000
  })
  .where(eq(scrapingJobs.id, jobId));
```

**5. Complex Query with Aggregation:**
```typescript
import { count, and, gte } from 'drizzle-orm';

const [result] = await db
  .select({ count: count() })
  .from(campaigns)
  .where(and(
    eq(campaigns.userId, userId),
    gte(campaigns.createdAt, startOfMonth)
  ));
```

**6. Join Query:**
```typescript
const jobsWithResults = await db
  .select()
  .from(scrapingJobs)
  .leftJoin(scrapingResults, eq(scrapingJobs.id, scrapingResults.jobId))
  .where(eq(scrapingJobs.userId, userId));
```

**7. Transaction:**
```typescript
await db.transaction(async (tx) => {
  const [campaign] = await tx.insert(campaigns).values({...}).returning();
  await tx.insert(scrapingJobs).values({
    campaignId: campaign.id,
    ...
  });
});
```

### User Data Query Helpers

**Helper Functions:** `/lib/db/queries/user-queries.ts`

```typescript
// Get full user profile (normalized)
export async function getUserProfile(clerkUserId: string) {
  return await db.query.users.findFirst({
    where: eq(users.userId, clerkUserId),
    with: {
      subscriptions: true,
      billing: true,
      usage: true,
      systemData: true
    }
  });
}

// Update user profile (handles normalization)
export async function updateUserProfile(clerkUserId: string, data: any) {
  // Intelligently updates correct normalized table
  // See implementation for details
}

// Get user by Stripe customer ID
export async function getUserByStripeCustomerId(customerId: string) {
  return await db.query.users.findFirst({
    where: eq(userBilling.stripeCustomerId, customerId),
    with: { /* ... */ }
  });
}
```

### Migration Strategy

**Migration Tool:** Drizzle Kit
**Migration Files:** `/drizzle/` directory

**Create Migration:**
```bash
npx drizzle-kit generate:pg
```

**Run Migration:**
```bash
npx drizzle-kit push:pg
```

**Manual Migration Script:**
```bash
node scripts/run-single-migration.js
```

**Migration Best Practices:**
1. Always generate migration, never edit schema directly in production
2. Test migration on local database first
3. Backup production data before migration
4. Use transactions for multi-step migrations
5. Have rollback plan ready

## Common Patterns

### Pattern 1: Querying Normalized User Data

```typescript
// Good: Use helper function
import { getUserProfile } from '@/lib/db/queries/user-queries';

const profile = await getUserProfile(userId);
// Returns denormalized view of user across all 5 tables

// Access any field:
profile.email // from users
profile.currentPlan // from user_subscriptions
profile.stripeCustomerId // from user_billing
profile.planCampaignsLimit // from user_usage
profile.lastWebhookEvent // from user_system_data
```

**When to use**: Anytime you need user data (most API endpoints)

### Pattern 2: Paginated Results

```typescript
// Good: Server-side pagination
import { desc, asc } from 'drizzle-orm';

const pageSize = 20;
const offset = (page - 1) * pageSize;

const campaigns = await db.query.campaigns.findMany({
  where: eq(campaigns.userId, userId),
  orderBy: [desc(campaigns.createdAt)],
  limit: pageSize,
  offset: offset
});
```

**When to use**: Listing campaigns, jobs, or search results

### Pattern 3: JSONB Query

```typescript
// Good: Query nested JSONB data
import { sql } from 'drizzle-orm';

const jobs = await db.select()
  .from(scrapingJobs)
  .where(sql`${scrapingJobs.keywords}::jsonb @> '["fitness"]'::jsonb`);

// Or check if key exists
const jobs = await db.select()
  .from(scrapingJobs)
  .where(sql`${scrapingJobs.searchParams}::jsonb ? 'targetAudience'`);
```

**When to use**: Searching within JSONB columns

## Anti-Patterns (Avoid These)

### Anti-Pattern 1: N+1 Query Problem

```typescript
// BAD: N+1 queries
const jobs = await db.query.scrapingJobs.findMany({
  where: eq(scrapingJobs.userId, userId)
});

for (const job of jobs) {
  const results = await db.query.scrapingResults.findMany({
    where: eq(scrapingResults.jobId, job.id)
  });
}
```

**Why it's bad**: Makes N additional queries

**Do this instead**:
```typescript
// GOOD: Single query with relation
const jobs = await db.query.scrapingJobs.findMany({
  where: eq(scrapingJobs.userId, userId),
  with: { results: true }
});

// Access results: jobs[0].results
```

### Anti-Pattern 2: Selecting All Columns

```typescript
// BAD: Selecting huge JSONB columns unnecessarily
const jobs = await db.select().from(scrapingJobs);
// Returns all jobs with full searchParams and keywords JSONB
```

**Why it's bad**: Waste of network and memory for large JSONB

**Do this instead**:
```typescript
// GOOD: Select only needed columns
const jobs = await db.select({
  id: scrapingJobs.id,
  status: scrapingJobs.status,
  createdAt: scrapingJobs.createdAt
}).from(scrapingJobs);
```

### Anti-Pattern 3: Direct user_profiles Query

```typescript
// BAD: Querying old monolithic table
const user = await db.query.userProfiles.findFirst({
  where: eq(userProfiles.userId, userId)
});
```

**Why it's bad**: `user_profiles` is deprecated, data is in 5 normalized tables

**Do this instead**:
```typescript
// GOOD: Use normalized query helper
import { getUserProfile } from '@/lib/db/queries/user-queries';
const user = await getUserProfile(userId);
```

## Troubleshooting Guide

### Problem: "relation does not exist" Error

**Symptoms:**
- `error: relation "campaigns" does not exist`
- Query works in dev but fails in production

**Diagnosis:**
1. Check if migrations ran
2. Verify table exists in Supabase dashboard
3. Check connection string points to correct database

**Solution:**
```bash
# Check migration status
node scripts/test-migration-status.js

# Run pending migrations
npx drizzle-kit push:pg

# Verify in Supabase
# Go to Table Editor and check if table exists
```

### Problem: JSONB Query Not Working

**Symptoms:**
- JSONB query returns no results
- Error: `operator does not exist`

**Diagnosis:**
1. Check JSONB syntax (needs `::jsonb` cast)
2. Verify JSONB structure matches query
3. Check for null values

**Solution:**
```typescript
// Correct JSONB query syntax
import { sql } from 'drizzle-orm';

// Contains check (array)
const jobs = await db.select()
  .from(scrapingJobs)
  .where(sql`${scrapingJobs.keywords}::jsonb @> '["fitness"]'::jsonb`);

// Key exists check (object)
const jobs = await db.select()
  .from(scrapingJobs)
  .where(sql`${scrapingJobs.searchParams}::jsonb ? 'platform'`);

// Nested value check
const jobs = await db.select()
  .from(scrapingJobs)
  .where(sql`${scrapingJobs.searchParams}::jsonb->>'platform' = 'instagram'`);
```

### Problem: Slow Queries

**Symptoms:**
- Query takes >1 second
- Timeout errors on large datasets

**Diagnosis:**
1. Check if indexes exist
2. Look for full table scans
3. Verify JSONB queries use GIN indexes

**Solution:**
```sql
-- Add index for common queries
CREATE INDEX idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX idx_scraping_jobs_status ON scraping_jobs(status);
CREATE INDEX idx_scraping_jobs_user_id_created_at ON scraping_jobs(user_id, created_at DESC);

-- GIN index for JSONB
CREATE INDEX idx_scraping_jobs_keywords ON scraping_jobs USING GIN(keywords);
```

Use script:
```bash
node scripts/add-search-indexes.js
```

### Problem: User Data Not Found After Normalization

**Symptoms:**
- `getUserProfile` returns null
- User exists in Clerk but not in database
- Fields like `currentPlan` are null

**Diagnosis:**
1. Check if user row exists in `users` table
2. Verify foreign key relationships
3. Check if Clerk webhook created user

**Solution:**
```bash
# Inspect user state
node scripts/inspect-user-state.js --email user@example.com

# Manually create user if missing
node scripts/test-auto-create-user.js user_xxx
```

## Related Files

- `/lib/db/schema.ts` - Complete schema definition
- `/lib/db/index.ts` - Database client
- `/lib/db/queries/user-queries.ts` - User query helpers
- `/lib/db/queries/list-queries.ts` - List query helpers
- `/lib/db/queries/dashboard-queries.ts` - Dashboard queries
- `/lib/db/migrate.ts` - Migration runner
- `/drizzle/` - Migration files
- `/scripts/update-database-schema.js` - Schema update script
- `/scripts/baseline-drizzle-supabase.js` - Schema baseline

## Testing & Validation

**Test Database Connection:**
```bash
node scripts/test-local-db.js
```

**Inspect Database:**
```bash
node scripts/inspect-db.js
```

**Test Query Performance:**
```bash
node scripts/test-db-performance.js
```

**Expected Results:**
- Connection successful
- All tables exist
- Indexes created
- Queries return in <100ms

## Schema Relationships

```
users (1) ← (1) user_subscriptions
users (1) ← (1) user_billing
users (1) ← (1) user_usage
users (1) ← (1) user_system_data

users (1) ← (N) campaigns
campaigns (1) ← (N) scraping_jobs
scraping_jobs (1) ← (N) scraping_results

users (1) ← (N) creator_lists
creator_lists (1) ← (N) list_items

subscription_plans (1) ← (N) user_subscriptions
```

## Performance Tips

1. **Use Indexes**: Add indexes for frequently queried columns
2. **Limit Results**: Always use `limit` for large datasets
3. **Select Specific Columns**: Don't select entire JSONB when you need one field
4. **Use Relations**: Leverage Drizzle's `with` for joins
5. **Batch Operations**: Use transactions for multiple related inserts
6. **Connection Pooling**: Supabase handles this automatically
7. **JSONB Queries**: Use GIN indexes for JSONB containment queries

## Additional Resources

- [Drizzle ORM Documentation](https://orm.drizzle.team/docs/overview)
- [Postgres JSONB Guide](https://www.postgresql.org/docs/current/datatype-json.html)
- [Supabase Docs](https://supabase.com/docs)
- Internal: `/scripts/analyze-database.js` for schema analysis
