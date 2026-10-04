---
name: go-cli-structure
description: The shape of a Go CLI's command tree - main.go, the root command for each project type, Execute and the exit path, a command file, the Run body, Run against RunE, and subcommand packages. Use when scaffolding a Go CLI, writing or changing cmd/root.go, adding a command file or a subcommand package, wiring setupLogs and --debug, or deciding whether a command returns an error. Triggers on main.go, cmd/root.go, cobra.Command, rootCmd, Execute, AddCommand, cobra.OnInitialize, setupLogs, CompletionOptions, SetHelpCommand, SilenceErrors, SilenceUsage, Run, RunE, cmd/ packages, and AppVersion ldflags injection. Not for flag conventions, positional arguments, or a flag reading stdin.
user-invocable: false
---

# Go CLI Structure

**How a Cobra command tree is put together: the entry point, the root, the commands hanging off it, and where a command's work goes.**

CLI Only projects and Web Only projects use different roots, and a CLI + Web hybrid uses the CLI Only root plus a `serve` command.

| Aspect | CLI Only | Web Only |
|---|---|---|
| Imports | zerolog, utils, subcommand packages | zerolog, cobra, subcommand packages |
| Global flags | `--debug` | `--debug` |
| Logging setup | `setupLogs()` via `cobra.OnInitialize`, terminal check through `utils` | `setupLogs()` via `cobra.OnInitialize`, terminal check inline |
| Output | `utils.Print*` | zerolog only |

Both set `Use`, `Short`, `Version` from the `AppVersion` ldflag, and `CompletionOptions.HiddenDefaultCmd: true`.

## Entry Point

```go
package main

import "github.com/[GITHUB_USER]/REPO_NAME/cmd"

func main() {
    cmd.Execute()
}
```

`main.go` holds nothing else, so no logic ends up in the one function a test cannot call.

## Root Command, CLI Only

```go
package cmd

import (
    "io"
    "os"
    "time"

    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
    "github.com/spf13/cobra"
    "github.com/[GITHUB_USER]/REPO_NAME/utils"

    featureCmd "github.com/[GITHUB_USER]/REPO_NAME/cmd/feature-cmd"
)

var AppVersion = "dev-build" // set at build time via ldflags

var debugFlag bool

var rootCmd = &cobra.Command{
    Use:               "appname",
    Short:             "Brief description of the application",
    Version:           AppVersion,
    CompletionOptions: cobra.CompletionOptions{HiddenDefaultCmd: true},
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}

func setupLogs() {
    zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
    var out io.Writer = os.Stdout
    if utils.StdoutIsTerminal {
        out = zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.DateTime}
    }
    log.Logger = zerolog.New(out).With().Timestamp().Logger()
    zerolog.SetGlobalLevel(zerolog.InfoLevel)
    if debugFlag {
        zerolog.SetGlobalLevel(zerolog.DebugLevel)
        utils.GlobalDebugFlag = true
    }
}

func init() {
    rootCmd.SetHelpCommand(&cobra.Command{Hidden: true})

    rootCmd.PersistentFlags().BoolVar(&debugFlag, "debug", false, "Enable debug logging")

    cobra.OnInitialize(setupLogs)

    rootCmd.AddCommand(serveCmd)
    rootCmd.AddCommand(featureCmd.FeatureCmd)
}
```

`setupLogs` runs through `cobra.OnInitialize` rather than at package init, because the flag values it reads are not parsed until Cobra has matched the command.

`Execute` sets the exit code and prints nothing. Cobra has already written the error to stderr by the time it returns one (`cobra@v1.10.2 command.go:1159-1161`), so a wrapper that prints it again shows the user the same line twice.

The help and completion commands are hidden so `appname --help` lists only the commands the tool actually offers.

A root declaring `cobra.Group`s needs one line more. The hidden help command still counts toward `AllChildCommandsHaveGroup` (`cobra@v1.10.2 command.go:1376-1383`), and leaving it ungrouped renders an empty `Additional Commands:` header:

```go
rootCmd.AddGroup(&cobra.Group{ID: "main", Title: "Main Commands:"})
rootCmd.SetHelpCommandGroupID("main")
```

An ungrouped root needs nothing extra, since the usage template reaches that header only when `len .Groups` is non-zero.

## Root Command, Web Only

```go
package cmd

import (
    "io"
    "os"
    "time"

    "github.com/charmbracelet/x/term"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
    "github.com/spf13/cobra"
)

var AppVersion = "dev-build"

var debugFlag bool

var rootCmd = &cobra.Command{
    Use:               "appname",
    Short:             "Brief description of the application",
    Version:           AppVersion,
    CompletionOptions: cobra.CompletionOptions{HiddenDefaultCmd: true},
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}

func setupLogs() {
    zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
    var out io.Writer = os.Stdout
    if term.IsTerminal(os.Stdout.Fd()) {
        out = zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.DateTime}
    }
    log.Logger = zerolog.New(out).With().Timestamp().Logger()
    zerolog.SetGlobalLevel(zerolog.InfoLevel)
    if debugFlag {
        zerolog.SetGlobalLevel(zerolog.DebugLevel)
    }
}

func init() {
    rootCmd.SetHelpCommand(&cobra.Command{Hidden: true})
    rootCmd.PersistentFlags().BoolVar(&debugFlag, "debug", false, "Enable debug logging")
    cobra.OnInitialize(setupLogs)
    rootCmd.AddCommand(serveCmd)
}
```

Same logger and same `--debug` as CLI Only, without the `utils` import. What a server has no use for is the printers, since nobody is watching a container's stdout for a styled checkmark.

## Simple Command

A command without subcommands is defined directly in `cmd/`, with its own flag struct and `init()`. Grouping flags in a struct per command keeps two commands from colliding over a variable named `output` in the shared `cmd` package.

```go
// cmd/serve.go
package cmd

import (
    "fmt"

    "github.com/spf13/cobra"
    "github.com/[GITHUB_USER]/REPO_NAME/internal/server"
    u "github.com/[GITHUB_USER]/REPO_NAME/utils"
)

var serveFlags struct {
    port int
    host string
}

var serveCmd = &cobra.Command{
    Use:   "serve",
    Short: "Start the web server",
    Run: func(cmd *cobra.Command, args []string) {
        srv := server.New(serveFlags.host, serveFlags.port)
        if err := srv.Setup(); err != nil {
            u.PrintFatal("Failed to set up server", err)
        }
        u.PrintInfo(fmt.Sprintf("Starting server on %s:%d", serveFlags.host, serveFlags.port))
        if err := srv.Run(); err != nil {
            u.PrintFatal("Server error", err)
        }
    },
}

func init() {
    serveCmd.Flags().IntVarP(&serveFlags.port, "port", "p", 8080, "Port to listen on")
    serveCmd.Flags().StringVarP(&serveFlags.host, "host", "H", "0.0.0.0", "Host to bind to")
}
```

The same command in a Web Only project swaps `u.PrintFatal(msg, err)` for `log.Fatal().Err(err).Msg(msg)` and `u.PrintInfo` for `log.Info()`, and drops the `utils` import.

## Run Function Shape

A `Run` body validates flags, builds a config struct, calls into `internal/`, and reports the result. Keeping the work in `internal/` leaves the command as the only layer that knows about flags and terminals, which is what lets the logic be tested without one.

```go
Run: func(cmd *cobra.Command, args []string) {
    if flags.required == "" {
        u.PrintFatal("--required flag is required", nil)
    }

    cfg := internal.Config{Field1: flags.field1, Field2: flags.field2}

    result, err := internal.DoThing(cfg)
    if err != nil {
        u.PrintFatal("Failed to do thing", err)
    }

    u.PrintSuccess("Thing completed")
    u.PrintGeneric(result)
}
```

`Run` with `u.PrintFatal` is the default. `RunE` is for a command holding something a deferred function has to release, such as a lock file, a temporary directory, or a half-written output file, since `PrintFatal` calls `os.Exit(1)` and skips defers.

Everywhere else `RunE` costs two things. `PrintFatal(msg, err)` carries a human label and the wrapped error separately, which is what lets the normal tier show the label alone while `--debug` shows the chain, and a returned `error` collapses both into one string. Cobra then prints `Error: <err>` followed by the entire usage block (`cobra@v1.10.2 command.go:1159-1167`), burying the message under a wall of flags.

A tree that uses `RunE` anywhere sets both silences on the root and reports the error itself, which arrives back at `PrintFatal`:

```go
func init() {
    rootCmd.SilenceErrors = true
    rootCmd.SilenceUsage = true
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        u.PrintFatal("Command failed", err)
    }
}
```

## Subcommand Package

A group of related subcommands gets a package under `cmd/`. The parent command is exported and has no `Run`, so invoking it bare prints help instead of doing something arbitrary; the children are unexported and each carry a `Run`.

```go
// cmd/feature-cmd/feature.go
package featureCmd

import (
    "fmt"

    "github.com/spf13/cobra"
    "github.com/[GITHUB_USER]/REPO_NAME/internal/feature"
    u "github.com/[GITHUB_USER]/REPO_NAME/utils"
)

var createFlags struct {
    name   string
    config string
}

var FeatureCmd = &cobra.Command{
    Use:   "feature",
    Short: "Feature management commands",
}

var createCmd = &cobra.Command{
    Use:   "create",
    Short: "Create a new feature",
    Run: func(cmd *cobra.Command, args []string) {
        cfg := feature.CreateConfig{Name: createFlags.name, Config: createFlags.config}
        if err := feature.Create(cfg); err != nil {
            u.PrintFatal("Failed to create feature", err)
        }
        u.PrintSuccess(fmt.Sprintf("Created feature: %s", createFlags.name))
    },
}

func init() {
    FeatureCmd.AddCommand(createCmd)

    createCmd.Flags().StringVarP(&createFlags.name, "name", "n", "", "Feature name (required)")
    createCmd.MarkFlagRequired("name")
    createCmd.Flags().StringVarP(&createFlags.config, "config", "c", "", "Config file path")
}
```
