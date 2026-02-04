---
name: fsharp-backend
description: |
  Implement F# backend using Giraffe + Fable.Remoting with proper layer separation.
  Use when: "implement backend", "add API", "create endpoint", "server logic", "business rules",
  "backend for X", "API implementation", "server-side", "Giraffe", "Fable.Remoting".
  Layers: Validation → Domain (pure) → Persistence (I/O) → API.
  Creates code in src/Server/: Validation.fs, Domain.fs, Persistence.fs, Api.fs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# F# Backend Implementation

## When to Use This Skill

Activate when:
- User requests "implement backend for X"
- Need to add API endpoints
- Implementing business logic
- Creating server-side functionality
- Project has src/Server/ directory with Giraffe

## Architecture Layers

```
API (Fable.Remoting)
    ↓
Validation (Input checking)
    ↓
Domain (Pure business logic - NO I/O)
    ↓
Persistence (Database/File I/O)
```

## Layer 1: Validation (`src/Server/Validation.fs`)

**Purpose:** Validate input at API boundary before processing

> For detailed validation patterns, see the **fsharp-validation** skill.

### Basic Pattern
```fsharp
module Validation

open Shared.Domain

let validateCreateRequest (req: CreateTodoRequest) : Result<CreateTodoRequest, string list> =
    let errors = [
        if String.IsNullOrWhiteSpace(req.Title) then "Title is required"
        if req.Title.Length > 100 then "Title too long"
    ]
    if errors.IsEmpty then Ok req else Error errors
```

**Key points:**
- Validate at API boundary, before domain logic
- Return `Result<'T, string list>` to accumulate errors
- Convert to single string for API: `String.concat "; " errors`

## Layer 2: Domain (`src/Server/Domain.fs`)

**Purpose:** Pure business logic - NO side effects, NO I/O

### Pattern
```fsharp
module Domain

open System
open Shared.Domain

// ✅ PURE transformations only
let processNewTodo (request: CreateTodoRequest) : TodoItem =
    {
        Id = 0  // Will be set by persistence
        Title = request.Title.Trim()
        Description = request.Description |> Option.map (fun d -> d.Trim())
        Priority = request.Priority
        Status = Active
        CreatedAt = DateTime.UtcNow
        UpdatedAt = DateTime.UtcNow
    }

let completeTodo (item: TodoItem) : TodoItem =
    { item with Status = Completed; UpdatedAt = DateTime.UtcNow }

let updateTodo (existing: TodoItem) (updates: CreateTodoRequest) : TodoItem =
    {
        existing with
            Title = updates.Title.Trim()
            Description = updates.Description |> Option.map (fun d -> d.Trim())
            Priority = updates.Priority
            UpdatedAt = DateTime.UtcNow
    }

// ✅ PURE calculations
let calculatePriority (items: TodoItem list) : Priority =
    items
    |> List.map (fun item -> item.Priority)
    |> List.maxBy (function Urgent -> 4 | High -> 3 | Medium -> 2 | Low -> 1)
```

**CRITICAL:**
```fsharp
// ❌ BAD - I/O in domain
let processItem itemId =
    let item = Persistence.getItem itemId  // NO!
    { item with Status = Processed }

// ✅ GOOD - Pure function
let processItem item =
    { item with Status = Processed }
```

## Layer 3: Persistence (`src/Server/Persistence.fs`)

**Purpose:** All database and file I/O operations

### SQLite with Dapper
```fsharp
module Persistence

open System.Data
open Microsoft.Data.Sqlite
open Dapper
open Shared.Domain

let connectionString = "Data Source=./data/app.db"
let getConnection () = new SqliteConnection(connectionString)

let initializeDatabase () =
    use conn = getConnection()
    conn.Execute("""
        CREATE TABLE IF NOT EXISTS TodoItems (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            Priority INTEGER NOT NULL,
            Status INTEGER NOT NULL,
            CreatedAt TEXT NOT NULL,
            UpdatedAt TEXT NOT NULL
        )
    """) |> ignore

// READ operations
let getAllTodos () : Async<TodoItem list> =
    async {
        use conn = getConnection()
        let! todos = conn.QueryAsync<TodoItem>(
            "SELECT * FROM TodoItems ORDER BY CreatedAt DESC"
        ) |> Async.AwaitTask
        return todos |> Seq.toList
    }

let getTodoById (id: int) : Async<TodoItem option> =
    async {
        use conn = getConnection()
        let! todo = conn.QuerySingleOrDefaultAsync<TodoItem>(
            "SELECT * FROM TodoItems WHERE Id = @Id",
            {| Id = id |}
        ) |> Async.AwaitTask
        return if isNull (box todo) then None else Some todo
    }

// WRITE operations
let insertTodo (todo: TodoItem) : Async<TodoItem> =
    async {
        use conn = getConnection()
        let! id = conn.ExecuteScalarAsync<int64>(
            """INSERT INTO TodoItems (Title, Description, Priority, Status, CreatedAt, UpdatedAt)
               VALUES (@Title, @Description, @Priority, @Status, @CreatedAt, @UpdatedAt)
               RETURNING Id""",
            {|
                Title = todo.Title
                Description = todo.Description
                Priority = int todo.Priority
                Status = int todo.Status
                CreatedAt = todo.CreatedAt.ToString("o")
                UpdatedAt = todo.UpdatedAt.ToString("o")
            |}
        ) |> Async.AwaitTask
        return { todo with Id = int id }
    }

let updateTodo (todo: TodoItem) : Async<unit> =
    async {
        use conn = getConnection()
        let! _ = conn.ExecuteAsync(
            """UPDATE TodoItems
               SET Title = @Title, Description = @Description,
                   Priority = @Priority, Status = @Status, UpdatedAt = @UpdatedAt
               WHERE Id = @Id""",
            todo
        ) |> Async.AwaitTask
        return ()
    }

let deleteTodo (id: int) : Async<unit> =
    async {
        use conn = getConnection()
        let! _ = conn.ExecuteAsync(
            "DELETE FROM TodoItems WHERE Id = @Id",
            {| Id = id |}
        ) |> Async.AwaitTask
        return ()
    }
```

**Key points:**
- Use parameterized queries (SQL injection prevention)
- Always use `async` for I/O
- Dispose connections (`use` keyword)
- Return options for "not found" cases

## Layer 4: API (`src/Server/Api.fs`)

**Purpose:** Implement Fable.Remoting contracts, orchestrate layers

### Pattern
```fsharp
module Api

open Fable.Remoting.Server
open Fable.Remoting.Giraffe
open Shared.Api
open Shared.Domain

let todoApi : ITodoApi = {
    getAll = fun () ->
        Persistence.getAllTodos()

    getById = fun id -> async {
        match! Persistence.getTodoById id with
        | Some todo -> return Ok todo
        | None -> return Error "Todo not found"
    }

    create = fun request -> async {
        // 1. Validate
        match Validation.validateCreateRequest request with
        | Error errors -> return Error (String.concat "; " errors)
        | Ok validRequest ->
            // 2. Process with domain logic
            let newTodo = Domain.processNewTodo validRequest

            // 3. Persist
            let! saved = Persistence.insertTodo newTodo
            return Ok saved
    }

    update = fun todo -> async {
        // 1. Validate
        match Validation.validateTodoItem todo with
        | Error errors -> return Error (String.concat "; " errors)
        | Ok validTodo ->
            // 2. Check exists
            match! Persistence.getTodoById todo.Id with
            | None -> return Error "Todo not found"
            | Some existing ->
                // 3. Process with domain logic
                let updated = Domain.updateTodo existing validTodo

                // 4. Persist
                do! Persistence.updateTodo updated
                return Ok updated
    }

    complete = fun id -> async {
        match! Persistence.getTodoById id with
        | None -> return Error "Todo not found"
        | Some todo ->
            let completed = Domain.completeTodo todo
            do! Persistence.updateTodo completed
            return Ok completed
    }

    delete = fun id -> async {
        do! Persistence.deleteTodo id
        return Ok ()
    }
}

// Create HTTP handler
let webApp =
    Remoting.createApi()
    |> Remoting.fromValue todoApi
    |> Remoting.buildHttpHandler
```

**Orchestration pattern:**
1. Validate input
2. Return error if invalid
3. Transform with domain logic (pure)
4. Perform persistence operations
5. Return result

### Error Handling Patterns

**Not Found:**
```fsharp
getById = fun id -> async {
    match! Persistence.getById id with
    | Some item -> return Ok item
    | None -> return Error "Not found"
}
```

**Validation Errors:**
```fsharp
save = fun item -> async {
    match Validation.validate item with
    | Error errs -> return Error (String.concat "; " errs)
    | Ok valid ->
        do! Persistence.save valid
        return Ok valid
}
```

**Exception Handling:**
```fsharp
save = fun item -> async {
    try
        do! Persistence.save item
        return Ok item
    with
    | ex -> return Error $"Failed to save: {ex.Message}"
}
```

## Integration with Program.fs

```fsharp
module Program

open Microsoft.AspNetCore.Builder
open Giraffe

let configureApp (app: IApplicationBuilder) =
    // Initialize persistence
    Persistence.ensureDataDir()
    Persistence.initializeDatabase()

    app.UseStaticFiles() |> ignore
    app.UseRouting() |> ignore
    app.UseGiraffe(Api.webApp)

[<EntryPoint>]
let main args =
    let builder = WebApplication.CreateBuilder(args)
    builder.Services.AddGiraffe() |> ignore

    let app = builder.Build()
    configureApp app
    app.Run()
    0
```

## Complete Example

```fsharp
// Validation.fs
module Validation
open Shared.Domain

let validateCreateRequest (req: CreateTodoRequest) =
    let errors = [
        if String.IsNullOrWhiteSpace(req.Title) then "Title required"
        if req.Title.Length > 100 then "Title too long"
    ]
    if errors.IsEmpty then Ok req else Error errors

// Domain.fs
module Domain
open System
open Shared.Domain

let processNewTodo (req: CreateTodoRequest) : TodoItem =
    {
        Id = 0
        Title = req.Title.Trim()
        Description = req.Description
        Priority = req.Priority
        Status = Active
        CreatedAt = DateTime.UtcNow
        UpdatedAt = DateTime.UtcNow
    }

// Persistence.fs (SQLite example above)

// Api.fs
module Api
open Shared.Api

let todoApi : ITodoApi = {
    create = fun request -> async {
        match Validation.validateCreateRequest request with
        | Error errs -> return Error (String.concat "; " errs)
        | Ok valid ->
            let todo = Domain.processNewTodo valid
            let! saved = Persistence.insertTodo todo
            return Ok saved
    }
}
```

## Verification Checklist

- [ ] Validation in `src/Server/Validation.fs`
- [ ] Domain logic in `src/Server/Domain.fs` (PURE - no I/O)
- [ ] Persistence in `src/Server/Persistence.fs`
- [ ] API implementation in `src/Server/Api.fs`
- [ ] Proper error handling (Result types)
- [ ] Database initialized (if using SQLite)
- [ ] All async operations used for I/O
- [ ] No I/O in domain layer
- [ ] Parameterized queries (SQL injection prevention)

## Common Pitfalls

❌ **Don't:**
- Put database calls in Domain.fs
- Skip validation
- Use string concatenation for SQL queries
- Forget to dispose database connections
- Mix concerns across layers

✅ **Do:**
- Keep domain logic pure
- Validate at API boundary
- Use parameterized queries
- Handle all error cases explicitly
- Follow layer responsibilities strictly

## Related Skills

- **fsharp-validation** - Detailed validation patterns
- **fsharp-persistence** - More persistence patterns
- **fsharp-tests** - Testing backend logic
- **fsharp-shared** - Type definitions

## Related Documentation

- `/docs/03-BACKEND-GUIDE.md` - Detailed backend guide
- `/docs/05-PERSISTENCE.md` - Persistence patterns
- `/docs/09-QUICK-REFERENCE.md` - Quick templates
