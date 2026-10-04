---
name: rule-api-cli
description: MANDATORY when editing files matching ["api/src/cli/**/*.py"]. When working on Flask CLI commands in api/src/cli/
---

# API CLI Rules

## Module Layout

ALWAYS place each CLI command group in its own module under `api/src/cli/` (one file per group). ALWAYS define the group via `@click.group()` and register it centrally in `api/src/cli/__init__.py` through `app.cli.add_command()`. NEVER scatter inline command registrations across the codebase.

Correct:
```python
# api/src/cli/user_commands.py
"""User management CLI commands."""
import click

@click.group()
def user() -> None:
    """User management operations."""

@user.command()
@click.option("--user-id", type=click.UUID, required=True, help="Target user ID")
def create(user_id):
    """Create a new user."""
```

Incorrect:
```python
# api/src/cli/all_commands.py — unrelated groups crammed together
@click.command()
def create_user(): ...
@click.command()
def submit_application(): ...
```

## Argument Parsing

ALWAYS use Click decorators (`@click.argument`, `@click.option`) with explicit `type=` (`click.UUID`, `click.INT`, `click.Choice(...)`) and `help=` text. ALWAYS mark required options with `required=True`. NEVER parse `sys.argv` directly. NEVER validate inside service code what should be validated at the CLI boundary — raise `click.BadParameter()` for invalid input.

## Output and Verbosity

ALWAYS use `click.echo()` / `click.secho()` (NEVER `print()`). ALWAYS send error output to stderr via `err=True`. ALWAYS provide a `--verbose/-v` flag on commands that have optional detail output. Use green for success, red for error.

Correct:
```python
click.secho("Migration complete", fg="green")
click.secho(f"ERROR: {e}", fg="red", err=True)
```

## Error Handling and Exit Codes

ALWAYS translate expected errors to Click exceptions: `click.UsageError`, `click.BadParameter`, or `click.ClickException`. NEVER call `sys.exit()` with arbitrary codes — let Click manage exit codes (0 success, 1 application error, 2 usage error). NEVER print stack traces to users; log them with `logger.exception(...)` and raise a clean `ClickException`.

## DB Sessions and Transactions

ALWAYS decorate CLI handlers that touch the database with `@flask_db.with_db_session()` and accept `db_session` as a parameter. ALWAYS wrap mutations in `with db_session.begin():`. NEVER open multiple sessions in one command. NEVER call `commit()` / `rollback()` manually.

Correct:
```python
@click.command()
@click.option("--user-id", type=click.UUID, required=True)
@flask_db.with_db_session()
def activate_user(user_id, db_session):
    """Activate a user account."""
    with db_session.begin():
        user = db_session.query(User).filter_by(id=user_id).first()
        if not user:
            raise click.ClickException(f"User {user_id} not found")
        user.is_active = True
```

## Structured Logging

ALWAYS use the Flask app logger with static messages and `extra={}` context. ALWAYS log command start and completion with duration. NEVER log PII, tokens, or credentials. See `api-logging.mdc` and `cross-domain.mdc`.

## Testing

ALWAYS test CLI commands with `click.testing.CliRunner`. ALWAYS mock service functions — do not hit the database from CLI unit tests. ALWAYS assert `result.exit_code` and `result.output`. NEVER test via subprocess.

```python
from click.testing import CliRunner
def test_migrate_success():
    runner = CliRunner()
    with patch("api.src.cli.migration_commands.run_migration") as m:
        m.return_value = {"migrated_tables": ["users"]}
        result = runner.invoke(migrate_database, ["--verbose"])
    assert result.exit_code == 0
```

## Concurrency

ALWAYS document concurrency expectations in the command docstring. Prefer idempotent operations. Use advisory locks (`SELECT ... FOR UPDATE`) for commands that mutate shared state serially.

---

## Related Rules

- **`api-routes.mdc`** — decorator ordering, thin handler pattern
- **`api-services.mdc`** — service function conventions CLI delegates to
- **`api-logging.mdc`** — structured logging conventions
- **`api-error-handling.mdc`** — error classification and messages
- **`cross-domain.mdc`** — logging, boolean naming, PII rules

## Specialist Validation

**Simple (flag tweak, help text):** No specialist needed.
**Moderate (new command, new group):** Invoke `codebase-conventions-reviewer`.
**Complex (new CLI registry, session wiring, transactional workflows):** Invoke `architecture-strategist` and `kieran-python-reviewer` in parallel.
