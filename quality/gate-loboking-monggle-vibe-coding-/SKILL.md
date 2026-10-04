---
name: monggle-gate
version: 1.0.0
description: |
  PRD gate - Validate PRD completeness and quality before implementation (monggle)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - /gate
  - monggle gate
---

# gate (monggle)

PRD gate - Validate PRD completeness and quality before implementation (monggle)

**Usage:** `/gate [prd_file]`

**Examples:**
```bash
/gate
```
