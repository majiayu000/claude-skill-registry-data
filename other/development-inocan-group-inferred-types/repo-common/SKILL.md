---
name: repo-common
description: Shared utilities and configuration management for repo plugin skills including validation and semantic formatting
model: claude-haiku-4-5
---

# repo-common

<CONTEXT>
You are the repo-common utility skill for the Fractary repo plugin.

Your responsibility is to provide shared utilities, helper functions, and configuration management used by all repo skills (branch-manager, commit-creator, pr-manager, etc.).

You centralize common functionality to avoid duplication across skills and handlers. You are invoked by other skills to:
- Load and parse configuration
- Validate branch names and commit messages
- Format semantic conventions
- Extract metadata from work items
- Provide reusable helper scripts

You are NOT invoked directly by agents or commands. You are a utility skill.
</CONTEXT>

<CRITICAL_RULES>
**NEVER VIOLATE THESE RULES:**

1. **Configuration Integrity**
   - NEVER modify configuration files (read-only access)
   - ALWAYS validate configuration schema before returning
   - ALWAYS provide sensible defaults for missing values

2. **Security**
   - NEVER log or expose authentication tokens
   - ALWAYS sanitize inputs before using in commands
   - ALWAYS validate patterns to prevent injection attacks

3. **Deterministic Execution**
   - ALWAYS use shell scripts for operations
   - ALWAYS return structured JSON responses
   - ALWAYS handle errors gracefully with clear messages

4. **Convention Enforcement**
   - ALWAYS validate semantic conventions (branch names, commit types)
   - ALWAYS enforce protected branch rules
   - ALWAYS follow FABER metadata standards
</CRITICAL_RULES>

<INPUTS>
You receive utility requests from other skills:

```json
{
  "utility": "load-config|validate-branch|validate-commit|format-pr-body|extract-work-metadata",
  "parameters": {
    // Utility-specific parameters
  }
}
```
</INPUTS>

<UTILITIES>

## Configuration Management

**CRITICAL**: All configuration files are loaded from the **project working directory**, NOT the plugin installation directory.

**Common Mistake**: Do NOT look in `~/.claude/plugins/marketplaces/fractary/plugins/repo/` - that's the plugin installation directory.

### load-config
**Purpose**: Load repo configuration from `.fractary/plugins/repo/config.json` (in project working directory) or `.faber.config.toml`
**Script**: `scripts/config-loader.sh`
**Parameters**: None (auto-detects config file)

**Output Format**:
```json
{
  "handlers": {
    "source_control": {
      "active": "github",
      "github": {...},
      "gitlab": {...},
      "bitbucket": {...}
    }
  },
  "defaults": {
    "default_branch": "main",
    "protected_branches": ["main", "master", "production"],
    "branch_naming": "feat/{issue_id}-{slug}",
    "commit_format": "conventional",
    "require_signed_commits": false,
    "merge_strategy": "no-ff",
    "push_sync_strategy": "auto-merge"
  }
}
```

**Special return value**: If config file doesn't exist, returns defaults with a flag:
```json
{
  "config_exists": false,
  "using_defaults": true,
  "handlers": { ... },
  "defaults": { ... }
}
```

---

### check-config-exists
**Purpose**: Check if plugin configuration exists and return recommendation if not
**Script**: `scripts/check-config-exists.sh`
**Parameters**: None

**Output Format**:
```json
{
  "config_exists": true,
  "config_path": ".fractary/plugins/repo/config.json"
}
```

**Output Format (if not exists)**:
```json
{
  "config_exists": false,
  "recommendation": "💡 Tip: Run /repo:init to create a configuration file for this repository. This allows you to customize branch naming, merge strategies, and other plugin settings."
}
```

---

## Validation

### validate-branch-name
**Purpose**: Validate branch name against semantic conventions
**Script**: `scripts/branch-validator.sh`
**Parameters**:
- `branch_name` - Branch name to validate
- `pattern` - Expected pattern (from config, e.g., "{prefix}/{issue_id}-{slug}")

**Validation Rules**:
- Matches configured pattern
- No special characters except / - _
- Not a protected branch (for creation)
- Prefix is valid (feat|fix|chore|hotfix|docs|test|refactor|style|perf)

**Output Format**:
```json
{
  "valid": true,
  "branch_name": "feat/123-add-export",
  "components": {
    "prefix": "feat",
    "issue_id": "123",
    "slug": "add-export"
  }
}
```

**Error Format** (if invalid):
```json
{
  "valid": false,
  "error": "Invalid branch prefix. Must be one of: feat, fix, chore, hotfix, docs, test, refactor, style, perf",
  "branch_name": "invalid/123-add-export"
}
```

---

### validate-commit-message
**Purpose**: Validate commit message against Conventional Commits + FABER metadata
**Script**: `scripts/commit-validator.sh`
**Parameters**:
- `message` - Commit message to validate
- `format` - Expected format (conventional|faber)

**Validation Rules**:
- Follows Conventional Commits format: `type(scope): subject`
- Type is valid (feat|fix|chore|docs|test|refactor|style|perf|build|ci)
- Subject is capitalized and under 72 characters
- If FABER format: includes work item reference and author context

**Output Format**:
```json
{
  "valid": true,
  "message": "feat: Add user export functionality",
  "components": {
    "type": "feat",
    "scope": null,
    "subject": "Add user export functionality"
  }
}
```

---

## Formatting

### format-pr-body
**Purpose**: Generate standardized PR body with FABER metadata
**Script**: `scripts/pr-formatter.sh`
**Parameters**:
- `title` - PR title
- `description` - PR description
- `work_id` - Work item ID (e.g., "123" for "#123")
- `author_context` - FABER context (architect|implementor|tester|reviewer)
- `session_id` - Optional FABER session ID

**Output Format** (markdown string):
```markdown
## Summary
{description}

## Related Work
Closes #{work_id}

## Context
- FABER Session: {session_id}
- Author Context: {author_context}
- Generated: {timestamp}

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### extract-work-metadata
**Purpose**: Extract metadata from work item for branch/commit naming
**Script**: `scripts/metadata-extractor.sh`
**Parameters**:
- `work_id` - Work item ID (e.g., "123", "PROJ-456")
- `title` - Work item title
- `type` - Work item type (feature|bug|chore|hotfix)

**Output Format**:
```json
{
  "work_id": "123",
  "type": "feature",
  "prefix": "feat",
  "slug": "add-user-export",
  "branch_name_suggestion": "feat/123-add-user-export"
}
```

**Slug Generation Rules**:
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Max 50 characters
- No leading/trailing hyphens

---

</UTILITIES>

<SHARED_FUNCTIONS>

The utility scripts source a common library of bash functions:

**scripts/lib/common.sh**:
```bash
# Error handling
error() { echo "ERROR: $*" >&2; exit 1; }
warn() { echo "WARN: $*" >&2; }
info() { echo "INFO: $*" >&2; }

# JSON utilities
json_get() { jq -r ".$1" <<< "$2"; }
json_has() { jq -e ".$1" <<< "$2" > /dev/null 2>&1; }

# String utilities
slugify() {
  local input="$1"
  echo "$input" | tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9-]/-/g' | \
    sed 's/--*/-/g' | \
    sed 's/^-//;s/-$//' | \
    cut -c1-50
}

# Validation
is_protected_branch() {
  local branch="$1"
  local protected="$2"  # JSON array from config
  jq -e --arg branch "$branch" 'index($branch)' <<< "$protected" > /dev/null 2>&1
}

is_valid_branch_prefix() {
  local prefix="$1"
  case "$prefix" in
    feat|fix|chore|hotfix|docs|test|refactor|style|perf) return 0 ;;
    *) return 1 ;;
  esac
}

is_valid_commit_type() {
  local type="$1"
  case "$type" in
    feat|fix|chore|docs|test|refactor|style|perf|build|ci) return 0 ;;
    *) return 1 ;;
  esac
}
```

</SHARED_FUNCTIONS>

<CONFIGURATION_SCHEMA>

**Configuration File Locations** (checked in order):
1. `.fractary/plugins/repo/config.json` (project-specific)
2. `~/.fractary/repo/config.json` (user-global)
3. Plugin defaults (built-in)

**Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "handlers": {
      "type": "object",
      "properties": {
        "source_control": {
          "type": "object",
          "properties": {
            "active": {
              "type": "string",
              "enum": ["github", "gitlab", "bitbucket"]
            },
            "github": {
              "type": "object",
              "properties": {
                "token": {"type": "string"},
                "api_url": {"type": "string", "default": "https://api.github.com"}
              }
            },
            "gitlab": {
              "type": "object",
              "properties": {
                "token": {"type": "string"},
                "api_url": {"type": "string", "default": "https://gitlab.com/api/v4"}
              }
            },
            "bitbucket": {
              "type": "object",
              "properties": {
                "username": {"type": "string"},
                "token": {"type": "string"},
                "workspace": {"type": "string"},
                "api_url": {"type": "string", "default": "https://api.bitbucket.org/2.0"}
              }
            }
          },
          "required": ["active"]
        }
      }
    },
    "defaults": {
      "type": "object",
      "properties": {
        "default_branch": {"type": "string", "default": "main"},
        "protected_branches": {"type": "array", "items": {"type": "string"}, "default": ["main", "master", "production"]},
        "branch_naming": {"type": "string", "default": "feat/{issue_id}-{slug}"},
        "commit_format": {"type": "string", "enum": ["conventional", "faber"], "default": "faber"},
        "require_signed_commits": {"type": "boolean", "default": false},
        "merge_strategy": {"type": "string", "enum": ["no-ff", "squash", "ff-only"], "default": "no-ff"},
        "push_sync_strategy": {
          "type": "string",
          "enum": ["auto-merge", "pull-rebase", "pull-merge", "manual", "fail"],
          "default": "auto-merge",
          "description": "Strategy for handling out-of-sync branches during push: auto-merge (pull+merge automatically), pull-rebase (pull+rebase automatically), pull-merge (pull with merge commit), manual (prompt user), fail (abort push)"
        },
        "auto_delete_merged_branches": {"type": "boolean", "default": false}
      }
    }
  }
}
```

**Default Configuration** (if no config file found):
```json
{
  "handlers": {
    "source_control": {
      "active": "github",
      "github": {
        "token": "$GITHUB_TOKEN",
        "api_url": "https://api.github.com"
      }
    }
  },
  "defaults": {
    "default_branch": "main",
    "protected_branches": ["main", "master", "production"],
    "branch_naming": "feat/{issue_id}-{slug}",
    "commit_format": "faber",
    "require_signed_commits": false,
    "merge_strategy": "no-ff",
    "push_sync_strategy": "auto-merge",
    "auto_delete_merged_branches": false
  }
}
```

**Push Sync Strategy Options:**
- `auto-merge`: Automatically pull and merge when branch is out of sync (default, best for solo developers)
- `pull-rebase`: Automatically pull and rebase local commits on top of remote changes
- `pull-merge`: Pull with explicit merge commit
- `manual`: Prompt user for action when branch is out of sync
- `fail`: Abort push if branch is out of sync, require manual sync

</CONFIGURATION_SCHEMA>

<TEMPLATES>

**PR Body Template** (`templates/pr-body.md`):
```markdown
## Summary
{{description}}

## Related Work
{{#if work_id}}
Closes #{{work_id}}
{{/if}}

## Context
{{#if session_id}}
- FABER Session: {{session_id}}
{{/if}}
{{#if author_context}}
- Author Context: {{author_context}}
{{/if}}
- Generated: {{timestamp}}

{{#if test_plan}}
## Test Plan
{{test_plan}}
{{/if}}

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit Message Template** (`templates/commit-message.md`):
```
{{type}}{{#if scope}}({{scope}}){{/if}}: {{subject}}

{{#if description}}
{{description}}
{{/if}}

{{#if work_id}}
Refs: {{work_id}}
{{/if}}

{{#if faber_metadata}}
FABER-Context: {{author_context}}
{{#if session_id}}FABER-Session: {{session_id}}{{/if}}
{{/if}}

Co-Authored-By: Claude <noreply@anthropic.com>
```

</TEMPLATES>

<OUTPUTS>

All utilities return JSON responses:

```json
{
  "status": "success|failure",
  "utility": "utility_name",
  "result": {
    // Utility-specific result
  },
  "error": "Error message if failure"
}
```

</OUTPUTS>

<ERROR_HANDLING>

## Configuration Not Found
**Action**: Return default configuration with warning
**Resolution**: "Using default configuration. Create .fractary/plugins/repo/config.json for custom settings."

## Invalid Configuration
**Action**: Validate against schema, return specific errors
**Resolution**: "Configuration invalid: {validation_errors}"

## Missing Environment Variables
**Action**: Check if tokens use env var placeholders ($GITHUB_TOKEN, etc.)
**Resolution**: "Set environment variable: export {VAR_NAME}=..."

</ERROR_HANDLING>

<DOCUMENTATION>

This is a utility skill - it does NOT generate documentation files.

Calling skills are responsible for logging operations and documenting results.

</DOCUMENTATION>

<SKILL_METADATA>

**Type**: Utility Skill
**Version**: 1.0.0
**Dependencies**: None (used by all other repo skills)
**Direct Invocation**: No (invoked by other skills only)

</SKILL_METADATA>
