---
name: resolve-forward-references
description: "Order MDL statements so that every reference resolves — execution is sequential and immediate, so a document must exist before anything points at it. Use when a script fails on a reference to something defined later in the same file."
---

# Resolving Forward References in MDL Scripts

## Why Forward References Fail

MDL script execution is **sequential and immediate** — each `CREATE` statement commits
its document to the project database before the next statement runs. When a document is
being built, all its references (snippets, pages, microflows) are resolved against the
database at that moment. A reference to something defined *later in the same script* fails
because it is not in the database yet.

```
Error: snippet not found: MyModule.NavMenu
```

This applies to the following reference types:

| Reference | In | Fails when |
|---|---|---|
| `snippetcall` | page / snippet | snippet created after the page |
| `show page` in action | page / snippet | page created after the page that references it |
| `SHOW PAGE` | microflow | page created after the microflow |
| `call microflow` | microflow | callee microflow created after the caller (in the same script, `exec` resolves the call against the project/backend, not later same-script definitions — so order the callee first) |

> **Note:** `SHOW PAGE` inside a microflow body resolves the page reference at
> microflow-creation time, not at invocation time. If the target page doesn't exist yet,
> the microflow creation fails.

---

## The Placeholder Pattern

The standard workaround is a three-step sequence:

1. **Create a minimal placeholder** for the document that will be referenced.
2. **Create all documents that reference it.** They bind to the placeholder's ID.
3. **Fill in the placeholder** using `CREATE OR MODIFY` or `ALTER` — both preserve the
   original ID so existing bindings remain valid.

> **Critical:** Never use `CREATE OR REPLACE` for the fill-in step. `OR REPLACE` deletes
> the placeholder and creates a new document with a different ID. Every page or snippet
> that references the placeholder immediately becomes a dangling reference.

---

## Pattern 1 — Shared Navigation Snippet (most common)

A navigation snippet contains `show page` buttons (references pages) and pages include
the snippet via `snippetcall` (references the snippet). Both sides reference each other.

```sql
mdl 1;
-- Step 1: placeholder snippet (minimal valid content)
create snippet MyModule.NavMenu
{
  layoutgrid g { row { column (desktopwidth: 12) {
    dynamictext loading (content: 'Loading...')
  }}}
};

-- Step 2: pages that embed the snippet (snippet already exists → resolves OK)
create page MyModule.Customer_Overview
(
  title: 'Customers',
  layout: Atlas_Core.Atlas_Default
)
{
  layoutgrid g { row {
    column (desktopwidth: 3) {
      snippetcall nav (snippet: MyModule.NavMenu)
    }
    column (desktopwidth: 9) {
      datagrid dg (datasource: database MyModule.Customer) { }
    }
  }}
};

create page MyModule.Order_Overview
(
  title: 'Orders',
  layout: Atlas_Core.Atlas_Default
)
{
  layoutgrid g { row {
    column (desktopwidth: 3) {
      snippetcall nav (snippet: MyModule.NavMenu)
    }
    column (desktopwidth: 9) {
      datagrid dg (datasource: database MyModule.Order) { }
    }
  }}
};

-- Step 3: fill in the snippet with real content (pages now exist → show page resolves OK)
-- Use CREATE OR MODIFY (preserves ID) or ALTER SNIPPET (in-place)
create or modify snippet MyModule.NavMenu
{
  layoutgrid g { row { column (desktopwidth: 12) {
    actionbutton btnCustomers (
      caption: 'Customers',
      action: show page MyModule.Customer_Overview
    )
    actionbutton btnOrders (
      caption: 'Orders',
      action: show page MyModule.Order_Overview
    )
  }}}
};
```

---

## Pattern 2 — Page References Another Page (new/edit from overview)

An overview page has a New button that opens a NewEdit page via `show page`. The NewEdit
page must exist before the overview can reference it.

```sql
mdl 1;
-- Solution: declare the target page first (even if empty), then the referencing page

create page MyModule.Customer_NewEdit
(
  params: ( $Customer: MyModule.Customer ),
  title: 'Edit Customer',
  layout: Atlas_Core.PopupLayout
)
{
  layoutgrid g { row { column (desktopwidth: 12) {
    dataview dv (datasource: $Customer) {
      textbox txtName (label: 'Name', attribute: Name)
    }
    actionbutton btnSave (caption: 'Save', action: save changes)
    actionbutton btnCancel (caption: 'Cancel', action: cancel changes)
  }}}
};

-- Now the overview can safely reference the NewEdit page
create page MyModule.Customer_Overview
(
  title: 'Customers',
  layout: Atlas_Core.Atlas_Default
)
{
  layoutgrid g { row { column (desktopwidth: 12) {
    actionbutton btnNew (
      caption: 'New',
      action: call microflow MyModule.ACT_Customer_New
    )
    datagrid dg (datasource: database MyModule.Customer) {
      column (caption: 'Name', attribute: Name)
    }
  }}}
};
```

For simple cases, reordering declarations is sufficient and no placeholder is needed.

---

## Pattern 3 — Microflow References a Page Not Yet Created

```sql
mdl 1;
-- If the page is defined later in the script, create a placeholder or reorder.
-- Easiest fix: declare the page before the microflow that shows it.

-- Page first
create page MyModule.Order_Detail
(
  params: ( $Order: MyModule.Order ),
  title: 'Order Detail',
  layout: Atlas_Core.Atlas_Default
)
{
  layoutgrid g { row { column (desktopwidth: 12) {
    dataview dv (datasource: $Order) {
      textbox txtID (label: 'Order ID', attribute: OrderID)
    }
  }}}
};

-- Microflow after the page it references
create microflow MyModule.ACT_OpenOrder ($Order: MyModule.Order)
begin
  @position(200,200)
  show page MyModule.Order_Detail (Order = $Order);
  @position(400,200) return;
end;
```

---

## Ordering Rules for Dependency-Free Scripts

To avoid forward references entirely, follow this declaration order within a script:

```
1. Entities and associations       (no cross-document references)
2. Enumerations and constants      (no cross-document references)
3. Snippets (placeholder if needed)
4. Pages                           (reference snippets + other pages)
5. Snippets (fill-in step, if placeholder was used)
6. Microflows and nanoflows        (reference pages, entities)
7. Navigation                      (references pages)
```

When generating MDL scripts, write sections in this order. Doing so avoids the placeholder
pattern for the majority of scripts.

---

## Choosing Between CREATE OR MODIFY and ALTER SNIPPET

Both preserve the snippet's ID. Use whichever fits:

| Approach | When to use |
|---|---|
| `create or modify snippet` | Rewriting the whole snippet body from scratch |
| `alter snippet` | Inserting or replacing specific widgets within an existing layout |

```sql
mdl 1;
-- ALTER SNIPPET: targeted widget replacement (keeps surrounding structure)
alter snippet MyModule.NavMenu {
  replace loading with {
    actionbutton btnCustomers (
      caption: 'Customers',
      action: show page MyModule.Customer_Overview
    )
  }
};
```

---

## Script Template for a Full CRUD Module

```sql
mdl 1;
-- ============================================================
-- MyModule CRUD scaffold
-- Correct declaration order: snippets → pages → microflows → nav
-- ============================================================

-- 1. Placeholder for shared navigation (will reference pages created below)
create snippet MyModule.AppNav
{
  layoutgrid g { row { column (desktopwidth: 12) {
    dynamictext placeholder (content: '...')
  }}}
};

-- 2. NewEdit page (referenced by Overview's New button)
create page MyModule.Customer_NewEdit
(
  params: ( $Customer: MyModule.Customer ),
  title: 'Edit Customer',
  layout: Atlas_Core.PopupLayout
)
{
  -- ... widgets ...
};

-- 3. Overview page (references NewEdit + NavMenu)
create page MyModule.Customer_Overview
(
  title: 'Customers',
  layout: Atlas_Core.Atlas_Default
)
{
  layoutgrid g { row {
    column (desktopwidth: 3) {
      snippetcall nav (snippet: MyModule.AppNav)
    }
    column (desktopwidth: 9) {
      -- ... datagrid with New button calling ACT_Customer_New ...
    }
  }}
};

-- 4. Fill in navigation (pages now exist)
create or modify snippet MyModule.AppNav
{
  layoutgrid g { row { column (desktopwidth: 12) {
    actionbutton btnCustomers (
      caption: 'Customers',
      action: show page MyModule.Customer_Overview
    )
  }}}
};

-- 5. Microflows (pages already exist)
create microflow MyModule.ACT_Customer_New ()
begin
  $c = create MyModule.Customer ();
  show page MyModule.Customer_NewEdit (Customer = $c);
  return;
end;

-- 6. Navigation (pages already exist). This statement sets the whole profile,
-- its menu included: list every item the menu must keep.
create or modify navigation Responsive
  home page MyModule.Customer_Overview
  {
    menu item 'Customers' ( OnClick: show page MyModule.Customer_Overview )
  };
```

---

## Related Skills

- [Create Page](../create-page/SKILL.md) — Full page syntax reference
- [Overview Pages](../overview-pages/SKILL.md) — Overview + NewEdit page patterns
- [ALTER PAGE/SNIPPET](../alter-page/SKILL.md) — In-place snippet modification
