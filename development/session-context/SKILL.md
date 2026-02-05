---
name: session-context
description: Gathers session context for project-analysis agent including git history, recent plans, and pending work detection.
tools: Read, Glob, Grep, Bash
---

# Skill: session-context

Gathers session context for project-analysis agent: git history, recent plans, and pending work detection.

## Trigger

Agent invokes skill with: "Gather session context for [session_type]"

Where `session_type` is one of: `startup`, `resume`, `clear`, `compact`

## Usage

```bash
uv run --directory ${CLAUDE_SKILLS_PATH}/session-context python -m src [session_type] [--json]
```

## Arguments

- `session_type`: One of `startup`, `resume`, `clear`, `compact` (default: `startup`)
- `--json`: Output as JSON (default: human-readable)

## Output

Returns structured context including:

### Git Context
- Current branch
- Recent commits (configurable limit)
- Uncommitted changes summary
- Pending work flag

### Recent Plans
- Last N plans from `.claude/plans/`
- Topic, date, completion status for each

### Configuration
- Session behavior settings from config.yml

## Example Output (JSON)

```json
{
  "session_type": "startup",
  "git": {
    "branch": "main",
    "last_commits": [
      {"hash": "abc123", "message": "feat: add feature", "date": "2025-01-15"}
    ],
    "uncommitted_changes": {
      "staged": 2,
      "unstaged": 1,
      "untracked": 0
    },
    "has_pending_work": true
  },
  "recent_plans": [
    {
      "filename": "20250115_120000_feature-impl.md",
      "topic": "feature-impl",
      "date": "2025-01-15",
      "has_incomplete_todos": false
    }
  ],
  "config": {
    "session_behavior": "full"
  }
}
```

## Dependencies

- gitpython: Git repository interaction
- pyyaml: Config file parsing
- structlog: Logging

## Integration

This skill is invoked by the `project-analysis` agent to gather context before presenting session analysis.
