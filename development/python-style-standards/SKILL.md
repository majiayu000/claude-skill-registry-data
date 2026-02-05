---
name: Python Style Standards
description: Python coding standards including line length (80 chars), naming conventions (snake_case, PascalCase), type hints, docstrings, exception handling, and logging patterns. Use when writing new Python code or reviewing code quality.
allowed-tools: [Read, Bash]
---

# Python Style Standards

Practical Python coding standards focused on readability, maintainability, and quality.

## Line Length & Formatting

**80 characters maximum** (enforced)
- PEP 8 compliant
- Use `ruff format` for auto-formatting
- Check with `ruff check` and `pylint`

**Formatting Commands**:
```bash
# Auto-format first (ALWAYS run before committing)
ruff format . --config=/path/to/ruff.toml

# Check linting
ruff check . --config=/path/to/ruff.toml

# Additional quality checks
pylint --rcfile=/path/to/pylintrc.toml .

# Type checking
mypy --config-file=/path/to/mypy.ini .
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | `snake_case` | `process_scan_results()` |
| Variables | `snake_case` | `asset_count` |
| Modules | `snake_case` | `asset_processor.py` |
| Classes | `PascalCase` | `AssetProcessor` |
| Constants | `UPPER_CASE` | `DEFAULT_BATCH_SIZE` |

**Descriptive names over abbreviations**:
```python
# GOOD - obvious meaning
def get_asset_by_uuid(uuid: str) -> dict | None:
    return cache.lookup_and_parse('assets', 'uuid', uuid)

# BAD - cryptic abbreviations
def get_a(u: str) -> dict | None:
    return cache.lookup_and_parse('assets', 'uuid', u)
```

## Type Hints

**Required for all new code**
- Existing code can remain untyped unless refactoring
- Use mypy for type checking
- Modern Python 3.10+ union syntax preferred

**Examples**:
```python
# Function signatures
def process_scan(scan_id: int) -> dict[str, Any]:
    """Process a scan and return statistics."""
    return {'processed': scan_id}

# Optional values (use | None, not Optional)
def get_asset_id(dv: dict) -> str | None:
    assets = dv.get('related', {}).get('assets', [])
    return str(assets[0]) if assets else None

# Complex types
def batch_process(
    records: list[dict[str, Any]]
) -> tuple[int, dict[str, int]]:
    """Process records and return count and stats."""
    return len(records), {'processed': len(records)}
```

## Docstrings

**Required for**:
- Classes (purpose, key attributes)
- Modules (overview, main components)
- Complex functions (non-obvious logic)

**Skip for**:
- Simple getters/setters
- Obvious utility functions
- Functions with clear type hints

**Style**: PEP 8 conventions, explain WHY not WHAT

```python
# GOOD - explains non-obvious WHY
def skip_compliance_insert(self, severity: str) -> bool:
    """Skip inserting Pass/Info compliance records.

    WHY: Pass = compliant, no vulnerability exists.
    Creating DVs for passing checks pollutes the database.
    """
    return severity in ['0', 'Pass', 'Info']

# BAD - verbose restating of obvious code
def get_asset_id(self, dv: dict) -> str | None:
    """Retrieves the asset ID from a detected vulnerability document.

    Args:
        dv: The detected vulnerability document

    Returns:
        The asset ID as a string, or None if not found
    """
    assets = dv.get('related', {}).get('assets', [])
    return str(assets[0]) if assets else None

# GOOD - type hints make it obvious, no docstring needed
def get_asset_id(self, dv: dict) -> str | None:
    assets = dv.get('related', {}).get('assets', [])
    return str(assets[0]) if assets else None
```

## Exception Handling

**ONLY use try/except for connection errors**

```python
# BAD - unnecessary try/except (dict.get never raises)
def get_severity(record: dict) -> str:
    try:
        return record.get('severity', '0')
    except Exception:
        return '0'

# GOOD - direct access (safe operations don't need wrapping)
def get_severity(record: dict) -> str:
    return record.get('severity', '0')

# GOOD - try/except for connection errors only
def fetch_from_api(url: str) -> dict:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        LOG.warning(f"Timeout fetching {url}, retrying...")
        return fetch_from_api(url)  # Retry on timeout
    except requests.HTTPError as e:
        LOG.error(f"HTTP error {e.response.status_code}: {url}")
        raise
    except requests.ConnectionError as e:
        LOG.error(f"Connection error: {url}")
        raise
```

**When to use try/except** (ONLY connection errors):
- Network calls (requests, httpx, aiohttp)
- Database connections (pymongo, psycopg2, sqlalchemy)
- External API calls (any network I/O)
- Cache connections (redis, memcached)

**When NOT to use try/except**:
- dict.get() operations (returns None safely)
- list/dict access with defaults
- File I/O (let it fail with clear error)
- JSON parsing (let it fail with clear error)
- Type conversions (validate first, let it fail if invalid)
- Safe standard library operations

**Specific exceptions only** (never bare except):
```python
# GOOD - specific connection exceptions
try:
    result = api_call()
except requests.Timeout:
    handle_timeout()
except requests.HTTPError:
    handle_http_error()
except requests.ConnectionError:
    handle_connection_error()

# BAD - bare except masks bugs
try:
    result = api_call()
except:
    pass
```

## Logging Standards

**Setup** (once per class/module):
```python
import logging

# At module level (preferred)
LOG = logging.getLogger(__name__)

# In class (if needed)
class AssetProcessor:
    def __init__(self, config, sub_id):
        self.log = logging.getLogger(__name__)
```

**Logging Levels**:
- `LOG.debug()` - Detailed/verbose information (IDs, intermediate values)
- `LOG.info()` - Operation status and progress (milestones, counts)
- `LOG.warning()` - Recoverable issues (missing optional data)
- `LOG.error()` - Failures requiring attention (critical errors)

**Best Practices**:
```python
# Include context: IDs, counts, operation names
self.log.debug(f"Processing record {record_id}")
self.log.info(f"Processed batch of {count} records in {elapsed:.2f}s")

# Progress indicators for long operations
self.log.info(f"Processing {i}/{total} ({i/total*100:.1f}%)")

# Include "Started" messages for operations
self.log.info("Started asset cascade matching")
```

## Function Design

**Don't create pointless wrappers**:
```python
# BAD - wrapper adds no value
def get_severity(self, record: dict) -> str:
    return record.get('severity')

# GOOD - just use directly
severity = record.get('severity')

# GOOD - wrapper adds value (validation, transformation)
def get_normalized_severity(self, record: dict) -> int:
    """Convert severity string to integer with validation."""
    raw_severity = record.get('severity', '0')
    return int(raw_severity) if raw_severity.isdigit() else 0
```

**Function should add value**:
- Validation (check inputs, enforce constraints)
- Transformation (convert formats, normalize data)
- Abstraction (hide complexity, provide clear interface)
- Combination (coordinate multiple operations)

**No single-line functions** - readability over brevity

**Single responsibility principle** - each function does one thing well

## Constants

**Organization**:
```python
# Large projects: constants.py for shared values
DEFAULT_BATCH_SIZE = 5000
MAX_WORKERS = 10
TIMEOUT_SECONDS = 30

# Single-file usage: class-level constants
class AssetProcessor:
    BATCH_SIZE = 5000
    MAX_RETRIES = 3
```

**Naming with WHY comments**:
```python
# GOOD - explains the reason for the value
FLOWS_BATCH_SIZE = 5000  # Balance memory usage with DB efficiency
DAA_THRESHOLD = 20000    # Parallel creation at scale
```

## Import Organization

**All imports at top of file** (except circular import fixes)

**Grouped in order**:
1. Standard library
2. Third-party packages
3. Local/project imports

**Use absolute imports from project root**:
```python
# Standard library
import logging
import os
from typing import Any

# Third-party
import pymongo
import redis
from bson import ObjectId

# Local (absolute from project root)
from fisio.common.log import setup_logger
from fisio.common.mongo_helpers import retry_run
from fisio.imports.tenable_sc_refactor.processors import AssetProcessor
```

## Code Organization

**File structure**:
```python
# 1. Module docstring (if needed)
"""Asset processing for Tenable SC imports."""

# 2. Imports (grouped)
import logging
from typing import Any

# 3. Constants (module-level)
DEFAULT_BATCH_SIZE = 5000

# 4. Helper functions (above their callers)
def validate_asset_data(data: dict) -> bool:
    return 'uuid' in data

# 5. Classes
class AssetProcessor:
    pass

# 6. Main function (at bottom)
def run(config: dict, sub_id: str) -> dict:
    pass
```

**Helper functions above their callers** - top-down reading flow

## Refactoring Complex Functions

**When to refactor**:
- Function exceeds 50 statements or 12 branches
- Multiple distinct responsibilities mixed together
- Deep nesting (>3 levels) makes logic hard to follow
- Ruff/pylint complexity warnings

**How to refactor**:
- Extract focused methods with single responsibilities
- Main function becomes clear orchestration
- Each helper method handles one concern
- Use guard clauses to reduce nesting

```python
# BEFORE - 100+ lines with deep nesting
def process_record(self, record: dict) -> dict | None:
    if record.get('type') == 'asset':
        if record.get('uuid'):
            if self._validate_uuid(record['uuid']):
                asset = self._create_asset(record)
                if asset:
                    self._stage_relationships(asset, record)
                    return asset
    return None

# AFTER - clear orchestration + focused helpers
def process_record(self, record: dict) -> dict | None:
    """Process a single record and return created asset."""
    if not self._should_process_record(record):
        return None

    asset = self._create_asset_from_record(record)
    if asset:
        self._stage_relationships(asset, record)

    return asset

def _should_process_record(self, record: dict) -> bool:
    """Check if record should be processed."""
    if record.get('type') != 'asset':
        return False
    if not record.get('uuid'):
        return False
    return self._validate_uuid(record['uuid'])
```

## Common Anti-Patterns to Avoid

**Avoid**:
- Bare `except:` clauses (use specific exceptions)
- Try/except for operations that never raise
- Single-character variable names (except i, j in short loops)
- Functions that just call another function unchanged
- Magic numbers without explanation
- Commented-out code (delete it, use git history)
- Global mutable state
- Deep nesting (use guard clauses)

## Quick Reference Card

```python
# Names
function_name()    # snake_case
ClassName         # PascalCase
CONSTANT_VALUE    # UPPER_CASE

# Type hints (required for new code)
def process(data: dict[str, Any]) -> int | None:
    pass

# Docstrings (when non-obvious)
def complex_logic() -> bool:
    """Explain WHY, not WHAT."""
    pass

# Logging (include context)
LOG.debug(f"Processing record {record_id}")
LOG.info(f"Completed batch of {count} records")

# Exception handling (only when necessary)
try:
    api_call()  # Operations that can actually fail
except SpecificError:
    handle_error()  # Never bare except

# Imports (grouped: stdlib → third-party → local)
import os
import pymongo
from fisio.common import helpers
```

## Tools and Commands

**Format before committing**:
```bash
# Step 1: Auto-format (fixes most issues)
ruff format .

# Step 2: Check for remaining issues
ruff check .

# Step 3: Additional quality checks (if configured)
pylint .
mypy .
```

**Project-specific configs** (check for these):
- `ruff.toml` or `pyproject.toml`
- `pylintrc.toml` or `.pylintrc`
- `mypy.ini` or `pyproject.toml`

**Fallback configs** (if project lacks them):
- `~/.claude/configs/ruff.toml`
- `~/.claude/configs/pylintrc.toml`
- `~/.claude/configs/mypy.ini`

## Remember

**Priorities**:
1. **Clarity** - Code should be obvious to read
2. **Maintainability** - Easy to modify without breaking
3. **Quality** - Pass linting and tests before claiming done
4. **Simplicity** - Simple solutions over clever ones

**When in doubt**:
- Check existing code patterns in the project
- Ask for clarification rather than guess
- Err on the side of being more descriptive
- Let type hints and clear names replace documentation
