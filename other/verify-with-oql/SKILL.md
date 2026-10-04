---
name: verify-with-oql
description: "Verify microflow side effects and data changes with OQL against a running app. Use after executing changes to confirm data was created, updated or deleted as expected, or to back a browser test with a data assertion."
---

# Verify with OQL Skill

This skill documents how to verify microflow side effects and data changes using OQL queries against a running Mendix app.

## When to Use This Skill

Use this when:
- You've deployed changes and want to verify data was created/updated/deleted correctly
- You need to confirm a microflow produced the expected side effects
- You're combining Playwright UI tests with backend data verification
- You want a fast feedback loop: deploy, trigger, verify

## The Pattern

The core verification workflow is:

1. **Deploy** — apply MDL changes and rebuild
2. **Trigger** — execute the action (via UI, microflow call, or API)
3. **Verify** — query the database with OQL to confirm the result

```bash
# 1. Deploy
mxcli exec changes.mdl -p app.mpr
mxcli docker build -p app.mpr --skip-check
mxcli docker reload -p app.mpr   # or: mxcli docker up -p app.mpr --fresh --wait

# 2. Trigger (example: call a microflow that creates test data)
# This could be via Playwright, a rest call, or manual interaction

# 3. Verify
mxcli oql -p app.mpr "select Name, Email from MyModule.Customer where Name = 'Jane Doe'"
```

## OQL Verification Examples

### Check data was created

```bash
# Verify a customer was created
mxcli oql -p app.mpr "select Name, Email from Sales.Customer where Name = 'Test Customer'"

# count records
mxcli oql -p app.mpr "select count(*) as Total from Sales.Order"
```

### Check data was updated

```bash
# Verify status was changed
mxcli oql -p app.mpr "select OrderNumber, status from Sales.Order where OrderNumber = 'ORD-001'"
```

### Check data was deleted

```bash
# Verify record no longer exists (should return empty)
mxcli oql -p app.mpr "select count(*) as Total from Sales.Customer where Name = 'Deleted Customer'"
```

### Check associations

```bash
# Verify an association was set (join query)
mxcli oql -p app.mpr \
  "select o.OrderNumber, c.Name from Sales.Order o join o/Sales.Order_Customer/Sales.Customer c where o.OrderNumber = 'ORD-001'"
```

### JSON output for assertions

Use `--json` for structured output that's easy to parse in scripts:

```bash
# json output for piping to jq
mxcli oql -p app.mpr --json "SELECT Name FROM Sales.Customer" | jq '.[].Name'

# count check in a script
count=$(mxcli oql -p app.mpr --json "SELECT count(*) AS Total FROM Sales.Order" | jq -r '.[0].Total')
if [ "$count" -gt 0 ]; then
  echo "Orders exist: $count"
fi
```

## Combining with Playwright

The most powerful pattern: trigger actions through the UI with Playwright, then verify side effects with OQL.

### Example: Create via UI, verify via OQL

```typescript
// tests/verify-create.spec.ts
import { test, expect } from '@playwright/test';
import { execSync } from 'child_process';
import { login } from './utils/login';

function oql(query: string): any[] {
  const result = execSync(
    `mxcli oql -p app.mpr --json "${query}"`,
    { encoding: 'utf-8' }
  );
  return JSON.parse(result);
}

test('creating a customer via UI persists correctly', async ({ page }) => {
  await login(page);
  await page.goto('/p/Customer_Edit');

  // Fill the form
  await page.locator('.mx-name-txtName input').fill('OQL Test Customer');
  await page.locator('.mx-name-txtEmail input').fill('oql@test.com');
  await page.locator('.mx-name-btnSave').click();

  // wait for save to complete
  await page.waitForTimeout(2000);

  // Verify via OQL
  const rows = oql("select Name, Email from Sales.Customer where Name = 'OQL Test Customer'");
  expect(rows).toHaveLength(1);
  expect(rows[0].Email).toBe('oql@test.com');
});
```

### Example: Verify microflow side effects

```typescript
test('approving an order updates status and creates audit log', async ({ page }) => {
  await login(page);
  await page.goto('/p/Order_Overview');

  // Click approve on first order
  await page.locator('.mx-name-btnApprove').first().click();
  await page.waitForTimeout(2000);

  // Verify order status changed
  const orders = oql("select status from Sales.Order where OrderNumber = 'ORD-001'");
  expect(orders[0].Status).toBe('Approved');

  // Verify audit log was created
  const logs = oql("select action from Sales.AuditLog where action = 'Order Approved'");
  expect(logs.length).toBeGreaterThan(0);
});
```

## Combining with Hot Reload

For the fastest iteration loop when developing microflow logic:

```bash
# 1. Edit microflow
mxcli exec fix-logic.mdl -p app.mpr

# 2. Rebuild (fast)
mxcli docker build -p app.mpr --skip-check

# 3. Hot reload (no restart, keeps data)
mxcli docker reload -p app.mpr

# 4. Trigger the microflow (via UI or test)

# 5. Verify the result
mxcli oql -p app.mpr "select status from Sales.Order where OrderNumber = 'ORD-001'"

# Repeat from step 1 until correct
```

This loop avoids container restarts and database resets, making each iteration take seconds instead of minutes.

## Tips

- **Use `--json` for scripted assertions** — structured output is easier to parse than table format
- **OQL is read-only** — `mxcli oql` uses the `preview_execute_oql` action which cannot modify data
- **OQL won't see rows you wrote directly into Postgres until the runtime reloads.** `mxcli oql`
  executes through the *running app's* query layer (not a separate DB), so rows seeded with direct
  SQL `INSERT`s (see [demo-data](../demo-data/SKILL.md)) are invisible until the runtime re-reads them.
  After seeding, run `mxcli docker reload` (or restart the app) before trusting an OQL `count(*)` of
  `0`. To confirm the rows landed *before* a reload, query Postgres directly (`mxcli sql …`).
- **Check before and after** — query the state before triggering an action to establish a baseline
- **Common OQL patterns for testing:**
  - `count(*)` to verify record counts
  - `where` clauses to find specific records
  - `join` to verify associations were set
  - `ORDER by ... limit 1` to check the most recent record
- **`--direct` mode** is faster when the admin port is reachable (after `admin.addresses` build patch)

## Related Skills

- [/test-app](../test-app/SKILL.md) — Full Playwright test patterns and setup
- [/runtime-admin-api](../runtime-admin-api/SKILL.md) — Admin API details and curl examples
- [/docker-workflow](../docker-workflow/SKILL.md) — Build, run, and hot reload workflow
- [/write-oql-queries](../write-oql-queries/SKILL.md) — OQL syntax reference
