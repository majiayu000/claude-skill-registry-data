---
name: typer-patterns
description: Modern type-safe Typer CLI patterns with type hints, Enums, and sub-apps. Use when building CLI applications, creating Typer commands, implementing type-safe CLIs, or when user mentions Typer, CLI patterns, type hints, Enums, sub-apps, or command-line interfaces.
allowed-tools: Read, Write, Edit, Bash
---

# typer-patterns

Provides modern type-safe Typer CLI patterns including type hints, Enum usage, sub-app composition, and Typer() instance patterns for building maintainable command-line applications.

## Core Patterns

### 1. Type-Safe Commands with Type Hints

Use Python type hints for automatic validation and better IDE support:

```python
import typer
from typing import Optional
from pathlib import Path

app = typer.Typer()

@app.command()
def process(
    input_file: Path = typer.Argument(..., help="Input file path"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    count: int = typer.Option(10, help="Number of items to process")
) -> None:
    """Process files with type-safe parameters."""
    if verbose:
        typer.echo(f"Processing {input_file}")
```

### 2. Enum-Based Options

Use Enums for constrained choices with autocomplete:

```python
from enum import Enum

class OutputFormat(str, Enum):
    json = "json"
    yaml = "yaml"
    text = "text"

@app.command()
def export(
    format: OutputFormat = typer.Option(OutputFormat.json, help="Output format")
) -> None:
    """Export with enum-based format selection."""
    typer.echo(f"Exporting as {format.value}")
```

### 3. Sub-Application Composition

Organize complex CLIs with sub-apps:

```python
app = typer.Typer()
db_app = typer.Typer()
app.add_typer(db_app, name="db", help="Database commands")

@db_app.command("migrate")
def db_migrate() -> None:
    """Run database migrations."""
    pass

@db_app.command("seed")
def db_seed() -> None:
    """Seed database with test data."""
    pass
```

### 4. Typer() Instance Pattern

Use Typer() instances for better organization and testing:

```python
def create_app() -> typer.Typer:
    """Factory function for creating Typer app."""
    app = typer.Typer(
        name="myapp",
        help="My CLI application",
        add_completion=True,
        no_args_is_help=True
    )

    @app.command()
    def hello(name: str) -> None:
        typer.echo(f"Hello {name}")

    return app

app = create_app()

if __name__ == "__main__":
    app()
```

## Usage Workflow

1. **Identify pattern need**: Determine which Typer pattern fits your use case
2. **Select template**: Choose from templates/ based on complexity
3. **Customize**: Adapt type hints, Enums, and sub-apps to your domain
4. **Validate**: Run validation script to check type safety
5. **Test**: Use example tests as reference

## Template Selection Guide

- **basic-typed-command.py**: Single command with type hints
- **enum-options.py**: Commands with Enum-based options
- **sub-app-structure.py**: Multi-command CLI with sub-apps
- **typer-instance.py**: Factory pattern for testable CLIs
- **advanced-validation.py**: Custom validators and callbacks

## Validation

Run the type safety validation:

```bash
./scripts/validate-types.sh path/to/cli.py
```

Checks:
- All parameters have type hints
- Return types specified
- Enums used for constrained choices
- Proper Typer decorators

## Examples

See `examples/` for complete working CLIs:
- `examples/basic-cli/`: Simple typed CLI
- `examples/enum-cli/`: Enum-based options
- `examples/subapp-cli/`: Multi-command with sub-apps
- `examples/factory-cli/`: Testable Typer factory pattern

## Best Practices

1. **Always use type hints**: Enables auto-validation and IDE support
2. **Prefer Enums over strings**: For constrained choices
3. **Use Path for file paths**: Better validation than str
4. **Document with docstrings**: Typer uses them for help text
5. **Keep commands focused**: One command = one responsibility
6. **Use sub-apps for grouping**: Organize related commands together
7. **Test with factory pattern**: Makes CLIs unit-testable

## Common Patterns

### Callback for Global Options

```python
@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    ctx: typer.Context = typer.Context
) -> None:
    """Global options applied to all commands."""
    ctx.obj = {"verbose": verbose}
```

### Custom Validators

```python
def validate_port(value: int) -> int:
    if not 1024 <= value <= 65535:
        raise typer.BadParameter("Port must be between 1024-65535")
    return value

@app.command()
def serve(port: int = typer.Option(8000, callback=validate_port)) -> None:
    """Serve with validated port."""
    pass
```

### Rich Output Integration

```python
from rich.console import Console

console = Console()

@app.command()
def status() -> None:
    """Show status with rich formatting."""
    console.print("[bold green]System online[/bold green]")
```

## Integration Points

- Use with `cli-structure` skill for overall CLI architecture
- Combine with `testing-patterns` for CLI test coverage
- Integrate with `packaging` skill for distribution

## References

- Templates: `templates/`
- Scripts: `scripts/validate-types.sh`, `scripts/generate-cli.sh`
- Examples: `examples/*/`
