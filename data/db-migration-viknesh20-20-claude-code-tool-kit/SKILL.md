---
name: db-migration
description: "Generates database migration files for schema changes with up/down migrations, safety checks, rollback instructions, and index recommendations. Auto-detects the ORM/migration tool in use."
argument-hint: "[description of schema change]"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Database Migration Helper

## Detect Migration Tool
!`ls prisma/ migrations/ alembic/ alembic.ini db/migrate/ knexfile.* flyway.conf sequelize* typeorm* drizzle.config.* 2>/dev/null`
!`ls package.json 2>/dev/null && cat package.json 2>/dev/null | grep -E "prisma|knex|sequelize|typeorm|drizzle|kysely|mikro-orm" | head -5`
!`ls requirements.txt pyproject.toml 2>/dev/null && cat requirements.txt pyproject.toml 2>/dev/null | grep -iE "alembic|django|sqlalchemy|tortoise" 2>/dev/null | head -5`
!`ls go.mod 2>/dev/null && cat go.mod 2>/dev/null | grep -E "goose|migrate|atlas|ent" | head -5`

## Existing Migrations
!`find . -path "*/migrations/*" -o -path "*/migrate/*" -o -path "*/prisma/migrations/*" -o -path "*/db/migrate/*" 2>/dev/null | grep -v node_modules | tail -10`

---

## Migration Process

### Step 1: Understand the Change
1. Parse the requested schema change
2. Identify affected tables/collections
3. Check current schema state
4. Determine if this is: CREATE, ALTER, DROP, or INDEX

### Step 2: Safety Analysis

**Data Loss Risk Assessment:**
- Dropping a column/table → **HIGH RISK** — requires data backup
- Renaming a column → **MEDIUM RISK** — two-step migration recommended
- Adding NOT NULL without default → **HIGH RISK** — will fail on existing rows
- Changing column type → **MEDIUM RISK** — potential data truncation
- Adding column with default → **LOW RISK** — safe
- Adding index → **LOW RISK** — may lock table on large datasets

### Step 3: Generate Migration

#### For Prisma (Node.js)
```
npx prisma migrate dev --name <description>
```
Update `schema.prisma` first, then generate.

#### For Alembic (Python/SQLAlchemy)
```
alembic revision --autogenerate -m "<description>"
```

#### For Django
```
python manage.py makemigrations --name <description>
```

#### For Rails ActiveRecord
```
rails generate migration <Description>
```

#### For Knex/Sequelize
Create migration file manually following existing patterns.

#### For Go (goose/migrate)
Create SQL files with up/down sections.

#### For Raw SQL
Generate separate UP and DOWN files.

### Step 4: Migration Content

**UP migration must include:**
- Table/column creation or modification
- Default values for new NOT NULL columns
- Indexes for columns used in WHERE, JOIN, ORDER BY
- Foreign key constraints where appropriate
- Comments explaining the change

**DOWN migration must include:**
- Exact reversal of the UP migration
- Data preservation strategy if dropping columns
- Warning comments for irreversible operations

### Step 5: Index Recommendations
For the affected tables, recommend indexes based on:
- New foreign key columns (always index)
- Columns used in WHERE clauses
- Columns used in ORDER BY
- Columns used in JOIN conditions
- Composite indexes for multi-column queries

### Step 6: Deployment Notes
- Run on staging first
- Estimated duration for large tables
- Lock implications (table locks, row locks)
- Recommended maintenance window (if needed)
- Rollback command

---

## Rules
- Always generate both UP and DOWN migrations
- Never drop columns without explicit user confirmation
- Always add indexes for foreign keys
- Test migrations against a copy of production data when possible
- Include data migration logic if restructuring data
