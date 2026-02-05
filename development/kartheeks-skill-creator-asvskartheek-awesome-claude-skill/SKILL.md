---
name: kartheeks-skill-creator
description: Creates Claude skills with proper structure and best practices. Use when the user asks to create a new skill, generate a skill, or build a custom Claude capability.
---

# Kartheek's Skill Creator

Creates well-structured Claude skills following official guidelines and best practices.

## When to Use

Use this skill when the user requests:
- "Create a skill for..."
- "Generate a skill that..."
- "Build a skill to help with..."
- "Make a new Claude skill for..."

## Creation Workflow

Follow these steps in order:

### Step 1: Gather Requirements

Ask the user:
1. **Skill purpose**: What should this skill do?
2. **When to use it**: What keywords or scenarios should trigger it?
3. **Tools needed**: Which Claude tools should it use? (Read, Write, Edit, Bash, Grep, Glob, WebFetch, etc.)
4. **Location**: Personal (`~/.claude/skills/`) or project-specific (`.claude/skills/`)? Default to personal unless specified.

### Step 2: Design the Skill

Create a skill name following these rules:
- Use gerund form (verb + -ing): `processing-pdfs`, `analyzing-data`, `generating-reports`
- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Descriptive and specific

Write a description (max 1024 characters) that includes:
- **What it does**: Clear explanation of functionality
- **When to use it**: Specific trigger terms and scenarios
- Be specific, not vague

**Good description example:**
```
Analyzes Python code for performance issues, identifies bottlenecks, and suggests optimizations. Use when analyzing Python performance, profiling code, or when the user mentions slow Python code, performance optimization, or bottlenecks.
```

**Bad description example:**
```
Helps with code analysis
```

### Step 3: Structure the Content

Keep SKILL.md concise (under 500 lines). Structure content as:

```markdown
# [Skill Name]

## Quick Start
[Most common use case with example]

## Workflows
[Step-by-step processes for complex tasks]

## Examples
[Concrete input/output examples]

## Advanced
[Link to separate reference files if needed]
```

### Step 4: Apply Best Practices

**Conciseness:**
- Assume Claude is already smart
- Only add context Claude doesn't already have
- Remove obvious explanations
- Keep instructions focused

**Progressive Disclosure:**
- Put core instructions in SKILL.md
- Move detailed references to separate .md files
- Link to reference files from SKILL.md
- Keep references one level deep (no nested references)

**Workflows:**
- Break complex tasks into clear sequential steps
- Include validation/feedback loops
- Provide checklists for multi-step processes

**Templates:**
- Provide templates for consistent output
- Use strict templates for API/data formats
- Use flexible templates for creative tasks

**Examples:**
- Show input/output pairs for clarity
- Include edge cases
- Demonstrate desired style and detail level

### Step 5: Create the Skill

1. Create directory: `mkdir -p [location]/[skill-name]`
2. Create SKILL.md with proper frontmatter
3. Add any supporting files (reference.md, scripts/, etc.)
4. Test the skill with representative queries

## SKILL.md Template

```yaml
---
name: skill-name-here
description: What it does and when to use it with specific trigger terms
allowed-tools: Read, Write, Bash  # Optional: restrict tool access
---

# Skill Name

## Quick Start

[Most common use case with minimal example]

## Instructions

[Clear step-by-step guidance]

## Examples

**Example 1:**
Input: [scenario]
Output: [expected result]

**Example 2:**
Input: [scenario]
Output: [expected result]

## Advanced Features

[Link to separate files if needed]
See [reference.md](reference.md) for detailed API documentation.
```

## Common Patterns

### Script Automation Pattern
Bundle Python/Bash scripts in `scripts/` directory:

```markdown
## Utility Scripts

**analyze.py**: Analyzes input data
```bash
python scripts/analyze.py input.json
```

**validate.py**: Validates output
```bash
python scripts/validate.py output.json
```
```

### Read-Process-Write Pattern
```markdown
## Workflow

1. Read input files
2. Process data according to rules
3. Write output in specified format
4. Validate output
```

### Conditional Workflow Pattern
```markdown
## Decision Workflow

1. Determine task type:
   - **Creating new?** → Follow creation workflow
   - **Editing existing?** → Follow editing workflow

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

### Feedback Loop Pattern
```markdown
## Quality Assurance

1. Complete the task
2. Validate output against requirements
3. If validation fails:
   - Note specific issues
   - Fix problems
   - Validate again
4. Only proceed when validation passes
```

## Anti-Patterns to Avoid

- **Too verbose**: Don't explain what Claude already knows
- **Too many options**: Provide a default with escape hatch
- **Time-sensitive info**: Use "old patterns" sections instead
- **Inconsistent terminology**: Pick one term and stick with it
- **Vague descriptions**: Always include specific trigger terms
- **Windows paths**: Always use forward slashes (even on Windows)
- **Deep nesting**: Keep references one level from SKILL.md
- **Missing TOC**: Add table of contents to long reference files

## Quality Checklist

Before finalizing a skill, verify:

**Core Quality:**
- [ ] Name follows naming conventions (gerund form, lowercase, hyphens)
- [ ] Description is specific with trigger terms
- [ ] Description includes both what and when
- [ ] SKILL.md body is under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete
- [ ] File references are one level deep
- [ ] Workflows have clear steps

**Structure:**
- [ ] Proper YAML frontmatter
- [ ] Clear section organization
- [ ] Progressive disclosure used appropriately
- [ ] Supporting files in logical directories

**Testing:**
- [ ] Tested with example queries
- [ ] Skill activates on expected triggers
- [ ] Instructions are clear and complete

## Supporting Files Organization

```
skill-name/
├── SKILL.md              # Core instructions
├── reference/            # Detailed documentation
│   ├── api.md
│   └── examples.md
├── scripts/              # Utility scripts
│   ├── helper.py
│   └── validate.py
└── templates/            # Templates and assets
    └── template.txt
```

## Creation Example

**User Request:** "Create a skill for analyzing CSV files"

**Questions to Ask:**
- What type of analysis? (statistics, validation, transformation?)
- What triggers should activate it? (CSV files, data analysis, spreadsheets?)
- Need visualization? (charts, graphs?)
- Output format? (report, summary, processed CSV?)

**Resulting Skill Structure:**
```
~/.claude/skills/analyzing-csv-data/
├── SKILL.md
├── reference/
│   └── statistics.md
└── scripts/
    ├── analyze.py
    └── validate.py
```

## Final Steps

After creating the skill:

1. **Inform the user** of the location
2. **Provide test queries** to activate it
3. **Suggest improvements** based on their use case
4. **Remind about iteration**: Skills improve with real usage

## Remember

- Keep it concise - Claude is already smart
- Make descriptions specific with trigger terms
- Use progressive disclosure for complex skills
- Test with real queries
- Iterate based on actual usage
