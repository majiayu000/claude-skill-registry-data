---
name: Build-Assistant
description: Build Claude Code framework components (agents, slash commands, skills, plugins) following standardized templates. Use when creating new agents, commands, skills, or plugins for the multiagent framework.
allowed-tools: Read, Write, Bash
---

# Build-Assistant

This skill provides templates, validation scripts, and documentation for building Claude Code framework components following the multiagent framework standards.

## Instructions

### When Creating a New Agent

1. Read the agent template: `templates/agents/agent.md.template`
2. Read the agent example: `templates/agents/agent-example.md`
3. Read documentation: `docs/claude-code-agents.md` (if available)
4. Create agent file with:
   - Proper frontmatter (name, description, tools, model, color)
   - Clear process steps
   - Key rules and output format
5. Validate using: `scripts/validate-agent.sh <agent-file>`

### When Creating a Slash Command

1. Read the command template: `templates/commands/command.md.template`
2. Read the command example: `templates/commands/command-example.md`
3. Read documentation: `docs/01-claude-code-slash-commands.md`
4. Create command file with:
   - Frontmatter (description, argument-hint, allowed-tools)
   - Task invocation with proper subagent_type
   - Success criteria and notes
5. Validate using: `scripts/validate-command.sh <command-file>`

### When Creating a Skill

1. Read the skill template: `templates/skills/SKILL.md.template`
2. Read the skill example: `templates/skills/skill-example/SKILL.md`
3. Read documentation: `docs/02-claude-code-skills.md`
4. Read decision guide: `docs/04-skills-vs-commands.md`
5. Create SKILL.md with:
   - Frontmatter with "Use when" trigger context
   - Step-by-step instructions
   - Concrete examples
   - Requirements
6. Validate using: `scripts/validate-skill.sh <skill-directory>`

### When Creating a Plugin

1. Read the plugin template: `templates/plugins/plugin.json.template`
2. Read the plugin example: `templates/plugins/example-plugin/`
3. Read documentation: `docs/03-claude-code-plugins.md`
4. Create plugin structure with:
   - `.claude-plugin/plugin.json` manifest
   - README.md with components list
   - commands/, skills/, agents/ as needed
5. Validate using: `scripts/validate-plugin.sh <plugin-directory>`

### Choosing Between Skills and Commands

Consult `docs/04-skills-vs-commands.md` to decide:
- **Use Skill** when: Claude should discover it automatically, complex capability, multiple supporting files
- **Use Command** when: User explicitly triggers it, simple orchestration, workflow shortcut

## Available Resources

### Templates

**Agents:**
- `templates/agents/agent.md.template` - Standard agent template with frontmatter
- `templates/agents/agent-example.md` - Complete working example

**Commands:**
- `templates/commands/command.md.template` - Standard slash command template
- `templates/commands/command-example.md` - Complete working example

**Skills:**
- `templates/skills/SKILL.md.template` - Standard skill template
- `templates/skills/skill-example/SKILL.md` - Git commit helper example
- `templates/skills/README.md` - Skills template documentation

**Plugins:**
- `templates/plugins/plugin.json.template` - Plugin manifest template
- `templates/plugins/example-plugin/` - Complete plugin example with commands and skills

### Validation Scripts

- `scripts/validate-agent.sh` - Validates agent frontmatter and structure
- `scripts/validate-command.sh` - Validates command frontmatter and structure
- `scripts/validate-skill.sh` - Validates SKILL.md frontmatter and "Use when" context
- `scripts/validate-plugin.sh` - Validates plugin manifest and structure
- `scripts/test-build-system.sh` - Comprehensive build system test suite

### Documentation

- `docs/01-claude-code-slash-commands.md` - Slash command reference
- `docs/02-claude-code-skills.md` - Skills reference with frontmatter fields
- `docs/03-claude-code-plugins.md` - Plugin architecture and structure
- `docs/04-skills-vs-commands.md` - Decision guide for choosing component type

## Requirements

- Templates must exist in `templates/` directory
- Validation scripts must be executable
- Documentation files should be available in `docs/`
- Follow Claude Code standards for frontmatter
- Include "Use when" context in skill descriptions

## Best Practices

1. **Always validate** - Run validation scripts after creation
2. **Follow templates** - Use provided templates as starting point
3. **Read examples** - Study working examples before creating new components
4. **Check documentation** - Consult docs for standards and patterns
5. **Test thoroughly** - Use test-build-system.sh for comprehensive testing

---

**Generated from**: multiagent-build plugin build-assistant skill
**Purpose**: Standardize framework component creation across multiagent ecosystem
**Load when**: Creating agents, commands, skills, or plugins
