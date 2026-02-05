---
name: stash-pad
description: >
  Use this skill when the user wants to capture todos, ideas, or thoughts
  quickly during CLI coding sessions. Activate when user says :add, :a, :done, :d,
  :classify, :c, :show, :s, :now, :n, :restore, :r, :find, :f, :archive, or :ar.
  Manages a TODO.md file with inbox, categories, completion tracking, and restore.
  Works mid-session without disrupting workflow.
allowed-tools: Read, Edit, Write
---

# Stash Pad

A universal skill for capturing, organizing, and classifying thoughts, ideas, and todos using a simple file-based inbox system.

## Overview

This skill enables any LLM assistant to help users capture thoughts quickly and organize them later. It follows a "capture first, classify later" workflow that reduces friction when brainstorming.

---

## Triggers

Activate this skill when the user says any of the following:

| Command | Shortcut | Action |
|---------|----------|--------|
| `:add` | `:a` | Add item(s) to inbox |
| `:done` | `:d` | Mark item complete |
| `:classify` | `:c` | Organize inbox |
| `:show` | `:s` | Display list |
| `:now` | `:n` | Add + classify |
| `:restore` | `:r` | Restore from completed |
| `:find` | `:f` | Search all todos |
| `:archive` | `:ar` | Clear completed items |

> **Tip:** To customize triggers, edit this file directly.

### Activation Guidelines

**Use this skill when:**
- User explicitly wants to manage todos/tasks
- Command appears at the start of user input
- Context suggests todo management intent

**Do NOT activate when:**
- `:a`, `:d`, etc. appear mid-sentence or in code/paths
- User is discussing something unrelated to task management
- The colon-prefixed text is part of a filename, URL, or code snippet

---

## Core Behaviors

### 1. Capturing Items

When the user provides items to capture:

1. **Parse the input**:
   - If input contains semicolons (`;`), split into multiple items
   - Trim whitespace from each item
   - Preserve the user's original wording

2. **Add to Inbox**:
   - Open the project's `TODO.md` file
   - If `## Inbox` section doesn't exist, append it to the end of the file first
   - Append each item to the `## Inbox` section as `- [ ] <item>`
   - Confirm what was added

3. **Suggest classification** (optional):
   - Briefly note what category each item might belong to
   - Example: "Added. (That's likely a **Feature**)"

### 2. Classifying Items

When the user says "classify" or similar:

1. **Read the Inbox** section of `TODO.md`

2. **For each item**, determine the best category:
   - **Features** - New functionality
   - **Improvements** - Enhancements to existing functionality
   - **Bug Fixes** - Issues that need fixing
   - **Documentation** - Docs, README, examples
   - **Ideas** - Exploratory thoughts, research topics

3. **Group related items** under subheadings when patterns emerge
   - Example: Multiple UI items → create "### User Interfaces" subheading

4. **Move items** from Inbox to their categories

5. **Clear the Inbox** after classification

6. **Show summary** of what was classified where

7. **Handle empty inbox**:
   - If inbox is empty, respond: "Inbox is empty. Nothing to classify."

### 3. Completing Items

When the user says `:done <text>` or `:d <text>`:

1. **Search all categories** in `TODO.md` for matching items
   - Match partial text (case-insensitive)
   - Example: `done: auth` matches `- [ ] add user authentication`

2. **For each match**:
   - Change `- [ ]` to `- [x]`
   - Move the item to `## Completed` section
   - Add date prefix: `- [x] 2024.11.30 - item text`

3. **Handle ambiguity**:
   - If multiple items match, list them and ask which one(s)
   - If no items match, respond: "No matching items found for '<text>'."

4. **Confirm completion**:
   - Brief confirmation with the item text
   - Example: `✓ Marked "add user authentication" complete`

### 4. Add and Classify

When the user says `:now <text>` or `:n <text>`:

1. **Add item(s) to Inbox** (same as `:add`)
2. **Immediately classify** the new item(s)
3. **Return combined confirmation**:
   - Example: `Added and classified: "add dark mode" → Features`

### 5. Restoring Items

When the user says `:restore` or `:r`:

1. **Without arguments** - Display completed items (newest first):
   ```
   Completed (newest first):
   1. 2024.11.30 - add user authentication
   2. 2024.11.29 - fix login bug
   3. 2024.11.28 - update README

   Restore with :r <number> or :r <text>
   ```

2. **With number(s)** - `:r 1` or `:r 1 3`:
   - Restore specified items to Inbox
   - Remove from Completed section

3. **With text** - `:r auth`:
   - Search Completed for matches
   - Handle ambiguity same as `:done`

4. **Confirm restoration**:
   - Example: `Restored "add user authentication" to inbox.`

### 6. Searching Items

When the user says `:find <text>` or `:f <text>`:

1. **Search all sections** of TODO.md for matching items
   - Case-insensitive partial match

2. **Return matches with location**:
   ```
   Found 3 matches for "auth":

   Features:
   - add user authentication

   Bug Fixes:
   - fix auth token expiry

   Completed:
   - 2024.11.28 - remove old auth code
   ```

3. **Handle no matches**:
   - Respond: "No items found matching '<text>'."

### 7. Archiving Completed Items

When the user says `:archive` or `:ar`:

1. **Clear the Completed section**:
   - Remove all items from `## Completed`
   - Or move to `## Archived` section if it exists

2. **Confirm action**:
   - Example: `Archived 5 completed items.`

3. **Handle empty**:
   - If Completed is empty, respond: "Nothing to archive."

### 8. Creating TODO.md

If `TODO.md` doesn't exist:

1. **Ask the user first**: "No TODO.md found. Create one?"
2. **If user confirms**, create it with this template:

```markdown
# Project Todo List

## Features
<!-- New functionality to add -->

## Improvements
<!-- Enhancements to existing functionality -->

## Bug Fixes
<!-- Issues that need fixing -->

## Documentation
<!-- Docs, README, examples -->

## Ideas
<!-- Raw thoughts to classify later -->

---

## Inbox
<!-- Drop any thought here - assistant will classify it -->

---

## Completed
<!-- Done items moved here automatically -->

```

---

## Response Style

- **Be brief** when adding items - just confirm what was added
- **Be helpful** when classifying - show the organization clearly
- **Use tables or trees** to display structure when helpful
- **Don't over-explain** - the user knows what they meant

### Good Response (Adding)
```
Added 3 items to inbox.
```

### Good Response (Classifying)
```
Classified 5 items:

Features (3)
├── User authentication
├── Dark mode
└── Export to PDF

Improvements (2)
├── Faster load times
└── Better error messages

Inbox is empty.
```

---

## Customization

### Project-Specific Categories

Users may have custom categories. Detect these from the existing `TODO.md` structure and use them. Common variations:

- `## Technical Debt` - Code that needs refactoring
- `## Research` - Topics to investigate
- `## Questions` - Things to clarify with stakeholders
- `## Blocked` - Items waiting on dependencies

### Priority Markers

If the user includes priority markers, preserve them:
- `[P0]`, `[P1]`, `[P2]` - Priority levels
- `[urgent]`, `[low]` - Priority labels
- `!!!` - High priority indicator

---

## Examples

### Adding Items
**User**: `:a add user authentication`
**Assistant**: Added to inbox.

**User**: `:add fix login bug; add dark mode; update README`
**Assistant**: Added 3 items to inbox.

### Classification
**User**: `:c`
**Assistant**:
Classified 3 items:

| Item | Category |
|------|----------|
| Fix login bug | Bug Fixes |
| Add dark mode | Features |
| Update README | Documentation |

### Ambiguous Match
**User**: `:done bug`
**Assistant**:
Found 2 matches:
1. Fix login bug
2. Fix signup bug

Which one(s)? (1, 2, or both)

### Restore
**User**: `:r`
**Assistant**:
Completed (newest first):
1. 2024.11.30 - add user authentication
2. 2024.11.29 - fix login bug

Restore with :r <number> or :r <text>

**User**: `:r 1`
**Assistant**: Restored "add user authentication" to inbox.

---

## File Location

By default, look for `TODO.md` in the project root. If not found:
1. Ask user if they want to create one
2. Or check for alternatives: `TODOS.md`, `todo.md`, `.todo/inbox.md`

---

## Cross-LLM Compatibility

This skill is designed to work with any LLM that can:
- Read and write files
- Parse markdown
- Follow instruction patterns

### Claude Code
Place this file in `.claude/skills/` or reference it in `CLAUDE.md`

### Gemini
Include these instructions in your system prompt or context

### OpenAI Codex
Add to your instructions file or system context

### Other LLMs
Adapt the triggers and file operations to your platform's capabilities

---

## Version

2.0.1 - Anthropic guidelines compliance; activation guardrails; user consent for file creation
2.0.0 - Added restore, find, archive commands; date-prefixed completed items
1.0.0 - Initial release
