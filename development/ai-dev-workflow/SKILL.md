---
name: ai-dev-workflow
description: Multi-agent development workflow system for structured task execution. Use when working with tasks in .tasks/ directory, when user invokes /task, /explore, /research, /spec, /build, /review, or /refactor commands, or when Claude needs to understand the task orchestration system. Provides workflow state management, sub-agent coordination, and session persistence.
---

# AI Development Workflow

A structured workflow system where Claude Code orchestrates sub-agents to execute development tasks with full state persistence across sessions.

## Workflow Overview

```
User Input → /task → /explore → /research → /spec → /build → /review → /refactor → Done
```

Each stage persists state in `.tasks/{task-name}/` enabling:
- Session continuity (resume work anytime)
- Sub-agent coordination (agents read each other's output)
- Clear progress tracking

## Directory Structure

```
.tasks/
└── {task-name}/
    ├── status.md    # Current phase, activity log
    ├── task.md      # Requirements + clarifications Q&A
    ├── explore.md   # Codebase analysis
    ├── research.md  # Documentation, patterns, snippets
    ├── spec.md      # Implementation plan with phases
    ├── review.md    # Code review findings
    └── refactor.md  # Applied fixes
```

## Workflow Stages

### 1. Task (`/task`)
- Collect requirements from user
- Ask clarifying questions (document Q&A in task.md)
- Generate task name (kebab-case)
- Create directory structure

### 2. Explore (`/explore`)
- Analyze codebase relevant to task
- Use builtin Explore agent
- Document: structure, stack, relevant files, patterns

### 3. Research (`/research`)
- Delegate to `research` sub-agent with GRANULAR queries
- Spawn MULTIPLE research agents for specific topics (not one big request)
- Must match INSTALLED versions
- Output: code snippets, official docs, patterns

### 4. Spec (`/spec`)
- Delegate to `spec` sub-agent
- Create phases: small, independent, executable in separate sessions
- Include code snippets as implementation guides
- Define clear "done" criteria per phase

### 5. Build (`/build`)
- Follow spec.md exactly
- Implement phase by phase
- Update status.md progress
- Use research.md snippets as reference

### 6. Review (`/review`)
- Delegate to `review` sub-agent
- Check: naming, duplication, security, organization, docs
- Categorize: ❌ HIGH, ⚠️ MEDIUM, 💡 LOW
- Compare implementation vs spec

### 7. Refactor (`/refactor`)
- Delegate to `refactor` sub-agent
- Fix issues from review.md by priority
- Surgical changes only (no scope creep)
- Document all changes

## Sub-Agent Coordination

Claude Code acts as orchestrator. Sub-agents:
- Read previous stage outputs
- Write to their designated .md file
- Update status.md activity log

**Research agent pattern:** Call multiple times with specific queries:
```
Agent 1: "Better Auth session configuration"
Agent 2: "Drizzle auth schema pattern"
Agent 3: "Next.js 15 middleware auth"
```

## Status Tracking

status.md format:
```markdown
## Current Phase
- [x] Task Definition
- [x] Explore
- [ ] Research  ← current
- [ ] Spec
- [ ] Build
- [ ] Review
- [ ] Refactor

## Activity Log
- [2025-01-15 10:30] Task initialized
- [2025-01-15 10:45] Explore complete
```

## Session Continuity

When resuming work:
1. Check `.tasks/` for active tasks
2. Read `status.md` to find current phase
3. Read relevant .md files for context
4. Continue from where left off

## Rules

1. ALWAYS use plan mode to interact with user at decision points
2. ALWAYS update status.md after completing any stage
3. Each phase in spec.md must be independently executable
4. Research must be granular (multiple specific queries)
5. Never deviate from spec during build without discussion
6. Review must be thorough; refactor must be surgical

## References

- `references/file-formats.md` - Templates for each markdown file
- `references/slash-commands.md` - All slash commands for this workflow
- `references/sub-agents.md` - Descriptions for creating sub-agents via /agents
