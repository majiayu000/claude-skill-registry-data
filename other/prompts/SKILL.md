---
name: add-prompts-endpoint
description: >
  This skill covers the integration of various prompt types into the system.
  Trigger: When working with prompts in the application.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
---

## Critical Patterns

### Using skill_prompt

Utilize `skill_prompt` to define a new skill prompt for the system.

```python
from repoforge.prompts import skill_prompt

new_skill = skill_prompt("New skill description")
```

### Building skill registry

Leverage `build_skill_registry` to create a registry of all defined skills.

```python
from repoforge.prompts import build_skill_registry

registry = build_skill_registry([new_skill])
```

## When to Use

- When defining new skills for the application using prompts.
- When creating a registry of skills for orchestration.
- To debug prompt-related issues in the skill definitions.

## Commands

```bash
python repoforge/cli.py add-prompts-endpoint
```

## Anti-Patterns

### Don't: Overuse skill_prompt

Overusing `skill_prompt` can lead to a cluttered and unmanageable skill set.

```python
# BAD
from repoforge.prompts import skill_prompt

skill1 = skill_prompt("Skill 1")
skill2 = skill_prompt("Skill 2")
skill3 = skill_prompt("Skill 3")  # Too many skills without organization
```

## Quick Reference

| Task | Pattern |
|------|---------|
| Define a new skill prompt | `skill_prompt("description")` |
| Create a skill registry | `build_skill_registry([skills])` |