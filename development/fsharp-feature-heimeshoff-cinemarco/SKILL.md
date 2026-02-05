---
name: fsharp-feature
description: |
  Orchestrates end-to-end F# full-stack feature development across all layers.
  Use when: "add feature", "implement X", "build Y", "create new feature", "full stack",
  "new functionality", "add capability", "implement end-to-end", "complete feature".
  Guides through: Shared types → Backend → Frontend → Tests.
  Use this for features that touch multiple layers of the application.
---

# F# Full-Stack Feature Development

## When to Use This Skill

Activate when:
- User requests complete new feature ("add todo feature", "implement user management")
- Need structured guidance through entire stack
- Building feature from scratch with types, backend, frontend, and tests
- Project follows F# full-stack blueprint with Elmish + Giraffe

## Prerequisites

Project structure:
```
src/
├── Shared/        # Domain types and API contracts
├── Server/        # Giraffe backend
├── Client/        # Elmish.React + Feliz frontend
└── Tests/         # Expecto tests
```

## Development Process

### 1. Read Documentation First

Before implementing any feature:
```bash
# Check for project-specific patterns
Read: /docs/README.md
Read: /docs/09-QUICK-REFERENCE.md
Read: CLAUDE.md
```

### 2. Define Shared Contracts

**Location**: `src/Shared/`

Define domain types in `Domain.fs`:
```fsharp
module Shared.Domain

open System

type TodoItem = {
    Id: int
    Title: string
    Description: string option
    Priority: Priority
    Status: TodoStatus
    CreatedAt: DateTime
    UpdatedAt: DateTime
}

and Priority = Low | Medium | High | Urgent
and TodoStatus = Active | Completed
```

Define API contract in `Api.fs`:
```fsharp
module Shared.Api

open Domain

type ITodoApi = {
    getAll: unit -> Async<TodoItem list>
    getById: int -> Async<Result<TodoItem, string>>
    create: CreateTodoRequest -> Async<Result<TodoItem, string>>
    update: TodoItem -> Async<Result<TodoItem, string>>
    delete: int -> Async<Result<unit, string>>
}

type CreateTodoRequest = {
    Title: string
    Description: string option
    Priority: Priority
}
```

### 3. Implement Backend

**Location**: `src/Server/`

**Step 3a: Validation** (`Validation.fs`)
```fsharp
module Validation

let validateCreateRequest (req: CreateTodoRequest) =
    let errors = [
        if String.IsNullOrWhiteSpace(req.Title) then "Title required"
        if req.Title.Length > 100 then "Title too long"
    ]
    if errors.IsEmpty then Ok req else Error errors
```

**Step 3b: Domain Logic** (`Domain.fs` - PURE, NO I/O)
```fsharp
module Domain

open System
open Shared.Domain

let processNewTodo (req: CreateTodoRequest) : TodoItem =
    {
        Id = 0  // Set by persistence
        Title = req.Title.Trim()
        Description = req.Description |> Option.map (fun d -> d.Trim())
        Priority = req.Priority
        Status = Active
        CreatedAt = DateTime.UtcNow
        UpdatedAt = DateTime.UtcNow
    }

let completeTodo (todo: TodoItem) : TodoItem =
    { todo with Status = Completed; UpdatedAt = DateTime.UtcNow }
```

**Step 3c: Persistence** (`Persistence.fs`)
```fsharp
module Persistence

open Dapper
open Microsoft.Data.Sqlite
open Shared.Domain

let connectionString = "Data Source=./data/app.db"
let getConnection () = new SqliteConnection(connectionString)

let getAllTodos () : Async<TodoItem list> =
    async {
        use conn = getConnection()
        let! todos = conn.QueryAsync<TodoItem>(
            "SELECT * FROM TodoItems ORDER BY CreatedAt DESC"
        ) |> Async.AwaitTask
        return todos |> Seq.toList
    }

let insertTodo (todo: TodoItem) : Async<TodoItem> =
    async {
        use conn = getConnection()
        let! id = conn.ExecuteScalarAsync<int64>(
            """INSERT INTO TodoItems (Title, Description, Priority, Status, CreatedAt, UpdatedAt)
               VALUES (@Title, @Description, @Priority, @Status, @CreatedAt, @UpdatedAt)
               RETURNING Id""",
            todo
        ) |> Async.AwaitTask
        return { todo with Id = int id }
    }
```

**Step 3d: API Implementation** (`Api.fs`)
```fsharp
module Api

open Fable.Remoting.Server
open Fable.Remoting.Giraffe
open Shared.Api

let todoApi : ITodoApi = {
    getAll = Persistence.getAllTodos

    getById = fun id -> async {
        match! Persistence.getTodoById id with
        | Some todo -> return Ok todo
        | None -> return Error "Not found"
    }

    create = fun request -> async {
        match Validation.validateCreateRequest request with
        | Error errs -> return Error (String.concat "; " errs)
        | Ok valid ->
            let todo = Domain.processNewTodo valid
            let! saved = Persistence.insertTodo todo
            return Ok saved
    }
}

let webApp =
    Remoting.createApi()
    |> Remoting.fromValue todoApi
    |> Remoting.buildHttpHandler
```

### 4. Implement Frontend

**Location**: `src/Client/`

**Step 4a: State Management** (`State.fs`)
```fsharp
module State

open Elmish
open Shared.Domain
open Types

type Model = {
    Todos: RemoteData<TodoItem list>
    NewTodoTitle: string
    NewTodoDescription: string
}

type Msg =
    | LoadTodos
    | TodosLoaded of Result<TodoItem list, string>
    | UpdateNewTodoTitle of string
    | UpdateNewTodoDescription of string
    | CreateTodo
    | TodoCreated of Result<TodoItem, string>

let init () : Model * Cmd<Msg> =
    let model = {
        Todos = NotAsked
        NewTodoTitle = ""
        NewTodoDescription = ""
    }
    model, Cmd.ofMsg LoadTodos

let update (msg: Msg) (model: Model) : Model * Cmd<Msg> =
    match msg with
    | LoadTodos ->
        let cmd = Cmd.OfAsync.either
            Api.todoApi.getAll ()
            (Ok >> TodosLoaded)
            (fun ex -> Error ex.Message |> TodosLoaded)
        { model with Todos = Loading }, cmd

    | TodosLoaded (Ok todos) ->
        { model with Todos = Success todos }, Cmd.none

    | TodosLoaded (Error err) ->
        { model with Todos = Failure err }, Cmd.none

    | UpdateNewTodoTitle title ->
        { model with NewTodoTitle = title }, Cmd.none

    | UpdateNewTodoDescription desc ->
        { model with NewTodoDescription = desc }, Cmd.none

    | CreateTodo ->
        let request = {
            Title = model.NewTodoTitle
            Description = if String.IsNullOrWhiteSpace(model.NewTodoDescription)
                         then None else Some model.NewTodoDescription
            Priority = Medium
        }
        let cmd = Cmd.OfAsync.either
            Api.todoApi.create request
            TodoCreated
            (fun ex -> Error ex.Message |> TodoCreated)
        model, cmd

    | TodoCreated (Ok _) ->
        { model with NewTodoTitle = ""; NewTodoDescription = "" },
        Cmd.ofMsg LoadTodos

    | TodoCreated (Error _) ->
        model, Cmd.none
```

**Step 4b: View** (`View.fs`)
```fsharp
module View

open Feliz
open State
open Types

let private todoCard (todo: TodoItem) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "card bg-base-100 shadow-xl"
        prop.children [
            Html.div [
                prop.className "card-body"
                prop.children [
                    Html.h2 [ prop.className "card-title"; prop.text todo.Title ]
                    match todo.Description with
                    | Some desc -> Html.p [ prop.text desc ]
                    | None -> Html.none
                ]
            ]
        ]
    ]

let view (model: Model) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "container mx-auto p-4"
        prop.children [
            Html.h1 [ prop.className "text-4xl font-bold mb-8"; prop.text "Todos" ]

            // Form
            Html.input [
                prop.className "input input-bordered w-full mb-2"
                prop.placeholder "Title"
                prop.value model.NewTodoTitle
                prop.onChange (UpdateNewTodoTitle >> dispatch)
            ]
            Html.button [
                prop.className "btn btn-primary"
                prop.text "Create"
                prop.onClick (fun _ -> dispatch CreateTodo)
            ]

            // List
            match model.Todos with
            | NotAsked -> Html.div "Loading..."
            | Loading -> Html.span [ prop.className "loading loading-spinner" ]
            | Success todos ->
                Html.div [
                    prop.className "grid grid-cols-3 gap-4 mt-8"
                    prop.children [ for todo in todos -> todoCard todo dispatch ]
                ]
            | Failure err -> Html.div [ prop.className "alert alert-error"; prop.text err ]
        ]
    ]
```

### 5. Write Tests

**Location**: `src/Tests/`

```fsharp
module Tests.TodoTests

open Expecto
open Shared.Domain

[<Tests>]
let tests =
    testList "Todo Feature" [
        testList "Domain" [
            testCase "processNewTodo trims title" <| fun () ->
                let request = { Title = "  Test  "; Description = None; Priority = Low }
                let result = Domain.processNewTodo request
                Expect.equal result.Title "Test" "Should trim"

            testCase "completeTodo changes status" <| fun () ->
                let todo = { baseTodo with Status = Active }
                let result = Domain.completeTodo todo
                Expect.equal result.Status Completed "Should be completed"
        ]

        testList "Validation" [
            testCase "validates empty title" <| fun () ->
                let request = { Title = ""; Description = None; Priority = Low }
                let result = Validation.validateCreateRequest request
                Expect.isError result "Should fail"
        ]
    ]
```

## Key Principles

**Critical Rules:**
1. **Type Safety** - Define all types in `src/Shared/Domain.fs` first
2. **Pure Domain** - NO I/O in `src/Server/Domain.fs` (pure functions only)
3. **MVU Pattern** - All state changes through `update` function
4. **Explicit Errors** - Use `Result<'T, string>` for fallible operations
5. **Validate Early** - At API boundary before any processing
6. **RemoteData** - Use for async operations in frontend state

**Development Order:**
```
Shared Types → Backend (Validation → Domain → Persistence → API) → Frontend (State → View) → Tests
```

## Verification Checklist

Before marking feature complete:
- [ ] Types defined in `src/Shared/Domain.fs`
- [ ] API contract in `src/Shared/Api.fs`
- [ ] Validation in `src/Server/Validation.fs`
- [ ] Domain logic pure (no I/O) in `src/Server/Domain.fs`
- [ ] Persistence in `src/Server/Persistence.fs`
- [ ] API implementation in `src/Server/Api.fs`
- [ ] Frontend state (Model/Msg/update) in `src/Client/State.fs`
- [ ] Frontend view in `src/Client/View.fs`
- [ ] Tests written (minimum: domain + validation)
- [ ] `dotnet build` succeeds
- [ ] `dotnet test` passes

## Common Pitfalls

❌ **Don't:**
- Put I/O operations in Domain.fs
- Skip validation
- Use classes for domain types (use records)
- Ignore Result/RemoteData error states
- Start coding without defining types first

✅ **Do:**
- Read documentation first
- Define types before implementation
- Keep domain logic pure
- Handle all error cases explicitly
- Test domain logic thoroughly

## Related Skills

For deeper implementation:
- **fsharp-shared** - Detailed type patterns
- **fsharp-backend** - Backend layer details
- **fsharp-frontend** - Frontend patterns
- **fsharp-validation** - Complex validation
- **fsharp-persistence** - Database patterns
- **fsharp-tests** - Testing patterns
