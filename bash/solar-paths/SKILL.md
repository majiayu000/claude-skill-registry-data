---
name: solar-paths
description: >
  Where everything lives: workspace and framework discovery, runtime state
  directories, the OS app-data location and the installation secret store.
  The base every other Solar skill imports. Use when a script or a provider
  needs to resolve SOLAR_WORKSPACE, SOLAR_ROOT, a runtime directory or a
  secret — never to start, sync or install anything, which is `solar-client`.
---

# Solar Paths

The bottom of the stack. Nothing here depends on another skill, and everything
else depends on this: ten of the other thirteen skills resolve their paths
through it.

It was split out of `solar-client` on 2026-09-21. That package was both the
base everyone imported and the CLI that installs and starts the rest, so every
dependency cycle in the framework ran through it. The four resolvers never had
dependencies of their own — only the folder did.

## What lives here

| File | Answers |
|---|---|
| `resolve_solar_paths.sh` | Bash: where is the workspace, where is the framework (`solar_resolve_paths`) |
| `solar_paths.py` | The same discovery for Python (`resolve_solar_paths()`) |
| `solar_runtime.py` | Runtime state directories: `runtime_root()`, `runtime_dir(...)`, `planet_state_dir(...)` |
| `solar_runtime_paths.sh` | The same, for Bash (`solar_runtime_dir`) |
| `solar_secrets.sh` / `solar_secrets.py` | The installation secret store, 0600, outside every tree an IDE indexes |
| `host_platform/paths.py` | The OS app-data directory (`app_data_dir`, `host_global_dir`) |

## How to use it

From Bash, two directories up and back down:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../../solar-paths/scripts/resolve_solar_paths.sh
source "$SCRIPT_DIR/../../solar-paths/scripts/resolve_solar_paths.sh"
solar_resolve_paths --quiet
```

From Python, put the directory on `sys.path` before importing:

```python
_PATHS_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "solar-paths" / "scripts"
if str(_PATHS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_PATHS_SCRIPTS))

import solar_runtime  # noqa: E402
from solar_paths import resolve_solar_paths  # noqa: E402
```

## The rule that keeps it a base

**Nothing in this skill may import another skill.** A dependency added here
comes back as a cycle through every caller. If a resolver seems to need
something from `solar-app`, `solar-client` or the router, the thing it needs is
either a path (and belongs here) or it is not a path (and the caller passes it
in). `host_platform` moved here for exactly that reason.

## Required MCP

None

## Tests

```bash
bash core/tests/skills/solar-paths/test_resolve_solar_paths.sh
bash core/tests/skills/solar-paths/test_solar_paths_py.sh
uv run --project core/tests pytest core/tests/skills/solar-paths -q
```
