---
name: domain-modeling
description: >
  Model domains with algebraic types (C# by default, F# on request) following "Domain Modeling Made Functional" methodology.
  Use this skill whenever the task involves defining domain types, modeling entities, value objects,
  aggregates, or workflows as types. Trigger on: "model this domain", "define types for",
  "make illegal states unrepresentable", "domain model", "bounded context types",
  "constrained type", "smart constructor", "algebraic data type", "discriminated union for domain",
  "value object", "entity", "aggregate". Also trigger when reviewing or refactoring domain types
  for correctness, or when the user provides domain requirements that need to be captured as types.
---

# Domain Modeling with Types (DMF Methodology)

This skill encodes the type-driven domain modeling approach from "Domain Modeling Made Functional."
The core principle: **the domain model IS the types**. Types are not an implementation detail -
they ARE the design, the documentation, and the constraints, all in one.

## Language

Code in this skill is F#, the notation of the book.
Write C# unless the user asks for F# or the project is an F# project: **read** `${CLAUDE_PLUGIN_ROOT}/references/csharp-mapping.md` first and express every pattern below with it.
The project profile's Mapping section names the functional library and wins over the mapping's defaults.

## Core Philosophy

1. **Types replace UML** - The type system is expressive enough to capture the full domain model (natively in F#; in C# with closed unions and smart constructors).
2. **Make illegal states unrepresentable** - If a state shouldn't exist, make it impossible to construct.
3. **Use the Ubiquitous Language** - Type names and field names must match domain expert terminology exactly.
4. **No primitives in the domain** - Wrap all primitives in domain-specific types.
5. **Separate types per lifecycle stage** - `UnvalidatedOrder`, `ValidatedOrder`, `PricedOrder` are distinct types.
6. **Document effects in signatures** - If a function can fail, the return type says so (`Result<T,E>`).

## Decision Framework

When modeling a concept, follow this sequence:

```
1. Is it a simple value? (OrderId, Email, Quantity)
   → Single-case DU with smart constructor (see "Simple Constrained Types")

2. Is it a grouping of values? (Name = First + Last)
   → Record type (AND type)

3. Is it one of several alternatives? (ContactInfo = Email | Phone)
   → Discriminated Union (OR type)

4. Does it have identity? (Order has OrderId)
   → Entity: record with an Id field, equality by Id

5. Is it defined only by its values? (Address, MoneyAmount)
   → Value Object: record, structural equality

6. Is it a consistency boundary? (Order + its OrderLines)
   → Aggregate: top-level entity that owns its children

7. Is it a workflow step?
   → Function type alias: Input -> Output (with effects)
```

## Simple Constrained Types

Every primitive that enters the domain must be wrapped. The wrapper enforces constraints at creation time.

```fsharp
// Pattern: private constructor + smart constructor in companion module
type OrderId = private OrderId of string

module OrderId =
    let create str =
        if String.IsNullOrEmpty(str) then
            Error "OrderId must not be null or empty"
        elif str.Length > 50 then
            Error "OrderId must not be more than 50 chars"
        else
            Ok (OrderId str)

    let value (OrderId str) = str
```

**Rules for simple types:**
- Always `private` - construction only through `create`
- `create` returns `Result<T, string>` (never throws)
- `value` extracts the inner primitive (for serialization, display, etc.)
- Put `create` and `value` in a module with the same name as the type
- For optional creation (where empty/null → None), add `createOption`

Common simple types to define for most domains:
- `String50`, `String100` - length-constrained strings
- `EmailAddress` - format-validated string
- `ZipCode`, `PhoneNumber` - pattern-validated strings
- Numeric types with range constraints (`UnitQuantity`, `KilogramQuantity`)

Read `references/simple-types.md` for the full catalog of patterns.

## AND Types (Records)

Records model "this AND that" - a grouping of fields that always appear together.

```fsharp
type PersonalName = {
    FirstName : String50
    LastName : String50
}

type CustomerInfo = {
    Name : PersonalName
    EmailAddress : EmailAddress
}
```

**Rules:**
- Every field must be a domain type (no raw `string`, `int`, `DateTime`)
- Optional fields use `option` explicitly: `MiddleName : String50 option`
- Records are Value Objects by default (structural equality)
- To make a record an Entity, add an Id field and override equality

## OR Types (Discriminated Unions)

DUs model "this OR that" - mutually exclusive alternatives.

```fsharp
type ContactInfo =
    | Email of EmailAddress
    | Phone of PhoneNumber

type OrderQuantity =
    | Unit of UnitQuantity
    | Kilogram of KilogramQuantity

type ProductCode =
    | Widget of WidgetCode
    | Gizmo of GizmoCode
```

**When to use a DU vs. a flag:**
- WRONG: `{ IsVip: bool; VipDiscount: decimal option }` - the discount can be present when IsVip is false
- RIGHT: `type CustomerStatus = Normal | Vip of VipDiscount` - illegal state is unrepresentable

**When to use a DU vs. inheritance:**
- Always prefer DUs. They are closed (all cases known at compile time), which means the compiler
  enforces exhaustive matching. Inheritance is open and cannot provide this guarantee.
- In C#, a union is a closed record hierarchy: private base constructor, nested sealed cases, no behavior in the base.
  That is an encoding of a DU, not the open inheritance this rule forbids.

## Entities, Value Objects, Aggregates

**Value Object** - No identity. Two values with the same fields are equal.
```fsharp
type Address = {
    AddressLine1 : String50
    City : String50
    ZipCode : ZipCode
}
// F# records have structural equality by default - no extra work needed
```

**Entity** - Has identity. Two entities with the same Id are the same entity even if fields differ.
```fsharp
type Order = {
    OrderId : OrderId          // identity field
    CustomerInfo : CustomerInfo
    ShippingAddress : Address
    BillingAddress : Address
    Lines : OrderLine list
}
// Equality should be by OrderId only - use [<CustomEquality; CustomComparison>] if needed
```

**Aggregate** - A cluster of entities/value objects treated as a unit for consistency.
- The top-level entity is the **aggregate root** (e.g., `Order`)
- Child entities (e.g., `OrderLine`) are only accessible through the root
- A single database transaction = a single aggregate
- References between aggregates use IDs, not direct object references

```fsharp
// OrderLine belongs to Order aggregate - never persisted independently
type OrderLine = {
    OrderLineId : OrderLineId
    ProductCode : ProductCode
    Quantity : OrderQuantity
}

// Cross-aggregate reference: use CustomerId, not Customer
type Order = {
    OrderId : OrderId
    CustomerId : CustomerId   // reference by ID, not by embedding the full Customer
    Lines : OrderLine list
}
```

## Modeling Workflows as Function Types

Each workflow step is a function type alias. Dependencies are explicit parameters.

```fsharp
// Step function types
type ValidateOrder =
    CheckProductCodeExists    // dependency
      -> CheckAddressExists   // dependency
      -> UnvalidatedOrder     // input
      -> Result<ValidatedOrder, ValidationError list>  // output

type PriceOrder =
    GetProductPrice           // dependency
      -> ValidatedOrder       // input
      -> Result<PricedOrder, PricingError>  // output

// Dependency function types
type CheckProductCodeExists = ProductCode -> bool
type CheckAddressExists = UnvalidatedAddress -> AsyncResult<CheckedAddress, AddressValidationError>
type GetProductPrice = ProductCode -> Price
```

**Rules for workflow types:**
- One type per pipeline stage
- Dependencies come first, then input, then output
- Effects are explicit: `Result<T,E>` for fallible, `Async<T>` for async, `AsyncResult<T,E>` for both
- Each stage transforms one "document" type into the next
- The overall workflow is the composition of all stages

## Separate Types Per Lifecycle Stage

The same real-world concept (an "order") has different types at different stages.
This is intentional - each stage has different fields, constraints, and invariants.

```fsharp
// Stage 1: raw input from outside the bounded context
type UnvalidatedOrder = {
    OrderId : string                         // primitive - not yet validated
    CustomerInfo : UnvalidatedCustomerInfo
    Lines : UnvalidatedOrderLine list
}

// Stage 2: validated domain object
type ValidatedOrder = {
    OrderId : OrderId                        // constrained type
    CustomerInfo : CustomerInfo
    ShippingAddress : Address
    Lines : ValidatedOrderLine list
}

// Stage 3: priced
type PricedOrder = {
    OrderId : OrderId
    CustomerInfo : CustomerInfo
    ShippingAddress : Address
    Lines : PricedOrderLine list
    AmountToBill : BillingAmount
}
```

**Why separate types:**
- Prevents accidentally using unvalidated data in later stages
- Each type documents exactly what is known at that point
- The compiler enforces the correct ordering of stages

## Modeling Errors

Errors are part of the domain. Model them as choice types.

```fsharp
type ValidationError =
    | InvalidField of fieldName: string * message: string

type PricingError =
    | ProductNotFound of ProductCode
    | PriceCalculationError of string

type PlaceOrderError =
    | Validation of ValidationError list
    | Pricing of PricingError
    | RemoteService of RemoteServiceError
    | OutsideBusinessHours

type RemoteServiceError = {
    Service : ServiceInfo
    Exception : exn
}
```

**Rules:**
- Domain errors get their own choice type - they are first-class domain concepts
- Panics (out of memory, null ref) are exceptions - don't model them
- Infrastructure errors can be modeled if the business needs to react to them
- Each workflow has a top-level error type that is the union of all possible step errors

## File Organization

```
Domain/
├── SimpleTypes.fs          -- String50, EmailAddress, OrderId, etc.
├── PublicTypes.fs           -- Types exposed as the bounded context API
│                               (commands, events, workflow function type)
├── PlaceOrderWorkflow.fs    -- Internal types + implementation for one workflow
├── ChangeOrderWorkflow.fs   -- Internal types + implementation for another
└── Result.fs / Common.fs    -- Result helpers, AsyncResult, computation expressions
```

- Public types (commands, events, top-level workflow signature) go in a shared module
- Internal stage types (ValidatedOrder, PricedOrder) go in the workflow module
- Simple types are shared across the bounded context
- In C#: one assembly (asmdef) per bounded context or service, as the project profile maps it; simple types, public types (commands, events, workflow delegates) and one file per workflow with its internal stage types

## Checklist Before Moving to Implementation

Before implementing, verify:

- [ ] Every primitive is wrapped in a domain type with a smart constructor
- [ ] Every `option` (C#: `Optional<T>`) field is intentional (represents genuine optionality in the domain)
- [ ] No boolean flags that should be choice types
- [ ] No "impossible" combinations of fields are representable
- [ ] Every workflow step has a function type with explicit dependencies and effects
- [ ] Error types cover all domain-relevant failure modes
- [ ] Types use Ubiquitous Language - a domain expert could read the type names

## Output Format

Save the output as **`04-domain-model.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/design-directory.md` for choosing `<topic>`).
Start the file with a `> Source:` line naming the files it consumed (used for staleness checks).

**Input files:** `01-domain-discovery.md` §6-8 (workflows, data structures, ubiquitous language).
Optional, with the `lowy` plugin: `03-layered-architecture.md` §8 (service → bounded context mapping), used when it exists.
If `03-layered-architecture.md` does not exist, organize types by the bounded contexts in `01-domain-discovery.md` §2 instead, and say in the output that no service mapping was used.

**Output file:** `04-domain-model.md` - consumed by Phase 6 (`dmf:workflow-implementation`) and Phase 8 (`dmf:serialization-persistence`); with the `lowy` plugin, also Phase 7 (`lowy:wire-services`, to identify DTO boundaries).

Organize the output by bounded context (or by service, when `03-layered-architecture.md` maps services to contexts).
For each one, include:
1. Simple constrained types (with smart constructor signatures)
2. Record types (AND types)
3. Choice types (OR types / discriminated unions)
4. Entity and aggregate definitions
5. Lifecycle stage types (Unvalidated → Validated → Priced → ...)
6. Workflow function type signatures (with dependencies and effects)
7. Error types

Write the code blocks in C# unless F# was requested (see Language).

For detailed code patterns, see:
- `references/simple-types.md` - Full catalog of constrained type patterns
- `references/modeling-patterns.md` - Advanced patterns (units of measure, state machines, etc.)
