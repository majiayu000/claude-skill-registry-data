---
name: serialization-persistence
description: >
  Implement serialization (DTOs, JSON, Unity serializers) and persistence (database, CQRS) for domain models (C# by default, F# on request)
  following "Domain Modeling Made Functional." Use this skill whenever creating DTOs, converting
  between domain types and serializable types, implementing fromDomain/toDomain functions,
  persisting domain objects, or designing database schemas for algebraic types.
  Trigger on: "DTO", "data transfer object", "serialize", "deserialize", "fromDomain", "toDomain",
  "JSON", "persist", "database", "CQRS", "command query separation", "read model", "write model",
  "document database", "relational mapping", "choice type to table", "push I/O to edges",
  "persistence layer", "repository", "event sourcing". Also trigger when the user has a domain
  model and needs to bridge it to infrastructure (APIs, databases, queues, external services).
---

# Serialization & Persistence (DMF Methodology)

This skill covers bridging domain types to the outside world: converting to/from DTOs,
serializing to JSON/XML, and persisting to databases. It assumes domain types and
workflow implementations already exist.

## Language

Code in this skill is F#, the notation of the book.
Write C# unless the user asks for F# or the project is an F# project: **read** `${CLAUDE_PLUGIN_ROOT}/references/csharp-mapping.md` first and express every pattern below with it.
The project profile's Mapping section names the functional library and wins over the mapping's defaults.

In Unity, also read the "Serialization and DTOs in Unity" and "Versioning Persisted Data" sections of the mapping before choosing a serializer.

## Core Principles

1. **Domain types are NOT serialization types** - Always create separate DTO types.
2. **DTOs are the contract** - Between bounded contexts, the DTO format IS the API.
3. **Push I/O to the edges** - Pure domain logic in the center, I/O at the boundaries.
4. **Bounded contexts own their data** - No shared databases between contexts.
5. **CQS** - Functions that return data don't mutate. Functions that mutate don't return data.

## The DTO Pattern

For every domain type that crosses a boundary, create a corresponding DTO type
where all fields are primitives (string, int, DateTime, etc.).

```
Domain Type ──→ fromDomain ──→ DTO Type ──→ Serialize ──→ JSON/XML
JSON/XML ──→ Deserialize ──→ DTO Type ──→ toDomain ──→ Domain Type (Result)
```

**Key rule:** `fromDomain` always succeeds. `toDomain` returns `Result` because
deserialized data is untrusted and needs validation.

## DTO Translation Rules

Read `references/dto-patterns.md` for the complete translation table. Summary:

| Domain Type | DTO Type |
|------------|----------|
| Single-case DU (`OrderId of string`) | Primitive (`string`) |
| `option` | Nullable / null |
| Record | Record with primitive fields |
| List / Set | Array |
| Discriminated Union (enum-like) | .NET enum or string |
| Discriminated Union (with data) | Record with tag + nullable fields per case |
| Map | Array of key-value records, or parallel arrays |

## Complete Serialization Example

### Domain type

```fsharp
module Domain =
    type String50 = String50 of string
    type Birthdate = Birthdate of DateTime
    type Person = {
        First : String50
        Last : String50
        Birthdate : Birthdate
    }
```

### DTO type

```fsharp
module Dto =
    type Person = {
        First : string
        Last : string
        Birthdate : DateTime
    }
```

### Conversion functions

```fsharp
module Dto =
    module Person =
        let fromDomain (person: Domain.Person) : Dto.Person =
            let first = person.First |> String50.value
            let last = person.Last |> String50.value
            let birthdate = person.Birthdate |> Birthdate.value
            { First = first; Last = last; Birthdate = birthdate }

        let toDomain (dto: Dto.Person) : Result<Domain.Person, string> =
            result {
                let! first = dto.First |> String50.create "First"
                let! last = dto.Last |> String50.create "Last"
                let! birthdate = dto.Birthdate |> Birthdate.create
                return { First = first; Last = last; Birthdate = birthdate }
            }
```

### JSON wrapper

```fsharp
module Json =
    open Newtonsoft.Json
    let serialize obj = JsonConvert.SerializeObject obj
    let deserialize<'a> str =
        try JsonConvert.DeserializeObject<'a> str |> Ok
        with ex -> Error ex
```

### Full pipeline

```fsharp
// Domain → JSON (always succeeds)
let jsonFromDomain (person: Domain.Person) =
    person |> Dto.Person.fromDomain |> Json.serialize

// JSON → Domain (can fail)
type DtoError =
    | ValidationError of string
    | DeserializationException of exn

let jsonToDomain jsonString : Result<Domain.Person, DtoError> =
    result {
        let! dto =
            jsonString
            |> Json.deserialize<Dto.Person>
            |> Result.mapError DeserializationException
        let! domain =
            dto
            |> Dto.Person.toDomain
            |> Result.mapError ValidationError
        return domain
    }
```

## Serializing Choice Types

Choice types need a tag field + nullable data fields for each case.

```fsharp
// Domain
type Example =
    | A
    | B of int
    | C of string list
    | D of Name

// DTO
type ExampleDto = {
    Tag : string              // "A", "B", "C", or "D"
    BData : Nullable<int>
    CData : string[]
    DData : NameDto           // nullable via Unchecked.defaultof
}
```

See `references/dto-patterns.md` for full fromDomain/toDomain implementations.

## Connecting Serialization to the Workflow

Serialization is just another pipeline stage at the edges:

```fsharp
let workflowWithSerialization jsonString =
    jsonString
    |> deserializeInputDto      // JSON → DTO
    |> inputDtoToDomain         // DTO → Domain (validation here)
    |> workflow                 // Pure domain logic
    |> outputDtoFromDomain      // Domain → DTO
    |> serializeOutputDto       // DTO → JSON
```

## Persistence

### Push I/O to the Edges (Sandwich Pattern)

```
I/O (load)  →  Pure Domain Logic  →  I/O (save)
```

```fsharp
// BAD: I/O mixed with domain logic
let payInvoice invoiceId payment =
    let invoice = loadInvoiceFromDatabase invoiceId  // I/O
    invoice.ApplyPayment payment                     // logic
    if invoice.IsFullyPaid then
        markAsFullyPaidInDb invoiceId                // I/O

// GOOD: pure domain function returns a decision
type InvoicePaymentResult =
    | FullyPaid
    | PartiallyPaid of UpdatedInvoice

let applyPayment unpaidInvoice payment =
    let updated = applyPaymentLogic unpaidInvoice payment
    if isFullyPaid updated then FullyPaid
    else PartiallyPaid updated

// I/O wrapper at the edge
let payInvoiceHandler payInvoiceCommand =
    // Load (I/O)
    let invoice = loadInvoiceFromDatabase payInvoiceCommand.InvoiceId
    // Pure decision
    let result = applyPayment invoice payInvoiceCommand.Payment
    // Act on decision (I/O)
    match result with
    | FullyPaid ->
        markAsFullyPaidInDb payInvoiceCommand.InvoiceId
        postInvoicePaidEvent payInvoiceCommand.InvoiceId
    | PartiallyPaid updated ->
        updateInvoiceInDb updated
```

**If you need multiple I/O + logic steps**, use the "layer cake" pattern:
```
I/O → Pure → I/O → Pure → I/O
```
Or break into smaller workflows, each with its own sandwich.

### CQS / CQRS

**Command-Query Separation:** Functions that return data don't mutate. Functions that mutate return unit.

```fsharp
// Persistence function signatures
type InsertData = Data -> DbResult<unit>
type ReadData = Query -> DbResult<Data>
type UpdateData = Data -> DbResult<unit>
type DeleteData = Key -> DbResult<unit>

type DbResult<'a> = AsyncResult<'a, DbError>
```

**CQRS:** Separate types for reading and writing.

```fsharp
// WRONG: same type for both
type SaveCustomer = Customer -> DbResult<unit>
type LoadCustomer = CustomerId -> DbResult<Customer>

// RIGHT: separate read/write models
type SaveCustomer = WriteModel.Customer -> DbResult<unit>
type LoadCustomer = CustomerId -> DbResult<ReadModel.Customer>
```

Why separate:
- Queries often return denormalized/joined data
- Commands need only the fields being updated
- Read and write models evolve independently

### Document Database Persistence

Straightforward: domain → DTO → JSON → store.

```fsharp
let savePersonDtoToBlob personDto =
    let blobId = sprintf "Person%i" personDto.PersonId
    let json = Json.serialize personDto
    blob.UploadText json
```

### Relational Database Mapping

Records map to tables. Each field becomes a column with its primitive type.

```sql
CREATE TABLE Customer (
    CustomerId int NOT NULL,
    Name NVARCHAR(50) NOT NULL,
    Birthdate DATETIME NULL,  -- option → NULL
    CONSTRAINT PK_Customer PRIMARY KEY (CustomerId)
)
```

**Choice types** → two approaches:

1. **Single table** (default): tag columns + nullable data columns
```sql
CREATE TABLE ContactInfo (
    ContactId int NOT NULL,
    IsEmail bit NOT NULL,
    IsPhone bit NOT NULL,
    EmailAddress NVARCHAR(100) NULL,
    PhoneNumber NVARCHAR(25) NULL,
    PRIMARY KEY (ContactId)
)
```

2. **Multi-table**: parent table with flags + child tables per case
(Use when cases have very different, large data sets.)

**Nested types:**
- Entity (has identity) → separate table with FK to parent
- Value Object (no identity) → inline columns in parent table

```sql
CREATE TABLE [Order] (
    OrderId int NOT NULL,
    -- Value Object: inline
    ShippingAddress1 varchar(50),
    ShippingCity varchar(50),
    -- Entity reference: separate table
    PRIMARY KEY (OrderId)
)

CREATE TABLE OrderLine (
    OrderLineId int NOT NULL,
    OrderId int NOT NULL,         -- FK to parent aggregate
    ProductCode varchar(20) NOT NULL,
    Quantity decimal NOT NULL,
    PRIMARY KEY (OrderLineId)
)
```

### Reading from DB: toDomain with validation

Treat the database as an untrusted source:

```fsharp
let toDomain (dbRecord: ReadOneCustomer.Record) : Result<Customer, _> =
    result {
        let! customerId = dbRecord.CustomerId |> CustomerId.create
        let! name = dbRecord.Name |> String50.create "Name"
        let! birthdate = dbRecord.Birthdate |> Result.bindOption Birthdate.create
        return { CustomerId = customerId; Name = name; Birthdate = birthdate }
    }
```

Or, if you trust the DB and want panics on bad data:

```fsharp
let toDomain dbRecord : Customer =
    let customerId = dbRecord.CustomerId |> CustomerId.create |> panicOnError "CustomerId"
    let name = dbRecord.Name |> String50.create "Name" |> panicOnError "Name"
    { CustomerId = customerId; Name = name; Birthdate = birthdate }
```

### Bounded Context Data Ownership

- Each bounded context owns its data store and schema
- No direct cross-context DB access
- Other contexts use the public API (events/commands) to get data
- Reporting/BI is a separate context that subscribes to events

### Transactions

- One aggregate = one transaction (default)
- For multi-aggregate atomicity: use DB transactions if same store, or compensating transactions if different stores

```fsharp
// Compensating transaction pattern
markAsFullyPaid connection invoiceId
let result = markPaymentCompleted connection paymentId
match result with
| Error _ -> unmarkAsFullyPaid connection invoiceId  // compensate
| Ok _ -> ()
```

## File Organization

```
Infrastructure/
├── Dto.fs                 -- All DTO types + fromDomain/toDomain
├── Json.fs                -- JSON serializer wrapper
├── Database.fs            -- DB access functions (read/write)
├── CompositionRoot.fs     -- Wire everything together
```

## Checklist

- [ ] Every domain type that crosses a boundary has a DTO
- [ ] `fromDomain` (domain → DTO) always succeeds
- [ ] `toDomain` (DTO → domain) returns Result and validates
- [ ] JSON serializer is wrapped to return Result on failure
- [ ] Domain types never appear in serialization/DB code directly
- [ ] I/O is at the edges; domain logic is pure in the center
- [ ] Each bounded context has its own data store
- [ ] Read and write models are separate types (or at minimum, separate functions)
- [ ] Every persisted DTO has a version field and one migration per shipped version
- [ ] The chosen serializer can serialize the DTO shape (Unity: see the serializer table in the mapping)

## Output Format

Save the output as **`08-serialization-bridge.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/design-directory.md` for choosing `<topic>`).
Start the file with a `> Source:` line naming the files it consumed (used for staleness checks).

**Input files:** `04-domain-model.md` (domain types to serialize) + `06-workflow-pipelines.md` (I/O points at pipeline edges) + `07-service-wiring.md` §6 (DTO boundaries between services) and §3 (event catalog with payloads) if it exists (from the `lowy` plugin).
If `07-service-wiring.md` does not exist, derive the boundaries from `01-domain-discovery.md` §2-3 (each cross-context relationship in the context map), every persistence store and external system named in `01-domain-discovery.md`, `04-domain-model.md` or `06-workflow-pipelines.md`, and the event payloads from the `01-domain-discovery.md` §4 domain events that cross a context boundary, and say in the output that no service wiring was used.
If `01-domain-discovery.md` does not exist either, derive them from the bounded contexts and event types in `04-domain-model.md` and the I/O points in `06-workflow-pipelines.md`.

**Output file:** `08-serialization-bridge.md` - this is the final architecture artifact.

Organize the output by boundary. For each boundary (between services or bounded contexts, to a persistence store, or to an external system) and each event channel, include:
1. DTO type definitions (all fields as primitives)
2. `fromDomain` functions (domain → DTO, always succeeds)
3. `toDomain` functions (DTO → domain, returns Result)
4. Serialization format (JSON/XML/binary) and any config
5. Persistence strategy per service or bounded context (document DB, relational, event store, in-memory)
6. Read model definitions (if CQRS applies)
7. Database schema sketch (if relational - tables, key columns, choice-type mapping strategy)
8. Versioning and migration plan for every persisted DTO
