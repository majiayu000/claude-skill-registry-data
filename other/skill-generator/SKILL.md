---
name: skill-generator
description: "Creates new Antigravity skills with proper SKILL.md format, directory structure, scripts, and resources. Triggers when crystallizing a repeating pattern into a reusable skill, or when the agent or user requests a new skill to be created."
---

# Skill Generator (Meta-Skill)

## Goal

Create properly formatted, high-quality Antigravity skills that follow all conventions and will be reliably triggered by the agent when relevant.

## Instructions

### Step 1: Define the Skill

Before creating any files, define:
- **Name**: lowercase, hyphenated (e.g., `run-tests`, `deploy-staging`)
- **Trigger description**: The description that will go in the YAML frontmatter. This MUST be specific enough for the LLM to match semantically.
  - BAD: "Database tools" (too vague — agent will not know when to use this)
  - GOOD: "Executes the project test suite using pytest and reports results with coverage metrics"
- **What it does**: Plain-English explanation for the orchestrator
- **What files it needs**: Scripts? Resources? Templates?

### Step 2: Create the Directory

Create the skill directory at `.agent/skills/<skill-name>/`:
```
<skill-name>/
├── SKILL.md           # Required: definition and instructions
├── scripts/           # Optional: executable scripts
└── resources/         # Optional: templates, docs, references
```

### Step 3: Write the SKILL.md

Use the template in `resources/skill-template.md`. The file has two sections:

**YAML Frontmatter** (between `---` markers):
```yaml
---
name: <skill-name>
description: "<Specific trigger phrase. Describe WHEN this skill should activate and WHAT user intent it matches.>"
---
```

**Markdown Body**:
```markdown
# <Skill Name>

## Goal
[One sentence: what does this skill accomplish?]

## Instructions
[Step-by-step instructions for the agent to follow when this skill activates]

## Examples
[At least one example of input → output to show the expected behavior]

## Constraints
[What this skill should NOT do. Edge cases. Limitations.]
```

### Step 4: Create Supporting Files

- **Scripts** (`scripts/`): If the skill automates commands, create scripts that the agent can execute. Use Python over Bash for readability (the orchestrator is a non-coder).
- **Resources** (`resources/`): If the skill uses templates, reference docs, or static content, place them here. The SKILL.md should reference them by relative path.

### Step 5: Quality Check

Before finalizing, verify using `resources/skill-checklist.md`:
- Is the description specific enough for semantic matching?
- Are instructions clear and unambiguous?
- Are edge cases covered in constraints?
- Does it follow Antigravity SKILL.md conventions?
- Will the orchestrator understand what this skill does?

### Step 6: Log the Creation

Append an entry to `.agent/knowledge/evolution-log.md`:
```
[DATE] TYPE: skill NAME: <skill-name>
  TRIGGER: [What caused this skill to be created — pattern crystallization, user request, bootstrap]
  DESCRIPTION: [Plain-English description]
  METRIC: [What it improves]
  STATUS: active
```

### Step 7: Inform the Orchestrator

Tell the orchestrator:
- What the new skill does (plain English)
- When it will trigger automatically
- How they can also trigger it manually if needed
- That they can find it at `.agent/skills/<skill-name>/SKILL.md`

## Constraints

- Never create a skill without orchestrator approval
- Never create a skill that duplicates an existing one — check `.agent/skills/` first
- Never create a skill that modifies the core Ground Zero rules (files numbered 00-06)
- Skills must always be explainable in one sentence
