---
name: java-actions
description: "Create and call custom Java actions — extending Mendix with server-side Java, and invoking those actions from microflows in MDL. Use when logic needs a Java library, an algorithm microflows cannot express, or an integration only available in Java."
---

# Mendix Java Actions Skill

This skill provides comprehensive guidance for creating and using custom Java actions in Mendix projects.

## Reference files

`SKILL.md` covers declaring a Java action in MDL and calling it from a microflow —
the parts that touch the model. The Java side is next door:

- [`reference/writing-java.md`](reference/writing-java.md) — creating the action
  in Studio Pro, writing the `executeAction` body, the Core API surface you have,
  and the recurring patterns (HTTP calls, file handling, batch work).
- [`reference/best-practices.md`](reference/best-practices.md) — error handling,
  transactions and rollback, logging, threading, security, and performance. Read
  it before shipping a Java action that touches data or an external system.

## When to Use This Skill

Use this skill when:
- You need to extend Mendix with custom Java logic
- Building integrations with external Java libraries
- Implementing complex algorithms not feasible in microflows
- Calling Java actions from MDL microflows
- Debugging Java action calls

## Overview

Java actions allow you to extend Mendix with custom Java code. The workflow is:
1. **Define** the Java action in Studio Pro (parameters, return type)
2. **Implement** the Java code in Eclipse/IDE
3. **Call** the Java action from microflows using MDL

## Part 2.5: Creating Java Actions in MDL

MDL supports defining Java actions with inline Java code using `create java action`.

### Basic Syntax

```mdl
mdl 1;
create java action Module.ActionName(param1: type, param2: type) returns ReturnType
as $$
// java code here
return result;
$$;
```

**`AS $$ ... $$` is mandatory.** The body cannot be omitted even for placeholder or stub actions. Omitting it causes a parse error: `no viable alternative at input '...'`. Use a minimal body if the real implementation is not yet written:

```mdl
mdl 1;
create java action Module.Stub() returns boolean
as $$
return false;
$$;
```

### Type Parameters (Generics)

Type parameters let Java actions accept any entity type dynamically. Use `entity <pEntity>` in a parameter type to declare the type parameter inline. That parameter becomes the **entity type selector** (receives the entity type name, e.g., `'Module.Entity'`). Bare `pEntity` parameters become **parameterized entity** params (receive entity instances, e.g., `$Variable`).

```mdl
mdl 1;
-- ENTITY <pEntity> declares the type parameter; bare pEntity references it
create java action Module.Validate(
  EntityType: entity <pEntity> not null,
  InputObject: pEntity not null
) returns boolean
as $$
return InputObject != null;
$$;
```

Multiple type parameters use separate `entity <...>` declarations:

```mdl
mdl 1;
create java action Module.Transform(
  SourceType: entity <pSource> not null,
  TargetType: entity <pTarget> not null,
  source: pSource not null,
  Target: pTarget not null
) returns boolean
as $$
return true;
$$;
```

A list of type-parameter instances is `list of pEntity` (Studio Pro's "List of <type parameter>").

**A type parameter named after a primitive** (`String`, `Integer`, … — Studio Pro allows it): declare it with `entity <String>`, and refer to it **quoted** — `"String"`, `list of "String"`. Unquoted `String` is always the primitive. DESCRIBE quotes such names for you, so its output re-creates the action.

Type parameter names can be mixed with regular parameter types:

```mdl
mdl 1;
create java action Module.CopyAttributes(
  EntityType: entity <pEntity> not null,
  source: pEntity not null,
  Target: pEntity not null,
  AttributeNames: string not null
) returns boolean
as $$
return true;
$$;
```

When **calling** these actions from microflows, the entity type selector receives the entity type name as a string literal, while instance params receive variables:

```mdl
$Result = call java action Module.CopyAttributes(
  EntityType = 'Module.ProcessResult',
  source = $source,
  Target = $Target,
  AttributeNames = 'Name,Status'
);
```

### EXPOSED AS (Toolbox Visibility)

The `exposed as 'caption' in 'Category'` clause makes the Java action appear as a toolbox item in Studio Pro's microflow editor:

```mdl
mdl 1;
create java action Module.FormatCurrency(
  Amount: decimal not null,
  CurrencyCode: string not null
) returns string
exposed as 'Format Currency' in 'Formatting'
as $$
return String.format("%.2f %s", Amount, CurrencyCode);
$$;
```

Type parameters and EXPOSED AS can be combined:

```mdl
mdl 1;
create java action Module.DeepClone(
  EntityType: entity <pEntity> not null,
  Original: pEntity not null
) returns boolean
exposed as 'Deep Clone Object' in 'Object Utils'
as $$
return true;
$$;
```

#### Toolbox icon and image

The entry also carries four PNG bitmaps — an icon and a larger image, each with
a dark-mode variant. Paths resolve against the directory of the .mdl file, so a
script and its artwork travel together:

```mdl
exposed as 'Format Currency' in 'Formatting'
  icon 'assets/currency-64.png'
  icon dark 'assets/currency-64-dark.png'
  image 'assets/currency-256.png'
```

The icon should be **64x64** and the image **256x192**. A different size is
written with a warning (Studio Pro scales it); a file that is not a PNG is
refused, because Studio Pro renders nothing for one.

#### An omitted clause preserves — it does not clear

This is the rule to remember, and it is not the obvious one:

| You write | What happens |
|---|---|
| `exposed as 'X' in 'Y'` | Caption and category from MDL; **icon and image carried** from what was stored |
| *(no clause at all)* | The whole entry is **preserved**, bitmaps included |
| `not exposed` | The entry is removed |
| `exposed as 'X' in 'Y' drop icon dark` | Clears **one** bitmap; the other three are untouched |

Rewriting a Java action to change its body must not cost it the icon a designer
set in Studio Pro, and saying nothing about the toolbox is not the same as
asking to be taken out of it. Nothing below Studio Pro can see the difference:
an action with no toolbox entry is a valid action, so `mx check` reports 0
errors either way.

`describe java action` reports the bitmaps as comments rather than re-emitting
`icon`/`image` clauses — the clause names a file on disk and the model holds
only bytes. They survive a describe → exec round trip regardless, because an
omitted bitmap is preserved.

**Microflows have this too**, and two of them: `exposed as microflow action` and
`exposed as workflow action`, for Studio Pro's two toolboxes. See
`write-microflows`. Nanoflows and rules do not — only `Microflows$Microflow`
stores a toolbox entry, and the clause is refused on the other two with a
message saying so.

**Studio Pro-authored Java actions:** there is no `alter java action`. Before
re-executing `describe` output for one, note its export level; a `create or modify`
from describe output has changed an action's export level to Public. Check it again after
`exec` (see [choose-edit-mode](../choose-edit-mode/SKILL.md)).

### Supported Parameter Types

| MDL Type | Description |
|----------|-------------|
| `string` | Text value |
| `integer` | Whole number |
| `long` | Large whole number |
| `decimal` | Decimal number |
| `boolean` | True/false |
| `datetime` | Date and time |
| `Module.Entity` | Entity reference |
| `list of Module.Entity` | List of entities |
| `stringtemplate(sql)` | SQL/OQL query template with parameters |
| `stringtemplate(text)` | Text template with parameters |
| `entity <pEntity>` | Type parameter declaration (entity type selector) |
| `enum Module.EnumName` | Enumeration type |
| `enumeration(Module.EnumName)` | Enumeration type (alternative syntax) |
| `pEntity` (type param ref) | Type parameter reference (entity instance) |
| `list of pEntity` | List of type-parameter instances |

**In the `$$` body, a parameter is the generated field — not the raw value.** An entity
parameter is its proxy class (`module.proxies.Entity`; `.getMendixObject()` for the
`IMendixObject`), a list a `java.util.List` of proxies, `integer` a `java.lang.Long`, an
enumeration its proxy enum (but an enumeration *return* is a `String`). The full table is
in [writing-java.md](reference/writing-java.md#step-2-define-parameters); it is what mxbuild
generates, so the body compiles both under `--watch` and after a full build.

### Examples

#### Simple Action (No Parameters)

```mdl
mdl 1;
/** Returns the current timestamp. */
create java action MyModule.GetCurrentTimestamp() returns datetime
as $$
return new java.util.Date();
$$;
```

#### Action with Primitive Parameters

```mdl
mdl 1;
/** Calculates tax amount. */
create java action Finance.CalculateTax(Amount: decimal, TaxRate: decimal) returns decimal
as $$
if (Amount == null || TaxRate == null) {
    return java.math.BigDecimal.ZERO;
}
return Amount.multiply(TaxRate).divide(java.math.BigDecimal.valueOf(100), 2, java.math.RoundingMode.HALF_UP);
$$;
```

#### Action with StringTemplate (SQL/OQL)

```mdl
mdl 1;
/** Executes an OQL statement with parameterized query. */
create java action Database.ExecuteOQLStatement(OqlStatement: stringtemplate(sql) not null) returns boolean
as $$
// execute the parameterized OQL statement
// The stringtemplate handles parameter substitution safely
return true;
$$;
```

#### Action with NOT NULL Parameter

```mdl
mdl 1;
/** Validates an email address - email is required. */
create java action Validation.ValidateEmail(EmailAddress: string not null) returns boolean
as $$
string emailRegex = "^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$";
return EmailAddress.matches(emailRegex);
$$;
```

#### Action with Type Parameter (Generic)

```mdl
mdl 1;
/** Validates any entity - checks that required fields are filled. */
create java action Validation.ValidateEntity(
  EntityType: entity <pEntity> not null,
  InputObject: pEntity not null
) returns boolean
as $$
return InputObject.getMembers().values().stream()
    .allMatch(m -> !m.isRequired() || m.getValue(getContext()) != null);
$$;
```

#### Action with Type Parameter + EXPOSED AS

```mdl
mdl 1;
/** Deep clones any entity (toolbox-visible). */
create java action Utils.DeepClone(
  EntityType: entity <pEntity> not null,
  Original: pEntity not null
) returns boolean
exposed as 'Deep Clone Object' in 'Object Utils'
as $$
return true;
$$;
```

## Part 3: Calling Java Actions from MDL

### Basic Syntax

```mdl
-- Call Java action (no return value)
call java action Module.JA_ActionName(
    ParamName1 = value1,
    ParamName2 = value2
);

-- Call Java action with return value
$Result = call java action Module.JA_ActionName(
    ParamName1 = value1,
    ParamName2 = value2
);
```

### Avoiding Duplicate Variables (CE0111)

`$Var = call java action ...` **creates a new variable**. Do NOT `declare` a variable with the same name first:

```mdl
-- WRONG: DECLARE + CALL both create $Success → CE0111
declare $success boolean = false;
$success = call java action Module.DoWork();

-- CORRECT: Use a separate name when you need a default
declare $success boolean = false;
$WorkResult = call java action Module.DoWork();
set $success = $WorkResult;

-- CORRECT: Simple pass-through (no default needed)
$success = call java action Module.DoWork();
return $success;
```

When calling Java actions in **multiple branches**, use unique result variable names:

```mdl
declare $success boolean = false;
if $Priority = 'HIGH' then
    $UrgentResult = call java action Module.SendUrgent(Msg = $Email);
    set $success = $UrgentResult;
else
    $NormalResult = call java action Module.SendNormal(Msg = $Email);
    set $success = $NormalResult;
end if;
```

### Expression Escaping in String Arguments

Single quotes within string literal arguments must be doubled (`''`):

```mdl
-- OQL with embedded quotes — use '' to escape
$count = call java action Module.ExecuteOQL(
    Statement = 'SELECT * FROM Module.Entity WHERE Status = ''Active'''
);
```

### Complete Examples

#### Example 1: Simple Calculation

```mdl
mdl 1;
/**
 * Calculate tax using custom Java action
 */
create microflow Tax.ACT_CalculateOrderTax($order: Tax.Order)
returns decimal as $taxAmount
begin
    declare $subtotal decimal = $order/Subtotal;
    declare $taxRate decimal = 0.21;

    -- Call Java action for complex calculation
    $taxAmount = call java action Tax.JA_CalculateTax(
        Amount = $subtotal,
        TaxRate = $taxRate
    );

    change $order (TaxAmount = $taxAmount);
    commit $order;

    return $taxAmount;
end;
```

#### Example 2: External API Integration

```mdl
mdl 1;
/**
 * Send notification via external service using Java action
 */
create microflow Notifications.ACT_SendOrderConfirmation($order: Sales.Order)
returns boolean as $success
begin
    declare $customerEmail string = $order/Sales.Order_Customer/Email;
    declare $orderNumber string = $order/OrderNumber;

    -- Call Java action that integrates with external email service
    $success = call java action Notifications.JA_SendEmail(
        ToAddress = $customerEmail,
        Subject = 'Order Confirmation: ' + $orderNumber,
        body = 'Your order has been confirmed.',
        TemplateName = 'OrderConfirmation'
    );

    if $success then
        change $order (NotificationSent = true);
        commit $order;
    else
        log warning node 'Notifications' 'Failed to send email for order: ' + $orderNumber;
    end if;

    return $success;
end;
```

#### Example 3: OQL Bulk Operations (Mendix 11.6+)

```mdl
mdl 1;
/**
 * Bulk update using OQL via Java action
 */
create microflow Finance.ACT_ArchiveOldTransactions()
returns integer as $rowsAffected
begin
    -- Use built-in OQL execution Java action
    $rowsAffected = call java action CustomActivities.ExecuteOQLStatement(
        OqlStatement = 'UPDATE Finance.Transaction SET Status = ''ARCHIVED'' WHERE TransactionDate < ''2024-01-01'' AND Status = ''COMPLETED'''
    );

    log info node 'Finance' 'Archived ' + toString($rowsAffected) + ' transactions';

    return $rowsAffected;
end;
```

#### Example 4: OQL with Parameters

```mdl
/**
 * Parameterized OQL update via Java action
 */
create microflow Finance.ACT_UpdateTransactionStatus(
    $oldStatus: string,
    $newStatus: string,
    $cutoffDate: datetime
)
returns integer as $rowsUpdated
begin
    $rowsUpdated = call java action CustomActivities.ExecuteOQLStatementPars(
        OqlStatement = 'UPDATE Finance.Transaction SET Status = {1} WHERE Status = {2} AND TransactionDate < {3}' with (
            {1} = $newStatus,
            {2} = $oldStatus,
            {3} = $cutoffDate as datetime
        )
    );

    return $rowsUpdated;
end;
```

#### Example 5: Returning Objects

```mdl
mdl 1;
/**
 * Create complex object structure using Java action
 */
create microflow Import.ACT_ParseCSVFile($fileDocument: System.FileDocument)
returns list of Import.ImportRecord as $records
begin
    -- Java action parses CSV and returns list of objects
    $records = call java action Import.JA_ParseCSV(
        FileDocument = $fileDocument,
        HasHeader = true,
        Delimiter = ','
    );

    if $records = empty then
        log warning node 'Import' 'No records parsed from file';
    else
        log info node 'Import' 'Parsed ' + toString(length($records)) + ' records';
    end if;

    return $records;
end;
```

## Validation Checklist

Before deploying Java actions, verify:

- [ ] Java action has `JA_` prefix naming convention
- [ ] All parameters are defined with correct types
- [ ] Return type matches what you return in Java
- [ ] Code is only between `begin user CODE` / `end user CODE` markers
- [ ] Proper null checks for all parameters
- [ ] Exception handling with logging
- [ ] No hardcoded credentials or sensitive data
- [ ] Entity and attribute names match model exactly
- [ ] Unit tests cover main scenarios

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ClassNotFoundException` | Missing library | Add JAR to `userlib/` folder |
| `NullPointerException` | Null parameter | Add null checks |
| `Could not find entity` | Wrong entity name | Use exact qualified name |
| `attribute not found` | Wrong attribute name | Check model for exact name |
| `ClassCastException` | Wrong type cast | Check parameter types |
| `no viable alternative at input '...'` (parse error) | `AS $$ ... $$` body is missing — it is **mandatory** even for void/stub actions | Add `as $$ return null; $$;` (or appropriate stub) |

## Related Documentation

- [Mendix Java Actions Reference](https://docs.mendix.com/refguide/java-actions/)
- [Build Microflow Actions with Java](https://docs.mendix.com/howto/extensibility/howto-connector-kit/)
- [Java Programming in Mendix](https://docs.mendix.com/refguide/java-programming/)
- [Write Microflows Skill](../write-microflows/SKILL.md)
- [Validation Microflows Skill](../validation-microflows/SKILL.md)

## Quick Reference

### Java Action Definition Syntax
```mdl
mdl 1;
-- Basic Java action
create java action Module.JA_IsValid(Param: string not null) returns boolean
as $$
return true;
$$;

-- With type parameters (generics)
-- ENTITY <pEntity> = entity type selector, bare pEntity = entity instances
create java action Module.JA_HasObject(
  EntityType: entity <pEntity> not null,
  Obj: pEntity not null
) returns boolean
as $$
return Obj != null;
$$;

-- With EXPOSED AS (toolbox visibility)
create java action Module.JA_FormatAmount(Amount: decimal) returns string
exposed as 'Format Amount' in 'Formatting'
as $$
return Amount.toString();
$$;

-- Combined type parameters + EXPOSED AS
create java action Module.JA_ValidateObject(
  EntityType: entity <pEntity> not null,
  Obj: pEntity not null
) returns boolean
exposed as 'Validate Object' in 'Validation'
as $$
return Obj != null;
$$;
```

### Java Action Call Syntax
```mdl
-- Without return value
call java action Module.JA_ActionName(Param1 = value1, Param2 = value2);

-- With return value
$Result = call java action Module.JA_ActionName(Param1 = value1);

-- With OQL parameters (Mendix 11.6+)
$Rows = call java action Module.JA_ExecuteOQL(
    Statement = 'UPDATE Module.Entity SET Attr = {1} WHERE Id = {2}' with (
        {1} = $value1,
        {2} = $value2 as integer
    )
);
```

### Core API Quick Reference
```java
// context
IContext context = getContext();

// create
IMendixObject obj = Core.instantiate(context, "Module.Entity");

// read
object value = obj.getValue(context, "attributename");

// update
obj.setValue(context, "attributename", newValue);

// Save
Core.commit(context, obj);

// delete
Core.delete(context, obj);

// query
list<IMendixObject> results = Core.createXPathQuery("//Module.Entity[attr = 'value']").execute(context);

// log
Core.getLogger("ModuleName").info("message");
```
