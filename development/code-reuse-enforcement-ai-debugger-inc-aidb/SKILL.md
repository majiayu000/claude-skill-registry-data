---
name: code-reuse-enforcement
description: 'CRITICAL guardrail for preventing code duplication and magic strings
  in the AIDB codebase.

  Enforces discovery of existing constants, enums, and utilities BEFORE writing new
  code.

  '
version: 1.0.0
tags:
  - code-quality
  - constants
  - enums
  - utilities
  - dry
  - guardrails
---

# Code Reuse Enforcement

**CRITICAL GUARDRAIL:** Discover existing code BEFORE writing new code.

## Why This Matters

- Magic strings scatter across 50 files instead of 1 constant
- Duplicate utilities create maintenance nightmares
- Inconsistent values break features silently

______________________________________________________________________

## The Discovery-First Workflow

**BEFORE writing ANY code with literals or utilities:**

1. **Check Constants** - URLs, paths, timeouts, limits, env var names
1. **Check Enums** - States, statuses, types, actions
1. **Check Utilities** - Path ops, env reading, file ops, validation

**Quick Reference:** [discovery-catalog.md](resources/discovery-catalog.md)

______________________________________________________________________

## Common Violations

### Magic Strings

```python
# ❌ BAD
url = "https://ai-debugger.com/support"
log_dir = ".aidb/log"
debug = os.getenv("AIDB_LOG_LEVEL", "INFO")

# ✅ GOOD
from aidb_common.constants import AIDB_BASE_URL
from aidb_common.path import get_aidb_log_dir
from aidb_logging.utils import get_log_level

url = f"{AIDB_BASE_URL}/support"
log_dir = get_aidb_log_dir()
log_level = get_log_level(default="INFO")
```

### Magic Numbers

```python
# ❌ BAD
await asyncio.sleep(0.1)
timeout = 5.0

# ✅ GOOD
from aidb.common.constants import EVENT_POLL_TIMEOUT_S, CONNECTION_TIMEOUT_S

await asyncio.sleep(EVENT_POLL_TIMEOUT_S)
timeout = CONNECTION_TIMEOUT_S
```

### Reimplementing Utilities

```python
# ❌ BAD
def get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    return value.lower() in ("true", "1", "yes") if value else default

# ✅ GOOD
from aidb_common.env import read_bool
result = read_bool("AIDB_TRACE", default=False)
```

### String States

```python
# ❌ BAD
if session_state == "running":
    pass

# ✅ GOOD
from aidb_mcp.core.constants import SessionState
if session_state == SessionState.RUNNING:
    pass
```

______________________________________________________________________

## Quick Discovery

### Constants Files (8 total)

| Location                       | Contents                           |
| ------------------------------ | ---------------------------------- |
| `aidb_common/constants.py`     | Language enum, paths, domains      |
| `aidb/dap/client/constants.py` | DAP events, commands, stop reasons |
| `aidb/common/constants.py`     | Timeouts (seconds), defaults       |
| `aidb_mcp/core/constants.py`   | MCP tool names, actions            |
| `aidb_cli/core/constants.py`   | Icons, exit codes, Docker          |
| `tests/_helpers/constants.py`  | Test ports, timeouts, patterns     |

### Utility Packages

| Need       | Package                    |
| ---------- | -------------------------- |
| JSON       | `aidb_common.io`           |
| YAML       | `aidb_cli.core.yaml` (CLI) |
| Paths      | `aidb_common.path`         |
| Env vars   | `aidb_common.env`          |
| Validation | `aidb_common.validation`   |

**Full reference:** See docstrings in `src/aidb_common/`

### Search Commands

```bash
grep -r "value_to_find" src --include="*.py"
find src -name "constants.py"
grep -r "class.*Enum" src --include="*.py" -l
```

______________________________________________________________________

## When to Create NEW Constants

Only when:

1. **Truly new concept** - Not covered by existing constants
1. **Used 2+ times** - Will be reused
1. **Proper location** - Adding to the RIGHT constants file
1. **Following patterns** - Matches existing naming conventions

______________________________________________________________________

## Enforcement Checklist

Before committing:

- [ ] No hardcoded URLs (use aidb_common constants)
- [ ] No hardcoded paths (use path utilities)
- [ ] No magic numbers for timeouts (use api/constants.py)
- [ ] No string literals for states (use enums)
- [ ] No reimplemented utilities (check aidb_common)
- [ ] No manual env var parsing (use aidb_common.env)

______________________________________________________________________

## Resources

- **[Discovery Catalog](resources/discovery-catalog.md)** - Complete constants, enums, utilities reference
- **`src/aidb_common/`** - Source code with detailed docstrings
