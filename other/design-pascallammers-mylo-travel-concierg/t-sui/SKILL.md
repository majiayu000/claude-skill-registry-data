---
name: t-sui
description: Server-rendered TypeScript UI framework. Use when building t-sui applications, creating UI components, handling forms with server actions, using data tables, setting up routes, or implementing WebSocket patches. Triggered by "t-sui", "server-rendered UI", "TypeScript UI framework", form handling, or data collation.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# t-sui Framework

Server-rendered UI framework for TypeScript. All HTML generation, business logic, and state management occur on the server. Interactivity achieved through server actions and WebSocket patches.

## Quick Start

```typescript
import ui from "./ui";
import { MakeApp, Context } from "./ui.server";

const app = MakeApp("en");

app.Page("/", function(ctx: Context): string {
    return app.HTML("Home", "bg-gray-100",
        ui.Div("p-8")(
            ui.Div("text-2xl font-bold")("Hello World"),
        ),
    );
});

app.Listen(1423);
```

## Documentation Index

| Topic | File | Description |
|-------|------|-------------|
| Core Concepts | [CORE.md](CORE.md) | Architecture, Context, Actions, Targets, server rendering |
| UI Components | [COMPONENTS.md](COMPONENTS.md) | Buttons, inputs, forms, tables, alerts, cards, tabs, etc. |
| Data Management | [DATA.md](DATA.md) | Data collation, search, sort, filter, pagination, helpers |
| Server Setup | [SERVER.md](SERVER.md) | App initialization, routes, WebSocket, PWA, assets |
| Best Practices | [PATTERNS.md](PATTERNS.md) | Testing, validation, security, state management patterns |

## Core Philosophy

1. **Server-Centric Rendering** - All HTML generated server-side as strings
2. **String-Based Components** - Components are TypeScript functions returning HTML strings
3. **Action-Based Interactivity** - User interactions trigger server handlers returning HTML
4. **WebSocket-Enhanced** - Real-time updates via `/__ws` endpoint
5. **Type-Safe** - Full TypeScript support with proper type definitions

## Key Types

```typescript
type Callable = (ctx: Context) => string  // All handlers return HTML
type Attr = {
    ID?: string;
    Class?: string;
    Value?: string;
    OnClick?: string;
    OnSubmit?: string;
    // ... other HTML attributes
}
```

## Common Imports

```typescript
import ui from "./ui";
import { MakeApp, Context, Callable } from "./ui.server";
import { createCollate, TQuery, BOOL, SELECT } from "./ui.data";
```

## Development Commands

```bash
npm run dev           # Run examples (Node.js)
npm run dev:bun       # Run examples (Bun)
npm run check         # Type-check without emitting JS
npm test              # Run Playwright tests
```

## Runtime Support

- **Node.js 18+** - Uses built-in `http` module
- **Bun 1.0+** - Uses native `serve()` API for better performance

Both runtimes support WebSocket connections, session management, and form submissions.
