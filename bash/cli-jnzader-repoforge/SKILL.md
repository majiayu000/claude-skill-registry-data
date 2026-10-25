---
name: add-cli-options
description: >
  This skill covers the creation of shared options for CLI commands.
  Trigger: When defining command-line interfaces using the `click` library.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
---

## Critical Patterns

### Define Main Command

Use the `main` function to set up the entry point for your CLI application.

```python
import click
from repoforge.cli import main

@main.command()
def my_command():
    click.echo("This is my command.")
```

### Add Skills

Utilize the `skills` export to define reusable command options.

```python
import click
from repoforge.cli import skills

@skills.option('--verbose', is_flag=True, help='Enable verbose output.')
def my_command(verbose):
    if verbose:
        click.echo("Verbose mode is on.")
```

## When to Use

- When creating a new command for the CLI.
- To add common options across multiple commands.
- To streamline the execution of default commands.

## Commands

```bash
python repoforge/cli.py my_command
```

## Anti-Patterns

### Don't: Hardcode Options

Hardcoding options reduces flexibility and reusability across commands.

```python
# BAD
@click.command()
@click.option('--option', default='value', help='Hardcoded option.')
def my_command(option):
    click.echo(option)
```

## Quick Reference

| Task                | Pattern                |
|---------------------|------------------------|
| Define a command    | `@main.command()`      |
| Add shared options   | `@skills.option()`     |