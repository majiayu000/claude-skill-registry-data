---
name: config-consistency-checker
description: Detects configuration drift and inconsistencies across environments by comparing dev, staging, and production configs, validating schemas, and reporting.
---

# Config Consistency Checker

Specialized skill for detecting, reporting, and resolving configuration drift across deployment environments. This skill compares configuration files, environment variables, secret references, and infrastructure parameters across dev, staging, and production to find missing keys, type mismatches, value inconsistencies, and schema violations. It produces actionable reports that identify exactly what differs, why it matters, and how to resolve each discrepancy. The approach works with any configuration format (YAML, JSON, TOML, .env, Kubernetes ConfigMaps) and integrates into CI/CD pipelines for continuous enforcement.

## When to Use This Skill

Use this skill for:

- Comparing configuration across environments (dev, staging, production) to find drift
- Detecting missing configuration keys that exist in one environment but not another
- Validating configuration files against a JSON Schema or custom schema definition
- Finding type mismatches where the same key holds different data types across environments
- Auditing secret references to ensure all required secrets are defined in every environment
- Generating drift reports for compliance audits or change review processes
- Integrating configuration validation into CI/CD pipelines as a pre-deployment check
- Debugging failures that only occur in specific environments due to configuration differences
- Enforcing configuration standards across microservices in a platform team context

**Trigger phrases**: "config drift", "configuration consistency", "environment comparison", "config validation", "missing config", "config mismatch", "environment variables check", "config audit", "schema validation", "config diff", "environment parity"

## What This Skill Does

This skill follows a structured methodology for configuration consistency:

1. **Config Discovery**: Locates all configuration sources for each environment, including files (YAML, JSON, TOML, .env), environment variables, Kubernetes ConfigMaps/Secrets, cloud provider parameter stores, and CI/CD variables.

2. **Normalization**: Converts all configuration sources into a common key-value representation with metadata (source file, environment, data type, whether it is a secret reference).

3. **Cross-Environment Comparison**: Compares normalized configuration across environments to identify keys that are missing, added, or have different values or types.

4. **Schema Validation**: Validates each environment's configuration against a defined schema (JSON Schema, custom rules) to catch constraint violations such as invalid URLs, out-of-range numbers, or malformed connection strings.

5. **Secret Reference Audit**: Checks that all secret references (environment variable placeholders, Vault paths, cloud secret ARNs) point to secrets that actually exist in the target secret store.

6. **Report Generation**: Produces a structured report (Markdown, JSON, or terminal output) that categorizes each finding by severity (critical, warning, info) with specific remediation guidance.

## Instructions

### Step 1: Define the Configuration Inventory

Before checking consistency, document what configuration sources exist for each environment:

```yaml
# config-inventory.yaml
environments:
  dev:
    config_files:
      - path: config/dev.yaml
        format: yaml
      - path: .env.dev
        format: dotenv
    kubernetes:
      namespace: app-dev
      configmaps:
        - app-config
      secrets:
        - app-secrets
    secret_store:
      type: aws-secrets-manager
      prefix: dev/

  staging:
    config_files:
      - path: config/staging.yaml
        format: yaml
      - path: .env.staging
        format: dotenv
    kubernetes:
      namespace: app-staging
      configmaps:
        - app-config
      secrets:
        - app-secrets
    secret_store:
      type: aws-secrets-manager
      prefix: staging/

  production:
    config_files:
      - path: config/production.yaml
        format: yaml
      - path: .env.production
        format: dotenv
    kubernetes:
      namespace: app-production
      configmaps:
        - app-config
      secrets:
        - app-secrets
    secret_store:
      type: aws-secrets-manager
      prefix: prod/

schema:
  path: config/schema.json
  format: json-schema

ignore_keys:
  - DATABASE_HOST
  - DATABASE_PORT
  - LOG_LEVEL
  - REPLICA_COUNT
```

### Step 2: Build the Configuration Parser

**Multi-Format Configuration Loader** (`scripts/config_loader.py`):

```python
"""Load configuration from multiple formats into a normalized structure."""
import json
import os
import re
from pathlib import Path
from typing import Any


def load_yaml(path: str) -> dict[str, Any]:
    """Load a YAML configuration file."""
    import yaml
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_json(path: str) -> dict[str, Any]:
    """Load a JSON configuration file."""
    with open(path) as f:
        return json.load(f)


def load_toml(path: str) -> dict[str, Any]:
    """Load a TOML configuration file."""
    import tomllib
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_dotenv(path: str) -> dict[str, str]:
    """Load a .env file into a flat dictionary."""
    result = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Remove surrounding quotes
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            result[key] = value
    return result


LOADERS = {
    "yaml": load_yaml,
    "yml": load_yaml,
    "json": load_json,
    "toml": load_toml,
    "dotenv": load_dotenv,
    "env": load_dotenv,
}


def flatten_dict(d: dict, prefix: str = "") -> dict[str, Any]:
    """Flatten a nested dictionary into dot-separated keys.

    Example: {"database": {"host": "localhost"}} -> {"database.host": "localhost"}
    """
    items = {}
    for key, value in d.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            items.update(flatten_dict(value, full_key))
        else:
            items[full_key] = value
    return items


def detect_type(value: Any) -> str:
    """Detect the semantic type of a configuration value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, str):
        # Detect common patterns
        if re.match(r"^https?://", value):
            return "url"
        if re.match(r"^\d+$", value):
            return "integer_string"
        if re.match(r"^(true|false)$", value, re.IGNORECASE):
            return "boolean_string"
        if re.match(r"^(arn:|vault:|ssm:)", value):
            return "secret_reference"
        return "string"
    return "unknown"


def load_config(path: str, format: str) -> dict[str, Any]:
    """Load a configuration file and return flattened key-value pairs with metadata."""
    loader = LOADERS.get(format)
    if loader is None:
        raise ValueError(f"Unsupported format: {format}")

    raw = loader(path)
    flat = flatten_dict(raw)

    # Annotate each value with type metadata
    annotated = {}
    for key, value in flat.items():
        annotated[key] = {
            "value": value,
            "type": detect_type(value),
            "source": path,
        }

    return annotated
```

### Step 3: Implement Cross-Environment Comparison

**Configuration Comparator** (`scripts/config_compare.py`):

```python
"""Compare configuration across environments and detect inconsistencies."""
import json
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class FindingType(str, Enum):
    MISSING_KEY = "missing_key"
    TYPE_MISMATCH = "type_mismatch"
    VALUE_DRIFT = "value_drift"
    EXTRA_KEY = "extra_key"
    SECRET_REFERENCE_MISSING = "secret_reference_missing"
    SCHEMA_VIOLATION = "schema_violation"


@dataclass
class Finding:
    finding_type: FindingType
    severity: Severity
    key: str
    message: str
    environments: dict = field(default_factory=dict)
    remediation: str = ""


def compare_environments(
    configs: dict[str, dict[str, Any]],
    reference_env: str = "production",
    ignore_keys: Optional[list[str]] = None,
) -> list[Finding]:
    """Compare all environments against a reference environment.

    Args:
        configs: Mapping of environment name to flattened config dict.
        reference_env: The environment to treat as the source of truth.
        ignore_keys: Keys to skip during comparison (environment-specific by design).

    Returns:
        List of findings sorted by severity.
    """
    findings = []
    ignore = set(ignore_keys or [])

    if reference_env not in configs:
        raise ValueError(f"Reference environment '{reference_env}' not found")

    ref_config = configs[reference_env]
    all_keys = set()
    for env_config in configs.values():
        all_keys.update(env_config.keys())

    for key in sorted(all_keys):
        if key in ignore:
            continue

        in_ref = key in ref_config
        env_presence = {env: key in cfg for env, cfg in configs.items()}
        present_envs = [env for env, present in env_presence.items() if present]
        missing_envs = [env for env, present in env_presence.items() if not present]

        # Check for missing keys
        if in_ref and missing_envs:
            findings.append(Finding(
                finding_type=FindingType.MISSING_KEY,
                severity=Severity.CRITICAL,
                key=key,
                message=f"Key exists in {reference_env} but is missing from: {', '.join(missing_envs)}",
                environments={
                    env: ref_config[key]["value"] if env == reference_env else "MISSING"
                    for env in configs
                },
                remediation=f"Add '{key}' to the configuration for: {', '.join(missing_envs)}",
            ))

        # Check for extra keys (in non-reference environments only)
        if not in_ref and present_envs:
            non_ref_present = [e for e in present_envs if e != reference_env]
            if non_ref_present:
                findings.append(Finding(
                    finding_type=FindingType.EXTRA_KEY,
                    severity=Severity.INFO,
                    key=key,
                    message=f"Key exists in {', '.join(non_ref_present)} but not in {reference_env}",
                    environments={
                        env: configs[env][key]["value"] if key in configs[env] else "MISSING"
                        for env in configs
                    },
                    remediation=f"Either add '{key}' to {reference_env} or remove it from {', '.join(non_ref_present)}",
                ))

        # Check for type mismatches across environments that have the key
        if len(present_envs) > 1:
            types = {
                env: configs[env][key]["type"]
                for env in present_envs
            }
            unique_types = set(types.values())
            if len(unique_types) > 1:
                findings.append(Finding(
                    finding_type=FindingType.TYPE_MISMATCH,
                    severity=Severity.WARNING,
                    key=key,
                    message=f"Type varies across environments: {types}",
                    environments={
                        env: f"{configs[env][key]['value']} ({configs[env][key]['type']})"
                        for env in present_envs
                    },
                    remediation=f"Ensure '{key}' has the same type in all environments. Expected type based on {reference_env}: {types.get(reference_env, 'unknown')}",
                ))

        # Check for secret references that might be missing
        for env in present_envs:
            entry = configs[env][key]
            if entry["type"] == "secret_reference":
                findings.append(Finding(
                    finding_type=FindingType.SECRET_REFERENCE_MISSING,
                    severity=Severity.WARNING,
                    key=key,
                    message=f"Secret reference in {env}: {entry['value']}. Verify this secret exists in the target store.",
                    environments={env: entry["value"]},
                    remediation=f"Verify that the secret '{entry['value']}' exists and is accessible from the {env} environment",
                ))

    # Sort by severity (critical first)
    severity_order = {Severity.CRITICAL: 0, Severity.WARNING: 1, Severity.INFO: 2}
    findings.sort(key=lambda f: severity_order[f.severity])

    return findings


def load_and_compare(inventory_path: str) -> list[Finding]:
    """Load configuration inventory and run comparison."""
    import yaml
    from config_loader import load_config

    with open(inventory_path) as f:
        inventory = yaml.safe_load(f)

    configs = {}
    for env_name, env_def in inventory["environments"].items():
        env_config = {}
        for file_def in env_def.get("config_files", []):
            file_config = load_config(file_def["path"], file_def["format"])
            env_config.update(file_config)
        configs[env_name] = env_config

    ignore_keys = inventory.get("ignore_keys", [])

    return compare_environments(
        configs,
        reference_env="production",
        ignore_keys=ignore_keys,
    )


if __name__ == "__main__":
    inventory = sys.argv[1] if len(sys.argv) > 1 else "config-inventory.yaml"
    output = sys.argv[2] if len(sys.argv) > 2 else "config_findings.json"

    findings = load_and_compare(inventory)

    with open(output, "w") as f:
        json.dump([asdict(f) for f in findings], f, indent=2, default=str)

    critical = sum(1 for f in findings if f.severity == Severity.CRITICAL)
    warnings = sum(1 for f in findings if f.severity == Severity.WARNING)
    info = sum(1 for f in findings if f.severity == Severity.INFO)

    print(f"Findings: {len(findings)} total ({critical} critical, {warnings} warning, {info} info)")

    if critical > 0:
        print("CRITICAL findings detected. Review config_findings.json for details.")
        sys.exit(1)
```

### Step 4: Implement Schema Validation

Define a JSON Schema that describes the expected configuration structure and validate each environment against it.

**Configuration Schema** (`config/schema.json`):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Application Configuration",
  "type": "object",
  "required": [
    "database.host",
    "database.port",
    "database.name",
    "server.port",
    "server.host",
    "auth.jwt_secret",
    "auth.token_expiry_seconds",
    "logging.level",
    "logging.format"
  ],
  "properties": {
    "database.host": {
      "type": "string",
      "minLength": 1,
      "description": "Database hostname or IP address"
    },
    "database.port": {
      "type": "integer",
      "minimum": 1,
      "maximum": 65535,
      "description": "Database port number"
    },
    "database.name": {
      "type": "string",
      "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$",
      "description": "Database name (alphanumeric and underscores)"
    },
    "database.max_connections": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1000,
      "default": 20,
      "description": "Maximum number of database connections in the pool"
    },
    "server.port": {
      "type": "integer",
      "minimum": 1,
      "maximum": 65535
    },
    "server.host": {
      "type": "string",
      "format": "hostname"
    },
    "auth.jwt_secret": {
      "type": "string",
      "minLength": 32,
      "description": "JWT signing secret (minimum 32 characters)"
    },
    "auth.token_expiry_seconds": {
      "type": "integer",
      "minimum": 60,
      "maximum": 604800,
      "description": "Token expiry in seconds (1 minute to 7 days)"
    },
    "logging.level": {
      "type": "string",
      "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    },
    "logging.format": {
      "type": "string",
      "enum": ["json", "text"]
    },
    "cache.ttl_seconds": {
      "type": "integer",
      "minimum": 0,
      "description": "Cache time-to-live in seconds (0 to disable)"
    },
    "cache.max_size_mb": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10240
    },
    "feature_flags.enable_new_search": {
      "type": "boolean"
    },
    "feature_flags.enable_export_v2": {
      "type": "boolean"
    }
  },
  "additionalProperties": true
}
```

**Schema Validator** (`scripts/config_validate_schema.py`):

```python
"""Validate configuration against a JSON Schema."""
import json
import sys
from dataclasses import dataclass
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator


@dataclass
class SchemaViolation:
    key: str
    message: str
    schema_path: str
    environment: str
    value: Any
    severity: str = "critical"


def validate_config(
    config: dict[str, Any],
    schema: dict,
    environment: str,
) -> list[SchemaViolation]:
    """Validate a flattened config dict against a JSON Schema.

    The config dict uses dot-separated keys. The schema must also use
    dot-separated keys in its properties (not nested objects).
    """
    violations = []

    # Extract just the values from annotated config
    values = {}
    for key, entry in config.items():
        if isinstance(entry, dict) and "value" in entry:
            values[key] = entry["value"]
        else:
            values[key] = entry

    # Coerce string values to their schema-expected types for validation
    properties = schema.get("properties", {})
    coerced = {}
    for key, value in values.items():
        if key in properties:
            expected_type = properties[key].get("type")
            if expected_type == "integer" and isinstance(value, str):
                try:
                    coerced[key] = int(value)
                except ValueError:
                    coerced[key] = value
            elif expected_type == "boolean" and isinstance(value, str):
                coerced[key] = value.lower() in ("true", "1", "yes")
            elif expected_type == "number" and isinstance(value, str):
                try:
                    coerced[key] = float(value)
                except ValueError:
                    coerced[key] = value
            else:
                coerced[key] = value
        else:
            coerced[key] = value

    # Validate
    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(coerced):
        # Determine the key from the error path
        if error.path:
            key = ".".join(str(p) for p in error.path)
        elif error.validator == "required":
            key = error.message.split("'")[1] if "'" in error.message else "unknown"
        else:
            key = "root"

        violations.append(SchemaViolation(
            key=key,
            message=error.message,
            schema_path=".".join(str(p) for p in error.absolute_schema_path),
            environment=environment,
            value=coerced.get(key),
        ))

    return violations


def validate_all_environments(
    configs: dict[str, dict[str, Any]],
    schema_path: str,
) -> dict[str, list[SchemaViolation]]:
    """Validate all environments against the schema."""
    with open(schema_path) as f:
        schema = json.load(f)

    results = {}
    for env_name, config in configs.items():
        violations = validate_config(config, schema, env_name)
        results[env_name] = violations

    return results


if __name__ == "__main__":
    import yaml
    from config_loader import load_config

    inventory_path = sys.argv[1] if len(sys.argv) > 1 else "config-inventory.yaml"

    with open(inventory_path) as f:
        inventory = yaml.safe_load(f)

    schema_path = inventory["schema"]["path"]

    all_violations = {}
    for env_name, env_def in inventory["environments"].items():
        env_config = {}
        for file_def in env_def.get("config_files", []):
            file_config = load_config(file_def["path"], file_def["format"])
            env_config.update(file_config)

        with open(schema_path) as f:
            schema = json.load(f)
        violations = validate_config(env_config, schema, env_name)
        all_violations[env_name] = violations

        if violations:
            print(f"\n{env_name}: {len(violations)} schema violations")
            for v in violations:
                print(f"  [{v.severity}] {v.key}: {v.message}")
        else:
            print(f"\n{env_name}: schema valid")

    total = sum(len(v) for v in all_violations.values())
    if total > 0:
        print(f"\nTotal schema violations: {total}")
        sys.exit(1)
    else:
        print("\nAll environments pass schema validation")
```

### Step 5: Implement Secret Reference Validation

Verify that all secret references in configuration actually point to existing secrets.

**Secret Reference Validator** (`scripts/validate_secrets.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:?Usage: validate_secrets.sh <environment> <config_file>}"
CONFIG_FILE="${2:?Missing config file path}"
SECRET_STORE="${3:-aws-secrets-manager}"

echo "=== Secret Reference Validation ==="
echo "Environment:  $ENVIRONMENT"
echo "Config file:  $CONFIG_FILE"
echo "Secret store: $SECRET_STORE"
echo ""

ERRORS=0
WARNINGS=0
CHECKED=0

# Extract secret references from config (values starting with arn:, vault:, ssm:)
while IFS='=' read -r KEY VALUE; do
  # Skip comments and empty lines
  [[ -z "$KEY" || "$KEY" =~ ^# ]] && continue

  # Remove quotes from value
  VALUE=$(echo "$VALUE" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")

  case "$VALUE" in
    arn:aws:secretsmanager:*)
      CHECKED=$((CHECKED + 1))
      SECRET_ID=$(echo "$VALUE" | sed 's|arn:aws:secretsmanager:[^:]*:[^:]*:secret:||')
      echo -n "Checking AWS secret: $SECRET_ID ... "
      if aws secretsmanager describe-secret --secret-id "$SECRET_ID" > /dev/null 2>&1; then
        echo "OK"
      else
        echo "MISSING"
        ERRORS=$((ERRORS + 1))
        echo "  ERROR: Secret '$SECRET_ID' referenced by '$KEY' does not exist"
      fi
      ;;

    ssm:*)
      CHECKED=$((CHECKED + 1))
      PARAM_NAME="${VALUE#ssm:}"
      echo -n "Checking SSM parameter: $PARAM_NAME ... "
      if aws ssm get-parameter --name "$PARAM_NAME" > /dev/null 2>&1; then
        echo "OK"
      else
        echo "MISSING"
        ERRORS=$((ERRORS + 1))
        echo "  ERROR: SSM parameter '$PARAM_NAME' referenced by '$KEY' does not exist"
      fi
      ;;

    vault:*)
      CHECKED=$((CHECKED + 1))
      VAULT_PATH="${VALUE#vault:}"
      echo -n "Checking Vault path: $VAULT_PATH ... "
      if vault kv get "$VAULT_PATH" > /dev/null 2>&1; then
        echo "OK"
      else
        echo "MISSING"
        ERRORS=$((ERRORS + 1))
        echo "  ERROR: Vault secret '$VAULT_PATH' referenced by '$KEY' does not exist"
      fi
      ;;

    *PASSWORD*|*SECRET*|*API_KEY*|*TOKEN*)
      # Value looks like it might be a plaintext secret
      if [[ "$VALUE" != *"arn:"* && "$VALUE" != *"vault:"* && "$VALUE" != *"ssm:"* ]]; then
        WARNINGS=$((WARNINGS + 1))
        echo "  WARNING: '$KEY' may contain a plaintext secret (not a reference)"
      fi
      ;;
  esac
done < "$CONFIG_FILE"

echo ""
echo "=== Results ==="
echo "Checked:  $CHECKED secret references"
echo "Errors:   $ERRORS (missing secrets)"
echo "Warnings: $WARNINGS (potential plaintext secrets)"

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi
```

### Step 6: Generate Drift Reports

**Drift Report Generator** (`scripts/generate_drift_report.py`):

```python
"""Generate a human-readable drift report from comparison findings."""
import json
import sys
from datetime import datetime, timezone


def generate_markdown_report(
    findings: list[dict],
    schema_violations: dict[str, list[dict]] | None = None,
) -> str:
    """Generate a Markdown drift report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = []
    lines.append("# Configuration Drift Report")
    lines.append("")
    lines.append(f"**Generated**: {now}")
    lines.append("")

    # Summary
    critical = [f for f in findings if f["severity"] == "critical"]
    warnings = [f for f in findings if f["severity"] == "warning"]
    info = [f for f in findings if f["severity"] == "info"]

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Severity | Count |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Critical | {len(critical)} |")
    lines.append(f"| Warning  | {len(warnings)} |")
    lines.append(f"| Info     | {len(info)} |")
    lines.append(f"| **Total** | **{len(findings)}** |")
    lines.append("")

    if not findings:
        lines.append("No configuration drift detected. All environments are consistent.")
        return "\n".join(lines)

    # Critical findings
    if critical:
        lines.append("## Critical Findings")
        lines.append("")
        lines.append("These issues will likely cause failures in the affected environments.")
        lines.append("")
        for f in critical:
            lines.append(f"### {f['key']}")
            lines.append("")
            lines.append(f"**Type**: {f['finding_type']}")
            lines.append(f"**Issue**: {f['message']}")
            lines.append("")
            if f.get("environments"):
                lines.append("| Environment | Value |")
                lines.append("|-------------|-------|")
                for env, val in f["environments"].items():
                    display_val = str(val)
                    if len(display_val) > 60:
                        display_val = display_val[:57] + "..."
                    lines.append(f"| {env} | `{display_val}` |")
                lines.append("")
            lines.append(f"**Remediation**: {f['remediation']}")
            lines.append("")

    # Warning findings
    if warnings:
        lines.append("## Warnings")
        lines.append("")
        lines.append("These issues may cause unexpected behavior or indicate configuration debt.")
        lines.append("")
        for f in warnings:
            lines.append(f"- **{f['key']}** ({f['finding_type']}): {f['message']}")
            if f.get("remediation"):
                lines.append(f"  - Remediation: {f['remediation']}")
        lines.append("")

    # Info findings
    if info:
        lines.append("## Informational")
        lines.append("")
        lines.append("These findings are non-critical but worth reviewing.")
        lines.append("")
        for f in info:
            lines.append(f"- **{f['key']}**: {f['message']}")
        lines.append("")

    # Schema violations
    if schema_violations:
        lines.append("## Schema Violations")
        lines.append("")
        for env, violations in schema_violations.items():
            if not violations:
                continue
            lines.append(f"### {env}")
            lines.append("")
            for v in violations:
                lines.append(f"- **{v['key']}**: {v['message']} (current value: `{v['value']}`)")
            lines.append("")

    return "\n".join(lines)


def generate_json_report(findings: list[dict]) -> str:
    """Generate a machine-readable JSON report."""
    now = datetime.now(timezone.utc).isoformat()
    report = {
        "generated_at": now,
        "total_findings": len(findings),
        "by_severity": {
            "critical": [f for f in findings if f["severity"] == "critical"],
            "warning": [f for f in findings if f["severity"] == "warning"],
            "info": [f for f in findings if f["severity"] == "info"],
        },
        "by_type": {},
    }

    for f in findings:
        ftype = f["finding_type"]
        report["by_type"].setdefault(ftype, []).append(f)

    return json.dumps(report, indent=2, default=str)


if __name__ == "__main__":
    findings_path = sys.argv[1] if len(sys.argv) > 1 else "config_findings.json"
    output_format = sys.argv[2] if len(sys.argv) > 2 else "markdown"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "drift_report.md"

    with open(findings_path) as f:
        findings = json.load(f)

    if output_format == "json":
        report = generate_json_report(findings)
        output_path = output_path.replace(".md", ".json")
    else:
        report = generate_markdown_report(findings)

    with open(output_path, "w") as f:
        f.write(report)

    print(f"Drift report written to {output_path}")
```

### Step 7: Integrate into CI/CD

**GitHub Actions Configuration Check** (`.github/workflows/config-check.yml`):

```yaml
name: Configuration Consistency Check

on:
  pull_request:
    paths:
      - "config/**"
      - ".env.*"
      - "k8s/**/configmap*.yaml"
  push:
    branches: [main]
    paths:
      - "config/**"
      - ".env.*"
  schedule:
    - cron: "0 8 * * 1"  # Weekly Monday at 08:00 UTC

jobs:
  check-config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install pyyaml jsonschema

      - name: Run configuration comparison
        run: |
          python scripts/config_compare.py config-inventory.yaml config_findings.json
        continue-on-error: true

      - name: Run schema validation
        run: |
          python scripts/config_validate_schema.py config-inventory.yaml
        continue-on-error: true

      - name: Generate drift report
        run: |
          python scripts/generate_drift_report.py config_findings.json markdown drift_report.md

      - name: Post report as PR comment
        if: github.event_name == 'pull_request'
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          path: drift_report.md

      - name: Check for critical findings
        run: |
          CRITICAL=$(python -c "
          import json
          with open('config_findings.json') as f:
              findings = json.load(f)
          critical = [f for f in findings if f['severity'] == 'critical']
          print(len(critical))
          ")

          if [ "$CRITICAL" -gt 0 ]; then
            echo "CRITICAL configuration issues detected: $CRITICAL"
            echo "Review drift_report.md for details"
            exit 1
          fi

          echo "No critical configuration issues found"

      - name: Upload drift report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: config-drift-report
          path: drift_report.md
          retention-days: 30
```

**Complete Pipeline Script** (`scripts/check-config-consistency.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

INVENTORY="${1:-config-inventory.yaml}"
OUTPUT_DIR="${2:-.config-check}"

echo "=== Configuration Consistency Check ==="
echo "Inventory: $INVENTORY"
echo ""

mkdir -p "$OUTPUT_DIR"

# Step 1: Compare environments
echo "--- Step 1: Cross-Environment Comparison ---"
python scripts/config_compare.py "$INVENTORY" "$OUTPUT_DIR/findings.json" || true

# Step 2: Schema validation
echo ""
echo "--- Step 2: Schema Validation ---"
python scripts/config_validate_schema.py "$INVENTORY" || true

# Step 3: Generate report
echo ""
echo "--- Step 3: Drift Report ---"
python scripts/generate_drift_report.py "$OUTPUT_DIR/findings.json" markdown "$OUTPUT_DIR/drift_report.md"

# Step 4: Summary
echo ""
echo "=== Results ==="
CRITICAL=$(python -c "
import json
with open('$OUTPUT_DIR/findings.json') as f:
    findings = json.load(f)
critical = [f for f in findings if f['severity'] == 'critical']
print(len(critical))
")

echo "Report: $OUTPUT_DIR/drift_report.md"
echo "Critical findings: $CRITICAL"

if [ "$CRITICAL" -gt 0 ]; then
  echo ""
  echo "FAIL: Critical configuration drift detected"
  exit 1
fi

echo "PASS: No critical configuration drift"
```

## Best Practices

- **Define a reference environment**: Always compare against one authoritative environment (typically production). This avoids ambiguity about which environment has the "correct" value when they differ.

- **Maintain an ignore list**: Some keys are expected to differ across environments (database hostnames, replica counts, log levels). Maintain an explicit ignore list so these expected differences do not generate noise in drift reports.

- **Use a schema from day one**: Defining a configuration schema is not overhead; it is documentation that validates itself. Start with required keys and basic type constraints, then add value constraints (min/max, regex patterns, enums) as you learn from production issues.

- **Run checks on every config change**: Integrate the consistency check into your CI pipeline so that every pull request modifying configuration files is automatically validated before merge.

- **Schedule weekly drift scans**: Configuration can drift outside of pull requests (through manual changes, infrastructure automation, or secret store updates). A weekly scheduled check catches drift that bypasses your CI pipeline.

- **Track drift over time**: Store drift reports as artifacts and track the trend. Increasing drift over time indicates process problems that need attention beyond fixing individual findings.

- **Validate secret references, not secret values**: Never compare actual secret values across environments (they should be different). Instead, validate that secret references (ARNs, Vault paths, SSM parameter names) resolve to existing secrets.

- **Version the schema alongside the application**: When the application adds a new required configuration key, update the schema in the same pull request. This keeps the schema in sync with the code that depends on it.

## Common Pitfalls

- **Comparing values that should differ**: Database hostnames, API URLs, and replica counts are expected to differ across environments. Comparing them produces false positives that train the team to ignore drift reports. Use an ignore list or mark these keys as "environment-specific" in the schema.

- **Not accounting for format differences**: The same logical value can be represented differently across formats. The integer `8080` in YAML becomes the string `"8080"` in a .env file. Your comparison logic must normalize types before comparing, or you will report false type mismatches on every dotenv-sourced key.

- **Ignoring configuration sources outside version control**: If production configuration is partially managed through a cloud console, Terraform state, or a parameter store, your drift check must include those sources. Checking only files in the repository misses a significant class of drift.

- **Treating all findings as equal severity**: A missing database connection string is critical; an extra debug flag is informational. Without severity classification, teams either fix everything (wasting time on noise) or ignore everything (missing critical issues).

- **Running checks only in CI**: CI checks catch drift introduced by pull requests, but not drift caused by manual changes, infrastructure automation, or secret rotation. Complement CI checks with scheduled scans that query live configuration.

- **Hardcoding environment names**: If your checker only works with "dev", "staging", and "production", it will break when a team adds "qa" or "performance" environments. Design the tool to work with any set of environment names defined in the inventory file.

- **Not handling missing files gracefully**: If a configuration file does not exist for an environment (perhaps because that environment uses only environment variables), the tool should report the missing file as a finding rather than crashing.

- **Comparing secret values across environments**: Production secrets should not match dev secrets. If your checker flags "API_KEY differs between dev and production" as a finding, it is generating noise. Compare secret presence and reference validity, not secret values.

- **Letting the ignore list grow unchecked**: An ignore list that grows over time without review becomes a way to sweep real issues under the rug. Periodically audit the ignore list to ensure every entry has a documented justification and is still relevant.

- **Generating reports that nobody reads**: A drift report is only useful if someone acts on it. Assign ownership of drift findings, set SLAs for resolution, and track closure rates. An unread report is the same as no report at all.
