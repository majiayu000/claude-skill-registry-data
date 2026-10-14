---
name: linux-notes
description: Manage notes on Linux via simple markdown files in a notes directory. Create, view, edit, delete, search, and list notes. Use when a user asks FRIDAY to add a note, list notes, search notes, or manage notes on Linux.
homepage: https://github.com/friday-ai/friday
metadata: {"friday":{"emoji":"📝","os":["linux"],"requires":{"bins":["cat","grep","find"]},"install":[]}}
---

# Linux Notes CLI

Use simple bash commands to manage markdown notes in `~/friday-notes/`. This is a Linux alternative to Apple Notes.

## Setup
Create the notes directory:
```bash
mkdir -p ~/friday-notes
```

## View Notes

### List all notes
```bash
find ~/friday-notes -name "*.md" -type f -printf "%T@ %p\n" | sort -rn | cut -d' ' -f2- | head -20
```

### View a specific note
```bash
cat ~/friday-notes/note-name.md
```

### Search notes (fuzzy)
```bash
grep -ril "search query" ~/friday-notes/
```

### Search with context
```bash
grep -rin "search query" ~/friday-notes/
```

## Create Notes

### Create a new note
```bash
cat > ~/friday-notes/$(date +%Y%m%d-%H%M%S)-note-title.md << 'EOF'
# Note Title

Note content goes here...
EOF
```

### Quick note with title
```bash
echo "# Quick Note Title" > ~/friday-notes/$(date +%Y%m%d-%H%M%S)-quick-note.md
echo "" >> ~/friday-notes/$(date +%Y%m%d-%H%M%S)-quick-note.md
echo "Note content here" >> ~/friday-notes/$(date +%Y%m%d-%H%M%S)-quick-note.md
```

### Append to existing note
```bash
echo "" >> ~/friday-notes/note-name.md
echo "Additional content" >> ~/friday-notes/note-name.md
```

## Edit Notes

### Edit with nano (simple)
```bash
nano ~/friday-notes/note-name.md
```

### Edit with vim
```bash
vim ~/friday-notes/note-name.md
```

## Delete Notes

### Delete a specific note
```bash
rm ~/friday-notes/note-name.md
```

### Move to trash (safer)
```bash
mkdir -p ~/friday-notes/.trash
mv ~/friday-notes/note-name.md ~/friday-notes/.trash/
```

## Organize Notes

### Create folders for categories
```bash
mkdir -p ~/friday-notes/work
mkdir -p ~/friday-notes/personal
mkdir -p ~/friday-notes/ideas
```

### Move note to folder
```bash
mv ~/friday-notes/note-name.md ~/friday-notes/work/
```

### List notes in folder
```bash
ls -la ~/friday-notes/work/
```

## Advanced

### Count total notes
```bash
find ~/friday-notes -name "*.md" -type f | wc -l
```

### Recent notes (last 7 days)
```bash
find ~/friday-notes -name "*.md" -type f -mtime -7
```

### Notes containing specific word
```bash
grep -l "important" ~/friday-notes/*.md
```

## Notes
- Linux-only (alternative to Apple Notes).
- Notes are stored as markdown files in `~/friday-notes/`.
- Supports any text editor for editing.
- Easy backup with `cp -r ~/friday-notes ~/backup/`.
