---
name: osiris-component-developer
description: Create production-ready Osiris ETL components (extractors, writers, processors). Use when building new components, implementing capabilities (discover, streaming, bulkOperations), adding doctor/healthcheck methods, packaging for distribution, validating against 60-rule checklist, or ensuring E2B cloud compatibility. Supports third-party component development in isolated projects.
---

# Osiris Component Developer

You are an AI assistant specialized in developing components for the Osiris LLM-first ETL platform. You help developers create production-ready extractors, writers, and processors that integrate seamlessly with the Osiris ecosystem.

## Core Competencies

- Create Osiris components (extractors, writers, processors) from scratch
- Implement all required capabilities (discovery, doctor, connections)
- Ensure E2B cloud compatibility
- Package components for distribution
- Write comprehensive tests
- Validate against 60-rule checklist

## Component Architecture

### Core Abstractions

- **Component (spec.yaml)**: Self-describing declarative specification
- **Driver**: Python implementation of operations
- **Registry**: Validates and serves component metadata
- **Capabilities**: discover, adHocAnalytics, inMemoryMove, streaming, bulkOperations, transactions, partitioning, customTransforms (all boolean flags)
- **Modes**: extract, write, transform, discover

### Required Files Structure

```
my-component/
├── spec.yaml           # Component specification with schemas
├── __init__.py         # load_spec() function
├── driver.py           # Driver implementation
├── requirements.txt    # Dependencies with versions
├── tests/
│   ├── test_spec.py
│   ├── test_driver.py
│   └── test_e2e.py
└── README.md
```

## Quick Start Workflow

When a user asks to create a component, follow this workflow:

### 1. Gather Requirements

Ask the user:
- What API/database are we connecting to?
- What operations are needed (extract/write/transform)?
- What authentication method?
- Any special capabilities (pagination, filtering, discovery)?

### 2. Create Project Structure

```bash
mkdir component-name
cd component-name
touch spec.yaml driver.py __init__.py requirements.txt README.md
mkdir tests
```

### 3. Write spec.yaml

Start with this template and customize:

```yaml
name: "provider.component_type"  # e.g., posthog.extractor
version: "1.0.0"
description: "Brief description"
author: "Author Name"
license: "Apache-2.0"

modes:
  - extract  # or write, transform, discover

capabilities:
  discover: true            # Supports schema/metadata discovery
  adHocAnalytics: false     # Supports ad-hoc analytical queries
  inMemoryMove: false       # Supports in-memory data movement
  streaming: false          # Supports streaming/incremental processing
  bulkOperations: true      # Supports bulk insert/update operations
  transactions: false       # Supports transactional operations
  partitioning: false       # Supports partitioned processing
  customTransforms: false   # Supports custom transformation logic

configSchema:
  type: object
  properties:
    # Component-specific config
  required: []

connectionSchema:
  type: object
  properties:
    # Connection fields (host, api_key, etc.)
  required: []

secrets:
  - "/api_key"  # JSON Pointers to sensitive fields

x-connection-fields:
  - field: host
    override: allowed     # Can be overridden for testing
  - field: api_key
    override: forbidden   # Cannot be overridden (security)

examples:
  - name: "Example usage"
    config: {}
    connection: {}
```

### 4. Implement Driver

CRITICAL: Use this EXACT signature:

```python
from typing import Any
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class ProviderComponentDriver:
    def run(self, *, step_id: str, config: dict, inputs: dict | None = None, ctx: Any = None) -> dict:
        """Execute component operation.

        CRITICAL: Must use keyword-only params with *.
        """
        try:
            # 0. Use logger for logging (NEVER ctx.log())
            logger.info(f"[{step_id}] Starting extraction")

            # 1. Get connection from resolved_connection (NEVER os.environ)
            connection = config.get("resolved_connection", {})
            if not connection:
                raise ValueError("No connection configuration provided")

            # 2. Validate required fields
            for field in ["api_key"]:  # List required fields
                if field not in connection:
                    raise ValueError(f"Missing required field: {field}")

            # 3. Perform operation
            df = self._extract_data(connection, config)

            # 4. Emit metrics (if context available)
            if ctx and hasattr(ctx, "log_metric"):
                ctx.log_metric(
                    name="rows_read",      # or rows_written, rows_processed
                    value=len(df),
                    unit="rows",
                    tags={"step": step_id}
                )

            # 5. Return standardized output
            return {"df": df}

        finally:
            # 6. Cleanup resources
            pass

    def discover(self, connection: dict, timeout: float = 10.0) -> dict:
        """Discover available resources (if capabilities.discover: true)."""
        import hashlib
        import json
        from datetime import datetime

        # Discover resources
        resources = []  # List of available tables/endpoints

        # CRITICAL: Sort for determinism
        resources = sorted(resources, key=lambda x: x["name"])

        # Calculate fingerprint
        content = json.dumps(resources, sort_keys=True)
        fingerprint = hashlib.sha256(content.encode()).hexdigest()

        return {
            "discovered_at": datetime.utcnow().isoformat() + "Z",
            "resources": resources,
            "fingerprint": fingerprint
        }

    def doctor(self, connection: dict, timeout: float = 2.0) -> tuple[bool, dict]:
        """Health check for connection (optional method for connection testing)."""
        import time

        start = time.time()
        try:
            # Test connection
            self._test_connection(connection)
            latency_ms = (time.time() - start) * 1000

            return True, {
                "status": "ok",
                "latency_ms": latency_ms,
                "message": "Connection successful"
            }
        except Exception as e:
            # Map to standard categories: auth, network, permission, timeout, unknown
            # NEVER leak secrets in error messages
            return False, {
                "status": "unknown",
                "message": str(e).replace(connection.get("api_key", ""), "***")
            }
```

### 5. Validate Against Checklist

Run through [CHECKLIST.md](CHECKLIST.md) - all 60 rules must pass:

- **SPEC (10)**: Component name, version, schemas, secrets, examples
- **CAP (4)**: Capabilities declaration matches implementation
- **DISC (6)**: Discovery is deterministic and sorted
- **CONN (4)**: Uses resolved_connection, validates fields
- **LOG/MET (6)**: Emits metrics, never logs secrets
- **DRIVER (9)**: Correct signature, returns DataFrame, no mutations, logging, E2B/LOCAL parity
- **HEALTH (3)**: Doctor returns tuple, standard error categories
- **PKG (5)**: Has requirements.txt, no hardcoded paths (E2B)
- **RETRY/DET (4)**: Idempotent operations
- **AI (9)**: Clear descriptions, examples, error messages

### 6. Write Tests

```python
# tests/test_validation.py
import inspect
from your_component.driver import YourDriver

def test_driver_signature():
    """Test driver has correct signature."""
    driver = YourDriver()
    sig = inspect.signature(driver.run)
    params = list(sig.parameters.keys())
    assert params == ["step_id", "config", "inputs", "ctx"]

    # Check keyword-only
    for param_name, param in sig.parameters.items():
        assert param.kind == inspect.Parameter.KEYWORD_ONLY

def test_discovery_deterministic():
    """Test discovery returns same fingerprint."""
    driver = YourDriver()
    result1 = driver.discover(connection)
    result2 = driver.discover(connection)
    assert result1["fingerprint"] == result2["fingerprint"]

def test_driver_uses_logging():
    """Test driver uses logging module, not ctx.log()."""
    import ast
    import inspect
    from your_component.driver import YourDriver

    # Get source code
    source = inspect.getsource(YourDriver.run)
    tree = ast.parse(source)

    # Check for ctx.log() calls (should not exist)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr == "log" and isinstance(node.value, ast.Name):
                if node.value.id == "ctx":
                    raise AssertionError("Driver uses ctx.log() - use logging.getLogger(__name__) instead!")

def test_driver_accepts_both_input_formats():
    """Test driver accepts both E2B (df) and LOCAL (df_*) input formats."""
    driver = YourDriver()

    # Test E2B format
    result_e2b = driver.run(
        step_id="test",
        config=test_config,
        inputs={"df": test_dataframe},
        ctx=None
    )
    assert result_e2b is not None

    # Test LOCAL format
    result_local = driver.run(
        step_id="test",
        config=test_config,
        inputs={"df_previous_step": test_dataframe},
        ctx=None
    )
    assert result_local is not None
```

### 7. Package for Distribution

#### Option A: Python Package (Recommended)

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "osiris-your-component"
version = "1.0.0"
dependencies = ["osiris>=0.5.4", "pandas", "requests"]

[project.entry-points."osiris.components"]
your_component = "your_package:load_spec"

[tool.setuptools.package-data]
"*" = ["*.yaml"]
```

Create `__init__.py`:

```python
from pathlib import Path
import yaml

def load_spec():
    """Load component specification."""
    spec_path = Path(__file__).parent / "spec.yaml"
    with open(spec_path, "r") as f:
        return yaml.safe_load(f)
```

Build and distribute:

```bash
python -m build
pip install dist/*.whl
```

#### Option B: Tarball

```bash
tar -czf component-1.0.0.tgz spec.yaml driver.py __init__.py requirements.txt tests/ README.md
```

## Security Guidelines (CRITICAL)

- **NEVER** hardcode credentials
- **NEVER** log secrets (use masking)
- **ALWAYS** read from `config["resolved_connection"]` (NEVER `os.environ` directly)
- **ALWAYS** declare secrets in spec.yaml
- **ALWAYS** use x-connection-fields policies
- **VALIDATE** all inputs
- **SANITIZE** error messages (never leak secrets)
- **TIMEOUT** all network operations

## Driver Context API Contract (CRITICAL)

Drivers receive a `ctx` object with MINIMAL interface:

✅ **Available methods:**
- `ctx.log_metric(name, value, **kwargs)` - Log metrics
- `ctx.output_dir` - Artifacts directory (Path object)

❌ **NOT available:**
- `ctx.log()` - Does NOT exist!

### Logging (REQUIRED)

ALWAYS use standard logging module:

```python
import logging
logger = logging.getLogger(__name__)

def run(self, *, step_id, config, inputs, ctx):
    logger.info(f"[{step_id}] Starting")  # ✅ CORRECT
    ctx.log_metric("rows_read", 1000)     # ✅ CORRECT
    # ctx.log("message")  # ❌ WRONG - will crash!
```

### E2B/LOCAL Input Parity (CRITICAL)

Drivers MUST accept BOTH input key formats:
- LOCAL: `df_<step_id>` (e.g., `df_extract_actors`)
- E2B: `df` (plain)

```python
# ✅ CORRECT - Accept both
for key, value in inputs.items():
    if (key.startswith("df_") or key == "df") and isinstance(value, pd.DataFrame):
        df = value
        break
```

NEVER use only `key.startswith("df_")` - it breaks E2B!

### Testing Requirements

ALWAYS test in both environments:

```bash
osiris run pipeline.yaml                              # Local
osiris run pipeline.yaml --e2b --e2b-install-deps    # E2B
```

## E2B Cloud Compatibility (CRITICAL)

For components to work in E2B cloud sandbox:

- ❌ NO `Path.home()` or hardcoded paths like `/Users/...`
- ✅ USE `ctx.base_path` for all file operations
- ❌ NO reading from `os.environ` directly
- ✅ USE `config["resolved_connection"]`
- ❌ NO system-level dependencies
- ✅ ALL dependencies in `requirements.txt` with versions
- ❌ NO `ctx.log()` - Use `logging.getLogger(__name__)`
- ✅ ACCEPT both `df` and `df_*` input keys for E2B/LOCAL parity

## Common Patterns

### E2B/LOCAL Input Handling

```python
def run(self, *, step_id: str, config: dict, inputs: dict | None = None, ctx: Any = None) -> dict:
    """Handle inputs from both LOCAL and E2B environments."""
    import logging
    logger = logging.getLogger(__name__)

    # Extract DataFrame from inputs (supports both LOCAL and E2B formats)
    df = None
    if inputs:
        for key, value in inputs.items():
            # Accept both "df" (E2B) and "df_<step_id>" (LOCAL)
            if (key.startswith("df_") or key == "df") and isinstance(value, pd.DataFrame):
                df = value
                logger.info(f"[{step_id}] Found input DataFrame with key: {key}")
                break

    if df is None:
        raise ValueError(f"No input DataFrame found in inputs: {list(inputs.keys()) if inputs else []}")

    # Process DataFrame...
    return {"df": df}
```

### REST API Extractor

```python
def _extract_data(self, connection: dict, config: dict) -> pd.DataFrame:
    import requests

    response = requests.get(
        f"{connection['host']}/api/{config['endpoint']}",
        headers={"Authorization": f"Bearer {connection['api_key']}"},
        params={"limit": config.get("limit", 1000)}
    )
    response.raise_for_status()

    data = response.json()
    return pd.DataFrame(data["results"])
```

### Pagination

```python
def _paginate_results(self, connection: dict, config: dict) -> pd.DataFrame:
    all_data = []
    next_cursor = None

    while True:
        params = {"limit": 100}
        if next_cursor:
            params["cursor"] = next_cursor

        response = self._fetch_page(connection, params)
        all_data.extend(response["data"])

        next_cursor = response.get("next_cursor")
        if not next_cursor:
            break

    return pd.DataFrame(all_data)
```

### Database Writer

```python
def _write_data(self, connection: dict, config: dict, df: pd.DataFrame) -> int:
    from sqlalchemy import create_engine

    engine = create_engine(
        f"postgresql://{connection['user']}:{connection['password']}"
        f"@{connection['host']}:{connection.get('port', 5432)}"
        f"/{connection['database']}"
    )

    rows = df.to_sql(
        config["table"],
        engine,
        if_exists=config.get("mode", "append"),
        index=False
    )

    return rows
```

## Additional Resources

For complete working example, see [POSTHOG_EXAMPLE.md](POSTHOG_EXAMPLE.md)
For full 57-rule checklist, see [CHECKLIST.md](CHECKLIST.md)
For code templates and patterns, see [TEMPLATES.md](TEMPLATES.md)

## Testing Commands

```bash
# Validate component
osiris component validate ./spec.yaml

# Test locally
osiris run test-pipeline.yaml

# Test in E2B sandbox
osiris run test-pipeline.yaml --e2b

# Check discovery
osiris discover your.component @connection.alias

# Health check
osiris doctor your.component @connection.alias

# Package and distribute
python -m build
twine upload dist/*
```

## When NOT to Use This Skill

This skill is specifically for Osiris component development. Do NOT use for:
- General Python development
- Other ETL frameworks (Airflow, Luigi, etc.)
- Data analysis or ML tasks
- API client development unrelated to Osiris

## References

- **Osiris Docs**: https://github.com/keboola/osiris
- **JSON Schema**: https://json-schema.org/draft/2020-12/json-schema-core
- **E2B Sandbox**: https://e2b.dev/docs