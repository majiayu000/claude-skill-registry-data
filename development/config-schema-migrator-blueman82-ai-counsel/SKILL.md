---
name: "config-schema-migrator"
description: "Expert at evolving Pydantic configuration schemas with backward compatibility and automated migrations"
---

# Config Schema Migrator Skill

## When to Use This Skill

Activate this skill when you need to:
- Evolve Pydantic configuration schemas (add fields, change types, restructure sections)
- Maintain backward compatibility with existing config files
- Write migration scripts to automate config updates
- Implement environment variable substitution in config fields
- Add deprecation warnings for old config patterns
- Validate config schemas with field validators
- Create discriminated unions for config type discrimination

## Key Principles

1. **Backward Compatibility First**: Never break existing configs without a migration path
2. **Deprecation Before Removal**: Warn users before removing old config sections
3. **Automatic Migration**: Provide scripts to automate config updates (don't force manual editing)
4. **Type Safety**: Use Pydantic validators to catch config errors at load time
5. **Environment Variables**: Support ${VAR_NAME} substitution for secrets
6. **Clear Messaging**: Provide helpful error messages with migration instructions

## Pattern 1: Adding New Config Sections with Backward Compatibility

### Example: Adding `adapters` Section While Keeping `cli_tools`

**Problem**: You need to add a new config section (`adapters`) to replace an old one (`cli_tools`) without breaking existing configs.

**Solution Pattern** (from `models/config.py`):

```python
from typing import Optional
from pydantic import BaseModel
import warnings

class Config(BaseModel):
    """Root configuration model."""

    # New section (preferred)
    adapters: Optional[dict[str, AdapterConfig]] = None

    # Legacy section (deprecated)
    cli_tools: Optional[dict[str, CLIToolConfig]] = None

    def model_post_init(self, __context):
        """Post-initialization validation."""
        # Ensure at least one section exists
        if self.adapters is None and self.cli_tools is None:
            raise ValueError(
                "Configuration must include either 'adapters' or 'cli_tools' section"
            )

        # Emit deprecation warning for old section
        if self.cli_tools is not None and self.adapters is None:
            warnings.warn(
                "The 'cli_tools' configuration section is deprecated. "
                "Please migrate to 'adapters' section with explicit 'type' field. "
                "See migration guide: docs/migration/cli_tools_to_adapters.md",
                DeprecationWarning,
                stacklevel=2,
            )
```

**Key Techniques**:
- Use `Optional` for both old and new sections
- Validate in `model_post_init()` that at least one exists
- Emit `DeprecationWarning` when old section is used
- Reference migration documentation in warning message
- Allow both sections temporarily for gradual migration

## Pattern 2: Type Discrimination with Discriminated Unions

### Example: CLI vs HTTP Adapters

**Problem**: You have config objects that can be one of several types (CLI adapter, HTTP adapter, etc).

**Solution Pattern** (from `models/config.py`):

```python
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

class CLIAdapterConfig(BaseModel):
    """Configuration for CLI-based adapter."""
    type: Literal["cli"] = "cli"
    command: str
    args: list[str]
    timeout: int = 60

class HTTPAdapterConfig(BaseModel):
    """Configuration for HTTP-based adapter."""
    type: Literal["http"] = "http"
    base_url: str
    api_key: Optional[str] = None
    timeout: int = 60
    max_retries: int = 3

# Discriminated union - Pydantic uses 'type' field to determine which model
AdapterConfig = Annotated[
    Union[CLIAdapterConfig, HTTPAdapterConfig],
    Field(discriminator="type")
]
```

**YAML Usage**:
```yaml
adapters:
  claude:
    type: cli  # Discriminator field
    command: "claude"
    args: ["-p", "{prompt}"]
    timeout: 60

  ollama:
    type: http  # Different type triggers HTTPAdapterConfig
    base_url: "http://localhost:11434"
    timeout: 120
```

**Key Techniques**:
- Use `Literal["value"]` for discriminator field with default value
- Create `Annotated[Union[...], Field(discriminator="type")]`
- Pydantic automatically routes to correct model based on `type` field
- Each type has different required fields (validated automatically)

## Pattern 3: Environment Variable Substitution

### Example: API Keys and Secrets

**Problem**: You need to inject secrets from environment variables without hardcoding in YAML.

**Solution Pattern** (from `models/config.py`):

```python
import os
import re
from pydantic import BaseModel, field_validator

class HTTPAdapterConfig(BaseModel):
    """Configuration for HTTP-based adapter."""
    base_url: str
    api_key: Optional[str] = None

    @field_validator("api_key", "base_url")
    @classmethod
    def resolve_env_vars(cls, v: Optional[str], info) -> Optional[str]:
        """Resolve ${ENV_VAR} references in string fields."""
        if v is None:
            return v

        # Pattern: ${VAR_NAME}
        pattern = r"\$\{([^}]+)\}"
        is_api_key = info.field_name == "api_key"

        def replacer(match):
            env_var = match.group(1)
            value = os.getenv(env_var)
            if value is None:
                # For optional fields like api_key, use sentinel
                if is_api_key:
                    return "__MISSING_API_KEY__"
                # For required fields, raise error
                raise ValueError(
                    f"Environment variable '{env_var}' is not set. "
                    f"Required for configuration."
                )
            return value

        result = re.sub(pattern, replacer, v)

        # If api_key has sentinel marker, return None (graceful degradation)
        if is_api_key and "__MISSING_API_KEY__" in result:
            return None

        return result
```

**YAML Usage**:
```yaml
adapters:
  openrouter:
    type: http
    base_url: "https://openrouter.ai/api/v1"
    api_key: "${OPENROUTER_API_KEY}"  # Resolved from environment
```

**Key Techniques**:
- Use `@field_validator` on fields that may contain env vars
- Use `info.field_name` to customize behavior per field
- Regex pattern `r"\$\{([^}]+)\}"` to find `${VAR_NAME}`
- For optional fields (api_key): return `None` if env var missing
- For required fields (base_url): raise `ValueError` if env var missing
- Always load `.env` file first with `dotenv.load_dotenv()` in `load_config()`

## Pattern 4: Writing Migration Scripts

### Example: CLI Tools to Adapters Migration

**Problem**: You need to migrate existing config files from old format to new format automatically.

**Solution Pattern** (from `scripts/migrate_config.py`):

```python
#!/usr/bin/env python3
"""
Migration script: cli_tools → adapters

Migrates config.yaml from legacy cli_tools format to new adapters format
with explicit type fields.

Usage:
    python scripts/migrate_config.py [path/to/config.yaml]
"""

import shutil
import sys
from pathlib import Path
from typing import Any, Dict
import yaml

def migrate_config_dict(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Migrate config dictionary from cli_tools to adapters format.

    Returns:
        Migrated config with adapters section
    """
    # If already migrated, return as-is
    if "adapters" in config and "cli_tools" not in config:
        print("Info: Config already migrated (has 'adapters' section)")
        return config

    # If no cli_tools, nothing to migrate
    if "cli_tools" not in config:
        print("Warning: No 'cli_tools' section found, nothing to migrate")
        return config

    # Create new config with adapters
    migrated = config.copy()

    # Transform cli_tools → adapters
    adapters = {}
    for name, cli_config in config["cli_tools"].items():
        adapters[name] = {
            "type": "cli",  # Add explicit type discriminator
            "command": cli_config["command"],
            "args": cli_config["args"],
            "timeout": cli_config["timeout"],
        }

    migrated["adapters"] = adapters
    del migrated["cli_tools"]

    print(f"Success: Migrated {len(adapters)} CLI tools to adapters format")
    return migrated

def migrate_config_file(path: str) -> None:
    """
    Migrate config file from cli_tools to adapters format.

    Creates a backup at {path}.bak before modifying.
    """
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    # Create backup BEFORE modifying
    backup_path = Path(f"{path}.bak")
    shutil.copy2(config_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Load config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Migrate
    migrated = migrate_config_dict(config)

    # Write migrated config
    with open(config_path, "w") as f:
        yaml.dump(migrated, f, default_flow_style=False, sort_keys=False)

    print(f"Migrated config written to: {config_path}")
    print(f"\nInfo: Review the changes and delete {backup_path} when satisfied.")

def main():
    """Main entry point."""
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"

    print(f"Migrating config: {config_path}")
    print("-" * 50)

    try:
        migrate_config_file(config_path)
        print("\nMigration complete!")
        print("\nNext steps:")
        print("1. Review the migrated config.yaml")
        print("2. Test loading: python -c 'from models.config import load_config; load_config()'")
        print("3. Delete backup if satisfied: rm config.yaml.bak")
    except Exception as e:
        print(f"\nError: Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Key Techniques**:
- **Always create backup** before modifying config file (`shutil.copy2`)
- **Idempotent migrations**: Check if already migrated, return early if so
- **Separate dict and file logic**: `migrate_config_dict()` for logic, `migrate_config_file()` for I/O
- **Clear console output**: Print status messages for user feedback
- **Testing instructions**: Print validation commands after migration
- **Error handling**: Catch exceptions, print helpful message, exit with code 1
- **YAML preservation**: Use `sort_keys=False` to preserve key order

## Pattern 5: Field Validation for Path Resolution

### Example: Database Path with Environment Variables

**Problem**: You need to resolve relative paths and environment variables for config fields.

**Solution Pattern** (from `models/config.py`):

```python
import os
import re
from pathlib import Path
from pydantic import BaseModel, field_validator

class DecisionGraphConfig(BaseModel):
    """Configuration for decision graph memory."""
    db_path: str = "decision_graph.db"

    @field_validator("db_path")
    @classmethod
    def resolve_db_path(cls, v: str) -> str:
        """
        Resolve db_path to absolute path relative to project root.

        Processing steps:
        1. Resolve ${ENV_VAR} environment variable references
        2. Convert relative paths to absolute paths relative to project root
        3. Keep absolute paths unchanged
        4. Return normalized absolute path as string

        Examples:
            "decision_graph.db" → "/path/to/project/decision_graph.db"
            "/tmp/foo.db" → "/tmp/foo.db" (unchanged)
            "${DATA_DIR}/graph.db" → "/var/data/graph.db" (if DATA_DIR=/var/data)
        """
        # Step 1: Resolve environment variables
        pattern = r"\$\{([^}]+)\}"

        def replacer(match):
            env_var = match.group(1)
            value = os.getenv(env_var)
            if value is None:
                raise ValueError(
                    f"Environment variable '{env_var}' is not set. "
                    f"Required for db_path configuration."
                )
            return value

        resolved = re.sub(pattern, replacer, v)

        # Step 2: Convert to Path object
        path = Path(resolved)

        # Step 3: If relative, make it relative to project root
        if not path.is_absolute():
            # This file is at: project_root/models/config.py
            # Project root is two levels up from this file
            project_root = Path(__file__).parent.parent
            path = (project_root / path).resolve()

        # Step 4: Return as string (normalized, absolute)
        return str(path)
```

**Key Techniques**:
- Resolve env vars BEFORE path resolution
- Use `Path(__file__).parent.parent` to find project root
- Convert relative paths to absolute (prevents CWD issues)
- Keep absolute paths unchanged
- Return as string for serialization compatibility

## Pattern 6: Deprecating Fields with Validation

### Example: Deprecating `similarity_threshold` in Favor of `tier_boundaries`

**Problem**: You need to replace a single config field with a more complex structure.

**Solution Pattern** (from `models/config.py`):

```python
from pydantic import BaseModel, Field, field_validator

class DecisionGraphConfig(BaseModel):
    """Configuration for decision graph memory."""

    # DEPRECATED field (kept for backward compatibility)
    similarity_threshold: float = Field(
        0.7,
        ge=0.0,
        le=1.0,
        description="DEPRECATED: Use tier_boundaries instead.",
    )

    # NEW field (preferred)
    tier_boundaries: dict[str, float] = Field(
        default_factory=lambda: {"strong": 0.75, "moderate": 0.60},
        description="Similarity score boundaries for tiered injection"
    )

    @field_validator("tier_boundaries")
    @classmethod
    def validate_tier_boundaries(cls, v: dict[str, float]) -> dict[str, float]:
        """Validate tier boundaries: strong > moderate > 0."""
        if not isinstance(v, dict) or "strong" not in v or "moderate" not in v:
            raise ValueError("tier_boundaries must have 'strong' and 'moderate' keys")

        if not (0.0 < v["moderate"] < v["strong"] <= 1.0):
            raise ValueError(
                f"tier_boundaries must satisfy: 0 < moderate ({v['moderate']}) "
                f"< strong ({v['strong']}) <= 1"
            )

        return v
```

**YAML Usage**:
```yaml
decision_graph:
  # OLD (still works, but deprecated in field description)
  similarity_threshold: 0.7

  # NEW (preferred)
  tier_boundaries:
    strong: 0.75
    moderate: 0.60
```

**Key Techniques**:
- Keep deprecated field with default value
- Add "DEPRECATED" to field description
- Validate new field structure with `@field_validator`
- Document migration in code comments and CLAUDE.md
- Eventually remove deprecated field in future major version

## Testing Migration Scripts

### Before Deployment Checklist

1. **Unit Test the Migration Logic**:
   ```python
   def test_migrate_config_dict():
       """Test migration transforms cli_tools to adapters."""
       old_config = {
           "cli_tools": {
               "claude": {
                   "command": "claude",
                   "args": ["-p", "{prompt}"],
                   "timeout": 60
               }
           }
       }

       migrated = migrate_config_dict(old_config)

       assert "adapters" in migrated
       assert "cli_tools" not in migrated
       assert migrated["adapters"]["claude"]["type"] == "cli"
       assert migrated["adapters"]["claude"]["command"] == "claude"
   ```

2. **Test Idempotency**:
   ```python
   def test_migrate_idempotent():
       """Test migrating already-migrated config is safe."""
       already_migrated = {
           "adapters": {
               "claude": {"type": "cli", "command": "claude"}
           }
       }

       result = migrate_config_dict(already_migrated)
       assert result == already_migrated  # No changes
   ```

3. **Manual Testing Steps**:
   ```bash
   # 1. Create test config
   cp config.yaml config.test.yaml

   # 2. Run migration
   python scripts/migrate_config.py config.test.yaml

   # 3. Verify backup created
   ls -la config.test.yaml.bak

   # 4. Test loading migrated config
   python -c "from models.config import load_config; c = load_config('config.test.yaml'); print('OK')"

   # 5. Compare files
   diff config.test.yaml.bak config.test.yaml

   # 6. Clean up
   rm config.test.yaml config.test.yaml.bak
   ```

4. **Load-Time Validation**:
   ```bash
   # After migration, always test that config loads without errors
   python -c "from models.config import load_config; load_config()"
   ```

## Complete Migration Workflow

When you need to evolve a config schema:

### Step 1: Update Pydantic Models

1. Add new section/fields as `Optional` (don't break existing configs)
2. Keep old section/fields for backward compatibility
3. Add `@field_validator` for new field validation
4. Add deprecation warnings in `model_post_init()`

### Step 2: Write Migration Script

1. Create `scripts/migrate_*.py` with clear docstring
2. Implement `migrate_config_dict()` for logic (testable)
3. Implement `migrate_config_file()` for I/O (backup, load, migrate, save)
4. Add `main()` with CLI argument parsing
5. Print clear instructions after migration

### Step 3: Test Migration

1. Write unit tests for `migrate_config_dict()`
2. Test idempotency (running twice is safe)
3. Test edge cases (missing sections, already migrated)
4. Manually test on real config file
5. Verify migrated config loads successfully

### Step 4: Document Migration

1. Update CLAUDE.md with migration instructions
2. Add migration notes to config.yaml comments
3. Reference migration script in deprecation warnings
4. Update README if needed

### Step 5: Deploy

1. Commit schema changes + migration script together
2. Announce deprecation to users
3. Provide migration timeline (e.g., "deprecated in v2.0, removed in v3.0")
4. Keep backward compatibility for at least one major version

## Real-World Example: The cli_tools → adapters Migration

**Context**: AI Counsel needed to support both CLI and HTTP adapters, requiring type discrimination.

**Changes Made**:

1. **Schema Evolution** (`models/config.py`):
   - Created `CLIAdapterConfig` and `HTTPAdapterConfig` with `type` discriminator
   - Made `adapters` and `cli_tools` both optional
   - Added validation that at least one exists
   - Added deprecation warning for `cli_tools`

2. **Migration Script** (`scripts/migrate_config.py`):
   - Transforms `cli_tools` → `adapters` with `type: "cli"`
   - Creates backup before modifying
   - Idempotent (safe to run multiple times)
   - Clear user feedback and next steps

3. **Testing**:
   - Unit tests for `migrate_config_dict()`
   - Integration tests for file I/O
   - Manual testing on production config

4. **Documentation**:
   - Updated CLAUDE.md with migration guide
   - Added comments to config.yaml explaining both formats
   - Referenced migration script in deprecation warning

**Result**: Users can migrate seamlessly with one command, and old configs continue working with a warning.

## Common Patterns Summary

| Pattern | Use Case | Key Technique |
|---------|----------|---------------|
| Optional Sections | Add new section while keeping old | `Optional[T]` + validation |
| Discriminated Union | Type discrimination (CLI vs HTTP) | `Literal["type"]` + `Field(discriminator="type")` |
| Env Var Substitution | Inject secrets from environment | `@field_validator` + regex `\$\{VAR\}` |
| Path Resolution | Resolve relative paths | `Path(__file__).parent` + `resolve()` |
| Deprecation Warnings | Signal old patterns | `warnings.warn()` in `model_post_init()` |
| Migration Scripts | Automate config updates | Backup + dict transform + YAML dump |
| Field Validation | Complex field constraints | `@field_validator` + custom logic |

## File References

- **Config Models**: `/Users/harrison/Github/ai-counsel/models/config.py`
- **Migration Script**: `/Users/harrison/Github/ai-counsel/scripts/migrate_config.py`
- **Config File**: `/Users/harrison/Github/ai-counsel/config.yaml`
- **Project Docs**: `/Users/harrison/Github/ai-counsel/CLAUDE.md`

## Key Takeaways

1. **Never break existing configs** - always provide migration path
2. **Automate migrations** - don't force manual editing
3. **Use Pydantic validators** - catch errors at load time
4. **Support env vars** - never hardcode secrets
5. **Test thoroughly** - unit + integration + manual testing
6. **Document clearly** - in code, CLAUDE.md, and warnings
7. **Version carefully** - deprecate → warn → remove (over multiple versions)

---

When you detect config schema evolution needs, activate this skill and follow these patterns to ensure smooth, backward-compatible migrations.
