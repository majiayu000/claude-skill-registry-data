---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
tags: [meta, workflow, documentation]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

## Overview
**Writing skills IS Test-Driven Development applied to process documentation.**

You write test cases (pressure scenarios), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## What is a Skill?
A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future AI instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## When to Create a Skill
**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in project rules instead)
- Mechanical constraints (if it's enforceable with linting, automate it)

## Directory Structure
```
skills/
  <category>/             # flutter, general, go, devops
    skill-name/
      SKILL.md            # Main reference (required)
      supporting-file.*   # Only if needed
```

**Categories in this repo:**
- `general/` — Cross-language workflow and process skills
- `flutter/` — Flutter-specific development skills
- `go/` — Go-specific development skills
- `devops/` — Infrastructure and deployment skills

## SKILL.md Structure
**Frontmatter (YAML):**

```markdown
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
tags: [relevant, tags]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

# Skill Name

## Overview / Context
What is this? Core principle in 1-2 sentences.

## When to Use (if decision is non-obvious)
Bullet list with SYMPTOMS and use cases
When NOT to use

## Instructions / Core Pattern
Step-by-step guidance or before/after code comparison

## Examples
Concrete input → output

## Anti-patterns
What to avoid + why

## Common Mistakes
What goes wrong + fixes
```

## Description Field — Critical for Discovery

**Format:** Start with "Use when..." to focus on triggering conditions

**CRITICAL: Description = When to Use, NOT What the Skill Does**

The description should ONLY describe triggering conditions. Do NOT summarize the skill's process or workflow.

**Why:** When a description summarizes workflow, agents may follow the description instead of reading the full skill content.

```yaml
# ❌ BAD: Summarizes workflow
description: Use for state management — create Cubit, define states with freezed, emit states

# ✅ GOOD: Just triggering conditions
description: Use when adding or modifying state management in Flutter features
```

## Key Principles

### Token Efficiency
- Keep skills concise — agents load them into context
- Move heavy reference to separate files
- Use cross-references instead of repeating content
- One excellent example beats many mediocre ones

### Naming Conventions
**Use active voice, verb-first:**
- ✅ `building-forms` not `form-building`
- ✅ `http-and-json` not `networking`
- ✅ `systematic-debugging` not `debug-techniques`

### Cross-Referencing
Use skill name with explicit requirement markers:
- ✅ Good: `**REQUIRED:** Use the writing-plans skill`
- ❌ Bad: Path references that force-load files

## Skill Creation Checklist

- [ ] Name uses only letters, numbers, hyphens
- [ ] YAML frontmatter with `name`, `description`, `tags`, `applies-to`, `level`
- [ ] Description starts with "Use when..." and includes specific triggers
- [ ] Clear overview with core principle
- [ ] Instructions that an agent can follow step-by-step
- [ ] At least one concrete example
- [ ] Anti-patterns section (what to avoid)
- [ ] Keywords throughout for search (errors, symptoms, tools)
- [ ] Verify the skill is discoverable from `using-skills` registry
- [ ] Update `using-skills/SKILL.md` skill registry table
- [ ] Commit and push

## After Creating a Skill

**Always update** `skills/general/using-skills/SKILL.md`:
1. Add the new skill to the Skill Registry table
2. Add a matching entry to the "Matching Skills to Tasks" lookup table
3. Commit both files together

## The Bottom Line
**Creating skills IS TDD for process documentation.**

Same Iron Law: No skill without understanding the problem first.
Same benefits: Better quality, fewer surprises, bulletproof results.
