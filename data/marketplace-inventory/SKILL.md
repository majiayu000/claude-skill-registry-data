---
name: tools-marketplace-inventory
description: Scans and reports complete marketplace inventory (bundles, agents, commands, skills, scripts)
allowed-tools:
  - Read
  - Bash
  - Glob
---

# Marketplace Inventory Skill

Provides complete marketplace inventory scanning capabilities using the scan-marketplace-inventory.py script.

## Purpose

This skill scans the marketplace directory structure and returns a comprehensive TOON inventory of all bundles and their resources (agents, commands, skills, scripts).

## When to Use This Skill

Activate this skill when you need to:
- Get a complete inventory of marketplace bundles
- Discover all available agents, commands, and skills
- Validate marketplace structure
- Generate reports on marketplace contents

## Workflow

When activated, this skill scans the marketplace and returns structured TOON inventory.

### Step 1: Execute Inventory Scan

Run the marketplace inventory scanner script:

**Script**: `pm-plugin-development:tools-marketplace-inventory`

```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --scope marketplace
```

The script will:
- Discover all bundles in marketplace/bundles/
- Enumerate agents, commands, and skills in each bundle
- Identify bundled scripts
- Write full TOON inventory to `.plan/temp/tools-marketplace-inventory/inventory-{timestamp}.toon`
- Return TOON summary with file path to stdout

### Step 2: Read Full Inventory

The script outputs a TOON summary to stdout:

```toon
status: success
output_mode: file
output_file: .plan/temp/tools-marketplace-inventory/inventory-20260116-143022.toon
scope: marketplace
base_path: /path/to/marketplace/bundles
statistics:
  total_bundles: 8
  total_agents: 28
  total_commands: 46
  total_skills: 30
  total_scripts: 7
  total_resources: 111
next_step: Read .plan/temp/tools-marketplace-inventory/inventory-20260116-143022.toon for full inventory details
```

Read the `output_file` to get the full inventory in TOON format.

## Script Parameters

### --scope (optional)

Directory scope to scan. Default: `auto`

| Value | Description |
|-------|-------------|
| `auto` | **Default**. Tries `marketplace/bundles/` first, falls back to `plugin-cache` |
| `marketplace` | Explicit: scans marketplace/bundles/ directory only |
| `plugin-cache` | Explicit: scans ~/.claude/plugins/cache/plan-marshall/ only |
| `global` | Scans ~/.claude directory |
| `project` | Scans .claude directory in current working directory |

The `auto` default makes the script work in both the marketplace repo and other projects without specifying a scope.

**Example**:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --scope marketplace
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --scope project
```

### --resource-types (optional)

Filter which resource types to include in the inventory. Default: `all`

| Value | Description |
|-------|-------------|
| `all` | Include all resource types (default) |
| `agents` | Include only agents |
| `commands` | Include only commands |
| `skills` | Include only skills |
| `scripts` | Include only scripts |

Multiple types can be combined with commas:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --resource-types agents,skills
```

### --include-descriptions (optional flag)

When specified, extracts description fields from YAML frontmatter of each resource file.

**Example**:
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --include-descriptions
```

**Output with descriptions** (excerpt from file):
```toon
agents[1]{name,path,description}:
java-implement-agent,marketplace/bundles/pm-dev-java/agents/java-implement-agent.md,Implements Java code following CUI standards
```

### --name-pattern (optional)

Filter resources by name using fnmatch glob patterns. Use pipe (`|`) to separate multiple patterns.

| Pattern | Matches |
|---------|---------|
| `*-plan-*` | Names containing "-plan-" |
| `plan-*` | Names starting with "plan-" |
| `*-agent` | Names ending with "-agent" |

**Examples**:
```bash
# Single pattern
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --name-pattern "*-plan-*"

# Multiple patterns (pipe-separated)
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --name-pattern "*-plan-*|*-specify-*|plan-*|manage-*"
```

### --bundles (optional)

Filter to specific bundles by name (comma-separated).

**Example**:
```bash
# Single bundle
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --bundles planning

# Multiple bundles
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory --bundles "planning,pm-dev-java,pm-dev-frontend"
```

### --direct-result (optional flag)

Output full TOON directly to stdout instead of writing to file.

| Mode | Behavior |
|------|----------|
| Default (no flag) | Writes to `.plan/temp/tools-marketplace-inventory/inventory-{timestamp}.toon`, prints summary |
| `--direct-result` | Outputs full TOON inventory directly to stdout |

**When to use `--direct-result`**:
- Small inventories (filtered bundles/patterns)
- Piped usage where file I/O is not desired
- Script-to-script calls where caller parses TOON directly

**Example**:
```bash
# Get full TOON directly (for small/filtered results)
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --bundles pm-workflow --direct-result
```

## Error Handling

If the script fails:
- Check that the working directory is the repository root
- Verify marketplace/bundles/ directory exists
- Ensure script has execute permissions

## Non-Prompting Requirements

This skill is designed to run without user prompts. Required permissions:

**Script Execution:**
- `Bash(bash:*)` - Bash interpreter
- Script permissions synced via `/tools-setup-project-permissions`

**Ensuring Non-Prompting:**
- Resolve script paths from `.plan/scripts-library.toon` (system convention)
- Script reads marketplace directory structure
- Writes inventory to `.plan/temp/` (covered by `Write(.plan/**)` permission)
- All output is TOON format

## References

- Script location: scripts/scan-marketplace-inventory.py
- Marketplace root: marketplace/bundles/
