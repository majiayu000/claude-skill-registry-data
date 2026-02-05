---
name: managing-claude-code-meta
description: "MUST be loaded when setting up, installing, migrating, reviewing, auditing, or checking CLAUDE.md files in projects. Covers installing the promode CLAUDE.md into new projects, migrating existing CLAUDE.md content to AGENT_ORIENTATION.md (progressive disclosure), and auditing projects for conformance. Invoke PROACTIVELY when user mentions CLAUDE.md, project setup, agent configuration, or code meta files."
---

<essential_principles>
This skill manages projects that adopt the **promode methodology** — a set of principles and workflows for AI agents to develop software. The methodology emphasises TDD, context conservation, progressive disclosure, and clear delegation patterns.

**1. CLAUDE.md is for main agent behaviour**
CLAUDE.md defines the main agent's role: conversing with users, delegating to sub-agents, and following the promode methodology. It does NOT contain project-specific technical details — those belong in AGENT_ORIENTATION.md.

**2. Sub-agents use phase-specific agents**
Claude Code sub-agents don't inherit CLAUDE.md. Promode provides phase-specific agents (implementer, reviewer, debugger) with the methodology baked in. Main agents handle brainstorming, planning, and orchestration directly, then delegate execution to the appropriate phase agent.

**3. AGENT_ORIENTATION.md is the agent knowledge graph**
Each package/directory can have an AGENT_ORIENTATION.md with compact, token-efficient guidance for agents. This is distinct from README.md (which is for humans). Agents read these just-in-time when working in that area.

**4. Tests are the documentation**
Long-lived markdown should cover architecture and principles only. Detailed behaviour documentation belongs in executable tests. If behaviour isn't tested, it's not guaranteed.

**5. CLAUDE.md is standardised**
The standard CLAUDE.md (`standard/MAIN_AGENT_CLAUDE.md`) should be copied exactly into projects. It is designed to work universally. All project-specific content belongs in AGENT_ORIENTATION.md.
</essential_principles>

<never_do>
- NEVER modify `standard/MAIN_AGENT_CLAUDE.md` content — it must be copied exactly into projects
- NEVER add project-specific content to CLAUDE.md (use AGENT_ORIENTATION.md instead)
- NEVER duplicate content between CLAUDE.md and AGENT_ORIENTATION.md — single source of truth
- NEVER skip verifying CLAUDE.md matches the standard after installation or migration
</never_do>

<escalation>
Stop and ask the user when:
- Project is not under git version control or has uncommited changes
- Content doesn't fit KEEP/MOVE/DELETE categories during migration
- Existing AGENT_ORIENTATION.md conflicts with the suggested structure
- You've attempted the same step 3+ times without success
- Changes would affect more than 10 files
</escalation>

<intake>
What would you like to do?

1. **Install** — Set up promode in a new project (no existing CLAUDE.md)
2. **Update** — Update an existing promode installation to the latest version
3. **Migrate** — Refactor a non-promode CLAUDE.md, moving content to AGENT_ORIENTATION.md
4. **Audit** — Check if a project follows progressive disclosure principles

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action | Workflow |
|----------|-------------|----------|
| 1, "install", "setup", "new", "create" | Confirm project path | workflows/install.md |
| 2, "update", "upgrade", "latest", "refresh" | Check existing installation | workflows/update.md |
| 3, "migrate", "refactor", "move", "convert" | Analyze existing CLAUDE.md | workflows/migrate.md |
| 4, "audit", "check", "review", "assess" | Scan project structure | workflows/audit.md |

**Intent-based routing:**
- "set up CLAUDE.md", "add agent config", "install promode" → workflows/install.md
- "update promode", "get latest", "upgrade", "update CLAUDE.md" → workflows/update.md
- "CLAUDE.md is too big", "slim down", "refactor existing" → workflows/migrate.md
- "is this right?", "check conformance", "audit" → workflows/audit.md

**Key distinction:**
- **Install** = No promode yet, start fresh
- **Update** = Promode exists, bring to latest version and ensure all components present
- **Migrate** = Has CLAUDE.md but it's not promode (contains project-specific content)
- **Audit** = Read-only check, no modifications

**After reading the workflow, follow it exactly.**
</routing>

<quick_reference>
**CLAUDE.md**: Copy `standard/MAIN_AGENT_CLAUDE.md` exactly. Do not modify. This configures the main agent with promode methodology.

**Sub-agents**: Main agents delegate execution to phase-specific agents (implementer, reviewer, debugger), which already know the methodology. Brainstorming, planning, and orchestration are done by the main agent.

**Promode project structure:**
```
project/
├── CLAUDE.md              # Main agent behaviour (promode methodology)
├── KANBAN_BOARD.md        # Project tracking across sessions
├── AGENT_ORIENTATION.md   # Compact agent guidance (tools, patterns, gotchas)
├── .mcp.json              # MCP server configuration
├── README.md              # Human documentation (optional, for GitHub etc)
└── packages/
    └── {package}/
        └── AGENT_ORIENTATION.md  # Package-specific agent guidance
```
</quick_reference>

<reference_index>
- `standard/MAIN_AGENT_CLAUDE.md` — The canonical CLAUDE.md (copy exactly into projects)
- `references/progressive-disclosure.md` — Why and how to distribute content to AGENT_ORIENTATION.md
</reference_index>

<workflows_index>
All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| install.md | Install promode into new project |
| update.md | Update existing promode installation to latest version |
| migrate.md | Migrate non-promode CLAUDE.md content to AGENT_ORIENTATION.md |
| audit.md | Audit project for progressive disclosure conformance |
</workflows_index>

<success_criteria>
A well-configured project has these components:

**Required:**
- CLAUDE.md — exact copy of `standard/MAIN_AGENT_CLAUDE.md`
- KANBAN_BOARD.md — project tracking across sessions
- AGENT_ORIENTATION.md — compact agent guidance at project root
- .mcp.json — MCP servers configured (context7, exa, grep_app)

**Recommended:**
- Package AGENT_ORIENTATION.md files for domain-specific context
- LSP configured for detected languages
- Tests document system behaviour, not markdown files
- README.md exists for humans (GitHub, etc) but is not agent-oriented
</success_criteria>
