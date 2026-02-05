---
name: go-installer-dev
description: Go development guide for the dotfiles-installer project. Use when writing Go code, adding features, fixing bugs, creating tests, working with package managers (brew, apt, dnf), implementing interfaces, using the commander/logger/filesystem utilities, handling privilege escalation, or understanding the codebase architecture. Covers coding patterns, testing conventions, interface design, error handling, and project structure.
---

# Go Installer Development

Development guide for the dotfiles-installer Go codebase.

## Project Structure

```
installer/
├── main.go                    # Entry point (version injection)
├── cmd/                       # CLI commands (Cobra)
│   ├── root.go               # Root command, global setup
│   ├── install.go            # Main installation workflow
│   ├── checkCompatibility.go # Compatibility check command
│   └── version.go            # Version display
├── lib/                       # Core business logic
│   ├── compatibility/        # OS/distro detection
│   ├── pkgmanager/          # Package manager interface
│   ├── brew/                # Homebrew implementation
│   ├── apt/                 # APT implementation
│   ├── dnf/                 # DNF implementation
│   ├── gpg/                 # GPG key management
│   ├── shell/               # Shell installation
│   ├── dotfilesmanager/     # Chezmoi integration
│   └── packageresolver/     # Package name resolution
├── utils/                     # Shared utilities
│   ├── logger/              # Logging with progress display
│   ├── osmanager/           # OS operations interface
│   ├── privilege/           # Sudo/doas escalation
│   ├── commander.go         # Command execution
│   ├── filesystem.go        # File operations
│   └── httpclient/          # HTTP client interface
├── cli/                       # Interactive UI components
├── internal/config/           # Embedded YAML configs
├── Taskfile.yml              # Task runner commands
└── .goreleaser.yaml          # Release configuration
```

## Key Interfaces

### Commander (utils/commander.go)

Execute system commands with functional options:

```go
result, err := commander.RunCommand(ctx, "brew", []string{"install", pkg},
    WithCaptureOutput(),
    WithEnv(env),
    WithTimeout(5 * time.Minute),
)
```

Available options: `WithEnv()`, `WithDir()`, `WithInput()`, `WithCaptureOutput()`, `WithDiscardOutput()`, `WithInteractive()`, `WithTimeout()`, `WithStdout()`, `WithStderr()`

### Logger (utils/logger/)

Logging with progress tracking:

```go
logger.StartProgress("Installing packages")
logger.UpdateProgress("Installing git")
logger.FinishProgress()
// or
logger.FailProgress(err)
```

Methods: `Trace`, `Debug`, `Info`, `Success`, `Warning`, `Error`

### FileSystem (utils/filesystem.go)

File operations interface for testability:

```go
exists, err := fs.PathExists(path)
data, err := fs.ReadFile(path)
err = fs.WriteFile(path, data, 0644)
err = fs.CreateDirectory(path)
```

### OsManager (utils/osmanager/)

OS-level operations (user management, environment, program queries, permissions).

### Privilege Escalator (utils/privilege/)

Smart privilege escalation (prefers sudo, falls back to doas):

```go
escalatedCmd, escalatedArgs, err := escalator.EscalateCommand("apt-get", []string{"install", "git"})
isRoot := escalator.IsRunningAsRoot()
```

### Optional Types

Use `samber/mo` for safer nil handling:

```go
import "github.com/samber/mo"

type Config struct {
    Shell mo.Option[string]
}

if shell, ok := config.Shell.Get(); ok {
    // use shell
}
```

## Code Style & Testing

**For all coding conventions and patterns:** See [Code Style Reference][code-style]

**For all testing conventions:** See [Test Style Reference][test-style]

## Development Commands

| Command | Purpose |
|---------|---------|
| `task build` | Build binary via goreleaser |
| `task test` | Run tests with race detection |
| `task fmt` | Format code (gofumpt, goimports, golines) |
| `task lint` | Run golangci-lint and typos |
| `task check` | Run tests + lint |
| `task cov` | Generate coverage report |
| `task bench` | Run benchmarks |
| `task sloc` | Print lines of code stats |

## Adding Features

### New Package Manager

1. Create package in `lib/{managername}/`
2. Implement `PackageManager` interface (see lib/pkgmanager/pkgmanager.go)
3. Add installer interface if installation needed
4. Add unit and integration tests (see [Test Style Reference][test-style])
5. Update `internal/config/packagemap.yaml` for package name mappings

### New Utility Interface

1. Define interface in `utils/`
2. Create implementation with constructor (see [Code Style Reference][code-style])
3. Generate mock: run `mockery` in project root
4. Inject via constructors where needed

### New CLI Command

1. Create file in `cmd/`
2. Define `cobra.Command` with flags
3. Register in `root.go` init()
4. Implement run logic using injected dependencies

## Configuration Files

### compatibility.yaml (internal/config/)

Defines supported OS/distros, architectures, and prerequisites:

```yaml
supported_os:
  darwin:
    name: macOS
    distros:
      - name: macOS
        architectures: [amd64, arm64]
        prerequisites: [git, curl]
```

### packagemap.yaml (internal/config/)

Maps generic package codes to manager-specific names:

```yaml
packages:
  git:
    brew: git
    apt: git
    dnf: git
  neovim:
    brew: neovim
    apt: neovim
    dnf: neovim
```

## Reference Files

- [Code Style Reference][code-style] - All Go coding conventions, formatting rules, patterns
- [Test Style Reference][test-style] - All testing patterns, naming conventions, mock usage

[code-style]: references/code-style.md
[test-style]: references/test-style.md
