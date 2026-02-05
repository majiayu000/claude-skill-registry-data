---
name: agent-creator
description: |
  Authoritative templates and scaffolding for creating agent system prompts (primary agents and subagents).
  This skill should be used when creating new agents, reviewing existing agent prompts for template
  compliance, verifying agent structure, or extracting knowledge into agent prompts. Contains YAML
  templates with section-by-section instructions and scaffolding scripts for generating skeleton files.
---

# Agent Creator

This skill provides authoritative templates and tools for creating agent system prompts.

## When to Use This Skill

- **Creating** new primary agents or subagents
- **Reviewing** existing agent prompts for template compliance
- **Verifying** agent structure against templates
- **Extracting** knowledge into agent prompts (need to know valid section names)
- **Understanding** what sections an agent should have

## Agent Types

### Primary Agents

Full-featured agents that may orchestrate subagents. They have:
- Complete identity (Role Definition, Who You Are/NOT, Philosophy)
- Cognitive approach (When to Think Deeply, Analysis Mindset)
- Orchestration patterns (if they spawn subagents)
- Knowledge Base with domain expertise
- Multi-phase Workflow
- Learned Constraints

**Template**: `references/primary-agent.yaml`

### Subagents

Focused specialists spawned by primary agents via Task tool. They have:
- Narrow identity (Opening Statement)
- Core Responsibilities (3-4 focused tasks)
- Domain Strategy
- Structured Output Format
- Execution Boundaries

**Template**: `references/subagent.yaml`

## Scripts

Execute scaffolding via justfile or directly with uv:

### Via Justfile (Recommended)

```bash
just -f {base_dir}/justfile <recipe> [args...]
```

| Recipe | Arguments | Description |
|--------|-----------|-------------|
| `scaffold-primary` | `name path` | Create primary agent skeleton |
| `scaffold-subagent` | `name path` | Create subagent skeleton |

### Direct Execution

```bash
uv run {base_dir}/scripts/scaffold_agent.py <type> <name> --path <path>
```

| Argument | Description |
|----------|-------------|
| `type` | `primary` or `subagent` |
| `name` | Agent name (kebab-case) |
| `--path` | Directory to create agent file |

### Examples

```bash
# Create a primary agent
just -f {base_dir}/justfile scaffold-primary my-agent .opencode/agent

# Create a subagent
just -f {base_dir}/justfile scaffold-subagent code-analyzer .opencode/agent

# Direct execution
uv run {base_dir}/scripts/scaffold_agent.py primary my-agent --path .opencode/agent
```

## Template Reference

The YAML templates in `references/` are the authoritative source for agent structure.

Each template contains:
- **frontmatter**: Required and optional metadata fields
- **sections**: Ordered list of sections with:
  - `id`: Unique section identifier
  - `title`: Section heading
  - `type`: Content type (text, bullet-list, structured, etc.)
  - `instruction`: Detailed guidance on what to write
  - `template`: Example format/structure
  - `optional`: Whether section can be omitted

### Reading Templates

To understand what an agent section should contain:
1. Read the appropriate template from `references/`
2. Find the section by `id` or `title`
3. Follow the `instruction` field for guidance
4. Use the `template` field as a structural example

## Domain Patterns

### Variable Notation Standard

Apply consistent variable notation across all prompts:

**Assignment formats**:
- Static: `VARIABLE_NAME: "fixed-value"`
- Dynamic: `VARIABLE_NAME: $ARGUMENTS`
- Parsing: `VARIABLE_NAME: [description-of-what-to-extract]`

**Usage in instructions**:
- Always: `{{VARIABLE_NAME}}` (double curly braces)
- Never: `$VARIABLE_NAME`, `[[VARIABLE_NAME]]`, or bare `VARIABLE_NAME`

**Rationale**: `{{}}` notation matches LLM training on template systems (Jinja2, Handlebars, Mustache). It's unambiguous and visually clear.

## Workflow Integration

When Prompter creates an agent:

1. **Analyze plan** - Identify requirements
2. **Determine type** - Primary (orchestrator) or Subagent (specialist)
3. **Scaffold** - Run scaffolding script to create skeleton
4. **Reference template** - Read YAML for section instructions
5. **Fill sections** - Work through todo list, section by section
6. **Consider skills** - Does this agent need domain expertise externalized?

The scaffolding creates the structure; the templates guide the content.
