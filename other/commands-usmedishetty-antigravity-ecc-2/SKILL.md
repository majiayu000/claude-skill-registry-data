---
command: /skill
agent: orchestrator
skill: progressive-skill-disclosure
tools:
  - view_file
description: Browse and load skills from the modular skill catalog
---

# Command: `/skill`

> **Invokes Agent:** `orchestrator`  
> **Associated Skill:** `progressive-skill-disclosure`  

## Description
Browse and load skills from the modular skill catalog

## Permitted Antigravity Tools
- `view_file`

## Usage
```bash
/skill [options]
```

## Lifecycle Execution
1. Evaluates prerequisites against the 8-stage lifecycle loop.
2. Invokes specialist agent `orchestrator`.
3. Activates modular skill package `progressive-skill-disclosure`.
4. Validates output and records telemetry into persistent memory.
