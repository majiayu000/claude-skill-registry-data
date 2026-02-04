---
name: skill-importer
description: Upgrades external Claude Skills to factory spec - analyzes existing skill folders and generates missing files, restructures docs, validates compliance
---

# Skill Importer

Bring externally-built Claude Skills up to factory specification. Point me at a skill folder and I'll analyze what's there, identify gaps, and generate the missing pieces.

## Capabilities

- **Gap Analysis**: Scan skill folder and identify missing factory-required files
- **Structure Upgrade**: Restructure SKILL.md to match factory template
- **File Generation**: Create missing HOW_TO_USE.md, sample_input.json, expected_output.json, README.md
- **Validation**: Check YAML frontmatter, naming conventions, Python code quality
- **Composability Check**: Ensure skill follows factory composability patterns

## Input Requirements

Provide:
- **Path to skill folder**: Absolute or relative path to the skill to upgrade
- **Skill context** (optional): Additional info about what the skill does if not clear from files

## Output

After import/upgrade:
```
skill-name/
├── SKILL.md          (restructured to factory template)
├── HOW_TO_USE.md     (generated if missing)
├── README.md         (generated if missing)
├── sample_input.json (generated if missing)
├── expected_output.json (generated if missing)
└── *.py              (preserved, analyzed for docs)
```

## Workflow

### Step 1: Analyze Existing Skill

Read all files in the skill folder:
- Check SKILL.md for YAML frontmatter (name, description)
- Identify existing Python modules
- List any existing sample/expected files
- Note documentation gaps

### Step 2: Gap Report

Generate a checklist:
```
[ ] SKILL.md - exists but needs restructuring
[x] YAML frontmatter - valid
[ ] HOW_TO_USE.md - missing
[ ] README.md - missing
[ ] sample_input.json - missing
[ ] expected_output.json - missing
[x] Python modules - analyze.py found
```

### Step 3: Upgrade SKILL.md

Restructure to factory template:
```markdown
---
name: skill-name-kebab-case
description: One-line description
---

# Human-Readable Title

Brief introduction.

## Capabilities
- **Feature 1**: Description
- **Feature 2**: Description

## Input Requirements
- What data/info needed
- Required vs optional

## Output Formats
- What gets produced
- File types

## How to Use
Example phrases...

## Scripts (if applicable)
- `script.py`: What it does

## Best Practices
1. Guidelines

## Limitations
- Honest constraints
```

### Step 4: Generate Missing Files

**HOW_TO_USE.md**:
```markdown
# How to Use This Skill

Hey Claude—I just added the "{skill-name}" skill. Can you [primary use case]?

## Example Invocations

**Example 1:**
[Natural language request]

**Example 2:**
[Alternative request]

## What to Provide
- [Input 1]
- [Input 2]

## What You'll Get
- [Output 1]
- [Output 2]
```

**sample_input.json**: Minimal realistic example based on skill purpose

**expected_output.json**: Expected output structure

**README.md**: Installation and overview

### Step 5: Validate

Run final validation:
- YAML frontmatter present and valid
- Name is kebab-case
- Description is concise (10-25 words)
- All required files present
- No backup/cache files
- Python compiles (if present)

## How to Use

**Import a skill:**
"Import the skill at generated-skills/issue-analysis"
"Bring generated-skills/my-custom-skill up to factory spec"

**Analyze only (no changes):**
"Analyze generated-skills/issue-analysis and show me what's missing"

**Upgrade specific files:**
"Generate a HOW_TO_USE.md for generated-skills/issue-analysis"

## Factory Compliance Checklist

| File | Required | Purpose |
|------|----------|---------|
| SKILL.md | Yes | Main definition with YAML frontmatter |
| HOW_TO_USE.md | Yes | Example invocations |
| sample_input.json | Yes | Test input data |
| expected_output.json | Yes | Expected output |
| README.md | Recommended | Installation guide |
| *.py | If needed | Functional code |

## Best Practices

1. Run analysis first before making changes
2. Review generated files - they're templates to customize
3. Test sample_input produces expected_output
4. Ensure skill name is unique in your catalog

## Limitations

- Cannot infer complex business logic from minimal context
- Generated samples may need manual refinement
- Python analysis is structural, not behavioral
- Won't auto-fix broken Python code
