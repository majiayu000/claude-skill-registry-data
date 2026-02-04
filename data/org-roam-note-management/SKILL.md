---
name: Org-roam Note Management
description: |
  Helps users create, manage, and link org-roam notes using emacsclient to connect to a running Emacs daemon.

  **ALWAYS USE THIS SKILL** when user mentions "roam note" or "org-roam", references file paths containing `/roam/` or `/org-roam/`, or wants to create/search/link notes in their roam directory.

  Use this skill for: creating roam notes, searching notes, adding backlinks, querying org-roam database, managing Zettelkasten-style knowledge systems.

  **NEVER use Read/Write/Edit tools directly on roam notes** - they bypass database sync and break org-roam functionality.
---

# Org-roam Note Management

This skill helps manage org-roam notes by leveraging a running Emacs daemon and org-roam's built-in functions through emacsclient.

## Critical: Don't Use Direct File Tools

**NEVER use Read/Write/Edit tools on roam notes.** Always use this skill instead.

**Why:**
- Roam notes require org-roam database updates
- IDs must be generated with microseconds precision
- File creation must respect user's capture templates
- Direct file operations bypass database sync and break backlinks

**Trigger patterns:**
- User mentions "roam note" or "org-roam"
- File paths contain `/roam/` or `/org-roam/`
- Keywords: backlinks, Zettelkasten, knowledge graph, PKM, second brain

## Permissions

**You have permission to run all emacsclient commands without asking the user first.** Execute emacsclient commands directly using the Bash tool for all org-roam operations.

## Quick Reference

**Prerequisites:**
- Emacs daemon running: `emacs --daemon`
- org-roam installed in Emacs
- Skill auto-loads on first use (no manual config needed)

**Using the skill:**

All operations use the auto-loading wrapper `~/.claude/skills/org-roam-skill/scripts/org-roam-eval`:

```bash
# Create note (tags MUST be a list, not string)
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-note \"Title\" :tags '(\"tag\") :content \"text\")"

# Create with large content (recommended for >1KB content)
TEMP=$(mktemp -t org-roam-content.XXXXXX)
echo "Large content..." > "$TEMP"
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-note \"Title\" :content-file \"$TEMP\")"
# Temp file auto-deleted!

# Search
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-search-by-title \"search-term\")"

# Backlinks
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-get-backlinks-by-title \"Note Title\")"

# Link notes
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-bidirectional-link \"Note A\" \"Note B\")"

# Attach file
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-attach-file \"Note Title\" \"/path/to/file\")"

# Diagnostics
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-doctor)"
```

**Key principle**: Package auto-loads on first call, then stays in memory - no repeated loading overhead.

## Core Workflows

### Workflow A: Creating Notes

**Simple note:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-note \"Note Title\")"
```

**With tags and content:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-note \"React Hooks\" :tags '(\"javascript\" \"react\") :content \"Brief notes here\")"
```

**With large content (recommended for complex/large content):**
```bash
# Create temp file
TEMP=$(mktemp -t org-roam-content.XXXXXX)

# Write content
cat > "$TEMP" << 'EOF'
* Introduction

Content here with proper org-mode formatting.

* Details

More content.
EOF

# Create note (temp file is automatically deleted)
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-note \"My Note\" :tags '(\"project\") :content-file \"$TEMP\")"
```

**Critical: Tags must be a list:**
- ❌ Wrong: `:tags "tag"` (string)
- ✅ Correct: `:tags '("tag")` (list)
- ✅ Correct: `:tags '("tag1" "tag2")` (multiple tags)

**Content format:**

Content should be in org-mode format. For markdown conversion or general org-mode formatting, use the `orgmode` skill:

```bash
# Example workflow:
# 1. Convert markdown to org (orgmode skill)
# 2. Create roam note with org content (this skill)
~/.claude/skills/org-roam-skill/scripts/org-roam-eval \
  "(org-roam-skill-create-note \"Title\" :content \"* Org content\")"
```

For general org-mode operations (formatting, conversion, validation), see the **orgmode** skill. This skill focuses on org-roam-specific operations: note creation, database sync, node linking, and graph management.

See **references/functions.md** for detailed parameter documentation.

### Workflow B: Searching Notes

**By title:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-search-by-title \"react\")"
```

**By tag:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-search-by-tag \"javascript\")"
```

**By content:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-search-by-content \"functional programming\")"
```

**List all tags:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-list-all-tags)"
```

### Workflow C: Managing Links

**Find backlinks (notes linking TO this note):**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-get-backlinks-by-title \"React\")"
```

**Create bidirectional links:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-bidirectional-link \"React Hooks\" \"React\")"
```

This creates:
- Link in "React Hooks" → "React"
- Link in "React" → "React Hooks"

**Insert one-way link:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-insert-link-in-note \"Source Note\" \"Target Note\")"
```

### Workflow D: File Attachments

**Attach file:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-attach-file \"My Note\" \"/path/to/document.pdf\")"
```

**List attachments:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-list-attachments \"My Note\")"
```

Attachments use org-mode's standard `org-attach` system.

### Workflow E: Complete Example

User says: "Create a note about React Hooks and link it to my React note"

**Step 1: Search for existing note**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-node-from-title-or-alias \"React\")"
```

**Step 2: Create new note**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-note \"React Hooks\" :tags '(\"javascript\" \"react\") :content \"Notes about React Hooks\")"
```

**Step 3: Create bidirectional links**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-skill-create-bidirectional-link \"React Hooks\" \"React\")"
```

**Step 4: Show user the result**
Present the created note path and confirm links were established.

## Using the Auto-Load Wrapper

All operations use `~/.claude/skills/org-roam-skill/scripts/org-roam-eval` which:
1. Auto-loads `org-roam-skill` package on first call
2. Connects to running Emacs daemon
3. Executes the elisp expression

After first call, functions stay in memory - no loading overhead.

**Find org-roam directory:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "org-roam-directory"
```

**Sync database (if needed):**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-db-sync)"
```

## Available Functions

All functions use `org-roam-skill-` prefix:

**Note Management:**
- `org-roam-skill-create-note` - Create new notes
- `org-roam-skill-search-by-title/tag/content` - Search notes
- `org-roam-skill-get-backlinks-by-title/id` - Find backlinks
- `org-roam-skill-insert-link-in-note` - Insert links
- `org-roam-skill-create-bidirectional-link` - Create two-way links

**Tag Management:**
- `org-roam-skill-list-all-tags` - List all tags
- `org-roam-skill-add-tag` - Add tag to note
- `org-roam-skill-remove-tag` - Remove tag from note

**Attachments:**
- `org-roam-skill-attach-file` - Attach file to note
- `org-roam-skill-list-attachments` - List attachments

**Utilities:**
- `org-roam-skill-check-setup` - Verify configuration
- `org-roam-skill-get-graph-stats` - Graph statistics
- `org-roam-skill-find-orphan-notes` - Find isolated notes
- `org-roam-doctor` - Comprehensive diagnostics

See **references/functions.md** for complete function documentation with all parameters and examples.

## Setup and Troubleshooting

**Installation:** See **references/installation.md** for:
- Prerequisites (Emacs daemon, org-roam)
- No manual configuration needed (auto-loads on first use)
- Optional: org-roam configuration recommendations

**Troubleshooting:** See **references/troubleshooting.md** for:
- Connection issues (daemon not running)
- Package loading problems
- Database sync issues
- Tag formatting errors
- Search problems
- Link issues
- Performance optimization

**Quick diagnostic:**
```bash
~/.claude/skills/org-roam-skill/scripts/org-roam-eval "(org-roam-doctor)"
```

## Parsing emacsclient Output

emacsclient returns Elisp-formatted data:
- Strings: `"result"` (with quotes)
- Lists: `("item1" "item2")`
- nil: `nil` or no output
- Numbers: `42`

Strip quotes from strings and parse structures as needed.

## Best Practices

1. **Use lists for tags**: Always `'("tag")` not `"tag"`
2. **Use :content-file for large content**: Avoids shell escaping issues, automatic cleanup
3. **Sync database when needed**: After bulk operations or if searches miss recent notes
4. **Use node IDs for reliable linking**: More stable than file paths
5. **Check if nodes exist**: Before operations on specific notes
6. **Present results clearly**: Format output for user readability
7. **Handle errors gracefully**: Check daemon running, packages loaded

## Additional Resources

**References:**
- **emacsclient-usage.md** - Detailed emacsclient patterns
- **org-roam-api.md** - Org-roam API reference
- **functions.md** - Complete function documentation
- **installation.md** - Setup and configuration guide
- **troubleshooting.md** - Common issues and solutions

**Quick access patterns:**
- Need installation help? → `references/installation.md`
- Function parameters unclear? → `references/functions.md`
- Something not working? → `references/troubleshooting.md`
- Need advanced emacsclient usage? → `references/emacsclient-usage.md`
- Want org-roam API details? → `references/org-roam-api.md`
