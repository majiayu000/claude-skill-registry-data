---
name: go-cli
description: "Golang CLI application development. Covers command structure (Cobra), configuration layering (Viper), exit codes, and I/O patterns."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:00:00 GMT
---

## Core Stack

- **[Cobra](https://github.com/spf13/cobra)**: Command and subcommand structure.
- **[Viper](https://github.com/spf13/viper)**: Configuration management (flags, env vars, config files).
- **[pflag](https://github.com/spf13/pflag)**: POSIX-compliant flags (integrated with Cobra).

## Project Structure

```
myapp/
├── cmd/
│   └── myapp/
│       ├── main.go      # Entry point
│       ├── root.go      # Root command
│       └── serve.go     # Subcommand
```

## Best Practices

1. **Silence Usage on Error** — Set `SilenceUsage: true` in your root command to avoid printing help text on every runtime error.
2. **Bind Flags to Viper** — Ensure flags can be overridden by environment variables or config files.
3. **Stderr for Logs, Stdout for Data** — Diagnostic info should never go to stdout, as it breaks unix pipes.
4. **Graceful Shutdown** — Use `signal.NotifyContext` to handle SIGINT/SIGTERM.
5. **Unix Exit Codes** — Return `0` for success, `1` for general failure, `2` for usage errors.
6. **Machine-Readable Output** — Provide an `--output` flag (json, table, plain) for automation.
7. **Embed Version Info** — Use `ldflags` to inject version and git commit hash at build time.

## Code Snippets

### Root Command Setup
```go
var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My awesome CLI",
    SilenceUsage:  true,
    SilenceErrors: true,
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        return initializeConfig(cmd)
    },
}
```

### Binding Flags to Viper
```go
func init() {
    rootCmd.PersistentFlags().String("config", "", "config file")
    viper.BindPFlag("config", rootCmd.PersistentFlags().Lookup("config"))
}
```

### Argument Validation
```go
var cmd = &cobra.Command{
    Use:   "greet [name]",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Printf("Hello %s\n", args[0])
    },
}
```

## Anti-patterns

- ❌ **Calling `os.Exit()` inside commands** — Prevents cleanup and tests from running. Return an error from `RunE` instead.
- ❌ **Hardcoded config paths** — Allow users to specify a config file via flag or env var.
- ❌ **Logging to Stdout** — Corrupts the data stream when users pipe your program to another.
- ❌ **Missing help descriptions** — Makes the CLI hard to discover for new users.
- ❌ **Ignoring signals** — Hard-stopping services can leave data in an inconsistent state.
