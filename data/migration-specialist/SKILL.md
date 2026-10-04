---
name: migration-specialist
version: "2.0"
trigger: database migration, schema change, zero-downtime, drizzle migrate
description: Database migrations, schema evolution, data transformation, and zero-downtime deployments. Use when creating migrations, evolving database schema, transforming data, or planning deployment strategies.
---

# Migration Specialist

## Migration Patterns

### Safe Schema Changes
```typescript
// 0001_add_user_tier.ts
export async function up(db: Kysely<any>) {
  // Add column as nullable first
  await db.schema
    .alterTable('users')
    .addColumn('tier', 'integer')
    .execute();
  
  // Backfill data
  await db.updateTable('users')
    .set({ tier: 1 })
    .where('tier', 'is', null)
    .execute();
  
  // Make non-nullable
  await db.schema
    .alterTable('users')
    .alterColumn('tier', col => col.setNotNull())
    .execute();
  
  // Add index
  await db.schema
    .createIndex('user_tier_idx')
    .on('users')
    .column('tier')
    .execute();
}

export async function down(db: Kysely<any>) {
  await db.schema
    .alterTable('users')
    .dropColumn('tier')
    .execute();
}
```

### Zero-Downtime Migration
```typescript
// Expand-contract pattern for renaming column
// Phase 1: Expand - add new column
export async function up(db: Kysely<any>) {
  await db.schema
    .alterTable('users')
    .addColumn('email_address', 'varchar(255)')
    .execute();
  
  // Copy data
  await db.execute(sql`
    UPDATE users 
    SET email_address = email 
    WHERE email_address IS NULL
  `);
  
  // Add triggers to keep in sync
  await db.execute(sql`
    CREATE OR REPLACE FUNCTION sync_email()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.email_address = NEW.email;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
  `);
}

// Phase 2: Update app to use new column
// Phase 3: Contract - remove old column
export async function up_final(db: Kysely<any>) {
  await db.schema
    .alterTable('users')
    .dropColumn('email')
    .execute();
  
  await db.execute(sql`DROP FUNCTION sync_email`);
}
```

## Data Transformation

### Batch Processing
```typescript
export async function transformData() {
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;
  
  while (hasMore) {
    const rows = await db
      .selectFrom('legacy_data')
      .selectAll()
      .limit(batchSize)
      .offset(offset)
      .execute();
    
    if (rows.length === 0) {
      hasMore = false;
      continue;
    }
    
    const transformed = rows.map(transformRow);
    
    await db.transaction().execute(async trx => {
      for (const row of transformed) {
        await trx
          .insertInto('new_data')
          .values(row)
          .execute();
      }
    });
    
    offset += batchSize;
    console.log(`Processed ${offset} rows`);
  }
}
```

### Migration Testing
```typescript
describe('Migration 0001', () => {
  beforeAll(async () => {
    await migrate.downTo('0000');
  });
  
  it('adds tier column', async () => {
    await migrate.upTo('0001');
    
    const result = await db
      .insertInto('users')
      .values({ email: 'test@test.com', tier: 2 })
      .returningAll()
      .executeTakeFirst();
    
    expect(result.tier).toBe(2);
  });
  
  it('is reversible', async () => {
    await migrate.upTo('0001');
    await migrate.downTo('0000');
    
    const columns = await db.execute(sql`
      SELECT column_name 
      FROM information_schema.columns 
      WHERE table_name = 'users' AND column_name = 'tier'
    `);
    
    expect(columns.rows).toHaveLength(0);
  });
});
```

## Deployment Strategies

### Blue-Green Deployment
```typescript
export class BlueGreenDeployer {
  async deploy(newVersion: string) {
    // Deploy to green environment
    await this.deployTo('green', newVersion);
    
    // Run migrations on green
    await this.runMigrations('green');
    
    // Health check
    const healthy = await this.healthCheck('green');
    if (!healthy) {
      throw new Error('Green deployment unhealthy');
    }
    
    // Switch traffic
    await this.switchTraffic('green');
    
    // Keep blue as rollback option
    await this.waitAndCleanup('blue', '30m');
  }
}
```

### Feature Flags for Schema
```typescript
export async function migrateWithFeatureFlag() {
  // Add new column behind feature flag
  await db.schema
    .alterTable('users')
    .addColumn('new_feature_data', 'jsonb')
    .execute();
  
  // App checks feature flag before using
  if (await featureFlags.isEnabled('new-feature')) {
    // Use new schema
  }
}
```

## Protocol

1. **Assess** — Understand the specific requirement and context
2. **Plan** — Determine the approach based on the guidance above
3. **Execute** — Apply the migration specialist methodology
4. **Verify** — Validate the output against expected standards
5. **Report** — Document results and any issues encountered
