---
name: handoff-tracking
description: |
  Create detailed handoff documents for session transitions. Captures task status,
  learnings, decisions, and next steps in a structured format that gets indexed
  for future retrieval.

trigger: |
  - Session ending or transitioning
  - User runs /create-handoff command
  - Context pressure requiring /clear
  - Completing a major milestone

skip_when: |
  - Quick Q&A session with no implementation
  - No meaningful work to document
  - Session was exploratory with no decisions

related:
  before: [executing-plans, subagent-driven-development]
  after: [artifact-query]
---

# Handoff Tracking

## Overview

Create structured handoff documents that preserve session context for future sessions. Handoffs capture what was done, what worked, what failed, key decisions, and next steps.

**Core principle:** Handoffs are indexed immediately on creation, making them searchable before the session ends.

**Announce at start:** "I'm creating a handoff document to preserve this session's context."

## When to Create Handoffs

| Situation | Action |
|-----------|--------|
| Session ending | ALWAYS create handoff |
| Running /clear | Create handoff BEFORE clear |
| Major milestone complete | Create handoff to checkpoint progress |
| Context at 70%+ | Create handoff, then /clear |
| Blocked and need help | Create handoff with blockers documented |

## Handoff File Location

**Path:** `docs/handoffs/{session-name}/YYYY-MM-DD_HH-MM-SS_{description}.md`

Where:
- `{session-name}` - From active work context (e.g., `context-management`, `auth-feature`)
- `YYYY-MM-DD_HH-MM-SS` - Current timestamp in 24-hour format
- `{description}` - Brief kebab-case description of work done

**Example:** `docs/handoffs/context-management/2025-12-27_14-30-00_handoff-tracking-skill.md`

If no clear session context, use `general/` as the folder name.

## Handoff Document Template

Use this exact structure for all handoff documents:

~~~markdown
---
date: {ISO timestamp with timezone}
session_name: {session-name}
git_commit: {current commit hash}
branch: {current branch}
repository: {repository name}
topic: "{Feature/Task} Implementation"
tags: [implementation, {relevant-tags}]
status: {complete|in_progress|blocked}
outcome: UNKNOWN
root_span_id: {trace ID if available, empty otherwise}
turn_span_id: {turn span ID if available, empty otherwise}
---

# Handoff: {concise description}

## Task Summary
{Description of task(s) worked on and their status: completed, in_progress, blocked.
If following a plan, reference the plan document and current phase.}

## Critical References
{2-3 most important file paths that must be read to continue this work.
Leave blank if none.}
- `path/to/critical/file.md`

## Recent Changes
{Files modified in this session with line references}
- `src/path/to/file.py:45-67` - Added validation logic
- `tests/path/to/test.py:10-30` - New test cases

## Learnings

### What Worked
{Specific approaches that succeeded - these get indexed for future sessions}
- Approach: {description} - worked because {reason}
- Pattern: {pattern name} was effective for {use case}

### What Failed
{Attempted approaches that didn't work - helps future sessions avoid same mistakes}
- Tried: {approach} -> Failed because: {reason}
- Error: {error type} when {action} -> Fixed by: {solution}

### Key Decisions
{Important choices made and WHY - future sessions reference these}
- Decision: {choice made}
  - Alternatives: {other options considered}
  - Reason: {why this choice}

## Files Modified
{Exhaustive list of files created or modified}
- `path/to/new/file.py` - NEW: Description
- `path/to/existing/file.py:100-150` - MODIFIED: Description

## Action Items & Next Steps
{Prioritized list for the next session}
1. {Most important next action}
2. {Second priority}
3. {Additional items}

## Other Notes
{Anything else relevant: codebase locations, useful commands, gotchas}
~~~

## The Process

### Step 1: Gather Session Metadata

```bash
# Get current git state
git rev-parse HEAD        # Commit hash
git branch --show-current # Branch name
git remote get-url origin # Repository

# Get timestamp
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

### Step 2: Determine Session Name

Check for active work context:
1. Recent plan files in `docs/plans/` - extract feature name
2. Recent branch name - use as session context
3. If unclear, use `general`

### Step 3: Write Handoff Document

1. Create handoff directory if needed: `mkdir -p docs/handoffs/{session-name}/`
2. Write handoff file with template structure
3. Fill in all sections with session details
4. Be thorough in learnings - these feed compound learning

### Step 4: Verify Indexing

After writing the handoff, verify it was indexed:

```bash
# Check artifact index updated (if database exists)
sqlite3 .ring/cache/artifact-index/context.db \
  "SELECT id, session_name FROM handoffs ORDER BY indexed_at DESC LIMIT 1"
```

The PostToolUse hook automatically indexes handoffs on Write.

## Integration with Ring

### Execution Reports
When working within dev-team cycles, the handoff's "Recent Changes" and "Files Modified" sections should mirror the execution report format:

| Metric | Include |
|--------|---------|
| Duration | Time spent on session |
| Tasks Completed | X/Y from plan |
| Files Created | N |
| Files Modified | N |
| Tests Added | N |

### Session Traces
If session tracing is enabled (Braintrust, etc.), include:
- `root_span_id` - Main trace ID
- `turn_span_id` - Current turn span

These enable correlation between handoffs and detailed session logs.

## Outcome Tracking

Outcomes are marked AFTER the handoff is created, either:
1. User responds to Stop hook prompt
2. User runs outcome marking command later

**Valid outcomes:**
| Outcome | Meaning |
|---------|---------|
| SUCCEEDED | Task completed successfully |
| PARTIAL_PLUS | Mostly done, minor issues remain |
| PARTIAL_MINUS | Some progress, major issues remain |
| FAILED | Task abandoned or blocked |

Handoffs start with `outcome: UNKNOWN` and get updated when marked.

## Remember

- **Be thorough in Learnings** - These feed the compound learning system
- **Include file:line references** - Makes resumption faster
- **Document WHY not just WHAT** - Decisions without rationale are useless
- **Index happens automatically** - PostToolUse hook handles it
- **Outcome is separate** - Don't try to guess outcome, leave as UNKNOWN
