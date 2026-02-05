---
name: Generate Marketplace
description: Generate marketplace catalog files from Betty Framework registries
---

# generate.marketplace

## Overview

**generate.marketplace** generates the RiskExec Claude Marketplace catalogs by filtering certified skills, agents, commands, and hooks from the Betty Framework registries. It transforms registry entries into marketplace-ready JSON files optimized for discovery and distribution.

## Purpose

Automates the generation of marketplace catalogs to maintain consistency between:
- **Skill Registry** (`registry/skills.json`) - All registered skills
- **Agent Registry** (`registry/agents.json`) - All registered agents
- **Command Registry** (`registry/commands.json`) - All registered commands
- **Hook Registry** (`registry/hooks.json`) - All registered hooks
- **Skills Marketplace** (`marketplace/skills.json`) - Certified skills for distribution
- **Agents Marketplace** (`marketplace/agents.json`) - Certified agents for distribution
- **Commands Marketplace** (`marketplace/commands.json`) - Certified commands for distribution
- **Hooks Marketplace** (`marketplace/hooks.json`) - Certified hooks for distribution

This eliminates manual curation of marketplace catalogs and ensures only production-ready, certified components are published.

## What It Does

1. **Reads Registries**: Loads `registry/skills.json`, `registry/agents.json`, `registry/commands.json`, and `registry/hooks.json`
2. **Filters Active Items**: Processes only entries with `status: active`
3. **Filters Certified Items**: Includes only entries with `certified: true` (if field exists)
4. **Transforms Format**: Converts registry entries to marketplace format
5. **Enriches Metadata**: Adds maintainer, usage examples, documentation URLs, and last_updated timestamps
6. **Generates Catalogs**: Outputs `marketplace/skills.json`, `marketplace/agents.json`, `marketplace/commands.json`, and `marketplace/hooks.json`
7. **Reports Statistics**: Shows certification counts and totals

## Usage

### Basic Usage

```bash
python skills/generate.marketplace/generate_marketplace.py
```

No arguments required - reads from standard registry locations.

### Via Betty CLI

```bash
/marketplace/generate
```

### Expected Directory Structure

```
betty/
├── registry/
│   ├── skills.json      # Source: All registered skills
│   ├── agents.json      # Source: All registered agents
│   ├── commands.json    # Source: All registered commands
│   └── hooks.json       # Source: All registered hooks
└── marketplace/
    ├── skills.json      # Output: Certified skills only
    ├── agents.json      # Output: Certified agents only
    ├── commands.json    # Output: Certified commands only
    └── hooks.json       # Output: Certified hooks only
```

## Filtering Logic

### Certification Criteria

A skill, agent, command, or hook is included in the marketplace if:

1. **Status is Active**: `status: "active"`
2. **Certified Flag** (if present): `certified: true`

If the `certified` field is not present, active items are considered certified by default.

### Status Values

| Status | Included in Marketplace | Purpose |
|--------|------------------------|---------|
| `active` | Yes | Production-ready, certified items |
| `draft` | No | Work in progress, not ready for distribution |
| `deprecated` | No | Outdated, should not be used |
| `experimental` | No | Testing phase, unstable |

## Output Format

### Skills Marketplace Structure

```json
{
  "marketplace_version": "1.0.0",
  "generated_at": "2025-10-23T17:51:58.579847+00:00",
  "last_updated": "2025-10-23T17:51:58.579847+00:00",
  "description": "Betty Framework Certified Skills Marketplace",
  "total_skills": 20,
  "certified_count": 16,
  "draft_count": 4,
  "catalog": [
    {
      "name": "api.validate",
      "version": "0.1.0",
      "description": "Validate OpenAPI and AsyncAPI specifications",
      "status": "certified",
      "tags": ["api", "validation", "openapi"],
      "maintainer": "Betty Core Team",
      "usage_examples": [
        "Validate OpenAPI spec: /skill/api/validate --spec_path api.yaml"
      ],
      "documentation_url": "https://betty-framework.dev/docs/skills/api.validate",
      "dependencies": ["context.schema"],
      "entrypoints": [...],
      "inputs": [...],
      "outputs": [...]
    }
  ]
}
```

### Agents Marketplace Structure

```json
{
  "marketplace_version": "1.0.0",
  "generated_at": "2025-10-23T17:03:16.154165+00:00",
  "last_updated": "2025-10-23T17:03:16.154165+00:00",
  "description": "Betty Framework Certified Agents Marketplace",
  "total_agents": 5,
  "certified_count": 3,
  "draft_count": 2,
  "catalog": [
    {
      "name": "api.designer",
      "version": "0.1.0",
      "description": "Design RESTful APIs following enterprise guidelines",
      "status": "certified",
      "reasoning_mode": "iterative",
      "skills_available": ["api.define", "api.validate"],
      "capabilities": [
        "Design RESTful APIs from natural language requirements"
      ],
      "tags": ["api", "design", "openapi"],
      "maintainer": "Betty Core Team",
      "documentation_url": "https://betty-framework.dev/docs/agents/api.designer",
      "dependencies": ["context.schema"]
    }
  ]
}
```

### Commands Marketplace Structure

```json
{
  "marketplace_version": "1.0.0",
  "generated_at": "2025-10-23T17:51:58.579847+00:00",
  "last_updated": "2025-10-23T17:51:58.579847+00:00",
  "description": "Betty Framework Certified Commands Marketplace",
  "total_commands": 4,
  "certified_count": 1,
  "draft_count": 3,
  "catalog": [
    {
      "name": "/test-workflow-command",
      "version": "1.0.0",
      "description": "Test complete workflow",
      "status": "certified",
      "tags": ["test", "workflow"],
      "execution": {
        "type": "skill",
        "target": "api.validate"
      },
      "parameters": [
        {
          "name": "input",
          "type": "string",
          "required": true,
          "description": "Input parameter"
        }
      ],
      "maintainer": "Betty Core Team"
    }
  ]
}
```

### Hooks Marketplace Structure

```json
{
  "marketplace_version": "1.0.0",
  "generated_at": "2025-10-23T17:51:58.579847+00:00",
  "last_updated": "2025-10-23T17:51:58.579847+00:00",
  "description": "Betty Framework Certified Hooks Marketplace",
  "total_hooks": 4,
  "certified_count": 1,
  "draft_count": 3,
  "catalog": [
    {
      "name": "test-workflow-hook",
      "version": "1.0.0",
      "description": "Test complete workflow",
      "status": "certified",
      "tags": ["test", "workflow", "openapi"],
      "event": "on_file_edit",
      "command": "python validate.py {file_path}",
      "blocking": true,
      "when": {
        "pattern": "*.openapi.yaml"
      },
      "timeout": 30000,
      "on_failure": "show_errors",
      "maintainer": "Betty Core Team"
    }
  ]
}
```

## Marketplace Transformations

### From Registry to Marketplace

The skill transforms registry entries to marketplace format:

#### Skills and Agents

| Registry Field | Marketplace Field | Transformation |
|----------------|-------------------|----------------|
| `status: "active"` | `status: "certified"` | Renamed for marketplace context |
| `name` | `name` | Preserved |
| `version` | `version` | Preserved |
| `description` | `description` | Preserved |
| `tags` | `tags` | Preserved (default: `[]`) |
| `dependencies` | `dependencies` | Preserved (default: `[]`) |
| `entrypoints` | `entrypoints` | Preserved (skills only) |
| `inputs` | `inputs` | Preserved (skills only) |
| `outputs` | `outputs` | Preserved (skills only) |
| `skills_available` | `skills_available` | Preserved (agents only) |
| `capabilities` | `capabilities` | Preserved (agents only) |
| `reasoning_mode` | `reasoning_mode` | Preserved (agents only) |
| N/A | `maintainer` | Added (default: "Betty Core Team") |
| N/A | `usage_examples` | Generated from entrypoints or provided |
| N/A | `documentation_url` | Generated: `https://betty-framework.dev/docs/{type}/{name}` |
| N/A | `last_updated` | Added: ISO timestamp |

#### Commands

| Registry Field | Marketplace Field | Transformation |
|----------------|-------------------|----------------|
| `status: "active"` | `status: "certified"` | Renamed for marketplace context |
| `name` | `name` | Preserved |
| `version` | `version` | Preserved |
| `description` | `description` | Preserved |
| `tags` | `tags` | Preserved (default: `[]`) |
| `execution` | `execution` | Preserved |
| `parameters` | `parameters` | Preserved (default: `[]`) |
| N/A | `maintainer` | Added (default: "Betty Core Team") |
| N/A | `last_updated` | Added: ISO timestamp |

#### Hooks

| Registry Field | Marketplace Field | Transformation |
|----------------|-------------------|----------------|
| `status: "active"` | `status: "certified"` | Renamed for marketplace context |
| `name` | `name` | Preserved |
| `version` | `version` | Preserved |
| `description` | `description` | Preserved |
| `tags` | `tags` | Preserved (default: `[]`) |
| `event` | `event` | Preserved |
| `command` | `command` | Preserved |
| `blocking` | `blocking` | Preserved (default: `false`) |
| `when` | `when` | Preserved (default: `{}`) |
| `timeout` | `timeout` | Preserved |
| `on_failure` | `on_failure` | Preserved |
| N/A | `maintainer` | Added (default: "Betty Core Team") |
| N/A | `last_updated` | Added: ISO timestamp |

### Metadata Enrichment

The skill adds marketplace-specific metadata:

1. **Maintainer**: Defaults to "Betty Core Team" if not specified
2. **Usage Examples**: Auto-generated from entrypoint commands if missing (skills only)
3. **Documentation URL**: Generated following the pattern `https://betty-framework.dev/docs/{skills|agents}/{name}` (skills and agents only)
4. **Last Updated**: ISO timestamp added to all marketplace files
5. **Statistics**: Adds total counts, certified counts, and draft counts

## Behavior

### 1. Registry Loading

Reads JSON files from:
- `registry/skills.json`
- `registry/agents.json`
- `registry/commands.json`
- `registry/hooks.json`

If a registry file is missing, the skill fails with an error.

### 2. Filtering

For each skill/agent/command/hook in the registry:
- Checks `status` field - must be `"active"`
- Checks `certified` field (if present) - must be `true`
- Skips items that don't meet criteria
- Logs which items are included/excluded

### 3. Transformation

Converts each certified entry:
- Copies core fields (name, version, description, tags)
- Transforms `status: "active"` → `status: "certified"`
- Adds marketplace metadata (maintainer, last_updated timestamp)
- For skills: Adds docs URL and generates usage examples if not provided
- For agents: Adds docs URL
- Preserves all technical details (entrypoints, inputs, outputs, execution, parameters, event, command, etc.)

### 4. Statistics Calculation

Tracks:
- **Total items**: All items in registry
- **Certified count**: Items included in marketplace
- **Draft count**: Items excluded (total - certified)

### 5. File Writing

Writes marketplace catalogs:
- Creates `marketplace/` directory if needed
- Formats JSON with 2-space indentation
- Preserves Unicode characters (no ASCII escaping)
- Adds generation timestamp

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "success",
  "skills_output": "/home/user/betty/marketplace/skills.json",
  "agents_output": "/home/user/betty/marketplace/agents.json",
  "commands_output": "/home/user/betty/marketplace/commands.json",
  "hooks_output": "/home/user/betty/marketplace/hooks.json",
  "skills_certified": 16,
  "skills_total": 20,
  "agents_certified": 3,
  "agents_total": 5,
  "commands_certified": 1,
  "commands_total": 4,
  "hooks_certified": 1,
  "hooks_total": 4
}
```

### Failure Response

```json
{
  "ok": false,
  "status": "failed",
  "error": "Registry file not found: /home/user/betty/registry/skills.json"
}
```

## Examples

### Example 1: Basic Marketplace Generation

**Scenario**: Generate marketplace catalogs after adding new certified skills

```bash
# Register new skills
/skill/define skills/data.transform/skill.yaml
/skill/define skills/api.monitor/skill.yaml

# Update registry
/registry/update

# Generate marketplace
/marketplace/generate
```

**Output**:
```
INFO: Starting marketplace catalog generation from registries...
INFO: Loading registry files...
INFO: Generating marketplace catalogs...
INFO: Added certified skill: api.validate
INFO: Added certified skill: api.define
INFO: Skipped non-certified skill: test.hello (status: draft)
INFO: Added certified agent: api.designer
INFO: Added certified command: /test-workflow-command
INFO: Skipped non-certified command: /test-command (status: draft)
INFO: Added certified hook: test-workflow-hook
INFO: Skipped non-certified hook: test-validation-hook (status: draft)
INFO: Writing marketplace files...
INFO: ✅ Written marketplace file to /home/user/betty/marketplace/skills.json
INFO: ✅ Written marketplace file to /home/user/betty/marketplace/agents.json
INFO: ✅ Written marketplace file to /home/user/betty/marketplace/commands.json
INFO: ✅ Written marketplace file to /home/user/betty/marketplace/hooks.json
INFO: ✅ Generated marketplace catalogs:
INFO:    Skills: 16/20 certified
INFO:    Agents: 3/5 certified
INFO:    Commands: 1/4 certified
INFO:    Hooks: 1/4 certified
```

### Example 2: After Promoting Skills to Active

**Scenario**: Skills were marked as active and should now appear in marketplace

```bash
# Edit registry to mark skills as active
# (Normally done via skill.define)

# Regenerate marketplace
/marketplace/generate
```

**Before** (registry):
```json
{
  "name": "my.skill",
  "status": "draft"
}
```

**After** (registry updated):
```json
{
  "name": "my.skill",
  "status": "active"
}
```

**Marketplace** (now includes):
```json
{
  "name": "my.skill",
  "status": "certified"
}
```

### Example 3: Publishing to GitHub Pages

**Scenario**: Deploy marketplace catalogs to public API endpoint

```bash
# Generate marketplace
/marketplace/generate

# Copy to GitHub Pages directory
cp marketplace/*.json docs/api/v1/

# Commit and push
git add marketplace/ docs/api/v1/
git commit -m "Update marketplace catalog"
git push
```

Now accessible at:
- `https://riskexec.github.io/betty/api/v1/skills.json`
- `https://riskexec.github.io/betty/api/v1/agents.json`
- `https://riskexec.github.io/betty/api/v1/commands.json`
- `https://riskexec.github.io/betty/api/v1/hooks.json`

### Example 4: CI/CD Integration

**Scenario**: Auto-generate marketplace on every registry change

```yaml
# .github/workflows/marketplace.yml
name: Update Marketplace
on:
  push:
    paths:
      - 'registry/*.json'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate Marketplace
        run: python skills/generate.marketplace/generate_marketplace.py
      - name: Commit Changes
        run: |
          git config user.name "Betty Bot"
          git config user.email "bot@riskexec.com"
          git add marketplace/
          git commit -m "chore: update marketplace catalog"
          git push
```

## Integration

### With skill.define Workflow

After registering skills, regenerate marketplace:

```bash
/skill/define skills/new.skill/skill.yaml
/registry/update
/marketplace/generate
```

### With Workflows

Include marketplace generation as a workflow step:

```yaml
# workflows/skill_lifecycle.yaml
steps:
  - skill: skill.create
    args: ["new.skill", "Description"]

  - skill: skill.define
    args: ["skills/new.skill/skill.yaml"]

  - skill: registry.update
    args: ["skills/new.skill/skill.yaml"]

  - skill: generate.marketplace
    args: []
```

### With Hooks

Auto-regenerate marketplace when registries change:

```yaml
# .claude/hooks.yaml
- event: on_file_save
  pattern: "registry/*.json"
  command: python skills/generate.marketplace/generate_marketplace.py
  blocking: false
  description: Auto-regenerate marketplace when registry changes
```

## What Gets Included

### Included in Marketplace

- Skills/agents/commands/hooks with `status: "active"`
- Skills/agents/commands/hooks with `certified: true` (if field exists)
- All technical metadata (entrypoints, inputs, outputs, execution, parameters, event, command, etc.)
- All semantic metadata (tags, dependencies)
- Last updated timestamp for all entries

### Not Included

- Skills/agents/commands/hooks with `status: "draft"`
- Skills/agents/commands/hooks with `status: "deprecated"`
- Skills/agents/commands/hooks with `certified: false`
- Internal-only items
- Test/experimental items (unless marked active)

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Registry file not found" | Missing registry file | Ensure `registry/skills.json` and `registry/agents.json` exist |
| "Failed to parse JSON" | Invalid JSON syntax | Fix JSON syntax in registry files |
| "Permission denied" | Cannot write marketplace files | Check write permissions on `marketplace/` directory |
| Empty marketplace | No active skills | Mark skills as `status: "active"` in registry |

## Files Read

- `registry/skills.json` - Skill registry (source)
- `registry/agents.json` - Agent registry (source)
- `registry/commands.json` - Command registry (source)
- `registry/hooks.json` - Hook registry (source)

## Files Modified

- `marketplace/skills.json` - Skills marketplace catalog (output)
- `marketplace/agents.json` - Agents marketplace catalog (output)
- `marketplace/commands.json` - Commands marketplace catalog (output)
- `marketplace/hooks.json` - Hooks marketplace catalog (output)

## Exit Codes

- **0**: Success (marketplace catalogs generated successfully)
- **1**: Failure (error during generation)

## Logging

Logs generation progress:

```
INFO: Starting marketplace catalog generation from registries...
INFO: Loading registry files...
INFO: Generating marketplace catalogs...
INFO: Added certified skill: api.validate
INFO: Added certified skill: hook.define
DEBUG: Skipped non-certified skill: test.hello (status: draft)
INFO: Added certified agent: api.designer
INFO: Added certified command: /test-workflow-command
DEBUG: Skipped non-certified command: /test-command (status: draft)
INFO: Added certified hook: test-workflow-hook
DEBUG: Skipped non-certified hook: test-validation-hook (status: draft)
INFO: Writing marketplace files...
INFO: ✅ Written marketplace file to marketplace/skills.json
INFO: ✅ Written marketplace file to marketplace/agents.json
INFO: ✅ Written marketplace file to marketplace/commands.json
INFO: ✅ Written marketplace file to marketplace/hooks.json
INFO: ✅ Generated marketplace catalogs:
INFO:    Skills: 16/20 certified
INFO:    Agents: 3/5 certified
INFO:    Commands: 1/4 certified
INFO:    Hooks: 1/4 certified
```

## Best Practices

1. **Run After Registry Updates**: Regenerate marketplace after adding/updating skills
2. **Automate with CI/CD**: Set up automated marketplace generation in pipelines
3. **Review Before Publishing**: Check generated catalogs before deploying
4. **Version Control**: Commit marketplace files with registry changes
5. **Keep Registries Clean**: Remove deprecated skills to keep marketplace focused
6. **Document Thoroughly**: Ensure skills have good descriptions and examples

## Troubleshooting

### Marketplace Files Not Updating

**Problem**: Changes to registry don't appear in marketplace

**Solutions**:
- Ensure skill status is `"active"` in registry
- Check that `certified` field is `true` (if present)
- Run `/registry/update` before `/marketplace/generate`
- Verify registry JSON syntax is valid

### Skills Missing from Marketplace

**Problem**: Active skills not appearing in marketplace

**Solutions**:
- Check skill status in `registry/skills.json`
- Verify no `certified: false` field
- Ensure skill.yaml has been validated with `/skill/define`
- Check logs for filtering messages

### Empty Marketplace Catalogs

**Problem**: Marketplace has 0 certified items

**Solutions**:
- Mark skills as `status: "active"` in registry
- Remove `certified: false` from skill entries
- Ensure registry files are not empty
- Run `/skill/define` to register skills first

## Version Diff (Optional)

To add version diff vs. last release:

```python
# Future enhancement
def get_version_diff(old_marketplace, new_marketplace):
    """Compare two marketplace versions and return diff."""
    added = [s for s in new if s not in old]
    removed = [s for s in old if s not in new]
    updated = [s for s in new if s in old and version_changed(s)]
    return {"added": added, "removed": removed, "updated": updated}
```

## Upload to API (Optional)

To upload generated catalogs to an API:

```python
# Future enhancement
import requests

def upload_to_api(marketplace_data, api_endpoint, api_key):
    """Upload marketplace catalog to internal API."""
    response = requests.post(
        api_endpoint,
        json=marketplace_data,
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return response.status_code == 200
```

## Architecture

### Skill Categories

**Infrastructure** - generate.marketplace maintains the marketplace layer by transforming registry state into certified catalogs.

### Design Principles

- **Single Source of Truth**: Registry files are the source
- **Idempotent**: Can be run multiple times safely
- **Certification Filter**: Only production-ready items included
- **Metadata Enrichment**: Adds marketplace-specific fields
- **Clear Statistics**: Reports certification rates

## See Also

- **plugin.sync** - Generate plugin.yaml from registries ([SKILL.md](../plugin.sync/SKILL.md))
- **registry.update** - Update skill registry ([SKILL.md](../registry.update/SKILL.md))
- **skill.define** - Validate and register skills ([SKILL.md](../skill.define/SKILL.md))
- **Betty Architecture** - Framework overview ([betty-architecture.md](../../docs/betty-architecture.md))

## Dependencies

- **registry.update**: Registry management
- **betty.config**: Configuration constants and paths
- **betty.logging_utils**: Logging infrastructure

## Status

**Active** - Production-ready infrastructure skill

## Version History

- **0.2.0** (Oct 2025) - Added support for commands and hooks, added last_updated timestamps
- **0.1.0** (Oct 2025) - Initial implementation with filtering and marketplace generation for skills and agents
