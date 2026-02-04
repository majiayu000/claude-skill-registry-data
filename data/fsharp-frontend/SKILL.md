---
name: fsharp-frontend
description: |
  Implement F# frontend using Elmish MVU architecture with Feliz for React components.
  Use when: "add UI", "create component", "build form", "frontend", "client-side", "user interface",
  "view", "display", "render", "Elmish", "Feliz", "button", "input", "state management".
  Creates Model/Msg/update in src/Client/State.fs and views in src/Client/View.fs.
  Follows strict MVU pattern with RemoteData for async operations and TailwindCSS/DaisyUI for styling.
allowed-tools: Read, Edit, Write, Grep
---

# F# Frontend Implementation (Elmish + Feliz)

## When to Use This Skill

Activate when:
- User requests "add UI for X", "create component for Y"
- Implementing client-side functionality
- Managing application state
- Creating interactive features
- Project uses Elmish.React + Feliz

## MVU Architecture

```
View (user sees UI)
    ↓ (user action)
Msg (message describing action)
    ↓
Update (pure state transition)
    ↓ (optional)
Cmd (side effects like API calls)
    ↓ (result)
Msg (result wrapped in message)
    ↓
Update → new Model
    ↓
View (re-renders with new model)
```

## Client Types (`src/Client/Types.fs`)

### RemoteData Pattern
```fsharp
module Types

type RemoteData<'T> =
    | NotAsked
    | Loading
    | Success of 'T
    | Failure of string
```

This represents the state of async operations:
- **NotAsked** - Haven't requested yet
- **Loading** - Request in progress
- **Success** - Request succeeded with data
- **Failure** - Request failed with error message

## State Management (`src/Client/State.fs`)

### 1. Model (Application State)

```fsharp
module State

open Elmish
open Shared.Domain
open Types

type Model = {
    // Data from server
    Todos: RemoteData<TodoItem list>
    CurrentTodo: RemoteData<TodoItem>

    // Form inputs
    NewTodoTitle: string
    NewTodoDescription: string
    SelectedPriority: Priority

    // UI state
    IsFormVisible: bool
}
```

**Key points:**
- Use `RemoteData<'T>` for async operations
- Separate form state from loaded data
- Include UI state (modals, dropdowns, etc.)

### 2. Messages (State Transitions)

```fsharp
type Msg =
    // Load todos
    | LoadTodos
    | TodosLoaded of Result<TodoItem list, string>

    // Load single todo
    | LoadTodo of int
    | TodoLoaded of Result<TodoItem, string>

    // Create todo
    | UpdateNewTodoTitle of string
    | UpdateNewTodoDescription of string
    | UpdateSelectedPriority of Priority
    | CreateTodo
    | TodoCreated of Result<TodoItem, string>

    // Update todo
    | CompleteTodo of int
    | TodoCompleted of Result<TodoItem, string>

    // Delete todo
    | DeleteTodo of int
    | TodoDeleted of Result<unit, string>

    // UI actions
    | ToggleForm
```

**Pattern:**
- Action message (user intent)
- Result message (API response)

### 3. Init Function

```fsharp
let init () : Model * Cmd<Msg> =
    let model = {
        Todos = NotAsked
        CurrentTodo = NotAsked
        NewTodoTitle = ""
        NewTodoDescription = ""
        SelectedPriority = Medium
        IsFormVisible = false
    }
    let cmd = Cmd.ofMsg LoadTodos
    model, cmd
```

### 4. Update Function

```fsharp
let update (msg: Msg) (model: Model) : Model * Cmd<Msg> =
    match msg with
    | LoadTodos ->
        let cmd =
            Cmd.OfAsync.either
                Api.todoApi.getAll
                ()
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

    | UpdateSelectedPriority priority ->
        { model with SelectedPriority = priority }, Cmd.none

    | CreateTodo ->
        let request = {
            Title = model.NewTodoTitle
            Description =
                if String.IsNullOrWhiteSpace(model.NewTodoDescription)
                then None
                else Some model.NewTodoDescription
            Priority = model.SelectedPriority
        }
        let cmd =
            Cmd.OfAsync.either
                Api.todoApi.create
                request
                TodoCreated
                (fun ex -> Error ex.Message |> TodoCreated)
        model, cmd

    | TodoCreated (Ok _) ->
        // Reset form and reload
        { model with
            NewTodoTitle = ""
            NewTodoDescription = ""
            SelectedPriority = Medium
            IsFormVisible = false },
        Cmd.ofMsg LoadTodos

    | TodoCreated (Error err) ->
        model, Cmd.none  // Could add error to model

    | CompleteTodo id ->
        let cmd =
            Cmd.OfAsync.either
                Api.todoApi.complete
                id
                TodoCompleted
                (fun ex -> Error ex.Message |> TodoCompleted)
        model, cmd

    | TodoCompleted (Ok _) ->
        model, Cmd.ofMsg LoadTodos

    | TodoCompleted (Error _) ->
        model, Cmd.none

    | DeleteTodo id ->
        let cmd =
            Cmd.OfAsync.either
                Api.todoApi.delete
                id
                (fun _ -> Ok () |> TodoDeleted)
                (fun ex -> Error ex.Message |> TodoDeleted)
        model, cmd

    | TodoDeleted (Ok _) ->
        model, Cmd.ofMsg LoadTodos

    | TodoDeleted (Error _) ->
        model, Cmd.none

    | ToggleForm ->
        { model with IsFormVisible = not model.IsFormVisible }, Cmd.none
```

## View Components (`src/Client/View.fs`)

### Basic Component

```fsharp
module View

open Feliz
open Shared.Domain
open State
open Types

let private todoCard (todo: TodoItem) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "card bg-base-100 shadow-xl"
        prop.children [
            Html.div [
                prop.className "card-body"
                prop.children [
                    Html.h2 [
                        prop.className "card-title"
                        prop.text todo.Title
                    ]

                    match todo.Description with
                    | Some desc ->
                        Html.p [
                            prop.className "text-sm text-gray-600"
                            prop.text desc
                        ]
                    | None -> Html.none

                    Html.div [
                        prop.className "badge badge-primary"
                        prop.text (string todo.Priority)
                    ]

                    Html.div [
                        prop.className "card-actions justify-end"
                        prop.children [
                            if todo.Status = Active then
                                Html.button [
                                    prop.className "btn btn-success btn-sm"
                                    prop.text "Complete"
                                    prop.onClick (fun _ -> dispatch (CompleteTodo todo.Id))
                                ]

                            Html.button [
                                prop.className "btn btn-error btn-sm"
                                prop.text "Delete"
                                prop.onClick (fun _ -> dispatch (DeleteTodo todo.Id))
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]
```

### Form Component

```fsharp
let private createTodoForm (model: Model) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "card bg-base-200 mb-8"
        prop.children [
            Html.div [
                prop.className "card-body"
                prop.children [
                    Html.h3 [
                        prop.className "card-title"
                        prop.text "Create New Todo"
                    ]

                    Html.input [
                        prop.className "input input-bordered w-full mb-2"
                        prop.type' "text"
                        prop.placeholder "Title"
                        prop.value model.NewTodoTitle
                        prop.onChange (UpdateNewTodoTitle >> dispatch)
                    ]

                    Html.textarea [
                        prop.className "textarea textarea-bordered w-full mb-2"
                        prop.placeholder "Description (optional)"
                        prop.value model.NewTodoDescription
                        prop.onChange (UpdateNewTodoDescription >> dispatch)
                    ]

                    Html.select [
                        prop.className "select select-bordered w-full mb-2"
                        prop.value (string model.SelectedPriority)
                        prop.onChange (fun (value: string) ->
                            let priority =
                                match value with
                                | "Low" -> Low
                                | "High" -> High
                                | "Urgent" -> Urgent
                                | _ -> Medium
                            dispatch (UpdateSelectedPriority priority))
                        prop.children [
                            Html.option [ prop.value "Low"; prop.text "Low" ]
                            Html.option [ prop.value "Medium"; prop.text "Medium" ]
                            Html.option [ prop.value "High"; prop.text "High" ]
                            Html.option [ prop.value "Urgent"; prop.text "Urgent" ]
                        ]
                    ]

                    Html.button [
                        prop.className "btn btn-primary"
                        prop.text "Create"
                        prop.onClick (fun _ -> dispatch CreateTodo)
                        prop.disabled (String.IsNullOrWhiteSpace(model.NewTodoTitle))
                    ]
                ]
            ]
        ]
    ]
```

### RemoteData View Pattern

```fsharp
let private todosView (remoteData: RemoteData<TodoItem list>) (dispatch: Msg -> unit) =
    match remoteData with
    | NotAsked ->
        Html.div [
            prop.className "text-center p-8"
            prop.children [
                Html.button [
                    prop.className "btn btn-primary"
                    prop.text "Load Todos"
                    prop.onClick (fun _ -> dispatch LoadTodos)
                ]
            ]
        ]

    | Loading ->
        Html.div [
            prop.className "flex justify-center items-center p-8"
            prop.children [
                Html.span [ prop.className "loading loading-spinner loading-lg" ]
            ]
        ]

    | Success todos when todos.IsEmpty ->
        Html.div [
            prop.className "alert alert-info"
            prop.text "No todos yet. Create one above!"
        ]

    | Success todos ->
        Html.div [
            prop.className "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
            prop.children [
                for todo in todos -> todoCard todo dispatch
            ]
        ]

    | Failure error ->
        Html.div [
            prop.className "alert alert-error"
            prop.children [
                Html.span [ prop.text $"Error: {error}" ]
                Html.button [
                    prop.className "btn btn-sm"
                    prop.text "Retry"
                    prop.onClick (fun _ -> dispatch LoadTodos)
                ]
            ]
        ]
```

### Main View

```fsharp
let view (model: Model) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "container mx-auto p-4"
        prop.children [
            Html.h1 [
                prop.className "text-4xl font-bold mb-8"
                prop.text "Todo App"
            ]

            createTodoForm model dispatch

            todosView model.Todos dispatch
        ]
    ]
```

## Common Patterns

### Loading States
```fsharp
match model.Data with
| NotAsked -> Html.div "Click to load"
| Loading -> Html.span [ prop.className "loading loading-spinner" ]
| Success data -> // render data
| Failure err -> Html.div [ prop.className "alert alert-error"; prop.text err ]
```

### Form Input
```fsharp
Html.input [
    prop.value model.InputValue
    prop.onChange (fun (value: string) -> dispatch (UpdateInput value))
]
```

### Button Click
```fsharp
Html.button [
    prop.onClick (fun _ -> dispatch SaveData)
    prop.text "Save"
]
```

### Conditional Rendering
```fsharp
if condition then
    Html.div "Show this"
else
    Html.none
```

### Lists
```fsharp
Html.ul [
    prop.children [
        for item in items -> Html.li [ prop.text item.Name ]
    ]
]
```

## TailwindCSS + DaisyUI Classes

**Layout:**
- Container: `container mx-auto p-4`
- Grid: `grid grid-cols-3 gap-4`
- Flex: `flex justify-center items-center`

**Components (DaisyUI):**
- Button: `btn btn-primary btn-sm`
- Card: `card bg-base-100 shadow-xl`
- Input: `input input-bordered w-full`
- Alert: `alert alert-error`
- Badge: `badge badge-primary`
- Loading: `loading loading-spinner loading-lg`

## Verification Checklist

- [ ] RemoteData type in `src/Client/Types.fs`
- [ ] API client in `src/Client/Api.fs`
- [ ] Model defined in `src/Client/State.fs`
- [ ] Messages defined
- [ ] Init function
- [ ] Update function handles all messages
- [ ] View components in `src/Client/View.fs`
- [ ] RemoteData pattern used
- [ ] Proper error handling in views
- [ ] TailwindCSS/DaisyUI styling

## Common Pitfalls

❌ **Don't:**
- Mutate model (always return new)
- Put side effects in update (use Cmd)
- Skip handling error states
- Forget to dispatch messages
- Mix logic in view functions

✅ **Do:**
- Keep update pure
- Use Cmd for side effects
- Handle all RemoteData states
- Use dispatch for all user actions
- Keep views simple and composable

## Related Skills

- **fsharp-shared** - Type definitions
- **fsharp-backend** - API to call
- **fsharp-tests** - Test state transitions

## Related Documentation

- `/docs/02-FRONTEND-GUIDE.md` - Detailed frontend guide
- `/docs/09-QUICK-REFERENCE.md` - Quick templates
