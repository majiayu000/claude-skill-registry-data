---
name: migrate-oracle-forms
description: "Assess and migrate Oracle Forms applications to Mendix — .fmb forms to pages, PL/SQL to microflows, and a staged migration strategy. Use when analysing or converting an Oracle Forms system."
---

# Oracle Forms to Mendix Migration Skill

This skill provides comprehensive guidance for migrating Oracle Forms applications to Mendix using MDL (Mendix Definition Language).

## When to Use This Skill

Use this skill when:
- Converting Oracle Forms (.fmb) applications to Mendix
- Translating PL/SQL logic to Mendix microflows
- Mapping Oracle Forms UI elements to Mendix widgets
- Planning a migration strategy for legacy Oracle Forms systems

## Migration Overview

Oracle Forms migration to Mendix involves:
1. **Data Model**: Oracle tables → Mendix entities
2. **Business Logic**: PL/SQL triggers/procedures → Mendix microflows
3. **User Interface**: Forms blocks/items → Mendix pages/widgets
4. **Navigation**: Form canvases → Mendix page navigation

## Reserved Word Conflicts

Most common words (`check`, `text`, `format`, `value`, `type`, `index`, `status`, `select`, etc.) now work **unquoted** as attribute names in MDL. Only structural keywords (`create`, `delete`, `begin`, `end`, `return`, `entity`, `module`) need quoting.

### Naming Best Practices

While most words are no longer reserved, using descriptive names is still recommended for clarity:

| Oracle Forms Field | Recommended Mendix Name | Notes |
|-------------------|-------------------------|-------|
| `check` | `check` or `CheckStatus` | Works unquoted |
| `text` | `text` or `TextContent` | Works unquoted |
| `format` | `format` or `FormatType` | Works unquoted |
| `value` | `value` or `FieldValue` | Works unquoted |
| `Name` | `Name` or `ItemName` | Works unquoted (not a keyword) |
| `type` | `type` or `ItemType` | Works unquoted |
| `create` | `"create"` or `CreatedBy` | **Requires quoting** (structural keyword) |
| `delete` | `"delete"` or `IsDeleted` | **Requires quoting** (structural keyword) |

### Example

```mdl
mdl 1;
create persistent entity MyModule.FormField (
  check: boolean default false,  -- Works unquoted
  text: string(500),             -- Works unquoted
  format: string(50),            -- Works unquoted
  CheckFlag: boolean default false, -- Renamed alternative (also fine)
  TextContent: string(500), -- Renamed
  FormatType: string(50)    -- Renamed
);
```

## Script Organization

### Execution Order Dependencies

MDL scripts execute statements sequentially. Items created in one statement can be referenced in subsequent statements within the **same script execution**.

**Key Insight**: Microflows and pages created earlier in the script are tracked and can be resolved by later statements.

### Recommended Script Structure

```mdl
mdl 1;
-- ============================================
-- PHASE 1: Domain Model (Entities & Associations)
-- ============================================

create persistent entity MyModule.Customer (
  CustomerCode: string(50),
  CustomerName: string(200),
  Email: string(200),
  IsActive: boolean default true
);

create persistent entity MyModule.Order (
  OrderNumber: string(50),
  OrderDate: datetime,
  TotalAmount: decimal
);

create association MyModule.Order_Customer
from MyModule.Order to MyModule.Customer
type reference;

-- ============================================
-- PHASE 2: Microflows (Business Logic)
-- ============================================

/**
 * Validates and saves a customer record
 * Replaces Oracle Forms POST-INSERT/POST-UPDATE triggers
 */
create microflow MyModule.ACT_Customer_Save ($Customer: MyModule.Customer)
returns boolean as $success
begin
  declare $success boolean = false;

  -- Validation (replaces WHEN-VALIDATE-ITEM)
  if $Customer/CustomerCode = empty then
    validation feedback $Customer/CustomerCode message 'Customer code is required';
    return false;
  end if;

  commit $Customer;
  set $success = true;
  return $success;
end;

-- ============================================
-- PHASE 3: Pages (User Interface)
-- ============================================

-- Now this page can reference the microflow created above
create page MyModule.Customer_Edit (
  Title: 'Edit Customer',
  Layout: Atlas_Core.PopupLayout,
  Params: ( $Customer: MyModule.Customer )
) {
  dataview dvCustomer (DataSource: $Customer) {
    textbox txtCode (Label: 'Customer Code', Attribute: CustomerCode)
    textbox txtName (Label: 'Name', Attribute: CustomerName)
    textbox txtEmail (Label: 'Email', Attribute: Email)
    footer {
      -- Reference to the microflow created in Phase 2
      actionbutton btnSave (Caption: 'Save', Action: call microflow MyModule.ACT_Customer_Save(Customer = $Customer), ButtonStyle: Primary)
      actionbutton btnCancel (Caption: 'Cancel', Action: close page)
    }
  }
};
```

## Validation Feedback

### VALIDATION FEEDBACK Syntax

**CRITICAL**: VALIDATION FEEDBACK requires an attribute path, not just a message.

**WRONG:**
```mdl
validation feedback 'Customer code is required';  -- Missing attribute!
```

**CORRECT:**
```mdl
-- Syntax: VALIDATION FEEDBACK $entity/attribute MESSAGE 'message'
validation feedback $Customer/CustomerCode message 'Customer code is required';
validation feedback $Order/OrderDate message 'Order date cannot be in the future';
```

### Mapping Oracle Forms Validation

| Oracle Forms | Mendix MDL |
|--------------|------------|
| `when-VALIDATE-item` trigger | `if ... validation feedback` in microflow |
| `raise FORM_TRIGGER_FAILURE` | `validation feedback` + `return false` |
| `message('error text')` | `validation feedback $entity/attribute message 'error text'` |

### Complete Validation Pattern

```mdl
mdl 1;
/**
 * Validates order before save
 * Replaces Oracle Forms WHEN-VALIDATE-RECORD trigger
 */
create microflow MyModule.ACT_Order_Validate ($Order: MyModule.Order)
returns boolean as $IsValid
begin
  declare $IsValid boolean = true;

  -- Required field validation
  if $Order/OrderNumber = empty then
    validation feedback $Order/OrderNumber message 'Order number is required';
    set $IsValid = false;
  end if;

  -- Date validation
  if $Order/OrderDate > [%CurrentDateTime%] then
    validation feedback $Order/OrderDate message 'Order date cannot be in the future';
    set $IsValid = false;
  end if;

  -- Cross-field validation
  if $Order/TotalAmount < 0 then
    validation feedback $Order/TotalAmount message 'Total amount cannot be negative';
    set $IsValid = false;
  end if;

  return $IsValid;
end;
```

## PL/SQL to Microflow Mapping

### Data Manipulation

| Oracle PL/SQL | Mendix MDL |
|---------------|------------|
| `insert into table ...` | `$var = create Module.Entity (...)` |
| `update table set ...` | `change $var (...)` + `commit $var` |
| `delete from table ...` | `delete $var` |
| `select ... into ...` | `retrieve $var from Module.Entity where ...` |
| `commit` | `commit $var` |
| `rollback` | Built-in with error handlers |

### Control Flow

| Oracle PL/SQL | Mendix MDL |
|---------------|------------|
| `if ... then ... elsif ... else ... end if` | `if ... then ... else ... end if` |
| `for ... loop ... end loop` | `loop $item in $list begin ... end loop` |
| `while ... loop ... end loop` | Not directly supported; use recursive microflow |
| `CURSOR` | `retrieve $list from ...` then `loop` |
| `EXCEPTION when ... then` | `on error begin ... end error` |

### Example: PL/SQL to MDL

**Oracle PL/SQL:**
```sql
declare
  v_count NUMBER := 0;
  v_total NUMBER := 0;
begin
  for rec in (select * from orders where status = 'PENDING') loop
    v_count := v_count + 1;
    v_total := v_total + rec.amount;

    update orders set status = 'PROCESSED' where id = rec.id;
  end loop;

  commit;
  DBMS_OUTPUT.PUT_LINE('Processed ' || v_count || ' orders, total: ' || v_total);
EXCEPTION
  when OTHERS then
    rollback;
    raise;
end;
```

**Mendix MDL:**
```mdl
mdl 1;
create microflow MyModule.ACT_ProcessPendingOrders ()
returns string as $Result
begin
  declare $count integer = 0;
  declare $Total decimal = 0;
  declare $Result string = '';

  -- Retrieve pending orders (replaces CURSOR) — retrieve creates $OrderList,
  -- never declare a list variable first (CE0053/CE0038, MDL040)
  retrieve $OrderList from MyModule.Order
    where status = 'PENDING';

  -- Process each order (replaces FOR LOOP)
  loop $Order in $OrderList
  begin
    set $count = $count + 1;
    set $Total = $Total + $Order/Amount;

    change $Order (status = 'PROCESSED');
    commit $Order on error begin
      log error 'Failed to process order: ' + $Order/OrderNumber;
    end error;
  end loop;

  log info 'Processed ' + toString($count) + ' orders, total: ' + toString($Total);
  set $Result = 'Processed ' + toString($count) + ' orders';
  return $Result;
end;
```

## UI Component Mapping

### Oracle Forms Items to Mendix Widgets

| Oracle Forms Item | Mendix Widget | MDL Syntax |
|-------------------|---------------|------------|
| Text Item | Text Input | `INPUT 'name' attribute attr` |
| Display Item | Text | `text 'content'` |
| Check Box | Check Box | `checkbox 'name' attribute attr` |
| Radio Group | Radio Buttons | `RADIO 'name' attribute attr` |
| List Item (LOV) | Drop-down | `dropdown 'name' attribute attr` |
| Push Button | Button | `button 'name' on CLICK ...` |
| Tab Canvas | Tab Container | `TAB_CONTAINER (TAB 'name' (...))` |

### Oracle Forms Blocks to Mendix DataViews

**Oracle Forms Block → Mendix DataView:**
```mdl
-- Single-record block
dataview source $Customer (
  INPUT 'Code' attribute CustomerCode,
  INPUT 'Name' attribute CustomerName
)

-- Multi-record block (tabular)
datagrid source $OrderList (
  column 'OrderNumber' attribute OrderNumber,
  column 'OrderDate' attribute OrderDate,
  column 'Amount' attribute TotalAmount
)
```

### Master-Detail Pattern

**Oracle Forms Master-Detail → Mendix:**
```mdl
-- check-skip: shorthand pseudo-syntax sketch of the migrated page, not runnable
-- MDL. See create-page / overview-pages for real page syntax.
create page MyModule.CustomerOrders
layout Atlas_Default
title 'Customer Orders'
parameter $Customer: MyModule.Customer
widgets (
  -- Master block
  dataview source $Customer (
    INPUT 'Code' attribute CustomerCode readonly,
    INPUT 'Name' attribute CustomerName readonly
  ),

  -- Detail block (orders for this customer)
  datagrid 'OrderGrid' source database MyModule.Order
    where '[MyModule.Order_Customer = $Customer]' (
    column 'OrderNumber' attribute OrderNumber,
    column 'OrderDate' attribute OrderDate,
    column 'Amount' attribute TotalAmount
  )
);
/
```

## Triggers to Microflows

### Common Trigger Mappings

| Oracle Forms Trigger | Mendix Implementation |
|---------------------|----------------------|
| `when-NEW-FORM-INSTANCE` | Page load microflow (data source) |
| `when-NEW-RECORD-INSTANCE` | OnChange microflow on data source |
| `when-VALIDATE-item` | OnChange microflow or validation in save |
| `when-VALIDATE-RECORD` | Validation microflow before save |
| `post-query` | Microflow data source with transformation |
| `PRE-insert` / `PRE-update` | Before commit event handler |
| `post-insert` / `post-update` | After commit event handler |
| `key-commit` | Save button action microflow |
| `on-error` | `on error begin ... end error` blocks |

## Migration Checklist

Before starting migration:
- [ ] Export Oracle Forms XML (.xml) or use Forms2XML utility
- [ ] Document all triggers and their purposes
- [ ] Map database tables to Mendix entities
- [ ] Identify LOVs and map to enumerations
- [ ] Check for structural keyword conflicts (Create, Delete, Begin, End, Return)

During migration:
- [ ] Create entities first (Phase 1)
- [ ] Create microflows second (Phase 2)
- [ ] Create pages last (Phase 3) - they can reference microflows
- [ ] Test validation patterns thoroughly
- [ ] Use `validation feedback $entity/attribute message 'message'` for all validations

After migration:
- [ ] Run `mxcli check script.mdl -p app.mpr --references`
- [ ] Open in Mendix Studio Pro to verify
- [ ] Test all validation scenarios
- [ ] Verify master-detail relationships work correctly

## Common Migration Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Parse error: mismatched input 'Create'" | Structural keyword as attribute | Use `"create"` (quoted) or rename |
| "microflow not found" | Referenced before created | Move microflow definition before page |
| "page not found" | Referenced before created | Move page definition earlier |
| "VALIDATION FEEDBACK requires attribute" | Missing attribute path | Use `validation feedback $entity/attribute message 'msg'` |
| CE0117 "Error in expression" | Missing module prefix | Use fully qualified names |

## Tips for Success

1. **Plan attribute names carefully**: Most words work unquoted; only structural keywords (`create`, `delete`, `begin`, `end`, `return`) need quoting
2. **Organize scripts by phase**: Entities → Microflows → Pages
3. **Test incrementally**: Migrate one form at a time
4. **Keep validation close to logic**: Embed validation in save microflows
5. **Document mappings**: Track which Oracle Forms items map to which Mendix elements
6. **Use meaningful names**: `ACT_Customer_Save` not `SUB_SAVE`
7. **Leverage CRUD generation**: Use `/create-crud` skill for standard operations

## Related Skills

- [/write-microflows](../write-microflows/SKILL.md) - Detailed microflow syntax
- [/create-crud](./create-crud.md) - Generate CRUD operations
- [/overview-pages](../overview-pages/SKILL.md) - Page building patterns
- [/master-detail-pages](../master-detail-pages/SKILL.md) - Master-detail layouts
