---
name: organize-project
description: "Organise documents into folders and move them between folders and modules with MOVE. Use when a module has grown unstructured, when restructuring a project, or when a document is in the wrong place."
---

# Project Organization: Folders and Moving Documents

This skill covers organizing Mendix project documents (pages, microflows, snippets, nanoflows) into folders and moving them between folders and modules.

## When to Use This Skill

Use this skill when:
- Organizing documents into folder hierarchies within a module
- Moving documents between folders
- Moving documents between modules
- Restructuring a project for better maintainability
- Setting up folder conventions for a new module

## Folder Conventions

Organize by **functional grouping** — keep all artifacts for a feature together, not separated by document type. This way, a developer working on "Customer" finds everything in one place: pages, microflows, snippets, and validation logic.

Recommended folder structure within a module:

```
CRM/
├── Customer/
│   ├── Customer_Overview        -- Overview page
│   ├── Customer_NewEdit         -- Edit page
│   ├── CustomerCard             -- Snippet
│   ├── ACT_Customer_Save        -- Save microflow
│   ├── ACT_Customer_Delete      -- Delete microflow
│   ├── ACT_Customer_New         -- New microflow
│   ├── VAL_Customer             -- Validation microflow
│   └── DS_Customer_Filter       -- Data source microflow
├── Order/
│   ├── Order_Overview
│   ├── Order_NewEdit
│   ├── ACT_Order_Save
│   └── VAL_Order
└── Shared/                      -- Cross-cutting concerns
    ├── SUB_SendNotification
    └── Navigation_Snippet
```

**Why functional grouping over type grouping:**
- All related artifacts are in one place — easier to navigate and review
- Adding or removing a feature is a single folder operation
- Naming prefixes (ACT_, VAL_, SUB_, DS_) already indicate document type
- Mirrors how developers think: "I'm working on Customer" not "I'm working on microflows"

Adapt to your project's conventions. The key is consistency across modules.

## Creating Documents in Folders

### Microflows

Use the `folder` keyword after the return type, before `begin`:

```mdl
mdl 1;
create microflow MyModule.ACT_ProcessOrder ($Order: MyModule.Order)
returns boolean as $success
folder 'Order'
begin
  commit $Order;
  return true;
end;
```

### Pages

Use the `folder` property inside the page properties:

```sql
mdl 1;
create page MyModule.Customer_Overview folder 'Customer'
(
  title: 'Customer Overview',
  layout: Atlas_Core.Atlas_Default
)
{
  -- widgets
};
```

### Snippets

```sql
mdl 1;
create snippet MyModule.CustomerCard folder 'Customer'
{
  -- widgets
};
```

### Nested Folders

Use `/` to create nested folder paths. Missing folders are created automatically:

```mdl
mdl 1;
-- Creates 'Order', then 'Order/Batch' if they don't exist
create microflow MyModule.ACT_BatchProcess ($list: list of MyModule.Order)
folder 'Order/Batch'
begin
  loop $Order in $list begin
    commit $Order;
  end loop;
  return;
end;
```

## Reading the Layout Back

`list folders` shows the folder layout of a module and what is in each folder.
This is the counterpart to `move`: `move` puts a document somewhere, `list
folders` shows where everything actually is.

```sql
-- One module
list folders in MyModule;

-- Every module in the project
list folders;
```

```
MyModule
  (module root)  [1]
    Microflow ACT_Unfiled
  Api  [0]
  Api/Published  [1]
    ODataService PublicApi
  Support  [1]
    JavaAction Helper

(3 folder(s), 3 document(s))
```

Three things about the output are deliberate:

- **Empty folders are listed** (`Api  [0]`), so the listing is the whole layout
  and can be diffed against an intended one.
- **Documents still at the module root** appear under `(module root)` — what is
  not filed yet is the thing you most want to notice.
- **Ordering is stable**, so a diff between two runs shows only real movement.

Use the CLI's `--json` flag for a row per document (`Module, Folder, Kind, Document`)
when comparing against a checked-in layout.

Do **not** reach for `describe structure` here: it groups by document type at every
depth and never shows which folder a document sits in.

## Moving Documents

The `move` command relocates existing documents between folders and modules.

### Move to a Folder (Same Module)

```mdl
mdl 1;
move page MyModule.CustomerEdit to folder 'Customer';
move microflow MyModule.ACT_ProcessOrder to folder 'Order';
move snippet MyModule.NavigationMenu to folder 'Shared';
move nanoflow MyModule.NAV_OpenCustomer to folder 'Customer';
move enumeration MyModule.OrderStatus to folder 'Shared';
```

### Move to Module Root (Out of Folder)

```mdl
mdl 1;
move page MyModule.CustomerEdit to MyModule;
```

### Move Across Modules

```mdl
mdl 1;
-- Move to another module's root
move page OldModule.CustomerPage to NewModule;

-- Move to a folder in another module
move page OldModule.CustomerPage to folder 'Pages' in NewModule;
```

### Cross-Module Move Warning

Cross-module moves change the qualified name (e.g., `OldModule.CustomerPage` becomes `NewModule.CustomerPage`). This **breaks by-name references** such as:
- Microflows calling `show page OldModule.CustomerPage`
- Other microflows calling `call microflow OldModule.SomeMicroflow`
- Widget actions referencing the old qualified name

**Always check impact before cross-module moves:**

```mdl
mdl 1;
list impact of OldModule.CustomerPage;
-- Review the output, then move if safe:
move page OldModule.CustomerPage to NewModule;
```

## Folder Rules

- Folder names are **case-sensitive**
- Use `/` as separator for nested folders: `'Parent/Child/Grandchild'`
- Folders are **created automatically** if they don't exist
- Moving to a folder that doesn't exist creates it
- Empty folders are preserved in the project

## Supported Document Types

`move` accepts **every top-level document type**, spelled the way `describe`
spells it:

| Group | Types |
|-------|-------|
| Pages | `page`, `snippet`, `building block`, `layout`, `menu` |
| Logic | `microflow`, `nanoflow`, `workflow`, `task queue`, `scheduled event` |
| Domain | `enumeration`, `constant`, `regular expression` |
| Mappings | `json structure`, `import mapping`, `export mapping` |
| Code | `java action`, `javascript action`, `database connection`, `data transformer` |
| Resources | `image collection`, `icon collection` |
| Integration | `consumed rest service`, `published rest service`, `consumed odata service`, `published odata service`, `business event service` |
| AI | `model`, `agent`, `knowledge base`, `consumed mcp service` |

`move entity` is the exception: an entity lives inside a domain model, so it
moves between **modules** only, never into a folder.

If the named document turns out to be a different type, the statement is refused
and the error names what it really is — `move task queue Mod.JSON_Order` reports that
`Mod.JSON_Order` is a json structure.

### FOLDER on Create

Every document type takes a folder clause on `create`, so a document can be
placed in the statement that creates it rather than in a separate `move`. Where
the clause goes depends on the statement's shape:

| Document Type | FOLDER on Create |
|---------------|-----------------|
| Page, Snippet | `folder: 'path'` — a property, inside the parentheses |
| Microflow, Nanoflow | `folder 'path'` — a keyword, before `begin` |
| Enumeration, Constant | `folder 'path'` — a keyword, after the definition |
| Everything else | `folder 'path'` — a keyword, straight after the qualified name |

```mdl
mdl 1;
create import mapping CRM.IMM_Order folder 'Private/Import mappings'
  with json structure CRM.JSON_Order { create CRM.Order { Id = id } };

create task queue CRM.Q_Orders folder 'Private/Queues' ( Parallelism: 3 );

create java action CRM.JA_Sync folder 'Private/Java' () returns string
  as $$return null;$$;
```

**A folder clause on `create or modify` moves an existing document.** It used to
be silently ignored: the statement reported success, the folder was created, and
the document stayed where it was (#932). Omitting the clause leaves placement
alone — it never returns a document to the module root — so adding a folder to a
script is safe and removing it is a no-op.

`describe` emits the clause, so a description replays into the same folder
rather than into the module root.

## Example: Reorganize a Module

```mdl
mdl 1;
-- Group all Customer artifacts together
move page CRM.Customer_Overview to folder 'Customer';
move page CRM.Customer_NewEdit to folder 'Customer';
move microflow CRM.ACT_Customer_Save to folder 'Customer';
move microflow CRM.ACT_Customer_Delete to folder 'Customer';
move microflow CRM.ACT_Customer_New to folder 'Customer';
move microflow CRM.VAL_Customer to folder 'Customer';
move snippet CRM.CustomerCard to folder 'Customer';

-- Group all Order artifacts together
move page CRM.Order_Overview to folder 'Order';
move page CRM.Order_NewEdit to folder 'Order';
move microflow CRM.ACT_Order_Save to folder 'Order';
move microflow CRM.ACT_Order_Process to folder 'Order/Processing';

-- Move shared artifacts to a Shared folder or common module
list impact of CRM.Header_Snippet;
move snippet CRM.Header_Snippet to folder 'Shared' in Common;

-- Move entity to different module
list impact of CRM.Customer;
move entity CRM.Customer to CustomerModule;

-- Move enumeration to different module
move enumeration CRM.OrderStatus to SharedModule;
```

## Moving Folders

Use `move folder` to reorganize folders. Syntax matches document moves: `Module.FolderName`.

```sql
mdl 1;
-- Move a folder into another folder
move folder MyModule.Resources to folder 'Archive';

-- Move a nested folder (use double quotes for paths with /)
move folder MyModule."Orders/Archive" to MyModule;

-- Move a folder to a different module
move folder MyModule.SharedWidgets to CommonModule;

-- Move a folder into a folder in another module
move folder MyModule.Templates to folder 'Shared' in CommonModule;
```

## Deleting Folders

Use `drop folder` to remove empty folders. The folder must not contain any documents or sub-folders.

```sql
mdl 1;
-- Drop an empty folder
drop folder 'OldPages' in MyModule;

-- Drop a nested folder (only the leaf is removed)
drop folder 'Orders/Archive' in MyModule;

-- Move contents out first, then drop
move microflow MyModule.ACT_Process to MyModule;
drop folder 'Processing' in MyModule;
```

## Validation Checklist

- [ ] Folder paths use `/` separator (not `\`)
- [ ] FOLDER keyword placement is correct (before BEGIN for microflows, inside properties for pages)
- [ ] Cross-module moves: checked impact with `list impact of` first
- [ ] Folder naming is consistent across modules
- [ ] DROP FOLDER: verify folder is empty before dropping
- [ ] After a batch of moves: `list folders in MyModule` to confirm the layout
