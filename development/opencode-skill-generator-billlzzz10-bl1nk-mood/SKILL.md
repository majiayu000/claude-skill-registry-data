---
name: opencode-skill-generator
description: Generate OpenCode configuration components and skills. Use this skill when you need to create or update OpenCode agents, commands, MCP servers, plugins, tools, or full agent skills following the official opencode.json schema. Supports generating supagents, commands, mcp configs, frontmatter, plugins, and tool mappings.
---

# OpenCode Skill & Component Generator

This skill provides specialized workflows for generating valid OpenCode configuration snippets and full skill structures based on the `opencode.json` schema.

## Component Generation Guide

When generating components, always refer to the schema in [references/schema.json](references/schema.json).

### 1. Supagent (Agent Configuration)
Agents are defined in the `agent` object. 
- **Subagent Example**:
  ```json
  "researcher": {
    "model": "anthropic/claude-3-5-sonnet",
    "prompt": "You are a research assistant...",
    "mode": "subagent",
    "tools": { "websearch": true }
  }
  ```
- **Primary Agent Example**:
  ```json
  "manager": {
    "model": "anthropic/claude-3-5-opus",
    "prompt": "You manage the workflow...",
    "mode": "primary"
  }
  ```

### 2. Command
Commands go into the `command` object.
- **Example**:
  ```json
  "review": {
    "template": "Please review the following code: {{selection}}",
    "description": "Reviews the selected code block",
    "agent": "reviewer"
  }
  ```

### 3. MCP (Model Context Protocol)
- **Local Server**:
  ```json
  "my-local-mcp": {
    "type": "local",
    "command": ["python", "/path/to/server.py"],
    "enabled": true
  }
  ```
- **Remote Server**:
  ```json
  "my-remote-mcp": {
    "type": "remote",
    "url": "https://mcp.example.com",
    "enabled": true
  }
  ```

### 4. Frontmatter
Every Skill must start with this block:
```yaml
---
name: name-of-skill
description: Comprehensive description for triggering.
---
```

### 5. Plugin
List of plugin names:
```json
"plugin": [
  "opencode-plugin-git",
  "opencode-plugin-search"
]
```

### 6. Agent Skill (Folder Structure)
When creating a full skill:
1. Create directory: `skills/<namespace>/<skill-name>/`
2. Create `SKILL.md` with YAML frontmatter.
3. (Optional) Create `scripts/`, `references/`, `assets/`.

### 7. Tool
Enable tools in the `tools` config:
```json
"tools": {
  "edit": true,
  "bash": true
}
```

## Workflow
1. Identify the component type requested.
2. Read [references/schema.json](references/schema.json) for the exact property paths and constraints.
3. Generate the JSON/YAML/Markdown content.
4. For skills, verify the directory structure follows the standard.
