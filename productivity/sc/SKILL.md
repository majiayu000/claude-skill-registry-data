---
name: sc
description: Supernal Coding CLI for development workflows - task management, requirements tracking, testing, git automation, ralph loops, compliance, and documentation. Use for task management (sc task), project health checks, traceability, spec management, or autonomous task execution.
---

# sc - Supernal Coding CLI

Development workflow automation, task management, requirements tracking, and autonomous task execution.

Canonical scope:
- `sc` is for developer/project workflow commands.
- `orch` is for orchestration runtime operations (capacity/spawn/triage/heartbeat/automation).
- Do not assume same-name commands across CLIs are semantic equivalents.

## Installation

```bash
npm install -g @supernalintelligence/supernal-coding
```

## Quick Reference

### Task Management (PRIMARY)
```bash
sc task create "Title" --assignee @me --priority P2
sc task list                         # Your tasks  
sc task list --all                   # All repos
sc task list --status in-progress    # Filter by status
sc task view TASK-123                # View task details
sc task start TASK-123               # Begin work (sets in-progress)
sc task done TASK-123 --notes "..."  # Complete task
sc task next                         # Get next task (ralph mode)
sc task verify TASK-123              # Check evidence (optional)
sc task edit TASK-123                # Edit in $EDITOR

# Session linkage (dashboard only - requires localhost:3006)
sc task link TASK-123                # Link to current session (needs OPENCLAW_SESSION_KEY)
sc task link TASK-123 --session "..."  # Link with explicit session
sc task linked                       # List linked tasks
sc task unlink TASK-123              # Remove link
```

**Storage:** `.supernal/tasks/` (per-repo) or `~/.supernal/tasks/` (global)

**Workflow Guide:** See `docs/TASK_WORKFLOW.md` for how tasks, requirements, features, and specs work together.

### Project Health & Status
```bash
sc health                    # Run health checks
sc monitor                   # Development status dashboard
sc status                    # Alias for monitor
```

### Requirements & Traceability
```bash
sc trace                     # Traceability matrix
sc planning                  # Manage epics, features, requirements, tasks
sc audit                     # Audit features, requirements, tests
```

### Git & Workflow
```bash
sc git                       # Git workflow operations
sc git smart                 # Smart commits, branch management
sc workflow                  # Project workflow management
```

### Ralph (Autonomous Loops)
```bash
sc ralph                     # Autonomous task execution
sc spec <action> [target]    # Spec file management for ralph loops
```

### Code Quality
```bash
sc code <action>             # Code quality and contracts
sc compliance                # HIPAA, SOC 2, ISO 27001 validation
sc security                  # Database security verification
```

### Documentation
```bash
sc docs                      # Documentation management
sc search <query>            # Search across all content
```

### System
```bash
sc init [dir]                # Initialize project
sc update                    # Check for updates
sc system                    # Config, upgrade, sync, license
```

## Common Patterns

### New Feature Workflow
```bash
sc planning feature create "Add user auth"
sc spec create auth-feature.md
sc ralph execute auth-feature.md
```

### Health Check Before PR
```bash
sc health
sc audit
sc compliance check
```

### Knowledge & Workspace Hygiene
```bash
# Run knowledge store cleanup (pair with sc health)
know tidy              # Audit knowledge store
know tidy --fix        # Auto-fix issues (normalize tags, move misplaced files)
know reindex           # Rebuild INDEX.md
know validate          # Check frontmatter schema

# Recommended: add to heartbeat or nightly cron
know tidy --fix && know reindex
```

### Traceability Report
```bash
sc trace report --format markdown
```

## Integration with Agents

### Task Assignment Flow
```bash
# Orchestrator assigns task
sc task create "Build API endpoint" --assignee @codex-coder --priority P1

# Agent picks up work
sc task next                # Get your next assigned task
sc task start TASK-123      # Mark as in-progress
# ... do work ...
sc task done TASK-123 --notes "Completed, PR #456"
```

### Ralph Loops (Autonomous Execution)
```bash
# Create spec
sc spec create task-name.md

# Execute with ralph
sc ralph execute task-name.md --max-iterations 10
```

See `orch` skill for agent orchestration and spawning.
