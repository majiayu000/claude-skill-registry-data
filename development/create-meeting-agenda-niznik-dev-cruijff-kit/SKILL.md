---
name: create-meeting-agenda
description: Create weekly software meeting agenda in the wiki repo.
---

# Create Meeting Agenda

Create a new weekly software meeting agenda by copying the previous week's agenda and updating the wiki index.

## Wiki Repository Location

The wiki is located at: `/scratch/gpfs/MSALGANIK/niznik/GitHub/cruijff_kit_wiki/`

## Workflow

### 1. Pull Latest Wiki

```bash
cd /scratch/gpfs/MSALGANIK/niznik/GitHub/cruijff_kit_wiki
git pull
```

### 2. Find Most Recent Agenda

Look for the most recent `YYYY-MM-DD-SM.md` file in the wiki directory. Files use special unicode hyphens (‐ U+2010) not regular hyphens.

### 3. Determine New Meeting Date

- Ask the user for the meeting date if not provided
- Format: `YYYY-MM-DD` (e.g., `2025-12-02`)
- Meetings are typically on Tuesdays

### 4. Create New Agenda

1. Read the most recent agenda file
2. Create a new file with the new date: `YYYY‐MM‐DD‐SM.md` (using unicode hyphens ‐)
3. Copy contents exactly - do not modify

### 5. Update Software-Meetings.md

Add a new entry at the TOP of `Software-Meetings.md`:

```markdown
* [YYYY-MM-DD](https://github.com/niznik-dev/cruijff-kit/wiki/YYYY%E2%80%90MM%E2%80%90DD%E2%80%90SM)
```

Note: The URL uses `%E2%80%90` for each unicode hyphen (‐).

### 6. Commit and Push

```bash
cd /scratch/gpfs/MSALGANIK/niznik/GitHub/cruijff_kit_wiki
git add "YYYY‐MM‐DD‐SM.md" Software-Meetings.md
git commit -m "Add [DATE] meeting agenda

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

## Important Notes

- Always `git pull` first to avoid conflicts
- The agenda file uses unicode hyphens (‐ U+2010), not regular hyphens (-)
- Copy the previous agenda exactly without modifications - the user wants to see what was discussed last time
- The wiki repo is separate from the main cruijff_kit repo
