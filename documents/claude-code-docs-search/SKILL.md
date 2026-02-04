---
name: claude-code-docs-search
description: Search local Claude Code documentation to answer implementation questions. Use when asked about Claude Code features, subagents, workflows, skills, hooks, MCP servers, plugins, settings, CLI options, headless mode, or any Claude Code capability.
allowed-tools: Read, Grep, Glob
---

# Claude Code Documentation Search

Search the local `docs/` folder to answer questions about Claude Code implementation details.

## Instructions

1. **Start with the index** - Read `docs/index.txt` to see available documentation files and their topics

2. **In addition: Search for specific terms** - In addition to identifying docs based on their description in index.txt, use grep to find relevant content:
   Examples:
   ```
   Grep pattern="subagent" path="docs/"
   Grep pattern="hooks" path="docs/"
   ```

3. **Read relevant files** - Once you identify relevant docs, read them fully:
   Examples:
   ```
   Read file_path="docs/sub-agents.md"
   Read file_path="docs/hooks.md"
   ```

4. **Cite your sources** - Always reference which documentation file(s) your answer comes from

## Documentation Topics

Key files for common questions:
- `sub-agents.md` - Task tool, agent types, parallel execution
- `hooks.md`, `hooks-guide.md` - Lifecycle hooks, shell commands on events
- `skills.md` - Creating and using skills
- `mcp.md` - MCP server configuration
- `plugins.md`, `plugins-reference.md` - Plugin development
- `headless.md` - Non-interactive/CI usage
- `cli-reference.md` - Command line options
- `settings.md` - Configuration options
- `memory.md` - CLAUDE.md and context management

## Example Queries

- "How do I create a subagent?"
- "What hooks are available?"
- "How do I configure MCP servers?"
- "What settings can I customize?"
- "How does Claude Code work?"