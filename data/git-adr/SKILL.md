---
name: git-adr
description: >
  Manage Architecture Decision Records (ADRs) using git-adr, a CLI tool that stores
  ADRs in git notes instead of files. Execute commands (init, new, edit, list, show,
  search, sync, supersede, link, attach, stats, export, import), generate ADR content
  in any format (MADR, Nygard, Y-Statement, Alexandrian, Business Case, Planguage),
  and teach ADR best practices. Use when users ask about: ADRs, architecture decisions,
  decision records, git-adr commands, documenting technical decisions, or need help
  creating/managing ADRs in a git repository.
---

# git-adr Skill

Comprehensive skill for managing Architecture Decision Records using the git-adr CLI tool.

## Auto-Context Loading

**At session start**, if in a git-adr repository, automatically load ADR summary:

```bash
# Silent detection and load
git notes --ref=adr list &>/dev/null && git adr list --format oneline 2>/dev/null
```

This provides awareness of existing decisions without consuming excessive context.
See [workflows/session-start.md](workflows/session-start.md) for full behavior.

## On-Demand Hydration

Use **progressive loading** for token efficiency:

| Trigger | Action |
|---------|--------|
| "Show me ADR {id}" | `git adr show {id}` → full content |
| "What did we decide about X" | `git adr search "X"` → snippets |
| "Record this decision" | Guided creation workflow |

See [workflows/decision-recall.md](workflows/decision-recall.md) for recall patterns.
See [workflows/decision-capture.md](workflows/decision-capture.md) for creation flow.

## CRITICAL RULES

**NEVER modify user configuration without explicit permission.**

- Do NOT run `git-adr config --set` or `git config adr.*` commands unless the user explicitly asks to change config
- Do NOT "check" config by running set commands - use `git config --get` or `git-adr config --get` only
- Before using AI features, READ the existing config with `git config --local --list | grep adr` - do NOT assume or set values
- If AI config is missing, ASK the user what provider/model they want - do NOT set defaults
- The user's config is sacred - treat it as read-only unless explicitly told otherwise

## What is git-adr?

git-adr is a command-line tool that manages ADRs using **git notes** instead of files:
- **Non-intrusive**: ADRs don't clutter the working tree
- **Portable**: Travel with git history
- **Linkable**: Associate decisions with commits
- **Syncable**: Push/pull like regular git content

## Quick Command Reference

| Command | Description |
|---------|-------------|
| `git adr init` | Initialize ADR tracking |
| `git adr new "<title>"` | Create new ADR |
| `git adr list` | List all ADRs |
| `git adr show <id>` | Display an ADR |
| `git adr edit <id>` | Edit an ADR |
| `git adr search "<query>"` | Search ADRs |
| `git adr supersede <old-id> "<title>"` | Supersede a decision |
| `git adr link <id> <commit>` | Link ADR to commit |
| `git adr sync --push` | Push ADRs to remote |
| `git adr sync --pull` | Pull ADRs from remote |
| `git adr stats` | Show statistics |
| `git adr export` | Export to files |
| `git adr config list` | Show configuration |

For full command documentation, see [references/commands.md](references/commands.md).

## Execution Patterns

### Before Executing Commands

Always verify the environment:

```bash
# 1. Check git-adr is installed
git adr --version

# 2. Verify in a git repository
git rev-parse --is-inside-work-tree

# 3. For most commands, check if initialized
git notes --ref=adr list 2>/dev/null || echo "Not initialized"
```

### Error Handling

If git-adr is not installed:
```
git-adr is not installed. Install with:
  cargo install git-adr
  # or
  brew tap zircote/tap && brew install git-adr
```

If not in a git repository:
```
git-adr requires a git repository. Initialize with:
  git init
  git adr init
```

If ADRs not initialized:
```
ADR tracking not initialized. Run:
  git adr init
```

## Format Selection

### Reading Project Configuration

Always check the project's configured template before generating content:

```bash
# Get configured template (defaults to madr if not set)
TEMPLATE=$(git config --get adr.template 2>/dev/null || echo "madr")
echo "Using template: $TEMPLATE"
```

### Available Formats

| Format | Config Value | Best For |
|--------|--------------|----------|
| MADR | `madr` | General purpose, option analysis (default) |
| Nygard | `nygard` | Quick, minimal decisions |
| Y-Statement | `y-statement` | Ultra-concise, single sentence |
| Alexandrian | `alexandrian` | Pattern-based, forces analysis |
| Business Case | `business` | Stakeholder approval, ROI |
| Planguage | `planguage` | Measurable quality requirements |

For format templates, see [references/formats/](references/formats/).

## Creating ADRs

### Workflow

1. **Check format**: Read `adr.template` config
2. **Load template**: Read appropriate format from references/formats/
3. **Generate content**: Fill template with user's context
4. **Execute command**: `git adr new "<title>"` with content

### Example: Creating a MADR

```bash
# Create ADR (opens editor with template)
git adr new "Use PostgreSQL for primary database"

# Or with specific format override
git adr new "Use PostgreSQL" --template nygard
```

When generating content, follow the structure in the appropriate format template.

## Common Workflows

### New Project Setup

```bash
git adr init
git adr new "Record architecture decisions"
git adr sync --push
```

### Team Collaboration

```bash
git adr sync --pull        # Get latest
git adr new "Add caching"  # Create decision
git adr sync --push        # Share with team
```

### Linking to Implementation

```bash
# After implementing a decision
git adr link 20250115-use-postgresql abc1234

# View linked commits
git adr show 20250115-use-postgresql
```

### Superseding Decisions

```bash
# When replacing a decision
git adr supersede 20250101-use-mysql "Migrate to PostgreSQL"
```

For more workflows, see [references/workflows.md](references/workflows.md).

## Configuration

Common configuration options:

```bash
# Set default template
git adr config adr.template madr

# Set editor
git adr config --global adr.editor "code --wait"

# Enable auto-sync
git adr config adr.sync.auto_push true
git adr config adr.sync.auto_pull true
```

For all configuration options, see [references/configuration.md](references/configuration.md).

## ADR Best Practices

### When to Write an ADR

Write an ADR for decisions that are:
- **Significant**: Affects architecture or design
- **Structural**: Changes system organization
- **Hard to reverse**: Would require substantial effort to change

### What Makes a Good ADR

- **Clear context**: Explains the situation and constraints
- **Explicit decision**: States what was decided
- **Documented consequences**: Lists positive, negative, and neutral effects
- **Alternatives considered**: Shows options evaluated

### Common Mistakes

- Too detailed (specification, not decision)
- Too brief (no context or rationale)
- Not updating status when decisions change
- Writing long after the decision was made

For complete guidance, see [references/best-practices.md](references/best-practices.md).

## Progressive Loading Guide

Load reference files based on user intent:

| User Intent | Load File |
|-------------|-----------|
| "Create an ADR" | `references/formats/{template}.md` |
| "What commands are available?" | `references/commands.md` |
| "Configure git-adr" | `references/configuration.md` |
| "What is an ADR?" | `references/best-practices.md` |
| "Set up for my team" | `references/workflows.md` |
| "Find decisions about X" | `references/search-patterns.md` |
| "Record this decision" | `workflows/decision-capture.md` |
| "What did we decide" | `workflows/decision-recall.md` |

## ADR Content Generation

When generating ADR content:

1. **Read the project's configured format**
2. **Load the corresponding template** from references/formats/
3. **Ask clarifying questions** if context is insufficient:
   - What problem are you solving?
   - What alternatives did you consider?
   - What are the constraints?
4. **Fill the template** with the gathered information
5. **Execute the command** to create the ADR

### Content Quality Checklist

Before creating an ADR, ensure:
- [ ] Context explains the situation clearly
- [ ] Decision is explicitly stated
- [ ] Consequences are categorized (positive/negative/neutral)
- [ ] Alternatives were considered (for MADR format)
- [ ] Status is appropriate (proposed/accepted)

## Reference Files

| File | Purpose |
|------|---------|
| `references/commands.md` | Full command documentation |
| `references/configuration.md` | All config options |
| `references/best-practices.md` | ADR writing guidance |
| `references/workflows.md` | Common workflow patterns |
| `references/search-patterns.md` | Natural language → search mapping |
| `references/formats/madr.md` | MADR template |
| `references/formats/nygard.md` | Nygard template |
| `references/formats/y-statement.md` | Y-Statement template |
| `references/formats/alexandrian.md` | Alexandrian template |
| `references/formats/business-case.md` | Business Case template |
| `references/formats/planguage.md` | Planguage template |
| `workflows/session-start.md` | Auto-context loading behavior |
| `workflows/decision-capture.md` | Guided ADR creation workflow |
| `workflows/decision-recall.md` | Find past decisions workflow |
