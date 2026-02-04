---
name: payload-migration-workflow
description: Guide for migrating from PHP/MySQL to Payload CMS with PostgreSQL. Use when working on migration tasks, understanding data models, or implementing Payload collections. Covers migration strategy, architecture decisions, and step-by-step tasks for the Y-Not Radio site migration.
---

# Payload CMS Migration Workflow

**Project Goal:** Migrate from homemade PHP/MySQL to Payload CMS with PostgreSQL on Netlify + Neon, then build a modern responsive site redesign.

## Quick Start

When starting a migration task:

1. **Find your task:** See [Migration Tasks](#migration-tasks) or `docs/payload-migration/04-migration-tasks.md`
2. **Check context:** Review [Architecture Decisions](#key-architecture-decisions) below
3. **Verify completion:** Follow success criteria for your collection
4. **Get help:** See [Quick Reference](#quick-reference) for commands and queries

## Why Payload + PostgreSQL

- **Relational continuity**: MySQL → PostgreSQL is simpler than MySQL → NoSQL
- **Direct database access**: PHP can query PostgreSQL directly without learning GraphQL/GROQ
- **Code-first configuration**: Collections defined in TypeScript with full type safety
- **Built-in APIs**: REST + GraphQL without learning GROQ
- **Self-hosted flexibility**: Full control over CMS and deployment

## Key Architecture Decisions

### Database Strategy
- **Single PostgreSQL database** for all data (including votes)
- Neon serverless PostgreSQL for production
- Direct SQL access from PHP using PDO
- ACID transactions for data consistency

### Collection Patterns
1. **Base collections**: People, DJs, Artists, Venues, Media
2. **Content collections**: Concerts, Shows, Posts, Songs, Records
3. **Interactive collections**: Top11, YearEndPolls, ModernRockMadness (with votes)

### Migration Approach
- Two-phase: (1) Migrate data and CMS, (2) Redesign frontend
- Feature flags for gradual cutover
- PHP site continues querying PostgreSQL directly
- Payload Admin UI for content management

## Core Data Models (Priority Order)

| Priority | Collection | Status | Dependencies |
|----------|-----------|--------|--------------|
| 1 | People | 🔲 Todo | None |
| 2 | DJs | 🔲 Todo | People |
| 3 | Artists | 🔲 Todo | People (many-to-many) |
| 4 | Venues | 🔲 Todo | None |
| 5 | Media | 🔲 Todo | Cloudinary integration |
| 6 | Ads | 🔲 Todo | Media |
| 7 | Concerts | 🔲 Todo | Artists, Venues |
| 8 | Songs | 🔲 Todo | Artists |
| 9 | Records | 🔲 Todo | Artists |
| 10 | CdOfTheWeek | 🔲 Todo | Records |
| 11 | OnDemand | 🔲 Todo | Artists, DJs |
| 12 | Shows | 🔲 Todo | DJs |
| 13 | Posts | 🔲 Todo | Media (unified Story + CustomText) |
| 14-23 | Interactive (Top11, YearEnd, MRM) | 🔲 Todo | Various |

**Full details:** `docs/payload-migration/03-core-data-models.md`

## Migration Tasks

### Task 0: Setup Environment ✅ Complete
- Payload Admin UI at http://localhost:3000/admin
- PostgreSQL connection (Neon)
- Netlify deployment configured
- Cloudinary for media uploads

**Details:** `docs/payload-migration/04-migration-tasks.md#task-0`

### Task 1: MySQL to PostgreSQL Schema
Convert MySQL schema to PostgreSQL:
- Data type conversions (DATETIME → TIMESTAMP, TINYINT → BOOLEAN)
- Foreign key constraints
- Indexes for performance
- Soft delete columns (`deleted_at`)

**Details:** `docs/payload-migration/04-migration-tasks.md#task-1`

### Task 2: Data Migration
Export MySQL data and import to PostgreSQL:
- Use `mysqldump` for data export
- Transform data during import
- Validate relationships
- Test with sample queries

**Details:** `docs/payload-migration/04-migration-tasks.md#task-2`

### Task 3+: Collection Implementation
For each collection:
1. Define Payload collection schema in TypeScript
2. Configure fields, relationships, access control
3. Run migrations: `yarn payload migrate`
4. Seed with sample data
5. Test CRUD operations in Admin UI
6. Verify PHP can query via PostgreSQL

**Per-collection checklists:** `docs/payload-migration/07-success-criteria.md`

## PHP PostgreSQL Integration

PHP can query PostgreSQL directly without learning GraphQL:

```php
// Connect to PostgreSQL (same as MySQL but different driver)
$pdo = new PDO(
  "pgsql:host=localhost;port=5432;dbname=ynot_payload_dev",
  "username",
  "password"
);

// Query Payload tables directly
$stmt = $pdo->prepare("
  SELECT c.id, c.date, c.venue_id, v.name as venue_name
  FROM concerts c
  JOIN venues v ON c.venue_id = v.id
  WHERE c.date >= NOW()
  ORDER BY c.date ASC
  LIMIT 10
");
$stmt->execute();
$concerts = $stmt->fetchAll(PDO::FETCH_ASSOC);
```

**Full guide:** `docs/payload-migration/03.5-php-postgresql-querying.md`

## Cloudinary Media Storage

For image uploads:
1. Configure Cloudinary plugin in `payload.config.ts`
2. Set environment variables (`CLOUDINARY_CLOUD_NAME`, etc.)
3. Use Media collection for all uploads
4. Images auto-optimized and delivered via CDN

**Detailed setup:** `docs/payload-migration/12-cloudinary-integration.md`

## Success Criteria Per Collection

Each collection must meet:
- [ ] Payload schema defined in TypeScript
- [ ] Migrations run successfully
- [ ] Admin UI shows collection with correct fields
- [ ] Can create/edit/delete records
- [ ] Relationships work correctly
- [ ] PHP can query via PostgreSQL
- [ ] Sample data seeded for testing

**Complete checklists:** `docs/payload-migration/07-success-criteria.md`

## Quick Reference

### Development Commands
```bash
# Start Payload dev server
yarn payload:dev

# Run migrations
yarn payload migrate

# Seed sample data
yarn seed:payload

# Access Admin UI
open http://localhost:3000/admin
```

### PostgreSQL Connection
```env
DATABASE_URI=postgresql://user:pass@localhost:5432/ynot_payload_dev
DATABASE_SSL=disable  # For local development
```

### Useful Queries
```sql
-- List all collections (tables)
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;

-- Check collection structure
\d concerts

-- Sample data query
SELECT * FROM concerts 
ORDER BY date DESC 
LIMIT 5;
```

**More examples:** `docs/payload-migration/08-quick-reference.md`

## Common Patterns

### Many-to-Many Relationships
Use Payload's relationship field with `hasMany: true`:
```typescript
{
  name: 'artists',
  type: 'relationship',
  relationTo: 'artists',
  hasMany: true,
}
```

### Soft Deletes
Payload handles this automatically with `timestamps: true` in collection config.

### Rich Text Content
Use Payload's lexical editor for Posts:
```typescript
{
  name: 'content',
  type: 'richText',
}
```

### File Uploads
Configure cloudinary plugin for Media collection:
```typescript
plugins: [
  cloudinaryPlugin({
    collections: {
      media: true,
    },
  }),
]
```

## Troubleshooting

### Migration Fails
- Check PostgreSQL connection
- Verify all dependencies installed
- Review migration logs: `yarn payload migrate --debug`

### Admin UI Not Accessible
- Ensure `yarn payload:dev` is running
- Check port 3000 is available
- Verify DATABASE_URI in `.env.local`

### PHP Can't Query
- Confirm PostgreSQL credentials
- Test connection: `psql -h localhost -U user -d ynot_payload_dev`
- Check table names match schema

## Reference Documentation

Comprehensive details in these chapters:

1. **[Project Overview](docs/payload-migration/01-project-overview.md)** - Goals, current state, strategy
2. **[Architecture Decisions](docs/payload-migration/02-architecture-decisions.md)** - Data handling, patterns
3. **[Core Data Models](docs/payload-migration/03-core-data-models.md)** - All collections with status
4. **[PHP PostgreSQL Querying](docs/payload-migration/03.5-php-postgresql-querying.md)** - Direct SQL access
5. **[Migration Tasks](docs/payload-migration/04-migration-tasks.md)** - Step-by-step tasks
6. **[Shared Utilities](docs/payload-migration/05-shared-utilities.md)** - File structure, patterns
7. **[Frontend Cutover](docs/payload-migration/06-frontend-cutover.md)** - Feature flags, deployment
8. **[Success Criteria](docs/payload-migration/07-success-criteria.md)** - Per-collection checklists
9. **[Quick Reference](docs/payload-migration/08-quick-reference.md)** - Commands, queries, templates
10. **[Relational Advantages](docs/payload-migration/09-relational-advantages.md)** - Why PostgreSQL
11. **[CMS Comparison](docs/payload-migration/10-cms-switching-considerations.md)** - Sanity vs Payload
12. **[Capacity Planning](docs/payload-migration/11-capacity-planning.md)** - Limits, pricing
13. **[Cloudinary Integration](docs/payload-migration/12-cloudinary-integration.md)** - Media storage setup

Each chapter is self-contained for cold-start agent conversations.

## Workflow Tips

1. **Start small**: Begin with base collections (People, Venues)
2. **Test incrementally**: Verify each collection before moving to next
3. **Seed data**: Use sample data to test relationships
4. **Document issues**: Note any migration problems for team review
5. **Follow priority order**: Collections are ordered by dependencies

---

**Remember:** This is a two-phase project. Phase 1 (current) focuses on data migration and CMS setup. Phase 2 will handle frontend redesign.
