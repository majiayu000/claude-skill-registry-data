---
name: test-data-cleanup
description: Use after running tests to clean up test data. Analyzes tenant structure, identifies test-created tenants (empty shells), and safely removes only records with "Test" pattern. Always shows preview and requires confirmation before deletion.
---

# Test Data Cleanup Skill

## Golden Rule

**All test data MUST contain "Test" in the name or "@test." in email.**

This ensures safe, pattern-based cleanup that never touches real data.

## Tenant Structure (CRITICAL)

### Production Tenant
- **Volta** (`11111111-1111-1111-1111-111111111111`) - Main org with REAL data mixed with test data
- Contains: Real companies, contacts, Fireflies meetings, AND test forms/programs

### Test-Created Tenants (Empty Shells)
Tests often create new tenants instead of using Volta. These are identifiable by:
- Timestamp in name: `Org A 1763320623066`
- Generic test names: `Test`, `Organization A`, `Organization B`
- All have **0 records** - safe to delete entirely

### Predefined Test Tenants (May Not Exist)
- Acme/Volta: `11111111-1111-1111-1111-111111111111`
- Beta: `22222222-2222-2222-2222-222222222222`
- Gamma: `33333333-3333-3333-3333-333333333333`

## Cleanup Strategy

### Step 1: Analyze Tenant Structure

```sql
-- Show all tenants with data counts
SELECT
  t.name as tenant_name,
  t.id as tenant_id,
  CASE
    WHEN t.id = '11111111-1111-1111-1111-111111111111' THEN 'VOLTA (Main)'
    WHEN t.name ~ '\d{10,}' THEN 'TEST-CREATED (timestamp)'
    WHEN t.name IN ('Test', 'Organization A', 'Organization B') THEN 'TEST-CREATED (generic)'
    ELSE 'UNCLEAR'
  END as tenant_type,
  (SELECT COUNT(*) FROM companies c WHERE c.tenant_id = t.id) as companies,
  (SELECT COUNT(*) FROM contacts co WHERE co.tenant_id = t.id) as contacts,
  (SELECT COUNT(*) FROM forms f WHERE f.tenant_id = t.id) as forms
FROM tenants t
ORDER BY tenant_type, t.name;
```

### Step 2: Delete Empty Test-Created Tenants

```sql
-- Find empty test-created tenants
SELECT id, name FROM tenants
WHERE (name ~ '\d{10,}' OR name IN ('Test', 'Organization A', 'Organization B'))
  AND id != '11111111-1111-1111-1111-111111111111'
  AND id != '22222222-2222-2222-2222-222222222222'
  AND id != '33333333-3333-3333-3333-333333333333';

-- Delete them (after verification)
DELETE FROM tenants WHERE id IN (...);
```

### Step 3: Clean Test Data in Volta (Pattern-Based)

Only delete records with "Test" in name/title:

```sql
-- Preview counts in Volta
SELECT 'forms' as table_name, COUNT(*) FILTER (WHERE title ILIKE '%test%') as test_matches
FROM forms WHERE tenant_id = '11111111-1111-1111-1111-111111111111'
UNION ALL
SELECT 'programs', COUNT(*) FILTER (WHERE name ILIKE '%test%')
FROM programs WHERE tenant_id = '11111111-1111-1111-1111-111111111111'
UNION ALL
SELECT 'report_sessions', COUNT(*) FILTER (WHERE title ILIKE '%test%')
FROM report_sessions WHERE tenant_id = '11111111-1111-1111-1111-111111111111'
UNION ALL
SELECT 'companies', COUNT(*) FILTER (WHERE business_name ILIKE '%test%')
FROM companies WHERE tenant_id = '11111111-1111-1111-1111-111111111111';
```

### Step 4: Delete Test Users

```sql
-- Find test users by email pattern
SELECT id, email FROM auth.users
WHERE email LIKE '%@test.%' OR email LIKE '%@example.%';
```

## Tables to Clean (FK-Safe Order)

| Order | Table | Pattern Column | Query |
|-------|-------|----------------|-------|
| 1 | forms | title | `title ILIKE '%test%'` |
| 2 | report_sessions | title | `title ILIKE '%test%'` |
| 3 | programs | name | `name ILIKE '%test%'` |
| 4 | companies | business_name | `business_name ILIKE '%test%'` |
| 5 | contacts | first_name/last_name | `first_name ILIKE '%test%' OR last_name ILIKE '%test%'` |
| 6 | user_sessions | (linked) | Delete for test users |
| 7 | organization_members | (linked) | Delete for test users |
| 8 | auth.users | email | `email LIKE '%@test.%'` |
| 9 | tenants | name | Empty test-created tenants |

## Tables to NEVER Clean (Real Data)

| Table | Reason |
|-------|--------|
| fireflies_staged_meetings | Real imported meetings |
| meeting_transcripts | Real meeting data |
| interactions | Real meeting records |
| contacts (without Test) | Real people |
| companies (without Test) | Real businesses |
| reports | Real generated reports |

## Naming Conventions (For Writing Tests)

### Users/Emails
```typescript
// CORRECT - contains @test.com
`test-feature-${Date.now()}@test.com`

// WRONG - real domain
`user-${Date.now()}@gmail.com`
```

### Companies
```typescript
// CORRECT - contains "Test"
`Test Company ${Date.now()}`

// WRONG - no "Test" identifier
`Company A ${Date.now()}`
```

### Contacts
```typescript
// CORRECT - contains "Test"
{ first_name: 'Test', last_name: `User ${Date.now()}` }

// WRONG - looks like real person
{ first_name: 'Alice', last_name: 'Smith' }
```

### Tenants
```typescript
// CORRECT - use existing test tenant
const tenantId = TEST_TENANT_ACME // '11111111-1111-1111-1111-111111111111'

// WRONG - creating new tenant
const { data: tenant } = await adminClient.from('tenants').insert({ name: 'Org A' })
```

## Agent Workflow

When asked to clean up test data:

1. **Analyze** - Query tenant structure and data distribution
2. **Identify** - Find test-created tenants and test pattern records
3. **Preview** - Show summary table to user
4. **Confirm** - Ask for explicit approval
5. **Delete** - Execute in FK-safe order
6. **Report** - Show results

### Example Output

```
## Tenant Analysis
- Volta (main): 283 companies, 836 contacts, 318 Fireflies meetings
- Test-created tenants: 13 (all empty)

## Test Data in Volta
- Forms with "Test": 203
- Programs with "Test": 10
- Report sessions with "Test": 18
- Companies with "Test": 3

## Test Users
- @test.com/@example.com emails: 527

## Recommended Cleanup
1. Delete 13 empty test-created tenants
2. Delete 527 test users
3. Delete 203 test forms
4. Delete 10 test programs
5. Delete 18 test report sessions
6. Delete 3 test companies

Proceed? (y/n)
```

## Test Helper Integration

Use `__tests__/api/helpers.ts`:

```typescript
import {
  createTestUser,           // Uses @test.com email
  createTestCompany,        // Defaults to "Test Company..."
  createTestContact,        // Defaults to "Test" first name
  createTestForm,           // Defaults to "Test Form..."
  createTestReport,         // Defaults to "Test Report..."
  countTestDataByPattern,   // Preview before delete
  cleanupTestDataByPattern, // Safe pattern-based cleanup
  TEST_TENANT_ACME,         // Use this, don't create new tenants!
  TEST_TENANT_BETA,
  TEST_TENANT_GAMMA
} from '@/__tests__/api/helpers'
```

## Common Issues

### Issue: Tests create new tenants
**Fix**: Always use `TEST_TENANT_ACME` instead of creating new tenants

### Issue: Test data doesn't have "Test" in name
**Fix**: Update test to use proper naming convention

### Issue: Real data accidentally has "Test" in name
**Check**: Verify before deletion - this should be rare
