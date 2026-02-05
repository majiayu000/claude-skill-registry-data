---
name: Advanced Patterns
description: SCD Type 2, Closure Table, Shared Family Budget patterns
version: 3.0.0
author: Family Budget Team
tags: [scd-type-2, closure-table, shared-budget, hierarchy, versioning]
dependencies: [db-management, api-development]
architecture_refs:
  - $ref: ../../docs/architecture/database/history.yaml
  - $ref: ../../docs/architecture/database/hierarchy.yaml
  - $ref: ../../docs/architecture/guides/change-checklist.yaml#/checklists/add_history_tracking
---

# Advanced Patterns Skill

Реализация продвинутых архитектурных паттернов: SCD Type 2, Closure Table, Shared Family Budget.

## When to Use

- Добавить SCD Type 2 versioning к dimension таблице
- Создать Closure Table для иерархии
- Реализовать Shared Family Budget endpoint
- Обновить History tracking

## Architecture Context

**References:**
- History Tables: [$ref](../../docs/architecture/database/history.yaml)
- Hierarchy: [$ref](../../docs/architecture/database/hierarchy.yaml)
- Change Checklist: [$ref](../../docs/architecture/guides/change-checklist.yaml#/checklists/add_history_tracking)

**Key Patterns:**

### SCD Type 2 (Slowly Changing Dimension Type 2)

**Purpose:** Track full history of dimension changes

**Current Implementation:** SCD Type 1 (main tables) + SCD Type 2 (history tables)

**Main Tables (SCD Type 1 - In-place updates):**
- `Article`, `User`, `FinancialCenter`, `CostCenter` - NO versioning fields
- Updates modify existing row directly
- Stable PK for fact table FK references

**History Tables (SCD Type 2 - Full versioning):**
- `ArticleHistory`, `UserHistory`, etc. - ALL changes tracked
- Fields: `is_current`, `valid_from`, `valid_to`, `change_type`
- Audit trail with complete snapshot of each version

**Why This Hybrid?**
- Simple queries on main tables (no is_current filter needed)
- Complete audit history in separate tables
- Stable PKs for fact table relationships

### Closure Table

**Purpose:** O(1) hierarchical queries without recursion

**Table Structure:**
```sql
CREATE TABLE t_d_article_hierarchy (
    ancestor_id INT,      -- Parent (or self)
    descendant_id INT,    -- Child (or self)
    depth INT,            -- 0 = self, 1 = direct child, 2+ = nested
    PRIMARY KEY (ancestor_id, descendant_id)
);
```

**Queries:**
- Get all descendants: `WHERE ancestor_id = X`
- Get all ancestors: `WHERE descendant_id = X`
- Get direct children: `WHERE ancestor_id = X AND depth = 1`

### Shared Family Budget

**Purpose:** 2-5 family members see ALL transactions (full transparency)

**Rules:**
- **Fact tables**: NO user_id filtering (all see all)
- **Dimension tables**: Admin-only CREATE/UPDATE/DELETE, all can READ
- **user_id**: Audit trail only (who created/modified)

Reference: `_shared/validation-logic.md#3-shared-budget-model-consistency`

## Commands

### Command: add-scd2-history

**Usage:**
```
Добавь SCD Type 2 history tracking к модели <ModelName>.
```

**What It Does:**
1. Create History table model with ALL fields from main table
2. Add `is_current`, `valid_from`, `valid_to`, `change_type` fields
3. Create service functions for history tracking
4. Create Alembic migration for History table

**Template Reference:**
- `templates/scd-type-2-service.py` - History service
- `examples/article-history.md` - Real Article history implementation

**Critical:** History table MUST have ALL fields from main table!

Reference: `_shared/validation-logic.md#2-history-table-field-completeness`

### Command: add-closure-table

**Usage:**
```
Добавь Closure Table для модели <ModelName> hierarchy.
```

**What It Does:**
1. Create Hierarchy table (ancestor_id, descendant_id, depth)
2. Create indexes on (ancestor_id, depth), (descendant_id, depth)
3. Initialize self-references (depth=0)
4. Create HierarchyService for CRUD operations

**Template Reference:**
- `templates/closure-table.py` - Hierarchy model
- `templates/hierarchy-service.py` - HierarchyService implementation

### Command: implement-shared-budget

**Usage:**
```
Реализуй Shared Budget pattern для endpoint <endpoint-name>.
```

**What It Does:**
1. Remove user_id filtering from fact queries
2. Add admin checks for dimension CREATE/UPDATE/DELETE
3. Keep user_id for audit trail only

**Template Reference:**
- `templates/shared-budget-endpoint.py` - Shared Budget pattern

## Validation Checklist

### SCD Type 2 History
- [ ] History table has ALL fields from main table
- [ ] NO NULL in NOT NULL columns
- [ ] `change_type` set (CREATE/UPDATE/DELETE)
- [ ] `valid_from`, `valid_to`, `is_current` set correctly
- [ ] Service layer updates history on changes

### Closure Table
- [ ] Hierarchy table created (ancestor_id, descendant_id, depth)
- [ ] Indexes on (ancestor_id, depth), (descendant_id, depth), (depth)
- [ ] Self-references initialized (depth=0)
- [ ] HierarchyService handles updates
- [ ] NO direct SQL updates to closure table

### Shared Budget
- [ ] Fact tables: NO user_id filtering
- [ ] Dimension tables: Admin-only CREATE/UPDATE/DELETE
- [ ] user_id used for audit trail only

## Common Mistakes

**Forgot History field:**
- **Symptom**: IntegrityError: null value in column "record_type"
- **Fix**: Copy ALL fields from main table to History table
- **Reference**: `_shared/validation-logic.md#2`

**User_id filtering in Shared Budget:**
- **Symptom**: Users can't see family transactions
- **Fix**: Remove `.where(BudgetFact.user_id == current_user.id)`
- **Reference**: `_shared/validation-logic.md#3`

**Direct UPDATE on dimension (instead of history):**
- **Symptom**: No history record created, audit trail broken
- **Fix**: Use service layer to create history records
- **Reference**: `_shared/validation-logic.md#5`

## Related Skills

- **db-management**: Create models and migrations
- **api-development**: Implement endpoints with patterns

## Quick Links

- History Tables Architecture: [$ref](../../docs/architecture/database/history.yaml)
- Hierarchy Architecture: [$ref](../../docs/architecture/database/hierarchy.yaml)
- Article Example: `backend/app/models/article.py`, `backend/app/models/article_history.py`
