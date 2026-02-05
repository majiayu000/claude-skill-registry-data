---
name: executing-tasks-with-shannon-do
description: Use when creating files, implementing features, or executing development tasks - guides shannon do command usage, dashboard integration, caching behavior, when to use vs shannon exec or shannon analyze
---

# Executing Tasks with shannon do

## Overview

shannon do executes development tasks by invoking Shannon Framework exec skill, wrapped with V3 intelligence (cache, analytics, cost optimization).

## When to Use

**Use shannon do for**:
- Creating files: "create hello.py"
- Implementing features: "add authentication to API"
- Fixing bugs: "fix login validation error"
- Multi-file tasks: "create models.py, views.py, tests.py"

**Don't use for**:
- Analyzing specs → shannon analyze
- Autonomous with git automation → shannon exec
- Wave orchestration → shannon wave

## Basic Usage

```bash
# Simple task
shannon do "create calculator.py with add and multiply"

# Complex application
shannon do "create Flask API with user auth, posts CRUD, SQLite database"

# With real-time dashboard
shannon do "create app" --dashboard
```

## Dashboard Mode

Start services once:
```bash
# Terminal 1: WebSocket server
python -m shannon.server.app

# Terminal 2: Dashboard UI
cd dashboard && npm run dev
```

Then use --dashboard:
```bash
shannon do "create authentication system" --dashboard
# Open browser: http://localhost:5173
```

Shows real-time: task progress, files created, validation status, agents.

## vs Other Commands

| Need | Use |
|------|-----|
| Create code | shannon do |
| Analyze spec | shannon analyze |
| With git commits | shannon exec |
| Multi-agent waves | shannon wave |

## Caching

Automatic via UnifiedOrchestrator:
- First run: Full execution
- Check cache: shannon cache stats
- Clear: shannon cache clear
