---
name: maceff-tree-awareness
description: USE *IMMEDIATELY* AFTER COMPACTION RECOVERY BEFORE REPORTING TO USER! Refresh structural awareness of MacEff repository to prevent assumption errors about file locations, package organization, and module structure. Also use after refactoring or when experiencing confusion about missing files.
---

# MacEff Tree Awareness Skill

## 🚨 CRITICAL: Post-Compaction Priority

**USE THIS SKILL IMMEDIATELY AFTER COMPACTION RECOVERY BEFORE REPORTING TO USER!**

After reading consciousness artifacts (reflection, checkpoint, roadmap), run this skill to restore structural awareness of the MacEff repository. This prevents assumption errors that lead to destructive actions.

## Purpose

This skill helps you avoid assumption errors about the MacEff repository structure by running targeted `tree` commands to reveal the actual organization.

## When to Invoke This Skill

**MANDATORY:**
- Immediately after compaction recovery (before reporting completion to user)

**Also invoke when you detect:**
- Confusion about where files/packages/modules are located
- Uncertainty about module import paths
- After major refactoring that changes directory structure
- Before making assumptions like "the functions should be in X"

**Key Lesson from Cycle 120**: User correction "Did you consider that the functions you are looking for might be under macf.utils.session?" prevented deletion of 10 valid tests. Tree awareness prevents destructive assumption errors.

## Commands to Execute

Run these commands **sequentially** (NOT in parallel - see prohibitions below).

### 0. Resolve MacEff Root (REQUIRED FIRST)

Before running tree commands, resolve the MacEff root path:

```bash
# Resolution order: git detection → env var → container default
MACEFF_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "${MACEFF_ROOT:-/opt/maceff}")"
echo "MacEff root: ${MACEFF_ROOT}"
```

**Resolution contexts**:
- **If run from MacEff directory**: Git detection finds root automatically
- **If MACEFF_ROOT env var set**: Uses that path
- **Container default**: Falls back to `/opt/maceff`

### 1. MacEff Root Structure (2 levels, filtered)
```bash
tree -L 2 -I '__pycache__|*.pyc|*.egg-info' "${MACEFF_ROOT}"
```

**Purpose**: Overview of main directories (docker/, framework/, macf/, maceff_tools/, tests/)

### 2. MACF Package Structure (3 levels, source only)
```bash
tree -L 3 -I '__pycache__|*.pyc|*.egg-info' "${MACEFF_ROOT}/macf/src/macf"
```

**Purpose**: Detailed view of package modules (cli.py, hooks/, utils/, models/, forensics/)

### 3. Framework Policies Structure
```bash
tree -L 3 "${MACEFF_ROOT}/framework"
```

**Purpose**: Policy files, subagent definitions, templates organization

## After Running Commands

**Report to user using this language:**
```
✅ MacEff structural awareness refreshed:
- Root structure: [X] directories identified
- MACF package: [Y] modules discovered
- Framework policies: [Z] policy sets located
```

Then:
1. **Integrate structural knowledge** - Update your mental model
2. **Note surprises** - Any unexpected structure or locations
3. **Verify assumptions** - Don't assume, check the tree output first
4. **Remember key patterns**:
   - `macf/src/macf/` contains actual package code
   - `macf/tests/` contains test specifications
   - `framework/` contains policies, subagents, templates
   - `maceff_tools/` contains shell scripts for container ops

## 🚨 CRITICAL PROHIBITIONS

When working with MacEff after using this skill:

**❌ NEVER use naked `cd` commands:**
- Not: `cd /path/to/dir`
- Not: `cd /path && command`
- Only allowed: `(cd /path && command)` in subshell if absolutely necessary
- **Preferred**: Use absolute paths in all commands

**❌ NEVER use concurrent tool calls carelessly:**
- Concurrent tool calls can cause API errors and session failures
- Sequential execution is safer when operations might conflict
- Only use concurrent calls when operations are proven independent

**Why these matter:**
- Naked `cd` triggers premature stopping and tool failure
- Concurrent tool calls can overwhelm API limits and corrupt state
- Both violations waste time and require user intervention

## Key Structural Patterns

**Module Locations**:
- CLI commands: `macf/src/macf/cli.py`
- Hook handlers: `macf/src/macf/hooks/handle_*.py`
- Utilities: `macf/src/macf/utils/*.py`
- Configuration: `macf/src/macf/config.py`

**Import Patterns**:
- From package: `from macf.utils.session import get_current_session_id`
- NOT: `from macf.session import ...` (doesn't exist as module)
- Session utils are in `macf/utils/session.py`, not `macf/session.py`

## Common Mistakes This Prevents

- Assuming `macf.session` module exists (it's `macf.utils.session`)
- Deleting tests because "functions don't exist" (verify module first)
- Wrong import paths in test files
- Confusion about where CLI commands are implemented
- Not knowing framework vs package boundaries
- Using naked `cd` commands (causes session failures)
- Running too many concurrent tool calls (API errors)

## Version History

- v1.1 (2025-12-01): Path portability fix - replaced hardcoded paths with git-aware detection + env var fallback (Cycle 194, Phase 2 of Path Portability DETOUR)
- v1.0 (2025-11-09): Initial skill creation - Cycle 121 learning from Cycle 120 user corrections, emphasizing post-compaction usage and prohibitions
