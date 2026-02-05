---
name: project-status-report
description: Generate comprehensive project health and status reports for rapid developer onboarding. Use when starting sessions, checking project health mid-work, or needing overview of git status, open work items, and suggested next actions.
---

# Project Status Report

Generate comprehensive project health and status reports for rapid developer onboarding.

## When to Use

- **Session start**: Get full project context before deciding what to work on
- **Mid-session check**: Quick health check without session overhead
- **Context switching**: Rapid re-immersion after days away from project
- **Before major changes**: Understand current state before refactoring

## What It Reports

### Priority 1: Health Indicators 🏥
- Test status (passing/failing)
- Linting errors
- Coverage metrics
- Build status
- Context health (from claude-context-manager if available)

### Priority 2: Git Status 📍
- Current branch
- Uncommitted changes
- Sync status with remote
- Active branches (recent activity)

### Priority 3: Recent Session 📖
- Last checkpoint summary
- What was accomplished
- Where you left off

### Priority 4: Open Work Items 📋
- Session objectives
- TODOs in code
- FIXMEs in code

### Priority 5: Backlog 📚
- Planned features (if configured)
- Technical debt items

### Priority 6: AI Suggestions 💡
- Recommended next actions based on project state
- Effort estimates
- Priority guidance

## Usage

### Standalone

```bash
python scripts/report.py
```

### From Claude Code

```
/project-report
```

### Programmatic

```python
from report import ReportGenerator

generator = ReportGenerator()
report = generator.generate()
print(report)
```

## Output Format

Markdown report with sections in priority order. Designed for quick scanning with emojis and clear hierarchy.

## Integration

**Used by session-management**: Automatically invoked during `/session-start` to provide onboarding context.

**Standalone utility**: Can be run independently without session management.

## Configuration

No configuration required. Automatically detects:
- Git repository
- Test frameworks (pytest)
- Session state (`.sessions/` directory)
- CCMP plugin state (`.ccmp/state.json`)

## Best Practices

**Quick check**: Run `/project-report` anytime you need project overview

**Before work**: Check health indicators before starting new work

**After context switch**: First command after returning to project

**Share with team**: Generate report for handoffs or status updates

## See Also

- **session-management**: Uses this skill for session start onboarding
- **claude-context-manager**: Provides context health metrics
