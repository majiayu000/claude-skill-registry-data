---
name: hk
description: Use jdx/hk git hook manager to setup, configure, and manage git hooks and linters. Invoke when user asks to setup hk, configure hooks, add linters, or work with pre-commit/pre-push hooks.
---

# hk - Git Hook Manager

You are an expert in using **hk**, a high-performance git hook manager and project linting tool created by jdx. This skill helps users set up, configure, and use hk in their projects.

## What is hk?

hk is a git hook manager with tight integration with linters, emphasizing performance through concurrency and file locking. It pairs excellently with mise-en-place for dependency management.

## Installation

When the user needs to install hk, recommend these methods in order:

1. **mise-en-place** (recommended): `mise use hk pkl`
   - Also installs pkl (required for configuration)
2. **Homebrew**: `brew install hk`
3. **Cargo**: `cargo install hk`
4. **Aqua**: `aqua g -i jdx/hk`

## Project Setup

### Initial Setup

1. Initialize configuration:
   ```bash
   hk init
   ```
   This generates `hk.pkl` in the project root.

2. Install hooks into git:
   ```bash
   hk install
   ```
   This configures git to use hooks from `hk.pkl`.

### Configuration Structure

The `hk.pkl` file uses Apple's Pkl configuration language with this basic structure:

```pkl
amends "package://github.com/jdx/hk/releases/download/v1.20.0/hk@1.20.0#/Config.pkl"

linters {
  ["my-linter"] {
    glob = "**/*.py"
    check = "python -m pylint"
    fix = "python -m black"
  }
}

hooks {
  ["pre-commit"] {
    steps {
      ["my-linter"] {}
    }
  }
}
```

## Core Concepts

### Linters

Linters define the actual checks and fixes to run. Key properties:

- **glob**: File patterns to match (e.g., `"**/*.ts"`, `"src/**/*.py"`)
- **check**: Read-only command to validate files (runs with `hk check`)
- **fix**: Command to automatically correct issues (runs with `hk fix`)
- **stage**: Glob patterns for files to stage after fixes
- **batch**: Enable parallel processing across file batches
- **exclusive**: Set to `true` to block concurrent execution
- **workspace_indicator**: File to identify workspace root (e.g., `"Cargo.toml"` for Rust)

### Hooks

Hooks define when linters execute. Available hooks:

- **pre-commit**: Runs before git commits
- **pre-push**: Runs before git pushes
- **fix**: Manual invocation via `hk fix`
- **check**: Manual invocation via `hk check`

Hook configuration options:

- `fix: bool` - Enable modification mode
- `stash: String` - Preserve unstaged changes ("git", "patch-file", "none")
- `steps` - Mapping of linters to execute

### Built-in Linters

hk provides many built-in linters accessible via the Builtins library:

```pkl
import "package://github.com/jdx/hk/releases/download/v1.20.0/hk@1.20.0#/Builtins.pkl"

linters = Builtins.linters
```

Common built-ins include: prettier, eslint, black, ruff, shellcheck, actionlint, and many more.

## Common Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `hk init` | Initialize new hk.pkl config | First-time setup |
| `hk install` | Configure git to use hk hooks | After creating/updating hk.pkl |
| `hk check` | Verify files without modification | CI/CD, pre-commit validation |
| `hk check --all` | Check all files in repo | CI/CD pipelines |
| `hk check --from-ref main` | Check changes since main branch | PR validation |
| `hk fix` | Fix issues and modify files | Local development |
| `hk run pre-commit` | Manually execute specific hook | Testing hook configuration |
| `hk run pre-commit --all` | Run hook on all files | Testing, CI |

## Configuration Examples

### Simple Python Linter

```pkl
linters {
  ["black"] {
    glob = "**/*.py"
    check = "black --check"
    fix = "black"
  }
}

hooks {
  ["pre-commit"] {
    steps {
      ["black"] {}
    }
  }
}
```

### Using Built-in Linters

```pkl
import "package://github.com/jdx/hk/releases/download/v1.20.0/hk@1.20.0#/Builtins.pkl"

linters = Builtins.linters.toMap()

hooks {
  ["pre-commit"] {
    steps {
      ["prettier"] {}
      ["eslint"] {}
    }
  }
}
```

### Multiple Hooks with Different Behavior

```pkl
linters {
  ["quick-lint"] {
    glob = "src/**/*.ts"
    check = "eslint"
  }
  ["thorough-lint"] {
    glob = "**/*.ts"
    check = "eslint --max-warnings 0"
  }
}

hooks {
  ["pre-commit"] {
    steps {
      ["quick-lint"] {}
    }
  }
  ["pre-push"] {
    steps {
      ["thorough-lint"] {}
    }
  }
}
```

### Conditional Steps

```pkl
linters {
  ["test"] {
    glob = "**/*.test.ts"
    check = "npm test"
    condition = "git diff --cached --name-only | grep -q '.test.ts$'"
  }
}
```

## Advanced Features

### Global Configuration

Create `~/.hkrc.pkl` for settings shared across all projects:

```pkl
amends "package://github.com/jdx/hk/releases/download/v1.20.0/hk@1.20.0#/Config.pkl"

jobs = 8
fail_fast = false
exclude = [".git/**", "node_modules/**"]
```

### Environment Variables

Set environment variables for linters:

```pkl
env {
  ["NODE_ENV"] = "development"
}

linters {
  ["eslint"] {
    glob = "**/*.js"
    check = "eslint"
    env {
      ["ESLINT_USE_FLAT_CONFIG"] = "true"
    }
  }
}
```

### Configuration Precedence

Settings merge from multiple sources (highest to lowest priority):

1. CLI flags: `--fail-fast`, `--jobs`
2. Environment variables: `HK_JOBS=8`
3. Git config (local/global)
4. User rc file: `~/.hkrc.pkl`
5. Project config: `hk.pkl`
6. Built-in defaults

## Integration with mise

hk works exceptionally well with mise-en-place:

```bash
# Install both tools
mise use hk pkl

# Use mise tasks for complex workflows
mise task add lint "hk check --all"
mise task add fix "hk fix"
```

## Best Practices

1. **Start Simple**: Begin with built-in linters, customize only when needed
2. **Use mise**: Manage hk and pkl versions with mise for consistency
3. **Check in CI**: Use `hk check --all` in CI to validate all files
4. **Incremental Checks**: Use `hk check --from-ref main` for PR validation
5. **Exclusive Steps**: Mark sequential operations as `exclusive = true`
6. **Test Hooks**: Run `hk run pre-commit --all` before pushing config changes
7. **Global Excludes**: Set common exclusions in `~/.hkrc.pkl`
8. **Workspace Awareness**: Use `workspace_indicator` for monorepos

## Troubleshooting

### Hook Not Running

```bash
# Reinstall hooks
hk install

# Verify git hook configuration
cat .git/hooks/pre-commit
```

### Performance Issues

```pkl
// Increase parallelism
jobs = 8

// Disable check before fix
check_first = false
```

### Linter Not Matching Files

```bash
# Test glob pattern
hk check --all --verbose

# Verify files exist
find . -name "*.py"
```

## When to Use This Skill

Invoke this skill when the user:

- Wants to set up git hooks in a project
- Needs to configure pre-commit or pre-push hooks
- Asks about managing linters or formatters
- Wants to improve code quality automation
- Mentions hk, git hooks, or linting workflows
- Needs to integrate linters with git workflow

## Instructions

When helping users with hk:

1. **Assess Current State**: Check if hk is installed and configured
2. **Understand Goals**: Ask what linters/hooks they want to set up
3. **Recommend Installation**: Suggest mise-based installation when possible
4. **Provide Config**: Create appropriate `hk.pkl` based on their project
5. **Test Setup**: Help run `hk check` or `hk fix` to verify configuration
6. **Document**: Explain what each configuration does and why

Always consider:

- Project language and existing tooling
- Whether they use mise-en-place
- CI/CD integration needs
- Team collaboration (project skills vs personal)
- Performance requirements (parallelism, exclusions)

## Additional Resources

For more details, see [reference.md](reference.md) for comprehensive configuration options and examples.
