---
name: go-spf13-cobra
description: "Advanced CLI development with spf13/cobra. Covers command trees, argument validation, hooks, and shell completion."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:20:00 GMT
---

## Core Concepts

Cobra is built on a structure of **Commands**, **Args**, and **Flags**.

- **Commands**: The actions (e.g., `git clone`, `docker run`).
- **Args**: Positional arguments passed to the command.
- **Flags**: Modifiers for the command (e.g., `--verbose`, `-p 8080`).

## Best Practices

1. **Use `RunE` over `Run`** — `RunE` allows returning an error, which Cobra can then format and display.
2. **Standardize Error Handling** — Set `SilenceUsage: true` in your root command to avoid printing the help block on every logic error.
3. **Use Built-in Arg Validators** — Instead of manual length checks, use `cobra.ExactArgs(1)`, `cobra.MinimumNArgs(1)`, etc.
4. **Persistent Flags** — Use `PersistentFlags()` for flags that should apply to a command and all its subcommands (e.g., `--config` or `--verbose`).
5. **Output via `OutOrStdout()`** — Never use `os.Stdout` directly. Using `cmd.OutOrStdout()` makes your CLI testable by allowing you to redirect output.

## Command Hooks Lifecycle

Cobra commands follow this execution order:
1. `PersistentPreRunE` (Inherited from parents)
2. `PreRunE`
3. `RunE`
4. `PostRunE`
5. `PersistentPostRunE` (Inherited from parents)

**Note**: A child's `PersistentPreRunE` *overwrites* the parent's. If you need both, the child must explicitly call the parent's hook.

## Code Example: Root Command

```go
var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My awesome CLI application",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        // Initialize config or auth here
        return nil
    },
    RunE: func(cmd *cobra.Command, args []string) error {
        return cmd.Help()
    },
    SilenceUsage: true,
}
```

## Argument Validation

```go
var subCmd = &cobra.Command{
    Use:   "greet [name]",
    Short: "Greets a person",
    Args:  cobra.ExactArgs(1), // Built-in validator
    RunE: func(cmd *cobra.Command, args []string) error {
        fmt.Fprintf(cmd.OutOrStdout(), "Hello, %s!\n", args[0])
        return nil
    },
}
```

## Testing Cobra Commands

```go
func TestCommand(t *testing.T) {
    buf := new(bytes.Buffer)
    cmd := NewRootCommand()
    cmd.SetOut(buf)
    cmd.SetArgs([]string{"greet", "World"})
    
    err := cmd.Execute()
    assert.NoError(t, err)
    assert.Contains(t, buf.String(), "Hello, World!")
}
```

## Anti-patterns

- ❌ **`os.Exit()` inside commands** — Prevents cleanup and tests. Return an error from `RunE` instead.
- ❌ **Global state in commands** — Makes concurrent tests impossible. Initialize the command tree per test.
- ❌ **Hardcoded `os.Stdout`** — Breaks testability. Use `cmd.OutOrStdout()`.
- ❌ **Ignoring `PersistentPreRunE` inheritance** — Child commands accidentally skipping parent initialization logic.
- ❌ **No argument validation** — Letting the app panic or fail with "index out of range" instead of a clear usage error.
