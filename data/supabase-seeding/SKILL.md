---
name: supabase-seeding
description: "Database seeding toolkit for Supabase projects. Use when: (1) Creating seed data files, (2) Populating lookup/reference tables, (3) Generating test data, (4) Bulk loading data with COPY, (5) Running seed files against database, (6) Managing large seed files with DVC"
license: Proprietary. LICENSE.txt has complete terms
---

# Supabase Database Seeding

Toolkit for populating Supabase databases with seed data.

**Helper Scripts Available** (uv scripts - no install needed):
- `scripts/run_seeds.py` - Run seed files with progress monitoring
- `scripts/generate_seed.py` - Generate seed data from schema (uses Faker)

**Always run scripts with `--help` first** to see usage:
```bash
uv run scripts/run_seeds.py --help
uv run scripts/generate_seed.py --help
```

## Decision Tree: Seeding Approach

```
Task → What type of data?
    ├─ Lookup tables (categories, statuses, roles)
    │   └─ Write INSERT with ON CONFLICT DO NOTHING
    │
    ├─ Test/dev data (<1000 rows)
    │   └─ Write INSERT statements in seed file
    │
    ├─ Large dataset (>1000 rows)
    │   └─ Use COPY from CSV
    │       └─ File >1MB? Track with DVC
    │
    └─ Generated data (users, transactions)
        └─ Run: uv run scripts/generate_seed.py --help
```

## Directory Structure

```
supabase/
├── migrations/          # Schema only (DDL) - NO INSERTs
└── seed/                # Data population (DML)
    ├── 01_lookup_tables.sql
    ├── 02_dev_users.sql
    ├── 03_test_data.sql
    └── large_dataset.sql.dvc  # DVC-tracked
```

## Seed File Template

```sql
-- seed/01_lookup_tables.sql
BEGIN;

INSERT INTO tb_categories (id, name, sort_order_num) VALUES
    ('cat-electronics', 'Electronics', 1),
    ('cat-clothing', 'Clothing', 2),
    ('cat-books', 'Books', 3)
ON CONFLICT (id) DO NOTHING;

INSERT INTO tb_statuses (id, name, description_txt) VALUES
    ('active', 'Active', 'Item is active and visible'),
    ('inactive', 'Inactive', 'Item is hidden from users'),
    ('archived', 'Archived', 'Item is archived for records')
ON CONFLICT (id) DO NOTHING;

COMMIT;
```

## Running Seeds

**Single file:**
```bash
psql $DATABASE_URL < supabase/seed/01_lookup_tables.sql
```

**All files in order with progress:**
```bash
uv run scripts/run_seeds.py supabase/seed/
```

**With Supabase CLI (runs seed.sql on reset):**
```bash
supabase db reset
```

## Bulk Loading with COPY

For datasets >1000 rows, MUST use COPY instead of INSERT:

```sql
-- From CSV file
COPY tb_products (id, name, price_amt)
FROM '/path/to/products.csv'
WITH (FORMAT csv, HEADER true);

-- From stdin (useful in seed files)
COPY tb_products (id, name, price_amt) FROM stdin WITH (FORMAT csv);
uuid-1,Product 1,10.00
uuid-2,Product 2,20.00
uuid-3,Product 3,30.00
\.
```

## Large Files with DVC

Track large seed files (>1MB) with [DVC](https://dvc.org/):

```bash
# Initialize DVC (once per repo)
dvc init

# Track large seed file
dvc add supabase/seed/large_dataset.sql
git add supabase/seed/large_dataset.sql.dvc .gitignore

# Push to remote storage
dvc push

# Pull when needed
dvc pull
```

## Best Practices

1. **Numbered prefixes** - `01_`, `02_` ensure execution order
2. **ON CONFLICT DO NOTHING** - Makes seeds idempotent
3. **Wrap in transaction** - BEGIN/COMMIT prevents partial seeds
4. **Separate concerns** - Lookup data vs test data in different files
5. **No PII in git** - Use DVC for sensitive test data
