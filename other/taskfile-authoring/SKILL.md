---
name: taskfile-authoring
description: "Author and maintain Taskfile.yml files for the Task runner (taskfile.dev). Use when creating, editing, or troubleshooting Taskfiles, writing task definitions, configuring task variables, environment variables, dependencies, or when users ask about Task automation, task runner configuration, or YAML-based build systems. Covers Taskfile schema, task composition, includes, remote Taskfiles, and cross-platform compatibility."
metadata:
  version: 0.1.0
  taskfile_schema_version: "3"
  task_cli_version: "3.50.0"
  latest_task_cli_version: "3.51.1"
  last_verified: "2026-09-13"
---

# Taskfile Authoring Skill

Create and maintain Taskfile.yml files for the Task runner (taskfile.dev). This skill provides procedural knowledge for authoring effective Taskfiles, grounded in official documentation.

## Quick start

Create a new Taskfile:
```sh
task --init
```

Minimal Taskfile structure:
```yaml
version: '3'

tasks:
  default:
    desc: Print a greeting
    cmds:
      - echo "Hello, World!"
    silent: true
```

Run with `task` (default task) or `task <task-name>`.

## Core concepts

### Task definition
```yaml
tasks:
  build:
    desc: Build the project
    cmds:
      - go build ./cmd/main.go
    env:
      CGO_ENABLED: "0"
    dir: ./cmd
    deps: [clean]
    preconditions:
      - test -f main.go
    generates:
      - ./bin/app
    sources:
      - "*.go"
    method: checksum
```

### Variables and templating
```yaml
vars:
  APP_NAME: myapp
  VERSION:
    sh: git describe --tags --always
tasks:
  greet:
    cmds:
      - echo "Building {{.APP_NAME}} v{{.VERSION}}"
```

### Environment variables
```yaml
env:
  GOOS: linux
  GOARCH: amd64
tasks:
  build:
    cmds:
      - go build -o bin/app .
```

### Includes and namespaces
```yaml
includes:
  docs: ./documentation
  docker: ./DockerTasks.yml
```

### Task dependencies and composition
```yaml
tasks:
  test:
    cmds:
      - go test ./...
  lint:
    cmds:
      - golangci-lint run
  ci:
    deps: [test, lint]
    desc: Run all CI checks
```

## Common patterns

### Cross-platform compatibility
Task uses mvdan/sh, a native Go sh interpreter. Write sh/bash-like commands that work across platforms.

### Conditional execution
```yaml
tasks:
  deploy:
    preconditions:
      - test -f deploy.key
      - sh: test "$ENV" = "production"
        msg: "Not in production environment"
    cmds:
      - ./deploy.sh
```

### Watch mode
```yaml
tasks:
  dev:
    cmds:
      - npm run dev
    desc: Start development server
    run: once
```

### File operations
```yaml
tasks:
  clean:
    cmds:
      - rm -rf dist/
      - rm -f *.log
    desc: Clean build artifacts
```

## Reference documentation

For detailed information, consult these reference files:
- **[Installation](references/installation.md)**: All methods to install Task (package managers, binary, script, GitHub Actions)
- **[Guide](references/guide.md)**: Comprehensive guide covering Taskfile features, includes, variables, environment, and advanced usage
- **[Schema](references/schema.md)**: Taskfile schema reference and supported file names

## Workflow

1. **Identify task requirements**: What commands, environment, dependencies?
2. **Structure the Taskfile**: Use appropriate version, define tasks with clear names
3. **Add metadata**: descriptions, preconditions, generates/sources for incremental builds
4. **Test tasks**: Run `task --list` to verify, `task <name>` to execute
5. **Validate**: Use `task --dry` for dry runs, check for syntax errors

## Best practices

- Use `version: '3'` for latest features
- Add `desc` to all tasks for discoverability
- Use `silent: true` for cleaner output
- Define variables at top level for reuse
- Use `preconditions` for safety checks
- Use `generates` and `sources` for incremental builds
- Prefer `deps` over `cmds` for parallel execution
- Use `dir` for tasks that need to run in specific directories

## Version Tracking

This skill tracks the Taskfile schema version and Task CLI version it supports:

- **Skill version**: 0.1.0
- **Taskfile schema version**: 3
- **Task CLI version**: 3.50.0
- **Latest Task CLI version**: 3.51.1
- **Last verified**: 2026-09-13

### Upgrading Task CLI

To update Task CLI to the latest version:
```sh
# Using winget (Windows)
winget upgrade Task.TaskCommunity

# Using Homebrew (macOS)
brew upgrade go-task

# Using npm
npm update -g @go-task/cli

# Using install script (Linux/macOS)
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
```

### Upgrading the Skill

When new Taskfile versions are released:

1. **Check the official changelog**: Visit [taskfile.dev/docs/changelog](https://taskfile.dev/docs/changelog) for new features
2. **Compare versions**: Check if `taskfile_schema_version` or `task_cli_version` in this skill's metadata are outdated
3. **Update references**: Update `references/schema.md` with new schema features
4. **Test compatibility**: Verify examples work with the new version
5. **Update metadata**: Bump `version` and update `last_verified` date

### Version Comparison Template

When checking for updates, compare:
```yaml
# Current skill metadata
metadata:
  version: 0.1.0
  taskfile_schema_version: "3"
  task_cli_version: "3.50.0"
  latest_task_cli_version: "3.51.1"
  last_verified: "2026-09-13"

# Compare with latest Taskfile release
# If schema version > "3" or CLI version > "3.50.0", update this skill
```

## Troubleshooting

- **Task not found**: Check task name with `task --list`
- **Variable not expanding**: Ensure proper `{{.VAR}}` syntax
- **Command not found**: Task uses mvdan/sh; ensure executables are in PATH
- **Cross-platform issues**: Test on target platforms; avoid shell-specific features
- **Include not working**: Verify relative paths and schema version compatibility

For installation instructions and platform-specific details, see [references/installation.md](references/installation.md).
For comprehensive guide and advanced features, see [references/guide.md](references/guide.md).