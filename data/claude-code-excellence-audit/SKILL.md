---
name: claude-code-excellence-audit
description: Audits Claude Code project setup and provides score with recommendations. Use when user asks about Claude Code setup, configuration quality, or wants to improve their Claude Code configuration.
allowed-tools: Bash, Read, Glob, Grep
---

# Claude Code Excellence Audit Skill

You are an expert at auditing Claude Code configurations. When invoked, perform a comprehensive audit of the user's Claude Code setup.

## Trigger Phrases

Activate when user says things like:
- "audit my claude code setup"
- "how is my claude code configured"
- "check my claude code configuration"
- "score my claude code setup"
- "improve my claude code"
- "claude code best practices"

## Audit Process

### 1. Discovery Phase

Check these locations:

**Global (User-Level):**
- `~/.claude/CLAUDE.md` - Personal memory
- `~/.claude/rules/` - Personal rules
- `~/.claude/settings.json` - User settings
- `~/.claude/commands/` - Personal commands
- `~/.claude/agents/` - Personal agents
- `~/.claude/skills/` - Personal skills

**Project-Level:**
- `./CLAUDE.md` or `./.claude/CLAUDE.md` - Project memory
- `./CLAUDE.local.md` - Local secrets/config
- `./.claude/rules/` - Project rules
- `./.claude/settings.json` - Project settings
- `./.claude/settings.local.json` - Local settings
- `./.claude/commands/` - Project commands
- `./.claude/agents/` - Project agents
- `./.claude/skills/` - Project skills
- `./.mcp.json` - MCP servers

### 2. Scoring Rubric (100 Points)

| Category | Max | Key Checks |
|----------|-----|------------|
| Memory | 25 | CLAUDE.md with build commands, code style, architecture |
| Rules | 15 | Modular rules in .claude/rules/, path-scoping |
| Settings | 15 | Permission allow/deny lists, sandbox enabled |
| Subagents | 15 | Custom agents with tool restrictions |
| Commands | 10 | Custom slash commands with frontmatter |
| Hooks | 10 | PostToolUse, PreToolUse, Stop hooks |
| MCP | 5 | External tool integrations |
| Skills | 5 | Model-invoked capabilities |

### 3. Output Format

Provide a visual report with:
- Overall score and grade
- Category breakdown with progress bars
- Strengths (what's done well)
- Gaps (what's missing)
- Specific recommendations with code
- Prioritized action plan

### 4. Recommendations

For each gap, provide:
1. Clear description of what's missing
2. Why it matters (impact on productivity)
3. Exact code/commands to implement the fix
4. Points gained by implementing

## Quality Standards

A perfect 100/100 setup has:

- **Memory**: Comprehensive CLAUDE.md with build commands, code style, architecture
- **Rules**: 3+ modular rule files with path-scoping for different areas
- **Settings**: Permission allow-list for safe commands, deny-list for secrets
- **Subagents**: At least 2 custom agents (e.g., code-reviewer, debugger)
- **Commands**: Useful project shortcuts with arguments support
- **Hooks**: Auto-formatting, validation, completion checks
- **MCP**: Relevant external integrations (GitHub, database, etc.)
- **Skills**: Domain-specific capabilities for automatic invocation

## Example Recommendations

Always provide ready-to-use code blocks that can be directly copied and executed.
