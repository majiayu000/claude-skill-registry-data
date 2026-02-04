---
name: claude-permissions
description: Configure, manage, update and review Claude Code permissions, sandboxing, and tool access. Use when user wants to set up permissions, configure sandboxing, update allowed tools, manage settings.json permissions, or review permissions in skills or commands or agents or settings.json. When user writes a new skill, command, agent, or updates settings.json, they should use this skill to manage permissions.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Claude Code Permissions Management

Guide for configuring permissions, sandboxing, and tool access in Claude Code.

## Overview

Claude Code uses a tiered permission system to balance functionality and security. Permissions control what actions Claude can perform without explicit approval.

## Permission Tiers

### Read-Only Operations (No Approval Required)

These operations are automatically allowed:

- **FileReadTool**: Reading file contents
- **LSTool**: Listing files and directories
- **GrepTool**: Searching text within files
- **GlobTool**: Finding files matching patterns
- **NotebookReadTool**: Reading Jupyter notebook content

### Bash Commands (Requires Approval)

**BashTool** execution requires user approval. Users can:

- Approve individual commands
- Choose "Always allow" for specific commands in a project directory
- Configure persistent permissions in `settings.json`

### File Modifications (Requires Approval)

These operations require session-based approval:

- **FileEditTool**: Making partial edits to files
- **FileWriteTool**: Creating or overwriting files
- **NotebookEditTool**: Modifying cells in Jupyter notebooks

## Available Tools

Claude Code provides these tools:

- **AgentTool**: Runs sub-agents for multi-step tasks
- **BashTool**: Executes shell commands
- **GlobTool**: Finds files matching patterns
- **GrepTool**: Searches text within files
- **LSTool**: Lists files and directories
- **FileReadTool**: Reads file contents
- **FileEditTool**: Makes partial edits to files
- **FileWriteTool**: Creates or overwrites files
- **NotebookReadTool**: Reads Jupyter notebook content
- **NotebookEditTool**: Modifies cells in Jupyter notebooks

## Managing Permissions

### Method 1: `/permissions` Command

Use the `/permissions` command to access the interactive UI for managing permissions:

- **Allow**: Grant Claude Code permission to use specified tools without further approval
- **Ask**: Prompt for confirmation each time a tool is used
- **Deny**: Prevent the use of specified tools entirely

### Method 2: `settings.json` Configuration

Configure persistent permissions in `.claude/settings.json` or `~/.claude.json`:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(git status)",
      "Bash(git commit -m:*)"
    ],
    "deny": ["Read(.env*)", "Bash(rm -rf /)", "Bash(sudo:*)"],
    "ask": ["Bash(git push --force:*)", "Bash(docker run:*)"]
  }
}
```

### Method 3: `/allowed-tools` Command

Use CLI to add or remove tools from allowlist:

- Add: `/allowed-tools +Edit`
- Remove: `/allowed-tools -Bash`
- Pattern: `/allowed-tools +Bash(git commit:*)`

### Method 4: Session Flags

Use `--allowedTools` flag for session-specific permissions (not persistent).

## Permission Patterns

### Tool Patterns

- **Simple tool**: `"Read"`, `"Write"`, `"Edit"`, `"Bash"`
- **Specific command**: `"Bash(git status)"`
- **Command pattern**: `"Bash(git commit:*)"` (matches all git commit commands)
- **File pattern**: `"Read(.env*)"` (matches .env files)
- **Directory pattern**: `"Read(./secrets/**)"` (matches files in secrets directory)

### Wildcard Patterns

- `*` matches any string
- `**` matches directories recursively
- Pattern matching is case-sensitive

### Skill and SlashCommand Patterns

- **All slash commands**: `"SlashCommand(*)"`
- **Specific main skill**: `"Skill(typescript-coding)"`
- **All plugin skills**: `"Skill(plugin-name:*)"` (e.g., `"Skill(meta-work:*)"`)
- **Specific plugin skill**: `"Skill(plugin-name:skill-name)"` (e.g., `"Skill(meta-work:prompting)"`)
- **Note**: `Skill(*)` may not work for plugin-scoped skills; use explicit names or plugin wildcards

## Sandboxing

Sandboxing provides filesystem and network isolation to enhance security and reduce permission prompts.

### Benefits

- **Filesystem Isolation**: Restricts Claude's access to specified directories
- **Network Isolation**: Limits network access to approved servers
- **Reduced Prompts**: Auto-approve commands within sandbox boundaries
- **Protection**: Mitigates risks like data exfiltration or malicious downloads

### Configuration

Add sandboxing configuration to `settings.json`:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "npm"],
    "network": {
      "allowUnixSockets": ["/path/to/socket"],
      "allowLocalBinding": false
    }
  }
}
```

### Sandbox Options

- **enabled**: Enable bash sandboxing (default: false)
- **autoAllowBashIfSandboxed**: Auto-approve bash commands when sandboxed (default: true)
- **excludedCommands**: Commands that should run outside the sandbox
- **network.allowUnixSockets**: Accessible Unix socket paths within sandbox
- **network.allowLocalBinding**: Allow binding to localhost ports (macOS only, default: false)

## Best Practices

### Security

1. **Deny Dangerous Operations**: Block destructive commands (rm -rf, sudo, etc.)
2. **Protect Sensitive Files**: Deny access to `.env`, credentials, secrets
3. **Use Sandboxing**: Enable sandboxing for enhanced security
4. **Principle of Least Privilege**: Grant minimum permissions needed

### Productivity

1. **Allow Common Commands**: Pre-approve frequently used git/npm commands
2. **Pattern Matching**: Use wildcards for command families (`Bash(git:*`)
3. **Team Consistency**: Check `settings.json` into source control for team-wide permissions
4. **Exclude from Sandbox**: Add trusted commands to `excludedCommands` if needed

### Organization

1. **Project-Level**: Use `.claude/settings.json` for project-specific permissions
2. **User-Level**: Use `~/.claude.json` for personal preferences
3. **Documentation**: Document why specific permissions are granted
4. **Regular Review**: Periodically review and audit permissions

## Examples

### Allow Git Operations

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git commit -m:*)",
      "Bash(git push origin:*)"
    ],
    "ask": ["Bash(git push --force:*)", "Bash(git rebase:*)"]
  }
}
```

### Protect Sensitive Files

```json
{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Write(.env*)",
      "Read(./secrets/**)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/credentials)"
    ]
  }
}
```

### Safe Development Environment

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(git:* except: git push --force, git rebase)",
      "Bash(pnpm:* except: pnpm remove)"
    ],
    "deny": ["Read(.env*)", "Bash(rm -rf /)", "Bash(sudo:*)"],
    "ask": ["Bash(git push --force:*)", "Bash(docker run:*)"]
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git"]
  }
}
```

### Allow All Skills and Commands

```json
{
  "permissions": {
    "allow": [
      "SlashCommand(*)",
      "Skill(analyze-size)",
      "Skill(brainwriting)",
      "Skill(scratchpad-fetch)",
      "Skill(timestamp)",
      "Skill(typescript-coding)",
      "Skill(meta-work:*)",
      "Skill(development-lifecycle:*)"
    ]
  }
}
```

## Skills and Agents

### Skill-Level Permissions

Skills can restrict tool access using `allowed-tools` in frontmatter:

```yaml
---
name: safe-reader
description: Read-only file operations
allowed-tools: Read, Grep, Glob
---
```

### Agent-Level Permissions

Agents (subagents) can be configured with specific tool permissions at:

- User-level: `~/.claude/agents/` (available across all projects)
- Project-level: `.claude/agents/` (shareable with team)

Each agent can have custom prompts and tool permissions defined in their YAML frontmatter.

## Troubleshooting

### Permission Denied

- Check `settings.json` for deny rules matching the operation
- Verify permission pattern matches the command/file path
- Check both project-level and user-level settings files

### Too Many Prompts

- Enable sandboxing to reduce prompts
- Add frequently used commands to allow list
- Use pattern matching for command families

### Sandbox Not Working

- Verify `sandbox.enabled` is `true`
- Check `excludedCommands` if commands should run outside sandbox
- Ensure network restrictions aren't blocking needed connections

## References

- [Claude Code Permissions Documentation](https://docs.anthropic.com/en/docs/claude-code/team)
- [Claude Code Settings Documentation](https://docs.claude.com/en/docs/claude-code/settings)
- [Sandboxing Documentation](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Agent Skills Documentation](https://anthropic.mintlify.app/en/docs/agents-and-tools/agent-skills/overview)
