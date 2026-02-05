---
name: working-with-context
description: Use when analyzing existing projects or codebases - onboard project to store context in Serena MCP, then use context-aware analysis that mentions existing code, modules, and patterns for better recommendations
---

# Working with Context

## Overview

Context management enables project-aware analysis that references existing code structure, tech stack, and patterns.

## Workflow

**1. Onboard project** (one-time):
```bash
shannon onboard /path/to/project --project-id myapp
```

Scans and stores:
- File inventory and structure
- Tech stack detection
- Module identification
- Pattern recognition

**2. Use context in analysis**:
```bash
shannon analyze new_feature.md --project myapp
```

**Difference**:
- Without context: Generic "add authentication" advice
- With context: "Integrate with existing UserModel in models/user.py, use JWT pattern from auth.py"

## Commands

**shannon onboard PATH**:
- Scans codebase
- Stores in ~/.shannon/projects/
- Saves to Serena MCP

**shannon context status**:
- Shows onboarded projects
- Last update time

**shannon context update**:
- Incremental update after code changes
- Faster than full re-onboarding

**shannon context clean**:
- Remove stale entries
- Use --all for all projects

## Storage

Context stored in:
- Local: ~/.shannon/projects/<project-id>/
- Serena MCP: Entities and relations
- Persistent across sessions

## When to Update

Update context after:
- Major code changes (new modules)
- Architecture changes
- Dependency updates
- Tech stack changes

## Performance

- Onboarding: <30s for most projects
- Context loading: <1s (automatic in analyze)
- Update: <10s (incremental)
