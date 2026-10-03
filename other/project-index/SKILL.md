---
name: project-index
description: "Analyze codebase structure, generate domain-specific sub-skills (UI, Backend, Database, etc.), and create agent-guidance files to help AI agents navigate and develop consistently within a project. Use when onboarding to a new codebase, creating project documentation, or setting up agent guidance systems."
---

# Project Index

A skill for analyzing existing codebases and creating structured guidance systems for AI agents. Generates domain-specific knowledge and navigation aids without modifying source code locations.

## When to Use

Use this skill when:
- Starting work on an unfamiliar codebase
- Creating agent guidance for team projects
- Setting up structured project documentation
- Analyzing project architecture and patterns
- Creating domain-specific agent knowledge (UI, Backend, Database, etc.)

## Quick Start


1. Scan the codebase structure

 ```bash
python ./skills/project-index/scripts/scan_codebase.py /path/to/project --output codebase_index.json
```
2. Analyze the generated index and identify domains
3. Create sub-skills using skill-writer
4. Generate agent-guidance files


## Instructions

### Step 1: Scan the Codebase

Run the scanning script to generate a complete structural map:

```bash
python ./skills/project-index/scripts/scan_codebase.py <project_path> --output codebase_index.json
```

**Important**: The script provides a structural overview. You MUST also:
- Read key configuration files (package.json, tsconfig.json, etc.)
- Examine existing code patterns and conventions
- Understand the project's architecture and dependencies
- Review README files and existing documentation

**Parameters**:
- `<project_path>`: Absolute path to the project root
- `--output`: Output filename (default: `codebase_index.json`)

**Excluded directories**: `.git`, `node_modules`, `__pycache__`, `dist`, `build`, `.next`, `.expo`

### Step 2: Analyze the Index

Review the generated `codebase_index.json` and:

1. **Identify main domains**: UI, Backend, Database, API, Components, Utils, etc.
2. **Map relationships**: How do domains interact?
3. **Find patterns**: Naming conventions, folder structures, architectural patterns
4. **Locate key files**: Entry points, configuration files, core modules

**CRITICAL**: Do not rely solely on the JSON index. Actually explore the codebase:
- Open and read representative files from each domain
- Understand the tech stack and frameworks used
- Identify coding standards and conventions
- Note any custom patterns or abstractions

### Step 3: Create Sub-Skills

For each identified domain, create a focused sub-skill using **skill-writer**:

```bash
# Load the skill-writer skill first, then:
# Create sub-skills like project-index-ui, project-index-backend, etc.
```

Each sub-skill should:
- Focus on ONE domain only
- Include specific navigation guidance
- Reference relevant agent-guidance files
- Be discoverable with clear triggers

**Use the template**: `./skills/project-index/templates/skill-template.md`

**Naming convention**: `project-index-<domain>` (e.g., `project-index-ui`, `project-index-backend`)

### Step 4: Generate Agent-Guidance Files

Create `agent-<name>.md` files in relevant project directories:

**Use the template**: `./skills/project-index/templates/agent-template.md`

Each file should contain:
- **Purpose**: Clear description of the directory/section
- **Methodology & Patterns**: Design patterns and architectural approaches used
- **Best Practices**: Explicit do's and don'ts
- **Key Components/Files**: Important files in this section
- **Integration**: How to add new elements following existing patterns

## Templates

### Sub-Skill Template

Location: `./skills/project-index/templates/skill-template.md`

```markdown
---
name: project-index-{{domain}}
description: "Domain-specific knowledge for {{domain}} in this project. Use when working on {{path}} or when user mentions {{domain}}-related tasks."
---

# {{Domain}} Domain Guide

## Overview
Context and purpose of the {{domain}} layer located in `{{path}}`.

## Navigation
- **Main Logic**: [Where core logic resides]
- **Data Flow**: [How data moves through this domain]
- **Key Files**: [Important entry points]

## Guidelines
1. [Specific guideline 1]
2. [Specific guideline 2]

## Reference
See `agent-{{domain}}.md` in the directory for implementation details.
```

### Agent-Guidance Template

Location: `./skills/project-index/templates/agent-template.md`

```markdown
# Agent Guide: {{name}}

## Purpose
Guidance for working in `{{path}}` following established patterns and practices.

## Methodology & Patterns
- **Pattern 1**: [Description]
- **Pattern 2**: [Description]

## Best Practices
- **Do**: [Recommended practice]
- **Avoid**: [Practice to avoid]

## Key Files
- [Important file 1]
- [Important file 2]

## Integration
Follow the structure of `{{example_file}}` when adding new elements.
```

## Best Practices

### DO
- **Investigate thoroughly**: Read actual code files, not just the index
- **Be specific**: Provide concrete examples and file paths
- **Keep it focused**: One sub-skill per domain
- **Use skill-writer**: Follow proper skill creation workflow
- **Update incrementally**: Refine guidance as you learn more
- **Test navigation**: Verify agents can find relevant information

### AVOID
- **Relying only on scripts**: The index is a starting point, not the whole picture
- **Creating mega-skills**: Keep each sub-skill focused on one domain
- **Vague descriptions**: Be specific about patterns and conventions
- **Duplicating docs**: Reference existing READMEs rather than copying
- **Hardcoded assumptions**: Note when patterns vary across the codebase

## File Structure

```
.skills/project-index/
├── SKILL.md                    # This file
├── templates/
│   ├── skill-template.md       # Template for sub-skills
│   └── agent-template.md       # Template for agent guides
└── scripts/
    └── scan_codebase.py        # Codebase scanning utility
```

## Advanced Usage

### Progressive Enhancement

Start with basic structure analysis, then iteratively improve:

1. **Phase 1**: Scan and identify main domains
2. **Phase 2**: Create basic sub-skills with navigation
3. **Phase 3**: Add detailed agent-guidance files
4. **Phase 4**: Refine based on actual usage

### Multi-Project Setup

For organizations with multiple projects:
- Create base patterns in a shared skill
- Extend with project-specific sub-skills
- Maintain consistent naming conventions

### Validation Checklist

Before considering the index complete:
- [ ] Scanned codebase with script
- [ ] Manually reviewed key files and directories
- [ ] Identified all major domains
- [ ] Created focused sub-skills using skill-writer
- [ ] Generated agent-guidance files in relevant directories
- [ ] Verified navigation paths are clear
- [ ] Tested with sample queries

## Troubleshooting

### Script fails to run
- Check Python 3 is installed
- Verify the project path is absolute and exists
- Ensure write permissions for output directory

### Sub-skills not activating
- Use skill-writer to validate the skill structure
- Check description includes trigger words
- Verify file location matches skill name

### Guidance feels incomplete
- Remember: The index is a living document
- Add more detail as you work with the codebase
- Update agent-guidance files based on new discoveries

## Credits

Original concept and implementation by b4san.
