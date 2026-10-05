---
name: okr
description: "Generate OKR cascades from company strategy to team objectives. Usage: /okr generate <strategy>"
version: 1.0.0
author:
  name: "Alireza Rezvani"
  github: alirezarezvani
tags: [okr]
category: product
platforms: [macos, linux, windows]
license: MIT
metadata:
  hermes:
    related_skills: []
    source: "claude-skills"
    original_author: "Alireza Rezvani"
---

# /okr

Generate cascaded OKR frameworks from company-level strategy down to team-level key results.

## Usage

```
/okr generate <strategy>                                     Generate OKR cascade
```

Supported strategies: `growth`, `retention`, `revenue`, `innovation`, `operational`

## Input Format

Pass a strategy keyword directly. The generator produces company, department, and team-level OKRs aligned to the chosen strategy.

## Examples

```
/okr generate growth
/okr generate retention
/okr generate revenue
/okr generate innovation
/okr generate operational
/okr generate growth --json
```

## Scripts
- `product-team/skills/product-strategist/scripts/okr_cascade_generator.py` — OKR cascade generator (`<strategy> [--teams "A,B,C"] [--contribution 0.3] [--json]`)

## Skill Reference
> `product-team/skills/product-strategist/SKILL.md`