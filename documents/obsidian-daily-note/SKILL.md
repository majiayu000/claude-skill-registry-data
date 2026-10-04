---
name: obsidian-daily-note
description: Create or append to today's daily note in an Obsidian vault from the terminal. Adds timestamped sections to the right dated file without overwriting anything, creating the note with a date heading if it does not exist yet. Use when the user says "daily note", "log this to today", "add to my daily note", or "note this down".
---

# Obsidian Daily Note

Append a thought, log entry, or reminder to today's daily note in an Obsidian vault without leaving the terminal. The note is created if it does not exist, and existing content is never overwritten.

## Step 0: Find the vault (once)

Resolve the configuration in this order:

1. A `daily-note.config.md` file in the current project or its parents, with:

```
VAULT_PATH      Absolute path to the Obsidian vault root
NOTES_FOLDER    Folder for daily notes relative to the vault, e.g. "Daily" or "_Notes"
DATE_FORMAT     File name date format, default YYYY-MM-DD
```

2. If no config file exists: check whether the current directory (or a parent) contains a `.obsidian` folder. If so, that is the vault; read `.obsidian/daily-notes.json` for the folder and format if present.
3. Otherwise ask the user for vault path and notes folder, then offer to save the answers to `daily-note.config.md` for next time.

Never guess a vault path. Writing notes into the wrong directory is worse than asking once.

## Step 1: Build the file path

1. Get today's date from the current-date context (never from training data).
2. Build the path: `VAULT_PATH/NOTES_FOLDER/<date in DATE_FORMAT>.md`

## Step 2: Write

- If the file **does not exist**: create it with a `# <date>` heading, then the new section.
- If the file **already exists**: read it first, then append the new section at the end. Never overwrite or reorder existing content.

Section format:

```markdown
## <section title>

<the user's text>
```

Title rules:
- If the user separates a title from the body (for example with a `|`), use their title.
- If the text starts with an obvious label ("Meeting with X:", "Reminder:"), use that.
- Otherwise use `Note`.

Keep the user's text as written. Light cleanup (trim whitespace, fix an obvious typo the user flags) is fine; rewriting their words is not.

## Step 3: Confirm

Report what was written and the full file path, and whether the note was created or appended to.

## Rules

- Never overwrite existing daily note content. Append only.
- Never modify other notes in the vault.
- Do not add frontmatter unless the user's daily note template uses it (check an existing daily note for the pattern and match it).
- If a daily note template exists in the vault settings, follow its structure when creating a new note.
