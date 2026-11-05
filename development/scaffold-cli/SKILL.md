---
name: scaffold-cli
description: Generate CLI command with argument parsing, handler, help text, and tests
type: scaffold
project_types: [cli]
trigger: "create command, add CLI command, create subcommand"
inputs:
  - name: name
    description: Command/subcommand name (e.g. init, deploy, migrate)
    required: true
  - name: description
    description: Short description of what the command does
    required: false
    default: ""
  - name: args
    description: Arguments and flags description (e.g. "--output -o string, --verbose bool")
    required: false
    default: ""
---

## Context

Project {{project_name}} is a CLI application using {{stack}}.
You will create a new command "{{input.name}}".

Read AGENTS.md for conventions. Read existing commands to understand patterns.

## Instructions

1. **Analyze existing command patterns**
   - Read existing command files
   - Identify: argument parsing library (cobra, clap, click, commander, argparse, etc.)
   - Identify: command registration pattern (subcommands, router, etc.)
   - Identify: output formatting (table, JSON, plain text, colored)
   - Note error handling patterns (exit codes, stderr vs stdout)

2. **Create command file**
   - Path: according to project convention
     - Go (cobra): `cmd/{{input.name}}.go` or `internal/cmd/{{input.name}}.go`
     - Rust (clap): `src/commands/{{input.name}}.rs`
     - Python (click): `src/commands/{{input.name}}.py`
     - Node (commander): `src/commands/{{input.name}}.ts`
   - Implement:
     - Command definition with name, description, aliases
     - Argument/flag parsing with validation
     - Help text with usage examples
     - Handler function with business logic

3. **Create argument/flag definitions**
   - Define all required and optional flags
   - Set proper types (string, bool, int, etc.)
   - Add short aliases where appropriate (-o for --output)
   - Set sensible defaults
   - Add validation for required args

4. **Register command**
   - Add to root command / command registry
   - Ensure it shows up in `--help` output
   - Set up proper parent-child relationship for subcommands

5. **Implement handler logic**
   - Separate business logic from CLI plumbing
   - Use project's existing service/logic layer
   - Handle errors gracefully with helpful messages
   - Respect --quiet/--verbose flags if they exist
   - Use proper exit codes (0 = success, 1 = error, 2 = usage error)

6. **Create tests**
   - Path: according to convention
   - Test cases:
     - Command executes successfully with valid args
     - Help text is correct
     - Required args validation works
     - Flag parsing works correctly
     - Error cases return proper exit codes
     - Output format is correct

## Script

```bash
#!/bin/bash
# Detect CLI framework
if [ -f "go.mod" ]; then
  if grep -q "cobra" go.mod 2>/dev/null; then
    echo "Framework: Cobra (Go)"
    echo "Command path: cmd/{{input.name}}.go"
  elif grep -q "urfave/cli" go.mod 2>/dev/null; then
    echo "Framework: urfave/cli (Go)"
  fi
elif [ -f "Cargo.toml" ]; then
  if grep -q "clap" Cargo.toml 2>/dev/null; then
    echo "Framework: Clap (Rust)"
    echo "Command path: src/commands/{{input.name}}.rs"
  fi
elif [ -f "package.json" ]; then
  if grep -q "commander" package.json 2>/dev/null; then
    echo "Framework: Commander (Node)"
  elif grep -q "yargs" package.json 2>/dev/null; then
    echo "Framework: Yargs (Node)"
  fi
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  if grep -q "click" pyproject.toml requirements.txt 2>/dev/null; then
    echo "Framework: Click (Python)"
  elif grep -q "typer" pyproject.toml requirements.txt 2>/dev/null; then
    echo "Framework: Typer (Python)"
  fi
fi
```

## Validation

- [ ] Command file created and follows existing patterns
- [ ] Command registered and shows in `--help`
- [ ] Arguments and flags parsed correctly
- [ ] Help text is clear with usage examples
- [ ] Error messages are helpful (not stack traces)
- [ ] Exit codes are correct (0 success, non-zero error)
- [ ] Tests created and passing
- [ ] Typecheck/compile passing
- [ ] Lint passing
