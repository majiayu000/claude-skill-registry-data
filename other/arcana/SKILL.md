---
name: arcana
description: >
  Gateway skill for transforming and transporting Claude Code skills to other Claude surfaces.
  Routes to appropriate skill based on intent: export-zip for claude.ai, upload-api for Messages API.
  Trigger phrases: "export skill", "upload skill", "sync skill", "publish skill", "arcana".
user-invocable: true
---

# Arcana: Skill Transformation Gateway

Transform and transport Claude Code skills to other Claude surfaces.

## Path Convention

`{PLUGIN_ROOT}` = This plugin's root directory (where plugin.json lives)

## What This Does

Routes skill transformation requests to the appropriate handler:

| Intent | Skill | Target |
|--------|-------|--------|
| Export for claude.ai | `arcana-export-zip` | ZIP file for manual upload |
| Upload to API | `arcana-upload-api` | Messages API (workspace-wide) |
| Find skills | `arcana-discover` | List skills in a directory |

## Usage

When the user invokes this skill (e.g., `/arcana` or asks to export/upload a skill):

### Step 1: Determine Intent

Ask if not clear using AskUserQuestion:

**Question:** "What would you like to do?"

**Options:**
1. **Export for claude.ai** - Create ZIP for manual upload to claude.ai web
2. **Upload to API** - Upload directly to Messages API (workspace-wide)
3. **Discover skills** - Find and analyze skills in a directory

### Step 2: Get Target

If not provided, ask for the skill or directory to process:

**Question:** "What skill would you like to process?"

**Options:**
1. **Specify path** - Enter a path to a skill directory
2. **Current directory** - Look for skills in the current directory
3. **Installed plugin** - Choose from `~/.claude/plugins/`

### Step 3: Route to Handler

Based on intent, invoke the appropriate skill:

- **Export for claude.ai** → Read and follow `{PLUGIN_ROOT}/skills/arcana-export-zip/SKILL.md`
- **Upload to API** → Read and follow `{PLUGIN_ROOT}/skills/arcana-upload-api/SKILL.md`
- **Discover skills** → Read and follow `{PLUGIN_ROOT}/skills/arcana-discover/SKILL.md`

## Quick Commands

If the user provides clear intent, skip the questions:

| User Says | Action |
|-----------|--------|
| `/arcana export ~/my-skill` | Go directly to arcana-export-zip |
| `/arcana upload ~/my-skill` | Go directly to arcana-upload-api |
| `/arcana discover ~/my-plugin` | Go directly to arcana-discover |
| `/arcana ~/my-skill` | Ask about export vs upload |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `arcana-discover` | Find and analyze skills |
| `arcana-export-zip` | Export for claude.ai |
| `arcana-upload-api` | Upload to Messages API |
