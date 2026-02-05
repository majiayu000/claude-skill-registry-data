---
name: schema-doc-sync
description: "Update database schema documentation when Prisma schema changes. Use after modifying schema.prisma or when the user asks to sync database documentation."
event: schema-change
auto_trigger: true
version: "2.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - schema_diff
  - affected_tables
  - migration_name
output: updated_schema_docs
output_format: "Updated database-schema markdown files"
output_path: "docs/technical/backend/database/"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "schema-change"
    - "migration-complete"
  file_patterns:
    - "prisma/schema.prisma"
    - "prisma/migrations/**"
  conditions:
    - "migration skill completed"
    - "schema.prisma modified"

# Validation
validation_rules:
  - "all affected tables documented"
  - "schema_stats updated"
  - "version bumped"

# Chaining
chain_after: [migration]
chain_before: [doc-index-update]

# Agent Association
called_by: ["@DataArchitect"]
mcp_tools:
  - mcp_payment-syste_query_docs_by_type
  - read_file
  - replace_string_in_file
---

# Schema Documentation Sync Skill

> **Purpose:** Automatically update database schema documentation when Prisma schema changes. Maintains consistency between code and docs.

## Trigger

**When:** After `migration.skill` completes OR `prisma/schema.prisma` is modified
**Context Needed:** Schema diff, affected tables, existing docs
**MCP Tools:** `mcp_payment-syste_query_docs_by_type`, `read_file`, `replace_string_in_file`

## Schema → Doc Mapping

| Schema Model             | Doc File                   | Module         |
| :----------------------- | :------------------------- | :------------- |
| User, Business, Role     | 01-AUTH-SCHEMA.md          | authentication |
| Merchant, Location       | 02-BUSINESS-SCHEMA.md      | business       |
| Notification, Template   | 03-COMMUNICATION-SCHEMA.md | communication  |
| Product, Category, Stock | 04-INVENTORY-SCHEMA.md     | inventory      |
| Order, OrderItem, Cart   | 05-SALES-SCHEMA.md         | sales          |
| Payment, Transaction     | 06-PAYMENTS-SCHEMA.md      | payments       |
| Invoice, TaxConfig       | 07-BILLING-SCHEMA.md       | billing        |
| Customer, Loyalty        | 08-CRM-SCHEMA.md           | crm            |
| Metrics, Reports         | 09-ANALYTICS-SCHEMA.md     | analytics      |

## Update Process

1. **Detect changes** - Parse schema diff
2. **Identify affected docs** - Map models to schema docs
3. **Load existing docs** - Read current content
4. **Update tables** - Modify table definitions
5. **Update stats** - Recalculate schema_stats
6. **Bump version** - Increment patch version
7. **Update date** - Set last_updated to today
8. **Update ER diagram** - Modify FULL-ER-DIAGRAM.md

## Table Format

```markdown
### TableName

| Column     | Type     | Constraints             | Description        |
| :--------- | :------- | :---------------------- | :----------------- |
| id         | String   | PK, CUID                | Unique identifier  |
| createdAt  | DateTime | NOT NULL, DEFAULT now() | Creation timestamp |
| name       | String   | NOT NULL                | Display name       |
| merchantId | String   | FK → Merchant           | Owner reference    |
```

## Frontmatter Updates

```yaml
# Auto-update these fields
last_updated: "2026-01-26" # Today's date
version: "1.0.1" # Bump patch

# Recalculate these
schema_stats:
  total_tables: 5 # Count models
  total_columns: 45 # Count fields
  total_indexes: 12 # Count @@index
```

## ER Diagram Update

When models change, update PlantUML in FULL-ER-DIAGRAM.md:

```plantuml
' Add new entity
entity "NewModel" {
  *id : String <<PK>>
  --
  createdAt : DateTime
  name : String
}

' Add relation
NewModel ||--o{ OtherModel : has
```

## Validation

After sync:

- [ ] Doc version incremented
- [ ] last_updated is today
- [ ] Table columns match schema
- [ ] Indexes documented
- [ ] Relations accurate

## Reference

- [03-DATABASE-SCHEMA-TEMPLATE.md](/docs/templates/03-DATABASE-SCHEMA-TEMPLATE.md)
- [FULL-ER-DIAGRAM.md](/docs/technical/backend/database/FULL-ER-DIAGRAM.md)
- [DATABASE-DESIGN.md](/docs/technical/backend/DATABASE-DESIGN.md)
