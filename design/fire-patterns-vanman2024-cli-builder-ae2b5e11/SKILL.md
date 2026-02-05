---
name: fire-patterns
description: Auto-generated CLI patterns using Google Fire with class-based structure, docstring parsing, and nested classes. Use when building Python CLI applications, creating Fire CLIs, implementing auto-generated commands, designing class-based CLIs, or when user mentions Fire, Google Fire, CLI generation, docstring commands, nested command groups, or Python command-line tools.
allowed-tools: Read, Write, Edit, Bash
---

# fire-patterns

Provides patterns for building Python CLI applications using Google Fire with automatic command generation from class methods, docstring-based help text, nested class structures for command groups, and rich console output integration.

## Core Patterns

### 1. Class-Based Fire CLI with Docstring Parsing

Fire automatically generates CLI commands from class methods and extracts help text from docstrings:

```python
import fire
from rich.console import Console

console = Console()

class MyCLI:
    """A powerful CLI tool with auto-generated commands"""

    def __init__(self):
        self.version = "1.0.0"
        self.config = {}

    def init(self, template='basic'):
        """Initialize a new project

        Args:
            template: Project template to use (default: basic)
        """
        console.print(f"[green]✓[/green] Initializing project with {template} template...")
        return {"status": "success", "template": template}

    def deploy(self, environment, force=False, mode='safe'):
        """Deploy to specified environment

        Args:
            environment: Target environment (dev, staging, prod)
            force: Force deployment without confirmation (default: False)
            mode: Deployment mode - fast, safe, or rollback (default: safe)
        """
        console.print(f"[cyan]Deploying to {environment} in {mode} mode[/cyan]")
        if force:
            console.print("[yellow]⚠ Force mode enabled - skipping confirmation[/yellow]")
        return {"environment": environment, "mode": mode, "forced": force}

if __name__ == '__main__':
    fire.Fire(MyCLI)
```

**Usage:**
```bash
python mycli.py init --template=react
python mycli.py deploy production --force
python mycli.py deploy staging --mode=fast
python mycli.py --help  # Auto-generated from docstrings
```

### 2. Nested Class Structure for Command Groups

Organize related commands using nested classes:

```python
import fire
from rich.console import Console

console = Console()

class MyCLI:
    """Main CLI application"""

    def __init__(self):
        self.version = "1.0.0"

    class Config:
        """Manage configuration settings"""

        def get(self, key):
            """Get configuration value

            Args:
                key: Configuration key to retrieve
            """
            value = self._load_config().get(key)
            console.print(f"[blue]Config[/blue] {key}: {value}")
            return value

        def set(self, key, value):
            """Set configuration value

            Args:
                key: Configuration key to set
                value: Configuration value
            """
            config = self._load_config()
            config[key] = value
            self._save_config(config)
            console.print(f"[green]✓[/green] Set {key} = {value}")

        def list(self):
            """List all configuration values"""
            config = self._load_config()
            console.print("[bold]Configuration:[/bold]")
            for key, value in config.items():
                console.print(f"  {key}: {value}")

        @staticmethod
        def _load_config():
            # Load configuration from file
            return {}

        @staticmethod
        def _save_config(config):
            # Save configuration to file
            pass

    class Database:
        """Database management commands"""

        def migrate(self, direction='up'):
            """Run database migrations

            Args:
                direction: Migration direction - up or down (default: up)
            """
            console.print(f"[cyan]Running migrations {direction}...[/cyan]")

        def seed(self, dataset='default'):
            """Seed database with test data

            Args:
                dataset: Dataset to use for seeding (default: default)
            """
            console.print(f"[green]Seeding database with {dataset} dataset[/green]")

        def reset(self, confirm=False):
            """Reset database to initial state

            Args:
                confirm: Confirm destructive operation (default: False)
            """
            if not confirm:
                console.print("[red]⚠ Use --confirm to reset database[/red]")
                return
            console.print("[yellow]Resetting database...[/yellow]")

if __name__ == '__main__':
    fire.Fire(MyCLI)
```

**Usage:**
```bash
python mycli.py config get database_url
python mycli.py config set api_key abc123
python mycli.py config list
python mycli.py database migrate
python mycli.py database seed --dataset=production
python mycli.py database reset --confirm
```

### 3. Multiple Return Types and Output Formatting

Fire handles different return types automatically:

```python
import fire
from rich.console import Console
from rich.table import Table
import json

console = Console()

class MyCLI:
    """CLI with rich output formatting"""

    def status(self):
        """Show application status (returns dict)"""
        return {
            "status": "running",
            "version": "1.0.0",
            "uptime": "24h",
            "active_users": 42
        }

    def list_items(self):
        """List items with table formatting (returns list)"""
        items = [
            {"id": 1, "name": "Item A", "status": "active"},
            {"id": 2, "name": "Item B", "status": "pending"},
            {"id": 3, "name": "Item C", "status": "completed"}
        ]

        table = Table(title="Items")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="green")

        for item in items:
            table.add_row(str(item['id']), item['name'], item['status'])

        console.print(table)
        return items

    def export(self, format='json'):
        """Export data in specified format

        Args:
            format: Output format - json, yaml, or text (default: json)
        """
        data = {"items": [1, 2, 3], "total": 3}

        if format == 'json':
            return json.dumps(data, indent=2)
        elif format == 'yaml':
            return f"items:\n  - 1\n  - 2\n  - 3\ntotal: 3"
        else:
            return f"Total items: {data['total']}"

if __name__ == '__main__':
    fire.Fire(MyCLI)
```

### 4. Property-Based Access and Chaining

Use properties and method chaining with Fire:

```python
import fire
from rich.console import Console

console = Console()

class MyCLI:
    """CLI with property access"""

    def __init__(self):
        self._version = "1.0.0"
        self._debug = False

    @property
    def version(self):
        """Get application version"""
        return self._version

    @property
    def debug(self):
        """Get debug mode status"""
        return self._debug

    def info(self):
        """Display application information"""
        console.print(f"[bold]Application Info[/bold]")
        console.print(f"Version: {self.version}")
        console.print(f"Debug: {self.debug}")
        return {"version": self.version, "debug": self.debug}

if __name__ == '__main__':
    fire.Fire(MyCLI)
```

**Usage:**
```bash
python mycli.py version  # Access property directly
python mycli.py debug    # Access property directly
python mycli.py info     # Call method
```

## Available Templates

Use the following templates for generating Fire CLI applications:

- **basic-fire-cli.py.template** - Simple single-class Fire CLI
- **nested-fire-cli.py.template** - Multi-class CLI with command groups
- **rich-fire-cli.py.template** - Fire CLI with rich console output
- **typed-fire-cli.py.template** - Type-annotated Fire CLI
- **config-fire-cli.py.template** - Fire CLI with configuration management
- **multi-command-fire-cli.py.template** - Complex multi-command Fire CLI

## Available Scripts

- **generate-fire-cli.sh** - Generate Fire CLI from specification
- **validate-fire-cli.py** - Validate Fire CLI structure and docstrings
- **extract-commands.py** - Extract command structure from Fire CLI
- **test-fire-cli.py** - Test Fire CLI commands programmatically

## Key Fire CLI Principles

### Automatic Command Generation

Fire automatically generates CLI commands from:
- Public methods (commands)
- Method parameters (command arguments and flags)
- Docstrings (help text and argument descriptions)
- Nested classes (command groups)
- Properties (read-only values)

### Docstring Parsing

Fire parses docstrings to generate help text:

```python
def command(self, arg1, arg2='default'):
    """Command description shown in help

    Args:
        arg1: Description of arg1 (shown in help)
        arg2: Description of arg2 (shown in help)

    Returns:
        Description of return value
    """
    pass
```

### Boolean Flags

Fire converts boolean parameters to flags:

```python
def deploy(self, force=False, verbose=False):
    """Deploy with optional flags"""
    pass

# Usage:
# python cli.py deploy --force --verbose
# python cli.py deploy --noforce  # Explicitly set to False
```

### Default Values

Default parameter values become default flag values:

```python
def init(self, template='basic', port=8000):
    """Initialize with defaults"""
    pass

# Usage:
# python cli.py init                    # Uses defaults
# python cli.py init --template=react   # Override template
# python cli.py init --port=3000        # Override port
```

## Integration with Rich Console

Enhance Fire CLIs with rich formatting:

```python
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
import fire
import time

console = Console()

class MyCLI:
    """Rich-enhanced Fire CLI"""

    def process(self, items=100):
        """Process items with progress bar

        Args:
            items: Number of items to process
        """
        console.print(Panel("[bold green]Processing Started[/bold green]"))

        for i in track(range(items), description="Processing..."):
            time.sleep(0.01)  # Simulate work

        console.print("[green]✓[/green] Processing complete!")

if __name__ == '__main__':
    fire.Fire(MyCLI)
```

## Best Practices

1. **Clear Docstrings**: Write comprehensive docstrings for auto-generated help
2. **Nested Classes**: Use nested classes for logical command grouping
3. **Default Values**: Provide sensible defaults for all optional parameters
4. **Type Hints**: Use type annotations for better IDE support
5. **Return Values**: Return data structures that Fire can serialize
6. **Rich Output**: Use rich console for enhanced terminal output
7. **Validation**: Validate inputs within methods, not in Fire setup
8. **Error Handling**: Use try-except blocks and return error messages

## Common Patterns

### Confirmation Prompts

```python
def delete(self, resource, confirm=False):
    """Delete resource with confirmation

    Args:
        resource: Resource to delete
        confirm: Skip confirmation prompt
    """
    if not confirm:
        console.print("[yellow]Use --confirm to delete[/yellow]")
        return

    console.print(f"[red]Deleting {resource}...[/red]")
```

### Environment Selection

```python
from enum import Enum

class Environment(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

def deploy(self, env: Environment):
    """Deploy to environment

    Args:
        env: Target environment (dev, staging, prod)
    """
    console.print(f"Deploying to {env.value}")
```

### Verbose Mode

```python
def __init__(self):
    self.verbose = False

def build(self, verbose=False):
    """Build project

    Args:
        verbose: Enable verbose output
    """
    self.verbose = verbose
    if self.verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
```

## Requirements

- Python 3.7+
- google-fire package: `pip install fire`
- rich package (optional): `pip install rich`
- Type hints support for better IDE integration

## Examples

See `examples/` directory for complete working examples:
- `basic-cli.md` - Simple Fire CLI walkthrough
- `nested-commands.md` - Multi-level command structure
- `rich-integration.md` - Rich console integration examples
- `advanced-patterns.md` - Complex Fire CLI patterns

---

**Purpose**: Generate maintainable Python CLI applications with automatic command generation
**Framework**: Google Fire
**Key Feature**: Zero boilerplate - commands auto-generated from class methods
