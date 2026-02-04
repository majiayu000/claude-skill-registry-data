---
name: g-sui
description: Server-rendered Go UI framework. Use when building g-sui applications, creating UI components, handling forms with server actions, using data tables, setting up routes, or implementing WebSocket patches. Triggered by "g-sui", "server-rendered UI", "Go UI framework", form handling, or data collation.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# g-sui Framework

Server-rendered UI framework for Go. All HTML generation, business logic, and state management occur on the server. Interactivity achieved through server actions and WebSocket patches.

## Quick Start

```go
package main

import "github.com/michalCapo/g-sui/ui"

func main() {
    app := ui.MakeApp("en")

    app.Page("/", func(ctx *ui.Context) string {
        return app.HTML("Home", "bg-gray-100",
            ui.Div("p-8")(
                ui.Div("text-2xl font-bold")("Hello World"),
            ),
        )
    })

    app.Listen(":8080")
}
```

## Documentation Index

| Topic | File | Description |
|-------|------|-------------|
| Core Concepts | [CORE.md](CORE.md) | Architecture, Context, Actions, Targets, server rendering |
| UI Components | [COMPONENTS.md](COMPONENTS.md) | Buttons, inputs, forms, tables, alerts, cards, tabs, etc. |
| Data Management | [DATA.md](DATA.md) | Data collation, search, sort, filter, pagination, Excel export |
| Server Setup | [SERVER.md](SERVER.md) | App initialization, routes, WebSocket, PWA, assets |
| Best Practices | [PATTERNS.md](PATTERNS.md) | Testing, validation, security, state management |

## Core Philosophy

1. **Server-Centric Rendering** - All HTML generated server-side as strings
2. **String-Based Components** - Components are Go functions returning HTML strings
3. **Action-Based Interactivity** - User interactions trigger server handlers returning HTML
4. **WebSocket-Enhanced** - Real-time updates via `/__ws` endpoint

## Key Types

```go
type Callable = func(*ui.Context) string  // All handlers return HTML
type Attr struct { ID, Class, Value, OnClick, OnSubmit, ... }  // HTML attributes
```

## Common Imports

```go
import "github.com/michalCapo/g-sui/ui"
```

## Development Commands

```bash
go run examples/main.go      # Run example app
go test ./...                # Run all tests
go test ./ui/...             # Test UI package
go build                     # Build project
./deploy                     # Create and push new version tag
```

## Releases

To create a new version release:

```bash
./deploy
```

The `deploy` script automatically:
- Starts at version `v0.100` if no tags exist
- Increments the minor version by 1 (e.g., `v0.100` → `v0.101` → `v0.102`)
- Ensures working tree is clean before tagging
- Creates an annotated git tag and pushes to remote

Version numbering: `v0.XXX` format, auto-incremented from `v0.100`.
