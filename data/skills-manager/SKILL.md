---
name: skills-manager
description: "Branch skill for building and improving skills. Use when creating new skills, adapting marketplace skills, validating skill structure, writing progressive disclosure, or improving existing skills. Triggers: 'create skill', 'improve skill', 'validate skill', 'fix skill', 'skill frontmatter', 'progressive disclosure', 'adapt skill', 'SKILL.md', 'skill references'."
---

# Skills Manager - Branch of JARVIS-04

Build and improve skills following the skills-management policy.

## Policy Source

**Primary policy**: JARVIS-04 → `.claude/skills/skills-management/SKILL.md`

This branch **executes** the policy defined by JARVIS-04. Always sync with Primary before major operations.

## Quick Decision Tree

```text
Task Received
    │
    ├── Create new skill? ───────────────> Workflow 1: Build
    │   └── What type?
    │       ├── Primary (JARVIS-XX) ─────> Full policy skill
    │       ├── Branch (plugin-dev) ─────> Execution skill
    │       └── Domain (category) ───────> Domain knowledge skill
    │
    ├── Adapt marketplace skill? ────────> Workflow 3: Adapt
    │
    ├── Fix existing skill? ─────────────> Workflow 2: Improve
    │
    └── Validate skill? ─────────────────> Validation Checklist
```

## Skill Overview

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools.

**What Skills Provide:**
- Specialized workflows - Multi-step procedures for specific domains
- Tool integrations - Instructions for working with specific file formats or APIs
- Domain expertise - Company-specific knowledge, schemas, business logic
- Bundled resources - Scripts, references, and assets for complex tasks

## Skill Structure

```text
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash)
    ├── references/       - Documentation loaded as needed
    ├── examples/         - Working code examples
    └── assets/           - Files used in output (templates, icons)
```

## Progressive Disclosure Principle

Skills use a three-level loading system to manage context efficiently:

| Level | Content | When Loaded | Size Target |
|-------|---------|-------------|-------------|
| 1. Metadata | name + description | Always in context | ~100 words |
| 2. SKILL.md body | Main instructions | When skill triggers | <2000 words |
| 3. Bundled resources | Details, examples, scripts | As needed by Claude | Unlimited |

**What Goes Where:**

| Content Type | Location | Loaded |
|--------------|----------|--------|
| Core concepts, overview | SKILL.md | On trigger |
| Essential procedures | SKILL.md | On trigger |
| Quick reference tables | SKILL.md | On trigger |
| Detailed patterns | references/ | On demand |
| Advanced techniques | references/ | On demand |
| API documentation | references/ | On demand |
| Working code examples | examples/ | On demand |
| Utility scripts | scripts/ | Executed |
| Templates, assets | assets/ | Used in output |

## Skill Types

| Type | Location | Purpose | Content Focus |
|------|----------|---------|---------------|
| Primary | JARVIS-XX/.claude/skills/ | Define policy | What and why |
| Branch | plugin-dev/skills/ | Execute policy | How to do |
| Domain | plugin-category/skills/ | Domain knowledge | Specific guidance |

## Workflow 1: Build New Skill

### Step 1: Understand the Skill Purpose

Answer these questions:

- What functionality should this skill support?
- What triggers should invoke this skill?
- What procedural knowledge does Claude need?
- What scripts, references, or examples would be helpful?

### Step 2: Determine Skill Type

| Question | Answer → Type |
|----------|---------------|
| Defines policy for JARVIS? | Primary skill |
| Executes policy from Primary? | Branch skill |
| Provides domain knowledge? | Domain skill |

### Step 3: Write Frontmatter

```yaml
---
name: skill-name
description: "This skill [does what]. Use when [conditions]. Triggers: '[trigger1]', '[trigger2]', '[trigger3]'."
---
```

**Description Requirements:**

- **Third-person format**: "This skill should be used when..."
- **"Use when" clause**: Specific conditions for triggering
- **"Triggers:" section**: 3+ terms in single quotes
- **Specific phrases**: Exact words users would say

**Good example:**

```yaml
description: "This skill should be used when the user asks to 'create a hook', 'add a PreToolUse hook', 'validate tool use', or mentions hook events (PreToolUse, PostToolUse, Stop)."
```

**Bad examples:**

```yaml
# Wrong: Vague, no triggers
description: "Provides hook guidance."

# Wrong: Not third person
description: "Use this skill when working with hooks."

# Wrong: Missing trigger phrases
description: "Load when user needs hook help."
```

### Step 4: Choose Content Pattern

**Pattern 1: Policy Skill (Primary)**

```markdown
---
name: [domain]-management
description: "This skill defines [domain] policy for JARVIS. Use when [conditions]. Triggers: '[trigger1]', '[trigger2]', '[trigger3]'."
---

# [Domain] Management - JARVIS-XX

[Core concept in 2-3 sentences explaining what this policy covers]

## Core Concept
[What this domain is about, key principles]

## When to Use This Skill
- [Condition 1]
- [Condition 2]
- [Condition 3]

## Key Structures
[Tables, diagrams, templates]

## Workflows
### Workflow 1: [Name]
1. [Step]
2. [Step]

### Workflow 2: [Name]
1. [Step]
2. [Step]

## Validation Checklist
- [ ] [Check 1]
- [ ] [Check 2]

## Reference Files
- [references/detail.md](references/detail.md) - [Description]
```

**Pattern 2: Execution Skill (Branch)**

```markdown
---
name: [domain]-manager
description: "Branch skill for [action]. Use when [conditions]. Triggers: '[trigger1]', '[trigger2]'."
---

# [Domain] Manager - Branch of JARVIS-XX

[What this branch executes]

## Policy Source
**Primary policy**: JARVIS-XX → `.claude/skills/[domain]-management/SKILL.md`

## Quick Decision Tree
[ASCII diagram for routing]

## Workflow 1: [Name]
### Step 1: [Action]
[Details]

### Step 2: [Action]
[Details]

## Validation Checklist
- [ ] [Check 1]
- [ ] [Check 2]

## Common Issues & Fixes
| Issue | Fix |
|-------|-----|
| [Problem] | [Solution] |

## Sync Protocol
[How to sync with Primary]
```

**Pattern 3: Domain Skill**

```markdown
---
name: [domain]
description: "Domain knowledge for [area]. Use when [conditions]. Triggers: '[trigger1]', '[trigger2]'."
---

# [Domain] Knowledge

## Overview
[What this domain covers]

## Key Concepts
### [Concept 1]
[Explanation]

## Common Operations
```bash
[Example command or code]
```

## Best Practices
- [Practice 1]
- [Practice 2]

## Troubleshooting
| Issue | Solution |
|-------|----------|
| [Problem] | [Fix] |
```

### Step 5: Write Main Content

**Word limit**: Under 2000 words

**Writing style**: Imperative form ("Create...", "Validate...", "Check...")

**Required sections:**
1. Title with context (e.g., "- Branch of JARVIS-XX")
2. Core concept or Policy Source
3. When to Use (Primary) or Quick Decision Tree (Branch)
4. Main workflows with numbered steps
5. Validation Checklist
6. Reference Files (if references/ exists)

### Step 6: Create Bundled Resources (if needed)

**scripts/** - Executable utilities:

```bash
# When to include: Same code rewritten repeatedly
# Example: scripts/validate-skill.sh
# Benefits: Token efficient, deterministic
```

**references/** - Detailed documentation:

```markdown
# When to include: Content that would bloat SKILL.md
# Examples: references/patterns.md, references/advanced.md
# Benefits: Loaded only when needed
```

**examples/** - Working code:

```markdown
# When to include: Complete, runnable examples
# Examples: examples/hook-example.sh
# Benefits: Users can copy and adapt
```

**assets/** - Output files:

```markdown
# When to include: Files used in output
# Examples: assets/template.json, assets/logo.png
# Benefits: Used without loading into context
```

### Step 7: Validate

Run full validation checklist.

## Workflow 2: Improve Existing Skill

### Step 1: Analyze Current State

```bash
# Read skill
cat skills/[name]/SKILL.md

# Check word count
wc -w skills/[name]/SKILL.md

# Check references
ls skills/[name]/references/
```

### Step 2: Gap Analysis

| Component | Check | Common Issues |
|-----------|-------|---------------|
| name | lowercase-hyphens? | Spaces, uppercase |
| description | Third person? | "Use this skill when..." |
| description | Has triggers? | Missing "Triggers:" section |
| description | Has "Use when"? | Only describes, no conditions |
| content | Under 2000 words? | Too long, needs references/ |
| content | Imperative style? | "You should...", passive voice |
| references | Exists if needed? | Long content without references/ |

### Step 3: Apply Fixes

**Fixing description format:**

Before (wrong):

```yaml
description: "Use this skill when working with hooks."
```

After (correct):

```yaml
description: "This skill should be used when the user asks to 'create a hook', 'validate hooks', or mentions PreToolUse/PostToolUse events. Triggers: 'create hook', 'hook validation', 'PreToolUse'."
```

**Converting to imperative:**

Before (wrong):

```markdown
You should start by reading the configuration file.
The skill is used to create hooks.
```

After (correct):

```markdown
Start by reading the configuration file.
Create hooks following these steps.
```

**Moving content to references:**

1. Identify sections > 500 words
2. Create references/[section].md
3. Move content
4. Add link: `See [references/section.md](references/section.md)`

**Adding comparison tables:**

```markdown
| Option | Pros | Cons | Use When |
|--------|------|------|----------|
| [A] | [+] | [-] | [Condition] |
| [B] | [+] | [-] | [Condition] |
```

**Adding ASCII diagrams:**

```text
Task Received
    │
    ├── Condition A? ──> Action 1
    │
    └── Condition B? ──> Action 2
```

### Step 4: Validate

Run full validation checklist.

## Workflow 3: Adapt Marketplace Skill

When taking a skill from wshobson-agents, obra-superpowers, or similar:

### Step 1: Read Original Skill

```bash
cat marketplace-plugin/skills/[skill]/SKILL.md
ls marketplace-plugin/skills/[skill]/references/
```

Note:
- Writing patterns used
- Content organization
- Triggers format
- Reference structure

### Step 2: Identify JARVIS Fit

| Original Focus | JARVIS Target |
|----------------|---------------|
| Generic orchestration | plugin-orchestrator skill |
| Self-improvement | plugin-dev branch skill |
| Data/analytics | Plugin-BigQuery skill |
| Domain-specific | Plugin-Category skill |

### Step 3: Adapt Description

**Original (generic):**

```yaml
description: "Build production-ready monitoring..."
```

**Adapted (JARVIS-specific):**

```yaml
description: "This skill should be used when setting up monitoring for JARVIS categories, tracking MCP server metrics, or implementing category alerting. Triggers: 'monitoring', 'observability', 'metrics', 'alerts'."
```

### Step 4: Add JARVIS Context

**For Primary skills:**

```markdown
## When to Use This Skill
- Creating monitoring for new JARVIS category
- Setting up MCP server observability
- Implementing cross-category metrics
- Configuring JARVIS-00 dashboards
```

**For Branch skills:**

```markdown
## Policy Source
**Primary policy**: JARVIS-XX → `.claude/skills/[domain]-management/SKILL.md`
```

### Step 5: Adapt Content

- Replace generic examples with JARVIS examples
- Add references to JARVIS tools (MCP, BigQuery)
- Include category-specific workflows
- Update validation to include JARVIS checks

### Step 6: Validate Adaptation

Run full validation checklist.

## Skill Auto-Discovery

Claude Code automatically discovers skills:

1. Scans `skills/` directory in plugin
2. Finds subdirectories containing `SKILL.md`
3. Loads skill metadata (name + description) always
4. Loads SKILL.md body when skill triggers
5. Loads references/examples as needed

**Skill locations:**

| Location | Scope |
|----------|-------|
| plugin/skills/ | Available when plugin installed |
| .claude/skills/ | Available in project |
| ~/.claude/skills/ | Available in all projects |

## Validation Checklist

### Structure

- [ ] File is `SKILL.md` in skill subdirectory
- [ ] Skill directory follows kebab-case naming
- [ ] Referenced files actually exist

### Frontmatter

- [ ] Valid YAML between `---` markers
- [ ] `name`: lowercase, hyphens, 3-50 characters
- [ ] `description`: uses third person ("This skill should be used when...")
- [ ] `description`: has "Use when" clause with conditions
- [ ] `description`: has "Triggers:" with 3+ specific terms

### Content

- [ ] Title with context (e.g., "- Branch of JARVIS-XX")
- [ ] Core concept or Policy Source section
- [ ] Main content under 2000 words
- [ ] Imperative writing style throughout (not "You should...")
- [ ] Numbered steps for workflows
- [ ] Validation Checklist section
- [ ] References to bundled resources if they exist

### Bundled Resources (if applicable)

- [ ] `references/` exists if content > 1500 words
- [ ] No duplicate content between SKILL.md and references/
- [ ] Links to references work
- [ ] Scripts are executable
- [ ] Examples are complete and runnable

### Integration

- [ ] No conflicts with other skills in same plugin
- [ ] References JARVIS patterns where relevant

## Writing Best Practices

**DO:**

- ✅ Use third person in description ("This skill should be used when...")
- ✅ Include specific trigger phrases ("'create hook'", "'validate'")
- ✅ Use imperative form in body ("Create...", "Validate...", "Check...")
- ✅ Keep SKILL.md under 2000 words
- ✅ Move detailed content to references/
- ✅ Include comparison tables for options
- ✅ Provide ASCII diagrams for complex flows
- ✅ Link to references for detailed content
- ✅ Include "Common Issues & Fixes" table

**DON'T:**

- ❌ Use second person ("You should...", "You can...")
- ❌ Have vague triggers ("Provides guidance")
- ❌ Exceed 2000 words in SKILL.md
- ❌ Duplicate content between files
- ❌ Leave procedures vague ("do the thing")
- ❌ Skip validation checklists
- ❌ Include broken examples

## Common Issues & Fixes

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Skill not triggering | Vague description | Add specific "Triggers:" terms |
| Wrong person | "Use this skill when..." | Use "This skill should be used when..." |
| No triggers | Description lacks "Triggers:" | Add comma-separated trigger terms |
| Too long | SKILL.md > 2000 words | Move details to references/ |
| Passive voice | "is used to", "should be" | Rewrite with imperative verbs |
| Vague steps | "configure the thing" | Add numbered, specific steps |
| Missing checklist | No validation section | Add checkbox list |
| No examples | Procedures without examples | Add code blocks, templates |
| Duplicate content | Same info in SKILL.md and references | Keep in one place only |

## When to Use This Skill

- User asks to create a new skill
- User asks to adapt a marketplace skill
- User asks to validate skill structure
- User asks to improve skill content or description
- User asks about progressive disclosure or references
- DEV-Manager detects skill issues during improvement cycle
- Regular improvement cycle (~6 sessions)

## Sync Protocol

Before executing any workflow:

1. Read JARVIS-04's skills-management SKILL.md
2. Check for policy updates
3. Apply current policy, not cached knowledge
