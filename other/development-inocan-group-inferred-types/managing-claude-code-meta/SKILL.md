---
name: managing-claude-code-meta
description: "MUST be loaded when setting up, installing, migrating, reviewing, auditing, or checking CLAUDE.md files in projects. Covers installing the promode CLAUDE.md into new projects, migrating existing CLAUDE.md content to READMEs (progressive disclosure), and auditing projects for conformance. Invoke PROACTIVELY when user mentions CLAUDE.md, project setup, agent configuration, or code meta files."
---

<essential_principles>
This skill manages projects that adopt the **promode methodology** — a set of principles and workflows for AI agents to develop software. The methodology emphasises TDD, context conservation, progressive disclosure, and clear delegation patterns.

**1. CLAUDE.md is for main agent behaviour**
CLAUDE.md defines the main agent's role: conversing with users, delegating to sub-agents, and following the promode methodology. It does NOT contain project-specific technical details — those belong in README.md files.

**2. Sub-agents use the promode-subagent**
Claude Code sub-agents don't inherit CLAUDE.md. The `promode-subagent` mirrors the same methodology so sub-agents apply the same principles. Main agents delegate to promode-subagent rather than instructing sub-agents to read CLAUDE.md.

**3. README.md files are the knowledge graph**
Each package/directory can have a README.md with domain-specific context. Agents read these just-in-time when working in that area. This keeps initial context lean while making deep knowledge available.

**4. Tests are the documentation**
Long-lived markdown should cover architecture and principles only. Detailed behaviour documentation belongs in executable tests. If behaviour isn't tested, it's not guaranteed.

**5. CLAUDE.md is standardised**
The standard CLAUDE.md (`standard/MAIN_AGENT_CLAUDE.md`) should be copied exactly into projects. It is designed to work universally. All project-specific content belongs in README.md files.
</essential_principles>

<never_do>
- NEVER modify `standard/MAIN_AGENT_CLAUDE.md` content — it must be copied exactly into projects
- NEVER add project-specific content to CLAUDE.md (use README.md files instead)
- NEVER duplicate content between CLAUDE.md and README.md — single source of truth
- NEVER skip verifying CLAUDE.md matches the standard after installation or migration
</never_do>

<escalation>
Stop and ask the user when:
- Project is not under git version control or has uncommited changes
- Content doesn't fit KEEP/MOVE/DELETE categories during migration
- Existing README.md files conflict with the suggested structure
- You've attempted the same step 3+ times without success
- Changes would affect more than 10 files
</escalation>

<intake>
What would you like to do?

1. **Install** — Set up the standard CLAUDE.md in a new project
2. **Migrate** — Refactor an existing CLAUDE.md, moving content to READMEs
3. **Audit** — Check if a project follows progressive disclosure principles

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action | Workflow |
|----------|-------------|----------|
| 1, "install", "setup", "new", "create" | Confirm project path | workflows/install.md |
| 2, "migrate", "refactor", "move", "convert" | Analyze existing CLAUDE.md | workflows/migrate.md |
| 3, "audit", "check", "review", "assess" | Scan project structure | workflows/audit.md |

**Intent-based routing:**
- "set up CLAUDE.md", "add agent config" → workflows/install.md
- "CLAUDE.md is too big", "slim down", "refactor" → workflows/migrate.md
- "is this right?", "check conformance" → workflows/audit.md

**After reading the workflow, follow it exactly.**
</routing>

<quick_reference>
**CLAUDE.md**: Copy `standard/MAIN_AGENT_CLAUDE.md` exactly. Do not modify. This configures the main agent with promode methodology.

**Sub-agents**: Main agents delegate to `promode-subagent`, which already knows the methodology.

**README.md distribution:**
```
project/
├── CLAUDE.md           # Main agent behaviour (promode methodology)
├── README.md           # Project overview, links to main components of system, etc
└── docs/
    └── {feature}/      # Ephemeral planning docs, and task specs
```
</quick_reference>

<reference_index>
- `standard/MAIN_AGENT_CLAUDE.md` — The canonical CLAUDE.md (copy exactly into projects)
- `references/progressive-disclosure.md` — Why and how to distribute content to READMEs
- `references/claude-md-sections.md` — Purpose of each CLAUDE.md section
</reference_index>

<workflows_index>
All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| install.md | Install standard CLAUDE.md into new project |
| migrate.md | Migrate existing CLAUDE.md content to READMEs |
| audit.md | Audit project for progressive disclosure conformance |
</workflows_index>

<success_criteria>
A well-configured project:

- CLAUDE.md is an exact copy of `standard/MAIN_AGENT_CLAUDE.md`
- README.md at project root with overview and navigation
- Component README.md files throughout for domain-specific context
- Tests document system behaviour, not markdown files
</success_criteria>
