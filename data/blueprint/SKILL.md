---
name: blueprint
description: Provides unified CLI access for Blueprint framework - gate validation, document templates, FrontMatter schemas, agent handoffs, constitutions, and agent registry.
allowed-tools: Bash, Read
---

# Blueprint

Unified CLI for the Blueprint orchestration framework.

## CRITICAL: Data Location

Blueprint project data (plans, session state, configurations) is **NOT stored in local project directories**.

**You MUST**:
- Load this skill FIRST when user asks about Blueprint projects, plans, or status
- Use `blueprint` commands to access project data

**You MUST NOT**:
- Search local directories (`./blueprint/`, `./.claude/`) for Blueprint data
- Assume "no local files" means "not initialized"

Without loading this skill, you cannot determine Blueprint project status.

## Quick Reference

| Submodule | Purpose | Data Source |
|-----------|---------|-------------|
| `aegis` | Gate validation & aspects | `blueprint/gates/` |
| `forma` | Document templates | `blueprint/templates/` |
| `frontis` | FrontMatter search & schemas | `blueprint/front-matters/` |
| `hermes` | Handoff forms | `blueprint/forms/` |
| `lexis` | Constitution viewer | `blueprint/constitutions/` |
| `plan` | Plan directory & listing | `blueprint/plans/` |
| `polis` | Agent registry | `.claude/agents/` |
| `project` | Project alias management | `~/.claude/blueprint/projects/` |

## Command Structure

```
blueprint <submodule> <subcommand> [flags] [arguments]
         │            │             │       └─ Positional values (e.g., <file>, <alias>)
         │            │             └─ Options (e.g., --list, --base, --data)
         │            └─ Submodule action (e.g., current, show, search)
         └─ Functional module (e.g., project, forma, lexis, plan)
```

**Terminology:**
- **Submodule**: Independent functional module (`aegis`, `forma`, `frontis`, `hermes`, `lexis`, `plan`, `polis`, `project`)
- **Subcommand**: Action within a submodule (`current`, `show`, `search`, `init`, `list`)
- **Flag**: Boolean switch (`--list`, `--base`, `--aspects`)
- **Argument**: Positional value (`<file>`, `<alias>`, `<gate>`)

## Commands

**How to Execute:**
1. This skill is loaded via `/blueprint` (provides this instruction)
2. Run commands in Bash using full path: `~/.claude/skills/blueprint/blueprint.sh <submodule> [args]`

```bash
# Execute via full path in Bash:
# General
blueprint --help
blueprint --list

# Aegis - Gates
blueprint aegis --list                # List all gates
blueprint aegis <gate>                # Show gate definition
blueprint aegis <gate> --aspects      # List aspects for gate
blueprint aegis <gate> <aspect>       # Show specific aspect

# Forma - Templates
blueprint forma list                  # List available templates
blueprint forma show <name>           # Show template content
blueprint forma copy <name> <dir>     # Copy template to directory (RECOMMENDED)

# Frontis - FrontMatter
blueprint frontis search <field> <value> [path]  # Search by FrontMatter
blueprint frontis show <file> [file...]          # Show frontmatter
blueprint frontis schema <type>                  # View schema
blueprint frontis schema --list                  # List schemas

# Hermes - Handoff Forms
blueprint hermes --list               # List all Handoff forms
blueprint hermes <form>               # Show Handoff form (after-*, request:*, response:*)

# Lexis - Constitutions
blueprint lexis --list                # List all agents
blueprint lexis <agent>               # Show agent constitution
blueprint lexis --base                # Show base constitution only

# Plan - Plans
blueprint plan dir                    # Get plans directory path
blueprint plan list                   # List all plans
blueprint plan list --status <status> # List plans by status (e.g., in-progress)
blueprint plan resolve <identifier>   # Resolve plan path from identifier

# Polis - Agents
blueprint polis --list                # List all agents with descriptions
blueprint polis <agent>               # Show agent instruction

# Project - Project Aliases
blueprint project init <alias> [--notes "text"]  # Initialize new project
blueprint project list                            # List all projects
blueprint project show <alias>                    # Show project details
blueprint project remove <alias> --registry [--data-dir]  # Remove project
blueprint project link <alias>                    # Link current path to project
blueprint project unlink <alias> [path]           # Unlink path from project
blueprint project rename <new-alias>              # Rename project alias
blueprint project manage                          # Scan and manage projects
blueprint project current                         # Show current project info
blueprint project current --data                  # Get data directory path
```

## Examples

```bash
# All examples below use 'blueprint' as shorthand.
# Actual execution: ~/.claude/skills/blueprint/blueprint.sh <submodule> [args]

# Find all spec documents
blueprint frontis search type spec

# View spec-lib template
blueprint forma show spec-lib

# Check gate aspects
blueprint aegis documentation --aspects

# View Handoff form
blueprint hermes after-load:standard

# Check agent constitution
blueprint lexis reviewer

# List available agents
blueprint polis --list

# Manage project aliases
blueprint project list
blueprint project init myproject --notes "My project"

# Get plans directory
blueprint plan dir

# List active plans
blueprint plan list --status in-progress

# Resolve specific plan
blueprint plan resolve 001
```

## When to Use

**Load this skill IMMEDIATELY** when user mentions:
- Blueprint project, plan, or phase
- Plan status or progress
- Project initialization or registration

Then use appropriate commands:
- **Checking status**: `project current` - determines if project is registered
- **Viewing plans**: `plan list` - shows available plans
- **Reading FrontMatter**: `frontis show` - do NOT use `head` or direct file reading
- **Creating documents**: `forma` for templates, `frontis` for schemas
- **Validating work**: `aegis` for gate criteria and aspects
- **Agent communication**: `hermes` for handoff formats
- **Understanding roles**: `lexis` for constitutions, `polis` for agent info

## Template Usage Guidelines

| Action | Command | Context Impact |
|--------|---------|----------------|
| Create file from template | `forma copy` | **None** (recommended) |
| View template structure | `forma show` | ~500 tokens |
| Validate FrontMatter | `frontis schema` | Necessary |

**IMPORTANT**: Use `forma copy` to create files. Avoid `forma show` unless you need to understand template structure without creating a file.

## Project Usage Guidelines

### Before `blueprint project init`

Use **AskUserQuestion** tool to ask the user:
1. **Project alias** - Suggest current directory name as default
2. **Notes** (optional) - Brief description for identification

### Workflows

**New Project:**
1. Ask user for alias and notes via AskUserQuestion
2. Execute in Bash: `~/.claude/skills/blueprint/blueprint.sh project init <alias> --notes "<notes>"`

**Existing Project on New Machine:**
1. Check if project exists: `~/.claude/skills/blueprint/blueprint.sh project list`
2. If project exists, link current path: `~/.claude/skills/blueprint/blueprint.sh project link <alias>`
3. If not, create new project: `~/.claude/skills/blueprint/blueprint.sh project init <alias>`

### Data Locations

| Data | Path | Access |
|------|------|--------|
| Registry | `~/.claude/blueprint/projects/.projects` | Use `project` submodule |
| Project data | `~/.claude/blueprint/projects/<alias>/` | Use `project` submodule |
| Plans | `~/.claude/blueprint/projects/<alias>/plans/` | Use `plan` submodule |

**NOTE**: For **querying** (status checks, listing), use submodule commands.
Direct file access is permitted when following skill instructions (e.g., `/bplan`, `/save`, `/load`).

### Session Guidelines

**path-based Project Notifications:**
- **Once per session per project**: Only mention rename suggestion once
- **Track mentioned projects**: Don't repeat for the same project in same session
- **Be concise**: Brief suggestion, not a lecture

Example (first mention):
```
Project 'Users-duyo-Desktop-test' uses path-based identification.
Consider: `blueprint project rename <alias>`
```

**Using `blueprint project manage`:**
1. Run `blueprint project manage` to scan
2. Use **AskUserQuestion** to gather alias preferences
3. Execute appropriate commands (`rename`, `init`, or cleanup)

**Before `blueprint project remove`:**
Use **AskUserQuestion** to confirm with user:
1. Confirm removal of the project
2. Ask whether to also delete data directory

Then execute with appropriate flags in Bash:
- Registry only: `~/.claude/skills/blueprint/blueprint.sh project remove <alias> --registry`
- Registry + data: `~/.claude/skills/blueprint/blueprint.sh project remove <alias> --registry --data-dir`
