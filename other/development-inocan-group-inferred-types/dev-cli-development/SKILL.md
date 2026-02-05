---
name: dev-cli-development
description: Guide for developing AIDB dev-cli commands and services. Covers Click
  framework patterns, service architecture, command development, decorators, error
  handling, CommandExecutor, CliOutput, BaseService, BaseManager patterns. Use when
  working with src/aidb_cli/, adding CLI commands, creating services, or integrating
  with Docker/test/adapter systems.
---

# Dev-CLI Development Guide

## Purpose

The AIDB dev-cli (`src/aidb_cli/`) is a Click-based command-line interface for AIDB development workflows. This skill guides developers in:

- Adding new CLI commands and command groups
- Creating reusable services following BaseService pattern
- Using custom decorators (@handle_exceptions, @require_repo_context)
- Integrating with Docker, test, and adapter systems
- Following Click framework best practices
- Proper error handling and output formatting

## When to Use This Skill

Auto-activates when:

- Editing files in `src/aidb_cli/`
- Mentioning "dev-cli", "CLI command", "Click", "CliOutput"
- Adding commands, services, or CLI utilities
- Working with test orchestration or Docker integration

## Related Skills

When developing CLI commands, you may also need:

- **testing-strategy** - CLI orchestrates test execution via test coordinator service
- **code-reuse-enforcement** - CLI must use existing constants and avoid magic strings

## Architecture Overview

**For comprehensive architecture details**, see `docs/developer-guide/cli-reference.md` and source code in `src/aidb_cli/`.

### Component Structure

```
src/aidb_cli/
├── commands/      # CLI command definitions (13 modules)
├── services/      # Business logic services (41+ files)
├── managers/      # High-level orchestration (singleton pattern)
├── core/          # Decorators, utilities, constants, param types
└── generators/    # Code generation for test scenarios
```

### Key Patterns

1. **Commands** - Thin wrappers that delegate to services
1. **Services** - Reusable business logic with CommandExecutor
1. **Managers** - Singleton orchestrators for complex workflows
1. **Context Injection** - Dependencies via Click's `ctx.obj`
1. **Unified Error Handling** - `@handle_exceptions` decorator
1. **Dynamic Parameter Types** - Custom types with shell completion

## Quick Start: Adding a Command

### Step 1: Create Command File

Create `src/aidb_cli/commands/mycommand.py`:

```python
"""My new command description."""

import click

from aidb_cli.core.decorators import handle_exceptions
from aidb_logging import get_cli_logger

logger = get_cli_logger(__name__)


@click.group(name="mycommand")
@click.pass_context
def group(ctx: click.Context) -> None:
    """Command group description."""
    pass


@group.command()
@click.option("--option", "-o", help="Option description")
@click.pass_context
@handle_exceptions
def subcommand(ctx: click.Context, option: str) -> None:
    """Subcommand description."""
    # Get dependencies from context
    output = ctx.obj.output
    repo_root = ctx.obj.repo_root
    executor = ctx.obj.command_executor

    # Delegate to service
    from aidb_cli.services.myservice import MyService
    service = MyService(repo_root, executor)
    result = service.do_something(option)

    # User-facing output (via OutputStrategy)
    output.success(f"Done: {result}")
```

### Step 2: Register Command

In `src/aidb_cli/cli.py`:

```python
from aidb_cli.commands import mycommand

# In main CLI setup
cli.add_command(mycommand.group)
```

### Step 3: Test

```bash
./dev-cli mycommand subcommand --option value
```

## Command Development Patterns

### Decorator Order (CRITICAL)

**Always stack decorators in this exact order**:

```python
@group.command()                    # 1. Click command
@click.option("--opt", "-o")        # 2. Options
@click.pass_context                 # 3. Context (BEFORE handle_exceptions)
@handle_exceptions                  # 4. Error handling (LAST)
def command(ctx: click.Context, opt: str) -> None:
    """Implementation."""
```

**Wrong order causes cryptic errors!**

### Custom Parameter Types

Use custom types for validation and autocompletion:

```python
from aidb_cli.core.param_types import TestSuiteParamType

@click.option("--suite", type=TestSuiteParamType(), required=True)
def command(ctx: click.Context, suite: str) -> None:
    """Command with validated suite parameter."""
```

Available: `TestSuiteParamType`, `LanguageParamType`, `DockerProfileParamType`, `TestMarkerParamType`

**For comprehensive Click patterns**, see [click-framework-patterns.md](resources/click-framework-patterns.md):

- Decorator stacking rules explained
- All custom parameter types with examples
- Context management patterns
- Error handling with @handle_exceptions
- Command groups and subcommands
- Advanced Click patterns

## Service Development Patterns

### BaseService Pattern (Recommended)

Most services extend `BaseService` for consistent dependency injection and utilities:

```python
from aidb_cli.managers.base.service import BaseService

class MyService(BaseService):
    def __init__(self, repo_root: Path, command_executor=None, ctx=None):
        super().__init__(repo_root, command_executor, ctx)
        # Inherited: command_executor, resolved_env, logging methods, path utilities

    def do_something(self) -> str:
        self.log_info("Starting operation...")
        return self.command_executor.execute(["cmd"], cwd=self.repo_root).stdout
```

**See [service-patterns.md](resources/service-patterns.md)** for comprehensive BaseService details, advanced patterns, and testing examples.

### Standalone Service Pattern

For simple services without BaseService:

```python
class MyService:
    """Service for my operations."""

    def __init__(
        self,
        repo_root: Path,
        command_executor: CommandExecutor,
        logger: Logger | None = None
    ):
        self.repo_root = repo_root
        self.executor = command_executor
        self.logger = logger or get_cli_logger(__name__)

    def do_something(self, arg: str) -> str:
        """Do something useful."""
        from aidb.common.errors import AidbError

        result = self.executor.execute(["command", arg], cwd=self.repo_root)
        if result.returncode != 0:
            raise AidbError(f"Operation failed: {result.stderr}")
        return result.stdout.strip()
```

**Key principles**:

- Accept dependencies in `__init__` (testable)
- Use `CommandExecutor` for all subprocess calls
- Log with `get_cli_logger(__name__)`
- Raise exceptions for errors

**For comprehensive service patterns**, see [service-patterns.md](resources/service-patterns.md):

- BaseService detailed patterns
- CommandExecutor comprehensive guide
- Service composition and singletons
- Testing services
- Real examples from AIDB codebase

## Error Handling

### @handle_exceptions Decorator

This decorator provides unified error handling:

```python
@handle_exceptions
def command(ctx: click.Context) -> None:
    """Command with automatic error handling."""
    # Just raise errors naturally - decorator handles:
    # - KeyboardInterrupt (cleanup Docker resources)
    # - AidbError (formatted error output)
    # - FileNotFoundError (specific exit code)
    # - PermissionError (specific exit code)
    # - Generic exceptions (traceback in verbose mode)

    if not valid:
        from aidb.common.errors import AidbError
        raise AidbError("Validation failed")
```

### Exit Codes

Use standard exit codes:

```python
from aidb_cli.core.constants import ExitCode

if error:
    CliOutput.error("Operation failed")
    ctx.exit(ExitCode.GENERAL_ERROR)  # 1

if not found:
    ctx.exit(ExitCode.NOT_FOUND)  # 2

if config_error:
    ctx.exit(ExitCode.CONFIG_ERROR)  # 3
```

## Output and Logging

### OutputStrategy for Commands

Commands use `ctx.obj.output` (OutputStrategy) for verbosity-aware user-facing output:

```python
output = ctx.obj.output

output.success("Operation completed")  # Always visible (green)
output.error("Operation failed")       # Always visible (red, stderr)
output.warning("Potential issue")      # Always visible (yellow)
output.plain("Regular message")        # Always visible (no color)
output.section("Title", Icons.ROCKET)  # Always visible (with separator)
output.info("Verbose detail")          # Only with -v flag
output.debug("Debug trace")            # Only with -vvv flag
```

### CliOutput for Services/Managers

Services and managers (without Click context) use the static `CliOutput` utility:

```python
from aidb_cli.core.utils import CliOutput

CliOutput.success("Operation completed successfully")
CliOutput.error("Operation failed")
```

### Logger for Debugging

Use logger for debugging/trace information:

```python
from aidb_logging import get_cli_logger

logger = get_cli_logger(__name__)

logger.debug("Detailed debugging info")
logger.info("General info")
```

**Rule**: Commands → `ctx.obj.output`, Services → `CliOutput`, Debugging → `logger`

## Verbosity Levels

CLI supports three verbosity levels via global flags:

| Flag   | Log Level | Enabled Features                                |
| ------ | --------- | ----------------------------------------------- |
| (none) | INFO      | Standard output only                            |
| `-v`   | DEBUG     | + AIDB_ADAPTER_TRACE=1                          |
| `-vvv` | TRACE     | + AIDB_ADAPTER_TRACE=1 + AIDB_CONSOLE_LOGGING=1 |

**What each level includes:**

- **INFO**: User-facing milestones (session started, breakpoint hit, etc.)
- **DEBUG**: Operation summaries, state transitions, adapter lifecycle
- **TRACE**: Full DAP/LSP JSON payloads, receiver timing, protocol details

**Examples:**

```bash
./dev-cli test run -s unit          # INFO level
./dev-cli -v test run -s unit       # DEBUG + adapter traces
./dev-cli -vvv test run -s unit     # TRACE + protocol payloads
```

Use `-vvv` for maximum observability when debugging DAP/LSP protocol issues.

## Common Patterns

### Import Organization

Follow project standard: stdlib → third-party → AIDB core → CLI → logging. All imports at top unless avoiding circular dependency.

**Avoiding circular imports**: Use `TYPE_CHECKING` for type-only imports:

```python
from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from aidb_cli.cli import Context  # Only imported for type checking
```

See `CLAUDE.md` for full style details.

### Service Instantiation in Commands

```python
@group.command()
@click.pass_context
@handle_exceptions
def command(ctx: click.Context) -> None:
    """Command that uses a service."""
    # Instantiate service with dependencies from context
    from aidb_cli.services.adapter.adapter_build_service import AdapterBuildService

    service = AdapterBuildService(
        repo_root=ctx.obj.repo_root,
        command_executor=ctx.obj.command_executor
    )

    # Call service method
    result = service.build_locally(["python"], verbose=False)

    # Output result
    CliOutput.success(f"Built adapter: {result}")
```

## Common Pitfalls

### 1. Decorator Order

**Wrong**: `@handle_exceptions` before `@click.pass_context`
**Right**: `@click.pass_context` then `@handle_exceptions`

### 2. Using subprocess Directly

**Wrong**: `subprocess.run(["cmd"])`
**Right**: `ctx.obj.command_executor.execute(["cmd"])`

### 3. Mixing Output Types

**Wrong**: `print("Success")` or `logger.info("User message")`
**Right**: `CliOutput.success("Message")` for users, `logger.debug()` for debugging

### 4. Hardcoded Paths

**Wrong**: `Path("/path/to/repo")`
**Right**: `ctx.obj.repo_root / "relative/path"`

## Real Code Examples

### Example 1: Simple Command

From `src/aidb_cli/commands/docker.py`:

```python
@group.command()
@click.option("--profile", "-p", type=DockerProfileParamType(), default=None)
@click.option("--no-cache", is_flag=True, help="Build without cache")
@click.pass_context
@handle_exceptions
def build(ctx: click.Context, profile: str | None, no_cache: bool) -> None:
    """Build Docker images."""
    from aidb_cli.services.docker.docker_build_service import DockerBuildService

    service = DockerBuildService(
        repo_root=ctx.obj.repo_root,
        command_executor=ctx.obj.command_executor
    )

    result = service.build_images(profile=profile, no_cache=no_cache)
    CliOutput.success(f"Build complete: {result}")
```

### Example 2: Service with CommandExecutor

**See real implementation**: `src/aidb_cli/services/docker/docker_build_service.py`

Key pattern - services delegate to CommandExecutor and raise exceptions on failure:

```python
class DockerBuildService:
    def __init__(self, repo_root: Path, command_executor: CommandExecutor):
        self.repo_root = repo_root
        self.executor = command_executor

    def build_images(self, profile: str | None = None) -> int:
        """Build Docker images."""
        from aidb.common.errors import AidbError

        cmd = ["docker-compose", "build"]
        if profile:
            cmd.extend(["--profile", profile])

        result = self.executor.execute(cmd, cwd=self.repo_root)
        if result.returncode != 0:
            raise AidbError(f"Build failed: {result.stderr}")
        return 0
```

## Testing Your Changes

### Run CLI Locally

```bash
./dev-cli mycommand subcommand --option value    # Run command
./dev-cli -v mycommand subcommand                # Verbose mode
./dev-cli --dry-run mycommand subcommand         # Dry run (no execution)
```

### Unit Testing Services

Test services by mocking CommandExecutor:

```python
from unittest.mock import Mock
from pathlib import Path

def test_my_service():
    """Test service logic without executing commands."""
    executor = Mock()
    executor.execute.return_value = Mock(returncode=0, stdout="success")

    service = MyService(Path("/tmp"), executor)
    result = service.do_something("arg")

    assert result == "success"
    executor.execute.assert_called_once_with(["command", "arg"], cwd=Path("/tmp"))
```

**See actual test examples**: `src/tests/aidb_cli/commands/integration/` for command integration tests and `src/tests/aidb_cli/services/` for service unit tests

## Service Discovery Guide

Common tasks and which services to use:

| Task                           | Service                        | Location                                             |
| ------------------------------ | ------------------------------ | ---------------------------------------------------- |
| Build Docker images            | `DockerBuildService`           | `services/docker/docker_build_service.py`            |
| Generate docker-compose.yaml   | `ComposeGeneratorService`      | `services/docker/compose_generator_service.py`       |
| Track Docker image checksums   | `DockerImageChecksumService`   | `services/docker/docker_image_checksum_service.py`   |
| Track framework deps checksums | `FrameworkDepsChecksumService` | `services/docker/framework_deps_checksum_service.py` |
| Check Docker health            | `DockerHealthService`          | `services/docker/docker_health_service.py`           |
| Run tests                      | `TestCoordinatorService`       | `services/test/test_coordinator_service.py`          |
| Build adapters                 | `AdapterBuildService`          | `services/adapter/adapter_build_service.py`          |
| Execute commands               | `CommandExecutor`              | `services/command_executor/__init__.py`              |
| Generate test programs         | `Generator`                    | `generators/core/generator.py`                       |

**Full service list**: See `src/aidb_cli/services/` subdirectories - `docker/` (Docker operations), `test/` (test execution), `adapter/` (adapter building), `docs/` (documentation), `command_executor/` (subprocess execution)

## Resource Files

For deeper dives into specific topics, see:

- **[service-patterns.md](resources/service-patterns.md)** - Comprehensive service architecture patterns, CommandExecutor guide, testing, real examples
- **[click-framework-patterns.md](resources/click-framework-patterns.md)** - Click decorator stacking, custom parameter types, context management, error handling
- **[docker-compose-generation.md](resources/docker-compose-generation.md)** - Template-based docker-compose.yaml generation, Jinja2 templates, languages.yaml configuration, hash-based cache invalidation
- **[checksum-services.md](resources/checksum-services.md)** - ChecksumServiceBase pattern, DockerImageChecksumService, FrameworkDepsChecksumService, container lifecycle tracking, creating custom checksum services

______________________________________________________________________
