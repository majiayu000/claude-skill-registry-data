---
name: long-running-agent
description: Framework for building AI agents that work effectively across multiple context windows on complex, long-running tasks. Use when building agents for multi-hour/multi-day projects, implementing persistent coding workflows, creating systems that need state management across sessions, or when an agent needs to make incremental progress on large codebases. Provides initializer and coding agent patterns, progress tracking, feature management, and session handoff strategies.
---

# Long-Running Agent Framework

Framework for enabling AI agents to work effectively across many context windows on complex tasks.

## Core Problem

Long-running agents must work in discrete sessions where each new session begins with no memory of previous work. Without proper scaffolding, agents tend to:

1. **One-shot attempts** - Try to complete everything at once, running out of context mid-implementation
2. **Premature completion** - See partial progress and declare the job done
3. **Undocumented states** - Leave code in broken or undocumented states between sessions

## Two-Agent Solution

### 1. Initializer Agent (First Session Only)

Sets up the environment with all context future agents need:

- Create `init.sh` script for environment setup
- Generate comprehensive `feature_list.json` with all requirements
- Initialize `claude-progress.txt` for session logging
- Make initial git commit

See [references/initializer-prompt.md](references/initializer-prompt.md) for the full prompt template.

### 2. Coding Agent (Every Subsequent Session)

Makes incremental progress while maintaining clean state:

- Read progress files and git logs to get bearings
- Run basic tests to verify working state
- Work on ONE feature at a time
- Test end-to-end before marking complete
- Commit progress with descriptive messages
- Update progress file

See [references/coding-prompt.md](references/coding-prompt.md) for the full prompt template.

## Session Startup Sequence

Every coding agent session should begin:

```
1. pwd                              # Understand working directory
2. cat claude-progress.txt          # Read recent progress
3. cat feature_list.json            # Check feature status
4. git log --oneline -20            # Review recent commits
5. ./init.sh                        # Start dev environment
6. <run basic test>                 # Verify app works
7. <select next feature>            # Choose one failing feature
```

## Key Files

### feature_list.json

Comprehensive list of all features with pass/fail status. Use JSON format to prevent inappropriate edits.

```json
{
  "features": [
    {
      "category": "functional",
      "description": "User can create new chat",
      "steps": ["Navigate to main", "Click New Chat", "Verify creation"],
      "passes": false
    }
  ]
}
```

Template: [assets/feature_list_template.json](assets/feature_list_template.json)

### claude-progress.txt

Session-by-session log of work completed. Each entry includes:

- Session timestamp
- Features worked on
- Changes made
- Current state
- Next steps

Template: [assets/progress_template.md](assets/progress_template.md)

### init.sh

Environment setup script that:

- Installs dependencies
- Starts development servers
- Sets up any required services

## Critical Rules

### For Feature List

- Never remove or edit test descriptions
- Only change `passes` field status
- Mark as passing ONLY after end-to-end verification

### For Progress Tracking

- Always commit before session end
- Write descriptive commit messages
- Update progress file with summary
- Leave environment in mergeable state

### For Testing

- Use browser automation for web apps (Puppeteer MCP)
- Test as a human user would
- Verify end-to-end, not just unit tests
- Document any known limitations

## Common Failure Modes & Solutions

| Problem | Solution |
|---------|----------|
| Agent one-shots entire project | Create detailed feature list, work one at a time |
| Declares victory too early | Check feature_list.json for failing tests |
| Leaves broken state | Run basic test at session start, fix first |
| Marks features done prematurely | Require end-to-end browser testing |
| Wastes time figuring out setup | Read init.sh, use established patterns |

## Adapting to Other Domains

This framework generalizes beyond web development. Key principles:

1. **Comprehensive task decomposition** - Break work into testable units
2. **Progress persistence** - Maintain state across sessions
3. **Incremental verification** - Test after each change
4. **Clean handoffs** - Leave work in resumable state
