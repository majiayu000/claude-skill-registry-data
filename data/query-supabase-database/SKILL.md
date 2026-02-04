---
name: Query Supabase Database
description: Execute PostgreSQL queries against the Supabase database using psql with 1Password credential retrieval
---

# Query Supabase Database

## Purpose
Provides a standardized way to query the Supabase PostgreSQL database:
- Execute SQL queries with secure credential retrieval
- View table structures and data
- Manage database records (INSERT, UPDATE, DELETE)
- Test migrations and schema changes

## When to Use
- Verifying migration results
- Debugging data issues
- Inspecting table structures
- Running ad-hoc queries
- Testing RLS policies

## Connection Pattern

All database queries use this connection string format:

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "SQL QUERY HERE"
```

**Important**:
- Single quotes around the 1Password reference: `'op://...'`
- Double quotes around the SQL query: `"SELECT ..."`
- Use the pooler connection for better performance

## Common Operations

### List Tables

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "\dt"
```

### Describe Table Structure

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "\d table_name"
```

### View Organizations

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "SELECT id, name, domain FROM organizations;"
```

### View User Profiles

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "SELECT id, email, full_name, role, organization_id FROM profiles;"
```

### View Integrations

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "SELECT id, organization_id, integration_type, name, auth_mode FROM integrations;"
```

## Data Manipulation

### Insert Organization

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "INSERT INTO organizations (name, slug, plan) VALUES ('Company Name', 'company-slug', 'pay_as_you_go') RETURNING id, name;"
```

### Update Record

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "UPDATE integrations SET auth_mode = 'realtime_approval' WHERE id = 'uuid-here' RETURNING id, name, auth_mode;"
```

### Delete Record

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "DELETE FROM table_name WHERE id = 'uuid-here' RETURNING id;"
```

## Running SQL Files

For migrations or complex scripts:

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -f path/to/script.sql
```

## Investigation Tables

### View Workflow Runs

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "SELECT id, workflow_id, status, started_at, metadata FROM workflow_runs ORDER BY started_at DESC LIMIT 10;"
```

### View Bank Transactions

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "SELECT id, bank_txn_id, account_id, date, amount, memo FROM bank_transactions ORDER BY date DESC LIMIT 10;"
```

### Test Full-Text Search

```bash
psql "postgresql://postgres.oegxmnknuqvibndnrgou:$(op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass')@aws-1-us-east-2.pooler.supabase.com:5432/postgres" -c "SELECT bank_txn_id, memo, name FROM bank_transactions WHERE search_vector @@ websearch_to_tsquery('english', 'interest payment');"
```

## Key Tables

- **organizations**: Organization/tenant records
- **profiles**: User profiles (linked to auth.users)
- **integrations**: External system integrations (NetSuite, QuickBooks, etc.)
- **workflows**: Temporal workflow execution records
- **sso_connections**: SSO/SAML connections via WorkOS
- **workflow_runs**: Bank reconciliation workflow executions (investigation)
- **bank_transactions**: Imported bank statements (investigation)
- **gl_transactions**: General ledger entries (investigation)
- **match_results**: Transaction matching results (investigation)
- **created_transactions**: JEs/transfers/checks created (investigation)
- **investigation_conversations**: Chat conversations
- **investigation_messages**: Chat messages

## Best Practices

1. **Always use RETURNING clause** for INSERT/UPDATE/DELETE to see results
2. **Test with LIMIT** when querying large tables
3. **Use transaction blocks** for complex operations:
   ```sql
   BEGIN;
   -- your queries here
   ROLLBACK; -- or COMMIT;
   ```
4. **Check RLS policies** - queries may return empty if user context isn't set
5. **Use pg_catalog** for metadata queries to avoid RLS issues

## Troubleshooting

### Connection Issues
- Verify 1Password CLI is installed: `op --version`
- Verify you're signed in: `op whoami`
- Test credential retrieval: `op read 'op://Private/wtoof5i5k7jiap6gnzmg3n7u5m/dbPass'`

### Empty Results
- Check if RLS is enabled: `SELECT tablename, rowsecurity FROM pg_tables WHERE tablename = 'your_table';`
- Verify organization_id: `SELECT organization_id FROM profiles WHERE id = auth.uid();`

### Performance
- Use EXPLAIN ANALYZE to check query plans
- Verify indexes exist: `\di table_name*`
- Check for sequential scans on large tables
