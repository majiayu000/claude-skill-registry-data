---
name: mdl-entities
description: "Complete syntax reference for entities, attributes and associations — every entity kind, attribute type, and association form. Use when writing or altering a domain model and the exact spelling matters."
---

# MDL Entity Syntax Reference

Complete syntax reference for creating entities, attributes, and associations.

## Entity Types

| Type | Keyword | Stored in DB | Use Case |
|------|---------|--------------|----------|
| Persistent | `create persistent entity` | Yes | Business data |
| Non-Persistent | `create non-persistent entity` | No | Temporary/view data |
| View | `create view entity` | No (OQL query) | Aggregated/computed data |

## Persistent Entity

```mdl
mdl 1;
/**
 * Customer entity for storing customer data
 */
create persistent entity Module.Customer (
  -- String attributes
  Name: string(100) not null,
  Email: string(200),
  Code: string(20) unique,

  -- Numeric attributes
  Age: integer,
  CreditLimit: decimal,

  -- Boolean
  IsActive: boolean default true,

  -- Date/Time
  BirthDate: datetime,   -- there is no date-only type; `date` is refused
  -- Use autocreateddate (not datetime) to record when the object was created.
  -- 'CreatedDate' as a plain datetime triggers lint error MDL020.
  CreatedDate: autocreateddate,

  -- Enumeration
  status: Module.CustomerStatus default Active,

  -- Auto-number (REQUIRES a seed via `default N` — without it the build fails
  -- CE7247 "Value cannot be empty")
  CustomerNumber: autonumber default 1
);
```

## Non-Persistent Entity

Used for temporary data, form parameters, or calculated values.

```mdl
mdl 1;
/**
 * Search parameters for customer search form
 */
create non-persistent entity Module.CustomerSearchParams (
  SearchName: string(100),
  SearchEmail: string(200),
  MinCreditLimit: decimal,
  IncludeInactive: boolean default false
);
```

## Attribute Types

| Type | Syntax | Example |
|------|--------|---------|
| String | `Name: string(length)` | `Name: string(100)` |
| Integer | `Name: integer` | `count: integer` |
| Long | `Name: long` | `BigNumber: long` |
| Decimal | `Name: decimal` | `Amount: decimal` |
| Boolean | `Name: boolean` | `IsActive: boolean` |
| DateTime | `Name: datetime` | `CreatedAt: datetime` |
| Enumeration | `Name: Module.EnumName` | `status: Module.Status` |
| AutoNumber | `Name: autonumber default 1` | `Code: autonumber default 1` (seed required) |
| Binary | `Name: binary` | `FileData: binary` |
| Hashed String | `Name: hashedstring` | `password: hashedstring` |

## Attribute Modifiers

| Modifier | Meaning | Example |
|----------|---------|---------|
| `not null` | Required field | `Name: string(100) not null` |
| `unique` | Unique constraint | `Code: string(20) unique` |
| `default value` | Default value | `IsActive: boolean default true` |

**Note:** Boolean attributes auto-default to `false` when no `default` is specified.

## Generalization (Inheritance)

**CRITICAL: EXTENDS goes BEFORE the opening parenthesis, not after!**

```mdl
mdl 1;
/**
 * Base entity
 */
create persistent entity Module.Person (
  PersonName: string(100) not null,
  Email: string(200)
);

/**
 * Customer extends Person - EXTENDS before (
 */
create persistent entity Module.Customer extends Module.Person (
  CustomerCode: string(20),
  CreditLimit: decimal
);
```

Common parent entities for file/image storage:
```mdl
mdl 1;
-- Image entity (inherits Name, Size, Contents, thumbnail)
create persistent entity Module.ProductPhoto extends System.Image (
  PhotoCaption: string(200),
  SortOrder: integer default 0
);

-- File document (inherits Name, Size, Contents)
create persistent entity Module.Attachment extends System.FileDocument (
  AttachmentDescription: string(500)
);
```

**Wrong** (parse error):
```mdl
-- EXTENDS after ) = parse error!
create persistent entity Module.Photo (
  PhotoCaption: string(200)
) extends System.Image;
```

## Associations

### Reference (Many-to-One)

```mdl
mdl 1;
/**
 * Order belongs to one Customer
 */
create association Module.Order_Customer
from Module.Order to Module.Customer
type reference;
```

Direction: `from` the entity that holds the foreign key (the "many" / child side) `to`
the entity being referenced (the "one" / parent side). Name convention is `Child_Parent`.

### Reference Set (Many-to-Many)

```mdl
mdl 1;
/**
 * Product can be in many Categories
 * Category can have many Products
 */
create association Module.Product_Category
from Module.Product to Module.Category
type ReferenceSet
owner both;
```

### Association with Delete Behavior

```mdl
mdl 1;
/**
 * Delete orders when their customer is deleted
 */
create association Module.Order_Customer
from Module.Order to Module.Customer
type reference
on delete cascade;
```

Delete behaviors (applied to the referenced `to` entity):
- `on delete cascade` - delete the referencing objects too (cascade)
- `on delete set null` - delete, nullify the reference (default)
- `on delete restrict` - only delete when nothing references it

## Enumerations

```mdl
mdl 1;
/**
 * Order status values
 */
create enumeration Module.OrderStatus (
  Draft 'Draft',
  Pending 'Pending',
  Approved 'Approved',
  Shipped 'Shipped',
  Delivered 'Delivered',
  Cancelled 'Cancelled'
);
```

## View Entity (OQL)

```mdl
mdl 1;
/**
 * Monthly sales summary by customer
 */
create view entity Module.CustomerSalesSummary (
  CustomerName: string(100),
  TotalOrders: integer,
  TotalAmount: decimal,
  LastOrderDate: datetime
)
as
  select
    c.Name as CustomerName,
    count(o.OrderID) as TotalOrders,
    sum(o.Amount) as TotalAmount,
    max(o.OrderDate) as LastOrderDate
  from Module.Customer c
  left join c/Module.Order_Customer/Module.Order o
  GROUP by c.Name;
```

**Derived string columns must be `string(200)`.** A plain pass-through column
(`c.Name as CustomerName`) inherits its source attribute's length, so declaring
`string(100)` above is fine. But a **derived** string column — `cast(x as
string)`, a string-returning `CASE`, or a string expression — is normalized by
Mendix to the platform default length **`string(200)`**. Declaring any other
length (`string(30)`, unlimited, …) passes `mxcli check`'s parser but fails the
MxBuild consistency check with **CE6770 "View Entity is out of sync with the OQL
Query."** `mxcli check` catches this pre-build as **MDL031** with a suggested
fix:

```mdl
mdl 1;
create view entity Module.TicketLabel (
  StatusLabel: string(200)          -- derived → must be 200, not string(30)
) as
  select cast(t.Status as string) as StatusLabel from Module.Ticket t;
```

## Entity with Index

```mdl
mdl 1;
/**
 * Product with search index
 */
create persistent entity Module.Product (
  Code: string(20) not null,
  Name: string(100) not null,
  Category: string(50),
  Price: decimal
)
index (Code)
index (Category);
```

> A Mendix index has **no name** — its columns, in order and direction, are its
> identity. A name is accepted (`index idx_code on (Code)`) but not stored, so
> `check` warns (MDL-IDX01), `describe` prints the index back as `index (Code)`,
> and `drop index idx_code` cannot find it. Write indexes anonymously; drop one
> by its columns: `alter entity Module.Product drop index (Code)`. Multi-column
> indexes list the columns in order: `index (Row, Col desc)`.

## Complete Domain Model Example

```mdl
mdl 1;
-- Enumeration
create enumeration Shop.OrderStatus (
  Draft 'Draft',
  Confirmed 'Confirmed',
  Shipped 'Shipped',
  Delivered 'Delivered'
);

-- Customer entity
create persistent entity Shop.Customer (
  Name: string(100) not null,
  Email: string(200) not null unique,
  Phone: string(20),
  IsActive: boolean default true,
  CreatedDate: autocreateddate
);

-- Product entity
create persistent entity Shop.Product (
  Code: string(20) not null unique,
  Name: string(100) not null,
  description: string(500),
  Price: decimal not null,
  Stock: integer default 0,
  IsAvailable: boolean default true
);

-- Order entity
create persistent entity Shop.Order (
  OrderNumber: autonumber default 1,
  OrderDate: datetime not null,
  status: Shop.OrderStatus default Draft,
  TotalAmount: decimal,
  Notes: string(500)
);

-- Order line entity
create persistent entity Shop.OrderLine (
  Quantity: integer not null,
  UnitPrice: decimal not null,
  LineTotal: decimal
);

-- Associations
create association Shop.Order_Customer
from Shop.Order to Shop.Customer
type reference;

create association Shop.OrderLine_Order
from Shop.OrderLine to Shop.Order
type reference
on delete cascade;

create association Shop.OrderLine_Product
from Shop.OrderLine to Shop.Product
type reference;
```

## Changing an Existing Domain Model

Choose the mode by who owns the entity ([choose-edit-mode](../choose-edit-mode/SKILL.md)).
An entity, association or enumeration authored in Studio Pro is changed with `alter`,
not by re-running `describe` output:

```mdl
mdl 1;
alter entity Shop.Order add attribute Note: string(200);
alter association Shop.Order_Customer set on delete set null;
alter enumeration Shop.OrderStatus add value Cancelled caption 'Cancelled';
```

Re-running `create or modify` from `describe` on a Studio Pro association has flipped
its storage from table to column, which is a schema change. Run `mxcli diff` first: it
runs the script on a scratch copy and lists every unit exec would write. Never `drop` and re-create an entity to change it: the new entity has a new
identity, and the runtime drops the old table and its rows.

## Quick Reference

### Entity Creation
```mdl
create persistent entity Module.Name (attributes);
create non-persistent entity Module.Name (attributes);
create view entity Module.Name (attributes) as select ...;
```

### Attribute Syntax
```mdl
attributename: type [(length)] [not null] [unique] [default value]
```

### Association Syntax
```mdl
create association Module.Child_Parent
from Module.ChildEntity to Module.ParentEntity
[type reference | ReferenceSet]
[owner default | both]
[storage column | table]
[on delete cascade | restrict | set null [error message '...']];
```

Every clause is optional; unstated means `type Reference owner Default storage column
on delete set null`. `describe` prints only the clauses that differ, so a table
association always shows `storage table`.

### Enumeration Syntax
```mdl
mdl 1;
create enumeration Module.Name (
  Value1 'Caption1',
  Value2 'Caption2'
);

-- Optionally place the enumeration in a module folder:
create enumeration Module.Currency (
  USD 'US Dollar',
  EUR 'Euro'
) FOLDER 'Shared';
-- Or move an existing one:  move enumeration Module.Currency to folder 'Shared';
```
