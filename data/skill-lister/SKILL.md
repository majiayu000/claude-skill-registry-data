---
name: skill-lister
description: Use this skill to discover all available SynthesisFlow skills and their capabilities. Provides a bootstrap context for AI agents by listing all skills, their descriptions, and script paths from the .claude/skills/ directory.
---

# Skill Lister

## Purpose

Provide a comprehensive overview of all available SynthesisFlow skills in the project. The skill-lister scans the `.claude/skills/` directory, extracts skill metadata from SKILL.md files, and returns a formatted list of all discovered skills with their descriptions and script paths. This enables AI agents to quickly understand what capabilities are available without manually exploring the directory structure.

## When to Use

Use this skill in the following situations:

- At the beginning of any work session to understand available SynthesisFlow capabilities
- When onboarding to a new project using SynthesisFlow
- Before deciding which skill to use for a particular task
- When documenting or auditing the project's SynthesisFlow setup
- To verify that all expected skills are installed and accessible

## Prerequisites

- The project must have a `.claude/skills/` directory
- Skills should follow the convention of including SKILL.md files with YAML frontmatter
- No additional tools required (pure bash implementation)

## Workflow

### Step 1: Run the Skill Lister

Execute the helper script to scan all skills in the .claude/skills/ directory:

```bash
bash .claude/skills/skill-lister/scripts/list-skills.sh
```

This will output a human-readable summary showing each skill's metadata including:
- Skill name
- Description
- Available scripts

For machine-readable JSON output (useful for programmatic processing):

```bash
bash .claude/skills/skill-lister/scripts/list-skills.sh -j
```

### Step 2: Review the Skills List

The scanner returns information about all skills found in `.claude/skills/`, including:

- **Skill name**: The identifier for the skill (from YAML frontmatter)
- **Description**: What the skill does and when to use it
- **Script paths**: All executable scripts available for the skill
- **Directory**: Location of the skill in the filesystem

### Step 3: Choose the Appropriate Skill

Based on the output, select the skill that best matches your current task:

- Need to understand documentation? → Use `doc-indexer`
- Starting work on an issue? → Use `issue-executor`
- Proposing a change? → Use `spec-authoring`
- Planning a sprint? → Use `sprint-planner`
- Setting up a new project? → Use `project-init`

## Error Handling

### No Skills Directory Found

**Symptom**: Script reports that `.claude/skills/` directory doesn't exist

**Solution**:
- Verify you're in the project root directory
- Run `project-init` skill to set up SynthesisFlow
- Check if skills are installed in a different location

### Missing SKILL.md Files

**Symptom**: Script lists skills but shows no metadata

**Solution**:
- Verify that each skill directory contains a SKILL.md file
- Check that SKILL.md files have proper YAML frontmatter with `name` and `description` fields
- Run validation script if available: `bash scripts/validate-skills.sh`

### No Scripts Found

**Symptom**: Skill is listed but shows no scripts

**Solution**:
- Verify that the skill's `scripts/` directory exists and contains executable files
- Check file permissions: `chmod +x .claude/skills/*/scripts/*`
- Some skills may not have scripts (documentation-only skills)

### Permission Denied

**Symptom**: Cannot read skill directories or files

**Solution**:
- Check directory permissions: `ls -la .claude/skills/`
- Ensure you have read access to the skills directory
- Verify the script itself is executable: `chmod +x .claude/skills/skill-lister/scripts/list-skills.sh`

## Notes

- **Bootstrap context**: Designed to be run by agent-integrator to provide AI agents with skill discovery capability
- **Lightweight**: Minimal dependencies, works with standard bash tools
- **Extensible**: Automatically discovers new skills as they're added
- **JSON support**: Can output structured data for integration with other tools
- **Convention-based**: Relies on standard SynthesisFlow skill structure (SKILL.md + scripts/)
- **Safe to run**: Read-only operation with no side effects
- **Discovery pattern**: Similar to doc-indexer but for skills instead of documentation
