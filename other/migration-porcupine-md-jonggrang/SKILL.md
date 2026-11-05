---
name: migration
description: Generate database migration, model update, and seed data
type: scaffold
project_types: [web-app, api]
trigger: "create migration, add table, change schema, database migration"
inputs:
  - name: description
    description: Description of database change (e.g. "add users table", "add email column to orders")
    required: true
  - name: table
    description: Related table name
    required: false
---

## Context

Project {{project_name}} uses {{stack}}.
You will create a database migration for: "{{input.description}}".

Read AGENTS.md and existing migrations to understand conventions.

## Instructions

1. **Detect ORM/migration tool**
   - Prisma: `prisma/schema.prisma`
   - Drizzle: `drizzle.config.ts` + `src/db/schema.ts`
   - Knex: `knexfile.js` + `migrations/`
   - TypeORM: `ormconfig.ts` + `src/entities/`
   - SQLAlchemy: `alembic/`
   - golang-migrate: `migrations/`

2. **Update schema/model**
   - Prisma: update `schema.prisma`
   - Drizzle: update schema file
   - TypeORM: update entity file
   - Others: according to ORM convention

3. **Generate migration file**
   - Prisma: `npx prisma migrate dev --name {{input.description | slugify}}`
   - Drizzle: `npx drizzle-kit generate`
   - Knex: `npx knex migrate:make {{input.description | slugify}}`
   - Manual: create timestamped migration file

4. **Update seed data** (if applicable)
   - Add/update seed for new/changed tables
   - Ensure seed is idempotent

5. **Update types** (if generated)
   - Prisma: `npx prisma generate`
   - Drizzle: types auto-generated from schema

6. **Test migration**
   - Run migration on test database
   - Verify schema is correct
   - Run existing tests (ensure nothing breaks)

## Script

```bash
#!/bin/bash
# Detect ORM
if [ -f "prisma/schema.prisma" ]; then
  echo "ORM: Prisma"
  echo "Run: npx prisma migrate dev"
elif [ -f "drizzle.config.ts" ] || [ -f "drizzle.config.js" ]; then
  echo "ORM: Drizzle"
  echo "Run: npx drizzle-kit generate"
elif [ -f "knexfile.js" ] || [ -f "knexfile.ts" ]; then
  echo "ORM: Knex"
  echo "Run: npx knex migrate:make"
elif ls src/entities/*.ts 1>/dev/null 2>&1; then
  echo "ORM: TypeORM"
fi
```

## Validation

- [ ] Schema/model updated correctly
- [ ] Migration file generated
- [ ] Migration runs successfully (up)
- [ ] Migration rollback works (down)
- [ ] Existing tests still pass
- [ ] Types updated (if applicable)
- [ ] Seed data updated (if applicable)
