---
name: cli-patterns
description: Lightweight Go CLI patterns using urfave/cli. Use when building CLI tools, creating commands with flags, implementing subcommands, adding before/after hooks, organizing command categories, or when user mentions Go CLI, urfave/cli, cobra alternatives, CLI flags, CLI categories.
allowed-tools: Bash, Read, Write, Edit
---

# CLI Patterns Skill

Lightweight Go CLI patterns using urfave/cli for fast, simple command-line applications.

## Overview

Provides battle-tested patterns for building production-ready CLI tools in Go using urfave/cli v2. Focus on simplicity, speed, and maintainability over complex frameworks like Cobra.

## Why urfave/cli?

- **Lightweight**: Minimal dependencies, small binary size
- **Fast**: Quick compilation, fast execution
- **Simple API**: Easy to learn, less boilerplate than Cobra
- **Production-ready**: Used by Docker, Nomad, and many other tools
- **Native Go**: Feels like standard library code

## Core Patterns

### 1. Basic CLI Structure

Use `templates/basic-cli.go` for simple single-command CLIs:
- Main command with flags
- Help text generation
- Error handling
- Exit codes

### 2. Subcommands

Use `templates/subcommands-cli.go` for multi-command CLIs:
- Command hierarchy (app → command → subcommand)
- Shared flags across commands
- Command aliases
- Command categories

### 3. Flags and Options

Use `templates/flags-demo.go` for comprehensive flag examples:
- String, int, bool, duration flags
- Required vs optional flags
- Default values
- Environment variable fallbacks
- Flag aliases (short and long forms)
- Custom flag types

### 4. Command Categories

Use `templates/categories-cli.go` for organized command groups:
- Group related commands
- Better help text organization
- Professional CLI UX
- Examples: database commands, deploy commands, etc.

### 5. Before/After Hooks

Use `templates/hooks-cli.go` for lifecycle management:
- Global setup (before all commands)
- Global cleanup (after all commands)
- Per-command setup/teardown
- Initialization and validation
- Resource management

### 6. Context and State

Use `templates/context-cli.go` for shared state:
- Pass configuration between commands
- Share database connections
- Manage API clients
- Context values

## Scripts

### Generation Scripts

**`scripts/generate-basic.sh <app-name>`**
- Generates basic CLI structure
- Creates main.go with single command
- Adds common flags (verbose, config)
- Includes help text template

**`scripts/generate-subcommands.sh <app-name>`**
- Generates multi-command CLI
- Creates command structure
- Adds subcommand examples
- Includes command categories

**`scripts/generate-full.sh <app-name>`**
- Generates complete CLI with all patterns
- Includes before/after hooks
- Adds comprehensive flag examples
- Sets up command categories
- Includes context management

### Utility Scripts

**`scripts/add-command.sh <app-name> <command-name>`**
- Adds new command to existing CLI
- Updates command registration
- Creates command file
- Adds to appropriate category

**`scripts/add-flag.sh <file> <flag-name> <flag-type>`**
- Adds flag to command
- Supports all flag types
- Includes environment variable fallback
- Adds help text

**`scripts/validate-cli.sh <project-path>`**
- Validates CLI structure
- Checks for common mistakes
- Verifies flag definitions
- Ensures help text exists

## Templates

### Core Templates

**`templates/basic-cli.go`**
- Single-command CLI
- Standard flags (verbose, version)
- Error handling patterns
- Exit code management

**`templates/subcommands-cli.go`**
- Multi-command structure
- Command registration
- Shared flags
- Help text organization

**`templates/flags-demo.go`**
- All flag types demonstrated
- Environment variable fallbacks
- Required flag validation
- Custom flag types

**`templates/categories-cli.go`**
- Command categorization
- Professional help output
- Grouped commands
- Category-based organization

**`templates/hooks-cli.go`**
- Before/After hooks
- Global setup/teardown
- Per-command hooks
- Resource initialization

**`templates/context-cli.go`**
- Context management
- Shared state
- Configuration passing
- API client sharing

### TypeScript Equivalent (Node.js)

**`templates/commander-basic.ts`**
- commander.js equivalent patterns
- TypeScript type safety
- Similar API to urfave/cli

**`templates/oclif-basic.ts`**
- oclif framework patterns (Heroku/Salesforce style)
- Class-based commands
- Plugin system

### Python Equivalent

**`templates/click-basic.py`**
- click framework patterns
- Decorator-based commands
- Python CLI best practices

**`templates/typer-basic.py`**
- typer framework (FastAPI CLI)
- Type hints for validation
- Modern Python patterns

## Examples

### Example 1: Database CLI Tool

**`examples/db-cli/`**
- Complete database management CLI
- Commands: connect, migrate, seed, backup
- Categories: schema, data, admin
- Before hook: validate connection
- After hook: close connections

### Example 2: Deployment Tool

**`examples/deploy-cli/`**
- Deployment automation CLI
- Commands: build, test, deploy, rollback
- Categories: build, deploy, monitor
- Context: share deployment config
- Hooks: setup AWS credentials

### Example 3: API Client

**`examples/api-cli/`**
- REST API client CLI
- Commands: get, post, put, delete
- Global flags: auth token, base URL
- Before hook: authenticate
- Context: share HTTP client

### Example 4: File Processor

**`examples/file-cli/`**
- File processing tool
- Commands: convert, validate, optimize
- Categories: input, output, processing
- Flags: input format, output format
- Progress indicators

## Best Practices

### CLI Design

1. **Keep it simple**: Start with basic structure, add complexity as needed
2. **Consistent naming**: Use kebab-case for commands (deploy-app, not deployApp)
3. **Clear help text**: Every command and flag needs description
4. **Exit codes**: Use standard codes (0=success, 1=error, 2=usage error)

### Flag Patterns

1. **Environment variables**: Always provide env var fallback for important flags
2. **Sensible defaults**: Required flags should be rare
3. **Short and long forms**: -v/--verbose, -c/--config
4. **Validation**: Validate flags in Before hook, not in action

### Command Organization

1. **Categories**: Group related commands (>5 commands = use categories)
2. **Aliases**: Provide shortcuts for common commands
3. **Subcommands**: Use for hierarchical operations (db migrate up/down)
4. **Help text**: Keep concise, provide examples

### Performance

1. **Fast compilation**: urfave/cli compiles faster than Cobra
2. **Small binaries**: Minimal dependencies = smaller output
3. **Startup time**: Use Before hooks for expensive initialization
4. **Lazy loading**: Don't initialize resources unless command needs them

## Common Patterns

### Configuration File Loading

```go
app.Before = func(c *cli.Context) error {
    configPath := c.String("config")
    if configPath != "" {
        return loadConfig(configPath)
    }
    return nil
}
```

### Environment Variable Fallbacks

```go
&cli.StringFlag{
    Name:    "token",
    Aliases: []string{"t"},
    Usage:   "API token",
    EnvVars: []string{"API_TOKEN"},
}
```

### Required Flags

```go
&cli.StringFlag{
    Name:     "host",
    Required: true,
    Usage:    "Database host",
}
```

### Global State Management

```go
type AppContext struct {
    Config *Config
    DB     *sql.DB
}

app.Before = func(c *cli.Context) error {
    ctx := &AppContext{
        Config: loadConfig(),
    }
    c.App.Metadata["ctx"] = ctx
    return nil
}
```

## Validation

Run `scripts/validate-cli.sh` to check:
- All commands have descriptions
- All flags have usage text
- Before/After hooks are properly defined
- Help text is clear and concise
- No unused imports
- Proper error handling

## Migration Guides

### From Cobra to urfave/cli

See `examples/cobra-migration/` for:
- Command mapping (cobra.Command → cli.Command)
- Flag conversion (cobra flags → cli flags)
- Hook equivalents (PreRun → Before)
- Context differences

### From Click (Python) to urfave/cli

See `examples/click-migration/` for:
- Decorator to struct conversion
- Option to flag mapping
- Context passing patterns

## References

- [urfave/cli v2 Documentation](https://cli.urfave.org/v2/)
- [Docker CLI Source](https://github.com/docker/cli) - Real-world example
- [Go CLI Best Practices](https://github.com/cli-dev/guide)
