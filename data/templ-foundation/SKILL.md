---
name: templ-foundation
description: Initialize Go templ project with CLI tools and basic structure. Use when starting new templ project, setting up Go HTML templating, mentions 'templ project', 'templ setup', or creating server-side rendered Go web application.
---

# Templ Foundation

## Overview

Sets up a Go project with [templ](https://templ.guide) - a type-safe HTML templating language that compiles to Go code.

**Key Benefits:**
- Type-safe templates with compile-time checks
- No runtime parsing overhead
- IDE autocompletion and refactoring
- Fast rendering (~2-3x faster than html/template)

## When to Use

1. Starting new templ project or Go web app with server-side rendering
2. User explicitly mentions templ, type-safe templates, or Go HTML
3. Building hypermedia-driven apps (HTMX, etc.)
4. Creating templ feature in Doodle project

## Quick Start (6 Steps)

### 1. Create Project Structure

```bash
mkdir project-name
cd project-name
mkdir -p components handlers static
```

### 2. Initialize Go Module

```bash
go mod init github.com/user/project-name
go get github.com/a-h/templ
```

### 3. Install Templ CLI

```bash
go install github.com/a-h/templ/cmd/templ@latest

# Verify
templ version
```

**Troubleshooting**: If `templ: command not found`, add to PATH:
```bash
export PATH=$PATH:$(go env GOPATH)/bin
```

### 4. Create First Component

Create `components/hello.templ`:

```templ
package components

templ Hello(name string) {
    <div>
        <h1>Hello, { name }!</h1>
    </div>
}
```

### 5. Generate Go Code

```bash
templ generate
```

This creates `components/hello_templ.go` with compiled Go code.

### 6. Use in Server

Create `main.go`:

```go
package main

import (
    "net/http"
    "project-name/components"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        components.Hello("World").Render(r.Context(), w)
    })

    http.ListenAndServe(":8080", nil)
}
```

Run:
```bash
go run .
```

Visit http://localhost:8080

## Core Workflow

### Development Cycle

1. Write `.templ` component
2. Run `templ generate` (or watch mode)
3. Import generated component in Go code
4. Call `.Render(ctx, writer)` method

### Development Modes

**Option A: Manual** (simple, no extra tools)
```bash
# Terminal 1
templ generate --watch

# Terminal 2
go run .
```

**Option B: Air** (auto-reload, recommended)
```bash
go install github.com/cosmtrek/air@latest
air
```

See [build-makefile.md](./references/build-makefile.md) for task automation and [build-air.md](./references/build-air.md) for live reload setup.

## Project Structure

Choose structure based on project size:

| Size | Components | Structure | When to Use | Guide |
|------|------------|-----------|-------------|-------|
| **Small** | < 10 | Flat | Personal projects, blogs, MVPs | [structure-small.md](./references/structure-small.md) |
| **Medium** | 10-50 | Type-based | SaaS, e-commerce, growing apps | [structure-medium.md](./references/structure-medium.md) |
| **Large** | 50+ | Domain-driven | Enterprise, multi-team, microservices | [structure-large.md](./references/structure-large.md) |

**Small** (< 10 components):
```
project/
├── main.go
├── components/      # All templates (flat)
├── handlers/
└── static/
```

**Medium** (10-50 components):
```
project/
├── cmd/server/
├── internal/
│   ├── components/
│   │   ├── layout/      # Page layouts
│   │   ├── pages/       # Full pages
│   │   └── shared/      # Reusable UI
│   └── handlers/
└── static/
```

**Large** (50+ components):
```
project/
├── cmd/server/
├── internal/
│   ├── app/             # Business logic
│   └── web/
│       ├── components/
│       │   ├── auth/    # By domain
│       │   ├── products/
│       │   └── shared/
│       └── handlers/
└── static/
```

**Migration path**: Small → Medium (add folders) → Large (add domains)

## Essential Files

### go.mod

```go
module github.com/user/project-name

go 1.21

require github.com/a-h/templ v0.2.543
```

### .gitignore

```gitignore
# Generated files (NEVER commit)
*_templ.go

# Build artifacts
tmp/
dist/
*.exe

# IDE
.vscode/
.idea/
.DS_Store
```

**Important**: `*_templ.go` files are build artifacts. Never commit them.

## IDE Setup

**VS Code** (recommended):
- Install extension: "templ" by a-h (ID: `a-h.templ`)
- Provides LSP, syntax highlighting, formatting

**Other editors**: GoLand, Neovim, Vim all support templ with plugins.

## Common Issues

### "templ: command not found"

Add `$GOPATH/bin` to PATH:
```bash
export PATH=$PATH:$(go env GOPATH)/bin
```

### Generated files not found

Run `templ generate` before `go run`:
```bash
templ generate && go run .
```

### Changes not reflecting

1. Check `templ generate` ran successfully
2. Verify `*_templ.go` file timestamp updated
3. Restart server (or use Air for auto-reload)

### Import errors

Ensure module path matches:
```go
// go.mod
module github.com/user/project

// Import as:
import "github.com/user/project/components"
```

## Doodle Integration

For features/ directory:

```bash
cd features/
mkdir templ-blog
cd templ-blog

# Standard setup
go mod init github.com/homveloper/doodle/features/templ-blog
go get github.com/a-h/templ
mkdir -p components handlers static

# Create README following Doodle conventions
# Add to features/ tests if applicable
```

## Best Practices

1. **Never commit generated files**: Add `*_templ.go` to `.gitignore`
2. **Use watch mode**: `templ generate --watch` in development
3. **Start simple**: Flat structure for small projects, grow as needed
4. **Generate before build**: CI/CD must run `templ generate`
5. **Leverage type safety**: Let compiler catch template errors

## Next Steps

After foundation setup:

1. **Learn syntax** → `templ-syntax` skill
2. **Build components** → `templ-components` skill
3. **HTTP integration** → `templ-http` skill
4. **Add interactivity** → `templ-htmx` skill

## References

Detailed guides (choose what you need):

- **Build Tools**:
  - **Makefile**: [build-makefile.md](./references/build-makefile.md) - Task automation
  - **Air**: [build-air.md](./references/build-air.md) - Live reload setup
- **Project Structure**:
  - **Small** (< 10 components): [structure-small.md](./references/structure-small.md)
  - **Medium** (10-50 components): [structure-medium.md](./references/structure-medium.md)
  - **Large** (50+ components): [structure-large.md](./references/structure-large.md)

## Assets

Template files for quick start:
- `go.mod.template`
- `main.go.template`
- `Makefile`
- `.gitignore`
- `.air.toml.template`

---

**Focus**: This skill covers project initialization only. For component writing, use `templ-components`. For server patterns, use `templ-http`.
