---
name: work-common
description: Common utilities for work plugin operations
model: claude-haiku-4-5
type: library
---

# Work Common Utilities

<CONTEXT>
You are the work-common utilities library providing shared helper functions for the work plugin. You are NOT invoked like other skills - instead, other skills and handlers call your scripts directly via Bash.

This library provides:
- Configuration loading and validation
- Data normalization across platforms (future)
- Input validation helpers (future)
- Standard error code definitions (future)
</CONTEXT>

<CRITICAL_RULES>
1. NEVER invoke this as a skill through work-manager
2. ALWAYS use these utilities as Bash scripts called directly
3. ALWAYS validate inputs in utility scripts
4. ALWAYS output structured data (JSON where applicable)
5. ALWAYS use standard error codes consistently
</CRITICAL_RULES>

<UTILITIES>

## config-loader.sh

**Purpose:** Load and validate work plugin configuration

**Location:** `plugins/work/skills/work-common/scripts/config-loader.sh`

**Usage:**
```bash
CONFIG_JSON=$(./plugins/work/skills/work-common/scripts/config-loader.sh) || exit $?
PLATFORM=$(echo "$CONFIG_JSON" | jq -r '.handlers["work-tracker"].active')
```

**Returns:** Full configuration JSON to stdout

**Exit Codes:**
- 0: Success - configuration loaded and valid
- 3: Validation error - config not found or invalid JSON

**CRITICAL**: Configuration must be loaded from the **project working directory**, NOT the plugin installation directory.

**Configuration Location:** `.fractary/plugins/work/config.json` (relative to project root / current working directory)

**Common Mistake:** Do NOT look in `~/.claude/plugins/marketplaces/fractary/plugins/work/` - that's the plugin installation directory, not the project config location.

**Special Behavior:** When config doesn't exist, the work plugin uses auto-detection (e.g., gh CLI automatically detects the repository). Skills can check if config exists and recommend running `/work:init` to persist settings.

**Example:**
```bash
# Load configuration
if ! CONFIG_JSON=$(./plugins/work/skills/work-common/scripts/config-loader.sh 2>&1); then
    echo "Error: Failed to load configuration" >&2
    exit 3
fi

# Extract platform-specific settings
PLATFORM=$(echo "$CONFIG_JSON" | jq -r '.handlers["work-tracker"].active')
GITHUB_OWNER=$(echo "$CONFIG_JSON" | jq -r '.handlers["work-tracker"].github.owner')
GITHUB_REPO=$(echo "$CONFIG_JSON" | jq -r '.handlers["work-tracker"].github.repo')
```

## check-config-exists.sh

**Purpose:** Check if work plugin configuration file exists

**Location:** `plugins/work/skills/work-common/scripts/check-config-exists.sh`

**Usage:**
```bash
if [ -f ".fractary/plugins/work/config.json" ]; then
    # Config exists
else
    # Show recommendation to run /work:init
fi
```

**Returns:** Exit code 0 if config exists, 1 if not

**Use Case:** Skills can check config existence and include init recommendation in completion messages when config doesn't exist.

## normalize-issue.sh (FUTURE)

**Purpose:** Normalize platform-specific issue JSON to universal format

**Status:** Not yet implemented - placeholder for Phase 5+

**Planned Usage:**
```bash
NORMALIZED=$(./plugins/work/skills/work-common/scripts/normalize-issue.sh "$PLATFORM" "$ISSUE_JSON")
```

## validate-issue-id.sh (FUTURE)

**Purpose:** Validate issue ID format for specific platform

**Status:** Not yet implemented - placeholder for Phase 5+

**Planned Usage:**
```bash
./plugins/work/skills/work-common/scripts/validate-issue-id.sh "github" "123"
```

## error-codes.sh (FUTURE)

**Purpose:** Centralized error code definitions and lookup

**Status:** Not yet implemented - placeholder for Phase 5+

**Planned Usage:**
```bash
source ./plugins/work/skills/work-common/scripts/error-codes.sh
exit $ERR_NOT_FOUND
```

</UTILITIES>

<ERROR_CODES>

Standard error codes used across all work plugin utilities:

- **0** - Success
- **1** - General error
- **2** - Invalid arguments
- **3** - Validation error (config, input format)
- **10** - Resource not found (issue, milestone, etc.)
- **11** - Authentication error
- **12** - Network error

</ERROR_CODES>

## Dependencies

- `jq` - JSON processing
- `bash` 4.0+ - Shell features
- Platform-specific CLIs:
  - `gh` for GitHub
  - `jira` for Jira
  - `linear` for Linear

## Configuration Structure

**CRITICAL**: Configuration must be loaded from the **project working directory**, NOT the plugin installation directory.

Expected configuration file at `.fractary/plugins/work/config.json` (relative to project root / current working directory):

```json
{
  "version": "2.0",
  "project": {
    "issue_system": "github",
    "repository": "owner/repo"
  },
  "handlers": {
    "work-tracker": {
      "active": "github",
      "github": {
        "owner": "myorg",
        "repo": "my-project",
        "api_url": "https://api.github.com"
      }
    }
  }
}
```

See `plugins/work/config/config.example.json` for complete configuration template.

## Testing

### Test config-loader.sh

```bash
# Test successful load
cd /mnt/c/GitHub/fractary/claude-plugins
./plugins/work/skills/work-common/scripts/config-loader.sh
# Expected: Outputs valid JSON configuration

# Test missing config
mv .fractary/plugins/work/config.json .fractary/plugins/work/config.json.bak
./plugins/work/skills/work-common/scripts/config-loader.sh
# Expected: Exit code 3, error message "Configuration file not found"

# Test invalid JSON
echo "{ invalid json" > .fractary/plugins/work/config.json
./plugins/work/skills/work-common/scripts/config-loader.sh
# Expected: Exit code 3, error message "Invalid JSON"
```

## Integration

Other skills and handlers integrate work-common utilities like this:

```bash
#!/bin/bash
# Example handler script

set -euo pipefail

# Load configuration using work-common utility
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_COMMON_DIR="$SCRIPT_DIR/../../work-common/scripts"

CONFIG_JSON=$("$WORK_COMMON_DIR/config-loader.sh") || exit $?

# Extract configuration values
PLATFORM=$(echo "$CONFIG_JSON" | jq -r '.handlers["work-tracker"].active')

# Continue with operation...
```

## Future Enhancements

- **normalize-issue.sh** - Standardize issue data across GitHub, Jira, Linear
- **validate-issue-id.sh** - Platform-specific ID format validation
- **error-codes.sh** - Shared error code constants
- **cache-helper.sh** - Optional caching for repeated API calls
- **auth-checker.sh** - Verify platform authentication before operations
