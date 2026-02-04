---
name: click-patterns
description: Click framework examples and templates - decorators, nested commands, parameter validation. Use when building Python CLI with Click, implementing command groups, adding CLI options/arguments, validating CLI parameters, creating nested subcommands, or when user mentions Click framework, @click decorators, command-line interface.
allowed-tools: Read, Write, Bash
---

# Click Framework Patterns

This skill provides comprehensive Click framework patterns, templates, and examples for building production-ready Python CLIs.

## Instructions

### When Building a Click CLI

1. Read the appropriate template based on complexity:
   - Simple CLI: `templates/basic-cli.py`
   - Nested commands: `templates/nested-commands.py`
   - Custom validators: `templates/validators.py`

2. Generate new Click project:
   ```bash
   bash scripts/generate-click-cli.sh <project-name> <cli-type>
   ```
   Where cli-type is: basic, nested, or advanced

3. Study complete examples:
   - `examples/complete-example.md` - Full-featured CLI
   - `examples/patterns.md` - Common patterns and best practices

4. Validate your Click setup:
   ```bash
   bash scripts/validate-click.sh <cli-file.py>
   ```

### Core Click Patterns

**Command Groups:**
```python
@click.group()
def cli():
    """Main CLI entry point"""
    pass

@cli.command()
def subcommand():
    """A subcommand"""
    pass
```

**Options and Arguments:**
```python
@click.option('--template', '-t', default='basic', help='Template name')
@click.argument('environment')
def deploy(template, environment):
    pass
```

**Nested Groups:**
```python
@cli.group()
def config():
    """Configuration management"""
    pass

@config.command()
def get():
    """Get config value"""
    pass
```

**Parameter Validation:**
```python
@click.option('--mode', type=click.Choice(['fast', 'safe', 'rollback']))
@click.option('--count', type=click.IntRange(1, 100))
def command(mode, count):
    pass
```

### Available Templates

1. **basic-cli.py** - Simple single-command CLI
2. **nested-commands.py** - Command groups and subcommands
3. **validators.py** - Custom parameter validators
4. **advanced-cli.py** - Advanced patterns with plugins and chaining

### Available Scripts

1. **generate-click-cli.sh** - Creates Click project structure
2. **validate-click.sh** - Validates Click CLI implementation
3. **setup-click-project.sh** - Setup dependencies and environment

### Available Examples

1. **complete-example.md** - Production-ready Click CLI
2. **patterns.md** - Best practices and common patterns
3. **edge-cases.md** - Edge cases and solutions

## Requirements

- Python 3.8+
- Click 8.0+ (`pip install click`)
- Rich for colored output (`pip install rich`)

## Best Practices

1. **Use command groups** for organizing related commands
2. **Add help text** to all commands and options
3. **Validate parameters** using Click's built-in validators
4. **Use context** (@click.pass_context) for sharing state
5. **Handle errors gracefully** with try-except blocks
6. **Add version info** with @click.version_option()
7. **Use Rich** for beautiful colored output

## Common Use Cases

- Building CLI tools with multiple commands
- Creating deployment scripts with options
- Implementing configuration management CLIs
- Building database migration tools
- Creating API testing CLIs
- Implementing project scaffolding tools

---

**Purpose:** Provide Click framework templates and patterns for Python CLI development
**Load when:** Building Click CLIs, implementing command groups, or validating CLI parameters
