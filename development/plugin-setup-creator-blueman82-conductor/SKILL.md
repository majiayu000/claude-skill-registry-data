---
name: plugin-setup-creator
description: Create a shareable Claude Code plugin package containing your commands, hooks, output styles, status lines, and agents. Use when you want to package and distribute your Claude Code customizations, create team plugins, or export your personal setup.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

# Plugin Setup Creator

**Version:** 1.0.0
**Last Updated:** 2025-11-10

## Purpose

This skill helps you create a complete, shareable Claude Code plugin that packages your personal setup including:
- Custom slash commands
- Event hooks and automation scripts
- Output style configurations
- Status line templates
- Specialized subagents/AI assistants
- Comprehensive plugin manifest and documentation

The generated plugin can be immediately shared with team members or published to community marketplaces.

## Instructions

### Phase 1: Discovery and Assessment

1. **Ask the user about their setup**
   - What custom commands do they have?
   - What hooks and automations are configured?
   - Do they use custom output styles?
   - What status line configurations exist?
   - What specialized agents/subagents have they created?
   - What's the intended audience (personal, team, public)?

2. **Verify existing configurations**
   - Check `~/.claude/commands/` for custom slash commands
   - Check `~/.claude/hooks/` for hook configurations
   - Check `~/.claude/output-styles/` for output style definitions
   - Check `~/.claude/status-lines/` for status line configs
   - Check `~/.claude/agents/` for subagent definitions
   - Review `.claude/settings.json` for project-level configurations

3. **Assess plugin metadata needs**
   - Plugin name (kebab-case, max 64 chars)
   - Description and purpose
   - Author information
   - License
   - Target audience and use cases

### Phase 2: Plugin Structure Creation

1. **Create plugin directory structure**
   ```
   plugin-name/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── commands/
   │   └── [custom commands]
   ├── agents/
   │   └── [subagent definitions]
   ├── hooks/
   │   ├── hooks.json
   │   └── scripts/
   ├── output-styles/
   │   └── [style configs]
   ├── status-lines/
   │   └── [status line configs]
   ├── README.md
   ├── LICENSE
   └── INSTALLATION.md
   ```

2. **Organize components**
   - Copy commands from `~/.claude/commands/` to `commands/`
   - Extract hooks configuration into `hooks/hooks.json`
   - Copy output style files to `output-styles/`
   - Copy status line configs to `status-lines/`
   - Convert agents to proper subagent format in `agents/`

3. **Create central plugin.json manifest**
   - Name: Use provided plugin name
   - Version: Start with 1.0.0
   - Description: Clear explanation with trigger keywords
   - Author: User information
   - Keywords: For marketplace discovery
   - Reference paths for all components

4. **Generate supporting documentation**
   - README.md: Overview and installation instructions
   - INSTALLATION.md: Step-by-step setup guide
   - COMPONENTS.md: Detail what each component does
   - USAGE.md: Examples and common workflows

### Phase 3: Component Validation

1. **Validate all files**
   - Check JSON syntax (plugin.json, hooks.json)
   - Verify markdown frontmatter in commands
   - Ensure relative paths (start with `./`)
   - Confirm no sensitive data (credentials, tokens)

2. **Verify directory structure**
   - All components at plugin root (not in .claude-plugin/)
   - Proper nesting (commands/*, agents/*, etc.)
   - Supporting files organized logically

3. **Test references**
   - Validate all file paths in hooks.json
   - Check command and agent paths
   - Verify output style references

### Phase 4: Distribution Preparation

1. **Create git repository**
   - Initialize git in plugin directory
   - Create .gitignore for sensitive files
   - Make initial commit

2. **Generate marketplace manifest** (optional)
   - Create `.claude-plugin/marketplace.json` if creating a marketplace
   - Define plugin entry with version info
   - Set category and metadata

3. **Create sharing documentation**
   - Installation instructions for recipients
   - Quick start guide
   - Troubleshooting section
   - Update/maintenance guidelines

### Phase 5: Testing and Finalization

1. **Local testing workflow**
   - Test marketplace setup locally
   - Install plugin from local path
   - Verify all components work
   - Check command invocation
   - Confirm hooks trigger properly
   - Test agent activation

2. **Generate plugin summary**
   - List all included commands
   - Document all hooks
   - Describe output styles
   - Detail status line configs
   - List agents/subagents

3. **Create deployment guide**
   - GitHub setup instructions
   - Marketplace submission process
   - Team distribution method
   - Version management approach

## Examples

### Example 1: Personal Productivity Plugin

**User Request:** "Package my custom commands and hooks into a shareable plugin"

**Skill Actions:**
1. Discovers existing commands: `/review`, `/commit`, `/doc`, `/test`
2. Finds hooks configuration for auto-formatting and linting
3. Creates `my-productivity-plugin/` structure
4. Generates comprehensive plugin.json
5. Creates README with installation instructions
6. Tests locally via dev marketplace
7. Provides GitHub setup guide

**Output:** Complete, tested plugin ready for team sharing or publication

### Example 2: Team AI Agents Plugin

**User Request:** "Create a plugin from my specialized subagents for code review and testing"

**Skill Actions:**
1. Identifies custom agents: `security-reviewer`, `test-generator`
2. Converts to proper subagent format
3. Creates plugin with bundled agents
4. Generates agent documentation
5. Creates example invocation commands
6. Sets up marketplace manifest for team distribution

**Output:** Plugin with ready-to-use specialized agents

### Example 3: Complete Setup Export

**User Request:** "Export my entire Claude Code setup as a plugin with all my customizations"

**Skill Actions:**
1. Discovers all commands, hooks, styles, status lines, and agents
2. Creates comprehensive plugin structure
3. Organizes components logically
4. Generates complete documentation
5. Creates setup.sh for easy installation
6. Tests all components together
7. Provides sharing and version management guide

**Output:** Complete, production-ready plugin of entire setup

## Key Features

### Automatic Discovery
- Scans existing Claude Code directories for customizations
- Identifies all commands, hooks, output styles, and agents
- Preserves configuration and functionality

### Smart Organization
- Proper directory structure for marketplace compatibility
- Component references in plugin.json
- Relative path handling

### Comprehensive Documentation
- README for overview
- INSTALLATION.md for setup
- COMPONENTS.md for detailed descriptions
- USAGE.md with examples

### Built-in Testing
- Validates all JSON syntax
- Checks file paths and references
- Tests local installation
- Verifies component activation

### Distribution Ready
- Git initialization
- .gitignore generation
- Marketplace manifest (optional)
- GitHub publishing guide
- Team distribution instructions

### Version Management
- Semantic versioning setup
- Version history tracking
- Update guidelines
- Tag recommendations

## Prerequisites

- Claude Code installed and configured
- Existing custom commands, hooks, or agents (at least some)
- Git installed (for repository creation)
- jq or Python (for JSON validation - optional but recommended)

## Supported Component Types

### Slash Commands
- Custom markdown files with YAML frontmatter
- Template variables support
- Argument handling

### Hooks
- PreToolUse and PostToolUse events
- SessionStart and SessionStop events
- Custom shell scripts with `${CLAUDE_PLUGIN_ROOT}` support
- Filter conditions (tool type, command patterns)

### Output Styles
- Custom formatting templates
- Color schemes
- Rendering preferences
- Display customizations

### Status Lines
- Multi-version status line configurations
- Custom key-value pairs
- Session metadata
- Display templates

### Subagents
- Markdown definitions with YAML frontmatter
- Custom system prompts
- Tool restrictions
- Model selection

## Common Workflows

### Share Personal Setup with Team
1. Run this skill
2. Select all personal customizations
3. Generate plugin
4. Publish to team marketplace
5. Team members install once, get all customizations

### Create Framework-Specific Plugin
1. Create specialized commands for framework
2. Add framework-aware subagents
3. Package with hooks for automation
4. Publish to community marketplace

### Export Project Setup
1. Gather all project-specific commands and hooks
2. Include project standards as agents
3. Create README with project context
4. Include in project repository as `.claude-plugin/`

### Build Team Plugin Library
1. Collect best practices as commands
2. Create specialized agents for common tasks
3. Add security hooks
4. Distribute via team marketplace

## Next Steps After Generation

1. **Test locally:**
   ```bash
   /plugin marketplace add ./plugin-name
   /plugin install plugin-name@dev-marketplace
   /help  # Verify commands appear
   ```

2. **Publish:**
   - Push to GitHub (for public/team sharing)
   - Submit to marketplace (for community)
   - Share locally (for immediate team use)

3. **Maintain:**
   - Update version in plugin.json
   - Track changes in COMPONENTS.md
   - Create git tags for releases
   - Update README with new features

## Version History

### v1.0.0 (2025-11-10)
- Initial release
- Full plugin structure generation
- Command, hook, agent, output style, and status line support
- Comprehensive documentation generation
- Local testing guidance
- Distribution preparation
- Marketplace manifest support
