---
name: fsharp-routing
description: |
  Implement client-side routing with Feliz.Router for F# Elmish applications.
  Use when: "add routing", "create pages", "navigation", "URL handling", "deep linking",
  "add page", "route to", "browser history", "SPA routing", "multi-page", "navigate to".
  Creates route definitions, URL parsing, and navigation patterns in src/Client/.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# F# Client-Side Routing (Feliz.Router)

## When to Use This Skill

Activate when:
- User requests "add routing", "create pages", "add navigation"
- Need to handle URLs in the SPA
- Implementing multi-page application structure
- Adding deep linking support
- User mentions "navigate to", "route to", "URL handling"

## Architecture

```
URL Change
    ↓
Router.currentUrl() - Parse URL segments
    ↓
Route (Discriminated Union)
    ↓
Update function - Set current page
    ↓
View - Render page based on route
```

## Route Definition

### Define Routes as Discriminated Union

```fsharp
// src/Client/Types.fs (or State.fs)
module Types

type Route =
    | Home
    | Items
    | ItemDetail of id: int
    | NewItem
    | Settings
    | NotFound

module Route =
    /// Parse URL segments into Route
    let parse (segments: string list) : Route =
        match segments with
        | [] -> Home
        | [ "items" ] -> Items
        | [ "items"; "new" ] -> NewItem
        | [ "items"; Route.Int id ] -> ItemDetail id
        | [ "settings" ] -> Settings
        | _ -> NotFound

    /// Convert Route to URL path
    let toPath (route: Route) : string =
        match route with
        | Home -> "/"
        | Items -> "/items"
        | ItemDetail id -> $"/items/{id}"
        | NewItem -> "/items/new"
        | Settings -> "/settings"
        | NotFound -> "/not-found"
```

**Key points:**
- Routes are a discriminated union (exhaustive matching)
- `Route.Int` is a Feliz.Router active pattern for parsing integers
- Bidirectional: parse URLs and generate URLs

## State Integration

### Model with Current Route

```fsharp
// src/Client/State.fs
module State

open Elmish
open Feliz.Router
open Types

type Model = {
    CurrentRoute: Route
    Items: RemoteData<Item list>
    SelectedItem: RemoteData<Item>
    // ... other state
}

type Msg =
    | UrlChanged of string list
    | NavigateTo of Route
    | LoadItems
    | ItemsLoaded of Result<Item list, string>
    // ... other messages
```

### Init with Route Parsing

```fsharp
let init () : Model * Cmd<Msg> =
    let initialRoute = Router.currentUrl() |> Route.parse

    let model = {
        CurrentRoute = initialRoute
        Items = NotAsked
        SelectedItem = NotAsked
    }

    // Load data based on initial route
    let cmd =
        match initialRoute with
        | Home | Items -> Cmd.ofMsg LoadItems
        | ItemDetail id -> Cmd.ofMsg (LoadItem id)
        | _ -> Cmd.none

    model, cmd
```

### Update with Navigation

```fsharp
let update (msg: Msg) (model: Model) : Model * Cmd<Msg> =
    match msg with
    | UrlChanged segments ->
        let route = Route.parse segments
        let model = { model with CurrentRoute = route }

        // Trigger data loading for new route
        let cmd =
            match route with
            | Items -> Cmd.ofMsg LoadItems
            | ItemDetail id -> Cmd.ofMsg (LoadItem id)
            | _ -> Cmd.none

        model, cmd

    | NavigateTo route ->
        // Programmatic navigation
        let path = Route.toPath route
        model, Cmd.navigatePath path

    | LoadItems ->
        // ... existing logic
```

## View with Router

### Main App with Router

```fsharp
// src/Client/App.fs
module App

open Feliz
open Feliz.Router
open State
open View

[<ReactComponent>]
let App () =
    let model, dispatch = React.useElmish(init, update, [| |])

    React.router [
        router.onUrlChanged (UrlChanged >> dispatch)
        router.children [
            view model dispatch
        ]
    ]
```

### Page-Based View

```fsharp
// src/Client/View.fs
module View

open Feliz
open Types
open State

let private navbar (dispatch: Msg -> unit) =
    Html.nav [
        prop.className "navbar bg-base-100 shadow-lg"
        prop.children [
            Html.div [
                prop.className "flex-1"
                prop.children [
                    Html.a [
                        prop.className "btn btn-ghost text-xl"
                        prop.href (Router.format [])
                        prop.text "Home"
                    ]
                ]
            ]
            Html.div [
                prop.className "flex-none"
                prop.children [
                    Html.ul [
                        prop.className "menu menu-horizontal px-1"
                        prop.children [
                            Html.li [
                                Html.a [
                                    prop.href (Router.format [ "items" ])
                                    prop.text "Items"
                                ]
                            ]
                            Html.li [
                                Html.a [
                                    prop.href (Router.format [ "settings" ])
                                    prop.text "Settings"
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]

let private homePage (model: Model) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "hero min-h-screen bg-base-200"
        prop.children [
            Html.div [
                prop.className "hero-content text-center"
                prop.children [
                    Html.h1 [ prop.className "text-5xl font-bold"; prop.text "Welcome" ]
                    Html.p [ prop.className "py-6"; prop.text "Your home page content" ]
                    Html.button [
                        prop.className "btn btn-primary"
                        prop.text "View Items"
                        prop.onClick (fun _ -> dispatch (NavigateTo Items))
                    ]
                ]
            ]
        ]
    ]

let private itemsPage (model: Model) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "container mx-auto p-4"
        prop.children [
            Html.h1 [ prop.className "text-3xl font-bold mb-4"; prop.text "Items" ]

            match model.Items with
            | NotAsked -> Html.button [
                prop.className "btn btn-primary"
                prop.text "Load Items"
                prop.onClick (fun _ -> dispatch LoadItems)
              ]
            | Loading -> Html.span [ prop.className "loading loading-spinner" ]
            | Success items ->
                Html.div [
                    prop.className "grid grid-cols-3 gap-4"
                    prop.children [
                        for item in items ->
                            Html.div [
                                prop.className "card bg-base-100 shadow"
                                prop.children [
                                    Html.div [
                                        prop.className "card-body"
                                        prop.children [
                                            Html.h2 [ prop.className "card-title"; prop.text item.Name ]
                                            Html.a [
                                                prop.className "btn btn-sm btn-primary"
                                                prop.href (Router.format [ "items"; string item.Id ])
                                                prop.text "View"
                                            ]
                                        ]
                                    ]
                                ]
                            ]
                    ]
                ]
            | Failure err -> Html.div [ prop.className "alert alert-error"; prop.text err ]
        ]
    ]

let private itemDetailPage (id: int) (model: Model) (dispatch: Msg -> unit) =
    Html.div [
        prop.className "container mx-auto p-4"
        prop.children [
            Html.a [
                prop.className "btn btn-ghost mb-4"
                prop.href (Router.format [ "items" ])
                prop.text "< Back to Items"
            ]

            match model.SelectedItem with
            | NotAsked | Loading -> Html.span [ prop.className "loading loading-spinner" ]
            | Success item ->
                Html.div [
                    Html.h1 [ prop.className "text-3xl font-bold"; prop.text item.Name ]
                    // ... item details
                ]
            | Failure err -> Html.div [ prop.className "alert alert-error"; prop.text err ]
        ]
    ]

let private notFoundPage () =
    Html.div [
        prop.className "hero min-h-screen bg-base-200"
        prop.children [
            Html.div [
                prop.className "hero-content text-center"
                prop.children [
                    Html.h1 [ prop.className "text-5xl font-bold"; prop.text "404" ]
                    Html.p [ prop.className "py-6"; prop.text "Page not found" ]
                    Html.a [
                        prop.className "btn btn-primary"
                        prop.href (Router.format [])
                        prop.text "Go Home"
                    ]
                ]
            ]
        ]
    ]

let view (model: Model) (dispatch: Msg -> unit) =
    Html.div [
        navbar dispatch

        Html.main [
            prop.className "min-h-screen"
            prop.children [
                match model.CurrentRoute with
                | Home -> homePage model dispatch
                | Items -> itemsPage model dispatch
                | ItemDetail id -> itemDetailPage id model dispatch
                | NewItem -> Html.div "New Item Form"
                | Settings -> Html.div "Settings Page"
                | NotFound -> notFoundPage ()
            ]
        ]
    ]
```

## Navigation Patterns

### Link Navigation (Declarative)

```fsharp
// Simple link
Html.a [
    prop.href (Router.format [ "items" ])
    prop.text "Items"
]

// Link with parameters
Html.a [
    prop.href (Router.format [ "items"; string itemId ])
    prop.text "View Item"
]

// Styled as button
Html.a [
    prop.className "btn btn-primary"
    prop.href (Router.format [ "items"; "new" ])
    prop.text "Create Item"
]
```

### Programmatic Navigation

```fsharp
// Via message dispatch
Html.button [
    prop.onClick (fun _ -> dispatch (NavigateTo (ItemDetail 42)))
    prop.text "Go to Item 42"
]

// In update function
| SaveCompleted (Ok item) ->
    model, Cmd.navigatePath (Route.toPath (ItemDetail item.Id))

| DeleteCompleted (Ok _) ->
    model, Cmd.navigatePath "/items"
```

### URL Helpers

```fsharp
// Format URL segments
Router.format [ "items" ]                    // "/items"
Router.format [ "items"; "123" ]             // "/items/123"
Router.format [ "items"; "new" ]             // "/items/new"

// With query parameters
Router.format ([ "items" ], [ "page", "2"; "sort", "name" ])
// "/items?page=2&sort=name"

// Navigate command
Cmd.navigatePath "/items"
Cmd.navigatePath (Router.format [ "items"; string id ])
```

## Active Patterns for Parsing

```fsharp
// Built-in active patterns from Feliz.Router
match segments with
| [ "items"; Route.Int id ] -> ItemDetail id      // Parse int
| [ "users"; Route.Guid guid ] -> UserDetail guid // Parse GUID
| [ "date"; Route.Date d ] -> DateView d          // Parse date

// Custom active pattern
let (|Slug|_|) (s: string) =
    if s.Length > 0 && s |> Seq.forall (fun c -> Char.IsLetterOrDigit c || c = '-')
    then Some s
    else None

match segments with
| [ "posts"; Slug slug ] -> PostBySlug slug
| _ -> NotFound
```

## Query Parameters

```fsharp
// Parse query parameters
let parseWithQuery (segments: string list) (query: Map<string, string>) : Route * QueryParams =
    let route = Route.parse segments
    let page = query |> Map.tryFind "page" |> Option.bind Int32.TryParse |> Option.defaultValue 1
    let sort = query |> Map.tryFind "sort" |> Option.defaultValue "date"
    route, { Page = page; Sort = sort }

// In update
| UrlChanged segments ->
    let query = Router.currentQuery() |> Map.ofList
    let route, params = parseWithQuery segments query
    { model with CurrentRoute = route; QueryParams = params }, Cmd.none
```

## Verification Checklist

- [ ] Route discriminated union defined
- [ ] `Route.parse` handles all URL patterns
- [ ] `Route.toPath` generates correct URLs
- [ ] `React.router` wraps the app
- [ ] `router.onUrlChanged` dispatches to update
- [ ] Init parses initial URL
- [ ] Update handles `UrlChanged` message
- [ ] View renders based on `CurrentRoute`
- [ ] Links use `Router.format`
- [ ] Programmatic navigation uses `Cmd.navigatePath`
- [ ] 404/NotFound route handled

## Common Pitfalls

**Don't:**
- Hardcode URL strings in multiple places
- Forget to handle the initial URL in `init`
- Skip the NotFound case
- Use `window.location` directly

**Do:**
- Define routes as discriminated union
- Use `Router.format` for all URLs
- Handle route changes in update
- Load data based on route
- Provide back navigation

## Related Skills

- **fsharp-frontend** - State and view patterns
- **fsharp-shared** - Types for route parameters
- **fsharp-feature** - Full feature with routing

## Related Documentation

- `/docs/02-FRONTEND-GUIDE.md` - Frontend patterns
- [Feliz.Router Documentation](https://zaid-ajaj.github.io/Feliz/#/Feliz.Router/Overview)
