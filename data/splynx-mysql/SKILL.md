---
name: splynx-mysql
description: |
  Direct MySQL access to Splynx ISP management database.
  Use when querying or modifying Splynx tables: customers, leads (category='lead'), services, tariffs, invoices, payments, tickets, network.
  Faster than REST API for bulk operations. Reference: src/migration/loaders/splynx_mysql/
---

# Splynx MySQL Database

Direct MySQL access to Splynx ISP management platform.

## Connection

```python
from src.migration.loaders.splynx_mysql.connection import mysql_connection

with mysql_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    row = cursor.fetchone()
    cursor.close()
# Auto-commit on success, rollback on exception
```

**Environment variables:**
- `SPLYNX_DB_HOST` - MySQL host (default: localhost)
- `SPLYNX_DB_USER` - MySQL username (required)
- `SPLYNX_DB_PASSWORD` - MySQL password (required)
- `SPLYNX_DB_NAME` - Database name (default: splynx)
- `SPLYNX_DB_PORT` - Port (default: 3306)
- `SPLYNX_DB_SOCKET` - Unix socket (optional, overrides host)

## Key Tables

### Customers
```sql
-- Main customer record (category: person, company, or lead)
-- Always check deleted='0' for active records
SELECT * FROM customers WHERE id = 123 AND deleted = '0';

-- Count all active accounts
SELECT COUNT(*) FROM customers WHERE deleted = '0';

-- Additional info (passport, company, birthday)
SELECT * FROM customer_info WHERE customer_id = 123;

-- Billing settings
SELECT * FROM customer_billing WHERE customer_id = 123;

-- Custom field values
SELECT * FROM customers_values WHERE customer_id = 123;

-- Customer labels
SELECT * FROM customers_labels WHERE customer_id = 123;
```

### Services
```sql
-- Internet services
SELECT * FROM services_internet WHERE customer_id = 123;

-- Custom/generic services
SELECT * FROM services_custom WHERE customer_id = 123;

-- Voice services
SELECT * FROM services_voice WHERE customer_id = 123;

-- Bundle services
SELECT * FROM services_bundle WHERE customer_id = 123;
```

### Tariffs (Service Plans)
```sql
-- Internet tariffs
SELECT * FROM tariffs_internet;

-- Custom tariffs
SELECT * FROM tariffs_custom;

-- Voice tariffs
SELECT * FROM tariffs_voice;

-- One-time tariffs
SELECT * FROM tariffs_one_time;

-- Bundle definitions
SELECT * FROM bundle;
SELECT * FROM bundle_to_tariffs_internet WHERE bundle_id = 1;
```

### Billing
```sql
-- Invoices
SELECT * FROM invoices WHERE customer_id = 123;

-- Invoice line items
SELECT ii.* FROM invoices_items ii
JOIN invoices i ON ii.invoice_id = i.id
WHERE i.customer_id = 123;

-- Payments
SELECT * FROM payments WHERE customer_id = 123;

-- Transactions
SELECT * FROM billing_transactions WHERE customer_id = 123;

-- Failed payments
SELECT * FROM bank_statements_records WHERE customer_id = 123;
```

### Network
```sql
-- Routers/NAS devices
SELECT * FROM routers;

-- Network sites
SELECT * FROM network_sites;

-- IPv4 networks
SELECT * FROM ipv4_networks;

-- IPv4 assignments
SELECT * FROM ipv4_networks_ip WHERE customer_id = 123;

-- IPv6 networks
SELECT * FROM ipv6_networks;
```

### Tickets
```sql
-- Tickets
SELECT * FROM ticket WHERE customer_id = 123;

-- Ticket messages
SELECT * FROM ticket_messages WHERE ticket_id = 456;

-- Ticket groups
SELECT * FROM ticket_groups;
```

### CRM / Leads
```sql
-- Leads are customers with category='lead'
-- NOTE: Always filter deleted='0' for active records
SELECT * FROM customers WHERE category = 'lead' AND deleted = '0';

-- Count active records by category (person, company, lead)
SELECT category, COUNT(*) FROM customers WHERE deleted = '0' GROUP BY category;

-- Lead additional info (deal value, score, owner, source)
-- leads_info.deleted is separate from customers.deleted
SELECT c.*, li.*
FROM customers c
JOIN leads_info li ON li.customer_id = c.id
WHERE c.category = 'lead' AND c.deleted = '0' AND li.deleted = '0';

-- Lead pipeline stages
SELECT * FROM crm_leads_pipeline;

-- Lead activity log
SELECT * FROM crm_activity_log WHERE customer_id = 123;

-- Lead status change history
SELECT * FROM crm_lead_status_logs_changes WHERE customer_id = 123;
```

### Scheduling
```sql
-- Projects
SELECT * FROM scheduling_projects WHERE customer_id = 123;

-- Tasks
SELECT * FROM scheduling_task WHERE project_id = 789;
```

## Query Patterns

### Upsert (Insert or Update)
```python
statement = """
INSERT INTO customers (id, name, email, status)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    email = VALUES(email),
    status = VALUES(status)
"""
cursor.execute(statement, (id, name, email, status))
```

### Batch Insert
```python
from src.migration.loaders.splynx_mysql.connection import chunk_records

statement = "INSERT INTO table (col1, col2) VALUES (%s, %s) ON DUPLICATE KEY UPDATE col2 = VALUES(col2)"
rows = [(1, 'a'), (2, 'b'), (3, 'c'), ...]

for batch in chunk_records(rows, size=200):
    cursor.executemany(statement, batch)
```

### Cascade Delete
```python
# Delete in correct order (children first)
cursor.execute("DELETE FROM invoices_items WHERE invoice_id IN (SELECT id FROM invoices WHERE customer_id = %s)", (cid,))
cursor.execute("DELETE FROM invoices WHERE customer_id = %s", (cid,))
cursor.execute("DELETE FROM services_internet WHERE customer_id = %s", (cid,))
cursor.execute("DELETE FROM customers WHERE id = %s", (cid,))
```

### Reference ID Lookup
```python
from src.migration.loaders.splynx_mysql.connection import fetch_reference_ids

# Get all existing customer IDs
existing_customers = fetch_reference_ids("customers")
if customer_id not in existing_customers:
    print(f"Customer {customer_id} not found")
```

## Loader Modules

Pre-built loaders in `src/migration/loaders/splynx_mysql/`:

| Module | Purpose |
|--------|---------|
| `customers.py` | Customer CRUD, billing, labels |
| `billing.py` | Invoices, payments, transactions |
| `services_tariffs.py` | Service plans, tariffs, bundles |
| `network.py` | Sites, routers, monitoring |
| `inventory.py` | Vendors, products, items |
| `tickets.py` | Tickets, messages, attachments |
| `scheduling.py` | Projects, tasks, checklists |
| `communications.py` | Emails, call logs, activity logs |
| `ip_management.py` | IPv4/IPv6 networks and addresses |
| `fields.py` | Custom field management |

### Example: Using Customer Loader
```python
from src.migration.loaders.splynx_mysql import upsert_customer_records

upsert_customer_records(
    core_row=(id, billing_type, partner_id, ...),
    info_row=(customer_id, company, ...),
    billing_row=(customer_id, payment_method, ...),
    custom_values={"sonar_id": "123"}
)
```

## Safety

**Always backup before modifications:**
```bash
make backup-splynx
```

**Use parameterized queries (prevent SQL injection):**
```python
# Good
cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))

# Bad - SQL injection risk!
cursor.execute(f"SELECT * FROM customers WHERE id = {customer_id}")
```

## Partner Links

Splynx uses partner association tables for multi-tenant:
```python
# Link tariff to partner
cursor.execute(
    "INSERT IGNORE INTO tariffs_internet_to_partners (tariff_id, partner_id) VALUES (%s, %s)",
    (tariff_id, 1)
)
```

## Reference

- Connection module: `src/migration/loaders/splynx_mysql/connection.py`
- All loaders: `src/migration/loaders/splynx_mysql/`
- Test connection:
```bash
mysql -h $SPLYNX_DB_HOST -u $SPLYNX_DB_USER -p$SPLYNX_DB_PASSWORD $SPLYNX_DB_NAME -e "SELECT COUNT(*) FROM customers"
```
