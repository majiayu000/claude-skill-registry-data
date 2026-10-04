---
name: justfile
description: This skill should be used every time you work on justfile projects or just command changes in this repository.
compatibility: opencode
---

# Justfile Structure

## Architecture Overview

Use a modular justfile architecture with separate recipe files organized by category in a `justfiles/` directory.

## Directory Structure

1. **`justfiles/` directory at project root** - All recipe files live here
2. **Category subdirectories** - Group by purpose: `development/`, `building/`, `verification/`, `testing/`, `utilities/`
3. **One command per file** - Each recipe gets its own `.just` file (e.g., `justfiles/development/web.just`)
4. **Main `justfile` at root** - Imports all recipe files, contains help command

## Main Justfile Structure

5. **Default command shows help** - Not `--list`, a themed help menu
6. **Imports organized by category** with section comment headers

```justfile
# Default: Show help menu
default:
    @just help

# ============================================================================
# Help Command
# ============================================================================

help:
    @echo ""
    @echo "\033[1;36m========== Project Commands ==========\033[0m"
    # ... help content ...

# ============================================================================
# Development Commands
# ============================================================================
import 'justfiles/development/web.just'
import 'justfiles/development/desktop.just'

# ============================================================================
# Building Commands
# ============================================================================
import 'justfiles/building/build-server.just'
```

## Example Directory Structure

```
project/
├── justfile                           # Main justfile with imports
└── justfiles/
    ├── development/
    │   ├── web.just
    │   ├── desktop.just
    │   └── dev.just
    ├── building/
    │   ├── build-server.just
    │   ├── build-desktop.just
    │   └── build-web.just
    ├── verification/
    │   ├── check-server.just
    │   ├── check-desktop.just
    │   └── check-web.just
    ├── testing/
    │   ├── test.just
    │   ├── test-unit.just
    │   ├── test-integration.just
    │   ├── test-e2e.just
    │   └── test-all.just
    └── utilities/
        ├── clean.just
        └── install-tools.just
```

## Benefits

- **Discoverability** - Easy to find and edit specific commands
- **Organization** - Logical grouping by purpose
- **Consistency** - Uniform patterns across all commands
- **Maintainability** - Add new commands by creating new files
- **Team-friendly** - Clear structure for collaboration
# Justfile Naming Conventions

## Command Naming

1. **Commands use kebab-case** - `build-server`, `test-e2e`, `install-tools`
2. **File name matches command name** - `build-server` command lives in `build-server.just`

## Parameter Naming

3. **Parameters use SCREAMING_CASE** - `PARAM`, `OPTIONAL`, `TARGET`

## Variadic Parameters and Quoting

4. **Variadic parameters (`*ARGS`) don't preserve quotes** - When using `*ARGS` to accept multiple words, the quotes from the shell are stripped
5. **Wrap variadic parameters in quotes** - Use `"{{ARGS}}"` to pass multi-word arguments correctly to subcommands

```justfile
# BAD: Quotes are not preserved, "foo bar" becomes two arguments
search *QUERY:
    my-tool {{QUERY}}
# `just search foo bar` runs: my-tool foo bar (2 args)

# GOOD: Wrap in quotes to preserve as single argument
search *QUERY:
    my-tool "{{QUERY}}"
# `just search foo bar` runs: my-tool "foo bar" (1 arg)
```

## Examples

```justfile
# Command: build-server
# File: justfiles/building/build-server.just
build-server TARGET="release":
    cargo build --release --bin {{TARGET}}

# Command: test-e2e
# File: justfiles/testing/test-e2e.just
test-e2e HEADLESS="true":
    playwright test --headed={{HEADLESS}}

# Command: search (with variadic parameter)
# File: justfiles/utilities/search.just
search *QUERY:
    cargo run --bin search -- "{{QUERY}}"
```
# Justfile Help Command Design

## Help Command Design

1. **Help command uses themed sections** with emojis and colors
2. **Default command shows help** - Users see help when running `just` with no arguments

## Color Codes

- `\033[1;36m` - Cyan for section headers/boxes
- `\033[0;33m` - Yellow for command names
- `\033[0;32m` - Green for descriptions
- `\033[1;35m` - Magenta for category labels
- `\033[0m` - Reset to default

## Section Emojis

- Most Common Commands
- Building
- Verification
- Testing
- Utilities
- Installation

## Help Format Template

```justfile
help:
    @echo ""
    @echo "\033[1;36m======================================\033[0m"
    @echo "\033[1;36m       Project Commands               \033[0m"
    @echo "\033[1;36m======================================\033[0m"
    @echo ""
    @echo "\033[1;35m  Most Common Commands:\033[0m"
    @echo "  just \033[0;33mweb\033[0m                     \033[0;32mStart web dev server\033[0m"
    @echo "  just \033[0;33mdesktop\033[0m                 \033[0;32mStart desktop app\033[0m"
    @echo "  just \033[0;33mtest\033[0m                    \033[0;32mRun all tests\033[0m"
    @echo ""
    @echo "\033[1;35m  Building:\033[0m"
    @echo "  just \033[0;33mbuild-server\033[0m            \033[0;32mBuild production server\033[0m"
    @echo ""
```
# Justfile Templates

## Recipe File Template

1. **Every recipe file has header comments** - Brief description, Usage, Example

```justfile
# Brief description of what this command does
# Usage: just command-name <required> [optional]
# Example: just command-name example-value

command-name PARAM OPTIONAL="default":
    command {{PARAM}} {{OPTIONAL}}
```

## Bash Script Template

2. **Use proper shebangs** - `#!/usr/bin/env bash`
3. **Enable strict mode** - `set -euo pipefail`

```justfile
# Description
# Usage: just command-name <param>

command-name PARAM:
    #!/usr/bin/env bash
    set -euo pipefail

    # Script content here
    echo "Processing {{PARAM}}"
```

## Command Patterns

4. **User-friendly messages** - Use emojis for feedback
5. **Calling other recipes** - Use `@just command-name`

```justfile
# Good: User feedback with emojis
build-server:
    @echo "Building server..."
    cargo build --release
    @echo "Build complete!"

# Good: Calling other recipes
test-all:
    @just test
    @just test-e2e
```
# Justfile Command Categories

## Standard Categories

### Development (hot-reload servers)
- `web` - Web dev server
- `desktop` - Desktop app
- `dev` - Both via mprocs

### Building (release builds)
- `build-server` - Production server
- `build-desktop` - Desktop bundle
- `build-web` - WASM bundle

### Verification (compile checks)
- `check-server` - Server compilation
- `check-desktop` - Desktop compilation
- `check-web` - WASM compilation

### Testing
- `test` - All Rust tests
- `test-unit` - Unit tests only
- `test-integration` - Integration tests
- `test-e2e` - E2E tests (headless)
- `test-e2e-ui` - E2E tests (interactive)
- `test-all` - All tests combined

### Utilities
- `clean` - Clean build artifacts
- `install-tools` - Install dev tools

## Category Guidelines

Place commands in the appropriate category based on their primary purpose:
- Hot-reload development → `development/`
- Release/production builds → `building/`
- Compilation checks (no artifacts) → `verification/`
- Any kind of testing → `testing/`
- Project maintenance → `utilities/`
