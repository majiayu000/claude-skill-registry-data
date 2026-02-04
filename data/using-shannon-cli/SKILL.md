---
name: using-shannon-cli
description: Use when starting work with Shannon CLI or need to understand available commands - introduces shannon analyze, wave, do, exec commands, explains when to use each, guides installation and basic workflows
---

# Using Shannon CLI

## Overview

Shannon CLI provides programmatic access to Shannon Framework with added intelligence (caching, analytics, cost optimization, context awareness).

## Core Commands

**shannon analyze** - Analyze specifications
- When: Have a spec/requirements document
- Output: 8D complexity, domains, phase plan
- Example: `shannon analyze project_spec.md`

**shannon wave** - Multi-agent wave execution
- When: Implementing from analyzed spec
- Uses: Shannon Framework wave-orchestration
- Example: `shannon wave "implement auth system"`

**shannon do** - Execute tasks (V5)
- When: Create files, implement features, fix bugs
- Uses: Shannon Framework exec skill
- Example: `shannon do "create REST API with users"`

**shannon exec** - Autonomous execution (V3.5)
- When: Need validation + git automation
- Uses: CompleteExecutor with 3-tier validation
- Example: `shannon exec "add tests for API"`

## Quick Start

```bash
# Install
pip install shannon-cli

# Analyze a spec
shannon analyze spec.md

# Execute a task
shannon do "create hello.py"

# With real-time dashboard
shannon do "create app" --dashboard
```

## Command Selection

| Need | Use |
|------|-----|
| Analyze requirements | shannon analyze |
| Implement from spec | shannon wave |
| Create files/features | shannon do |
| With validation/git | shannon exec |

## Features

- **Caching**: Automatic (7-30 day TTL)
- **Cost Optimization**: Auto model selection
- **Analytics**: Session tracking in SQLite
- **Context**: Project-aware analysis (after onboarding)
- **Dashboard**: Real-time execution monitoring
