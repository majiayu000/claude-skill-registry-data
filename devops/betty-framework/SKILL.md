---
name: Plugin Manifest Sync
description: Reconcile plugin.yaml with Betty Framework registries
---

# docs.sync.plugin_manifest

## Overview

**docs.sync.plugin_manifest** is a validation and reconciliation tool that compares `plugin.yaml` against Betty Framework's registry files to ensure consistency and completeness. It identifies missing commands, orphaned entries, metadata mismatches, and suggests corrections.

## Purpose

Ensures synchronization between:
- **Skill Registry** (`registry/skills.json`) – Active skills with entrypoints
- **Command Registry** (`registry/commands.json`) – Slash commands
- **Plugin Configuration** (`plugin.yaml`) – Claude Code plugin manifest

This skill helps maintain plugin.yaml accuracy by detecting:
- Active skills missing from plugin.yaml
- Orphaned commands in plugin.yaml not found in registries
- Metadata inconsistencies (permissions, runtime, handlers)
- Missing metadata that should be added

## What It Does

1. **Loads Registries**: Reads `skills.json` and `commands.json`
2. **Loads Plugin**: Reads current `plugin.yaml`
3. **Builds Indexes**: Creates lookup tables for both registries and plugin
4. **Compares Entries**: Identifies missing, orphaned, and mismatched commands
5. **Analyzes Metadata**: Checks permissions, runtime, handlers, descriptions
6. **Generates Preview**: Creates `plugin.preview.yaml` with suggested updates
7. **Creates Report**: Outputs `plugin_manifest_diff.md` with detailed analysis
8. **Provides Summary**: Displays key findings and recommendations

## Usage

### Basic Usage

```bash
python skills/docs.sync.plugin_manifest/plugin_manifest_sync.py
```

No arguments required - reads from standard locations.

### Via Betty CLI

```bash
/docs/sync/plugin-manifest
```

### Expected File Structure

```
betty/
├── registry/
│   ├── skills.json      # Source of truth for skills
│   └── commands.json    # Source of truth for commands
├── plugin.yaml          # Current plugin manifest
├── plugin.preview.yaml  # Generated preview (output)
└── plugin_manifest_diff.md  # Generated report (output)
```

## Behavior

### 1. Registry Loading

Reads and parses:
- `registry/skills.json` – All registered skills
- `registry/commands.json` – All registered commands

Only processes entries with `status: active`.

### 2. Plugin Loading

Reads and parses:
- `plugin.yaml` – Current plugin configuration

Extracts all command definitions.

### 3. Index Building

**Registry Index**: Maps command names to their registry sources

```python
{
  "skill/define": {
    "type": "skill",
    "source": "skill.define",
    "skill": {...},
    "entrypoint": {...}
  },
  "api/validate": {
    "type": "skill",
    "source": "api.validate",
    "skill": {...},
    "entrypoint": {...}
  }
}
```

**Plugin Index**: Maps command names to plugin entries

```python
{
  "skill/define": {
    "name": "skill/define",
    "handler": {...},
    "permissions": [...]
  }
}
```

### 4. Comparison Analysis

Performs four types of checks:

#### Missing Commands
Commands in registry but not in plugin.yaml:
```
- skill/create (active in registry, missing from plugin)
- api/validate (active in registry, missing from plugin)
```

#### Orphaned Commands
Commands in plugin.yaml but not in registry:
```
- old/deprecated (in plugin but not registered)
- test/removed (in plugin but removed from registry)
```

#### Metadata Mismatches
Commands present in both but with different metadata:

**Runtime Mismatch**:
```
- skill/define:
  - Registry: python
  - Plugin: node
```

**Permission Mismatch**:
```
- api/validate:
  - Missing: filesystem:read
  - Extra: network:write
```

**Handler Mismatch**:
```
- skill/create:
  - Registry: skills/skill.create/skill_create.py
  - Plugin: skills/skill.create/old_handler.py
```

**Description Mismatch**:
```
- agent/run:
  - Registry: "Execute a Betty agent..."
  - Plugin: "Run agent"
```

#### Missing Metadata Suggestions
Identifies registry entries missing recommended metadata:
```
- hook/define: Consider adding permissions metadata
- test/skill: Consider adding description
```

### 5. Preview Generation

Creates `plugin.preview.yaml` by:
- Taking all active commands from registries
- Converting to plugin.yaml format
- Including all metadata from registries
- Adding generation timestamp
- Preserving existing plugin metadata (author, license, etc.)

### 6. Report Generation

Creates `plugin_manifest_diff.md` with:
- Executive summary
- Lists of missing commands
- Lists of orphaned commands
- Detailed metadata issues
- Metadata suggestions

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "success",
  "preview_path": "/home/user/betty/plugin.preview.yaml",
  "report_path": "/home/user/betty/plugin_manifest_diff.md",
  "reconciliation": {
    "missing_commands": [...],
    "orphaned_commands": [...],
    "metadata_issues": [...],
    "metadata_suggestions": [...],
    "total_registry_commands": 19,
    "total_plugin_commands": 18
  }
}
```

### Console Output

```
============================================================
PLUGIN MANIFEST RECONCILIATION COMPLETE
============================================================

📊 Summary:
  - Commands in registry: 19
  - Commands in plugin.yaml: 18
  - Missing from plugin.yaml: 2
  - Orphaned in plugin.yaml: 1
  - Metadata issues: 3
  - Metadata suggestions: 2

📄 Output files:
  - Preview: /home/user/betty/plugin.preview.yaml
  - Diff report: /home/user/betty/plugin_manifest_diff.md

⚠️  2 command(s) missing from plugin.yaml:
    - registry/query (registry.query)
    - hook/simulate (hook.simulate)

⚠️  1 orphaned command(s) in plugin.yaml:
    - old/deprecated

✅ Review plugin_manifest_diff.md for full details
============================================================
```

### Failure Response

```json
{
  "ok": false,
  "status": "failed",
  "error": "Failed to parse JSON from registry/skills.json"
}
```

## Generated Files

### plugin.preview.yaml

Updated plugin manifest with all active registry commands:

```yaml
# Betty Framework - Claude Code Plugin (Preview)
# Generated by docs.sync.plugin_manifest skill
# Review changes before applying to plugin.yaml

name: betty-framework
version: 1.0.0
description: Betty Framework - Structured AI-assisted engineering
author:
  name: RiskExec
  email: platform@riskexec.com
  url: https://github.com/epieczko/betty
license: MIT

metadata:
  generated_at: "2025-10-23T20:00:00.000000+00:00"
  generated_by: docs.sync.plugin_manifest skill
  command_count: 19

commands:
  - name: skill/define
    description: Validate a Claude Code skill manifest
    handler:
      runtime: python
      script: skills/skill.define/skill_define.py
    parameters:
      - name: manifest_path
        type: string
        required: true
        description: Path to skill.yaml file
    permissions:
      - filesystem:read
      - filesystem:write

  # ... more commands ...
```

### plugin_manifest_diff.md

Detailed reconciliation report:

```markdown
# Plugin Manifest Reconciliation Report
Generated: 2025-10-23T20:00:00.000000+00:00

## Summary
- Total commands in registry: 19
- Total commands in plugin.yaml: 18
- Missing from plugin.yaml: 2
- Orphaned in plugin.yaml: 1
- Metadata issues: 3
- Metadata suggestions: 2

## Missing Commands (in registry but not in plugin.yaml)
- **registry/query** (skill: registry.query)
- **hook/simulate** (skill: hook.simulate)

## Orphaned Commands (in plugin.yaml but not in registry)
- **old/deprecated**

## Metadata Issues
- **skill/create**: Permissions Mismatch
  - Missing: process:execute
  - Extra: network:http
- **api/validate**: Handler Mismatch
  - Registry: `skills/api.validate/api_validate.py`
  - Plugin: `skills/api.validate/validator.py`
- **agent/run**: Runtime Mismatch
  - Registry: `python`
  - Plugin: `node`

## Metadata Suggestions
- **hook/define** (permissions): Consider adding permissions metadata
- **test/skill** (description): Consider adding description
```

## Examples

### Example 1: Routine Sync Check

**Scenario**: Regular validation after making registry changes

```bash
# Make some registry updates
/skill/define skills/new.skill/skill.yaml

# Check for discrepancies
/docs/sync/plugin-manifest

# Review the report
cat plugin_manifest_diff.md

# If changes look good, apply them
cp plugin.preview.yaml plugin.yaml
```

**Output**:
```
============================================================
PLUGIN MANIFEST RECONCILIATION COMPLETE
============================================================

📊 Summary:
  - Commands in registry: 20
  - Commands in plugin.yaml: 19
  - Missing from plugin.yaml: 1
  - Orphaned in plugin.yaml: 0
  - Metadata issues: 0
  - Metadata suggestions: 0

⚠️  1 command(s) missing from plugin.yaml:
    - new/skill (new.skill)

✅ Review plugin_manifest_diff.md for full details
```

### Example 2: Detecting Orphaned Commands

**Scenario**: A skill was removed from registry but command remains in plugin.yaml

```bash
# Remove skill from registry
rm -rf skills/deprecated.skill/

# Run reconciliation
/docs/sync/plugin-manifest

# Check report
cat plugin_manifest_diff.md
```

**Output**:
```
============================================================
PLUGIN MANIFEST RECONCILIATION COMPLETE
============================================================

📊 Summary:
  - Commands in registry: 18
  - Commands in plugin.yaml: 19
  - Missing from plugin.yaml: 0
  - Orphaned in plugin.yaml: 1
  - Metadata issues: 0
  - Metadata suggestions: 0

⚠️  1 orphaned command(s) in plugin.yaml:
    - deprecated/skill

✅ Review plugin_manifest_diff.md for full details
```

### Example 3: Finding Metadata Mismatches

**Scenario**: Registry was updated but plugin.yaml wasn't synced

```bash
# Update skill permissions in registry
/skill/define skills/api.validate/skill.yaml

# Check for differences
/docs/sync/plugin-manifest

# Review specific mismatches
grep -A 5 "Metadata Issues" plugin_manifest_diff.md
```

**Report Output**:
```markdown
## Metadata Issues
- **api/validate**: Permissions Mismatch
  - Missing: network:http
  - Extra: filesystem:write
```

### Example 4: Pre-Commit Validation

**Scenario**: Validate plugin.yaml before committing changes

```bash
# Before committing
/docs/sync/plugin-manifest

# If discrepancies found, fix them
if [ $? -eq 0 ]; then
  # Review and apply changes
  diff plugin.yaml plugin.preview.yaml
  cp plugin.preview.yaml plugin.yaml
fi

# Commit changes
git add plugin.yaml
git commit -m "Sync plugin.yaml with registries"
```

### Example 5: CI/CD Integration

**Scenario**: Automated validation in CI pipeline

```yaml
# .github/workflows/validate-plugin.yml
name: Validate Plugin Manifest

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Reconcile Plugin Manifest
        run: |
          python skills/docs.sync.plugin_manifest/plugin_manifest_sync.py

          # Check if there are discrepancies
          if grep -q "Missing from plugin.yaml: [1-9]" plugin_manifest_diff.md; then
            echo "❌ Plugin manifest has missing commands"
            cat plugin_manifest_diff.md
            exit 1
          fi

          if grep -q "Orphaned in plugin.yaml: [1-9]" plugin_manifest_diff.md; then
            echo "❌ Plugin manifest has orphaned commands"
            cat plugin_manifest_diff.md
            exit 1
          fi

          echo "✅ Plugin manifest is in sync"
```

## Integration

### With plugin.sync

Use reconciliation to verify before syncing:

```bash
# Check current state
/docs/sync/plugin-manifest

# Review differences
cat plugin_manifest_diff.md

# If satisfied, run full sync
/plugin/sync
```

### With skill.define

Validate after defining skills:

```bash
# Define new skill
/skill/define skills/my.skill/skill.yaml

# Check plugin consistency
/docs/sync/plugin-manifest

# Apply changes if needed
cp plugin.preview.yaml plugin.yaml
```

### With Hooks

Auto-check on registry changes:

```yaml
# .claude/hooks.yaml
- event: on_file_save
  pattern: "registry/*.json"
  command: python skills/docs.sync.plugin_manifest/plugin_manifest_sync.py
  blocking: false
  description: Check plugin manifest sync when registries change
```

### With Workflows

Include in skill lifecycle workflow:

```yaml
# workflows/update_plugin.yaml
steps:
  - skill: skill.define
    args: ["skills/new.skill/skill.yaml"]

  - skill: docs.sync.plugin_manifest
    args: []

  - skill: plugin.sync
    args: []
```

## What Gets Reported

### ✅ Detected Issues

- Active skills missing from plugin.yaml
- Orphaned commands in plugin.yaml
- Runtime mismatches (python vs node)
- Permission mismatches (missing or extra)
- Handler path mismatches
- Description mismatches
- Missing metadata (permissions, descriptions)

### ❌ Not Detected

- Draft/inactive skills (intentionally excluded)
- Malformed YAML syntax (causes failure)
- Handler file existence (use plugin.sync for that)
- Parameter schema validation

## Common Use Cases

| Use Case | When to Use |
|----------|-------------|
| **Pre-commit check** | Before committing plugin.yaml changes |
| **Post-registry update** | After adding/updating skills in registry |
| **CI/CD validation** | Automated pipeline checks |
| **Manual audit** | Periodic manual review of plugin state |
| **Debugging** | When commands aren't appearing as expected |
| **Migration** | After major registry restructuring |

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Failed to parse JSON" | Invalid JSON in registry | Fix JSON syntax in registry files |
| "Failed to parse YAML" | Invalid YAML in plugin.yaml | Fix YAML syntax in plugin.yaml |
| "Registry file not found" | Missing registry files | Ensure registries exist in registry/ |
| "Permission denied" | Cannot write output files | Check write permissions on directory |
| All commands missing | Empty or invalid registries | Verify registry files are populated |

## Files Read

- `registry/skills.json` – Skill registry (source of truth)
- `registry/commands.json` – Command registry (source of truth)
- `plugin.yaml` – Current plugin manifest (for comparison)

## Files Generated

- `plugin.preview.yaml` – Updated plugin manifest preview
- `plugin_manifest_diff.md` – Detailed reconciliation report

## Exit Codes

- **0**: Success (reconciliation completed successfully)
- **1**: Failure (error during reconciliation)

Note: Discrepancies found are reported but don't cause failure (exit 0). Only parsing errors or system failures cause exit 1.

## Logging

Logs reconciliation progress:

```
INFO: Starting plugin manifest reconciliation...
INFO: Loading registry files...
INFO: Loading plugin.yaml...
INFO: Building registry index...
INFO: Building plugin index...
INFO: Comparing registries with plugin.yaml...
INFO: Reconciling registries with plugin.yaml...
INFO: Generating updated plugin.yaml...
INFO: ✅ Written file to /home/user/betty/plugin.preview.yaml
INFO: Generating diff report...
INFO: ✅ Written diff report to /home/user/betty/plugin_manifest_diff.md
```

## Best Practices

1. **Run Before Committing**: Always check sync status before committing plugin.yaml
2. **Review Diff Report**: Read the full report to understand all changes
3. **Validate Preview**: Review plugin.preview.yaml before applying
4. **Include in CI**: Add validation to your CI/CD pipeline
5. **Regular Audits**: Run periodic checks even without changes
6. **Address Orphans**: Remove orphaned commands promptly
7. **Fix Mismatches**: Resolve metadata mismatches to maintain consistency
8. **Keep Registries Clean**: Mark inactive skills as draft instead of deleting

## Workflow Integration

### Recommended Workflow

```bash
# 1. Define or update skills
/skill/define skills/my.skill/skill.yaml

# 2. Check for discrepancies
/docs/sync/plugin-manifest

# 3. Review the report
cat plugin_manifest_diff.md

# 4. Review the preview
diff plugin.yaml plugin.preview.yaml

# 5. Apply changes if satisfied
cp plugin.preview.yaml plugin.yaml

# 6. Commit changes
git add plugin.yaml registry/
git commit -m "Update plugin manifest"
```

### Alternative: Auto-Sync Workflow

```bash
# 1. Define or update skills
/skill/define skills/my.skill/skill.yaml

# 2. Run full sync (overwrites plugin.yaml)
/plugin/sync

# 3. Validate the result
/docs/sync/plugin-manifest

# 4. If clean, commit
git add plugin.yaml registry/
git commit -m "Update plugin manifest"
```

## Troubleshooting

### Plugin.yaml Shows as Out of Sync

**Problem**: Reconciliation reports missing or orphaned commands

**Solutions**:
1. Run `/plugin/sync` to regenerate plugin.yaml from registries
2. Review and apply `plugin.preview.yaml` manually
3. Check if skills are marked as `active` in registry
4. Verify skills have `entrypoints` defined

### Metadata Mismatches Reported

**Problem**: Registry and plugin have different permissions/runtime/handlers

**Solutions**:
1. Update skill.yaml with correct metadata
2. Run `/skill/define` to register changes
3. Run `/docs/sync/plugin-manifest` to verify
4. Apply plugin.preview.yaml or run `/plugin/sync`

### Orphaned Commands Found

**Problem**: Commands in plugin.yaml not found in registry

**Solutions**:
1. Check if skill was removed from registry
2. Verify skill status is `active` in registry
3. Re-register the skill if it should exist
4. Remove from plugin.yaml if intentionally deprecated

### Preview File Not Generated

**Problem**: plugin.preview.yaml missing after running skill

**Solutions**:
1. Check write permissions on betty/ directory
2. Verify registries are readable
3. Check logs for errors
4. Ensure plugin.yaml exists and is valid

## Architecture

### Skill Category

**Documentation & Infrastructure** – Maintains consistency between registry and plugin configuration layers.

### Design Principles

- **Non-Destructive**: Never modifies plugin.yaml directly
- **Comprehensive**: Reports all types of discrepancies
- **Actionable**: Provides preview file ready to apply
- **Transparent**: Detailed report explains all findings
- **Idempotent**: Can be run multiple times safely

## See Also

- **plugin.sync** – Generate plugin.yaml from registries ([SKILL.md](../plugin.sync/SKILL.md))
- **skill.define** – Validate and register skills ([SKILL.md](../skill.define/SKILL.md))
- **registry.update** – Update skill registry ([SKILL.md](../registry.update/SKILL.md))
- **Betty Architecture** – Framework overview ([betty-architecture.md](../../docs/betty-architecture.md))

## Dependencies

- **plugin.sync**: Plugin generation infrastructure
- **registry.update**: Registry management
- **betty.config**: Configuration constants and paths
- **betty.logging_utils**: Logging infrastructure

## Status

**Active** – Production-ready documentation and validation skill

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with full reconciliation, preview generation, and diff reporting
