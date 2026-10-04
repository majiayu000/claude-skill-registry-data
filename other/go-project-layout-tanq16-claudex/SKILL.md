---
name: go-project-layout
description: The canonical Go project taxonomy, directory layout, logging discipline, the config directory, and config loading. Use when starting a Go project, adding a package or directory, deciding where a file belongs, wiring zerolog, or deciding where a tool keeps its config and credentials. Triggers on go.mod, main.go, cmd/, internal/, pkg/, utils/, internal/server/static/, setupLogs, ConsoleWriter, ~/.config, and on any question of whether a project is CLI Only, Web Only, CLI + Web, a Headless API Service, or a Library.
user-invocable: false
---

# Go Project Layout

**Which of the five Go project types you are in, what its tree looks like, and how it logs and loads config.**

Every other Go convention keys off the project type, so settling the type is the first step of any Go task.

## Project Taxonomy

| Type | What it is | Defining markers |
|---|---|---|
| CLI Only | Terminal tool for users | `cobra`, `utils/`, zerolog, lipgloss/bubbletea/bubbles v2; multi-platform binaries; no Docker |
| Web Only | Web app served from a Go binary, with no real CLI beyond `serve` | `cobra` with a lone `serve` command, embedded frontend at `internal/server/static/`, Docker, no `utils/` |
| CLI + Web | A real CLI tool that also serves a web app from one `serve` subcommand | The full CLI Only stack for the command surface, plus `internal/server/static/` and a `serve` command; Docker |
| Headless API Service | REST or gRPC backend with no frontend | `internal/server` handlers with no `static/`, Docker, no `utils/`; `cobra` only when it needs more than `serve` |
| Library / Module | Importable package with no entry point | No `main.go`, no `cobra`, no `utils/`; exported packages at the module root or under `pkg/`; consumed via `go get` |

Read the type off the tree before writing anything, because the same file is correct in one type and a defect in another: a `utils/` package belongs in CLI Only and is a defect in Web Only.

## Layout

### CLI Only

```
project-root/
├── main.go                 # calls cmd.Execute() and nothing else
├── go.mod / go.sum
├── Makefile                # build targets, no docker targets
├── README.md
├── .github/
│   ├── assets/logo.png
│   └── workflows/release.yaml   # binaries only
├── cmd/
│   ├── root.go             # zerolog, --debug, utils
│   ├── command.go          # simple commands
│   └── feature-cmd/        # grouped subcommands get their own package
│       ├── parent.go
│       └── child.go
├── internal/               # private packages, where 90% of the logic lives
│   ├── feature1/
│   └── feature2/
├── utils/                  # top-level, not inside internal/
│   ├── globals.go
│   ├── printer.go
│   ├── input.go
│   ├── table.go
│   └── config.go
└── pkg/                    # rare, only for genuinely reusable packages
```

### Web Only

```
project-root/
├── main.go
├── go.mod / go.sum
├── Makefile                # build, assets, and docker targets
├── Dockerfile
├── README.md
├── .github/
│   ├── assets/logo.png
│   └── workflows/release.yaml   # docker and binaries
├── cmd/
│   ├── root.go             # zerolog, --debug, no utils
│   └── serve.go            # the one command
└── internal/
    ├── feature1/
    └── server/
        ├── server.go
        └── static/         # embedded frontend
            ├── css/ fonts/ js/
            └── index.html
```

### CLI + Web

Structurally a CLI Only project with a Web Only server grafted on: the full `utils/` package and the CLI Only `cmd/root.go`, plus an `internal/server/` holding the embedded `static/` frontend reached through a single `serve` command. It ships Docker and multi-platform binaries.

```
project-root/
├── main.go
├── Makefile                # CLI Only targets plus docker targets and assets
├── Dockerfile
├── cmd/
│   ├── root.go             # zerolog, --debug, utils
│   ├── serve.go            # the one web command
│   └── operation.go        # CLI subcommands, full utils/zerolog/TUI stack
├── internal/
│   ├── feature1/
│   └── server/
│       ├── server.go
│       └── static/
└── utils/                  # present, the CLI surface uses it
```

What divides on command boundaries is the `utils` printers, which the CLI commands use and `serve` does not. Logging does not divide: every command in the binary writes through the same logger in the same format.

### Headless API Service

A Web Only project minus the frontend: no `utils/`, Dockerfile and Docker in CI, and `cobra` only when the service needs subcommands beyond `serve`.

```
project-root/
├── main.go                 # cmd.Execute() or a direct serve()
├── go.mod / go.sum
├── Makefile                # build and docker targets, no frontend assets
├── Dockerfile
├── cmd/serve.go            # optional, only when more than serve exists
└── internal/
    ├── server/server.go    # handlers, no static/ subtree
    └── feature1/
```

Its HTTP server drops the `embed.FS`, `static/`, and `handleIndex` pieces, since there is no frontend to serve.

### Library / Module

```
module-root/
├── go.mod / go.sum
├── README.md               # usage and API docs, since consumers read this
├── <package>.go            # exported API at the module root, or
├── pkg/<package>/          # grouped exported packages
└── internal/               # private helpers outside the public API
```

A library configures no global logging and avoids `log.Fatal` and `os.Exit`, because those decisions belong to the program importing it rather than to the package.

## Layout Rules

`main.go` holds an import and a call to `cmd.Execute()`, so the entry point stays free of logic that tests cannot reach.

New packages go under `internal/` by default. `pkg/` is for packages you intend other repositories to import, and putting private code there commits you to an API you never meant to promise.

A group of related subcommands gets its own package under `cmd/` (`cmd/feature-cmd/`), which keeps the flag variables of one group from colliding with another's in the shared `cmd` package.

Frontend assets live at `internal/server/static/` so a single `//go:embed static` directive in the server package picks them all up.

## Logging

One library, zerolog, in every project type that has an entry point, and one format rule underneath it: a `ConsoleWriter` when stdout is a terminal, and zerolog's own JSON otherwise. The destination decides, so a person at a terminal reads the pretty form and a container log collector reads structured JSON, with neither being a mode anyone selects.

```go
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
```

A CLI Only project reads the terminal check through `utils.StdoutIsTerminal`, which it already has. A Web Only or Headless API Service project calls `term.IsTerminal` directly, having no `utils/` to hold it, and sets `utils.GlobalDebugFlag` in the debug branch only when the package exists.

`--debug` sits on the root command of every project type and moves the level from info to debug. Nothing else rides on it.

Levels come from the library rather than from the message, so a formatted prefix is never written into the text:

```go
log.Info().Str("addr", addr).Msg("starting")
log.Error().Err(err).Msg("failed to validate token")
log.Fatal().Err(err).Msg("failed to bind")
```

`log.Fatal()` exits after writing, which is the zerolog form of the exit a fatal message implies.

What a CLI adds on top is the `utils` printers, not a second logger. Those are what a user reads in normal use, and zerolog is what they see when they pass `--debug`, so the two never describe the same event twice.

In a CLI the log messages stay generic and carry no package-name field, because most of them originate in the shared `utils` package where the field would be the same value every time.

## Config

Cobra flags alone cover most projects. Reach for a config file only when a project genuinely needs one, because a hierarchy nobody populates is four lookups to answer one question.

### The config directory

A CLI tool that persists anything puts it at `~/.config/[APP_NAME]/`, hardcoded, with no `--config-dir` flag and no XDG lookup. One path means a user, a backup script, and a support answer all name the same place.

```go
func configDir() string {
    home, err := os.UserHomeDir()
    if err != nil {
        u.PrintFatal("cannot resolve home directory", err)
    }
    return filepath.Join(home, ".config", "[APP_NAME]")
}
```

The directory is created at `0700` and every file inside it at `0600`, because what lives there is credentials: OAuth tokens, session cookies, API keys, and the config file that may hold any of them. A subdirectory per concern keeps them separable, and nothing else in the user's home belongs to the tool.

### Precedence

Highest first: an explicit flag, then the environment, then the config file, then the built-in default. The flag wins because it is the most specific thing the caller said in this invocation, and an environment variable reaches the command as that flag's default value rather than as an override applied afterwards, which is what keeps `--help` honest about what will be used.

A variable the tool owns is namespaced with the tool's name, so `[APP_NAME]_TOKEN` rather than `TOKEN`. A variable belonging to another tool keeps that tool's name, since renaming `GITHUB_TOKEN` only means the user has to set it twice.

### Where the loading lives

| Project type | Where config loading lives |
|---|---|
| CLI Only, CLI + Web | `utils/config.go`, returning a struct passed into functions |
| Web Only, Headless API Service | Cobra flags and environment variables directly, or a config package under `internal/` |
| Library / Module | Nowhere. A library takes its configuration as function arguments |

The loader returns a struct rather than exposing a global, so a caller can construct one in a test without touching the environment.

```go
func LoadConfig(path string) (*Config, error) {
    cfg := &Config{Server: ServerConfig{Port: 8080, Host: "0.0.0.0"}}
    if path == "" {
        path = filepath.Join(configDir(), "config.yaml")
    }
    data, err := os.ReadFile(path)
    if errors.Is(err, os.ErrNotExist) {
        return cfg, nil
    }
    if err != nil {
        return nil, err
    }
    if err := yaml.Unmarshal(data, cfg); err != nil {
        return nil, err
    }
    return cfg, nil
}
```

A missing config file falls back to defaults instead of erroring, because a first run has not written one yet. A file that exists and does not parse is an error, since silently ignoring it hands the user defaults they did not ask for and no way to tell.
