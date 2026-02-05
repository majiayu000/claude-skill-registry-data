---
name: thx-boris
description: Meta-workflow for using Claude Code effectively, based on patterns from Boris Cherny (Claude Code creator). Use when setting up a new project with Claude Code, optimizing an existing workflow, creating CLAUDE.md files, designing subagents, configuring hooks, or running parallel Claude sessions. Triggers on "how should I structure my CLAUDE.md", "create a subagent for X", "set up hooks", "optimize my Claude Code setup".
---

# thx-boris: Claude Code Mastery

Production-tested patterns for maximizing Claude Code effectiveness, based on workflows from the Claude Code team.

---

## The Living CLAUDE.md Pattern

**Core principle:** Every Claude mistake becomes a permanent lesson.

### Structure

```markdown
# Development Workflow

**Always use `[package-manager]`, not `[alternative]`.**

## Commands
[Ordered by frequency of use]

## Code Style
[Project-specific patterns Claude should follow]

## Anti-Patterns
[Things Claude got wrong - add new ones as discovered]

## Domain Knowledge
[Project-specific context Claude needs]
```

### The Feedback Loop

```
Claude makes mistake → Human notices → Add to CLAUDE.md → Claude never repeats
```

**Real example from Claude Code repo:**
```markdown
# Before (Claude used enum)
- Prefer `type` over `interface`; avoid `enum` (use string unions)

# After (strengthened after violation)
- Prefer `type` over `interface`; **never use `enum`** (use string literal unions instead)
```

### Team CLAUDE.md Protocol

For team projects, CLAUDE.md is a shared artifact:
1. Check into git alongside code
2. All team members contribute
3. Review CLAUDE.md changes in PRs
4. Treat as living documentation

---

## Subagent Design

Subagents are specialized Claude instances with focused responsibilities. Store in `.claude/agents/`.

### When to Create Subagents

| Task Type | Subagent? | Rationale |
|-----------|-----------|-----------|
| Repetitive validation | ✅ Yes | Consistent checks |
| Code review patterns | ✅ Yes | Domain expertise |
| Complex multi-step | ✅ Yes | Focused context |
| One-off tasks | ❌ No | Overhead not worth it |

### Subagent Templates

See `references/subagent-templates.md` for complete templates:
- **build-validator** - Verify builds pass before commit
- **code-architect** - High-level design decisions
- **code-simplifier** - Reduce complexity
- **oncall-guide** - Production incident response
- **verify-app** - End-to-end application testing

### Creating a Subagent

```bash
# Create agent file
touch .claude/agents/[agent-name].md

# Agent file structure:
# 1. Purpose (one line)
# 2. Trigger conditions
# 3. Step-by-step procedure
# 4. Success criteria
# 5. Handoff instructions
```

---

## Hook Automation

Hooks run automatically before/after Claude actions. Configure in `.claude/settings.json`.

### Common Patterns

**Auto-format on write:**
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "bun run format || true"
    }]
  }]
}
```

**Lint before commit:**
```json
{
  "PreToolUse": [{
    "matcher": "Bash(git commit*)",
    "hooks": [{
      "type": "command",
      "command": "bun run lint:claude && bun run test"
    }]
  }]
}
```

See `references/hooks-patterns.md` for complete hook configurations.

---

## Permission Optimization

Pre-allow safe commands to reduce friction. Access via `/permissions` command.

### Safe to Pre-Allow

```
# Build & test commands
Bash(bun run build:*)
Bash(bun run lint:*)
Bash(bun run test:*)
Bash(bun run typecheck:*)
Bash(npm run build:*)
Bash(npm run lint:*)
Bash(npm run test:*)
Bash(yarn build:*)
Bash(yarn lint:*)
Bash(yarn test:*)
Bash(pnpm build:*)
Bash(pnpm lint:*)
Bash(pnpm test:*)

# Git read operations
Bash(git status)
Bash(git diff*)
Bash(git log*)
Bash(git branch*)
Bash(git show*)

# File exploration
Bash(find:*)
Bash(grep:*)
Bash(cat:*)
Bash(head:*)
Bash(tail:*)
Bash(ls:*)
Bash(tree:*)
Bash(wc:*)
```

### Never Pre-Allow

```
Bash(rm -rf *)
Bash(git push -f *)
Bash(git reset --hard *)
Bash(sudo *)
Bash(curl * | bash)
Bash(chmod 777 *)
Bash(> /dev/*)
```

### Personal Overrides with settings.local.json

For personal permissions that shouldn't be committed:

```bash
# Create personal settings (gitignored)
touch .claude/settings.local.json
```

```json
// .claude/settings.local.json
{
  "permissions": {
    "allow": ["Bash(my-custom-script)"]
  }
}
```

---

## Parallel Orchestration

Running multiple Claudes maximizes throughput for complex projects.

### Terminal Strategy (Boris Pattern)

```
Tab 1: Feature A implementation
Tab 2: Tests for Feature A
Tab 3: Feature B implementation
Tab 4: Bug fixes
Tab 5: Documentation
```

**Key setup:**
1. Number tabs 1-5 for quick switching
2. Enable system notifications for when Claude needs input
3. Use descriptive window titles

### Git Worktrees (Recommended for True Parallelism)

Multiple terminals in the same directory can cause conflicts. Use git worktrees instead:

```bash
# Create worktrees for parallel work
git worktree add ../myproject-feature-a feature-a
git worktree add ../myproject-feature-b feature-b
git worktree add ../myproject-tests main

# Each worktree gets its own Claude instance
cd ../myproject-feature-a && claude
cd ../myproject-feature-b && claude
```

**Benefits:**
- No file conflicts between Claude instances
- Each branch is completely isolated
- Easy cleanup: `git worktree remove ../myproject-feature-a`

### Web + Terminal Hybrid

```
Terminal Claudes: Deep implementation work (numbered tabs)
Web Claudes: Research, docs, parallel exploration

Handoff patterns:
- Terminal → Web: Use & to background session
- Web → Terminal: Use --resume to continue locally
```

### Task Decomposition for Parallelization

```
❌ Bad: "Implement the entire authentication system"
✅ Good: Split into parallel tracks:
   - Claude 1: Auth API endpoints
   - Claude 2: Auth UI components
   - Claude 3: Auth tests
   - Claude 4: Auth documentation
```

---

## Custom Slash Commands

Create project-specific commands for common workflows.

### Example: /commit-push-pr

```markdown
# .claude/commands/commit-push-pr.md
Commit all changes with a descriptive message, push to origin, and open a PR.

Steps:
1. Stage all changes
2. Generate commit message from diff
3. Push to current branch
4. Create PR with description from commits
```

### Command Design Principles

1. **Atomic** - One clear outcome
2. **Idempotent** - Safe to run multiple times
3. **Verbose** - Log what's happening
4. **Recoverable** - Handle failures gracefully

---

## Model Selection

**Default: Opus 4.5 with thinking**

Why Opus over Sonnet for complex work:
- Less steering required
- Better tool use
- Fewer mistakes = faster overall
- Thinking mode catches edge cases

When Sonnet is acceptable:
- Simple, well-defined tasks
- High-volume, low-complexity work
- When latency matters more than quality

---

## MCP Integration

Connect Claude to external services via MCP servers.

### Example: Slack Integration

```json
// .mcp.json
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://slack.mcp.anthropic.com/mcp"
    }
  }
}
```

### Available First-Party MCPs

| MCP Server | Use Case |
|------------|----------|
| Slack | Send messages, read channels |
| Google Drive | Read/write docs, sheets |
| GitHub | Issues, PRs, code search |
| Sentry | Error tracking, issue lookup |
| PostgreSQL | Direct database queries |
| Puppeteer | Browser automation, screenshots |
| Filesystem | Extended file operations |

### Example: Multiple MCPs

```json
// .mcp.json
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://slack.mcp.anthropic.com/mcp"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/sse"
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

---

## Session Management

### Continue Previous Sessions

```bash
# Resume last session
claude --continue

# Resume specific session by ID
claude --resume <session-id>

# List recent sessions
claude sessions list
```

### Headless / CI Mode

Run Claude non-interactively for automation:

```bash
# Single task, output to stdout
claude -p "fix all TypeScript errors" --output-format json

# With file output
claude -p "generate API documentation" > docs/api.md

# In CI pipeline
claude -p "review this PR for security issues" --output-format json | jq '.result'
```

### Memory Commands

```bash
# Save context for future sessions
/memory add "This project uses pnpm, not npm"
/memory add "API responses follow JSON:API spec"

# View saved memories
/memory list

# Clear memories
/memory clear
```

---

## Quick Reference

| Task | Solution |
|------|----------|
| Claude repeats mistake | Add to CLAUDE.md |
| Repetitive workflow | Create subagent |
| Auto-format code | PostToolUse hook |
| Reduce permission prompts | /permissions allow |
| Complex feature | Parallel Claudes |
| Common multi-step | Custom slash command |

---

## References

- `references/subagent-templates.md` - Complete subagent templates
- `references/hooks-patterns.md` - Hook configuration examples
- `references/troubleshooting.md` - Common issues and fixes
- `references/anti-patterns.md` - What NOT to do
- `assets/agents/` - Ready-to-use agent files
- `CLAUDE.md.template` - Copy-paste starter for new projects
