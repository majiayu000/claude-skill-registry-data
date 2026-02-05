---
name: template-engineering
description: Guide creation of meta-prompt templates that encode engineering workflows into reusable, scalable units. Use when creating slash commands that generate plans, designing workflow templates, or encoding team best practices into agentic prompts.
allowed-tools: Read, Grep, Glob
---

# Template Engineering

Guide for creating meta-prompt templates - prompts that build prompts.

## When to Use

- Creating new slash commands that generate plans
- Encoding team workflows into reusable templates
- Designing meta-prompts for chores, bugs, features
- Analyzing existing templates for improvement

## Template Anatomy

Every effective template has five sections:

### 1. Purpose Section

Clear description at the top:

```markdown
# [Work Type] Planning

Create a new plan in specs/*.md to resolve the [Work Type] using
the exact specified markdown Plan Format.
```

### 2. Instructions Section

Guidance for the agent:

```markdown
## Instructions

- You are writing a plan, not implementing
- Use your reasoning model: THINK HARD about the plan
- Focus on files in the Relevant Files section
- Include validation commands that verify completion
- Fill in every section of the Plan Format
```

### 3. Relevant Files Section

Guide context loading:

```markdown
## Relevant Files

Focus on the following files:
- README.md (project context)
- src/** (source code)
- tests/** (test patterns)
- docs/** (documentation)
```

### 4. Plan Format Section

Template with placeholders:

```markdown
## Plan Format

# [WorkType]: <name>

## Description
<what needs to be done>

## Relevant Files
<files to modify>

## Step by Step Tasks
<numbered actionable tasks>

## Validation Commands
<commands proving completion>

## Notes
<edge cases and considerations>
```

### 5. Parameter Section

Accept user input:

```markdown
## [WorkType]
$ARGUMENTS
```

## Design Workflow

### Step 1: Identify the Work Type

What class of problems does this template solve?

- Chores: Maintenance, updates, cleanup
- Bugs: Investigation and fixes
- Features: New functionality
- Refactors: Code improvement

### Step 2: Define the Plan Structure

What sections does this work type need?

| Work Type | Essential Sections |
| --- | --- |
| Chore | Description, Files, Tasks, Validation |
| Bug | Problem, Solution, Reproduce, Root Cause, Tasks, Validation |
| Feature | User Story, Implementation Plan, Testing, Acceptance |
| Refactor | Before/After, Migration, Rollback |

### Step 3: Write Instructions

Guide the agent's reasoning:

- What should they focus on?
- What reasoning depth is needed? ("think hard")
- What common mistakes should they avoid?
- What format requirements are strict?

### Step 4: Specify Relevant Files

Limit scope to improve quality:

- Core files for this work type
- Test files to understand patterns
- Config files if relevant
- Avoid overly broad patterns

### Step 5: Test with Examples

Validate your template:

1. Run with simple input
2. Check generated plan completeness
3. Try edge cases
4. Refine based on results

## Quality Checklist

Before deploying a template:

- [ ] Purpose clearly states what template does
- [ ] Instructions include "THINK HARD" for reasoning
- [ ] Relevant Files are specific, not too broad
- [ ] Plan Format has all necessary sections
- [ ] Validation Commands section is mandatory
- [ ] Parameter uses `$ARGUMENTS` correctly
- [ ] Output location specified (specs/*.md)

## Common Patterns

### Reasoning Activation

```markdown
Use your reasoning model: THINK HARD about the plan
and the steps to accomplish this work.
```

### File Output Pattern

```markdown
Create a new plan in specs/*.md using the following naming:
specs/[worktype]-[descriptive-name].md
```

### Validation Mandate

```markdown
The Validation Commands section is REQUIRED. Every plan must
include commands that prove the work is complete.
```

## Anti-Patterns to Avoid

### Too Broad Relevant Files

**Bad**: `**/*` (everything)
**Good**: `src/auth/**, tests/auth/**` (focused)

### Missing Validation Section

**Bad**: No way to verify completion
**Good**: Specific test and lint commands

### Vague Instructions

**Bad**: "Make a good plan"
**Good**: "Focus on error handling edge cases, include rollback steps"

### No Output Location

**Bad**: Plan written somewhere undefined
**Good**: `specs/[worktype]-[name].md` pattern

## Related Memory Files

- @template-engineering.md - Core concepts and examples
- @meta-prompt-patterns.md - Prompt hierarchy
- @plan-format-guide.md - Standard plan structures

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
