---
name: cheatsheet-variables
description: "One-page reference for declaring and assigning variables in MDL microflows — every type, with the exact syntax. Use when writing a `declare` and unsure of the spelling, or when a declaration error needs fixing fast."
---

# MDL Variable Cheatsheet

Quick reference for variable declarations in MDL microflows.

## Declaration Syntax

| Type | Syntax | Example |
|------|--------|---------|
| String | `declare $name string = 'value';` | `declare $message string = '';` |
| Integer | `declare $name integer = 0;` | `declare $count integer = 0;` |
| Boolean | `declare $name boolean = true;` | `declare $IsValid boolean = true;` |
| Decimal | `declare $name decimal = 0.0;` | `declare $Amount decimal = 0;` |
| DateTime | `declare $name datetime = [%CurrentDateTime%];` | `declare $Now datetime = [%CurrentDateTime%];` |
| Enumeration | `declare $name Enumeration(Module.Enum) = Module.Enum.Value;` | `declare $s Enumeration(Sales.Status) = Sales.Status.Open;` |
| Object (Entity) | **Do not declare** — use a parameter, `retrieve`, `create`, or loop iterator | `$Customer = create Sales.Customer (Name = $n);` |
| List | **Do not declare** — use a parameter, `retrieve`, or `create list` | `$Orders = create list of Sales.Order;` |

## Key Rules

1. **Primitives** (String/Integer/Long/Decimal/Boolean/DateTime/Enumeration): Use `declare $var type = value;` — these are the *only* types `declare` (a Create Variable activity) accepts.
2. **Objects (entities)**: Never `declare` an object. Mendix forbids the Create Variable activity from holding an object (CE0053/CE0038, plus CE7247 on a later `set`; flagged as **MDL043** by `mxcli check`) — bare *or* initialized. Get the object from a microflow parameter, a `retrieve … first`, `$var = create Module.Entity(...)`, or a loop iterator. There is no "empty object variable" and no aliasing activity — reuse the variable you already have.
3. **Lists**: Never `declare` a list — same Create Variable restriction (CE0053/CE0038, flagged as **MDL040**). Get the list from a microflow parameter, a `retrieve`, or `$var = create list of Module.Entity;`
4. **SET requires DECLARE**: Always declare primitive variables before using SET.
5. **Parameters are pre-declared**: Microflow parameters don't need DECLARE (and a parameter *may* be an object/list type — that restriction is only on `declare`).

## Common Mistakes

### Object (Entity) "Declaration" — there is no such thing

```mdl
-- WRONG: declaring an object — Mendix rejects it (CE0053/CE0038, MDL043)
declare $Product Module.Product;            -- bare form is invalid
declare $Product Module.Product = $In;      -- aliasing a parameter is invalid
declare $Product as Module.Product;         -- the AS keyword is also a parse error

-- CORRECT: get the object from a source that produces one
$Product = create Module.Product (Name = $n);     -- create
retrieve $Product from Module.Product where Code = $c first;  -- retrieve
-- or accept it as a parameter, or use a loop iterator: loop $Product in $Products ...
```

### SET Without DECLARE

```mdl
-- WRONG: Variable not declared
if $value > 10 then
  set $message = 'High';  -- ERROR!
end if;

-- CORRECT: Declare first
declare $message string = '';
if $value > 10 then
  set $message = 'High';
end if;
```

### Lists (never declared)

```mdl
-- WRONG: declaring a list — Mendix rejects it (CE0053/CE0038, MDL040)
declare $Items list of Module.Item = empty;

-- CORRECT: build the list without declare
$Items = create list of Module.Item;          -- empty list to accumulate into
retrieve $Items from Module.Item where ...;    -- or populate from the database
-- or accept it as a parameter: create microflow M.Process ($Items: list of Module.Item) ...
```

## Special Values

| Value | Usage |
|-------|-------|
| `empty` | Null/empty value for any type |
| `[%CurrentDateTime%]` | Current date and time |
| `[%CurrentUser%]` | Currently logged in user object |
| `true` / `false` | Boolean literals |

## Parameter vs Variable

```mdl
mdl 1;
create microflow Module.Example (
  $Input: string,              -- Parameter: auto-declared
  $entity: Module.Customer     -- Parameter: auto-declared
)
returns boolean
begin
  -- Parameters $Input and $Entity are already available

  declare $Result boolean = true;  -- Local primitive: must declare
  -- Need a local object? Don't declare it — create/retrieve it:
  $Order = create Module.Order (Reference = $Input);  -- or retrieve … first

  return $Result;
end;
```

## Variable Scope

- Parameters: Available throughout the microflow
- DECLARE variables: Available from declaration point forward
- Loop variables: Only available inside the loop body

```mdl
loop $item in $ItemList
begin
  -- $Item is available here (derived from list type)
  set $count = $count + 1;
end loop;
-- $Item is NOT available here
```
