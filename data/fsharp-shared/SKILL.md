---
name: fsharp-shared
description: |
  Define shared domain types and API contracts for F# full-stack applications.
  Use when: "define types", "create entity", "add model", "API contract", "shared types",
  "domain model", "record", "discriminated union", "data structure", "DTO",
  "interface", "type definition", "new entity", "modify types".
  Creates types in src/Shared/Domain.fs and API interfaces in src/Shared/Api.fs.
  Always start here when adding new features.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# F# Shared Types and API Contracts

## When to Use This Skill

Activate when:
- Starting any new feature (always define types first)
- User requests "add X entity", "define Y types"
- Need to create API contracts between client and server
- Modifying existing domain types
- Creating shared data structures

## Prerequisites

Project must have:
- `src/Shared/Domain.fs` for domain types
- `src/Shared/Api.fs` for API contracts
- Fable.Remoting package installed

## Type Design Patterns

### Simple Entity (Records)

**Use for:** Basic data structures with named fields

```fsharp
// src/Shared/Domain.fs
module Shared.Domain

open System

type TodoItem = {
    Id: int
    Title: string
    Description: string option
    IsCompleted: bool
    CreatedAt: DateTime
    UpdatedAt: DateTime
}
```

**Key points:**
- Use records (not classes)
- Use `option` for nullable fields
- Include timestamps for auditing
- Immutable by default

### Discriminated Unions

**Use for:** Fixed sets of values or state machines

```fsharp
type Priority =
    | Low
    | Medium
    | High
    | Urgent

type TodoStatus =
    | NotStarted
    | InProgress
    | Completed
    | Cancelled

type TodoItem = {
    Id: int
    Title: string
    Priority: Priority
    Status: TodoStatus
    CreatedAt: DateTime
}
```

**Key points:**
- Exhaustive pattern matching
- Compiler-enforced state transitions
- Self-documenting code

### Smart Constructors (Constrained Types)

**Use for:** Types with validation rules

```fsharp
type EmailAddress = private EmailAddress of string

module EmailAddress =
    let create (s: string) : Result<EmailAddress, string> =
        if s.Contains("@") && s.Length > 3 then
            Ok (EmailAddress s)
        else
            Error "Invalid email format"

    let value (EmailAddress s) = s

type User = {
    Id: int
    Name: string
    Email: EmailAddress  // Guaranteed valid
}
```

**Key points:**
- Private constructor prevents invalid instances
- Factory function enforces validation
- Type system ensures correctness

### Collections and Nested Types

```fsharp
type TodoList = {
    Id: int
    Name: string
    Items: TodoItem list
    Owner: User
    CreatedAt: DateTime
}

type Dashboard = {
    User: User
    Lists: TodoList list
    TotalItems: int
}
```

## API Contract Patterns

### Basic CRUD API

**Location:** `src/Shared/Api.fs`

```fsharp
module Shared.Api

open Domain

type ITodoApi = {
    // Queries (always succeed, return empty on no data)
    getAll: unit -> Async<TodoItem list>

    // Queries that may fail (use Result)
    getById: int -> Async<Result<TodoItem, string>>

    // Commands that may fail
    create: TodoItem -> Async<Result<TodoItem, string>>
    update: TodoItem -> Async<Result<TodoItem, string>>
    delete: int -> Async<Result<unit, string>>
}
```

**Return type guide:**
- `Async<'T list>` - Always returns (empty list if none)
- `Async<Result<'T, string>>` - May fail (not found, validation error)
- `Async<Result<unit, string>>` - Success with no data to return

### API with DTOs (Create/Update Models)

**Use when:** Create and update have different fields

```fsharp
type CreateTodoRequest = {
    Title: string
    Description: string option
    Priority: Priority
}

type UpdateTodoRequest = {
    Id: int
    Title: string
    Description: string option
    Priority: Priority
    Status: TodoStatus
}

type ITodoApi = {
    getAll: unit -> Async<TodoItem list>
    getById: int -> Async<Result<TodoItem, string>>
    create: CreateTodoRequest -> Async<Result<TodoItem, string>>
    update: UpdateTodoRequest -> Async<Result<TodoItem, string>>
    delete: int -> Async<Result<unit, string>>
}
```

**Key points:**
- Separate request models from domain entities
- Client doesn't set server-managed fields (Id, timestamps)
- Clearer intent (create vs update)

### Multiple API Interfaces

**Use when:** Logically separate concerns

```fsharp
type ITodoApi = {
    getAll: unit -> Async<TodoItem list>
    save: TodoItem -> Async<Result<TodoItem, string>>
}

type IUserApi = {
    getCurrent: unit -> Async<User>
    updateProfile: User -> Async<Result<User, string>>
}

type IAppApi = {
    getInfo: unit -> Async<AppInfo>
    getConfig: unit -> Async<Config>
}
```

**Key points:**
- One interface per domain area
- Keep APIs focused and cohesive
- Easier to test and maintain

### Custom Result Types

**Use when:** Multiple possible outcomes

```fsharp
type SaveResult =
    | Created of TodoItem
    | Updated of TodoItem
    | ValidationError of string list
    | Conflict of existingItem: TodoItem

type ITodoApi = {
    save: TodoItem -> Async<SaveResult>
}
```

## Type Design Guidelines

### ✅ Do

**Use Records for Data:**
```fsharp
type Item = {
    Id: int
    Name: string
}
```

**Use Option for Nullable:**
```fsharp
type User = {
    Email: string
    Phone: string option  // May not have phone
}
```

**Use Result for Fallible Operations:**
```fsharp
getById: int -> Async<Result<Item, string>>
```

**Use DateTime from System:**
```fsharp
open System

type Event = {
    OccurredAt: DateTime  // Serializes correctly
}
```

**Descriptive Names:**
```fsharp
type OrderStatus = Pending | Confirmed | Shipped | Delivered
// NOT: type Status = A | B | C | D
```

### ❌ Don't

**Don't Use Classes:**
```fsharp
// ❌ BAD
type Item() =
    member val Id = 0 with get, set
    member val Name = "" with get, set

// ✅ GOOD
type Item = { Id: int; Name: string }
```

**Don't Use Null:**
```fsharp
// ❌ BAD
type User = { Email: string; Phone: string }  // null for no phone?

// ✅ GOOD
type User = { Email: string; Phone: string option }
```

**Don't Use Nullable<'T>:**
```fsharp
// ❌ BAD
type User = { Age: Nullable<int> }

// ✅ GOOD
type User = { Age: int option }
```

**Don't Add Logic to Types:**
```fsharp
// ❌ BAD - Keep types pure
type User = {
    Name: string
    member this.IsValid() = not (String.IsNullOrEmpty this.Name)
}

// ✅ GOOD - Separate logic
type User = { Name: string }
module User =
    let isValid user = not (String.IsNullOrEmpty user.Name)
```

## Common Type Patterns

### Timestamps
```fsharp
type Entity = {
    // ... fields
    CreatedAt: DateTime
    UpdatedAt: DateTime
}
```

### Soft Delete
```fsharp
type Entity = {
    // ... fields
    DeletedAt: DateTime option
    IsDeleted: bool
}
```

### Audit Trail
```fsharp
type Entity = {
    // ... fields
    CreatedBy: string
    CreatedAt: DateTime
    UpdatedBy: string option
    UpdatedAt: DateTime option
}
```

### Pagination
```fsharp
type PageRequest = {
    PageNumber: int
    PageSize: int
}

type PagedResult<'T> = {
    Items: 'T list
    TotalCount: int
    PageNumber: int
    PageSize: int
    TotalPages: int
}
```

## Complete Example

```fsharp
// src/Shared/Domain.fs
module Shared.Domain

open System

type Priority = Low | Medium | High
type TodoStatus = Active | Completed

type TodoItem = {
    Id: int
    Title: string
    Description: string option
    Priority: Priority
    Status: TodoStatus
    CreatedAt: DateTime
    UpdatedAt: DateTime
}

type CreateTodoRequest = {
    Title: string
    Description: string option
    Priority: Priority
}

type TodoList = {
    Id: int
    Name: string
    Items: TodoItem list
}

// src/Shared/Api.fs
module Shared.Api

open Domain

type ITodoApi = {
    getAll: unit -> Async<TodoItem list>
    getActive: unit -> Async<TodoItem list>
    getById: int -> Async<Result<TodoItem, string>>
    create: CreateTodoRequest -> Async<Result<TodoItem, string>>
    complete: int -> Async<Result<TodoItem, string>>
    delete: int -> Async<Result<unit, string>>
}

type IListApi = {
    getAllLists: unit -> Async<TodoList list>
    getListById: int -> Async<Result<TodoList, string>>
    addItemToList: listId: int * item: TodoItem -> Async<Result<unit, string>>
}
```

## Verification Checklist

- [ ] Types defined in `src/Shared/Domain.fs`
- [ ] API contracts in `src/Shared/Api.fs`
- [ ] Used records (not classes)
- [ ] Used `option` for nullable fields
- [ ] Used `Result<'T, string>` for fallible operations
- [ ] All types immutable
- [ ] No logic in type definitions
- [ ] Meaningful, descriptive names
- [ ] Compile succeeds (`dotnet build`)

## Next Steps

After defining shared types:
1. Implement backend with **fsharp-backend** skill
2. Or implement specific layers:
   - Validation: **fsharp-validation**
   - Persistence: **fsharp-persistence**
   - Frontend: **fsharp-frontend**

## Related Documentation

Check project docs:
- `/docs/04-SHARED-TYPES.md` - Detailed type design guide
- `/docs/09-QUICK-REFERENCE.md` - Quick code templates
- `CLAUDE.md` - Project-specific conventions
