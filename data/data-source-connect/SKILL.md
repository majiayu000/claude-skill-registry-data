---
name: data-source-connect
description: Connect your own data source to replace the demo unicorns data. Use when the user wants to use their own database URL or CSV file instead of the sample data. Triggers on requests to connect database, import CSV, change data source, use own data, or switch from demo data.
---

# Data Source Connect

Replace the demo unicorns data with user's own data source. Supports two modes:

1. **Database URL** - Connect to an existing PostgreSQL database
2. **CSV File** - Import a CSV file and create a new table

## Mode 1: Database URL

When user provides a PostgreSQL connection URL:

### Step 1: Update Environment

Update `.env` file:
```
POSTGRES_URL="<user-provided-connection-string>"
```

### Step 2: Discover Schema

Connect to the database and retrieve schema information:

```sql
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

### Step 3: Update Actions

Edit `app/actions.ts` - update the schema in these locations:

1. **`generateQuery` function** (~line 18): Replace the unicorns schema in the system prompt with the new table schema. Include:
   - Table name and column definitions
   - Data type hints (e.g., "valuation is in billions")
   - Available enum values for categorical fields
   - Query patterns specific to the data

2. **`explainQuery` function** (~line 115): Replace the unicorns schema in the system prompt.

3. **`runGenerateSQLQuery` function** (~line 93): Update the table name in error handling.

### Step 4: Generate Sample Prompts

Create 3-5 sample natural language queries for the new data to help users understand what they can ask.

## Mode 2: CSV File

When user provides a CSV file:

### Step 1: Analyze CSV Structure

Read the CSV file and analyze:
- Column names (header row)
- Data types (infer from sample values)
- Null/empty value handling requirements

### Step 2: Generate Schema

Create SQL schema based on CSV structure. Type inference rules:
- Numbers with decimals -> `DECIMAL(10, 2)`
- Integers -> `INTEGER`
- Dates (various formats) -> `DATE`
- Boolean values -> `BOOLEAN`
- Everything else -> `VARCHAR(255)` or `TEXT` for long content

### Step 3: Update seed.ts

Edit `lib/seed.ts`:

1. Update `CREATE TABLE` statement with new schema
2. Update CSV parsing logic for new column names
3. Add type conversion for each column
4. Handle missing/null values with appropriate defaults or skip logic

Example seed.ts structure:
```typescript
export async function seed() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS <table_name> (
      id SERIAL PRIMARY KEY,
      <column1> <type1>,
      <column2> <type2>,
      ...
    );
  `);

  // Parse CSV
  const results: any[] = [];
  const csvFilePath = path.join(process.cwd(), '<filename>.csv');

  await new Promise((resolve, reject) => {
    fs.createReadStream(csvFilePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', resolve)
      .on('error', reject);
  });

  // Insert with null handling
  for (const row of results) {
    // Skip rows with critical missing data or use defaults
    const value1 = row['ColumnName'] || null;

    await pool.query(
      `INSERT INTO <table_name> (...) VALUES (...) ON CONFLICT DO NOTHING`,
      [value1, ...]
    );
  }
}
```

### Step 4: Update Actions

Same as Database URL Mode Step 3 - update schema references in `app/actions.ts`.

### Step 5: Run Seed

```bash
pnpm run seed
```

### Step 6: Generate Sample Prompts

Create 3-5 sample natural language queries for the new data to help users understand what they can ask. Examples should cover:
- Basic filtering (e.g., "Show all records where X > Y")
- Aggregations (e.g., "What is the total/average X by Y?")
- Time-based queries if applicable (e.g., "Show trends over time")
- Top/bottom queries (e.g., "Top 10 by X")

## Critical Files to Update

| File | What to Update |
|------|----------------|
| `.env` | `POSTGRES_URL` connection string |
| `lib/seed.ts` | Table schema, CSV parsing, insert logic |
| `app/actions.ts` | Schema in `generateQuery` and `explainQuery` prompts |

## Schema Prompt Template

When updating the schema in `app/actions.ts`, use this template:

```typescript
system: `You are a SQL (postgres) and data visualization expert. Your job is to help the user write a SQL query to retrieve the data they need. The table schema is as follows:

<table_name> (
  id SERIAL PRIMARY KEY,
  <column_name> <data_type> <constraints>,
  ...
);

Only retrieval queries are allowed.

[Add data-specific hints here, e.g.:]
- Use ILIKE for case-insensitive text search
- <field_name> values include: value1, value2, value3
- <numeric_field> is in <units> (e.g., thousands, millions)

EVERY QUERY SHOULD RETURN QUANTITATIVE DATA THAT CAN BE PLOTTED ON A CHART!
`,
```

## Null Value Handling

For CSV imports with missing data:
- **Skip row**: When critical identifier is missing
- **Default value**: Use sensible defaults (0 for numbers, 'Unknown' for strings)
- **Allow null**: For truly optional fields
