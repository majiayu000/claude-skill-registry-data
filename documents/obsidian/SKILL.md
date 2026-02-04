---
name: obsidian
description: Interact with Obsidian vaults via obsidian-cli. Read, create, search, and manage markdown notes. Use when user references their Obsidian vault, wants to save information to notes, search their knowledge base, or organize their personal knowledge management system.
---

# Obsidian Vault Integration

This skill enables interaction with Obsidian vaults through the `obsidian-cli` tool and direct filesystem operations.

## When to Use This Skill

Use this skill when the user:
- Mentions their Obsidian vault or notes
- Wants to save information, research, or summaries to notes
- Asks to search their knowledge base or "my notes"
- Wants to organize, rename, or manage their notes
- References personal knowledge management (PKM)
- Asks to read or retrieve information from their notes

## Reading Notes

Read note contents directly:

```bash
# By note name (searches entire vault)
obsidian-cli print "note-name"

# By path from vault root
obsidian-cli print "folder/subfolder/note-name"

# Note: .md extension is optional
```

## Creating Notes

Use direct file writes for reliable note creation:

```bash
# Get vault path
VAULT=$(obsidian-cli print-default --path-only)

# Create a new note
cat > "$VAULT/note-name.md" << 'EOF'
# Note Title

Content goes here.
EOF

# Create in a subfolder
mkdir -p "$VAULT/folder"
cat > "$VAULT/folder/note-name.md" << 'EOF'
# Title

Content here.
EOF
```

## Appending to Notes

Add content to existing notes:

```bash
VAULT=$(obsidian-cli print-default --path-only)

# Append a new section
cat >> "$VAULT/note-name.md" << 'EOF'

## New Section

Additional content appended.
EOF
```

## Searching Notes

Use grep for non-interactive content search:

```bash
VAULT=$(obsidian-cli print-default --path-only)

# Search for content across all notes
grep -r -n -i "search term" "$VAULT" --include="*.md"

# Find files containing a term (filenames only)
grep -r -l -i "search term" "$VAULT" --include="*.md"

# List all notes in vault
find "$VAULT" -name "*.md" -type f | sed "s|$VAULT/||" | sort

# Search by filename pattern
find "$VAULT" -name "*.md" -type f | sed "s|$VAULT/||" | grep -i "pattern"
```

## Moving and Renaming Notes

The move command automatically updates all wikilinks:

```bash
# Rename a note (updates [[old-name]] links throughout vault)
obsidian-cli move "old-name" "new-name"

# Move to a different folder
obsidian-cli move "note-name" "folder/note-name"

# Move with full paths
obsidian-cli move "old-folder/note" "new-folder/note"
```

## Deleting Notes

```bash
# Delete a note (permanent, no trash)
obsidian-cli delete "note-name"

# Delete by path
obsidian-cli delete "folder/note-name"
```

## Working with Frontmatter

Extract and view YAML frontmatter:

```bash
# View full note including frontmatter
obsidian-cli print "note-name"

# Extract just the frontmatter
obsidian-cli print "note-name" | sed -n '/^---$/,/^---$/p'
```

To modify frontmatter, read the note, edit the content, and write it back:

```bash
VAULT=$(obsidian-cli print-default --path-only)

# Read current content
CONTENT=$(obsidian-cli print "note-name")

# Write modified content back
cat > "$VAULT/note-name.md" << 'EOF'
---
title: Updated Title
tags: [tag1, tag2]
---

# Heading

Updated content here.
EOF
```

## Multi-Vault Support

Specify a different vault for any command:

```bash
# Read from a specific vault
obsidian-cli print "note" --vault "work-vault"

# Move within a specific vault
obsidian-cli move "old" "new" --vault "personal-vault"
```

## Common Workflows

### Save Research to a Note

```bash
VAULT=$(obsidian-cli print-default --path-only)

# Check if note exists
if obsidian-cli print "Research/topic" >/dev/null 2>&1; then
    # Append to existing note
    cat >> "$VAULT/Research/topic.md" << 'EOF'

## Additional Findings

New research content here.
EOF
else
    # Create new note
    mkdir -p "$VAULT/Research"
    cat > "$VAULT/Research/topic.md" << 'EOF'
# Topic Research

Initial research content.
EOF
fi
```

### Find and Read Related Notes

```bash
VAULT=$(obsidian-cli print-default --path-only)

# Search for related notes
grep -r -l -i "keyword" "$VAULT" --include="*.md"

# Read each match
obsidian-cli print "matching-note-1"
obsidian-cli print "matching-note-2"
```

### Organize Notes into Folders

```bash
# Find notes matching a pattern
VAULT=$(obsidian-cli print-default --path-only)
find "$VAULT" -name "*meeting*.md" -type f | sed "s|$VAULT/||"

# Move each to organized folder
obsidian-cli move "standup-2024-01-15" "Meetings/standup-2024-01-15"
obsidian-cli move "standup-2024-01-16" "Meetings/standup-2024-01-16"
```

### Create a Daily Note

```bash
VAULT=$(obsidian-cli print-default --path-only)
TODAY=$(date +%Y-%m-%d)

mkdir -p "$VAULT/Daily"
cat > "$VAULT/Daily/$TODAY.md" << EOF
# Daily Note - $TODAY

## Tasks
- [ ]

## Notes

## End of Day Review

EOF
```

## Important Notes

1. **Path resolution**: Note names don't need `.md` extension; paths are relative to vault root
2. **Wikilink updates**: The `move` command automatically updates `[[note]]`, `[[note|display]]`, and `[[note#heading]]` links
3. **Case sensitivity**: Search is case-insensitive with `-i` flag
4. **Hidden files**: Operations skip hidden directories (starting with `.`)
5. **Large files**: Files over 10MB are skipped during search operations
6. **No trash**: Delete is permanent; there's no recycle bin

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot find vault config` | No default vault set | Run `obsidian-cli set-default "vault-name"` |
| `Vault not found in Obsidian config` | Vault name doesn't match | Check vault name in Obsidian app settings |
| `Cannot find note in vault` | Note doesn't exist | Verify note name/path with search |

