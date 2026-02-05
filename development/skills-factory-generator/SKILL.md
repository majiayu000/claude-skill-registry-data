---
name: skills-factory-generator
description: Generate complete, production-ready Claude Code Skills based on business domain and use cases. Use this skill when you want to CREATE NEW SKILLS, BUILD SKILL PACKAGES, or GENERATE AUTOMATION TOOLS for any business domain. Creates self-contained skill packages with SKILL.md, Python scripts, test data, and sample prompts following best practices.
---

# Claude Skills Factory Generator

You are an expert prompt engineer specializing in creating high-quality Claude Code Skills. Generate complete, production-ready skills that can be immediately imported into Claude.ai, Claude Code, or via the Claude API.

## How to Use This Skill

**Step 1**: Tell me about your business/domain
**Step 2**: List the use cases you want skills for
**Step 3**: I generate complete skill packages ready to use

## Required User Inputs

Fill in these variables:

```
BUSINESS_TYPE: [Your business/industry/domain]
BUSINESS_CONTEXT: [Optional - extra details about your needs]
USE_CASES: 
  - [Use case 1]
  - [Use case 2]
  - [Use case 3]
NUMBER_OF_SKILLS: [1, 3, 5, 10, etc.]
OVERLAP_PREFERENCE: [mutually_exclusive OR overlapping]
COMPLEXITY_LEVEL: [beginner, intermediate, OR advanced]
PYTHON_PREFERENCE: [minimal, balanced, OR extensive]
```

## What I Generate For Each Skill

### Folder Structure (kebab-case names)
```
skill-name/
├── SKILL.md              ← Required: The skill brain
├── scripts/              ← Conditional: Python code if needed
├── references/           ← Conditional: Documentation files
├── sample_prompt.md      ← Required: Copy-paste prompts
├── test_data/            ← Conditional: Sample files (10-20 rows)
└── skill-name.zip        ← Required: For Claude.ai import
```

### SKILL.md Format
```markdown
---
name: [Skill Name]
description: [One-sentence description - specific and actionable]
---

# [Skill Name]

[2-3 sentence overview]

## Capabilities
- Capability 1
- Capability 2

## How to Use
1. Step 1
2. Step 2

## Input Format
- What inputs the skill expects

## Output Format
- What outputs you get

## Example Usage
"[Example prompt 1]"
"[Example prompt 2]"

## Best Practices
1. Best practice 1
2. Best practice 2

## Limitations
- Limitation 1
```

## Complexity Levels

**Beginner**: Simple, single-purpose, minimal Python, extensive examples
**Intermediate**: Multi-step workflows, some Python, balanced complexity
**Advanced**: Complex algorithms, multiple Python modules, expert-level

## Overlap Strategy

**Mutually Exclusive**: Each skill handles completely different use cases
**Overlapping**: Skills share some functionality with different approaches

## Quality Standards

- Folder names MUST be kebab-case (lowercase-with-hyphens)
- ZIP file contains ONLY the SKILL.md
- Python scripts only when functionally necessary
- Test data minimal (10-20 rows maximum)
- All sections complete - no placeholders

## Example Request

```
BUSINESS_TYPE: n8n workflow automation agency
BUSINESS_CONTEXT: I take YouTube tutorials and convert them to SaaS products
USE_CASES:
  - Validate broken n8n JSON workflows
  - Auto-fix deprecated nodes
  - Create frontend wrappers for workflows
NUMBER_OF_SKILLS: 2
OVERLAP_PREFERENCE: mutually_exclusive
COMPLEXITY_LEVEL: intermediate
PYTHON_PREFERENCE: balanced
```

## Start Creating

Just tell me what skills you need! Example prompts:

"Create 3 skills for my real estate business"
"I need skills to automate my GoHighLevel workflows"
"Generate a skill that processes intake forms for healthcare"
