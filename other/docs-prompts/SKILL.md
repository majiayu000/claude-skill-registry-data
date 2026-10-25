---
name: get-chapter-prompts
description: >
  This skill covers the generation of chapter prompts for documentation.
  Trigger: When integrating shared system prompts in documentation workflows.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 250
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# get-chapter-prompts

This skill covers the generation of chapter prompts for documentation.

**Trigger**: When integrating shared system prompts in documentation workflows.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task                     | Pattern                     |
|--------------------------|-----------------------------|
| Generate index prompt    | `index_prompt`              |
| Generate overview prompt  | `overview_prompt`           |

## Critical Patterns (Summary)
- **Generate index prompt**: Use `index_prompt` to create an index for documentation.
- **Generate overview prompt**: Use `overview_prompt` to provide an overview of the documentation.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Generate index prompt

Use `index_prompt` to create an index for documentation, ensuring all chapters are listed.

```python
from repoforge.docs_prompts import index_prompt

index = index_prompt()
```

### Generate overview prompt

Use `overview_prompt` to provide an overview of the documentation, summarizing key points.

```python
from repoforge.docs_prompts import overview_prompt

overview = overview_prompt()
```

## When to Use

- When creating structured documentation for a project.
- When needing to summarize key sections of documentation for quick reference.

## Commands

```bash
python repoforge/cli.py generate-docs
```

## Anti-Patterns

### Don't: Hardcode prompts

Hardcoding prompts reduces flexibility and maintainability of documentation.

```python
# BAD
index = "1. Introduction\n2. Overview\n3. Conclusion"
```
<!-- L3:END -->