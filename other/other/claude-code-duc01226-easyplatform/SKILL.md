---
name: claude-code
version: 2.0.0
description: "[Tooling & Meta] Claude Code CLI setup, configuration, troubleshooting, and feature guidance. Triggers on claude code setup, hook not firing, MCP connection, context limit, skill creation, slash command setup."
infer: false
allowed-tools: Read, Bash, Grep, Glob
---

# Claude Code

## Summary

**Goal:** Help users install, configure, troubleshoot, and extend Claude Code CLI (skills, hooks, MCP, slash commands).

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Identify problem category | Setup, Hook Issues, MCP Issues, Context, Extensibility, Configuration |
| 2 | Execute category-specific diagnosis | Check prerequisites, configs, scripts, settings |
| 3 | Apply fix | Step-by-step solution with verification |
| 4 | Output report | Problem, Solution, Files Changed, Verification |

**Key Principles:**
- Load reference files on-demand per topic (10 reference docs available)
- Never modify settings without user approval
- For app code use `feature`/`debug` skills, not this one

## Purpose
Help users install, configure, troubleshoot, and extend Claude Code CLI -- Anthropic's agentic coding tool with skills, hooks, MCP servers, and slash commands.

## When to Use
- Setting up Claude Code for the first time
- Troubleshooting hooks that don't fire or produce errors
- Diagnosing MCP server connection failures
- Understanding or resolving context window limits
- Creating or modifying slash commands and agent skills
- Configuring settings (model, allowed tools, output style)

## When NOT to Use
- Writing application code -- use `feature`, `debug`, or `refactoring` skills
- Creating MCP servers from scratch -- use `mcp-builder` skill
- Managing existing MCP connections -- use `mcp-management` skill

## Workflow

### Step 1: Identify Problem Category

| User Says                                       | Category       | Go To   |
| ----------------------------------------------- | -------------- | ------- |
| "install", "set up", "authenticate"             | Setup          | Step 2A |
| "hook not firing", "hook error"                 | Hook Issues    | Step 2B |
| "MCP not connecting", "MCP error"               | MCP Issues     | Step 2C |
| "context too long", "compaction", "token limit" | Context Issues | Step 2D |
| "create skill", "create command"                | Extensibility  | Step 2E |
| "configure", "settings", "model"                | Configuration  | Step 2F |

### Step 2A: Setup
1. Check prerequisites: Node.js 18+, npm
2. Verify authentication: `claude auth status`
3. Verify project detection: check for `CLAUDE.md` in project root

### Step 2B: Hook Issues
1. Read the hook file causing issues
2. Check hook event type matches expected trigger
3. Verify hook script is executable with correct shebang
4. Check `.claude/settings.json` for hook registration
5. Test hook in isolation with mock input

**Common fixes:**
- Hook not firing: wrong event name or tool matcher pattern
- Hook errors: script not finding dependencies (check relative paths)
- Hook blocks unexpectedly: PreToolUse returning `{ "decision": "block" }` incorrectly

### Step 2C: MCP Issues
1. Check `.mcp.json` for server configuration
2. Verify the MCP server process can start manually
3. Check environment variables (API keys in `.env.local`)
4. Test connectivity: `claude mcp list`

### Step 2D: Context Issues
1. Check current context usage
2. Suggest `/compact` command if approaching limit
3. Review if large files are being read unnecessarily
4. Verify `session-resume.cjs` hook for session continuity

### Step 2E: Extensibility
1. For skills: read `references/agent-skills.md` for structure
2. For commands: create `.claude/skills/{name}.md`
3. Verify SKILL.md frontmatter has required fields (name, version, description)

### Step 2F: Configuration
1. Settings locations: `.claude/settings.json` (project), `~/.claude/settings.json` (user)
2. IMPORTANT: Never modify settings without user approval

## Output Format
```markdown
## Claude Code: [Issue/Task Summary]

### Problem
[What was wrong or what was requested]

### Solution
[Step-by-step fix or setup instructions]

### Files Changed
[List any config files modified]

### Verification
[How to confirm the fix works]
```

## Reference Guide

Load references as needed for specific topics:

| Topic | Reference File |
|-------|----------------|
| Installation & setup | `references/getting-started.md` |
| Creating skills | `references/agent-skills.md` |
| Hooks system | `references/hooks-comprehensive.md` |
| Configuration | `references/configuration.md` |
| Troubleshooting | `references/troubleshooting.md` |
| IDE integration | `references/ide-integration.md` |
| CI/CD | `references/cicd-integration.md` |
| Advanced features | `references/advanced-features.md` |
| API reference | `references/api-reference.md` |
| Best practices | `references/best-practices.md` |

## Related Skills
- `mcp-builder` -- creating new MCP servers
- `mcp-management` -- managing MCP connections
- `skill-plan` -- creating new agent skills

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
