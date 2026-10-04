---
name: stack-go
description: Go backend conventions, patterns, and test infrastructure. Use when working with Go files, go.mod projects, Go modules, Go CLI, go build, go test, BubbleTea TUI apps, Lip Gloss styling, Charm libraries, goroutines, channels, interfaces, or Go dependency management.
user-invocable: false
---

## Documentation Lookup

**CRITICAL**: Never read Go module cache source files to learn library APIs. This includes:
- `$GOMODCACHE/...` paths
- `/tmp/*/gomodcache/...` paths
- Any path containing `@v` version suffixes (e.g., `pkg@v1.2.3/`)
- `vendor/` directories

Instead, use the client's available documentation lookup, preferring official package
documentation. Use Context7 when that integration is configured. This produces
focused API information without polluting context with raw dependency source.

## Sandbox Environment

When the active sandbox does not permit writes to the default Go caches, set writable
cache paths on every Go shell call because environment assignments may not persist:

```bash
GOPATH=$TMPDIR/gopath GOCACHE=$TMPDIR/gocache GOMODCACHE=$TMPDIR/gomodcache go <command>
```

Apply this prefix only when the environment requires it, including `go build`,
`go test`, `go mod tidy`, and `go get`.

## Integration Tests

Go tests use table-driven patterns with subtests:

```go
func TestMyFunction(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
        wantErr  bool
    }{
        {name: "valid input", input: "hello", expected: "HELLO"},
        {name: "empty input", input: "", expected: ""},
        {name: "error case", input: "bad", wantErr: true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := MyFunction(tt.input)
            if tt.wantErr {
                if err == nil {
                    t.Fatal("expected error, got nil")
                }
                return
            }
            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            if got != tt.expected {
                t.Errorf("got %q, want %q", got, tt.expected)
            }
        })
    }
}
```

## Build & Test Commands

```bash
GOPATH=$TMPDIR/gopath GOCACHE=$TMPDIR/gocache GOMODCACHE=$TMPDIR/gomodcache go build ./...
GOPATH=$TMPDIR/gopath GOCACHE=$TMPDIR/gocache GOMODCACHE=$TMPDIR/gomodcache go test ./...
```

## BubbleTea Rules

When working with BubbleTea (`github.com/charmbracelet/bubbletea`) TUI apps:

- **Never discard `tea.Cmd`**: Every `Update` method returns `(tea.Model, tea.Cmd)`. Always propagate the `tea.Cmd` — dropping it silently breaks async operations (timers, I/O, sub-commands).
- **Use `lipgloss.Width()` for string width**: Never use `len()` for display width calculations — it counts bytes, not visual columns. Use `lipgloss.Width()` which handles ANSI escape codes and wide characters.
- **Async test commands**: When testing `tea.Cmd` functions that run goroutines, use a timeout pattern:
  ```go
  cmd := model.Init() // or from Update
  done := make(chan tea.Msg, 1)
  go func() { done <- cmd() }()
  select {
  case msg := <-done:
      // assert on msg
  case <-time.After(2 * time.Second):
      t.Fatal("command timed out")
  }
  ```
- **Model updates are pure**: `Update` should return a new model, not mutate in place. If the model is a pointer receiver, be explicit about what changes.

## Security
- Use parameterized queries with `database/sql` placeholder syntax (`$1`, `?`) — never string concatenation for SQL
- Use `html/template` (not `text/template`) for HTML output — it auto-escapes
- Validate and sanitize all user input at handler boundaries

Read the project's applicable agent guidance (`AGENTS.md` for Codex, `CLAUDE.md` for
Claude Code) and relevant `docs/<topic>.md` files for project-specific Go conventions
when they exist.
