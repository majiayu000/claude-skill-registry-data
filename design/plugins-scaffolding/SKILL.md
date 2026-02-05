---
name: plugins-scaffolding
description: Guide for creating Claude Code plugins with proper structure, metadata, and components. This skill should be used when creating plugins, writing manifests, or setting up marketplaces.
---

# Plugins Scaffold Skill

This skill provides guidance for creating Claude Code plugins, including structure, manifests, components (commands, agents, skills, hooks, MCP servers), and marketplace distribution.

## When to Use This Skill

This skill should be used when:
- Creating a new Claude Code plugin from scratch
- Understanding plugin architecture and components
- Writing plugin.json manifests
- Creating plugin commands, agents, skills, hooks, or MCP servers
- Setting up plugin marketplaces
- Distributing plugins to teams or the community
- Validating and testing plugins before distribution
- Understanding plugin vs marketplace structure

## Plugin Architecture Overview

### What Are Plugins?

Plugins are extensions that add custom functionality to Claude Code, shareable across projects and teams. They can include:

- **Commands**: Custom slash commands for interactive workflows
- **Agents**: Specialized Claude instances with specific capabilities
- **Skills**: Just-in-time expertise that Claude autonomously invokes
- **Hooks**: Event handlers for automation and workflow customization
- **MCP Servers**: External tool integrations via Model Context Protocol

### Plugin vs Marketplace

**Plugin:**
- A single package of functionality (one plugin = one purpose)
- Contains commands, agents, skills, hooks, or MCP servers
- Has a `.claude-plugin/plugin.json` manifest
- Can be distributed via marketplaces or standalone

**Marketplace:**
- A catalog of multiple plugins
- Has a `.claude-plugin/marketplace.json` manifest
- Enables centralized discovery and installation
- Can host plugins from multiple sources (local paths, GitHub repos, git URLs)

## Plugin Directory Structure

Every plugin must follow this standard structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── commands/                # Optional: Slash commands
│   ├── command-one.md
│   └── command-two.md
├── agents/                  # Optional: Custom agents
│   └── agent-name.md
├── skills/                  # Optional: Agent skills
│   ├── skill-one/
│   │   └── SKILL.md
│   └── skill-two/
│       └── SKILL.md
├── hooks/                   # Optional: Event handlers
│   └── hooks.json
├── .mcp.json               # Optional: MCP server config
├── scripts/                # Optional: Utility scripts
├── README.md               # Recommended: Documentation
└── LICENSE                 # Recommended: License file
```

**Critical Requirements:**
- The `.claude-plugin/plugin.json` file is REQUIRED for all plugins
- All component directories (commands, agents, skills, hooks) must exist at plugin root, NOT within `.claude-plugin/`
- Component directories are optional - only create what your plugin needs
- Use kebab-case for plugin directory names (e.g., `my-plugin`, not `MyPlugin` or `my_plugin`)

## Plugin Manifest (plugin.json)

The `plugin.json` file is your plugin's core configuration. It must be located at `.claude-plugin/plugin.json`.

### Required Fields

```json
{
  "name": "plugin-name"
}
```

**Field Specifications:**

- **name** (required)
  - Unique identifier in kebab-case format
  - Examples: `"deployment-tools"`, `"ai-security"`, `"git-helpers"`
  - Should be descriptive and match the plugin directory name
  - Must be unique within a marketplace

### Recommended Metadata Fields

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of what this plugin does",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://github.com/owner/plugin-repo",
  "repository": "https://github.com/owner/plugin-repo",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

**Field Specifications:**

- **version** (recommended)
  - Use semantic versioning: MAJOR.MINOR.PATCH
  - Example: `"2.1.0"`
  - See Versioning section below for details

- **description** (recommended)
  - Brief explanation of plugin purpose
  - Should clearly state what the plugin does
  - Keep under 200 characters for marketplace display

- **author** (recommended)
  - Object containing name, email (optional), and URL (optional)
  - Helps users know who maintains the plugin

- **homepage** (recommended)
  - URL to plugin documentation
  - Often same as repository URL

- **repository** (recommended)
  - Source code repository link
  - Enables users to view source and report issues

- **license** (recommended)
  - SPDX license identifier (e.g., `"MIT"`, `"Apache-2.0"`, `"GPL-3.0"`)
  - Critical for open source distribution

- **keywords** (recommended)
  - Array of tags for discovery
  - Examples: `["git", "automation", "security", "devops"]`
  - Helps users find your plugin in marketplaces

### Custom Component Paths (Advanced)

```json
{
  "name": "plugin-name",
  "commands": "./custom-commands",
  "agents": "./custom-agents/agent.md",
  "hooks": "./custom-hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Path Configuration Rules:**
- All paths must be relative to plugin root and begin with `./`
- Custom paths supplement (not replace) default directories
- Use `${CLAUDE_PLUGIN_ROOT}` environment variable for absolute path references in hooks and MCP configs

**When to Use Custom Paths:**
- Organizing complex plugins with non-standard layouts
- Migrating existing projects to plugin format
- Keeping components in specific directories for workflow reasons

## Plugin Components

### Commands (Slash Commands)

Commands are markdown files in the `commands/` directory that define interactive workflows.

**File Structure:**
```
commands/
├── setup-project.md
└── deploy-staging.md
```

**Command File Format:**
```markdown
# Command Title

Brief description of what this command does.

## Instructions

Step-by-step instructions for Claude Code to execute when this command is invoked.

1. First step
2. Second step
3. Third step

## Important Notes

Any constraints, requirements, or special considerations.
```

**Best Practices:**
- Use clear, imperative instructions
- Specify what NOT to do (constraints)
- Include examples when helpful
- Keep commands focused on one task
- Use commands for interactive setup and configuration

**When to Use Commands vs Skills:**
- Commands: One-time interactive setup, configuration, scaffolding
- Skills: Ongoing expertise that applies across multiple sessions

### Agents (Custom Agents)

Agents are markdown files in the `agents/` directory that describe specialized Claude instances.

**File Structure:**
```
agents/
└── security-auditor.md
```

**Agent File Format:**
```markdown
---
description: Specialized agent for security auditing and vulnerability detection
---

# Security Auditor Agent

This agent specializes in identifying security vulnerabilities, reviewing authentication mechanisms, and conducting security audits.

## Capabilities

- Identify SQL injection vulnerabilities
- Review authentication and authorization flows
- Validate input sanitization
- Assess data protection measures
- Generate security audit reports

## When to Invoke

Use this agent when:
- Implementing authentication flows
- Reviewing security-sensitive code
- Conducting pre-deployment security audits
```

**Best Practices:**
- Clearly define the agent's specialization
- List specific capabilities the agent provides
- Specify when the agent should be invoked
- Use agents for complex, multi-step specialized tasks

### Skills (Agent Skills)

Skills are directories in the `skills/` folder containing `SKILL.md` files that provide just-in-time expertise.

**File Structure:**
```
skills/
├── brand-guidelines/
│   └── SKILL.md
└── security-standards/
    ├── SKILL.md
    └── references/
        └── standards.md
```

**SKILL.md Format:**
```markdown
---
name: Skill Name
description: Guide for [topic]. This skill should be used when [specific use cases] (max 200 chars)
---

# Skill Name Skill

This skill provides guidance on [topic].

## When to Use This Skill

This skill should be used when:
- [Use case 1]
- [Use case 2]

## Guidelines

[Core expertise and instructions]
```

**Best Practices:**
- See the `skills-scaffold` skill for comprehensive skill creation guidance
- Use skills for ongoing expertise, not one-time setup
- Write discoverable descriptions with keywords using third-person form
- Keep skills focused on one domain
- Use progressive disclosure (core content in SKILL.md, details in references/ directory)

### Hooks (Event Handlers)

Hooks are JSON configurations in `hooks/hooks.json` that execute in response to events.

**File Location:**
```
hooks/
└── hooks.json
```

**Hook Configuration Format:**
```json
{
  "hooks": [
    {
      "name": "pre-commit-check",
      "event": "PreToolUse",
      "tool": "Bash",
      "script": "${CLAUDE_PLUGIN_ROOT}/scripts/pre-commit.sh",
      "blockOnNonZeroExit": true
    },
    {
      "name": "session-setup",
      "event": "SessionStart",
      "script": "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh"
    }
  ]
}
```

**Event Types:**
- `PreToolUse`: Before a tool is executed
- `PostToolUse`: After a tool completes
- `UserPromptSubmit`: When user submits a prompt
- `Notification`: When a notification is triggered
- `Stop`: When execution stops
- `SessionStart`: When a new session begins

**Best Practices:**
- Use `${CLAUDE_PLUGIN_ROOT}` for script paths
- Set `blockOnNonZeroExit: true` to halt execution on errors
- Keep hook scripts fast to avoid workflow delays
- Use hooks for automation, validation, and enforcement

### MCP Servers (External Tool Integration)

MCP servers integrate external tools via the Model Context Protocol.

**File Location:**
```
.mcp.json
```

**MCP Configuration Format:**
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-server/index.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Best Practices:**
- Use `${CLAUDE_PLUGIN_ROOT}` for script paths
- Document required environment variables
- Provide clear setup instructions in README.md
- Test MCP server functionality independently

## Plugin Development Workflow

### Step 1: Plan the Plugin

Before creating a plugin, determine:

- **Purpose**: What problem does this plugin solve?
- **Components**: What components does it need?
  - Commands for interactive workflows?
  - Agents for specialized tasks?
  - Skills for ongoing expertise?
  - Hooks for automation?
  - MCP servers for external tools?
- **Scope**: Is this one plugin or should it be split?
- **Distribution**: Will this be private (team) or public (community)?

**Design Principle:** One plugin = one purpose. When solving multiple unrelated problems, create multiple plugins.

### Step 2: Create Directory Structure

```bash
mkdir -p plugin-name/.claude-plugin
mkdir -p plugin-name/commands    # If needed
mkdir -p plugin-name/agents      # If needed
mkdir -p plugin-name/skills      # If needed
mkdir -p plugin-name/hooks       # If needed
mkdir -p plugin-name/scripts     # If needed
```

### Step 3: Write Plugin Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description of plugin purpose",
  "author": {
    "name": "Your Name",
    "url": "https://yoursite.com"
  },
  "repository": "https://github.com/owner/plugin-repo",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

### Step 4: Create Plugin Components

Add the components your plugin needs:

**For Commands:**
- Create markdown files in `commands/` directory
- Use clear, imperative instructions
- Specify constraints and requirements

**For Agents:**
- Create markdown files in `agents/` directory
- Define specialization and capabilities
- Specify invocation criteria

**For Skills:**
- Create `skills/{skill-name}/SKILL.md` with YAML frontmatter
- Follow the `skills-scaffold` skill guidance
- Use progressive disclosure for token efficiency

**For Hooks:**
- Create `hooks/hooks.json` configuration
- Write hook scripts in `scripts/` directory
- Use `${CLAUDE_PLUGIN_ROOT}` for paths

**For MCP Servers:**
- Create `.mcp.json` configuration
- Implement MCP server according to protocol spec
- Document setup and environment variables

### Step 5: Add Documentation

Create a comprehensive README.md:

```markdown
# Plugin Name

Brief description of what this plugin does.

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`bash
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace-name
\`\`\`

## Usage

### Commands

- \`/command-name\`: Description of what it does

### Skills

- \`skill-name\`: Description of expertise provided

## Configuration

Any required setup or environment variables.

## License

License information.
```

### Step 6: Validate and Test

Before distribution:

1. **Validate JSON syntax**
   ```bash
   # Check plugin.json is valid JSON
   cat .claude-plugin/plugin.json | jq .
   ```

2. **Test locally**
   ```bash
   # Add as local marketplace
   /plugin marketplace add ./path/to/plugin-parent-directory

   # Install the plugin
   /plugin install plugin-name@marketplace-name
   ```

3. **Test all components**
   - Invoke each command and verify it works
   - Test agents by requesting their specialized tasks
   - Verify skills load when expected
   - Check hooks execute at correct events
   - Test MCP server integration

4. **Review security**
   - Audit all scripts and code
   - Check for hardcoded credentials
   - Document required environment variables
   - Ensure no sensitive data in repository

### Step 7: Distribute via Marketplace

See Marketplace Distribution section below.

## Plugin Versioning

Follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **MAJOR** (x.0.0): Breaking changes or incompatible API changes
- **MINOR** (0.x.0): New features added in a backward-compatible manner
- **PATCH** (0.0.x): Backward-compatible bug fixes

**When to Bump Version:**

- **MAJOR**: Changing command names, removing components, changing behavior in incompatible ways
- **MINOR**: Adding new commands, agents, skills; enhancing existing features
- **PATCH**: Fixing bugs, typos, documentation; minor improvements

**Version Update Workflow:**

1. Update version in `.claude-plugin/plugin.json`
2. Update version in marketplace.json (if applicable)
3. Update CHANGELOG.md with changes
4. Update README.md if functionality changed
5. Create git tag for the release (e.g., `v1.2.0`)

## Marketplace Distribution

### Creating a Plugin Marketplace

A marketplace is a repository that catalogs multiple plugins.

**Directory Structure:**
```
marketplace-repo/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/                    # If using local plugins
│   ├── plugin-one/
│   └── plugin-two/
└── README.md
```

**Marketplace Manifest (.claude-plugin/marketplace.json):**
```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "metadata": {
    "description": "Brief description of this marketplace",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-one",
      "source": "./plugins/plugin-one",
      "description": "What plugin-one does",
      "version": "1.0.0",
      "author": {
        "name": "Author Name",
        "url": "https://example.com"
      },
      "repository": "https://github.com/owner/plugin-one",
      "license": "MIT",
      "keywords": ["keyword1", "keyword2"]
    }
  ]
}
```

**Required Fields:**
- `name`: Unique marketplace identifier (kebab-case)
- `owner`: Maintainer information with name and email
- `plugins`: Array of plugin entries

**Optional Metadata:**
- `metadata.description`: Marketplace overview
- `metadata.version`: Marketplace version
- `metadata.pluginRoot`: Base path for relative plugin sources (e.g., `"./plugins"`)

### Plugin Source Types

**Relative Paths** (same repository):
```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```
- Best for: Curated marketplaces with bundled plugins
- The `pluginRoot` metadata field sets the base directory

**GitHub Repositories:**
```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```
- Best for: Distributed development, individual plugin repositories
- Supports both public and private repositories

**Git Repositories:**
```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```
- Best for: GitLab, Bitbucket, or self-hosted git servers
- Works with any git-compatible URL

### Distribution Methods

**GitHub (Recommended):**

1. Create a repository with `.claude-plugin/marketplace.json` at root
2. Add plugins either:
   - As subdirectories (with `pluginRoot`)
   - As external GitHub repositories (with `source` objects)
3. Users add the marketplace:
   ```bash
   /plugin marketplace add owner/repo
   ```

**Other Git Services:**
```bash
/plugin marketplace add https://gitlab.com/company/plugins.git
```

**Local Development:**
```bash
/plugin marketplace add ./my-local-marketplace
```

### Marketplace Operations

**List configured marketplaces:**
```bash
/plugin marketplace list
```

**Update marketplace metadata:**
```bash
/plugin marketplace update marketplace-name
```

**Remove a marketplace:**
```bash
/plugin marketplace remove marketplace-name
```

**Install plugins:**
```bash
/plugin install plugin-name@marketplace-name
```

### Team Configuration

Configure `.claude/settings.json` in repositories to auto-install marketplaces:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

When team members trust the folder, configured marketplaces install automatically.

## Common Plugin Patterns

### Pattern: Developer Productivity Plugin

**Use Case:** Streamline common development tasks (git, deployments, testing)

**Structure:**
- Multiple commands for different workflows
- Hooks for automation (pre-commit, pre-push)
- Skills for best practices

**Example:**
```
git-helpers/
├── .claude-plugin/plugin.json
├── commands/
│   ├── commit-push.md
│   └── setup-repo.md
├── hooks/
│   └── hooks.json
└── scripts/
    └── pre-commit.sh
```

### Pattern: Domain Expertise Plugin

**Use Case:** Provide specialized knowledge (security, performance, architecture)

**Structure:**
- Agents for specialized tasks
- Skills for ongoing guidance
- Commands for audits and reports

**Example:**
```
security-expert/
├── .claude-plugin/plugin.json
├── agents/
│   └── security-auditor.md
├── skills/
│   ├── security-standards/
│   │   └── SKILL.md
│   └── owasp-guidelines/
│       └── SKILL.md
└── commands/
    └── security-audit.md
```

### Pattern: External Tool Integration Plugin

**Use Case:** Integrate external services (Azure DevOps, Jira, Slack)

**Structure:**
- MCP server for API integration
- Skills for tool usage guidelines
- Commands for configuration

**Example:**
```
ado-integration/
├── .claude-plugin/plugin.json
├── .mcp.json
├── commands/
│   └── ado-init.md
├── skills/
│   └── ado-work-items/
│       └── SKILL.md
└── mcp-server/
    └── index.js
```

### Pattern: Project Scaffolding Plugin

**Use Case:** Generate boilerplate code and project structure

**Structure:**
- Commands for interactive scaffolding
- Templates in supporting files
- Skills for architecture guidance

**Example:**
```
project-scaffold/
├── .claude-plugin/plugin.json
├── commands/
│   ├── create-react-app.md
│   └── create-api.md
├── skills/
│   └── architecture-patterns/
│       └── SKILL.md
└── templates/
    ├── react-component.tsx
    └── api-endpoint.ts
```

## Best Practices for Plugin Development

### 1. Keep Plugins Focused

- One plugin = one purpose or domain
- Create multiple small plugins rather than one mega-plugin
- Avoid creating plugins that try to do everything

**Good Examples:**
- `git-helpers` (git automation)
- `security-auditor` (security scanning)
- `deployment-tools` (deployment workflows)

**Bad Example:**
- `developer-tools` (git + security + deployment + testing + ...)

### 2. Use Appropriate Components

- Commands for interactive setup and configuration
- Skills for ongoing expertise and guidelines
- Agents for complex specialized tasks
- Hooks for automation and enforcement
- MCP servers for external tool integration

**Avoid:**
- Using commands for ongoing expertise (use skills instead)
- Using skills for one-time setup (use commands instead)
- Duplicating functionality across components

### 3. Write Clear Documentation

- Create comprehensive README.md with installation and usage instructions
- Provide examples for all commands and features
- Document required environment variables
- Include troubleshooting section

### 4. Follow Semantic Versioning

- Use MAJOR.MINOR.PATCH format
- Bump versions appropriately based on changes
- Document changes in CHANGELOG.md
- Create git tags for releases

### 5. Test Thoroughly

- Test locally before distribution
- Validate JSON manifests
- Test all commands, skills, agents
- Verify hooks execute correctly
- Test MCP server integration

### 6. Security Considerations

- Audit all scripts and code
- Never hardcode credentials
- Use environment variables for secrets
- Document security requirements
- Avoid bundling unvetted third-party code
- Avoid including sensitive organizational data

### 7. Use Consistent Naming

- Plugin names: kebab-case (`my-plugin`)
- Command files: kebab-case (`my-command.md`)
- Skill directories: kebab-case (`my-skill/`)
- Use descriptive names that indicate purpose

### 8. Leverage Environment Variables

- Use `${CLAUDE_PLUGIN_ROOT}` in hooks and MCP configs
- Document required environment variables
- Provide examples for configuration
- Use `.env.example` files for templates

### 9. Organize Supporting Files

```
plugin-name/
├── scripts/        # Executable scripts for hooks/automation
├── templates/      # Template files for scaffolding
├── examples/       # Example configurations
└── docs/          # Additional documentation
```

### 10. Provide Examples

- Include example usage in README.md
- Show before/after for commands
- Demonstrate integration patterns
- Provide sample configurations

## Plugin Validation Checklist

Before distributing a plugin, verify:

**Structure:**
- [ ] `.claude-plugin/plugin.json` exists with required fields
- [ ] Component directories at plugin root (not in `.claude-plugin/`)
- [ ] kebab-case naming for plugin and components
- [ ] README.md with installation and usage instructions

**Manifest:**
- [ ] Name is unique and descriptive
- [ ] Version follows semantic versioning
- [ ] Description clearly states plugin purpose
- [ ] Author information included
- [ ] Repository URL provided
- [ ] License specified
- [ ] Keywords for discoverability

**Components:**
- [ ] All commands tested and working
- [ ] All agents tested with appropriate tasks
- [ ] All skills have proper YAML frontmatter
- [ ] All hooks execute at correct events
- [ ] All MCP servers integrate correctly

**Documentation:**
- [ ] README.md is comprehensive
- [ ] All features documented with examples
- [ ] Environment variables documented
- [ ] Installation instructions clear
- [ ] Troubleshooting section included

**Quality:**
- [ ] JSON manifests are valid (test with `jq`)
- [ ] No hardcoded credentials or secrets
- [ ] All scripts audited for security
- [ ] Plugin tested locally before distribution
- [ ] CHANGELOG.md documents changes

**Marketplace (if applicable):**
- [ ] Plugin entry in marketplace.json
- [ ] Source path/URL is correct
- [ ] Marketplace metadata updated
- [ ] Version numbers consistent across files

## Troubleshooting Plugin Development

### Problem: Plugin Not Loading

**Possible Causes:**
- Missing `.claude-plugin/plugin.json`
- Invalid JSON in plugin.json
- Wrong directory structure
- Components in `.claude-plugin/` instead of plugin root

**Solution:**
- Verify plugin.json exists at `.claude-plugin/plugin.json`
- Validate JSON syntax: `cat .claude-plugin/plugin.json | jq .`
- Check component directories are at plugin root
- Review directory structure against standards

### Problem: Commands Not Appearing

**Possible Causes:**
- Commands directory in wrong location
- Command files not markdown (.md)
- Custom commands path misconfigured

**Solution:**
- Place commands in `commands/` directory at plugin root
- Ensure all command files end with `.md`
- If using custom path, verify it starts with `./`

### Problem: Skills Not Loading

**Possible Causes:**
- Missing `SKILL.md` file (case-sensitive)
- Missing YAML frontmatter
- Description too vague for Claude to match

**Solution:**
- Verify each skill directory has `SKILL.md` (uppercase)
- Ensure YAML frontmatter with name and description
- Make description specific with relevant keywords
- See `skills-scaffold` skill for details

### Problem: Hooks Not Executing

**Possible Causes:**
- Wrong path to hook script
- Script not executable
- Missing `${CLAUDE_PLUGIN_ROOT}` environment variable

**Solution:**
- Use `${CLAUDE_PLUGIN_ROOT}` for all script paths
- Make scripts executable: `chmod +x scripts/*.sh`
- Test hook scripts independently first

### Problem: MCP Server Not Connecting

**Possible Causes:**
- Wrong command or args in .mcp.json
- Missing environment variables
- Server code has errors

**Solution:**
- Verify command and args in .mcp.json
- Document and provide required environment variables
- Test MCP server independently
- Check server logs for errors

### Problem: Marketplace Not Installing Plugin

**Possible Causes:**
- Wrong plugin source path/URL
- Repository not accessible
- Plugin directory doesn't contain plugin.json
- Network connectivity issues

**Solution:**
- Verify source path is correct (relative or URL)
- Check repository is public or credentials configured
- Ensure plugin.json exists in plugin directory
- Test repository access manually

## Advanced Topics

### Plugin Composition

Plugins can reference each other's capabilities:

```markdown
For git automation, the git-helpers plugin provides comprehensive commands.

For security standards, refer to the security-expert plugin's skills.
```

**Best Practice:** Keep plugins independent where possible, but document complementary plugins in README.md.

### Multi-Language Support

Plugins can include scripts in different languages:

```
scripts/
├── python/
│   └── analyzer.py
├── javascript/
│   └── formatter.js
└── shell/
    └── deploy.sh
```

**Best Practice:** Document runtime requirements (Python version, Node version) in README.md and plugin.json dependencies field.

### Plugin Templates and Generators

Create meta-plugins that generate other plugins:

**Example:** The `ai-plugins` plugin includes:
- `/plugins-scaffold` command for generating plugin structure
- `plugins-scaffold` skill for plugin development guidance
- `skills-scaffold` skill for skill creation guidance

### Environment-Specific Configuration

Use environment variables for configuration:

```json
{
  "mcpServers": {
    "api-service": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "API_URL": "${API_URL}",
        "API_KEY": "${API_KEY}",
        "ENVIRONMENT": "${ENVIRONMENT:-development}"
      }
    }
  }
}
```

**Best Practice:** Provide `.env.example` file with required variables.

## Summary

Creating effective Claude Code plugins requires:

1. **Planning**: Determine purpose, components, and scope
2. **Structure**: Follow standard directory layout
3. **Manifest**: Write comprehensive plugin.json metadata
4. **Components**: Use appropriate component types for tasks
5. **Documentation**: Provide clear README with examples
6. **Testing**: Validate thoroughly before distribution
7. **Security**: Audit code and avoid hardcoded secrets
8. **Versioning**: Follow semantic versioning
9. **Distribution**: Share via marketplaces for easy discovery

Following these guidelines will result in well-structured plugins that enhance Claude Code's capabilities and provide value to users.

For skill creation specifically, the `skills-scaffold` skill provides detailed guidance.
