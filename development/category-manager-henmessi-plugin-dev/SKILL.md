---
name: category-manager
description: "Branch skill for building and improving categories. Use when creating new categories, validating category structure, improving existing categories, or migrating categories to new standard. Triggers: 'create category', 'improve category', 'validate category structure', 'fix category', 'category compliance', 'migrate category', 'JARVIS-XX structure', 'CLAUDE.md structure', 'settings.json format', 'self-improvement cycle'."
---

# Category Manager - Branch of JARVIS-01

Build and improve categories following the category-management policy.

## Policy Source

**Primary policy**: JARVIS-01 → `.claude/skills/category-management/SKILL.md`

This branch **executes** the policy defined by JARVIS-01. Always sync with Primary before major operations.

## Quick Decision Tree

```text
Task Received
    │
    ├── Create new category? ────────────> Workflow 1: Build
    │
    ├── Fix existing category? ──────────> Workflow 2: Improve
    │
    ├── Validate category? ──────────────> Validation Checklist
    │
    ├── Migrate to new standard? ────────> Workflow 3: Migrate
    │
    └── Self-improvement cycle? ─────────> Self-Improvement Process
```

## Category Overview

Each JARVIS category maintains effective configuration through:
- `CLAUDE.md` - Main Agent instructions at category root
- `.claude/settings.json` - Tool permissions and MCP configurations
- `.claude/mcp.json` - MCP server definitions (Execution layer)
- `.claude/skills/` - Primary Skill defining category policy
- `plugins/` - 4-Plugin Architecture

## Workflow 1: Build New Category

### Step 1: Determine Layer

| Range | Layer | Purpose | Example |
|-------|-------|---------|---------|
| 00-10 | Management | Build ecosystem infrastructure | JARVIS-07 MCP-Manager |
| 11+ | Execution | Control external system | JARVIS-11 Cloudflare |

**Decision criteria**:
- Does it build tools for OTHER categories? → Management
- Does it control ONE external API/system? → Execution

### Step 2: Assign Number

```bash
# Check existing categories
ls -d JARVIS-* | sort -t'-' -k2 -n
```

- Management: Limited to 00-10, must be approved
- Execution: Start from 11, take next available

### Step 3: Create Full Structure

```bash
# Create all directories at once
mkdir -p JARVIS-XX-Name/{.claude/skills/[name]-management/references,plugins/{orchestrator,dev,bigquery-[name],category-[name]},TASKS}
```

Expected structure:
```
JARVIS-XX-Category-Name/
├── CLAUDE.md                        <- Category identity (REQUIRED)
├── .claude/
│   ├── settings.json                <- Tool permissions
│   ├── mcp.json                     <- MCP config (Execution layer)
│   └── skills/
│       └── [name]-management/       <- Primary Skill
│           ├── SKILL.md             <- REQUIRED
│           └── references/          <- Optional details
├── plugins/                         <- 4 Plugins (REQUIRED)
│   ├── orchestrator/                <- Shared - task routing
│   ├── dev/                         <- Shared - self-improvement
│   ├── bigquery-[name]/             <- Template - data access
│   └── category-[name]/             <- Unique - domain logic
└── TASKS/                           <- Task tracking
    └── TASK-XX-[name]/
        └── README.md
```

### Step 4: Write CLAUDE.md

#### CLAUDE.md Structure

**Minimal Template** (for new categories):

```markdown
# JARVIS-XX-CategoryName

## Role
[One sentence describing primary function]

## Responsibilities
- [Key responsibility 1]
- [Key responsibility 2]
- [Key responsibility 3]

## MCP Servers
| Server | Location | Purpose |
|--------|----------|---------|
| vault | VPS | Secrets management |
| supabase-common | CloudRun | Database access |

## Quick Reference
[Most common commands or patterns]
```

**Full Template** (for mature categories):

```markdown
# JARVIS-XX-CategoryName

## Role
[Category's primary function and domain expertise]

## Responsibilities
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

## MCP Servers
| Server | Location | Purpose |
|--------|----------|---------|
| server1 | VPS/CloudRun/Local | Description |

## Schemas (if database access)
| Schema | Purpose |
|--------|---------|
| schema1 | Description |

## Common Tasks

### Task Type 1
[Step-by-step instructions]

### Task Type 2
[Step-by-step instructions]

## Best Practices
- [Practice 1]
- [Practice 2]

## Integration Points
- **Category XX**: [How they interact]
- **Category YY**: [How they interact]

## Learnings
- [Learning 1 from previous conversations]
- [Learning 2]

## Changelog
- YYYY-MM-DD: [Change description]
```

#### CLAUDE.md Best Practices

- Keep concise (500-2000 words ideal)
- Use tables for structured data
- Include practical examples
- Update changelog on changes
- Focus on actionable instructions

**Management Layer Template**:

```markdown
# JARVIS-XX-CategoryName

## Role
[Category function] for the JARVIS AI Ecosystem.

## Responsibilities
- Define [domain] policy for all categories
- Maintain [domain] standards
- Support categories in [domain] tasks

## Integration
- **Plugin-dev branch**: [branch-name]
- **Primary Skill**: [skill-name]-management

## Quick Reference
[Most common operations for this category]
```

**Execution Layer Template**:

```markdown
# JARVIS-XX-CategoryName

## Role
Control [External System] via MCP with full coverage.

## Responsibilities
- Manage [System] resources
- Automate [System] operations
- Monitor [System] status

## MCP Servers
| Server | Location | Coverage | Purpose |
|--------|----------|----------|---------|
| [name] | CloudRun | 90%+ | [Description] |

## Schemas (BigQuery)
| Schema | Purpose |
|--------|---------|
| jarvis_XX_[name] | [Data stored] |

## Quick Reference
[Most common MCP operations]
```

### Step 5: Configure settings.json

#### Settings.json Location

`.claude/settings.json` in category root

#### Basic Structure

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

#### With MCP Servers

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(git:*)",
      "mcp__vault__*"
    ],
    "deny": [
      "Bash(rm -rf:*)"
    ]
  },
  "mcpServers": {
    "vault": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-vault"],
      "env": {
        "VAULT_ADDR": "${VAULT_ADDR}"
      }
    }
  }
}
```

#### Permission Patterns

| Pattern | Meaning |
|---------|---------|
| `Bash(npm:*)` | Allow npm commands |
| `Bash(git:*)` | Allow git commands |
| `mcp__server__*` | Allow all tools from MCP server |
| `mcp__server__tool` | Allow specific MCP tool |
| `Read(path/**)` | Allow reading from path |
| `Write(path/**)` | Allow writing to path |

#### Settings.json Best Practices

- Follow least privilege principle
- Document why permissions exist
- Test after changes
- Use environment variables for secrets
- Keep MCP configs minimal

### Step 6: Create Primary Skill

Follow skills-manager for full details. Minimum:

```markdown
---
name: [category]-management
description: "This skill [function]. Use when [conditions]. Triggers: '[trigger1]', '[trigger2]'."
---

# [Category] Management - JARVIS-XX

[Core concept in 2-3 sentences]

## When to Use This Skill
- [Condition 1]
- [Condition 2]

## Core Workflows
### Workflow 1: [Name]
1. [Step]
2. [Step]

## Validation Checklist
- [ ] [Check 1]
- [ ] [Check 2]

## Reference Files
- [references/detail.md](references/detail.md) - [Description]
```

### Step 7: Set Up 4 Plugins

| Plugin | Action |
|--------|--------|
| orchestrator | Copy from shared source (identical) |
| dev | Copy from shared source (identical) |
| bigquery-[name] | Create from template, update table list |
| category-[name] | Create custom with domain agents/skills |

Use plugins-manager for detailed plugin creation.

### Step 8: Configure MCP (Execution Layer Only)

Work with JARVIS-07 to:
1. Build or adapt MCP server
2. Document all tools in Primary Skill
3. Configure .claude/mcp.json
4. Test tool coverage

### Step 9: Validate

Run full validation checklist (see below).

## Self-Improvement Cycle

Categories should run self-improvement periodically to maintain effectiveness.

### When to Run

- Every ~6 conversations
- After completing major tasks
- When issues or inefficiencies noticed
- On explicit request

### Self-Improvement Process

```text
1. Analyze Current State
   ├── Read CLAUDE.md
   ├── Read settings.json
   └── Review recent patterns

2. Identify Improvements
   ├── Missing instructions
   ├── Outdated information
   ├── Permission gaps
   └── New learnings

3. Apply Changes
   ├── Update CLAUDE.md
   ├── Update settings.json
   └── Document changes

4. Validate
   ├── Test configurations
   └── Verify no breakage
```

### What to Improve

**CLAUDE.md:**

- Add instructions for recurring tasks
- Remove outdated information
- Improve clarity and organization
- Add learnings from conversations
- Update MCP server documentation

**Settings.json:**

- Add permissions for frequently used tools
- Remove unnecessary permissions
- Update MCP configurations
- Fix broken server configs

### Self-Improvement Best Practices

- Make incremental changes
- Preserve working configurations
- Document all changes
- Test after modifications
- Review periodically

## Workflow 2: Improve Existing Category

### Step 1: Analyze Current State

```bash
# Run category audit
ls -la JARVIS-XX-Name/
cat JARVIS-XX-Name/CLAUDE.md
cat JARVIS-XX-Name/.claude/skills/*/SKILL.md
ls JARVIS-XX-Name/plugins/
```

### Step 2: Gap Analysis

| Component | Check | Common Issues |
|-----------|-------|---------------|
| CLAUDE.md | Exists? Up to date? | Missing MCP docs, outdated responsibilities |
| Primary Skill | Complete? References? | Missing triggers, no validation checklist |
| settings.json | Permissions correct? | Missing MCP tool permissions |
| 4 Plugins | All present? | Missing plugin directories |
| mcp.json | Configured? (Execution) | Wrong server URLs |

### Step 3: Apply Fixes

Priority order:
1. **Critical**: Missing CLAUDE.md or Primary Skill
2. **High**: Missing plugins
3. **Medium**: Outdated content
4. **Low**: Formatting, clarity

### Step 4: Document Changes

Create task record:
```markdown
# TASK-XX-Category-Improvement

## Date: YYYY-MM-DD

## Changes Made
- [ ] Updated CLAUDE.md with [changes]
- [ ] Added missing [component]
- [ ] Fixed [issue]

## Validation
- [ ] All checks pass
- [ ] Tested functionality
```

## Workflow 3: Migrate Category to New Standard

When category structure policy changes:

1. **Backup current state**
2. **Compare with new standard** (read Primary Skill)
3. **Create migration plan**
4. **Apply changes incrementally**
5. **Validate each step**
6. **Document migration**

## Validation Checklist

### Structure Checks
- [ ] Directory named `JARVIS-XX-Name` (XX = 2-digit number)
- [ ] Number matches layer (00-10 Management, 11+ Execution)
- [ ] CLAUDE.md exists at root
- [ ] CLAUDE.md has Role section
- [ ] CLAUDE.md has Responsibilities section

### Configuration Checks
- [ ] `.claude/settings.json` exists and valid JSON
- [ ] `.claude/mcp.json` exists (if Execution layer)
- [ ] MCP servers documented in CLAUDE.md

### Skill Checks
- [ ] Primary Skill at `.claude/skills/[name]-management/SKILL.md`
- [ ] SKILL.md has valid frontmatter (name, description)
- [ ] Description has "Triggers:" section
- [ ] references/ exists if SKILL.md > 1500 words

### Plugin Checks
- [ ] `plugins/orchestrator/` exists
- [ ] `plugins/dev/` exists
- [ ] `plugins/bigquery-[name]/` exists
- [ ] `plugins/category-[name]/` exists
- [ ] Each plugin has `.claude-plugin/plugin.json`

### Integration Checks
- [ ] If Management 01-06: branch exists in plugin-dev
- [ ] If Execution: MCP configured and tested
- [ ] TASKS/ directory exists

## Common Issues & Fixes

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Missing CLAUDE.md | `ls JARVIS-XX/CLAUDE.md` returns nothing | Create from template above |
| Wrong layer number | Category 15 doing management work | Renumber or reassign responsibilities |
| No Primary Skill | `.claude/skills/` empty | Create following skills-manager |
| Missing plugins | `ls plugins/` shows < 4 dirs | Create missing plugin directories |
| Outdated content | CLAUDE.md references old tools | Update with current MCP tools |
| No mcp.json | Execution category without MCP | Work with JARVIS-07 to create |

## BigQuery Integration (Optional)

Categories can track metrics in BigQuery for analytics and improvement:

```text
bigquery.jarvis_analytics.
├── jarvis_XX_conversations    # Conversation logs
├── jarvis_XX_improvements     # Improvement history
└── jarvis_XX_metrics          # Performance metrics
```

### Tracked Metrics

- Conversation count
- Task types and frequency
- Error patterns
- Improvement effectiveness

Use bigquery-[name] plugin for data access.

## When to Use This Skill

- User asks to create a new JARVIS category
- User asks to validate category compliance
- User asks to fix category structure issues
- User asks about CLAUDE.md structure or settings.json format
- User asks about self-improvement cycle
- DEV-Manager detects category problems during improvement cycle
- Migrating categories to updated standard
- Regular improvement cycle (~6 sessions)

## Sync Protocol

Before executing any workflow:
1. Read JARVIS-01's category-management SKILL.md
2. Check for policy updates
3. Apply current policy, not cached knowledge
