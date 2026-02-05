---
name: gemini-memory-sync
description: Synchronization patterns for CLAUDE.md and GEMINI.md memory files. Covers import syntax, drift detection, and one-way sync. Use when setting up GEMINI.md, detecting context drift between memory files, understanding @import syntax, or troubleshooting sync issues.
allowed-tools: Read, Glob, Grep, Bash
---

# Gemini Memory Sync

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini memory/memport:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific memory or import topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

This skill provides patterns for keeping Claude Code (`CLAUDE.md`) and Gemini CLI (`GEMINI.md`) memory files synchronized. The core principle is **CLAUDE.md as source of truth** with GEMINI.md importing and adding overrides.

## When to Use This Skill

**Keywords:** sync memory, sync context, claude.md gemini.md, memory import, context drift, @import, memport

**Use this skill when:**

- Setting up GEMINI.md for a new project
- Detecting drift between memory files
- Understanding the import syntax
- Troubleshooting sync issues

## Core Principle: Single Source of Truth

```text
CLAUDE.md (Source of Truth)
    │
    │ @import
    ▼
GEMINI.md (Imports + Overrides)
```

**Why CLAUDE.md is the source:**

- Claude Code is the primary development environment
- CLAUDE.md is already established in most projects
- Single point of update reduces maintenance burden
- Git history shows context evolution in one place

## GEMINI.md Structure

### Recommended Template

```markdown
# GEMINI.md

@CLAUDE.md

## Gemini-Specific Overrides

You are Gemini CLI. Your unique capabilities:
- Large context window (Flash) / Very large (Pro)
- Interactive PTY shell (vim, git rebase -i, htop)
- Checkpointing with instant rollback
- Policy engine for tool control
- Native Google Cloud authentication

### When to Use Your Strengths

- **Bulk analysis**: Use your large context for codebase-wide exploration
- **Interactive tools**: Handle vim, git interactive commands
- **Risky operations**: Use sandbox and checkpointing
- **Second opinions**: Provide independent validation

### Model Selection

- Use **Flash** for bulk analysis and simple tasks
- Use **Pro** for complex reasoning and very large contexts
```

### Import Syntax

Gemini CLI uses `@` prefix for imports (memport):

```markdown
# Import entire file
@CLAUDE.md

# Import relative path
@./docs/conventions.md

# Import from parent
@../shared/COMMON.md
```

**Note:** Unlike CLAUDE.md's flexible import, GEMINI.md's memport has:

- Maximum import depth: 5 levels
- Circular import detection
- File access validation

## Drift Detection

### Manual Detection

```bash
# Quick diff (ignoring Gemini-specific sections)
diff <(grep -v "^## Gemini-Specific" CLAUDE.md) <(grep -v "^## Gemini-Specific\|^@" GEMINI.md)
```

### Hash-Based Detection

```bash
# Store hash of CLAUDE.md
claude_hash=$(md5sum CLAUDE.md | cut -d' ' -f1)

# Store in sync state
echo "{\"claude_hash\": \"$claude_hash\", \"last_sync\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > .claude/temp/sync-state.json
```

### Check for Drift

```bash
# Compare current hash to stored
current_hash=$(md5sum CLAUDE.md | cut -d' ' -f1)
stored_hash=$(cat .claude/temp/sync-state.json 2>/dev/null | jq -r '.claude_hash // ""')

if [ "$current_hash" != "$stored_hash" ]; then
  echo "CLAUDE.md has changed since last sync"
fi
```

## Sync Patterns

### Pattern 1: Import-Based (Recommended)

GEMINI.md simply imports CLAUDE.md - no sync needed:

```markdown
# GEMINI.md
@CLAUDE.md

## Gemini-Specific
{overrides here}
```

**Pros:**

- No sync maintenance
- Always up-to-date
- Single source of truth enforced

**Cons:**

- GEMINI.md must start with @import
- Can't selectively import sections

### Pattern 2: Section-Based Sync

Copy specific sections from CLAUDE.md:

```bash
# Extract specific sections
conventions=$(sed -n '/^## Conventions/,/^## /p' CLAUDE.md | head -n -1)
build_commands=$(sed -n '/^## Build/,/^## /p' CLAUDE.md | head -n -1)

# Rebuild GEMINI.md
cat > GEMINI.md << EOF
# GEMINI.md

## Conventions (synced from CLAUDE.md)
$conventions

## Build Commands (synced from CLAUDE.md)
$build_commands

## Gemini-Specific Overrides
{your overrides}
EOF
```

**Pros:**

- Selective control
- Can transform content

**Cons:**

- Requires manual sync
- Can drift easily

### Pattern 3: Template Generation

Generate GEMINI.md from CLAUDE.md with transformations:

```bash
# Transform CLAUDE.md to GEMINI.md
cat CLAUDE.md | \
  sed 's/Claude Code/Gemini CLI/g' | \
  sed 's/claude/gemini/g' > GEMINI.md

# Append Gemini-specific section
cat >> GEMINI.md << 'EOF'

## Gemini-Specific Overrides
{overrides}
EOF
```

## Common Issues

### Issue: Import Not Working

**Symptom:** Gemini doesn't see CLAUDE.md content

**Fix:** Ensure correct path syntax

```markdown
# Correct
@CLAUDE.md
@./CLAUDE.md

# Incorrect
@/CLAUDE.md  (absolute paths may fail)
```

### Issue: Circular Import

**Symptom:** Error about circular references

**Fix:** Don't have CLAUDE.md import GEMINI.md

### Issue: Import Depth Exceeded

**Symptom:** Nested imports not loading

**Fix:** Memport has max depth of 5. Flatten import chain.

### Issue: Context Drift

**Symptom:** Gemini behaves differently than Claude

**Fix:**

1. Use `/sync-context` command
2. Or rebuild GEMINI.md with @import pattern

## Best Practices

### 1. Use @Import Pattern

Always prefer import over copy:

```markdown
# GEMINI.md - Good
@CLAUDE.md

## Gemini-Specific
...
```

### 2. Keep Overrides Minimal

Only override what's truly Gemini-specific:

- Model selection guidance
- Interactive shell instructions
- Sandbox usage patterns

### 3. Document What's Synced

If using section-based sync, note the source:

```markdown
## Conventions (synced from CLAUDE.md on 2025-11-30)
```

### 4. Validate After Sync

Test that Gemini understands the context:

```bash
gemini "What are the project conventions?" --output-format json
```

### 5. Regular Drift Checks

Include in CI or pre-commit:

```bash
# In CI
./scripts/check-memory-drift.sh
```

## Sync Workflow

### Initial Setup

```bash
# 1. Ensure CLAUDE.md exists
if [ ! -f "CLAUDE.md" ]; then
  echo "CLAUDE.md not found. Create it first."
  exit 1
fi

# 2. Create GEMINI.md with import
cat > GEMINI.md << 'EOF'
# GEMINI.md

@CLAUDE.md

## Gemini-Specific Overrides

You are Gemini CLI with unique capabilities:
- Large context window (exceeds typical LLM limits)
- Interactive PTY shell
- Checkpointing with rollback
- Policy engine

Prioritize tasks that leverage these strengths.
EOF

# 3. Initialize sync state
mkdir -p .claude/temp
echo "{\"claude_hash\": \"$(md5sum CLAUDE.md | cut -d' ' -f1)\", \"last_sync\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > .claude/temp/sync-state.json

echo "GEMINI.md created with @import to CLAUDE.md"
```

### Manual Sync

```bash
# Check if sync needed
if [ "$(md5sum CLAUDE.md | cut -d' ' -f1)" != "$(cat .claude/temp/sync-state.json | jq -r '.claude_hash')" ]; then
  echo "CLAUDE.md has changed. If using @import, no action needed."
  echo "If using section-based sync, rebuild GEMINI.md sections."

  # Update sync state
  echo "{\"claude_hash\": \"$(md5sum CLAUDE.md | cut -d' ' -f1)\", \"last_sync\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > .claude/temp/sync-state.json
fi
```

## Related Skills

- `gemini-workspace-bridge` - Overall workspace architecture
- `gemini-context-bridge` - Legacy context sharing

## Related Commands

- `/sync-context` - Trigger manual sync check

## Test Scenarios

### Scenario 1: Initial Setup

**Query**: "How do I set up GEMINI.md to use CLAUDE.md?"
**Expected Behavior**:

- Skill activates on "sync memory" or "claude.md gemini.md"
- Provides @import syntax and template
**Success Criteria**: User receives working GEMINI.md template with @CLAUDE.md import

### Scenario 2: Drift Detection

**Query**: "How do I check if my memory files are out of sync?"
**Expected Behavior**:

- Skill activates on "context drift" or "sync"
- Provides hash-based detection method
**Success Criteria**: User receives drift detection script

### Scenario 3: Import Issues

**Query**: "My GEMINI.md @import isn't working"
**Expected Behavior**:

- Skill activates on "import" troubleshooting
- Provides common issues and fixes
**Success Criteria**: User receives troubleshooting steps for path syntax

## Version History

- v1.1.0 (2025-12-01): Added MANDATORY section, Test Scenarios, Version History
- v1.0.0 (2025-11-25): Initial release
