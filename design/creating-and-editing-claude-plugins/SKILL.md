---
name: Creating and Editing Claude Plugins
description: Use before creating or editing plugin.json manifests, organizing .claude-plugin directories, or when user asks about plugin structure, versioning, or distribution. Provides expert guidance on manifest configuration, component organization, semantic versioning, and shareable plugin best practices. Invoke when working with any plugin files or discussing plugin architecture to ensure correct structure and discoverability.
---

# Building Claude Code Plugins

This skill provides comprehensive guidance for creating Claude Code plugins that extend Claude with shareable, discoverable functionality.

## What Are Claude Code Plugins?

Plugins are packages of functionality that can be shared across projects and teams. They can contain:
- **Custom slash commands**: User-invoked commands
- **Custom agents**: Specialized agent behaviors
- **Agent skills**: Reusable capabilities agents can invoke
- **Event hooks**: Handlers that trigger on specific events
- **MCP servers**: External tool integrations

Plugins are discoverable through plugin marketplaces and easy to install with `/plugin install`.

## Core Requirements

Every plugin requires exactly one file: `.claude-plugin/plugin.json`

**Minimum valid plugin:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0"
}
```

All other components (commands, agents, skills, hooks, MCP servers) are optional.

## Quick Start

1. **Create plugin directory**: `mkdir my-plugin`
2. **Create manifest**: `mkdir my-plugin/.claude-plugin`
3. **Create plugin.json** with name and version
4. **Add components** (skills, commands, etc.) as needed
5. **Test locally**: `/plugin install /path/to/my-plugin`

For complete templates, see `templates/plugin.json` and `templates/README.md`.

## Plugin Manifest

The `plugin.json` file defines your plugin's metadata and component locations.

### Required Fields
- `name`: Unique identifier in kebab-case
- `version`: Semantic versioning (MAJOR.MINOR.PATCH)

### Optional Metadata
- `description`: Brief plugin purpose
- `author`: Object with `name` (required) and `email` (optional)
- `homepage`: Documentation URL
- `repository`: Source code link
- `license`: Open source license identifier
- `keywords`: Array of discovery tags

### Component Paths
Specify where Claude should find each component type:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "commands": ["./commands"],
  "agents": ["./agents"],
  "skills": ["./skills"],
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Path rules:**
- Must be relative to plugin root
- Should start with `./`
- Can be arrays for multiple directories
- Use `${CLAUDE_PLUGIN_ROOT}` variable for flexible resolution

See `reference/plugin-structure.md` for detailed structure information.

## Component Types

### Commands
Custom slash commands users invoke directly.
- Location: Specified in `commands` field
- Format: Markdown files with frontmatter
- Example: `/my-command`

### Agents
Specialized agent behaviors with custom capabilities.
- Location: Specified in `agents` field
- Format: Markdown files describing agent

### Skills
Reusable capabilities agents can invoke autonomously.
- Location: Specified in `skills` field
- Format: Directories containing `SKILL.md`
- Most common component type

### Hooks
Event handlers triggered by specific events.
- Location: Specified in `hooks` field (points to hooks.json)
- Events: PreToolUse, PostToolUse, UserPromptSubmit
- Format: JSON configuration file

### MCP Servers
External tool integrations via Model Context Protocol.
- Location: Specified in `mcpServers` field (points to .mcp.json)
- Purpose: Connect external data sources and tools

## Ensuring Consistency Between Commands and Skills

**CRITICAL**: When a plugin contains both slash commands and skills that work together, they must provide consistent instructions. Inconsistencies cause Claude to follow the wrong workflow.

### The Problem

Slash commands execute first and provide initial instructions. If the command has different instructions than a skill it invokes, Claude will follow the command's approach instead of the skill's approach.

**Example issue:**
- Slash command says: "Clone the repository with `gh repo clone`"
- Skill says: "Create a git worktree with `git worktree add`"
- Result: Claude clones instead of using worktrees (following the command's instructions)

### The Solution

1. **Align workflows**: Ensure slash commands and skills describe the same approach
2. **Avoid duplication**: Have the command reference the skill rather than duplicating instructions
3. **Provide complete context**: When handing off to another Claude session, include all necessary details (what, where, what to skip)

### Example: Correct Pattern

**Slash command approach:**
```markdown
## 1. Setup
Create git worktree following the standard workflow:
[Include essential setup instructions]

## 2. Launch New Session
Provide user with complete context to continue:
- What PR/task they're working on
- Where the code is located
- Which skill to invoke
- What steps to skip (already completed)
```

**Skill approach:**
```markdown
## 1. Setup (if needed)
[Same setup instructions as command]

## 2. Continue workflow
[Rest of the process]
```

### Portability Considerations

**DON'T hardcode machine-specific paths:**
```markdown
# Bad: Assumes all users organize code the same way
cd ~/src/<repo_name>
```

**DO use adaptable instructions:**
```markdown
# Good: Adapts to any user's setup
First, check if the repository exists locally.
Ask the user where they keep repositories if not found.
```

This keeps plugins portable across different users and environments.

### Validation Checklist

When creating or reviewing plugins with both commands and skills:
- [ ] Commands and skills describe the same workflow approach
- [ ] No hardcoded machine-specific paths
- [ ] Handoffs between sessions include complete context
- [ ] Instructions clearly state what steps to skip when already completed
- [ ] Examples use generic paths, not specific to one developer

## Creating Your Plugin

### Choose Your Pattern

**Single-purpose plugin** (one component type):
```
my-command-plugin/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    └── my-command.md
```

**Skills-focused plugin** (most common):
```
my-skills-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        └── SKILL.md
```

**Full-featured plugin**:
```
enterprise-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
├── agents/
├── skills/
├── hooks/
│   └── hooks.json
└── .mcp.json
```

See `reference/plugin-structure.md` for more patterns and examples.

### Writing plugin.json

Start minimal, add metadata as needed:

```json
{
  "name": "data-processor",
  "version": "1.0.0",
  "description": "Tools for processing and analyzing data files",
  "author": {
    "name": "Your Name"
  },
  "keywords": ["data", "analysis", "processing"],
  "skills": ["./skills"]
}
```

**Key points:**
- Name must be unique and descriptive
- Version must follow semantic versioning
- Description helps with discoverability
- Only specify component paths you're using

## Best Practices

For comprehensive best practices, see `reference/best-practices.md`. Key highlights:

### Organization
- Keep related functionality together
- Use clear, descriptive naming
- One plugin = one cohesive purpose
- Don't create mega-plugins that do everything

### Versioning
- Follow semantic versioning strictly
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Documentation
- Write clear descriptions for discoverability
- Document each component's purpose
- Include usage examples
- Specify any requirements or dependencies

### Testing
- Test plugin installation: `/plugin install /path/to/plugin`
- Verify components load: Use `claude --debug`
- Test in clean environment before sharing
- Validate all paths are relative and correct

### Path Management
- Always use relative paths starting with `./`
- Verify paths are correct relative to plugin root
- Test that components are found after installation

## Reviewing Plugins

When reviewing plugins (your own or others') before sharing or adding to marketplaces, use this systematic approach to ensure quality and adherence to best practices.

### Review Process

Follow these five steps for thorough plugin review:

**Step 1: Initial Inspection**
1. Check plugin.json exists at `.claude-plugin/plugin.json`
2. Validate JSON syntax
3. Verify required fields (name, version)
4. Review overall directory structure

**Step 2: Component Verification**
1. Test each component path references valid location
2. Check component files exist and are properly formatted
3. Verify component-specific requirements (SKILL.md, frontmatter, etc.)

**Step 3: Local Testing**
1. Install plugin locally: `/plugin install /path/to/plugin`
2. Verify installation: `/plugin` shows plugin
3. Check for errors: `claude --debug`
4. Test each component works as documented
5. Uninstall and reinstall to verify clean installation

**Step 4: Quality Assessment**
1. Evaluate documentation completeness
2. Check if plugin has single, clear purpose
3. Assess naming quality and discoverability
4. Review for best practices adherence

**Step 5: Final Validation**
1. Confirm no security issues
2. Verify version is appropriate
3. Check all documentation is accurate
4. Ensure plugin is ready for intended audience

### Review Checklist

For a comprehensive checklist covering all aspects of plugin review, see `reference/review-checklist.md`. Key areas to review:

1. **Manifest Validation**: plugin.json structure, required fields, JSON syntax
2. **Path Validation**: Relative paths, correct references, no external dependencies
3. **Structure and Organization**: Clear patterns, cohesive purpose
4. **Component Quality**: Skills, commands, agents, hooks, MCP servers
5. **Documentation**: README, installation, usage examples
6. **Naming Conventions**: Descriptive, non-generic names
7. **Versioning**: Semantic versioning, appropriate version number
8. **Security and Safety**: No credentials, safe operations, no malicious code

The detailed checklist in `reference/review-checklist.md` provides specific items to verify for each category, common issues to flag (critical, important, minor), and decision criteria for determining if a plugin is ready to share.

### Quick Review Tips

1. **Test in clean environment**: Install plugin fresh to catch missing dependencies
2. **Read documentation first**: Verify docs match actual functionality
3. **Check debug output**: `claude --debug` reveals loading issues
4. **Try all components**: Don't assume untested components work
5. **Think like a user**: Is it easy to understand and use?
6. **Verify paths manually**: Walk through directory structure to confirm paths
7. **Check version history**: If updating, ensure version change is appropriate

## Testing and Debugging

### Local Testing
```bash
# Install locally
/plugin install /path/to/my-plugin

# Check installation
/plugin

# Verify components loaded
/help                    # Check for new commands
claude --debug          # See plugin loading details

# Update plugin after making changes
/plugin                 # Select plugin to update (easiest)
# OR manually uninstall/reinstall:
/plugin uninstall my-plugin@local
/plugin install /path/to/my-plugin
```

**Validation steps:**
- Plugin appears in `/plugin` list
- No errors in `claude --debug` output
- Commands appear in `/help` (if plugin has commands)
- Skills are discoverable in conversation
- All component paths resolve correctly

### Common Issues
- **Plugin not found**: Check plugin.json exists at `.claude-plugin/plugin.json`
- **Components not loaded**: Verify paths in plugin.json are relative and correct
- **Version conflicts**: Ensure version follows semantic versioning format
- **Invalid JSON**: Validate plugin.json syntax

Use `claude --debug` to see detailed plugin loading information.

## Sharing Your Plugin

### Via Marketplace
1. Create or add to a marketplace (see marketplace-builder skill)
2. Add plugin entry to marketplace.json
3. Share marketplace URL or path
4. Users add marketplace: `/plugin marketplace add <url>`
5. Users install: `/plugin install my-plugin@marketplace-name`

### Direct Installation
Users can install directly without a marketplace:
```bash
/plugin install /path/to/plugin
# or
/plugin install https://github.com/user/repo
```

## Key Principles

### 1. Single Responsibility
Each plugin should have one clear purpose. Don't create catch-all plugins.

### 2. Clear Naming
Use descriptive kebab-case names that indicate purpose:
- Good: `git-workflow`, `data-analyzer`, `react-toolkit`
- Avoid: `helpers`, `utils`, `misc`

### 3. Minimal Manifest
Only include what you need. Start with name and version, add components as needed.

### 4. Relative Paths
All paths must be relative to plugin root and start with `./`

### 5. Semantic Versioning
Version strictly: breaking changes = MAJOR, features = MINOR, fixes = PATCH

## Progressive Development

### Start Simple
1. Create minimal plugin.json
2. Add one component type
3. Test locally
4. Iterate and refine

### Add Complexity Gradually
1. Start with core functionality
2. Test thoroughly
3. Add additional components
4. Document as you go
5. Share when stable

### Iterate Based on Usage
1. Release early version
2. Gather feedback
3. Add features based on real needs
4. Maintain backward compatibility when possible

## References

- `reference/plugin-structure.md`: Complete structure details and patterns
- `reference/best-practices.md`: Comprehensive development guide
- `templates/plugin.json`: Starting template for plugin manifest
- `templates/README.md`: Starting template for plugin documentation

## Quick Decision Guide

Creating a plugin? Ask:
1. **What's the core purpose?** One clear goal per plugin
2. **What components do I need?** Start minimal, add as needed
3. **Is the name descriptive?** Clear, kebab-case, indicates purpose
4. **Are paths relative?** All paths start with `./` from plugin root
5. **Is it versioned correctly?** Semantic versioning (x.y.z)
6. **Have I tested locally?** Install and verify before sharing

Remember: Plugins package related functionality for easy sharing. Start simple, test thoroughly, and iterate based on real usage.
