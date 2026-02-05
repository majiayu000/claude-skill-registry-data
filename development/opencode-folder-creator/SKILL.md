---
name: opencode-folder-creator
description: Creates complete OpenCode folder structures with configuration files, agents, and commands
version: 1.0.0
author: Claude
tags: [opencode, folder, structure, configuration, setup]
---

# OpenCode Folder Creator

Creates complete `.opencode` directory structures for projects with all necessary configuration files, agents, and commands. This skill sets up the entire OpenCode project structure that teams can immediately use with `opencode serve`.

**IMPORTANT UNIVERSAL PRINCIPLE**: This skill creates FOLDERS and STRUCTURES only. The specific agent types mentioned (code-analyzer, documentation-writer, etc.) are EXAMPLES ONLY. Real swarms will have vastly different agent types, purposes, and specializations. This skill is universal and works with ANY agent configuration.

## Quick Start

### Basic Project Setup
```bash
# Create basic OpenCode structure
mkdir -p .opencode/{agent,command}

# Create main config file
cat > .opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "opencode",
  "autoupdate": true
}
EOF
```

### Specialized Agent Folder Creation (Swarm-Ready)

Creates specialized agent folders with proper communication protocols for swarm deployment:

**Folder Structure:**
```
folder-name/
├── AGENTS.md                    # Agent directory and communication protocol
└── .opencode/
    ├── opencode.json           # Folder-specific configuration
    ├── agent/
    │   └── folder_name.md     # Primary agent with communication requirements
    └── command/
```

**Communication Protocol:**
Every agent MUST introduce itself:
```
I am the [Agent_Name] agent from the [folder_name] folder. I am contacting you because [reason]. I need you to [request]. Please respond with [format].
```

**⚠️ EXAMPLE AGENT TYPES ONLY**:
The following are EXAMPLES to illustrate the pattern. Real swarms can have ANY agent types:
- `data-scientist/` - Data analysis and machine learning
- `ui-designer/` - User interface design and prototyping
- `api-developer/` - API development and integration
- `game-developer/` - Game logic and mechanics
- `researcher/` - Research and analysis
- `translator/` - Language translation and localization
- `music-composer/` - Music composition and audio production
- `financial-analyst/` - Financial modeling and analysis

**UNIVERSAL TRUTH**: This skill works with ANY folder name, ANY agent purpose, ANY specialization. The examples above are for illustration only.

## Project Templates

### 1. Development Project Structure
```bash
mkdir -p .opencode/{agent,command}

# Code reviewer agent
cat > .opencode/agent/code-reviewer.md << 'EOF'
---
description: Reviews code for best practices and potential issues
mode: subagent
tools:
  read: true
  grep: true
permissions:
  edit: deny
  write: deny
---

You are a code reviewer. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
EOF

# Main configuration
cat > .opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "opencode",
  "autoupdate": true
}
EOF
```

## Best Practices

### File Organization
- Use kebab-case for agent and command names
- Keep descriptions concise but informative
- Group related agents and commands together

### Permission Management
- Restrict write/edit access for security-focused agents
- Allow bash access only when necessary
- Use specific bash command permissions instead of wildcard

### Configuration Management
- Always include `$schema` for validation
- Use environment variables for sensitive data
- Keep project-specific config in `.opencode/`
- Store user preferences in `~/.config/opencode/`

### Agent Design
- Create focused agents with specific purposes
- Use subagents for specialized tasks
- Reserve primary agents for coordination tasks
- Include clear usage instructions in agent prompts

This skill provides everything needed to create complete, functional OpenCode folder structures for any project type, with ready-to-use agents, commands, and configurations.