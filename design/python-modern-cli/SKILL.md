---
name: python-modern-cli
description: Build professional Python CLIs with modern UX patterns using pyfiglet (ASCII banners), typer (commands), questionary (interactions), and rich (formatting). Use when creating command-line tools, automation scripts with user interaction, data processing pipelines with CLI interfaces, or upgrading existing Python scripts to professional CLIs. Ideal for ETL workflows, GIS tools, data analysis utilities, and civic tech projects requiring reproducible, scriptable interfaces.
---

# Python Modern CLI

Build professional command-line interfaces in Python combining visual appeal, interactive UX, and clear output formatting.

## Quick Start

Copy the base template from `assets/cli_template.py` as starting point. Install dependencies:

```bash
pip install typer[all] rich questionary pyfiglet --break-system-packages
```

Basic structure:

```python
import typer
from rich.console import Console
from pyfiglet import figlet_format
import questionary

app = typer.Typer()
console = Console()

def show_banner(title: str):
    console.print(figlet_format(title, font="slant"), style="bold cyan")

@app.command()
def process(
    input_file: str = typer.Argument(..., help="Input file path"),
    output: str = typer.Option("output.csv", "--output", "-o"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """Process data with clear feedback"""
    if verbose:
        show_banner("My Tool")
    
    console.print(f"[green]Processing {input_file}...[/green]")
    # ... processing logic ...
    console.print("[bold green]✓ Done![/bold green]")

if __name__ == "__main__":
    app()
```

## Core Components

### 1. Pyfiglet - Visual Identity

Create memorable ASCII art banners. Use sparingly for main commands or when `--verbose`.

```python
from pyfiglet import figlet_format
from rich.console import Console

console = Console()

# Simple banner
banner = figlet_format("Tool Name", font="slant")
console.print(banner, style="bold cyan")

# Common fonts: slant, banner, digital, standard
```

### 2. Typer - Command Structure

Define commands, arguments, options with type hints and validation.

```python
import typer
from pathlib import Path
from typing import Optional

app = typer.Typer()

@app.command()
def convert(
    input_file: Path = typer.Argument(..., exists=True, help="Input CSV"),
    format: str = typer.Option("geojson", "--format", "-f", 
                               help="Output format"),
    dry_run: bool = typer.Option(False, "--dry-run")
):
    """Convert data to specified format"""
    pass

# Multiple commands
data_app = typer.Typer()
app.add_typer(data_app, name="data")

@data_app.command("import")
def import_data(source: str):
    """Import from source"""
    pass
```

### 3. Questionary - User Interaction

Interactive prompts when flags/args are insufficient or for confirmations.

```python
import questionary

# Text input with validation
def validate_url(text):
    return text.startswith("http") or "URL must start with http"

url = questionary.text(
    "API endpoint:",
    validate=validate_url
).ask()

# Selection
operation = questionary.select(
    "Choose operation:",
    choices=["Extract", "Transform", "Load"]
).ask()

# Autocomplete for known values
dataset = questionary.autocomplete(
    "Select dataset:",
    choices=["istat_pop", "anac_contracts", "geo_comuni"]
).ask()

# Confirmation before destructive operations
if questionary.confirm("Delete all data?").ask():
    # proceed

# Multiple selection
features = questionary.checkbox(
    'Enable features:',
    choices=['Cache', 'Logging', 'Validation']
).ask()
```

### 4. Rich - Output Formatting

Tables, progress bars, colored messages, panels for structured output.

```python
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel

console = Console()

# Tables for data display
table = Table(title="Processing Results")
table.add_column("File", style="cyan")
table.add_column("Records", justify="right", style="green")
table.add_column("Status", justify="center")

for file in results:
    table.add_row(file.name, str(file.count), "✓")
console.print(table)

# Progress for long operations
with Progress() as progress:
    task = progress.add_task("[cyan]Processing files...", total=len(files))
    for file in files:
        process_file(file)
        progress.update(task, advance=1)

# Panels for important messages
console.print(Panel(
    "[bold]Configuration saved[/bold]\nLocation: ~/.myapp/config.json",
    title="Success",
    border_style="green"
))

# Errors
console.print(Panel(
    f"[bold red]Error:[/bold red] Invalid file format",
    border_style="red"
))
```

## Design Patterns

### ETL Pipeline CLI

```python
@app.command()
def pipeline(
    source: str = typer.Argument(..., help="Data source URL"),
    output_dir: Path = typer.Option("./output", "--output", "-o"),
    validate: bool = typer.Option(True, "--validate/--no-validate")
):
    """Run complete ETL pipeline"""
    show_banner("ETL Pipeline")
    
    steps = ["Extract", "Transform", "Validate", "Load"]
    with Progress() as progress:
        task = progress.add_task("[cyan]Pipeline", total=len(steps))
        
        # Extract
        data = extract_data(source)
        progress.update(task, advance=1, description="[cyan]Extracting...")
        
        # Transform
        transformed = transform(data)
        progress.update(task, advance=1, description="[cyan]Transforming...")
        
        if validate:
            errors = validate_data(transformed)
            progress.update(task, advance=1)
            if errors:
                console.print(f"[yellow]⚠ {len(errors)} validation errors[/yellow]")
        
        # Load
        save_data(transformed, output_dir)
        progress.update(task, advance=1)
    
    console.print("[bold green]✓ Pipeline completed[/bold green]")
```

### Interactive Configuration

```python
@app.command()
def configure():
    """Interactive configuration setup"""
    show_banner("Configuration")
    
    config = {
        "api_url": questionary.text(
            "API endpoint:",
            default="https://api.example.com"
        ).ask(),
        
        "format": questionary.select(
            "Default output format:",
            choices=["csv", "geojson", "parquet"]
        ).ask(),
        
        "cache": questionary.confirm(
            "Enable caching?",
            default=True
        ).ask()
    }
    
    # Display configuration
    table = Table(title="Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in config.items():
        table.add_row(key, str(value))
    
    console.print(table)
    
    if questionary.confirm("Save configuration?").ask():
        save_config(config)
        console.print("[green]✓ Configuration saved[/green]")
```

### Batch Processing with Feedback

```python
@app.command()
def batch(
    pattern: str = typer.Argument(..., help="File pattern (e.g., '*.csv')"),
    operation: str = typer.Option("validate", help="Operation to perform")
):
    """Process multiple files with detailed feedback"""
    files = list(Path(".").glob(pattern))
    
    if not files:
        console.print(f"[yellow]No files matching '{pattern}'[/yellow]")
        raise typer.Exit(1)
    
    console.print(f"Found {len(files)} files")
    
    results = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing", total=len(files))
        
        for file in files:
            try:
                result = process_file(file, operation)
                results.append(("✓", file.name, result))
            except Exception as e:
                results.append(("✗", file.name, str(e)))
            progress.update(task, advance=1)
    
    # Summary table
    table = Table(title="Results")
    table.add_column("Status", justify="center")
    table.add_column("File", style="cyan")
    table.add_column("Result")
    
    for status, name, result in results:
        style = "green" if status == "✓" else "red"
        table.add_row(f"[{style}]{status}[/{style}]", name, result)
    
    console.print(table)
```

## Key Principles

1. **Progressive verbosity**: Use banners/formatting only when useful. Support `--verbose`/`--quiet` flags.
2. **Clear feedback**: Always show progress for operations >2 seconds. Use colors consistently.
3. **Fail gracefully**: Validate inputs early. Show actionable error messages with suggestions.
4. **Scriptable**: Support non-interactive mode with all flags. Output machine-readable formats on request.
5. **Reproducible**: Log commands with full parameters. Support config files for repeated workflows.

## Advanced Patterns

For complex scenarios (multi-command apps, context state, custom styling, testing), see `references/advanced_patterns.md`.

Common advanced needs:
- Subcommands and command groups
- Shared state across commands
- Custom questionary styling
- Configuration file management
- Progress for streaming data
- CLI testing with CliRunner

## Template Usage

The `assets/cli_template.py` provides a working example demonstrating all four components. Copy and adapt:

```bash
cp assets/cli_template.py my_tool.py
chmod +x my_tool.py
./my_tool.py --help
```

Modify the commands, add your logic, keep the UX patterns.

## Source

Based on the approach shared by Gaël PENESSOT: [LinkedIn post](https://www.linkedin.com/posts/gael-penessot_la-prochaine-fois-que-tu-lances-ton-script-activity-7410212824226058240-WMDh/)
