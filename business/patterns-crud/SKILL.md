---
name: patterns-crud
description: "Standard Create/Read/Update/Delete microflow patterns with the naming conventions that go with them. Use when writing the action microflows behind page buttons rather than looking up individual syntax."
---

# CRUD Action Patterns

Standard patterns for Create, Read, Update, Delete operations on entities.

## Naming Conventions

| Prefix | Purpose | Example |
|--------|---------|---------|
| `ACT_` | Action microflow (page button) | `ACT_Customer_Save` |
| `VAL_` | Validation microflow | `VAL_Customer_Save` |
| `DS_` | Data source microflow | `DS_Customer_GetAll` |
| `SUB_` | Sub-microflow (internal) | `SUB_Customer_SendEmail` |

## Save Pattern (Create/Update)

Used for Save buttons on NewEdit pages.

```mdl
mdl 1;
/**
 * Save action for Customer NewEdit page
 * Validates, commits, and closes the page
 *
 * @param $Customer The customer to save
 * @returns true if saved successfully
 */
create microflow Module.ACT_Customer_Save (
  $Customer: Module.Customer
)
returns boolean
begin
  -- Validate first
  $IsValid = call microflow Module.VAL_Customer_Save(Customer = $Customer);

  if $IsValid then
    commit $Customer;
    close page;
  end if;

  return $IsValid;
end;
```

## Validation Pattern

Companion validation microflow for Save actions.

```mdl
mdl 1;
/**
 * Validate Customer before save
 *
 * @param $Customer The customer to validate
 * @returns true if valid
 */
create microflow Module.VAL_Customer_Save (
  $Customer: Module.Customer
)
returns boolean
begin
  declare $IsValid boolean = true;

  -- Required field validation
  if $Customer/Name = empty then
    validation feedback $Customer/Name message 'Name is required';
    set $IsValid = false;
  end if;

  if $Customer/Email = empty then
    validation feedback $Customer/Email message 'Email is required';
    set $IsValid = false;
  end if;

  -- Business rule validation
  if $Customer/CreditLimit < 0 then
    validation feedback $Customer/CreditLimit message 'Credit limit cannot be negative';
    set $IsValid = false;
  end if;

  return $IsValid;
end;
```

## Delete Pattern

Used for Delete buttons with confirmation.

```mdl
mdl 1;
/**
 * Delete a customer
 * Called after user confirms deletion
 *
 * @param $Customer The customer to delete
 * @returns true if deleted
 */
create microflow Module.ACT_Customer_Delete (
  $Customer: Module.Customer
)
returns boolean
begin
  delete $Customer;
  close page;
  return true;
end;
```

## Cancel Pattern

Used for Cancel buttons (discard changes).

```mdl
mdl 1;
/**
 * Cancel editing and close page
 * Discards uncommitted changes
 *
 * @param $Customer The customer being edited
 * @returns true
 */
create microflow Module.ACT_Customer_Cancel (
  $Customer: Module.Customer
)
returns boolean
begin
  rollback $Customer;
  close page;
  return true;
end;
```

## Create New Pattern

Used for New/Add buttons on overview pages.

```mdl
mdl 1;
/**
 * Create new customer and open edit page
 *
 * @returns true
 */
create microflow Module.ACT_Customer_New ()
returns boolean
begin
  $NewCustomer = create Module.Customer (
    IsActive = true,
    CreatedDate = [%CurrentDateTime%]
  );

  show page Module.Customer_NewEdit (Customer = $NewCustomer);
  return true;
end;
```

## Data Source Pattern

Used for data grid/list view sources.

```mdl
mdl 1;
/**
 * Get all active customers
 * Used as data source for Customer overview
 *
 * @returns List of active customers
 */
create microflow Module.DS_Customer_GetActive ()
returns list of Module.Customer
begin
  -- retrieve creates the list variable directly — never declare a list first
  retrieve $Customers from Module.Customer
    where IsActive = true;

  return $Customers;
end;
```

## Edit Pattern

Open existing entity for editing.

```mdl
mdl 1;
/**
 * Open customer for editing
 *
 * @param $Customer The customer to edit
 * @returns true
 */
create microflow Module.ACT_Customer_Edit (
  $Customer: Module.Customer
)
returns boolean
begin
  show page Module.Customer_NewEdit (Customer = $Customer);
  return true;
end;
```

## Complete CRUD Set

For a typical entity, create these microflows:

| Microflow | Purpose | Parameters |
|-----------|---------|------------|
| `ACT_Entity_New` | Create new | None |
| `ACT_Entity_Edit` | Open for edit | `$entity` |
| `ACT_Entity_Save` | Save changes | `$entity` |
| `VAL_Entity_Save` | Validate | `$entity` |
| `ACT_Entity_Delete` | Delete | `$entity` |
| `ACT_Entity_Cancel` | Cancel edit | `$entity` |
| `DS_Entity_GetAll` | List all | None |

## Best Practices

1. **Always validate before commit**: Call VAL_ microflow in ACT_Save
2. **Events are on by default**: a bare `commit $entity` triggers the event handlers; write `commit $entity without events` only to skip them
3. **Close page on success**: Use `close page` after successful save/delete
4. **Rollback on cancel**: Use `rollback $entity` to discard changes
5. **Initialize defaults**: Set default values in ACT_New microflow
6. **Return Boolean**: All action microflows should return success status
