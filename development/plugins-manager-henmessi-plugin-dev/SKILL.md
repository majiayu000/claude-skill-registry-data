---
name: plugins-manager
description: "Branch skill for building and improving plugins. Use when creating new plugins, validating plugin structure, adapting marketplace plugins, or improving existing plugins. Triggers: 'create plugin', 'improve plugin', 'validate plugin', 'fix plugin', 'plugin.json', 'adapt plugin', '4-plugin architecture', 'plugin structure', 'CLAUDE_PLUGIN_ROOT'."
---

# Plugins Manager - Branch of JARVIS-02

Build and improve plugins following the plugins-management policy.

## Policy Source

**Primary policy**: JARVIS-02 → `.claude/skills/plugins-management/SKILL.md`

This branch **executes** the policy defined by JARVIS-02. Always sync with Primary before major operations.

## Quick Decision Tree

```text
Task Received
    │
    ├── Create new plugin? ─────────────> Which type?
    │   ├── Task routing ────────────────> Use shared Orchestrator
    │   ├── Self-improvement ────────────> Use shared plugin-dev
    │   ├── Data access ─────────────────> Create BigQuery-[cat] from template
    │   └── Domain logic ────────────────> Create Category-[cat] custom
    │
    ├── Adapt marketplace plugin? ───────> Workflow 3: Adapt
    │
    ├── Fix existing plugin? ────────────> Workflow 2: Improve
    │
    └── Validate plugin? ────────────────> Validation Checklist
```

## Plugin Overview

Claude Code plugins follow a standardized directory structure with automatic component discovery.

**Key concepts:**
- Conventional directory layout for automatic discovery
- Manifest-driven configuration in `.claude-plugin/plugin.json`
- Component-based organization (commands, agents, skills, hooks)
- Portable path references using `${CLAUDE_PLUGIN_ROOT}`

## Directory Structure

Every Claude Code plugin follows this organizational pattern:

```text
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Slash commands (.md files)
├── agents/                   # Subagent definitions (.md files)
├── skills/                   # Agent skills (subdirectories)
│   └── skill-name/
│       └── SKILL.md         # Required for each skill
├── hooks/
│   ├── hooks.json           # Event handler configuration
│   └── scripts/             # Hook scripts
├── .mcp.json                # MCP server definitions
└── scripts/                 # Helper scripts and utilities
```

**Critical rules:**
1. **Manifest location**: The `plugin.json` MUST be in `.claude-plugin/` directory
2. **Component locations**: All component directories MUST be at plugin root level, NOT nested inside `.claude-plugin/`
3. **Optional components**: Only create directories for components the plugin actually uses
4. **Naming convention**: Use kebab-case for all directory and file names

## The 4-Plugin Architecture

Every JARVIS category has exactly 4 plugins:

| # | Plugin | Type | Source | Customization |
|---|--------|------|--------|---------------|
| 1 | Plugin-Orchestrator | Shared | github.com/henmessi/plugin-orchestrator | None - identical everywhere |
| 2 | plugin-dev | Shared | github.com/henmessi/plugin-dev | None - identical everywhere |
| 3 | Plugin-BigQuery-[Cat] | Template | Template from JARVIS-10 | Only table list changes |
| 4 | Plugin-Category-[Cat] | Custom | Created per category | Fully custom |

## Plugin Manifest (plugin.json)

Located at `.claude-plugin/plugin.json`:

### Required Fields

```json
{
  "name": "plugin-name"
}
```

**Name requirements:**
- Use kebab-case format (lowercase with hyphens)
- Must be unique across installed plugins
- No spaces or special characters

### Recommended Fields

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "repository": "https://github.com/user/plugin-name",
  "license": "MIT",
  "keywords": ["jarvis", "category-name"]
}
```

### Component Path Configuration

Specify custom paths for components:

```json
{
  "name": "plugin-name",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Path rules:**
- Must be relative to plugin root
- Must start with `./`
- Cannot use absolute paths
- Custom paths supplement defaults (don't replace)

## Portable Path References

### ${CLAUDE_PLUGIN_ROOT}

Use `${CLAUDE_PLUGIN_ROOT}` for all intra-plugin path references:

```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

**Where to use it:**
- Hook command paths
- MCP server command arguments
- Script execution references
- Resource file paths

**Never use:**
- Hardcoded absolute paths (`/Users/name/plugins/...`)
- Relative paths from working directory (`./scripts/...` in commands)
- Home directory shortcuts (`~/plugins/...`)

**In hook scripts:**

```bash
#!/bin/bash
# ${CLAUDE_PLUGIN_ROOT} available as environment variable
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

## Component Organization

### Commands

**Location**: `commands/` directory
**Format**: Markdown files with YAML frontmatter
**Auto-discovery**: All `.md` files in `commands/` load automatically

```text
commands/
├── review.md        # /review command
├── test.md          # /test command
└── deploy.md        # /deploy command
```

### Agents

**Location**: `agents/` directory
**Format**: Markdown files with YAML frontmatter
**Auto-discovery**: All `.md` files in `agents/` load automatically

```text
agents/
├── code-reviewer.md
├── test-generator.md
└── refactorer.md
```

### Skills

**Location**: `skills/` directory with subdirectories per skill
**Format**: Each skill in own directory with `SKILL.md` file
**Auto-discovery**: All `SKILL.md` files in skill subdirectories load automatically

```text
skills/
├── api-testing/
│   ├── SKILL.md
│   └── references/
└── database-migrations/
    ├── SKILL.md
    └── examples/
```

### Hooks

**Location**: `hooks/hooks.json` or inline in `plugin.json`
**Format**: JSON configuration defining event handlers

```text
hooks/
├── hooks.json           # Hook configuration
└── scripts/
    └── validate.sh      # Hook script
```

**Configuration format:**

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
        "timeout": 30
      }]
    }]
  }
}
```

### MCP Servers

**Location**: `.mcp.json` at plugin root
**Format**: JSON configuration for MCP server definitions

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## Auto-Discovery Mechanism

Claude Code automatically discovers and loads components:

1. **Plugin manifest**: Reads `.claude-plugin/plugin.json` when plugin enables
2. **Commands**: Scans `commands/` directory for `.md` files
3. **Agents**: Scans `agents/` directory for `.md` files
4. **Skills**: Scans `skills/` for subdirectories containing `SKILL.md`
5. **Hooks**: Loads configuration from `hooks/hooks.json` or manifest
6. **MCP servers**: Loads configuration from `.mcp.json` or manifest

**Discovery timing:**
- Plugin installation: Components register with Claude Code
- Plugin enable: Components become available for use
- No restart required for file changes (except hooks)

## File Naming Conventions

### Component Files

**Commands**: Use kebab-case `.md` files
- `code-review.md` → `/code-review`
- `run-tests.md` → `/run-tests`

**Agents**: Use kebab-case `.md` files
- `test-generator.md`
- `code-reviewer.md`

**Skills**: Use kebab-case directory names
- `api-testing/`
- `database-migrations/`

### Supporting Files

**Scripts**: Use descriptive kebab-case names
- `validate-input.sh`
- `generate-report.py`

**Configuration**: Use standard names
- `hooks.json`
- `.mcp.json`
- `plugin.json`

## Plugin Settings Pattern

Plugins can store user-configurable settings in `.claude/plugin-name.local.md`:

### Settings File Structure

```markdown
---
enabled: true
setting1: value1
setting2: value2
---

# Additional Context

This markdown body can contain:
- Task descriptions
- Additional instructions
- Prompts to feed back to Claude
```

### Reading Settings in Hooks

```bash
#!/bin/bash
STATE_FILE=".claude/my-plugin.local.md"

# Quick exit if file doesn't exist
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Plugin not configured
fi

# Parse YAML frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

# Extract field
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi
```

### Settings Best Practices

- Use `.claude/plugin-name.local.md` format
- Add `.claude/*.local.md` to `.gitignore`
- Provide sensible defaults when settings file doesn't exist
- Document that changes require Claude Code restart (for hooks)

## Workflow 1: Create New Plugin

### For Shared Plugins (Orchestrator, plugin-dev)

**Do NOT create new ones.** Copy from source repository:

```bash
# Copy shared plugin
cp -r /path/to/shared/plugin-orchestrator ./plugins/orchestrator
cp -r /path/to/shared/plugin-dev ./plugins/dev
```

### For BigQuery Plugin (Template)

1. **Copy template structure**

```bash
mkdir -p plugins/bigquery-[category]/.claude-plugin
mkdir -p plugins/bigquery-[category]/{agents,skills/bigquery-[category]}
```

2. **Create plugin.json**

```json
{
  "name": "plugin-bigquery-[category]",
  "version": "1.0.0",
  "description": "BigQuery data access for JARVIS-XX [Category]"
}
```

3. **Create BigQuery skill with HARDCODED tables**

```markdown
---
name: bigquery-[category]
description: "This skill provides BigQuery access for [Category]. Use when querying data, writing analytics, or accessing tables. Triggers: 'query', 'write data', 'analytics', 'BigQuery'."
---

# BigQuery - [Category]

## Allowed Tables (HARDCODED)

| Table | Access | Purpose |
|-------|--------|---------|
| jarvis_XX_table1 | READ/WRITE | [Purpose] |
| jarvis_XX_table2 | READ | [Purpose] |

## Query Patterns
[Standard patterns for this category]
```

### For Category Plugin (Custom)

1. **Create structure**

```bash
mkdir -p plugins/category-[name]/.claude-plugin
mkdir -p plugins/category-[name]/{agents,skills/[domain],commands,hooks/scripts}
```

2. **Create plugin.json**

```json
{
  "name": "plugin-category-[name]",
  "version": "1.0.0",
  "description": "Domain-specific plugin for [Category] operations"
}
```

3. **Add components using appropriate manager skills**
   - Agents → agents-manager
   - Skills → skills-manager
   - Commands → commands-manager
   - Hooks → hooks-manager

## Workflow 2: Improve Existing Plugin

### Step 1: Analyze Current State

```bash
# Plugin audit
cat plugins/[name]/.claude-plugin/plugin.json
ls -la plugins/[name]/agents/
ls -la plugins/[name]/skills/
ls -la plugins/[name]/commands/
ls -la plugins/[name]/hooks/
```

### Step 2: Gap Analysis

| Component | Check | Common Issues |
|-----------|-------|---------------|
| plugin.json | Valid? Complete? | Missing name, no description |
| Structure | .claude-plugin/ exists? | Manifest in wrong location |
| Paths | Uses ${CLAUDE_PLUGIN_ROOT}? | Hardcoded paths |
| agents/ | Valid frontmatter? | Missing examples in description |
| skills/ | SKILL.md in subdirs? | No references/, too long |
| commands/ | Valid frontmatter? | Written as message, not instructions |
| hooks/ | hooks.json valid? | Missing timeout, wrong exit codes |

### Step 3: Apply Fixes

Use the appropriate manager skill:
- Agent issues → agents-manager
- Skill issues → skills-manager
- Command issues → commands-manager
- Hook issues → hooks-manager

### Step 4: Validate

Run full validation checklist.

## Workflow 3: Adapt Marketplace Plugin

When taking a plugin from wshobson-agents, obra-superpowers, or other sources:

### Step 1: Analyze Source Plugin

```bash
ls -la source-plugin/
cat source-plugin/.claude-plugin/plugin.json
ls source-plugin/agents/
ls source-plugin/skills/
```

### Step 2: Determine Target Plugin Type

| Source Has | JARVIS Target |
|------------|---------------|
| Generic orchestration agents | Merge into Plugin-Orchestrator |
| Self-improvement skills | Merge into plugin-dev |
| Data/analytics focus | Merge into Plugin-BigQuery-[Cat] |
| Domain-specific content | Merge into Plugin-Category-[Cat] |

### Step 3: Adapt Components

**For each component:**
1. Read original file
2. Adapt for JARVIS (add triggers, context)
3. Use appropriate manager skill
4. Save to target plugin

### Step 4: Update plugin.json

```json
{
  "name": "plugin-category-[name]",
  "version": "1.0.0",
  "description": "Adapted from [source] - [purpose] for JARVIS-XX",
  "source": "[original repository]"
}
```

### Step 5: Validate Adaptation

Run full validation checklist.

## Validation Checklist

### Structure

- [ ] `.claude-plugin/plugin.json` exists (not at root)
- [ ] plugin.json has `name` field
- [ ] Name is kebab-case, 3-50 characters
- [ ] Component directories at plugin root (not in .claude-plugin/)
- [ ] All paths use `${CLAUDE_PLUGIN_ROOT}` for portability

### Agents (if any)

- [ ] Files in `agents/` with `.md` extension
- [ ] Each has valid YAML frontmatter
- [ ] Each has name, description, model, color
- [ ] Description has 2+ `<example>` blocks

### Skills (if any)

- [ ] Each skill in own subdirectory under `skills/`
- [ ] Each has SKILL.md with valid frontmatter
- [ ] Each has "Triggers:" in description
- [ ] Content under 2000 words

### Commands (if any)

- [ ] Files in `commands/` with `.md` extension
- [ ] Each has description in frontmatter
- [ ] Written as instructions FOR Claude
- [ ] Uses imperative form

### Hooks (if any)

- [ ] `hooks/hooks.json` is valid JSON
- [ ] Uses `{"hooks": {...}}` wrapper format
- [ ] Scripts in `hooks/scripts/` are executable
- [ ] Each hook has timeout specified
- [ ] Uses `${CLAUDE_PLUGIN_ROOT}` for script paths

### Type-Specific

- [ ] If shared plugin: identical to source
- [ ] If BigQuery: only table list differs from template
- [ ] If Category: domain-specific only, no generic content

## Plugin Templates

### Minimal Plugin

```text
plugin-name/
├── .claude-plugin/
│   └── plugin.json     <- {"name": "plugin-name"}
└── skills/
    └── [skill]/
        └── SKILL.md
```

### Full Plugin

```text
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── agent.md
├── skills/
│   └── domain/
│       ├── SKILL.md
│       └── references/
├── commands/
│   └── command.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── validate.sh
├── .mcp.json
└── scripts/
    └── utility.sh
```

## Common Issues & Fixes

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| No plugin.json | Missing manifest | Create in `.claude-plugin/` |
| Wrong manifest location | plugin.json at root | Move to `.claude-plugin/` |
| Invalid name | Spaces or uppercase | Use kebab-case |
| Hardcoded paths | `/home/user/...` in scripts | Use `${CLAUDE_PLUGIN_ROOT}` |
| Components not found | In `.claude-plugin/` | Move to plugin root |
| Wrong plugin type | Generic content in Category plugin | Move to correct plugin |

## Troubleshooting

**Component not loading:**
- Verify file is in correct directory
- Check YAML frontmatter syntax
- Ensure skill has `SKILL.md` (not README.md)
- Confirm plugin is enabled

**Path resolution errors:**
- Replace hardcoded paths with `${CLAUDE_PLUGIN_ROOT}`
- Verify paths start with `./` in manifest
- Test with `echo $CLAUDE_PLUGIN_ROOT` in hook scripts

**Auto-discovery not working:**
- Confirm directories are at plugin root
- Check file naming (kebab-case, correct extensions)
- Restart Claude Code

## When to Use This Skill

- User asks to create a new plugin
- User asks to validate plugin structure
- User asks to adapt a marketplace plugin
- User asks to fix plugin issues
- User asks about plugin.json or CLAUDE_PLUGIN_ROOT
- Setting up 4-plugin architecture for new category
- DEV-Manager detects plugin problems during improvement cycle
- Regular improvement cycle (~6 sessions)

## Sync Protocol

Before executing any workflow:

1. Read JARVIS-02's plugins-management SKILL.md
2. Check for policy updates
3. Apply current policy, not cached knowledge
