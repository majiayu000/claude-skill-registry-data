---
name: nb-notes
description: Manage persistent notes and todos using the nb note-taking system. This skill should be used when capturing cross-session learnings, technical decisions, deferred tasks, or codebase patterns that should persist beyond the current conversation. Use proactively after solving bugs, making architectural decisions, or discovering important patterns. Triggers on requests like "what did I learn yesterday", "check my notes", "what learnings do I have about X", or "capture insights". Do NOT use for tracking current work-in-progress (use TodoWrite for that).
---

# nb Notes

## Overview

Manage persistent notes and todos using `nb`, a command-line note-taking system. This skill enables Claude to capture insights, decisions, and deferred tasks that should persist across sessions, while keeping current work-in-progress tracked separately in TodoWrite.

**Notebook Access:**
- **Write access:** Only the `claude` notebook (for persisting information across Claude sessions)
- **Read access:** All notebooks (for understanding user's recent learnings, reference materials, and context)
- Users may organize their nb notebooks differently - check available notebooks with `nb notebooks` or look for organizational notes in the `claude` notebook

## When to Use This Skill

### Use nb for Persistent Information

**Proactively create nb notes when:**
- Solving a bug and understanding the root cause (tag: `#bug-fix`)
- Making architectural or technical decisions (tag: `#technical-decision`)
- Discovering patterns, conventions, or antipatterns in a codebase (tag: `#code-pattern`)
- Learning about user preferences or working style (tag: `#preference`)
- Finding workflow improvements or process discoveries (tag: `#workflow`)
- Capturing insights that will be valuable in future sessions (tag: `#session-insight`)

**Use nb todo/tasks for deferred work:**
- Issues discovered during work that should be addressed later (tag: `#deferred-task`)
- Follow-up tasks or improvements to make when time permits
- Technical debt to track

### Use TodoWrite for Current Work

Keep using TodoWrite for:
- Breaking down the current task into steps
- Tracking work-in-progress during the active session
- Managing what you're actively working on right now

**Key distinction:** nb is for persistence across sessions, TodoWrite is for tracking active work within the current session.

## Creating Notes

### Standard Notes

Create markdown notes in the `claude` notebook with appropriate tags:

```bash
nb claude:add --type md --title "Note Title" --tags tag1,tag2 --content "Note content here"
```

**Example - Technical Decision:**
```bash
nb claude:add --type md \
  --title "Use factory pattern for tool instantiation" \
  --tags technical-decision,code-pattern \
  --content "Decision: Implement factory pattern for creating tools in the MCP server.

Rationale:
- Allows dynamic tool registration
- Easier to test individual tools in isolation
- Follows existing patterns in codebase

Implementation: See ToolFactory in src/tools/factory.ts"
```

**Example - Bug Fix:**
```bash
nb claude:add --type md \
  --title "Race condition in async file watcher" \
  --tags bug-fix,session-insight \
  --content "Root cause: File watcher callbacks fired before initialization completed.

Solution: Added initialization lock using async mutex. Files are queued during init and processed after lock is released.

Location: src/watchers/file-watcher.ts:145"
```

**Example - Codebase Pattern:**
```bash
nb claude:add --type md \
  --title "Error handling pattern: wrap with context" \
  --tags code-pattern,preference \
  --content "This codebase wraps errors with additional context rather than throwing new errors.

Pattern:
catch (err) {
  throw Object.assign(err, { context: 'additional info' })
}

NOT:
catch (err) {
  throw new Error(\`Failed: \${err.message}\`)
}"
```

### Deferred Tasks

Use `nb todo` or `nb tasks` for deferred work:

```bash
# Add a deferred task
nb claude:todo add "Refactor authentication module to use new JWT library" --tags deferred-task,technical-decision

# List deferred tasks
nb claude:todo list

# Complete a task
nb claude:todo do <id>
```

## Searching Notes

Before creating a note, search to avoid duplicates and to leverage existing knowledge:

```bash
# Search by keyword
nb claude:search "authentication"

# Search by tag
nb claude:search --tags technical-decision

# List recent notes
nb claude:list --limit 10

# List notes with specific tags
nb claude:list --tags code-pattern,preference
```

**When to search:**
- Before starting work on a new area of the codebase
- When encountering a familiar problem
- When making decisions (check if similar decisions were made before)

## Editing Notes

Update existing notes when information changes or needs clarification:

```bash
# Edit a note
nb claude:edit <id>

# Show a note first to see its content
nb claude:show <id>
```

## Note Quality Guidelines

**Good notes are:**
- **Specific**: Include file paths, line numbers, concrete examples
- **Actionable**: Explain not just what, but why and how
- **Searchable**: Use clear titles and appropriate tags
- **Concise**: Focus on the essential information
- **Evergreen**: Avoid temporal references ("recently", "new", "old")

**Title conventions:**
- 5-10 words
- Present tense verbs for actions: "Use factory pattern for tool creation"
- Nouns for concepts: "Authentication flow in API layer"
- Include context: "React components: Prefer composition over inheritance"

**Content structure:**
- Start with the key insight or decision
- Include rationale/context
- Add implementation details or location references
- Use code examples when helpful

## Tag Reference

Standard tags for organization:

- `#technical-decision` - Architectural choices, framework decisions, design rationale
- `#session-insight` - Important learnings or patterns discovered during work
- `#deferred-task` - Issues or improvements to address later
- `#code-pattern` - Common patterns, antipatterns, or conventions found in codebases
- `#bug-fix` - Solutions to bugs and their root causes
- `#workflow` - Process improvements or workflow discoveries
- `#preference` - User preferences and working style notes

Apply multiple tags when appropriate.

## Resources

### references/nb_commands.md

Complete reference for all nb commands, including detailed syntax for creating notes, todos, tasks, searching, and editing. Consult this file for command-line syntax details and additional examples.
