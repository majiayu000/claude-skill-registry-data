---
name: setup-cdk-memory
description: Use when setting up context management for Claude Code - configures conversation search, context summarization, session export, and project memory patterns for long-running development
---

# Setup CDK Memory

## Overview

Context and memory management for Claude Code sessions. Helps maintain project knowledge across sessions, search past conversations, export session history, and optimize context usage.

## When to Use

- Setting up long-term project memory
- User asks about maintaining context across sessions
- Part of `setup-claude-dev-kit` full bundle
- Managing large codebases with Claude

## Quick Reference

| Component | Location |
|-----------|----------|
| Session logs | `~/.claude/sessions/` |
| Project memory | `.claude/memory/` |
| Context cache | `.claude/context/` |
| Export output | `~/.claude-dev-kit/exports/` |

## Memory Concepts

| Type | Scope | Purpose |
|------|-------|---------|
| **Session** | Single conversation | Current task context |
| **Project** | One codebase | Architecture, patterns, decisions |
| **Global** | All projects | Personal preferences, common patterns |

## Installation Steps

### 1. Create Memory Directories

```bash
# Global Claude directories
mkdir -p ~/.claude/sessions
mkdir -p ~/.claude-dev-kit/exports

# Project-level directories
mkdir -p .claude/memory
mkdir -p .claude/context
```

### 2. Project Memory File

Create `.claude/memory/project.md`:

```markdown
# Project Memory

## Architecture Decisions

### [Date] - Decision Title
**Context:** Why this decision was needed
**Decision:** What was decided
**Consequences:** Trade-offs and implications

## Key Patterns

### Pattern Name
- Where: `src/path/to/usage`
- When to use: Description
- Example: Brief code snippet

## Known Issues

### Issue Title
- Status: Open/Resolved
- Workaround: If applicable
- Related: Links to issues/PRs

## External Dependencies

| Dependency | Version | Purpose | Notes |
|------------|---------|---------|-------|
| name | x.y.z | why used | quirks |

## Team Conventions

- Naming: [conventions]
- File structure: [patterns]
- Testing: [approach]
```

### 3. Context Optimization Commands

Create `.claude/commands/context-status.md`:

```markdown
Analyze and report on the current context:

1. List files currently in context
2. Estimate token usage
3. Identify large files that could be summarized
4. Suggest files that could be removed from context
5. Recommend priority files to keep

Format as a table with file, tokens (estimate), and recommendation.
```

Create `.claude/commands/summarize-file.md`:

```markdown
Create a concise summary of the specified file for memory storage:

1. Purpose of the file
2. Key exports/functions (signature only)
3. Dependencies it relies on
4. Files that depend on it
5. Important implementation notes

Keep under 50 lines. Store in `.claude/context/summaries/`
```

### 4. Session Export Utility

Create `~/.claude-dev-kit/bin/claude-export`:

```bash
#!/bin/bash
# Export Claude session to markdown

OUTPUT_DIR="$HOME/.claude-dev-kit/exports"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
PROJECT_NAME=$(basename "$PWD")
OUTPUT_FILE="$OUTPUT_DIR/${PROJECT_NAME}-${TIMESTAMP}.md"

cat > "$OUTPUT_FILE" << EOF
# Claude Session Export

**Project:** $PROJECT_NAME
**Date:** $(date '+%Y-%m-%d %H:%M')
**Directory:** $PWD

---

## Session Summary

[Add summary here]

## Key Decisions

-

## Code Changes

-

## Follow-up Tasks

- [ ]

---

*Exported from Claude Code session*
EOF

echo "Created: $OUTPUT_FILE"
echo "Edit to add session details, or use Claude to fill in."
```

Make executable:
```bash
chmod +x ~/.claude-dev-kit/bin/claude-export
```

Add to PATH in `.zshrc`:
```bash
export PATH="$HOME/.claude-dev-kit/bin:$PATH"
```

### 5. Conversation Search Helper

Create `.claude/commands/search-memory.md`:

```markdown
Search project memory for relevant context:

1. Search `.claude/memory/` for keywords
2. Search `.claude/context/summaries/` for file summaries
3. Check CLAUDE.md for project context
4. Look in recent git commits for related changes

Report findings organized by relevance.
```

### 6. Context Refresh Command

Create `.claude/commands/refresh-context.md`:

```markdown
Refresh understanding of the project:

1. Re-read CLAUDE.md
2. Check `.claude/memory/project.md` for decisions
3. Review recent git log (last 10 commits)
4. Scan for TODO/FIXME comments
5. Check for failing tests

Provide a brief status report of the project state.
```

### 7. Memory Patterns

#### Decision Log Pattern

When making significant decisions, append to `.claude/memory/project.md`:

```markdown
### [YYYY-MM-DD] Decision Title

**Context:**
The situation that required a decision.

**Options Considered:**
1. Option A - pros/cons
2. Option B - pros/cons

**Decision:**
What was chosen and why.

**Consequences:**
- Positive: benefits
- Negative: trade-offs
- Risks: potential issues
```

#### Session Handoff Pattern

Before ending a session, create handoff notes:

```markdown
## Session Handoff - [Date]

### Completed
- [x] Task 1
- [x] Task 2

### In Progress
- [ ] Task 3 (blocked by X)

### Context for Next Session
- Working on feature Y
- Key file: `src/path/to/file.ts`
- Issue encountered: description
- Next step: what to do

### Open Questions
- Question 1?
- Question 2?
```

### 8. Global Memory Setup

Create `~/.claude/memory/preferences.md`:

```markdown
# Claude Preferences

## Code Style
- Prefer: [style preferences]
- Avoid: [anti-patterns]

## Communication
- Detail level: [concise/detailed]
- Explanation style: [examples/theory]

## Common Patterns
- Error handling: [approach]
- Testing: [preferences]
- Documentation: [style]

## Project-Agnostic Knowledge
- Frequently used libraries
- Personal conventions
- Learned lessons
```

## Verification

```bash
# Check directories exist
[ -d .claude/memory ] && echo "Project memory directory exists"
[ -d ~/.claude/sessions ] && echo "Session directory exists"

# Check memory file
[ -f .claude/memory/project.md ] && echo "Project memory file exists"

# Check export utility
command -v claude-export && echo "Export utility installed"

# Check commands
ls .claude/commands/ | grep -E "(context|memory|summarize)" && echo "Memory commands installed"
```

## Usage Patterns

### Starting a Session

```
"Refresh context on this project"
```

Claude will read CLAUDE.md, memory files, and recent history.

### During Development

```
"Log this architecture decision about [topic]"
```

Claude will append to the decision log.

### Ending a Session

```
"Create handoff notes for the next session"
```

Claude will summarize progress and open items.

### Searching History

```
"Search memory for how we handled [topic]"
```

Claude will search memory files and summaries.

## Adaptation Mode

When existing memory setup detected:

1. **Check for existing patterns:**
```bash
[ -f .claude/memory/* ] && echo "Existing memory files found"
[ -d docs/decisions ] && echo "ADR directory found"
```

2. **Merge approach:**
- Don't overwrite existing memory files
- Add CDK patterns alongside
- Suggest consolidation if duplicates found

3. **Integrate with ADRs:**
If project uses Architecture Decision Records:
```bash
# Link ADR directory to memory
ln -s ../docs/decisions .claude/memory/adr
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Memory files too large | Summarize and archive old entries |
| Context getting stale | Run refresh-context command |
| Can't find past decision | Search memory with specific keywords |
| Session export empty | Fill in manually or use Claude to summarize |

## Memory Maintenance

### Weekly
- Review and clean up session exports
- Update project.md with new decisions

### Monthly
- Archive old memory entries
- Update file summaries for changed files
- Review and update CLAUDE.md

### Per Release
- Document major changes in memory
- Update architecture decisions
- Clean up resolved issues

## Tips

1. **Keep memory concise** - Long files hurt context efficiency
2. **Use structured formats** - Tables and lists scan faster
3. **Date everything** - Helps track currency of information
4. **Link to code** - Use file:line references
5. **Summarize, don't duplicate** - Reference files, don't copy them
