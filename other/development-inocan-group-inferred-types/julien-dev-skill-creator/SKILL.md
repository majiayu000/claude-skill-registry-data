---
name: julien-dev-skill-creator
description: "Create or update Claude Code skills. Use when: user wants to create a skill, add a new skill, update skill, or mentions SKILL.md. Includes Skill Chaining documentation."
license: Apache-2.0
metadata:
  author: "Julien (based on Anthropic skill-creator)"
  version: "2.0.0"
  category: "development"
triggers:
  - "SKILL.md"
  - "skill.md"
  - "create skill"
  - "new skill"
  - "add skill"
  - "build skill"
  - "skill template"
  - "write skill"
  - "créer skill"
  - "nouvelle skill"
  - "ajouter skill"
  - "construire skill"
  - "écrire skill"
  - "créer une skill"
  - "faire une skill"
  - "développer une skill"
  - "create a new skill"
  - "build custom skill"
  - "skill development"
---

# Skill Creator

Enhanced guidance for creating effective skills with proper structure and documentation.

## Core Principles

### Concise is Key

Context window is shared. Only add what Claude doesn't already know. Challenge each piece: "Does this justify its token cost?"

### Progressive Disclosure (3 Levels)

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (**< 500 lines**)
3. **Bundled resources** - As needed by Claude

### Skill Structure

```
skill-name/
├── SKILL.md (required, < 500 lines)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation loaded on-demand
    └── assets/       - Output resources (templates, images)
```

**Key rules:**
- References must be **one level deep** from SKILL.md
- Files > 100 lines need **table of contents** at top
- Use **forward slashes** only (not Windows backslashes)
- No extraneous files (README.md, CHANGELOG.md, etc.)

### Naming & Description

See [references/naming-conventions.md](references/naming-conventions.md) for full guidelines.

**Quick rules:**
- Name: max 64 chars, lowercase + hyphens, gerund form preferred (`processing-pdfs`)
- Description: max 1024 chars, **third person**, include "what + when to use"

## Skill Creation Process

### Step 1: Understand with Examples

Ask clarifying questions:
- "What functionality should this skill support?"
- "Give examples of how it would be used"
- "What should trigger this skill?"

### Step 2: Plan Reusable Contents

For each example, identify:
- Scripts needed (deterministic/repeated code)
- References needed (schemas, docs, policies)
- Assets needed (templates, images)

### Step 3: Initialize Skill

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Or copy template: `cp -r assets/template-skill/ path/to/new-skill/`

### Step 4: Edit the Skill

#### YAML Frontmatter

```yaml
---
name: skill-name
description: What it does. Use when [specific triggers].
---
```

#### Body Instructions

Write using **imperative form** (verb-first). Reference bundled resources clearly.

#### Document Skill Chaining (Critical)

Add Skill Chaining section at end. See [references/skill-chaining-template.md](references/skill-chaining-template.md) for complete template.

Required subsections:
1. Skills Required Before
2. Input Expected
3. Output Produced
4. Compatible Skills After
5. Called By
6. Tools Used
7. Visual Workflow
8. Usage Example

### Step 5: Package Skill

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Validates then creates `.skill` file.

### Step 6: Add Semantic Routing Triggers

Add triggers to `configs/skill-triggers.json` for automatic skill suggestion:

```json
{
  "name": "your-skill-name",
  "triggers": [
    "keyword1", "keyword2",
    "full phrase that triggers this skill",
    "phrase en français aussi"
  ],
  "description": "Short description | Description courte"
}
```

**Tips:**
- Include both keywords AND full phrases
- Add French and English variants
- Test with `python scripts/benchmark-semantic-router.py`

### Step 7: Iterate with Self-Assessment

**Never fix everything at once.** Each iteration focuses on ONE improvement.

1. Score against quality rubric (see [references/quality-rubric.md](references/quality-rubric.md))
2. Identify top 3-5 gaps
3. Fix ONE dimension per iteration
4. Re-score until average ≥ 3.5/5

## Reference Files

| File | Content |
|------|---------|
| [references/quality-rubric.md](references/quality-rubric.md) | 9-dimension scoring (1-5 scale) |
| [references/skill-chaining-template.md](references/skill-chaining-template.md) | Complete chaining documentation format |
| [references/naming-conventions.md](references/naming-conventions.md) | Official Anthropic naming rules |
| [references/advanced-patterns.md](references/advanced-patterns.md) | Feedback loops, plan-validate-execute, templates |
| [references/final-checklist.md](references/final-checklist.md) | Pre-distribution verification checklist |

## Degrees of Freedom

Match specificity to task fragility:

| Freedom | When to Use | Example |
|---------|-------------|---------|
| **High** | Multiple valid approaches | Code review guidelines |
| **Medium** | Preferred pattern exists | Scripts with parameters |
| **Low** | Fragile/critical operations | Database migrations |

## What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- User-facing documentation
- Setup/testing procedures
- Any auxiliary context about creation process

## Security & Portability

### Security Checklist

- ✓ No hardcoded credentials (passwords, API keys, tokens)
- ✓ Sensitive data in `.env` file
- ✓ `.env` added to `.gitignore`
- ✓ Instructions use environment variables (`$VAR` or `source .env`)

### Portability Checklist

- ✓ Use relative paths (`.env`, `./scripts/`) instead of absolute paths
- ✓ Use `~/.claude/skills/` for user paths, not hardcoded home directories
- ✓ Avoid platform-specific paths (e.g., `C:\Users\...` in examples)
- ✓ Use forward slashes only (not Windows backslashes)

## Anti-Patterns to Avoid

❌ Description >200 chars (breaks progressive disclosure)
❌ Content >300 lines (too much detail)
❌ Duplicates existing docs (should reference instead)
❌ Development notes in content (timestamps, changelog)
❌ Generic/vague description (doesn't explain when to use)
❌ Second-person language ("you should...")
❌ Information in both SKILL.md and references files
❌ Hardcoded credentials (passwords, API keys, database credentials, tokens)
❌ Sensitive data in code examples (use placeholders or `.env` variables)
❌ Absolute paths in examples (`/home/user/...`, `C:\Users\...`)
❌ Platform-specific paths (Windows-only or Unix-only examples)

## Skill Chaining

### Skills Required Before
- None (entry point skill for skill creation)

### Input Expected
- User request to create/improve a skill
- Domain knowledge or examples from user
- Optional: existing skill to improve

### Output Produced
- **Format**: Complete skill directory with SKILL.md + resources
- **Side effects**: Creates files in specified path
- **Duration**: 10-30 minutes depending on complexity

### Compatible Skills After
**Recommandés:**
- **julien-dev-tools-skill-reviewer**: Review and score the created skill

### Called By
- Direct user invocation: "Create a skill for X"
- Skill improvement workflows

### Tools Used
- `Read` (usage: read existing skills, templates)
- `Write` (usage: create SKILL.md, references)
- `Bash` (usage: run init_skill.py, package_skill.py)
- `Edit` (usage: modify existing skills)

### Visual Workflow

```
User: "Create skill for X"
    ↓
[THIS SKILL]
    ├─► Step 1: Gather examples
    ├─► Step 2: Plan resources
    ├─► Step 3: Initialize structure
    ├─► Step 4: Write SKILL.md + refs
    ├─► Step 5: Package
    ├─► Step 6: Add semantic triggers
    └─► Step 7: Iterate
    ↓
skill-name.skill created
    ↓
[Optional] skill-reviewer for quality check
```

### Usage Example

**Scenario**: Create deployment skill for VPS

**Command**: "Create a skill for deploying to my Hostinger VPS"

**Result**:
- `hostinger-deployment/SKILL.md` created
- `hostinger-deployment/references/` with server docs
- `hostinger-deployment/scripts/` with deploy scripts
- Packaged as `hostinger-deployment.skill`
