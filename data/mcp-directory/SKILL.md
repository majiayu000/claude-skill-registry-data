---
name: mcp-directory
description: Complete directory of available MCP servers with usage guidelines, tool categories, and selection criteria. Helps Claude choose the right MCP for each task and avoid token waste.
---

# MCP Directory

## Purpose
This skill provides a master index of all available MCP servers in Kurt's environment, when to use each one, and how to choose between overlapping capabilities. Critical for reducing token waste and avoiding MCP confusion.

## When Claude Should Use This Skill
- At the start of conversations involving external tools
- When deciding between multiple MCPs for a task
- When Desktop Commander hangs or fails
- When confused about which tools are available
- Before loading heavy MCPs like GitHub (100+ tools)

## Available MCP Servers

### 1. n8n MCP (Railway-hosted)
**Status:** Active and Reliable
**Connection:** Railway-hosted server
**Token Cost:** Medium (~5-8k tokens)

**Use When:**
- Creating, deploying, or managing n8n workflows
- Building long-running automations
- Scheduling tasks (cron jobs)
- Integrating multiple systems
- Need workflow execution history

**Capabilities:**
- Workflow CRUD operations
- Node configuration
- Execution management
- Deployment across environments (dev/staging/prod)

**Best For:**
- Multi-step automations
- Webhook handlers
- Scheduled tasks
- Integration workflows

**Don't Use For:**
- Quick one-off scripts
- Synchronous operations needing immediate response

---

### 2. GitHub MCP
**Status:** Active and Reliable
**Connection:** Direct GitHub API integration
**Token Cost:** HIGH (~40-50k tokens for full tool list)

**Use When:**
- ANY GitHub operation (repos, PRs, issues, branches, commits)
- Code search across repositories
- Managing pull request reviews
- Creating or updating files IN GitHub repositories
- Branch and release management

**Capabilities:**
- 100+ tools covering all GitHub operations
- Repository management
- Pull request workflows (create, review, merge)
- Issue tracking and sub-issues
- Code search (very powerful)
- Branch and commit operations
- Team and user management

**Best For:**
- Source control operations
- Code review workflows
- Project management via GitHub Issues
- Release management

**CRITICAL: Use This Instead Of Desktop Commander For:**
- Reading files from GitHub repos
- Writing files to GitHub repos
- Any GitHub-related operations

**Token Management:**
- GitHub MCP is EXPENSIVE in tokens
- Only use when actually needed for GitHub operations
- Prefer specific tool calls over exploratory searches
- This is why this skill exists - to guide proper usage

---

### 3. Linear MCP
**Status:** Active and Reliable
**Connection:** Direct Linear API integration
**Token Cost:** Medium (~8-10k tokens)

**Use When:**
- Managing Linear issues (create, update, read)
- Project management and sprint planning
- Adding comments to issues
- Managing labels and status
- Coordinating team workflows
- Creating sub-issues or issue relationships

**Capabilities:**
- Issue CRUD operations
- Comment management
- Label and status tracking
- Project and cycle management
- Team coordination
- GraphQL query support

**Best For:**
- Software project management
- Sprint planning and tracking
- Issue workflow automation
- Team collaboration

**Don't Use For:**
- Personal task management (use Google Tasks)
- Code-related tasks (use GitHub Issues)

---

### 4. Desktop Commander MCP
**Status:** BUGGY - Use With Caution
**Connection:** Local system integration
**Token Cost:** Medium (~10-15k tokens)

**Use When:**
- Local file operations (read, write, search)
- Running shell commands or scripts

- Process management (start, read output, interact)
- Directory operations
- File system searches

**Capabilities:**
- File read/write/move/delete
- Directory creation and listing
- Process execution with output capture
- File searching (content and name)
- Configuration management

**CRITICAL ISSUES:**
- Hangs frequently without warning
- No way to detect hangs programmatically
- Windows emoji/unicode encoding issues in output
- Unreliable for time-sensitive operations

**Best For:**
- Local development tasks when GitHub MCP won't work
- File operations outside of Git repositories
- Quick system commands

**NEVER Use For:**
- GitHub repository operations (use GitHub MCP)
- Operations requiring reliability
- Anything where hanging would be problematic

**Workarounds:**
- Always use timeout_ms parameter for processes
- Do simple health check first (get_config)
- If no response in 30s, assume hung
- Have fallback plan (GitHub MCP for repo files)

---

### 5. Supermemory MCP
**Status:** Active and Reliable
**Connection:** Supermemory service
**Token Cost:** Low (~2-3k tokens)

**Use When:**
- Storing user preferences or patterns
- Saving project-specific context
- Recording important decisions
- Building long-term user knowledge

**Capabilities:**
- Memory storage and retrieval
- Project-based memory organization
- Semantic search across memories
- Pattern recognition

**Best For:**
- User preferences that should persist
- Workflow patterns worth remembering
- Important decisions and context

**Don't Use For:**
- Secrets or sensitive data (use environment variables)
- Temporary session data
- Redundant information already in skills

---

### 6. Google Tasks MCP
**Status:** Active and Reliable
**Connection:** Google Tasks API
**Token Cost:** Low (~1-2k tokens)

**Use When:**
- Managing personal to-do lists
- Simple task tracking
- Quick task creation/completion

**Capabilities:**
- Task CRUD operations
- Task list management
- Due date tracking
- Task completion

**Best For:**
- Personal task management
- Simple to-do lists
- Quick reminders

**Don't Use For:**
- Complex project management (use Linear)
- Software development tasks (use Linear or GitHub Issues)
- Team collaboration (use Linear)

---

## MCP Selection Decision Tree

### For File Operations:

**Is the file in a GitHub repository?**
- YES → Use GitHub MCP (get_file_contents, create_or_update_file, push_files)
- NO → Continue below

**Is the file on the local system?**
- YES → Use Desktop Commander (with caution, expect hangs)
  - Set timeout_ms parameter
  - Have fallback plan
  - Do health check first (get_config)

**Is the file at a remote URL?**
- YES → Use Desktop Commander read_file with isUrl=true

---

### For Automation:

**Is it a long-running workflow?**
- YES → Use n8n MCP

**Is it a scheduled task?**
- YES → Use n8n MCP

**Is it a multi-step integration?**
- YES → Use n8n MCP

**Is it a quick one-off script?**
- YES → Use Desktop Commander (with caution)

---

### For Project Management:

**Is it a software development project?**
- YES → Use Linear MCP

**Is it a personal to-do?**
- YES → Use Google Tasks MCP

**Is it code-specific (bugs, features)?**
- YES → Consider GitHub Issues (via GitHub MCP) if already using GitHub
- Otherwise → Use Linear MCP

---

### For Memory/Context:

**Should this persist across sessions?**
- YES → Use Supermemory MCP

**Is it a user preference?**
- YES → Use Supermemory MCP

**Is it a pattern worth remembering?**
- YES → Use Supermemory MCP

---

## Common Anti-Patterns to Avoid

### DON'T: Use Desktop Commander for GitHub Operations
**Wrong:**
```
Desktop Commander read_file("path/in/github/repo")
```

**Right:**
```
GitHub MCP get_file_contents(owner, repo, path)
```

**Why:** GitHub MCP is designed for this, more reliable, and provides proper GitHub context.

---

### DON'T: Load GitHub MCP for Non-GitHub Tasks
**Wrong:**
```
User: "Read the local config file"
Claude: [loads entire GitHub MCP for no reason]
```

**Right:**
```
User: "Read the local config file"
Claude: [uses Desktop Commander directly]
```

**Why:** GitHub MCP costs 40-50k tokens. Don't load it unless actually working with GitHub.

---

### DON'T: Forget Desktop Commander Hangs
**Wrong:**
```
Desktop Commander start_process(long_command)
[wait forever with no timeout]
```

**Right:**
```
Desktop Commander start_process(long_command, timeout_ms=15000)
[If no response in 30s, alert user]
```

**Why:** Desktop Commander hangs frequently. Always plan for it.

---

### DON'T: Use n8n for Quick Scripts
**Wrong:**
```
User: "Run this quick calculation"
Claude: [creates entire n8n workflow]
```

**Right:**
```
User: "Run this quick calculation"
Claude: [uses Desktop Commander or analysis tool]
```

**Why:** n8n is for persistent workflows, not one-off operations.

---

## Token Cost Awareness

**High Cost MCPs (40k+ tokens):**
- GitHub MCP (~40-50k tokens)
  - Only load when actually working with GitHub
  - Justify the cost by actually using GitHub tools
  - Don't load "just in case"

**Medium Cost MCPs (5-15k tokens):**
- Desktop Commander (~10-15k tokens)
- Linear MCP (~8-10k tokens)
- n8n MCP (~5-8k tokens)
  - Reasonable to load for relevant tasks
  - Still avoid loading unnecessarily

**Low Cost MCPs (1-5k tokens):**
- Supermemory MCP (~2-3k tokens)
- Google Tasks MCP (~1-2k tokens)
  - Very light, okay to load when relevant

---

## Reliability Rankings

**Most Reliable:**
1. GitHub MCP - Rock solid
2. n8n MCP - Very reliable
3. Linear MCP - Very reliable
4. Supermemory MCP - Reliable
5. Google Tasks MCP - Reliable

**Least Reliable:**
6. Desktop Commander - FREQUENTLY HANGS
   - Always use with timeouts
   - Always have fallback plan
   - Consider alternatives first

---

## Quick Reference: Common Tasks

### "Read a file from GitHub"
→ GitHub MCP: get_file_contents

### "Read a local file"
→ Desktop Commander: read_file (with timeout)

### "Create a GitHub PR"
→ GitHub MCP: create_pull_request

### "Create a Linear issue"
→ Linear MCP: create_issue

### "Build an automation workflow"
→ n8n MCP: create workflow

### "Remember this preference"
→ Supermemory MCP: addMemory

### "Add a task to my to-do list"
→ Google Tasks MCP: create task

### "Search for code in repositories"
→ GitHub MCP: search_code (very powerful!)

---

## Integration with Other Skills

### Works With n8n-flow-builder:
- n8n-flow-builder provides workflow patterns
- mcp-directory tells me to use n8n MCP to actually build them
- Together: design (skill) + execute (MCP)

### Works With skill-manager:
- skill-manager helps create/deploy skills
- mcp-directory helps decide which MCPs to document in skills
- Together: manage skills that use MCPs effectively

### Works With github-coordinator (future skill):
- github-coordinator provides GitHub workflow patterns
- mcp-directory tells me to use GitHub MCP for execution
- Together: strategy (skill) + tactics (MCP)

---

## When This Skill Should Load

**Auto-load triggers:**
- User mentions "MCP", "tool", "server"
- Task involves external system integration
- Deciding between multiple approaches
- Beginning of conversation about automation
- When confused about available capabilities

**Manual trigger:**
- User asks "What tools do you have?"
- User asks "Can you do X?" (check MCP directory)
- Troubleshooting MCP issues

---

## Notes

- Created: 2025-10-18
- Author: Kurt Anderson
- Version: 1.0.0
- Purpose: Solve MCP confusion and token waste
- Inspired by: YouTuber's insight about GitHub MCP token bloat
- Critical for: Proper MCP selection and avoiding Desktop Commander hangs
