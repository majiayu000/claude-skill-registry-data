---
name: vault-moc-manager
description: Create and maintain Maps of Content (MOCs) — find coverage gaps, generate a MOC for a topic cluster, and check which notes lack a hub. Use when the user says "make a MOC", "map of content", "organize this topic", or "which notes have no home". NOT for raw link repair/orphan hunting (use vault-link-index) or note creation (use vault-note-factory).
---

# MOC Manager

Helps create and maintain Maps of Content for better vault navigation.

## What is a MOC?

A **Map of Content** is an index note that links to related notes on a topic. It serves as a navigation hub.

```markdown
# Career MOC

## Job Search
- [[Resume]]
- [[Interview Prep]]
- [[Job Tracker]]

## Skills
- [[Python Learning]]
- [[Data Analysis]]
```

## Files

- **Script**: `80_Code/scripts/moc-manager.py`

## Naming Convention

MOCs use the `_` prefix:
- `_Career MOC.md`
- `_Health-Index.md`
- `_200 career MOC.md` (numbered for ordering)

## Commands

### Overview
```bash
python "80_Code/scripts/moc-manager.py"
```
Shows existing MOCs and folders that might need one.

### Find Gaps
```bash
python "80_Code/scripts/moc-manager.py" --gaps
```
Find folders with 5+ notes but no MOC.

### Find Stale MOCs
```bash
python "80_Code/scripts/moc-manager.py" --stale
```
Find MOCs that may need updates (fewer links than notes in folder).

### Generate MOC
```bash
python "80_Code/scripts/moc-manager.py" --generate "20_Areas/Health"
```
Generate MOC content for a folder (outputs to console, doesn't create file).

### Check Coverage
```bash
python "80_Code/scripts/moc-manager.py" --check "20_Areas/Career/_200 career MOC.md"
```
Check if MOC links to all notes in its folder.

## MOC Creation Workflow

When user asks to create a MOC:

1. **Run `--generate`** to get template content
2. **Show to user** for review
3. **Ask**: "Should I create this MOC at [path]?"
4. **Wait for confirmation**
5. **Create file** only after approval
6. **Suggest improvements** (add descriptions, group by theme)

## MOC Update Workflow

When user asks to update a MOC:

1. **Run `--check`** to find missing notes
2. **Show missing notes** to user
3. **Ask**: "Add these to the MOC?"
4. **Wait for confirmation**
5. **Edit MOC** to add new links

## MOC Best Practices

### Structure
```markdown
# Topic MOC

Brief description of what this covers.

## Category 1
- [[Note A]] - brief description
- [[Note B]]

## Category 2
- [[Note C]]

## Related
- [[Other MOC]]
```

### Guidelines
- Group notes by subtopic, not alphabetically
- Add brief descriptions for important notes
- Link to related MOCs
- Keep MOCs updated when adding new notes

## Obsidian CLI (MOC Analysis) — with Fallbacks

Try CLI first. Fall back to Glob/Grep/Read if Obsidian is unavailable.

```bash
OBS="bash 80_Code/scripts/obs.sh"

# What links TO a MOC? (shows notes that reference it)
$OBS backlinks file="_Career MOC"
# FALLBACK: Grep for '\[\[_Career MOC' across *.md

# What does a MOC link TO? (its coverage)
$OBS links file="_Career MOC"
$OBS links file="_Career MOC" total
# FALLBACK: Read the MOC file, extract [[...]] wikilinks

# List files in a folder (to compare against MOC coverage)
$OBS files folder="20_Areas/Career"
# FALLBACK: Glob for '20_Areas/Career/**/*.md'

# Find notes with a specific tag (alternative to MOC grouping)
$OBS tag name=career verbose
# FALLBACK: Grep for '#career' across *.md
```

**Workflow for MOC updates**: CLI `links` → CLI `files folder=X` → diff to find missing notes.
**Fallback workflow**: Read MOC → extract links → Glob folder → diff.

## Integration with Other Skills

- **vault-index**: Use CLI `backlinks` (or Grep fallback) to find notes that should be in MOC
- **knowledge-synthesis**: MOCs help find relevant notes faster
- **cleanup-studio**: Identify orphan notes that need MOC links

## When to Suggest MOCs

Claude Code should proactively suggest:
- "This folder has 15 notes but no MOC. Want me to create one?"
- "You just created 5 notes about Python. Should I add them to a Python MOC?"
- "The Health MOC is missing 8 recent notes. Want me to update it?"

## Example Interaction

```
User: Create a MOC for my health notes

Claude: Let me check what's in the Health folder.

[Runs --generate "20_Areas/Health"]

Here's a draft MOC:

# Health

## CBT Sessions
- [[2024-03-20 Anxiety]]
- [[2024-03-22 Anxiety]]
...

## Healing Logs
- [[2025-12-23-图书馆触发事件]]
...

Should I create this at `20_Areas/Health/_Health MOC.md`?
You can also tell me if you want to reorganize the sections.

User: Yes, but put CBT first

Claude: I'll create the MOC with CBT Sessions as the first section.
[Creates file]
Done! Created _Health MOC.md with 24 linked notes.
```


## Verify after writing

A MOC is a link hub — an unverified one silently rots.

1. Re-read the created/updated MOC. Every section has at least one entry; no placeholder headings left empty.
2. Run `python "80_Code/scripts/generate-link-index.py" --broken` — a MOC full of broken `[[links]]` is worse than no MOC. Fix every broken link you introduced.
3. Spot-check that the notes you linked actually exist and are the ones you meant (same name ≠ same note).

Report the MOC path + linked-note count. Never claim coverage you didn't check.
